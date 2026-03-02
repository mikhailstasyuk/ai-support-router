from __future__ import annotations

import os
import json
import re
from dataclasses import dataclass

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - local fallback path
    OpenAI = None

from ..constants import Intent


@dataclass
class AgentReply:
    intent: Intent
    confidence: float
    message: str


class OpenAIAgent:
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.model = os.getenv("OPENAI_MODEL", model)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if (self.api_key and OpenAI is not None) else None

    def _heuristic_intent(self, text: str) -> Intent:
        t = text.lower()
        if "payment" in t:
            return Intent.UNKNOWN
        if "rebook" in t:
            return Intent.REBOOK_APPOINTMENT
        if "schedule" in t or "book" in t or "appointment" in t:
            return Intent.SCHEDULE_APPOINTMENT
        if "update appointment" in t:
            return Intent.UPDATE_APPOINTMENT
        if "cancel" in t and "appointment" in t:
            return Intent.CANCEL_APPOINTMENT
        if "renew" in t:
            return Intent.RENEW_POLICY
        if "plan" in t:
            return Intent.INQUIRE_PLANS
        if "clinic" in t:
            return Intent.CHANGE_CLINIC
        if "callback" in t or "call me" in t:
            return Intent.REQUEST_CALLBACK
        if "compensation" in t and "appeal" in t:
            return Intent.SUBMIT_COMPENSATION_APPEAL
        if "compensation" in t or "claim" in t:
            return Intent.CHECK_COMPENSATION_STATUS
        if "agent" in t or "human" in t:
            return Intent.HANDOFF_TO_HUMAN
        return Intent.UNKNOWN

    def resolve_intent(self, utterance: str) -> AgentReply:
        intent = self._heuristic_intent(utterance)
        if self.client is None:
            return AgentReply(intent=intent, confidence=0.55 if intent != Intent.UNKNOWN else 0.3, message="heuristic")

        prompt = (
            "Classify insurance support intent into one of: "
            "schedule_appointment, update_appointment, cancel_appointment, rebook_appointment, "
            "renew_policy, inquire_plans, change_clinic, request_callback, "
            "check_compensation_status, submit_compensation_appeal, handoff_to_human, unknown. "
            "Return JSON with keys intent, confidence, message."
        )
        try:
            resp = self.client.responses.create(
                model=self.model,
                input=[{"role": "system", "content": prompt}, {"role": "user", "content": utterance}],
                temperature=0,
            )
            text = (resp.output_text or "").strip()
            parsed_intent, parsed_conf = self._parse_structured_response(text)
            return AgentReply(intent=parsed_intent, confidence=parsed_conf, message="openai")
        except Exception:
            return AgentReply(intent=intent, confidence=0.4 if intent != Intent.UNKNOWN else 0.2, message="fallback")

    def next_step_message(self, summary: str) -> str:
        if self.client is None:
            return f"Next steps: {summary}"
        try:
            resp = self.client.responses.create(
                model=self.model,
                input=f"Write one short caller-facing next-step sentence: {summary}",
                temperature=0.2,
            )
            return resp.output_text.strip() or f"Next steps: {summary}"
        except Exception:
            return f"Next steps: {summary}"

    def _parse_structured_response(self, output_text: str) -> tuple[Intent, float]:
        if not output_text:
            return Intent.UNKNOWN, 0.2
        try:
            payload = json.loads(output_text)
            raw_intent = str(payload.get("intent", "")).strip().lower()
            confidence = float(payload.get("confidence", 0.7))
            try:
                return Intent(raw_intent), max(0.0, min(confidence, 1.0))
            except ValueError:
                return self._heuristic_intent(raw_intent), max(0.0, min(confidence, 1.0))
        except Exception:
            # Support responses where JSON is wrapped in prose.
            match = re.search(r"\{.*\}", output_text, re.DOTALL)
            if match:
                return self._parse_structured_response(match.group(0))
            return self._heuristic_intent(output_text), 0.7
