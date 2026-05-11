import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session
from typing import Optional

from app.db.models import AuditEvent, Document
from app.db.session import get_db
from app.schemas.documents import (
    ApproveResponse, DocumentDetail, DocumentListItem,
    ReviewStateRequest, ReviewStateResponse,
)
from app.services.analysis import run_analysis
from app.services.parsing import NoExtractableTextError, parse_pdf

router = APIRouter()

VALID_REVIEW_STATES = {"pending", "approved", "rejected", "needs_review"}


@router.get("/documents", response_model=list[DocumentListItem])
def list_documents(
    include_dev: bool = Query(default=False),
    db: Session = Depends(get_db),
):
    q = db.query(Document)
    if not include_dev:
        q = q.filter((Document.source != "dev_source") | (Document.source.is_(None)))
    return q.order_by(Document.created_at.desc()).all()


@router.get("/documents/{document_id}", response_model=DocumentDetail)
def get_document(document_id: uuid.UUID, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.get("/documents/{document_id}/pdf")
def get_document_pdf(document_id: uuid.UUID, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if not doc.pdf_path:
        raise HTTPException(status_code=404, detail="No PDF stored for this document")
    pdf_path = Path(doc.pdf_path)
    if not pdf_path.exists():
        raise HTTPException(status_code=410, detail="PDF file missing from storage — reseed or re-upload")
    content = pdf_path.read_bytes()
    return Response(content=content, media_type="application/pdf")


@router.patch("/documents/{document_id}/review_state", response_model=ReviewStateResponse)
def set_review_state(
    document_id: uuid.UUID,
    body: ReviewStateRequest,
    db: Session = Depends(get_db),
):
    if body.state not in VALID_REVIEW_STATES:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid review state: {body.state!r}. Must be one of {sorted(VALID_REVIEW_STATES)}",
        )
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    old_state = doc.review_state or "pending"
    doc.review_state = body.state
    doc.review_note = body.note

    db.add(AuditEvent(
        document_id=document_id,
        event_type=f"review_state_changed:{old_state}→{body.state}",
        event_data={"old": old_state, "new": body.state, "note": body.note},
    ))
    db.commit()
    db.refresh(doc)
    return ReviewStateResponse(
        document_id=doc.id,
        review_state=doc.review_state,
        review_note=doc.review_note,
    )


@router.post("/documents/{document_id}/approve", response_model=ApproveResponse)
def approve_document(document_id: uuid.UUID, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    now = datetime.now(timezone.utc)
    doc.review_state = "approved"
    db.add(AuditEvent(
        document_id=document_id,
        event_type="approved",
        event_data={"approved_at": now.isoformat()},
    ))
    db.commit()
    return ApproveResponse(document_id=document_id, approved_at=now)
