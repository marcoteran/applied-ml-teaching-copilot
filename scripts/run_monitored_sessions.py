from __future__ import annotations

from pathlib import Path
import sys

from dotenv import load_dotenv
import logfire

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.monitoring import configure_monitoring, start_session_span
from src.teaching_agent import run_teaching_copilot


def summarize_run(result: dict) -> tuple[int, str, int, float | None]:
    tool_calls = len(result.get("tool_call_history", []))
    final_answer = result.get("final_answer", "")
    preview = " ".join(str(final_answer).split()[:30])
    answer_length = len(str(final_answer))

    token_usage = None
    estimated_cost = None
    usage = result.get("token_usage")
    if isinstance(usage, int):
        token_usage = usage
    if isinstance(result.get("estimated_cost_usd"), (float, int)):
        estimated_cost = float(result["estimated_cost_usd"])

    return tool_calls, preview, answer_length, token_usage or estimated_cost


def run_sessions() -> None:
    load_dotenv()
    configure_monitoring()

    queries = [
        "When should I use MAE instead of MSE in a regression problem?",
        "Give me a short study guide about decision trees.",
        "Can you explain convolutional neural networks using the course materials?",
    ]

    total_interactions = 0
    total_token_usage = 0
    total_cost = 0.0
    estimated_usage_available = False
    estimated_cost_available = False
    issues = []

    with start_session_span("teaching_copilot_session"):
        for query in queries:
            with start_session_span("teaching_copilot_run", query=query):
                result = run_teaching_copilot(query)

            total_interactions += 1
            tool_calls = len(result.get("tool_call_history", []))
            final_answer = result.get("final_answer", "")
            preview = " ".join(str(final_answer).split()[:30])
            token_usage = result.get("token_usage")
            estimated_cost = result.get("estimated_cost_usd")

            if isinstance(token_usage, int):
                total_token_usage += token_usage
                estimated_usage_available = True
            if isinstance(estimated_cost, (float, int)):
                total_cost += float(estimated_cost)
                estimated_cost_available = True

            is_insufficient = "current course materials are insufficient" in str(final_answer).lower()
            feedback_value = -1 if is_insufficient else 1
            logfire.info("user_feedback", feedback=feedback_value, query=query)

            print("Query:", query)
            print("Tool calls:", tool_calls)
            print("Final answer preview:", preview)
            print(
                "Token usage:", token_usage if token_usage is not None else "unknown",
                "Estimated cost:",
                f"${estimated_cost:.6f}" if isinstance(estimated_cost, (float, int)) else "unknown",
            )
            print("---")

            if is_insufficient:
                issues.append(f"Insufficient answer for query: {query}")

    print("Final summary:")
    print("Number of sessions collected:", 1)
    print("Total interactions:", total_interactions)
    print(
        "Total token usage:",
        total_token_usage if estimated_usage_available else "unavailable",
    )
    print(
        "Approximate cost:",
        f"${total_cost:.6f}" if estimated_cost_available else "unavailable",
    )
    print("Observed issues or patterns:")
    if issues:
        for issue in issues:
            print("-", issue)
    else:
        print("- No obvious issues observed.")


if __name__ == "__main__":
    run_sessions()
