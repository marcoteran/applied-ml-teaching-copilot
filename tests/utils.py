def extract_tool_names(tool_call_history: list[dict]) -> list[str]:
    return [call.get("tool", "") for call in tool_call_history]


def assert_tool_order(tool_call_history: list[dict], expected_prefix: list[str]) -> None:
    actual = extract_tool_names(tool_call_history)
    assert actual[: len(expected_prefix)] == expected_prefix


def contains_any(text: str, terms: list[str]) -> bool:
    text_lower = text.lower()
    return any(term.lower() in text_lower for term in terms)
