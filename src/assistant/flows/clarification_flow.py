from ..constants import RETRY_LIMIT_CLARIFICATION
from ..validation import enforce_clarification_limit


def clarification_prompt() -> str:
    return enforce_clarification_limit("Could you say that in one short sentence about what you need today?")


def register_unresolved_attempt(store, caller_id: str) -> tuple[int, bool]:
    retries = store.increment_clarification(caller_id)
    return retries, retries >= RETRY_LIMIT_CLARIFICATION
