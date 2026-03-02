from .template_engine import TemplateEngine


def appointment_alternatives(clinic: str, alternatives: list[str]) -> str:
    return TemplateEngine().render(
        "appointment_alternative_offer.j2",
        {"clinic": clinic, "alternatives": "; ".join(alternatives)},
    )


def appointment_confirmation(appointment_id: str) -> str:
    return f"Appointment {appointment_id} is confirmed."


def appointment_candidate_prompt(matches: list[dict]) -> str:
    if not matches:
        return "I could not find matching appointments. I can connect you to a human agent."
    labels = []
    for match in matches[:3]:
        labels.append(f"{match.get('appointment_id', 'unknown')} on {match.get('date', 'unknown date')}")
    return "I found these appointments: " + "; ".join(labels) + ". Please choose one."
