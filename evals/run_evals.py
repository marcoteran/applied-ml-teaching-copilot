from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from evals.scenarios import load_scenarios
from src.teaching_agent import run_teaching_copilot


RESULTS_PATH = PROJECT_ROOT / "evals" / "results.json"
SMOKE_RESULTS_PATH = PROJECT_ROOT / "evals" / "results_smoke.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Applied ML Teaching Copilot eval scenarios.")
    parser.add_argument("--limit", type=int, default=None, help="Optional number of scenarios to run.")
    parser.add_argument("--output", default=None, help="Path for eval results JSON.")
    args = parser.parse_args()

    load_dotenv()
    scenarios = load_scenarios()
    if args.limit is not None:
        scenarios = scenarios[: args.limit]

    results = []
    for scenario in scenarios:
        print(f"Running {scenario['id']}: {scenario['question']}")
        try:
            agent_result = run_teaching_copilot(scenario["question"])
            results.append(
                {
                    **scenario,
                    "final_answer": agent_result.get("final_answer", ""),
                    "tool_call_history": agent_result.get("tool_call_history", []),
                    "error": None,
                }
            )
        except Exception as exc:
            results.append({**scenario, "final_answer": "", "tool_call_history": [], "error": str(exc)})

    output_path = Path(args.output) if args.output else RESULTS_PATH
    if args.output is None and args.limit is not None:
        output_path = SMOKE_RESULTS_PATH

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {len(results)} results to {output_path}")


if __name__ == "__main__":
    main()
