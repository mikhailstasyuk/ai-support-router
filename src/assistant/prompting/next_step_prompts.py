from .template_engine import TemplateEngine


def missing_info_prompt(intent: str, missing_items: list[str]) -> str:
    return TemplateEngine().render(
        "missing_information_next_steps.j2",
        {"intent": intent, "missing_items": missing_items},
    )
