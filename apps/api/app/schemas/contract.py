from pydantic import BaseModel, field_validator


def _coerce_str_list(v: object) -> list[str]:
    """Flatten a list that may contain strings or dicts (LLM may return structured objects)."""
    if not isinstance(v, list):
        return []
    result = []
    for item in v:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, dict):
            # Join all string values from the dict into a readable sentence
            parts = [str(val) for val in item.values() if val is not None]
            result.append(": ".join(parts) if len(parts) > 1 else parts[0] if parts else "")
        else:
            result.append(str(item))
    return [s for s in result if s]


def _coerce_str_or_dict(v: object) -> str | None:
    if v is None or isinstance(v, str):
        return v
    if isinstance(v, dict):
        parts = [str(val) for val in v.values() if val is not None]
        return "; ".join(parts) if parts else None
    return str(v)


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
    def coerce_str_list(cls, v: object) -> list[str]:
        return _coerce_str_list(v)

    @field_validator("renewal_clause", mode="before")
    @classmethod
    def coerce_renewal(cls, v: object) -> str | None:
        return _coerce_str_or_dict(v)
