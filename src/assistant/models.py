from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CallerType(str, Enum):
    POLICY_HOLDER = "policy_holder"
    PROSPECTIVE_CUSTOMER = "prospective_customer"


class VerificationState(str, Enum):
    NOT_REQUIRED = "not_required"
    PENDING = "pending"
    VERIFIED = "verified"
    FAILED = "failed"
    ESCALATED = "escalated"


@dataclass
class CallerProfile:
    caller_id: str
    caller_type: CallerType | str
    phone_number: str | None = None
    verification_state: VerificationState | str = VerificationState.PENDING
    active_intent: str | None = None


@dataclass
class PolicyRecord:
    policy_id: str | None = None
    policy_number: str | None = None
    tariff_plan: str | None = None
    clinic: str | None = None
    eligibility_state: str = "unknown"


@dataclass
class AppointmentRequest:
    operation: str
    status: str = "initiated"
    preferred_date: str | None = None
    doctor_name: str | None = None
    doctor_specialization: str | None = None
    clinic: str | None = None
    appointment_id: str | None = None
    candidate_matches: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class RenewalRequest:
    policy_number: str
    tariff_choice: str
    clinic_choice: str
    status: str = "initiated"
    selected_tariff_plan: str | None = None
    selected_clinic: str | None = None


@dataclass
class PlanInquiry:
    inquiry_type: str
    status: str = "initiated"
    plan_name_filter: str | None = None
    cost_range_filter: str | None = None
    comparison_summary: str | None = None


@dataclass
class ClinicChangeRequest:
    request_mode: str
    eligibility_result: str = "unknown"
    status: str = "initiated"
    requested_clinic: str | None = None
    requested_location: str | None = None
    requested_metro: str | None = None
    alternatives: list[str] = field(default_factory=list)


@dataclass
class CallbackRequest:
    topic: str
    phone_number: str
    preferred_window: str
    status: str = "captured"
    policy_id: str | None = None


@dataclass
class CompensationCase:
    policy_id: str
    current_status: str
    appeal_requested: bool
    appeal_reason: str | None = None
    missing_items: list[str] = field(default_factory=list)
    next_steps: str | None = None


@dataclass
class HandoffSummary:
    intent: str
    caller_type: str
    verification_outcome: str
    collected_fields: dict[str, Any]
    retry_count: int
    blocker_reason: str
    recommended_next_action: str

    def validate(self) -> None:
        required_string_fields = (
            "intent",
            "caller_type",
            "verification_outcome",
            "blocker_reason",
            "recommended_next_action",
        )
        for key in required_string_fields:
            value = getattr(self, key)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"handoff summary requires non-empty string field: {key}")
        if not isinstance(self.collected_fields, dict):
            raise ValueError("handoff summary requires collected_fields as an object")
        if not isinstance(self.retry_count, int) or self.retry_count < 0:
            raise ValueError("handoff summary requires retry_count as non-negative integer")
