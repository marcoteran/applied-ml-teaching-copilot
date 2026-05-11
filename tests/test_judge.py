from src.teaching_agent import run_teaching_copilot
from tests.judge import assert_criteria


def test_judge_mae_vs_mse_grounding():
    result = run_teaching_copilot(
        "When should I use MAE instead of MSE in a regression problem?"
    )

    assert_criteria(
        result,
        [
            "The agent called search_course_materials before get_course_material.",
            "The answer compares MAE and MSE using the course material rather than unsupported general knowledge.",
            "The answer states that MAE is less sensitive to outliers or easier to interpret in target units.",
            "The answer states that MSE penalizes large errors more strongly.",
            "The answer cites material id aml-001.",
        ],
    )
