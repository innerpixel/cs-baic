"""Paragraph-based document chunker.

Splits on blank lines (\\n\\n). Chunks longer than MAX_CHARS are split
further at sentence boundaries. Documents that are one paragraph become
one chunk.
"""
import re

MIN_CHARS = 50
MAX_CHARS = 1000
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def chunk_paragraph(text: str) -> list[str]:
    """Return a list of content chunks for the given text."""
    raw = re.split(r"\n\s*\n", text)
    chunks: list[str] = []
    for block in raw:
        block = block.strip()
        if not block:
            continue
        if len(block) <= MAX_CHARS:
            chunks.append(block)
        else:
            # Sentence-split long paragraphs
            sentences = _SENTENCE_SPLIT.split(block)
            current: list[str] = []
            current_len = 0
            for sent in sentences:
                sent = sent.strip()
                if not sent:
                    continue
                if current_len + len(sent) > MAX_CHARS and current:
                    chunks.append(" ".join(current))
                    current = [sent]
                    current_len = len(sent)
                else:
                    current.append(sent)
                    current_len += len(sent) + 1
            if current:
                chunks.append(" ".join(current))
    # Drop very short fragments that add no retrieval value
    return [c for c in chunks if len(c) >= MIN_CHARS]
