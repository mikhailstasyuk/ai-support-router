from .template_engine import TemplateEngine


def renewal_confirmation(renewal_id: str) -> str:
    return f"Your renewal request {renewal_id} is submitted."


def plan_summary_response(summary: str) -> str:
    return summary


def clinic_alternatives(requested: str, alternatives: list[str]) -> str:
    return TemplateEngine().render(
        "clinic_alternative_offer.j2",
        {"requested_clinic": requested, "alternatives": ", ".join(alternatives)},
    )
