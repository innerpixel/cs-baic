from typing import Any, Protocol, runtime_checkable
from pydantic import BaseModel


class AnalyzerResult(BaseModel):
    analyzer_name: str
    analyzer_version: str
    prompt_input: str
    prompt_output_raw: str
    parsed_output: Any
    status: str  # "success" | "failed"
    error_message: str | None = None


@runtime_checkable
class Analyzer(Protocol):
    name: str
    version: str
    applies_to: set[str]

    def run(self, document: Any) -> AnalyzerResult: ...
