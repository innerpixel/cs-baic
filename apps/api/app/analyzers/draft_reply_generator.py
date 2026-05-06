"""DraftReplyGenerator: drafts a reply email using RAG-retrieved company context.

Retrieves top-3 chunks from OTHER documents (excludes this document's own chunks)
so the draft is grounded in existing company knowledge without circular reference.
"""
import json
from pathlib import Path

from app.analyzers.base import AnalyzerResult
from app.db.session import SessionLocal
from app.schemas.draft_reply import DraftReply
from app.services.embeddings import embed
from app.services.llm import complete
from app.services.retrieval import top_k

_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "email_reply_draft_v1.txt"
_PROMPT_TEMPLATE: str | None = None


def _load_prompt() -> str:
    global _PROMPT_TEMPLATE
    if _PROMPT_TEMPLATE is None:
        _PROMPT_TEMPLATE = _PROMPT_PATH.read_text(encoding="utf-8")
    return _PROMPT_TEMPLATE


def _format_context(hits) -> str:
    if not hits:
        return "(No relevant company context found.)"
    parts = [f"[{hit.filename}]\n{hit.content}" for hit in hits]
    return "\n\n---\n\n".join(parts)


class DraftReplyGenerator:
    name = "draft_reply_generator"
    version = "v1"
    applies_to = {"client_request"}

    def run(self, document) -> AnalyzerResult:
        raw_text: str = document.raw_text or ""
        prompt_template = _load_prompt()

        try:
            query_embedding = embed(raw_text)

            db = SessionLocal()
            try:
                hits = top_k(db, query_embedding, k=3, exclude_document_ids=[document.id])
            finally:
                db.close()

            context = _format_context(hits)
            prompt = (
                prompt_template
                .replace("{{EMAIL_TEXT}}", raw_text)
                .replace("{{COMPANY_CONTEXT}}", context)
            )

            raw_output = complete(prompt)

            try:
                data = json.loads(raw_output)
                draft = DraftReply(**data)
                status = "success"
                error_msg = None
            except Exception as parse_exc:
                return AnalyzerResult(
                    analyzer_name=self.name,
                    analyzer_version=self.version,
                    prompt_input=prompt,
                    prompt_output_raw=raw_output,
                    parsed_output=None,
                    status="failed",
                    error_message=f"Parse error: {parse_exc}",
                )

            return AnalyzerResult(
                analyzer_name=self.name,
                analyzer_version=self.version,
                prompt_input=prompt,
                prompt_output_raw=raw_output,
                parsed_output=draft,
                status=status,
                error_message=error_msg,
            )

        except Exception as exc:
            return AnalyzerResult(
                analyzer_name=self.name,
                analyzer_version=self.version,
                prompt_input=raw_text[:200],
                prompt_output_raw="",
                parsed_output=None,
                status="failed",
                error_message=str(exc)[:400],
            )
