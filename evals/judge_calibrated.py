from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from evals.judge_common import PROJECT_ROOT, judge_results


INSTRUCTIONS = """
You are a calibrated evaluator for an Applied ML Teaching Copilot.

Judge the response as good or bad based on whether it behaves like a grounded
course-material assistant, not based on whether a general ML expert could answer
the question from memory.

Strict rules:
- Penalize hallucinated facts, unsupported claims, missing retrieval, missing
  citations for substantive answers, and incomplete answers.
- If relevant course materials were retrieved, a good response should use them
  and cite material ids.
- If the course materials are genuinely insufficient and the agent clearly says
  that, the response can be good, even if a general ML expert could answer the
  question.
- Do not penalize a grounded insufficiency answer merely because it declines to
  provide a general ML explanation.
- For out-of-scope questions, reward clear insufficiency language and a useful
  suggestion to add relevant notes, slides, or readings.

Return predicted_label as exactly "good" or "bad".
Use failure_category only for bad responses, such as hallucination,
missing_grounding, incomplete, missing_tool_use, or error.
""".strip()


if __name__ == "__main__":
    judge_results(
        instructions=INSTRUCTIONS,
        output_path=PROJECT_ROOT / "evals" / "results_judged_calibrated.json",
    )
