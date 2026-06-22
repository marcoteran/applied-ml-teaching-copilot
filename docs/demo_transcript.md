# Demo Transcript

This transcript describes the intended reviewer demo for Applied ML Teaching Copilot. The exact wording may vary because the final answer is generated, but the tool and grounding behavior should stay stable.

## 1. MAE vs MSE

**User question:** When should I use MAE instead of MSE in a regression problem?

**Expected behavior:** The agent compares MAE and MSE, explaining that MAE is easier to interpret in target units and less sensitive to outliers, while MSE penalizes large errors more strongly.

**Expected tool pattern:** `search_course_materials` followed by `get_course_material`.

**Expected grounding behavior:** The answer should cite `aml-001` and use only the retrieved course-material explanation.

## 2. Decision Trees Study Guide

**User question:** Give me a short study guide about decision trees.

**Expected behavior:** The agent produces a compact study guide with key ideas such as feature-based splits, purity, interpretability, nonlinear relationships, and overfitting.

**Expected tool pattern:** `search_course_materials` followed by one or more `get_course_material` calls for relevant tree records.

**Expected grounding behavior:** The answer should cite material ids such as `aml-002`, and may also cite `aml-003`, `aml-004`, or `aml-005` if those records are fetched.

## 3. Imbalanced Classification and Accuracy

**User question:** Why can accuracy be misleading for an imbalanced classification dataset?

**Expected behavior:** The agent explains that a model can predict the majority class most of the time and still look accurate while failing on minority classes. It should mention alternatives such as precision, recall, F1 score, confusion matrices, and class-specific performance.

**Expected tool pattern:** `search_course_materials` followed by `get_course_material`.

**Expected grounding behavior:** The answer should cite `aml-008` and/or `aml-009`.

## 4. CNN Out of Scope

**User question:** Can you explain convolutional neural networks using the course materials?

**Expected behavior:** The agent should state that the current course materials are insufficient to answer using the course materials and suggest adding relevant notes, slides, or readings.

**Expected tool pattern:** `search_course_materials`; no unsupported CNN source should be fetched.

**Expected grounding behavior:** The response should not explain convolutional layers, pooling, filters, feature maps, or backpropagation from general model knowledge.

This CNN example is important because it tests the capstone's grounding behavior. A useful teaching copilot should be able to say "the materials do not cover this" rather than hallucinating an answer that sounds plausible but is unsupported by the course corpus.
