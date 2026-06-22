from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

from src.config import OPENAI_MODEL


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = PROJECT_ROOT / "evals" / "results.json"
LABELS_PATH = PROJECT_ROOT / "evals" / "labels.csv"


class JudgeDecision(BaseModel):
    predicted_label: str = Field(description="good or bad")
    failure_category: str | None = Field(default=None)
    rationale: str


def read_results(path: Path = RESULTS_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing eval results file: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Eval results JSON must contain a list.")
    return data


def read_labels(path: Path = LABELS_PATH) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    labels = {}
    for row in rows:
        scenario_id = row.get("id") or row.get("scenario_id") or row.get("eval_id")
        label = row.get("label") or row.get("human_label") or row.get("manual_label")
        if scenario_id and label:
            labels[scenario_id] = {**row, "label": label.strip().lower()}
    return labels


def judge_results(
    *,
    instructions: str,
    output_path: Path,
    model: str = OPENAI_MODEL,
) -> None:
    load_dotenv()
    results = read_results()
    labels = read_labels()
    labeled_results = [row for row in results if row.get("id") in labels]

    if not labeled_results:
        output_path.write_text(json.dumps([], indent=2), encoding="utf-8")
        print("No labeled rows found. Wrote an empty judged results file.")
        return

    client = OpenAI()
    judged = []
    for row in labeled_results:
        response = client.responses.parse(
            model=model,
            instructions=instructions,
            input=[
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "id": row.get("id"),
                            "question": row.get("question"),
                            "expected_material_ids": row.get("expected_material_ids", []),
                            "final_answer": row.get("final_answer", ""),
                            "tool_call_history": row.get("tool_call_history", []),
                            "error": row.get("error"),
                            "manual_label": labels[row["id"]]["label"],
                        },
                        indent=2,
                    ),
                }
            ],
            text_format=JudgeDecision,
            temperature=0,
        )
        decision = response.output_parsed.model_dump()
        judged.append({**row, "manual_label": labels[row["id"]]["label"], "judge": decision})
        print(f"Judged {row['id']}: {decision['predicted_label']}")

    output_path.write_text(json.dumps(judged, indent=2), encoding="utf-8")
    print(f"Wrote {len(judged)} judged rows to {output_path}")
