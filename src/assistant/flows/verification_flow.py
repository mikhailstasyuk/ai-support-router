from ..constants import RETRY_LIMIT_VERIFICATION


def verify(caller_profile: dict, provided_code: str | None, expected_code: str | None = "1234") -> tuple[bool, str]:
    if caller_profile.get("caller_type") != "policy_holder":
        return True, "not_required"
    if provided_code and provided_code == expected_code:
        caller_profile["verification_state"] = "verified"
        return True, "verified"
    caller_profile["verification_state"] = "failed"
    return False, "failed"


def register_failure_and_check(store, caller_id: str) -> tuple[int, bool]:
    failures = store.increment_verification_failure(caller_id)
    return failures, failures >= RETRY_LIMIT_VERIFICATION
