from .constants import Intent

CLARIFICATION_WORD_LIMIT = 18
NEXT_STEP_WORD_LIMIT = 30


def require_fields(payload: dict, required: list[str]) -> list[str]:
    return [field for field in required if not payload.get(field)]


def required_fields_for_intent(intent: Intent) -> list[str]:
    mapping = {
        Intent.SCHEDULE_APPOINTMENT: ["policy_id", "preferred_date", "clinic"],
        Intent.UPDATE_APPOINTMENT: [],
        Intent.CANCEL_APPOINTMENT: [],
        Intent.REBOOK_APPOINTMENT: [],
        Intent.RENEW_POLICY: ["policy_number", "tariff_choice", "clinic_choice"],
        Intent.INQUIRE_PLANS: [],
        Intent.CHANGE_CLINIC: [],
        Intent.REQUEST_CALLBACK: ["topic", "phone_number", "preferred_callback_window"],
        Intent.CHECK_COMPENSATION_STATUS: ["policy_id"],
        Intent.SUBMIT_COMPENSATION_APPEAL: ["policy_id", "appeal_reason"],
    }
    return mapping.get(intent, [])


def validate_intent_payload(intent: Intent, payload: dict) -> list[str]:
    missing = require_fields(payload, required_fields_for_intent(intent))
    if intent == Intent.SCHEDULE_APPOINTMENT and not (
        payload.get("doctor_name") or payload.get("doctor_specialization")
    ):
        missing.append("doctor_name_or_specialization")
    if intent in {Intent.UPDATE_APPOINTMENT, Intent.CANCEL_APPOINTMENT}:
        # Missing appointment ID is allowed; flow can present recent matches.
        pass
    if intent == Intent.CHANGE_CLINIC and not (
        payload.get("clinic_name")
        or payload.get("requested_clinic")
        or payload.get("location")
        or payload.get("requested_location")
        or payload.get("nearby_metro")
        or payload.get("requested_metro")
    ):
        missing.append("clinic_name_or_location_or_nearby_metro")
    if intent == Intent.INQUIRE_PLANS and not (
        payload.get("plan_name") or payload.get("cost_range") or payload.get("all_plans")
    ):
        missing.append("plan_name_or_cost_range_or_all_plans")
    return missing


def word_count(text: str) -> int:
    return len([token for token in text.strip().split() if token])


def enforce_prompt_limit(text: str, limit: int) -> str:
    tokens = [token for token in text.strip().split() if token]
    if len(tokens) <= limit:
        return text
    return " ".join(tokens[:limit])


def enforce_clarification_limit(text: str) -> str:
    return enforce_prompt_limit(text, CLARIFICATION_WORD_LIMIT)


def enforce_next_step_limit(text: str) -> str:
    return enforce_prompt_limit(text, NEXT_STEP_WORD_LIMIT)


def normalize_response(response: dict) -> dict:
    normalized = {
        "response_type": response.get("response_type", "next_steps"),
        "spoken_message": response.get("spoken_message", ""),
        "next_expected_input": response.get("next_expected_input", "Anything else?"),
        "collected_fields_delta": response.get("collected_fields_delta", {}),
    }
    for key, value in response.items():
        if key not in normalized:
            normalized[key] = value
    normalized["spoken_message"] = normalized["spoken_message"].strip()
    return normalized
