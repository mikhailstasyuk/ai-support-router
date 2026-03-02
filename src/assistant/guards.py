from .constants import Intent, SENSITIVE_INTENTS


def requires_verification(intent: Intent) -> bool:
    return intent in SENSITIVE_INTENTS


def is_verified(caller_profile: dict | None) -> bool:
    if not caller_profile:
        return False
    return caller_profile.get("verification_state") == "verified"
