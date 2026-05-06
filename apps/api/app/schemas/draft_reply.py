from typing import Any
from pydantic import BaseModel, field_validator


def _drop_nulls(v: object) -> list[str | dict[str, Any]]:
    if not isinstance(v, list):
        return []
    return [item for item in v if item is not None]


class DraftReply(BaseModel):
    detected_language: str = "unknown"
    reply_subject: str = ""
    reply_body: str = ""
    assumptions: list[str | dict[str, Any]] = []
    missing_information: list[str | dict[str, Any]] = []
    human_review_required: bool = True
    recommended_next_action: str | None = None

    @field_validator("assumptions", "missing_information", mode="before")
    @classmethod
    def drop_nulls(cls, v: object) -> list[str | dict[str, Any]]:
        return _drop_nulls(v)
