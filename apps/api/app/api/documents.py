import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from app.db.models import AuditEvent, Document
from app.db.session import get_db
from app.schemas.documents import ApproveResponse, DocumentDetail, DocumentListItem
from app.services.analysis import run_analysis

router = APIRouter()

VALID_TYPES = {
    "supplier_invoice", "client_invoice", "contract",
    "supplier_offer", "client_request", "accountant_request",
    "hr_document", "internal_procedure", "price_list", "unknown",
}


@router.post("/documents", status_code=202)
def upload_document(
    text: str = Form(...),
    filename: str = Form(...),
    type: str = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
):
    if type not in VALID_TYPES:
        raise HTTPException(status_code=422, detail=f"Invalid document type: {type}")

    doc_id = uuid.uuid4()
    doc = Document(id=doc_id, filename=filename, type=type, raw_text=text, status="queued")
    db.add(doc)

    db.add(AuditEvent(
        document_id=doc_id,
        event_type="uploaded",
        event_data={"filename": filename, "type": type},
    ))
    db.commit()

    background_tasks.add_task(run_analysis, doc_id, db)
    return {"id": str(doc_id), "status": "queued"}


@router.get("/documents", response_model=list[DocumentListItem])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.created_at.desc()).all()


@router.get("/documents/{document_id}", response_model=DocumentDetail)
def get_document(document_id: uuid.UUID, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.post("/documents/{document_id}/approve", response_model=ApproveResponse)
def approve_document(document_id: uuid.UUID, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    now = datetime.now(timezone.utc)
    db.add(AuditEvent(
        document_id=document_id,
        event_type="approved",
        event_data={"approved_at": now.isoformat()},
    ))
    db.commit()
    return ApproveResponse(document_id=document_id, approved_at=now)
