import json
from typing import Any
from app.analyzers.base import AnalyzerResult
from app.services import llm as llm_service
from app.services.prompts import load_prompt, substitute
from app.schemas.extraction import InvoiceExtraction


class InvoiceExtractor:
    name = "invoice_extractor"
    version = "v1"
    applies_to: set[str] = {"supplier_invoice"}

    def run(self, document: Any) -> AnalyzerResult:
        template, prompt_name, prompt_version = load_prompt("invoice_extractor")
        prompt_input = substitute(template, {"DOCUMENT_TEXT": document.raw_text})

        try:
            raw_output = llm_service.complete(prompt_input)
            cleaned = _strip_markdown_fences(raw_output)
            data = json.loads(cleaned)
            parsed = InvoiceExtraction.model_validate(data)
            return AnalyzerResult(
                analyzer_name=prompt_name,
                analyzer_version=prompt_version,
                prompt_input=prompt_input,
                prompt_output_raw=raw_output,
                parsed_output=parsed,
                status="success",
            )
        except Exception as exc:
            return AnalyzerResult(
                analyzer_name=self.name,
                analyzer_version=self.version,
                prompt_input=prompt_input,
                prompt_output_raw="",
                parsed_output=None,
                status="failed",
                error_message=str(exc),
            )


def _strip_markdown_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        # drop first line (```json or ```) and last line (```)
        text = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])
    return text.strip()
