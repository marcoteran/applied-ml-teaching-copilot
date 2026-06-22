from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.teaching_agent import run_teaching_copilot


PROMPTS = [
    "When should I use MAE instead of MSE in a regression problem?",
    "Give me a short study guide about decision trees.",
    "Why can accuracy be misleading for an imbalanced classification dataset?",
    "Can you explain convolutional neural networks using the course materials?",
]


def main() -> None:
    load_dotenv()
    try:
        import logfire

        logfire.configure()
        span_factory = logfire.span
        print("Logfire configured. Running monitored demo sessions.")
    except Exception as exc:
        logfire = None
        span_factory = None
        print(f"Logfire unavailable or not configured ({exc}). Running local demo sessions.")

    for prompt in PROMPTS:
        if span_factory is None:
            result = run_teaching_copilot(prompt)
        else:
            with span_factory("teaching-copilot-session", prompt=prompt):
                result = run_teaching_copilot(prompt)
                if logfire is not None:
                    logfire.info("feedback_event", prompt=prompt, tool_calls=result.get("tool_call_history", []))
        print("")
        print(f"User: {prompt}")
        print(f"Assistant: {result.get('final_answer', '')}")


if __name__ == "__main__":
    main()
