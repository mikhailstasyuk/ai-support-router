from .template_engine import TemplateEngine


def build_verification_prompt(caller_name: str | None = None) -> str:
    engine = TemplateEngine()
    return engine.render("verification_prompt.j2", {"caller_name": caller_name or "caller"})
