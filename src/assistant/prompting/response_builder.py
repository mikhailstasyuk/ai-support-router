from .template_engine import TemplateEngine


def build_response(template: str, variables: dict, voice_adapter) -> dict:
    engine = TemplateEngine()
    text = engine.render(template, variables)
    voice = voice_adapter.synthesize(text)
    if not voice.get("ok"):
        return {
            "response_type": "next_steps",
            "spoken_message": voice["text"],
            "next_expected_input": "Say continue or transfer",
            "collected_fields_delta": {},
        }
    return {
        "response_type": "success",
        "spoken_message": text,
        "next_expected_input": "Provide next detail",
        "collected_fields_delta": {},
    }
