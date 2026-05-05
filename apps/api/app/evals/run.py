"""CLI entry point for the eval harness.

Usage:
    uv run python -m app.evals.run
    uv run python -m app.evals.run --analyzer invoice_extractor
    uv run python -m app.evals.run --fixture invoice_lumina
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from app.evals.runner import run_all
from app.evals.scoring import EvalScore

RESULTS_DIR = Path(__file__).parent.parent.parent.parent / "tests" / "evals" / "results"


def _fmt_row(s: EvalScore) -> str:
    status = "PASS" if s.passed else "FAIL"
    errs = ""
    if s.critical_errors:
        errs += f"  critical: {'; '.join(s.critical_errors[:2])}"
    if s.minor_errors:
        errs += f"  minor: {'; '.join(s.minor_errors[:2])}"
    return f"  [{status}] {s.test_case} / {s.analyzer_name}  score={s.score}/10{errs}"


def main() -> int:
    parser = argparse.ArgumentParser(description="BCA Eval Harness")
    parser.add_argument("--analyzer", help="Only evaluate this analyzer")
    parser.add_argument("--fixture", help="Only evaluate this fixture")
    args = parser.parse_args()

    print("Running eval harness…")
    scores = run_all(analyzer_filter=args.analyzer, fixture_filter=args.fixture)

    if not scores:
        print("No evals matched the given filters.")
        return 1

    all_passed = all(s.passed for s in scores)
    pass_count = sum(1 for s in scores if s.passed)

    print(f"\nResults: {pass_count}/{len(scores)} passed\n")
    for s in scores:
        print(_fmt_row(s))

    # Write JSON results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = RESULTS_DIR / f"{ts}.json"
    payload = [s.model_dump() for s in scores]
    out_path.write_text(json.dumps(payload, indent=2))
    print(f"\nResults written to {out_path}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
