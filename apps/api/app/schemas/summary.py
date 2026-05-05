from typing import Literal
from pydantic import BaseModel


class Summary(BaseModel):
    short_summary: str | None = None
    key_points: list[str] = []
    deadlines: list[str] = []
    amounts: list[str] = []
    obligations: list[str] = []
    missing_information: list[str] = []
    recommended_next_action: str | None = None
    urgency: Literal["low", "medium", "high", "unknown"] = "unknown"
