from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from evals.judge_common import PROJECT_ROOT, judge_results


INSTRUCTIONS = """
You are a strict evaluator for an Applied ML Teaching Copilot.
Mark an answer bad if it lacks clear grounding, omits expected citations, gives
unsupported ML explanations, ignores tool results, or only partially answers the
question. Be especially careful with vague answers and responses that mention
course materials without showing material ids. If the answer says materials are
insufficient, verify that the tool history supports that claim.
""".strip()


if __name__ == "__main__":
    judge_results(
        instructions=INSTRUCTIONS,
        output_path=PROJECT_ROOT / "evals" / "results_judged_improved.json",
    )
