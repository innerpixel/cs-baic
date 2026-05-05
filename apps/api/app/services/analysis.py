import hashlib
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.analyzers.merge import merge_into_analysis
from app.analyzers.registry import analyzers_for
from app.core.config import settings
from app.db.models import AuditEvent, Document, DocumentAnalysis, PromptRun


def run_analysis(document_id: uuid.UUID, db: Session) -> None:
    doc = db.get(Document, document_id)
    if not doc:
        return

    applicable = analyzers_for(doc)

    if not applicable:
        db.add(AuditEvent(
            document_id=document_id,
            event_type="not_supported_yet",
            event_data={"doc_type": doc.type},
        ))
        doc.status = "not_supported"
        db.commit()
        return

    analysis_data: dict = {}
    last_prompt_run_id: uuid.UUID | None = None
    any_succeeded = False

    for analyzer in applicable:
        result = analyzer.run(doc)

        now = datetime.now(timezone.utc)
        prompt_run = PromptRun(
            id=uuid.uuid4(),
            document_id=document_id,
            prompt_name=result.analyzer_name,
            prompt_version=result.analyzer_version,
            model=settings.llm_model,
            input_text=result.prompt_input,
            input_hash=hashlib.sha256(result.prompt_input.encode()).hexdigest(),
            output_json=result.parsed_output.model_dump() if result.status == "success" and result.parsed_output else None,
            status=result.status,
            error_message=result.error_message,
            created_at=now,
            completed_at=now,
        )
        db.add(prompt_run)
        db.flush()
        last_prompt_run_id = prompt_run.id

        event_type = f"analyzed_by:{analyzer.name}"
        if result.status == "failed":
            event_type = f"analysis_failed:{analyzer.name}"

        db.add(AuditEvent(
            document_id=document_id,
            event_type=event_type,
            event_data={"status": result.status, "error": result.error_message},
        ))

        if result.status == "success":
            any_succeeded = True
            analysis_data = merge_into_analysis(analysis_data, result)

    existing = db.query(DocumentAnalysis).filter_by(document_id=document_id).first()
    if existing:
        existing.fields = analysis_data.get("fields")
        existing.missing_fields = analysis_data.get("missing_fields")
        existing.risk_flags = analysis_data.get("risk_flags")
        existing.summary = analysis_data.get("summary")
        existing.suggested_action = analysis_data.get("suggested_action")
        existing.detected_type = analysis_data.get("detected_type")
        existing.confidence = analysis_data.get("confidence")
        existing.language = analysis_data.get("language")
        existing.urgency = analysis_data.get("urgency")
        existing.analyzer_outputs = analysis_data.get("analyzer_outputs")
        existing.prompt_run_id = last_prompt_run_id
    else:
        db.add(DocumentAnalysis(
            id=uuid.uuid4(),
            document_id=document_id,
            prompt_run_id=last_prompt_run_id,
            fields=analysis_data.get("fields"),
            missing_fields=analysis_data.get("missing_fields"),
            risk_flags=analysis_data.get("risk_flags"),
            summary=analysis_data.get("summary"),
            suggested_action=analysis_data.get("suggested_action"),
            detected_type=analysis_data.get("detected_type"),
            confidence=analysis_data.get("confidence"),
            language=analysis_data.get("language"),
            urgency=analysis_data.get("urgency"),
            analyzer_outputs=analysis_data.get("analyzer_outputs"),
        ))

    doc.status = "done" if any_succeeded else "failed"
    db.commit()
