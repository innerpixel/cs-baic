"""Render Jinja2 HTML templates to PDF bytes via weasyprint."""
from pathlib import Path
from datetime import date

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import weasyprint

TEMPLATES_DIR = Path(__file__).parent.parent / "pdf_templates"
CSS_PATH = TEMPLATES_DIR / "styles.css"

_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=True,
)


def render(template_name: str, context: dict) -> bytes:
    """Render template_name.html with context to PDF bytes.

    Always injects css_path and generated_date into the context.
    Raises TemplateNotFound if template_name is unknown.
    Raises RuntimeError if weasyprint encounters a fatal error.
    """
    try:
        template = _env.get_template(f"{template_name}.html")
    except TemplateNotFound:
        raise TemplateNotFound(f"PDF template not found: {template_name}")

    ctx = {
        "css_path": f"file://{CSS_PATH}",
        "generated_date": date.today().strftime("%d.%m.%Y"),
        **context,
    }
    html_str = template.render(**ctx)

    wp = weasyprint.HTML(string=html_str, base_url=str(TEMPLATES_DIR))
    pdf_bytes = wp.write_pdf()
    if not pdf_bytes:
        raise RuntimeError(f"weasyprint produced empty PDF for template {template_name}")
    return pdf_bytes
