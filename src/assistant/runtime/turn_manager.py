from __future__ import annotations

import re
from datetime import datetime

from ..constants import Intent
from .session_state import ConversationSessionState


class TurnManager:
    CODE_RE = re.compile(r"\b(\d{4})\b")
    VERIFICATION_CODE_RE = re.compile(
        r"(?:verification\s*code|code)\s*(?:is|:)?\s*(\d{4})\b", re.IGNORECASE
    )
    POLICY_RE = re.compile(r"\b(POL-\d{3,}|\bPN-\d{4}-\d{4,}\b)\b", re.IGNORECASE)
    SPOKEN_POLICY_RE = re.compile(
        r"\bp\s*o\s*l\s*(?:-|minus|dash|hyphen)\s*(\d{3,})\b",
        re.IGNORECASE,
    )
    DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
    NATURAL_DATE_RE = re.compile(
        r"\b("
        r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
        r"jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|"
        r"nov(?:ember)?|dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?(?:,\s*|\s+)\d{4}"
        r")\b",
        re.IGNORECASE,
    )
    PHONE_RE = re.compile(r"(\+?\d[\d\- ]{8,}\d)")
    DOCTOR_RE = re.compile(r"\bdr\.?\s+([a-z][a-z\-]*(?:\s+[a-z][a-z\-]*)?)\b", re.IGNORECASE)
    CLINIC_RE = re.compile(r"\b([a-z][a-z\-]*(?:\s+[a-z][a-z\-]*)*\sclinic)\b", re.IGNORECASE)
    SPECIALIZATIONS = {
        "cardiologist",
        "dermatologist",
        "neurologist",
        "orthopedist",
        "pediatrician",
        "oncologist",
        "gynecologist",
        "endocrinologist",
        "urologist",
        "therapist",
    }

    def infer_intent(self, session: ConversationSessionState) -> Intent | None:
        return session.pending_intent

    def extract_from_utterance(
        self,
        intent: Intent | None,
        utterance: str,
        existing_payload: dict | None = None,
    ) -> dict:
        payload = dict(existing_payload or {})
        text = utterance.strip()
        lower = text.lower()

        verification_code = self.VERIFICATION_CODE_RE.search(text)
        if verification_code:
            payload.setdefault("verification_code", verification_code.group(1))
        else:
            all_codes = self.CODE_RE.findall(text)
            if all_codes:
                # Prefer the last 4-digit token; early tokens often contain years (e.g. 2026).
                payload.setdefault("verification_code", all_codes[-1])

        policy = self.POLICY_RE.search(text)
        if policy:
            value = policy.group(1)
            if value.upper().startswith("POL-"):
                payload.setdefault("policy_id", value.upper())
            if value.upper().startswith("PN-"):
                payload.setdefault("policy_number", value.upper())
        elif "policy_id" not in payload:
            spoken_policy = self.SPOKEN_POLICY_RE.search(text)
            if spoken_policy:
                payload["policy_id"] = f"POL-{spoken_policy.group(1)}"

        date = self.DATE_RE.search(text)
        if date:
            payload.setdefault("preferred_date", date.group(1))
        elif "preferred_date" not in payload:
            natural_date = self.NATURAL_DATE_RE.search(text)
            normalized_date = self._normalize_natural_date(natural_date.group(1)) if natural_date else None
            if normalized_date:
                payload["preferred_date"] = normalized_date

        phone = self.PHONE_RE.search(text)
        if phone:
            payload.setdefault("phone_number", phone.group(1).replace(" ", ""))

        doctor = self.DOCTOR_RE.search(text)
        if doctor and "doctor_name" not in payload:
            payload["doctor_name"] = doctor.group(1).strip().title()
        elif "doctor " in lower and "doctor_name" not in payload:
            payload["doctor_name"] = text.split("doctor", 1)[-1].strip().title()

        clinic = self.CLINIC_RE.search(text)
        if clinic and "clinic" not in payload:
            payload["clinic"] = clinic.group(1).strip().title()
        elif "clinic " in lower and "clinic" not in payload:
            payload["clinic"] = text.split("clinic", 1)[-1].strip().title()

        if "specialization" in lower and "doctor_specialization" not in payload:
            payload["doctor_specialization"] = text.split("specialization", 1)[-1].strip().title()
        elif "doctor_specialization" not in payload:
            tokens = {token.strip(" ,.!?()").lower() for token in lower.split()}
            matched = sorted(tokens.intersection(self.SPECIALIZATIONS))
            if matched:
                payload["doctor_specialization"] = matched[0].title()

        if "callback" in lower:
            payload.setdefault("topic", "callback request")
            payload.setdefault("preferred_callback_window", "next available window")

        if "appeal" in lower and "appeal_reason" not in payload:
            payload["appeal_reason"] = text

        if intent == Intent.INQUIRE_PLANS:
            payload.setdefault("all_plans", True)

        if intent == Intent.CHANGE_CLINIC and "requested_clinic" not in payload and "clinic" in payload:
            payload["requested_clinic"] = payload["clinic"]

        return payload

    def _normalize_natural_date(self, raw_date: str) -> str | None:
        cleaned = re.sub(r"(\d)(st|nd|rd|th)\b", r"\1", raw_date.strip(), flags=re.IGNORECASE)
        for fmt in ("%B %d %Y", "%b %d %Y", "%B %d, %Y", "%b %d, %Y"):
            try:
                return datetime.strptime(cleaned, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return None
