from pydantic import BaseModel, field_validator


def _coerce_confidence(v: object) -> float | None:
    if v is None or isinstance(v, float):
        return v
    if isinstance(v, (int, str)):
        try:
            return float(v)
        except (ValueError, TypeError):
            pass
    return None


class DetectedEntities(BaseModel):
    company_names: list[str] = []
    people_names: list[str] = []
    dates: list[str] = []
    amounts: list[str] = []
    emails: list[str] = []


class Classification(BaseModel):
    document_type: str = "unknown"
    confidence: float | None = None
    reason: str | None = None
    language: str = "unknown"
    detected_entities: DetectedEntities = DetectedEntities()

    @field_validator("confidence", mode="before")
    @classmethod
    def coerce_confidence(cls, v: object) -> float | None:
        return _coerce_confidence(v)
