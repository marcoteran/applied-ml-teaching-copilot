from __future__ import annotations

from collections import defaultdict


_usage_by_model: dict[str, dict[str, int]] = defaultdict(
    lambda: {"input_tokens": 0, "output_tokens": 0}
)


def capture_usage(model: str, input_tokens: int, output_tokens: int) -> None:
    _usage_by_model[model]["input_tokens"] += int(input_tokens or 0)
    _usage_by_model[model]["output_tokens"] += int(output_tokens or 0)


def display_total_usage() -> None:
    if not _usage_by_model:
        print("\nNo OpenAI token usage captured.")
        return

    print("\nOpenAI token usage:")
    for model, usage in sorted(_usage_by_model.items()):
        print(
            f"- {model}: "
            f"{usage['input_tokens']} input tokens, "
            f"{usage['output_tokens']} output tokens"
        )
