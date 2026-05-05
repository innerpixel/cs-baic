import io
import pdfplumber


class NoExtractableTextError(Exception):
    """Raised when a PDF contains no extractable text (e.g. image-only scan)."""


def parse_pdf(file_bytes: bytes) -> tuple[str, dict]:
    """Extract text from a PDF file.

    Returns (extracted_text, metadata).
    Raises NoExtractableTextError for image-only PDFs.
    """
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        pages_text = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)

        metadata = {
            "page_count": len(pdf.pages),
            "pages_with_text": len(pages_text),
        }

    extracted = "\n\n".join(pages_text).strip()
    if not extracted:
        raise NoExtractableTextError("No extractable text found in PDF")

    return extracted, metadata
