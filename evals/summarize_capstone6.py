from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


KNOWN_METRICS = {
    "scenarios": 60,
    "results_collected_without_errors": 60,
    "manual_labels": 33,
    "manual_good": 32,
    "manual_bad": 1,
    "failure_category": "incomplete",
}


def _load_report(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _print_report(name: str, report: dict | None) -> None:
    if report is None:
        print(f"{name}: not available")
        return
    print(
        f"{name}: accuracy={report.get('accuracy')}, "
        f"precision_bad={report.get('precision_bad')}, "
        f"recall_bad={report.get('recall_bad')}, "
        f"disagreements={report.get('disagreement_count')}"
    )


def main() -> None:
    print("Applied ML Teaching Copilot - Capstone 6 Summary")
    print("")
    print("Known evaluation set:")
    for key, value in KNOWN_METRICS.items():
        print(f"- {key}: {value}")
    print("")

    reports = {
        "initial judge": _load_report(PROJECT_ROOT / "evals" / "alignment_report.json"),
        "improved judge": _load_report(PROJECT_ROOT / "evals" / "alignment_report_improved.json"),
        "calibrated judge": _load_report(PROJECT_ROOT / "evals" / "alignment_report_calibrated.json"),
    }

    _print_report("Initial judge", reports["initial judge"])
    _print_report("Improved judge", reports["improved judge"])
    _print_report("Calibrated judge", reports["calibrated judge"])

    available = {name: report for name, report in reports.items() if report is not None}
    if available:
        best_accuracy = max(available.items(), key=lambda item: item[1].get("accuracy", 0))
        best_disagreement = min(available.items(), key=lambda item: item[1].get("disagreement_count", 10**9))
        print("")
        print(f"Best judge by accuracy: {best_accuracy[0]} ({best_accuracy[1].get('accuracy')})")
        print(
            "Best judge by disagreement count: "
            f"{best_disagreement[0]} ({best_disagreement[1].get('disagreement_count')})"
        )


if __name__ == "__main__":
    main()
