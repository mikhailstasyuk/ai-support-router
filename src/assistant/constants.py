from enum import Enum


class Intent(str, Enum):
    SCHEDULE_APPOINTMENT = "schedule_appointment"
    UPDATE_APPOINTMENT = "update_appointment"
    CANCEL_APPOINTMENT = "cancel_appointment"
    REBOOK_APPOINTMENT = "rebook_appointment"
    RENEW_POLICY = "renew_policy"
    INQUIRE_PLANS = "inquire_plans"
    CHANGE_CLINIC = "change_clinic"
    REQUEST_CALLBACK = "request_callback"
    CHECK_COMPENSATION_STATUS = "check_compensation_status"
    SUBMIT_COMPENSATION_APPEAL = "submit_compensation_appeal"
    HANDOFF_TO_HUMAN = "handoff_to_human"
    UNKNOWN = "unknown"


class ResponseType(str, Enum):
    SUCCESS = "success"
    CLARIFICATION = "clarification"
    ALTERNATIVE_OFFER = "alternative_offer"
    NEXT_STEPS = "next_steps"
    HANDOFF = "handoff"


SENSITIVE_INTENTS = {
    Intent.SCHEDULE_APPOINTMENT,
    Intent.UPDATE_APPOINTMENT,
    Intent.CANCEL_APPOINTMENT,
    Intent.REBOOK_APPOINTMENT,
    Intent.RENEW_POLICY,
    Intent.CHANGE_CLINIC,
    Intent.CHECK_COMPENSATION_STATUS,
    Intent.SUBMIT_COMPENSATION_APPEAL,
}

RETRY_LIMIT_CLARIFICATION = 2
RETRY_LIMIT_VERIFICATION = 3
RETRY_LIMIT_STT = 2
