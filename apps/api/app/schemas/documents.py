import uuid
from datetime import datetime
from pydantic import BaseModel


class DocumentUpload(BaseModel):
    text: str
    filename: str
    type: str


class DocumentListItem(BaseModel):
    id: uuid.UUID
    filename: str
    type: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AuditEventOut(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID | None
    event_type: str
    event_data: dict
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalysisOut(BaseModel):
    id: uuid.UUID
    fields: dict | None
    missing_fields: list | None
    risk_flags: list | None
    summary: str | None
    suggested_action: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class DocumentDetail(BaseModel):
    id: uuid.UUID
    filename: str
    type: str
    status: str
    created_at: datetime
    analysis: AnalysisOut | None
    audit_events: list[AuditEventOut]

    model_config = {"from_attributes": True}


class ApproveResponse(BaseModel):
    document_id: uuid.UUID
    approved_at: datetime
