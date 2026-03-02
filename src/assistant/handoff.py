from .models import HandoffSummary


def build_handoff_summary(
    intent: str,
    caller_type: str,
    verification_outcome: str,
    collected_fields: dict,
    retry_count: int,
    blocker_reason: str,
    recommended_next_action: str,
) -> HandoffSummary:
    summary = HandoffSummary(
        intent=intent,
        caller_type=caller_type,
        verification_outcome=verification_outcome,
        collected_fields=collected_fields,
        retry_count=retry_count,
        blocker_reason=blocker_reason,
        recommended_next_action=recommended_next_action,
    )
    summary.validate()
    return summary


def pack_verification_failure_handoff(collected_fields: dict, retry_count: int) -> HandoffSummary:
    return build_handoff_summary(
        intent=collected_fields.get("intent", "unknown"),
        caller_type=collected_fields.get("caller_type", "unknown"),
        verification_outcome="failed",
        collected_fields=collected_fields,
        retry_count=retry_count,
        blocker_reason="verification_failed_max_attempts",
        recommended_next_action="continue verification via human agent",
    )
