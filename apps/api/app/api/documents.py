import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.models import AuditEvent, Document
from app.db.session import get_db
from app.schemas.documents import ApproveResponse, DocumentDetail, DocumentListItem
from app.services.analysis import run_analysis
from app.services.parsing import NoExtractableTextError, parse_pdf

router = APIRouter()

VALID_TYPES = {
    "supplier_invoice", "client_invoice", "contract",
    "supplier_offer", "client_request", "accountant_request",
    "hr_document", "internal_procedure", "price_list", "unknown",
}


@router.post("/documents", status_code=202)
async def upload_document(
    filename: str = Form(...),
    type: str = Form(...),
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
):
    if type not in VALID_TYPES:
        raise HTTPException(status_code=422, detail=f"Invalid document type: {type}")

    if file is not None and file.content_type == "application/pdf":
        file_bytes = await file.read()
        try:
            raw_text, _ = parse_pdf(file_bytes)
        except NoExtractableTextError:
            doc_id = uuid.uuid4()
            doc = Document(
                id=doc_id,
                filename=filename,
                type=type,
                raw_text="",
                status="not_supported_yet",
            )
            db.add(doc)
            db.add(AuditEvent(
                document_id=doc_id,
                event_type="ocr_required",
                event_data={"filename": filename, "reason": "image-only PDF, no extractable text"},
            ))
            db.commit()
            return {"id": str(doc_id), "status": "not_supported_yet"}
    elif file is not None and file.content_type in ("text/plain", "text/plain; charset=utf-8"):
        file_bytes = await file.read()
        raw_text = file_bytes.decode("utf-8", errors="replace")
    elif text is not None:
        raw_text = text
    else:
        raise HTTPException(status_code=422, detail="Provide either 'text' or a PDF/text 'file'.")

    doc_id = uuid.uuid4()
    doc = Document(id=doc_id, filename=filename, type=type, raw_text=raw_text, status="queued")
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
