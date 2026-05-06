"""Provider adapter for text embeddings.

Uses the same OpenAI-compat client pattern as app/services/llm.py.
Only this module imports the openai SDK for embedding calls.
"""
from openai import OpenAI
from app.core.config import settings

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_api_base_url,
        )
    return _client


def embed(text: str) -> list[float]:
    """Embed a single text string. Returns a flat list of floats."""
    response = _get_client().embeddings.create(
        model=settings.embedding_model,
        input=text,
    )
    return response.data[0].embedding


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts. Returns a list of embedding vectors."""
    if not texts:
        return []
    response = _get_client().embeddings.create(
        model=settings.embedding_model,
        input=texts,
    )
    # API returns results in order
    return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]
