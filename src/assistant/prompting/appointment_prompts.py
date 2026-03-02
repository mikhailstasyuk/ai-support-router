from .template_engine import TemplateEngine


def appointment_alternatives(clinic: str, alternatives: list[str]) -> str:
    return TemplateEngine().render(
        "appointment_alternative_offer.j2",
        {"clinic": clinic, "alternatives": alternatives},
    )


def appointment_confirmation(appointment_id: str) -> str:
    return TemplateEngine().render(
        "appointment_confirmation.j2",
        {"appointment_id": appointment_id},
    )


def appointment_candidate_prompt(matches: list[dict]) -> str:
    if not matches:
        return "I could not find matching appointments. I can connect you to a human agent."
    normalized = [
        {
            "appointment_id": match.get("appointment_id", "unknown"),
            "date": match.get("date", "unknown date"),
        }
        for match in matches[:3]
    ]
    return TemplateEngine().render(
        "appointment_candidate_offer.j2",
        {"matches": normalized},
    )
