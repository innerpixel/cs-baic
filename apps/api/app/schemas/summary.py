from typing import Literal
from pydantic import BaseModel, field_validator


def _clean_str_list(v: object) -> list[str]:
    if not isinstance(v, list):
        return []
    return [str(item) for item in v if item is not None]


class Summary(BaseModel):
    short_summary: str | None = None
    key_points: list[str] = []
    deadlines: list[str] = []
    amounts: list[str] = []
    obligations: list[str] = []
    missing_information: list[str] = []
    recommended_next_action: str | None = None
    urgency: Literal["low", "medium", "high", "unknown"] = "unknown"

    @field_validator(
        "key_points", "deadlines", "amounts", "obligations", "missing_information",
        mode="before",
    )
    @classmethod
    def clean_str_list(cls, v: object) -> list[str]:
        return _clean_str_list(v)
