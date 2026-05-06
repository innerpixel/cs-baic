from typing import Any
from pydantic import BaseModel, field_validator


def _drop_nulls(v: object) -> list[str | dict[str, Any]]:
    if not isinstance(v, list):
        return []
    return [item for item in v if item is not None]


class AskAnswer(BaseModel):
    answer: str = ""
    source_documents: list[str | dict[str, Any]] = []
    confidence: str = "low"
    missing_information: list[str | dict[str, Any]] = []
    recommended_next_action: str | None = None
    requires_human_review: bool = False

    @field_validator("source_documents", "missing_information", mode="before")
    @classmethod
    def drop_nulls(cls, v: object) -> list[str | dict[str, Any]]:
        return _drop_nulls(v)
