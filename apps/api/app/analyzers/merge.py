from app.analyzers.base import AnalyzerResult
from app.schemas.classification import Classification
from app.schemas.contract import ContractReview
from app.schemas.extraction import InvoiceExtraction
from app.schemas.summary import Summary
from app.schemas.draft_reply import DraftReply


def _dedup_list(existing: list | None, new_items: list) -> list:
    result = list(existing or [])
    for item in new_items:
        if item not in result:
            result.append(item)
    return result


def merge_into_analysis(analysis: dict, result: AnalyzerResult) -> dict:
    """Merge an AnalyzerResult's parsed_output into the analysis dict.

    Each analyzer owns a specific set of keys. New analyzers add another isinstance branch.
    analyzer_outputs[<name>] always stores the full parsed output (single source of truth).
    """
    if result.status != "success":
        return analysis

    outputs = analysis.setdefault("analyzer_outputs", {})

    if isinstance(result.parsed_output, Classification):
        clf: Classification = result.parsed_output
        analysis["detected_type"] = clf.document_type
        analysis["confidence"] = clf.confidence
        analysis["language"] = clf.language
        outputs[result.analyzer_name] = clf.model_dump()

    elif isinstance(result.parsed_output, Summary):
        summ: Summary = result.parsed_output
        analysis["summary"] = summ.short_summary
        analysis["urgency"] = summ.urgency
        analysis["suggested_action"] = summ.recommended_next_action
        analysis["missing_fields"] = _dedup_list(
            analysis.get("missing_fields"), summ.missing_information
        )
        outputs[result.analyzer_name] = summ.model_dump()

    elif isinstance(result.parsed_output, InvoiceExtraction):
        extraction: InvoiceExtraction = result.parsed_output
        analysis["fields"] = extraction.model_dump(
            exclude={"missing_fields", "risk_flags", "recommended_next_action", "line_items"}
        )
        analysis["fields"]["line_items"] = [item.model_dump() for item in extraction.line_items]
        analysis["missing_fields"] = _dedup_list(
            analysis.get("missing_fields"), extraction.missing_fields
        )
        analysis["risk_flags"] = _dedup_list(
            analysis.get("risk_flags"), extraction.risk_flags
        )
        # extractor's suggested_action wins over summarizer's when both are present
        if extraction.recommended_next_action:
            analysis["suggested_action"] = extraction.recommended_next_action
        outputs[result.analyzer_name] = extraction.model_dump()

    elif isinstance(result.parsed_output, ContractReview):
        review: ContractReview = result.parsed_output
        analysis["risk_flags"] = _dedup_list(
            analysis.get("risk_flags"), review.risk_flags
        )
        outputs[result.analyzer_name] = review.model_dump()

    elif isinstance(result.parsed_output, DraftReply):
        draft: DraftReply = result.parsed_output
        outputs[result.analyzer_name] = draft.model_dump()

    elif isinstance(result.parsed_output, dict):
        # DocumentIndexer and similar dict-result analyzers (e.g. chunk_count)
        outputs[result.analyzer_name] = result.parsed_output

    return analysis
