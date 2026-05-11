"""Public upload endpoint — accepts PDF and ZIP only.

POST /api/uploads
  application/pdf  → validate + ingest → 200 {document_id, status}
  application/zip  → extract + ingest each PDF → 200 {batch_id, documents:[...]}
  text/plain       → 415 (use /api/_internal/uploads for text)
"""
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.documents import BatchUploadResponse, UploadResponse
from app.services.analysis import run_analysis
from app.services.upload_intake import extract_zip, ingest_pdf, validate_pdf

router = APIRouter()

_PDF_TYPES = {"application/pdf", "application/octet-stream"}
_ZIP_TYPES = {"application/zip", "application/x-zip-compressed"}


@router.post("/uploads", status_code=200)
async def upload_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
):
    content_type = (file.content_type or "").split(";")[0].strip()
    filename = file.filename or "upload"

    if content_type in ("text/plain",) or filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=415,
            detail="Text upload is not supported on this endpoint. Use the internal endpoint or upload a PDF or ZIP.",
        )

    file_bytes = await file.read()
    is_pdf = content_type in _PDF_TYPES or filename.lower().endswith(".pdf")
    is_zip = content_type in _ZIP_TYPES or filename.lower().endswith(".zip")

    if is_pdf:
        validate_pdf(file_bytes, filename)
        doc_id = ingest_pdf(filename, file_bytes, db, doc_type="unknown", source="public")
        background_tasks.add_task(run_analysis, doc_id, db)
        return UploadResponse(document_id=str(doc_id), status="queued")

    if is_zip:
        pdf_entries = extract_zip(file_bytes)
        if not pdf_entries:
            raise HTTPException(status_code=400, detail="ZIP contains no PDF files")
        batch_id = uuid.uuid4()
        results = []
        for pdf_name, pdf_bytes in pdf_entries:
            doc_id = ingest_pdf(pdf_name, pdf_bytes, db, doc_type="unknown", source="public", batch_id=batch_id)
            background_tasks.add_task(run_analysis, doc_id, db)
            results.append(UploadResponse(document_id=str(doc_id), status="queued"))
        return BatchUploadResponse(batch_id=str(batch_id), documents=results)

    raise HTTPException(
        status_code=415,
        detail=f"Unsupported file type: {content_type or filename}. Upload a PDF or ZIP file.",
    )
