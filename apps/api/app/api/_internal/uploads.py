"""Internal text upload endpoint — gated by ENABLE_INTERNAL_TEXT_UPLOAD env flag.

Only mounted when ENABLE_INTERNAL_TEXT_UPLOAD=true (default in dev, false in prod).
Used by eval harness and seed scripts via HTTP.
"""
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.db.models import AuditEvent, Document
from app.db.session import get_db
from app.services.analysis import run_analysis

router = APIRouter()

VALID_TYPES = {
    "supplier_invoice", "client_invoice", "contract",
    "supplier_offer", "client_request", "accountant_request",
    "hr_document", "internal_procedure", "price_list", "unknown",
}


@router.post("/_internal/uploads", status_code=202)
async def internal_upload(
    filename: str = Form(...),
    type: str = Form(default="unknown"),
    text: str | None = Form(None),
    file: UploadFile | None = File(None),
    source: str = Form(default="dev_source"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
):
    if type not in VALID_TYPES:
        raise HTTPException(status_code=422, detail=f"Invalid document type: {type}")

    if file is not None:
        raw = await file.read()
        raw_text = raw.decode("utf-8", errors="replace")
    elif text is not None:
        raw_text = text
    else:
        raise HTTPException(status_code=422, detail="Provide 'text' or a file.")

    doc_id = uuid.uuid4()
    doc = Document(
        id=doc_id,
        filename=filename,
        type=type,
        raw_text=raw_text,
        status="queued",
        source=source,
    )
    db.add(doc)
    db.add(AuditEvent(
        document_id=doc_id,
        event_type="uploaded",
        event_data={"filename": filename, "type": type, "source": source},
    ))
    db.commit()
    background_tasks.add_task(run_analysis, doc_id, db)
    return {"id": str(doc_id), "status": "queued"}
