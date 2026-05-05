from pydantic import BaseModel


class EvalScore(BaseModel):
    test_case: str
    analyzer_name: str
    prompt_version: str
    score: int  # 0-10
    passed: bool
    critical_errors: list[str] = []
    minor_errors: list[str] = []
    hallucinations: list[str] = []
    missing_information: list[str] = []
    format_errors: list[str] = []
    notes: str = ""
