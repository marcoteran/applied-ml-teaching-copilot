from __future__ import annotations

import json

from openai import OpenAI
from pydantic import BaseModel, Field

from tests.cost_tracker import capture_usage


class JudgeCriterion(BaseModel):
    criterion_description: str
    passed: bool
    judgement: str


class JudgeFeedback(BaseModel):
    criteria: list[JudgeCriterion] = Field(default_factory=list)
    feedback: str


def create_judge_client() -> OpenAI:
    return OpenAI()


def create_judge() -> OpenAI:
    return create_judge_client()


def assert_criteria(result: dict, criteria: list[str]) -> None:
    client = create_judge_client()

    response = client.responses.parse(
        model="gpt-4o-mini",
        instructions=(
            "You are a strict evaluator for an Applied ML Teaching Copilot. "
            "Assess only the submitted final answer and tool call history. "
            "Mark each criterion as passed only when the evidence is clear."
        ),
        input=[
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "final_answer": result["final_answer"],
                        "tool_call_history": result["tool_call_history"],
                        "criteria": criteria,
                    },
                    indent=2,
                ),
            }
        ],
        text_format=JudgeFeedback,
        temperature=0,
    )

    usage = getattr(response, "usage", None)
    if usage is not None:
        capture_usage(
            "gpt-4o-mini",
            getattr(usage, "input_tokens", 0) or 0,
            getattr(usage, "output_tokens", 0) or 0,
        )

    feedback = response.output_parsed
    failed = [criterion for criterion in feedback.criteria if not criterion.passed]

    assert not failed, (
        "LLM judge criteria failed:\n"
        + "\n".join(
            f"- {item.criterion_description}: {item.judgement}"
            for item in failed
        )
        + f"\nOverall feedback: {feedback.feedback}"
    )
