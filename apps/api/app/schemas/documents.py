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
    source: str | None
    review_state: str | None
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
    detected_type: str | None
    confidence: float | None
    language: str | None
    urgency: str | None
    analyzer_outputs: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}


class DocumentDetail(BaseModel):
    id: uuid.UUID
    filename: str
    type: str
    status: str
    source: str | None
    review_state: str | None
    review_note: str | None
    batch_id: uuid.UUID | None
    pdf_path: str | None
    created_at: datetime
    analysis: AnalysisOut | None
    audit_events: list[AuditEventOut]

    model_config = {"from_attributes": True}


class ApproveResponse(BaseModel):
    document_id: uuid.UUID
    approved_at: datetime


class ReviewStateRequest(BaseModel):
    state: str
    note: str | None = None


class ReviewStateResponse(BaseModel):
    document_id: uuid.UUID
    review_state: str
    review_note: str | None

    model_config = {"from_attributes": True}


class UploadResponse(BaseModel):
    document_id: str
    status: str


class BatchUploadResponse(BaseModel):
    batch_id: str
    documents: list[UploadResponse]
