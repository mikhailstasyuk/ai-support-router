def llm_unavailable_fallback() -> dict:
    return {
        "response_type": "next_steps",
        "fallback_type": "llm_unavailable",
        "spoken_message": "I cannot access automated reasoning right now. I can connect you to a human agent immediately.",
        "next_expected_input": "Say transfer to continue",
        "collected_fields_delta": {},
        "handoff_offer": True,
    }


def tts_unavailable_fallback() -> dict:
    return {
        "response_type": "next_steps",
        "fallback_type": "voice_unavailable",
        "spoken_message": "Voice output is limited right now. I can continue with fallback speech or transfer you.",
        "next_expected_input": "Say continue or transfer",
        "collected_fields_delta": {},
        "handoff_offer": True,
    }
