from __future__ import annotations

import json
from typing import Any

from openai import OpenAI

from src.tools import CourseMaterialTools, create_course_material_tools


DEFAULT_MODEL = "gpt-4o-mini"

DEFAULT_INSTRUCTIONS = """
You are Applied ML Teaching Copilot, an assistant for instructors and students
working with Applied Machine Learning course materials.

Rules:
- Use search_course_materials when the user asks about a topic.
- If search_course_materials returns relevant results, use get_course_material
  to fetch full detail for at least one relevant material before answering.
- Use only facts from retrieved course materials.
- Cite material ids such as aml-001 for every substantive answer.
- If search_course_materials returns zero relevant results, say that the current
  course materials are insufficient.
- Never provide a general explanation from model knowledge when the materials
  are insufficient.
- For out-of-scope questions, suggest adding relevant material to the knowledge
  base, such as course notes, slides, or readings.
""".strip()


def create_tool_schemas() -> list[dict]:
    return [
        {
            "type": "function",
            "name": "search_course_materials",
            "description": "Search Applied ML course materials for records relevant to a user query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query written by the user.",
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Maximum number of search results to return.",
                        "default": 5,
                    },
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
        {
            "type": "function",
            "name": "get_course_material",
            "description": "Retrieve the full content of a course-material record by id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "material_id": {
                        "type": "string",
                        "description": "The course-material id to retrieve, such as aml-001.",
                    },
                },
                "required": ["material_id"],
                "additionalProperties": False,
            },
        },
    ]


def _response_item_to_dict(item: Any) -> Any:
    if hasattr(item, "model_dump"):
        return item.model_dump()
    return item


def _capture_usage(model: str, response: Any) -> None:
    usage = getattr(response, "usage", None)
    if usage is None:
        return

    input_tokens = getattr(usage, "input_tokens", 0) or 0
    output_tokens = getattr(usage, "output_tokens", 0) or 0

    try:
        from tests.cost_tracker import capture_usage
    except Exception:
        return

    capture_usage(model, input_tokens, output_tokens)


def _should_force_insufficient_materials_answer(tool_call_history: list[dict]) -> bool:
    searched_with_no_results = any(
        call.get("tool") == "search_course_materials"
        and call.get("result_count") == 0
        for call in tool_call_history
    )
    fetched_material = any(
        call.get("tool") == "get_course_material"
        for call in tool_call_history
    )
    return searched_with_no_results and not fetched_material


def _insufficient_materials_answer(query: str) -> str:
    return (
        "The current course materials are insufficient to answer this question "
        f"using the course materials: {query} "
        "To support this query, add relevant course notes, slides, or readings "
        "to the knowledge base."
    )


def run_teaching_copilot(
    query: str,
    tools: CourseMaterialTools | None = None,
) -> dict:
    course_tools = tools or create_course_material_tools()
    course_tools.reset_history()

    client = OpenAI()
    tool_schemas = create_tool_schemas()
    available_tools = {
        "search_course_materials": course_tools.search_course_materials,
        "get_course_material": course_tools.get_course_material,
    }
    message_history: list[Any] = [{"role": "user", "content": query}]

    for _ in range(8):
        response = client.responses.create(
            model=DEFAULT_MODEL,
            instructions=DEFAULT_INSTRUCTIONS,
            input=message_history,
            tools=tool_schemas,
            tool_choice="auto",
            temperature=0,
        )
        _capture_usage(DEFAULT_MODEL, response)

        response_items = [_response_item_to_dict(item) for item in response.output]
        message_history.extend(response_items)

        function_calls = [
            item
            for item in response.output
            if getattr(item, "type", None) == "function_call"
        ]

        if not function_calls:
            final_answer = response.output_text
            if _should_force_insufficient_materials_answer(course_tools.tool_call_history):
                final_answer = _insufficient_materials_answer(query)

            return {
                "final_answer": final_answer,
                "tool_call_history": list(course_tools.tool_call_history),
                "message_history": message_history,
            }

        for function_call in function_calls:
            tool_name = function_call.name
            arguments = json.loads(function_call.arguments or "{}")
            tool_fn = available_tools.get(tool_name)

            if tool_fn is None:
                tool_result = {"error": f"Unknown tool: {tool_name}"}
            else:
                try:
                    tool_result = tool_fn(**arguments)
                except Exception as exc:
                    tool_result = {"error": f"Tool execution failed: {exc}"}

            message_history.append(
                {
                    "type": "function_call_output",
                    "call_id": function_call.call_id,
                    "output": json.dumps(tool_result),
                }
            )

    raise RuntimeError("Agent did not finish within the maximum number of turns.")
