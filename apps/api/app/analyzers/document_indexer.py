"""DocumentIndexer: chunks document text, embeds, and upserts into document_chunks.

Creates its own DB session — chunk persistence is a write concern
that doesn't fit the pure-LLM Analyzer shape, but keeping it as a
registered Analyzer preserves the framework: no dispatcher edits needed.
"""
import uuid
from app.analyzers.base import AnalyzerResult
from app.db.models import DocumentChunk
from app.db.session import SessionLocal
from app.services.chunking import chunk_paragraph
from app.services.embeddings import embed_batch

ALL_DOC_TYPES = {
    "supplier_invoice", "client_invoice", "contract",
    "supplier_offer", "client_request", "accountant_request",
    "hr_document", "internal_procedure", "price_list", "unknown",
}


class DocumentIndexer:
    name = "document_indexer"
    version = "v1"
    applies_to = ALL_DOC_TYPES

    def run(self, document) -> AnalyzerResult:
        doc_id: uuid.UUID = document.id
        raw_text: str = document.raw_text or ""

        try:
            chunks = chunk_paragraph(raw_text)
            if not chunks:
                return AnalyzerResult(
                    analyzer_name=self.name,
                    analyzer_version=self.version,
                    prompt_input=raw_text[:200],
                    prompt_output_raw="",
                    parsed_output={"chunk_count": 0},
                    status="success",
                )

            embeddings = embed_batch(chunks)

            db = SessionLocal()
            try:
                # Idempotent: delete existing chunks then insert fresh
                db.query(DocumentChunk).filter_by(document_id=doc_id).delete()
                for idx, (content, emb) in enumerate(zip(chunks, embeddings)):
                    db.add(DocumentChunk(
                        id=uuid.uuid4(),
                        document_id=doc_id,
                        chunk_index=idx,
                        content=content,
                        embedding=emb,
                        metadata_={"filename": document.filename, "doc_type": document.type},
                    ))
                db.commit()
            finally:
                db.close()

            return AnalyzerResult(
                analyzer_name=self.name,
                analyzer_version=self.version,
                prompt_input=raw_text[:200],
                prompt_output_raw=f"{len(chunks)} chunks",
                parsed_output={"chunk_count": len(chunks)},
                status="success",
            )

        except Exception as exc:
            return AnalyzerResult(
                analyzer_name=self.name,
                analyzer_version=self.version,
                prompt_input=raw_text[:200],
                prompt_output_raw="",
                parsed_output=None,
                status="failed",
                error_message=str(exc)[:400],
            )
