# Applied ML Teaching Copilot

A grounded AI assistant for Applied Machine Learning course materials.

Applied ML Teaching Copilot is an AI Engineering Buildcamp capstone project. It demonstrates a small but complete agentic application: course-material retrieval, tool use, grounded answering, insufficiency handling, monitoring hooks, tests, evaluation scenarios, LLM judge alignment, and a reviewer-friendly Streamlit UI.

## Problem Statement

Students and instructors need a reliable assistant that answers from course materials and avoids hallucinating unsupported ML content. A helpful teaching copilot should explain what the course actually covers, cite source material ids, and clearly say when the available materials are insufficient.

## What the Project Does

- Searches Applied ML course materials.
- Retrieves exact material records before answering.
- Answers with material ids such as `aml-001`.
- Identifies insufficient course coverage instead of inventing unsupported answers.
- Logs monitored demo sessions when Logfire is configured.
- Supports evaluation with scenarios, manual labels, LLM judges, and alignment reports.
- Provides a Streamlit chat UI for reviewers.

## Architecture

```text
User
  -> Streamlit UI / scripts
  -> Teaching Copilot Agent
  -> tools
  -> course material KB
  -> grounded answer

Monitoring
  -> Logfire

Evaluation
  -> scenarios
  -> results
  -> labels
  -> judge
  -> alignment
```

## Agent Tools

`search_course_materials(query, num_results=5)` searches the Applied ML knowledge base and returns compact records with ids, metadata, topics, and snippets.

`get_course_material(material_id)` retrieves the full source record for a selected material id. The agent is instructed to fetch full material before giving substantive grounded answers.

## Repository Structure

- `src/` - agent loop and course-material tools.
- `data/` - JSON course-material knowledge base.
- `tests/` - pytest checks and an LLM judge test.
- `scripts/` - monitored demo sessions.
- `evals/` - scenario runner, manual labels, judge variants, and alignment summary tools.
- `docs/` - demo transcript and project self-evaluation.
- `notebooks/` - setup, RAG baseline, and agentic prototype notebooks.
- `app.py` - Streamlit reviewer UI.

## Quickstart

```bash
uv sync
copy .env.example .env
```

Add your key to `.env`:

```text
OPENAI_API_KEY=...
```

Run tests:

```bash
uv run pytest -s
```

Launch the UI:

```bash
uv run streamlit run app.py
```

## Demo Prompts

- When should I use MAE instead of MSE in a regression problem?
- Give me a short study guide about decision trees.
- Why can accuracy be misleading for an imbalanced classification dataset?
- Can you explain convolutional neural networks using the course materials?

The CNN prompt is intentionally out of scope for the current knowledge base. The desired behavior is a grounded insufficiency response, not a generic CNN explanation.

## Testing

The test suite checks that the agent searches and fetches material, cites source ids, answers grounded questions, and refuses unsupported out-of-scope answers.

```bash
uv run pytest -s
```

Current tests include:

- MAE vs MSE tool use and citation behavior.
- Decision tree study-guide grounding.
- CNN out-of-scope insufficiency handling.
- LLM judge criteria for MAE vs MSE grounding.

## Monitoring

The monitored demo script runs representative sessions and uses Logfire when credentials are configured. It remains safe to run locally without Logfire credentials.

```bash
uv run python scripts/run_monitored_sessions.py
```

When Logfire is configured, the workflow is intended to capture session spans, agent run spans, and feedback-style events for review.

## Evaluation

Run a smoke eval:

```bash
uv run python evals/run_evals.py --limit 5
```

Run all scenarios:

```bash
uv run python evals/run_evals.py
```

Run judge alignment:

```bash
uv run python evals/judge.py
uv run python evals/compare_alignment.py --judged evals/results_judged.json --output evals/alignment_report.json

uv run python evals/judge_improved.py
uv run python evals/compare_alignment.py --judged evals/results_judged_improved.json --output evals/alignment_report_improved.json

uv run python evals/judge_calibrated.py
uv run python evals/compare_alignment.py --judged evals/results_judged_calibrated.json --output evals/alignment_report_calibrated.json
```

Known current evaluation metrics:

- 60 scenarios.
- 60 results collected.
- 33 manual labels.
- 32 good / 1 bad.
- Failure category: incomplete.
- Initial judge: accuracy 0.727, precision_bad 0.1, recall_bad 1.0, disagreements 9.
- Improved judge: accuracy 0.576, precision_bad 0.067, recall_bad 1.0, disagreements 14.
- Calibrated judge: accuracy 1.0, precision_bad 1.0, recall_bad 1.0, disagreements 0.

The calibrated judge fixed the disagreement pattern where earlier judges penalized correct insufficiency responses for out-of-scope topics like CNNs. This matters because the project is designed to reward grounded refusal when the course materials do not support a general ML answer.

## Reproducibility

Common commands are available through the Makefile:

```bash
make install
make test
make app
make monitor
make eval-smoke
make eval
make judge
make judge-improved
make summary
```

On Windows without `make`, run the underlying `uv` commands from the Makefile directly.

## Project Self-Evaluation

See [docs/PROJECT_SELF_EVALUATION.md](docs/PROJECT_SELF_EVALUATION.md).

## Limitations

- The knowledge base is intentionally small.
- Retrieval ranking has not yet been compared across multiple approaches.
- Judge labels are still limited.
- There is no cloud deployment unless one is added later.

## Future Work

- Expand the real course-material corpus.
- Add retrieval comparison experiments.
- Add a richer UI with source previews and feedback capture.
- Deploy to cloud.
- Add CI/CD.
- Improve judge calibration with a train/test label split.
