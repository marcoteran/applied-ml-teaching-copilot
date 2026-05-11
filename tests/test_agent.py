import re

from src.teaching_agent import run_teaching_copilot
from tests.utils import assert_tool_order, contains_any, extract_tool_names


def test_mae_vs_mse_agent_uses_search_and_fetch():
    result = run_teaching_copilot(
        "When should I use MAE instead of MSE in a regression problem?"
    )

    final_answer = result["final_answer"]

    assert final_answer.strip()
    assert_tool_order(
        result["tool_call_history"],
        ["search_course_materials", "get_course_material"],
    )
    assert "MAE" in final_answer
    assert "MSE" in final_answer
    assert "aml-001" in final_answer


def test_agent_handles_out_of_scope_cnn_without_hallucination():
    result = run_teaching_copilot(
        "Can you explain convolutional neural networks using the course materials?"
    )

    final_answer = result["final_answer"]

    assert "search_course_materials" in extract_tool_names(result["tool_call_history"])
    assert "current course materials are insufficient" in final_answer.lower()
    assert not contains_any(
        final_answer,
        [
            "convolutional layer",
            "pooling layer",
            "filters slide",
            "feature maps",
            "backpropagation",
        ],
    )
    assert contains_any(
        final_answer,
        ["add relevant", "add cnn", "course notes", "relevant course notes"],
    )


def test_decision_tree_study_guide_uses_course_materials():
    result = run_teaching_copilot("Give me a short study guide about decision trees.")

    final_answer = result["final_answer"]

    assert "search_course_materials" in extract_tool_names(result["tool_call_history"])
    assert "decision tree" in final_answer.lower()
    assert contains_any(final_answer, ["study guide", "learning guide", "key points"])
    assert re.search(r"aml-\d{3}", final_answer)
