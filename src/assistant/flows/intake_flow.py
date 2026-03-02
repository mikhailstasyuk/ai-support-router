from ..constants import Intent
from .clarification_flow import clarification_prompt, register_unresolved_attempt


def run_intake(utterance: str, agent, store, caller_id: str) -> dict:
    result = agent.resolve_intent(utterance)
    if result.intent == Intent.UNKNOWN:
        retries, should_handoff = register_unresolved_attempt(store, caller_id)
        if should_handoff:
            return {
                "intent": Intent.HANDOFF_TO_HUMAN,
                "response_type": "handoff",
                "spoken_message": "I could not determine your request. I will connect you to a human support agent.",
                "retry_count": retries,
            }
        return {
            "intent": Intent.UNKNOWN,
            "response_type": "clarification",
            "spoken_message": clarification_prompt(),
            "retry_count": retries,
        }
    store.reset_clarification(caller_id)
    return {
        "intent": result.intent,
        "response_type": "success",
        "spoken_message": f"I can help with {result.intent.value.replace('_', ' ')}.",
        "retry_count": 0,
    }
