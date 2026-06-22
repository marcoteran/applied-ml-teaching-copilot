from __future__ import annotations

import argparse
import json
from pathlib import Path


def _safe_divide(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 3) if denominator else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare LLM judge predictions to manual labels.")
    parser.add_argument("--judged", required=True, help="Path to judged results JSON.")
    parser.add_argument("--output", required=True, help="Path for alignment report JSON.")
    args = parser.parse_args()

    judged_path = Path(args.judged)
    rows = json.loads(judged_path.read_text(encoding="utf-8")) if judged_path.exists() else []

    total = len(rows)
    correct = 0
    disagreements = []
    true_bad = false_bad = predicted_bad = 0

    for row in rows:
        manual = str(row.get("manual_label", "")).lower()
        predicted = str((row.get("judge") or {}).get("predicted_label", "")).lower()
        if manual == predicted:
            correct += 1
        else:
            disagreements.append(
                {
                    "id": row.get("id"),
                    "manual_label": manual,
                    "predicted_label": predicted,
                    "question": row.get("question"),
                    "rationale": (row.get("judge") or {}).get("rationale"),
                }
            )
        if manual == "bad":
            true_bad += 1
        if predicted == "bad":
            predicted_bad += 1
        if manual != "bad" and predicted == "bad":
            false_bad += 1

    true_positive_bad = sum(
        1
        for row in rows
        if str(row.get("manual_label", "")).lower() == "bad"
        and str((row.get("judge") or {}).get("predicted_label", "")).lower() == "bad"
    )
    report = {
        "judged_file": str(judged_path),
        "total_labeled": total,
        "accuracy": _safe_divide(correct, total),
        "precision_bad": _safe_divide(true_positive_bad, predicted_bad),
        "recall_bad": _safe_divide(true_positive_bad, true_bad),
        "disagreement_count": len(disagreements),
        "false_bad_count": false_bad,
        "disagreements": disagreements,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
