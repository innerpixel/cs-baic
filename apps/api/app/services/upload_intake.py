"""PDF and ZIP intake: validation, storage, and document creation.

Public surface:
    validate_pdf(file_bytes, filename) -> None           raises HTTPException on bad input
    extract_zip(zip_bytes) -> list[(filename, bytes)]    raises HTTPException on bad input
    persist_pdf(doc_id, pdf_bytes) -> str                returns storage path
    ingest_pdf(filename, pdf_bytes, db, ...) -> UUID     creates Document row, persists bytes
"""
import io
import uuid
import zipfile
from pathlib import Path

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import AuditEvent, Document
from app.services.parsing import NoExtractableTextError, parse_pdf

STORAGE_DIR = Path(__file__).parent.parent.parent / "var" / "storage"
PDF_MAX_BYTES = 5 * 1024 * 1024   # 5 MB
ZIP_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
ZIP_MAX_PDFS = 20
PDF_MAGIC = b"%PDF"


def validate_pdf(file_bytes: bytes, filename: str) -> None:
    if len(file_bytes) > PDF_MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"PDF too large: {filename} is {len(file_bytes)//1024} kB, max 5 MB",
        )
    if not file_bytes.startswith(PDF_MAGIC):
        raise HTTPException(
            status_code=415,
            detail=f"File does not appear to be a valid PDF: {filename}",
        )


def extract_zip(zip_bytes: bytes) -> list[tuple[str, bytes]]:
    if len(zip_bytes) > ZIP_MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"ZIP too large: {len(zip_bytes)//1024} kB, max 10 MB",
        )
    try:
        zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    except zipfile.BadZipFile:
        raise HTTPException(status_code=415, detail="Not a valid ZIP file")

    pdf_entries = [n for n in zf.namelist() if n.lower().endswith(".pdf") and not n.startswith("__MACOSX")]
    if len(pdf_entries) > ZIP_MAX_PDFS:
        raise HTTPException(
            status_code=400,
            detail=f"ZIP contains {len(pdf_entries)} PDFs, max allowed is {ZIP_MAX_PDFS}",
        )

    results = []
    for name in pdf_entries:
        data = zf.read(name)
        fname = Path(name).name
        if len(data) > PDF_MAX_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"PDF inside ZIP too large: {fname} is {len(data)//1024} kB, max 5 MB",
            )
        if not data.startswith(PDF_MAGIC):
            raise HTTPException(
                status_code=415,
                detail=f"File inside ZIP is not a valid PDF: {fname}",
            )
        results.append((fname, data))

    return results


def persist_pdf(doc_id: uuid.UUID, pdf_bytes: bytes) -> str:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    path = STORAGE_DIR / f"{doc_id}.pdf"
    path.write_bytes(pdf_bytes)
    return str(path)


def ingest_pdf(
    filename: str,
    pdf_bytes: bytes,
    db: Session,
    doc_type: str = "unknown",
    source: str = "public",
    batch_id: uuid.UUID | None = None,
) -> uuid.UUID:
    """Create a Document from PDF bytes.

    - Persists PDF to var/storage/<doc_id>.pdf
    - Extracts raw_text via pdfplumber
    - Creates Document row + upload AuditEvent
    - Does NOT run analysis — caller handles that (sync or BackgroundTask)
    """
    validate_pdf(pdf_bytes, filename)

    doc_id = uuid.uuid4()
    pdf_path = persist_pdf(doc_id, pdf_bytes)

    try:
        raw_text, _ = parse_pdf(pdf_bytes)
    except NoExtractableTextError:
        raw_text = ""

    doc = Document(
        id=doc_id,
        filename=filename,
        type=doc_type,
        raw_text=raw_text,
        status="queued",
        source=source,
        batch_id=batch_id,
        pdf_path=pdf_path,
    )
    db.add(doc)
    db.add(AuditEvent(
        document_id=doc_id,
        event_type="uploaded",
        event_data={"filename": filename, "type": doc_type, "source": source, "size_bytes": len(pdf_bytes)},
    ))
    db.commit()
    return doc_id
