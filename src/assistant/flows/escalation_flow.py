from ..handoff import build_handoff_summary


def escalate_to_human(intent: str, caller_type: str, collected_fields: dict, retry_count: int, blocker_reason: str) -> dict:
    summary = build_handoff_summary(
        intent=intent,
        caller_type=caller_type,
        verification_outcome=collected_fields.get("verification_state", "unknown"),
        collected_fields=collected_fields,
        retry_count=retry_count,
        blocker_reason=blocker_reason,
        recommended_next_action="human agent continuation",
    )
    return {
        "response_type": "handoff",
        "spoken_message": "I will connect you to a human support agent now.",
        "collected_fields_delta": {},
        "next_expected_input": "Please wait while I transfer your call.",
        "handoff_summary": summary.__dict__,
    }


def stt_repeat_then_handoff(repeat_attempt: int) -> dict:
    if repeat_attempt == 1:
        return {
            "response_type": "clarification",
            "spoken_message": "I could not hear that clearly. Please repeat your request once.",
            "next_expected_input": "Repeat request",
            "collected_fields_delta": {},
        }
    return {
        "response_type": "handoff",
        "spoken_message": "I still cannot understand the audio input. I can transfer you to a human agent now.",
        "next_expected_input": "Say transfer",
        "collected_fields_delta": {},
    }


def handoff_unavailable_fallback() -> dict:
    return {
        "response_type": "next_steps",
        "spoken_message": "Our live transfer queue is unavailable. I can record a callback request now or share next steps.",
        "next_expected_input": "Provide callback phone and time window",
        "collected_fields_delta": {},
    }
