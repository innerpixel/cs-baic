from typing import Any
from pydantic import BaseModel, field_validator


def _drop_nulls(v: object) -> list[str | dict[str, Any]]:
    """Accept a list of strings or dicts; drop None elements; preserve LLM structure."""
    if not isinstance(v, list):
        return []
    return [item for item in v if item is not None]


class ContractReview(BaseModel):
    contract_type: str | None = None
    parties: list[str | dict[str, Any]] = []
    start_date: str | None = None
    end_date: str | None = None
    payment_terms: list[str | dict[str, Any]] = []
    obligations: list[str | dict[str, Any]] = []
    termination_terms: list[str | dict[str, Any]] = []
    penalties: list[str | dict[str, Any]] = []
    renewal_clause: str | dict[str, Any] | None = None
    important_dates: list[str | dict[str, Any]] = []
    risk_flags: list[str | dict[str, Any]] = []
    questions_for_human_review: list[str | dict[str, Any]] = []
    plain_language_summary: str | None = None
    recommended_next_action: str | None = None

    @field_validator(
        "parties", "payment_terms", "obligations", "termination_terms",
        "penalties", "important_dates", "risk_flags", "questions_for_human_review",
        mode="before",
    )
    @classmethod
    def drop_nulls(cls, v: object) -> list[str | dict[str, Any]]:
        return _drop_nulls(v)
