from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
RESULTS_PATH = PROJECT_ROOT / "evals" / "results.json"
LABELS_PATH = PROJECT_ROOT / "evals" / "labels.csv"


def main() -> None:
    if not RESULTS_PATH.exists():
        raise FileNotFoundError("Run evals/run_evals.py before labeling results.")

    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    existing = {}
    if LABELS_PATH.exists():
        with LABELS_PATH.open("r", encoding="utf-8", newline="") as file:
            for row in csv.DictReader(file):
                existing[row["id"]] = row

    rows = []
    for row in results:
        current = existing.get(row["id"], {})
        print("")
        print(f"{row['id']}: {row['question']}")
        print(row.get("final_answer", "")[:1200])
        label = input(f"Label [good/bad] ({current.get('label', '')}): ").strip().lower()
        if not label:
            label = current.get("label", "")
        failure_category = input(f"Failure category ({current.get('failure_category', '')}): ").strip()
        if not failure_category:
            failure_category = current.get("failure_category", "")
        notes = input(f"Notes ({current.get('notes', '')}): ").strip()
        if not notes:
            notes = current.get("notes", "")
        rows.append({"id": row["id"], "label": label, "failure_category": failure_category, "notes": notes})

    with LABELS_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "label", "failure_category", "notes"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote labels to {LABELS_PATH}")


if __name__ == "__main__":
    main()
