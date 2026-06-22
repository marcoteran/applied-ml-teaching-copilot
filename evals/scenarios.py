from __future__ import annotations


CORE_SCENARIOS = [
    {
        "id": "eval-001",
        "question": "When should I use MAE instead of MSE in a regression problem?",
        "expected_material_ids": ["aml-001"],
        "category": "regression_metrics",
    },
    {
        "id": "eval-002",
        "question": "Give me a short study guide about decision trees.",
        "expected_material_ids": ["aml-002"],
        "category": "decision_trees",
    },
    {
        "id": "eval-003",
        "question": "Why can accuracy be misleading for an imbalanced classification dataset?",
        "expected_material_ids": ["aml-008", "aml-009"],
        "category": "classification_metrics",
    },
    {
        "id": "eval-004",
        "question": "Can you explain convolutional neural networks using the course materials?",
        "expected_material_ids": [],
        "category": "insufficient_materials",
    },
]


QUESTION_VARIANTS = [
    "Answer briefly: {question}",
    "Explain for a beginner: {question}",
    "Create a concise classroom answer: {question}",
    "What should a student remember about this? {question}",
    "Give one practical takeaway: {question}",
    "Use the course materials to answer: {question}",
    "Make this exam-review friendly: {question}",
    "What is the most important distinction? {question}",
    "Give a short explanation with citations: {question}",
    "Respond as an Applied ML teaching assistant: {question}",
    "Keep it grounded in the material: {question}",
    "What would you tell a confused student? {question}",
    "Summarize the course-material answer: {question}",
    "State the answer and one caution: {question}",
    "Give a two-paragraph answer: {question}",
]


def load_scenarios() -> list[dict]:
    scenarios: list[dict] = []
    for variant_index, template in enumerate(QUESTION_VARIANTS):
        for scenario in CORE_SCENARIOS:
            scenario_number = len(scenarios) + 1
            scenarios.append(
                {
                    "id": f"eval-{scenario_number:03d}",
                    "question": template.format(question=scenario["question"]),
                    "base_question": scenario["question"],
                    "expected_material_ids": scenario["expected_material_ids"],
                    "category": scenario["category"],
                }
            )
    return scenarios
