"""Ask My Company — synchronous RAG orchestrator."""
import hashlib
import json
import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from app.db.models import PromptRun
from app.schemas.ask import AskAnswer
from app.services.embeddings import embed
from app.services.llm import complete, strip_json_fences
from app.services.retrieval import top_k

_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "ask_company_v1.txt"
_PROMPT_TEMPLATE: str | None = None


def _load_prompt() -> str:
    global _PROMPT_TEMPLATE
    if _PROMPT_TEMPLATE is None:
        _PROMPT_TEMPLATE = _PROMPT_PATH.read_text(encoding="utf-8")
    return _PROMPT_TEMPLATE


def _format_context(hits) -> str:
    if not hits:
        return "(No relevant documents found in your company knowledge base.)"
    parts = []
    for hit in hits:
        parts.append(f"[{hit.filename}]\n{hit.content}")
    return "\n\n---\n\n".join(parts)


def _enrich_sources(sources: list, filename_to_id: dict[str, str]) -> list:
    """Replace filename strings with {doc_id, filename} dicts when ID is known."""
    enriched = []
    for src in sources:
        if isinstance(src, str) and src in filename_to_id:
            enriched.append({"doc_id": filename_to_id[src], "filename": src})
        else:
            enriched.append(src)
    return enriched


def answer_question(query: str, db: Session) -> AskAnswer:
    """Embed query → top-K retrieval → LLM call → parse AskAnswer → save PromptRun."""
    prompt_template = _load_prompt()

    query_embedding = embed(query)
    hits = top_k(db, query_embedding, k=5)
    context = _format_context(hits)

    # Build a filename → doc_id map from retrieved hits for source linking
    filename_to_id: dict[str, str] = {h.filename: str(h.document_id) for h in hits}

    prompt = (
        prompt_template
        .replace("{{USER_QUESTION}}", query)
        .replace("{{RETRIEVED_CONTEXT}}", context)
    )

    raw_output = complete(prompt)

    try:
        data = json.loads(strip_json_fences(raw_output))
        answer = AskAnswer(**data)
    except Exception:
        answer = AskAnswer(
            answer=raw_output or "Could not parse answer.",
            confidence="low",
            requires_human_review=True,
        )

    # Enrich sources with doc IDs for deep-linking
    answer.source_documents = _enrich_sources(answer.source_documents, filename_to_id)

    status = "success"
    error_msg = None

    prompt_run = PromptRun(
        id=uuid.uuid4(),
        document_id=None,
        prompt_name="ask_company",
        prompt_version="v1",
        model=__import__("app.core.config", fromlist=["settings"]).settings.llm_model,
        input_text=prompt,
        input_hash=hashlib.sha256(prompt.encode()).hexdigest(),
        output_json=answer.model_dump(),
        status=status,
        error_message=error_msg,
    )
    db.add(prompt_run)
    db.commit()

    return answer
