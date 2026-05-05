from pydantic import BaseModel


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
