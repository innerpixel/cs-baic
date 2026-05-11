"""Demo archive endpoint.

GET /api/demo/atelier-nova/archive.zip
  Streams a fresh ZIP of all generated Atelier Nova PDFs.
  Returns 404 if the output dir is empty.
"""
import io
import zipfile
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter()

PDF_DIR = Path(__file__).parent.parent.parent / "var" / "demo_pdfs" / "atelier_nova"


@router.get("/demo/atelier-nova/archive.zip")
def atelier_nova_archive():
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        raise HTTPException(
            status_code=404,
            detail="Demo PDFs not generated yet. Run: uv run python scripts/generate_demo_pdfs.py",
        )

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in pdf_files:
            zf.write(p, arcname=p.name)
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=atelier-nova-archive.zip"},
    )
