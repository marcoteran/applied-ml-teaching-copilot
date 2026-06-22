from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from evals.judge_common import PROJECT_ROOT, judge_results


INSTRUCTIONS = """
You are an evaluator for an Applied ML Teaching Copilot.
Classify the response as good or bad using the final answer, tool call history,
and expected material ids. A good answer should answer the question, use the
course-material tools, cite relevant material ids when material exists, and avoid
unsupported general claims when material is missing. Penalize hallucination,
missing citations, missing retrieval, and incomplete answers.
""".strip()


if __name__ == "__main__":
    judge_results(
        instructions=INSTRUCTIONS,
        output_path=PROJECT_ROOT / "evals" / "results_judged.json",
    )
