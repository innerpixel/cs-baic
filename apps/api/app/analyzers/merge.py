from app.analyzers.base import AnalyzerResult
from app.schemas.extraction import InvoiceExtraction


def merge_into_analysis(analysis: dict, result: AnalyzerResult) -> dict:
    """Merge an AnalyzerResult's parsed_output into the analysis dict.

    Each analyzer owns a specific set of keys in DocumentAnalysis.
    New analyzers in slice-4+ extend this function with another isinstance branch.
    """
    if result.status != "success":
        return analysis

    if isinstance(result.parsed_output, InvoiceExtraction):
        extraction: InvoiceExtraction = result.parsed_output
        analysis["fields"] = extraction.model_dump(
            exclude={"missing_fields", "risk_flags", "recommended_next_action", "line_items"}
        )
        analysis["fields"]["line_items"] = [item.model_dump() for item in extraction.line_items]
        analysis["missing_fields"] = extraction.missing_fields
        analysis["risk_flags"] = extraction.risk_flags
        analysis["suggested_action"] = extraction.recommended_next_action

    return analysis
