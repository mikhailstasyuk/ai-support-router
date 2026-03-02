from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateNotFound
except ImportError:  # pragma: no cover - local fallback path
    Environment = None
    FileSystemLoader = None
    StrictUndefined = None
    TemplateNotFound = FileNotFoundError

from .fallbacks import missing_variable_fallback


class TemplateEngine:
    def __init__(self, template_dir: str = "prompts") -> None:
        self.template_dir = template_dir
        self.env = None
        if Environment is not None:
            self.env = Environment(
                loader=FileSystemLoader(template_dir),
                undefined=StrictUndefined,
                autoescape=False,
                trim_blocks=True,
                lstrip_blocks=True,
            )

    def render(self, template_name: str, variables: dict) -> str:
        try:
            if self.env is not None:
                template = self.env.get_template(template_name)
                return template.render(**variables).strip()
            # Simple fallback renderer when jinja2 is not installed.
            raw = Path(self.template_dir, template_name).read_text(encoding="utf-8")
            rendered = raw
            for key, value in variables.items():
                rendered = rendered.replace(f"{{{{ {key} }}}}", str(value))
                rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
            if "{{" in rendered and "}}" in rendered:
                raise ValueError("unresolved template variable(s)")
            return rendered.strip()
        except TemplateNotFound:
            return f"Template not found: {template_name}. Please continue with a human agent."
        except Exception as exc:
            return missing_variable_fallback(str(exc), variables)

    @staticmethod
    def required_templates() -> list[str]:
        return [
            "intent_clarification.j2",
            "verification_prompt.j2",
            "appointment_alternative_offer.j2",
            "clinic_alternative_offer.j2",
            "missing_information_next_steps.j2",
            "handoff_summary.j2",
        ]

    def validate_templates(self) -> list[str]:
        missing = []
        for template in self.required_templates():
            if not Path("prompts", template).exists():
                missing.append(template)
        return missing
