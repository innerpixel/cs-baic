"""Eval runner: runs analyzers against fixtures and scores their outputs."""

import json
import uuid
from types import SimpleNamespace
from app.analyzers.registry import ANALYZERS
from app.evals.scoring import EvalScore
from app.evals.fixtures import FIXTURES, ASK_FIXTURES


def _find_analyzer(name: str):
    for a in ANALYZERS:
        if a.name == name:
            return a
    return None


def _flatten_list(items: list) -> str:
    """Flatten a list of strings or dicts to a single searchable string."""
    parts = []
    for item in items:
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, dict):
            parts.extend(str(v) for v in item.values() if v is not None)
        else:
            parts.append(str(item))
    return " ".join(parts)


def _check_expected(actual_dict: dict, expected: dict) -> tuple[list[str], list[str], list[str]]:
    """Return (critical_errors, minor_errors, hallucinations)."""
    critical = []
    minor = []
    hallucinations = []

    for key, exp_val in expected.items():
        if key == "missing_fields_contains":
            # actual missing_fields list should contain all expected phrases
            actual_mf = actual_dict.get("missing_fields", [])
            actual_str = " ".join(actual_mf).lower()
            for phrase in exp_val:
                if phrase.lower() not in actual_str:
                    critical.append(f"missing_fields: expected phrase '{phrase}' not found (actual: {actual_mf})")
            continue

        if key == "short_summary_contains":
            actual_summ = actual_dict.get("short_summary", "") or ""
            for phrase in exp_val:
                if phrase.lower() not in actual_summ.lower():
                    minor.append(f"short_summary: expected phrase '{phrase}' not found")
            continue

        if key == "payment_terms_contains":
            actual_pt = _flatten_list(actual_dict.get("payment_terms", [])).lower()
            for phrase in exp_val:
                if phrase.lower() not in actual_pt:
                    critical.append(f"payment_terms: expected phrase '{phrase}' not found (actual: {actual_pt!r})")
            continue

        if key == "penalties_contains":
            actual_pen = _flatten_list(actual_dict.get("penalties", [])).lower()
            for phrase in exp_val:
                # phrase may be a list meaning "any one of these"
                if isinstance(phrase, list):
                    if not any(p.lower() in actual_pen for p in phrase):
                        critical.append(
                            f"penalties: expected one of {phrase!r} not found (actual: {actual_pen!r})"
                        )
                elif phrase.lower() not in actual_pen:
                    critical.append(f"penalties: expected phrase '{phrase}' not found (actual: {actual_pen!r})")
            continue

        if key == "termination_terms_nonempty":
            if not actual_dict.get("termination_terms"):
                critical.append("termination_terms: expected non-empty list, got empty or missing")
            continue

        if key == "risk_flags_nonempty":
            if not actual_dict.get("risk_flags"):
                critical.append("risk_flags: expected non-empty list, got empty or missing")
            continue

        if key == "urgency_not_critical":
            urgency = actual_dict.get("urgency", "unknown")
            if urgency == "high":
                minor.append(f"urgency: expected low/medium for this doc, got high")
            continue

        if key == "urgency_not_unknown":
            urgency = actual_dict.get("urgency", "unknown")
            if urgency == "unknown":
                minor.append(f"urgency: expected a specific value, got 'unknown'")
            continue

        if key == "reply_body_contains_any":
            body = actual_dict.get("reply_body", "") or ""
            if not any(word.lower() in body.lower() for word in exp_val):
                critical.append(
                    f"reply_body: expected at least one of {exp_val!r} but found none "
                    f"(body[:100]: {body[:100]!r})"
                )
            continue

        if key == "human_review_required":
            actual_hrr = actual_dict.get("human_review_required")
            if actual_hrr is not True:
                critical.append(
                    f"human_review_required: expected True, got {actual_hrr!r}"
                )
            continue

        # Direct value comparison
        if key not in actual_dict:
            critical.append(f"missing key: {key!r}")
            continue

        actual_val = actual_dict[key]
        if exp_val is None:
            if actual_val is None or actual_val == "":
                critical.append(f"{key}: expected non-null but got null/empty")
            continue

        # Compare values; monetary/date/CUI mismatches are critical
        is_critical_field = any(tok in key for tok in ("amount", "date", "cui", "number", "invoice"))
        if str(actual_val).strip() != str(exp_val).strip():
            if is_critical_field:
                # Check if actual value appears in input — if not, it's a hallucination
                msg = f"{key}: expected {exp_val!r}, got {actual_val!r}"
                critical.append(msg)
            else:
                minor.append(f"{key}: expected {exp_val!r}, got {actual_val!r}")

    return critical, minor, hallucinations


def _score_from_errors(critical: list, minor: list, hallucinations: list) -> int:
    score = 10
    score -= len(hallucinations) * 4
    score -= len(critical) * 2
    score -= len(minor) * 1
    return max(0, min(10, score))


def evaluate(fixture_id: str, analyzer_name: str) -> EvalScore | None:
    """Run a single analyzer against a single fixture and return an EvalScore."""
    fixture = FIXTURES.get(fixture_id)
    if not fixture:
        return None

    expected = fixture["expected"].get(analyzer_name)
    if expected is None:
        # This analyzer is not evaluated for this fixture
        return None

    analyzer = _find_analyzer(analyzer_name)
    if not analyzer:
        return EvalScore(
            test_case=fixture_id,
            analyzer_name=analyzer_name,
            prompt_version="unknown",
            score=0,
            passed=False,
            critical_errors=[f"Analyzer '{analyzer_name}' not found in registry"],
        )

    # Build a minimal document object the analyzer can consume.
    # id is provided so analyzers that need document.id (e.g. DraftReplyGenerator) don't error.
    doc = SimpleNamespace(
        id=uuid.uuid4(),
        raw_text=fixture["input_text"],
        type=fixture["doc_type"],
        filename=f"eval_{fixture_id}.txt",
    )

    if fixture["doc_type"] not in analyzer.applies_to:
        return EvalScore(
            test_case=fixture_id,
            analyzer_name=analyzer_name,
            prompt_version=analyzer.version,
            score=0,
            passed=False,
            critical_errors=[f"Analyzer '{analyzer_name}' does not apply to doc_type '{fixture['doc_type']}'"],
        )

    result = analyzer.run(doc)

    if result.status == "failed":
        return EvalScore(
            test_case=fixture_id,
            analyzer_name=analyzer_name,
            prompt_version=analyzer.version,
            score=0,
            passed=False,
            critical_errors=[f"Analyzer run failed: {result.error_message}"],
        )

    actual_dict = result.parsed_output.model_dump() if result.parsed_output else {}
    critical, minor, hallucinations = _check_expected(actual_dict, expected)
    score = _score_from_errors(critical, minor, hallucinations)
    passed = score >= 7 and len(critical) == 0 and len(hallucinations) == 0

    return EvalScore(
        test_case=fixture_id,
        analyzer_name=analyzer_name,
        prompt_version=result.analyzer_version,
        score=score,
        passed=passed,
        critical_errors=critical,
        minor_errors=minor,
        hallucinations=hallucinations,
    )


def evaluate_ask(fixture_id: str) -> EvalScore:
    """Run an Ask My Company fixture against the live RAG pipeline (requires DB)."""
    fixture = ASK_FIXTURES.get(fixture_id)
    if not fixture:
        return EvalScore(
            test_case=fixture_id,
            analyzer_name="ask_company",
            prompt_version="v1",
            score=0,
            passed=False,
            critical_errors=[f"Ask fixture '{fixture_id}' not found"],
        )

    try:
        from app.db.session import SessionLocal
        from app.services.ask import answer_question
    except Exception as e:
        return EvalScore(
            test_case=fixture_id,
            analyzer_name="ask_company",
            prompt_version="v1",
            score=0,
            passed=False,
            critical_errors=[f"Import error (DB not available?): {e}"],
        )

    db = SessionLocal()
    try:
        answer = answer_question(fixture["query"], db)
    except Exception as e:
        return EvalScore(
            test_case=fixture_id,
            analyzer_name="ask_company",
            prompt_version="v1",
            score=0,
            passed=False,
            critical_errors=[f"answer_question failed: {e}"],
        )
    finally:
        db.close()

    critical = []
    minor = []
    no_docs_expected: bool = fixture.get("no_docs_expected", False)
    expected_sources: set = fixture.get("expected_source_filenames", set())
    expected_keywords: list = fixture.get("expected_keywords", [])

    answer_text = answer.answer or ""
    actual_sources = set(answer.source_documents or [])

    # Source citation scoring
    if no_docs_expected:
        if actual_sources:
            minor.append(f"expected no source documents but got {actual_sources!r}")
        if not any(kw.lower() in answer_text.lower() for kw in expected_keywords):
            critical.append(
                f"'not found' response expected — none of {expected_keywords!r} found in answer"
            )
        source_score = 1.0 if not actual_sources else 0.5
        keyword_score = 1.0 if any(kw.lower() in answer_text.lower() for kw in expected_keywords) else 0.0
    else:
        if expected_sources:
            found = expected_sources & actual_sources
            source_score = len(found) / len(expected_sources)
            if source_score < 0.8:
                critical.append(
                    f"source citation: {found!r} found of {expected_sources!r} "
                    f"({source_score:.0%} < 80%)"
                )
        else:
            source_score = 1.0

        if expected_keywords:
            found_kws = [kw for kw in expected_keywords if kw.lower() in answer_text.lower()]
            keyword_score = len(found_kws) / len(expected_keywords)
            if keyword_score < 0.7:
                missing_kws = [kw for kw in expected_keywords if kw not in found_kws]
                minor.append(
                    f"keyword presence: {keyword_score:.0%} < 70% — missing: {missing_kws!r}"
                )
        else:
            keyword_score = 1.0

    combined = (source_score * 0.5 + keyword_score * 0.5)
    score = max(0, min(10, round(combined * 10)))
    score -= len(critical) * 2
    score = max(0, score)
    passed = (
        score >= 7
        and len(critical) == 0
        and (no_docs_expected or source_score >= 0.8)
        and keyword_score >= 0.7
    )

    return EvalScore(
        test_case=fixture_id,
        analyzer_name="ask_company",
        prompt_version="v1",
        score=score,
        passed=passed,
        critical_errors=critical,
        minor_errors=minor,
    )


def run_all_ask(fixture_filter: str | None = None) -> list[EvalScore]:
    results = []
    for fixture_id in ASK_FIXTURES:
        if fixture_filter and fixture_id != fixture_filter:
            continue
        results.append(evaluate_ask(fixture_id))
    return results


def run_all(
    analyzer_filter: str | None = None,
    fixture_filter: str | None = None,
) -> list[EvalScore]:
    results = []
    for fixture_id, fixture in FIXTURES.items():
        if fixture_filter and fixture_id != fixture_filter:
            continue
        for analyzer_name in fixture["expected"]:
            if analyzer_filter and analyzer_name != analyzer_filter:
                continue
            score = evaluate(fixture_id, analyzer_name)
            if score is not None:
                results.append(score)
    return results
