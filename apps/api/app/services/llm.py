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


def strip_json_fences(text: str) -> str:
    """Remove markdown code fences (```json ... ```) that some LLMs add around JSON output."""
    text = text.strip()
    if text.startswith("```"):
        # Drop opening fence line
        text = text[text.index("\n") + 1:] if "\n" in text else text
        # Drop closing fence
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3].rstrip()
    return text.strip()


def complete(prompt: str, model: str | None = None) -> str:
    client = _get_client()
    response = client.chat.completions.create(
        model=model or settings.llm_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    content = response.choices[0].message.content
    return content or ""
