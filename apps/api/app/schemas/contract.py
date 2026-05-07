from pydantic import BaseModel, field_validator


def _to_str(item: object) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        # prefer a description/name field; fallback to joining all string values
        for key in ("description", "name", "term", "clause", "text"):
            if key in item and isinstance(item[key], str):
                return item[key]
        return " · ".join(str(v) for v in item.values() if v is not None)
    return str(item)


def _drop_nulls(v: object) -> list[str]:
    if not isinstance(v, list):
        return []
    return [_to_str(item) for item in v if item is not None]


class ContractReview(BaseModel):
    contract_type: str | None = None
    parties: list[str] = []
    start_date: str | None = None
    end_date: str | None = None
    payment_terms: list[str] = []
    obligations: list[str] = []
    termination_terms: list[str] = []
    penalties: list[str] = []
    renewal_clause: str | None = None
    important_dates: list[str] = []
    risk_flags: list[str] = []
    questions_for_human_review: list[str] = []
    plain_language_summary: str | None = None
    recommended_next_action: str | None = None

    @field_validator(
        "parties", "payment_terms", "obligations", "termination_terms",
        "penalties", "important_dates", "risk_flags", "questions_for_human_review",
        mode="before",
    )
    @classmethod
    def drop_nulls(cls, v: object) -> list[str]:
        return _drop_nulls(v)
