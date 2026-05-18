# Applied ML Teaching Copilot

An AI Engineering Buildcamp capstone project for helping instructors and students work with the materials of an Applied Machine Learning course.

## The Problem

Technical course content is usually distributed across slides, notebooks, readings, assignments, and instructor notes. This makes it difficult to quickly prepare lectures, answer student questions, or generate reliable study material grounded in the actual course content.

## What It Does

Applied ML Teaching Copilot is an AI assistant that retrieves relevant passages from indexed course materials and uses them to answer questions or generate study-oriented outputs.

A typical interaction might be: the user asks a question such as "When should I use MAE instead of MSE?" or requests an output such as "Create a short study guide about decision trees." The system returns a clear explanation, examples, key points, and guidance based on the retrieved course content.

## Setup

1. Install uv if you don't have it yet: https://docs.astral.sh/uv/getting-started/installation/

2. Clone this repository (or download the zip and extract it).

3. Create a `.env` file from the template and add your API key:

       cp .env.example .env

4. Install dependencies:

       uv sync

5. Start Jupyter:

       uv run jupyter notebook

## Notebooks

- `notebooks/01-setup.ipynb` - smoke test that confirms your environment works
- `notebooks/02-rag.ipynb` - a minimal RAG baseline you can adapt to your own data
- `notebooks/03_agentic_teaching_copilot.ipynb` - an agentic teaching copilot prototype with tools over the course materials

## Capstone Preparation 3: Agentic Teaching Copilot

Notebook path: `notebooks/03_agentic_teaching_copilot.ipynb`

Tools implemented:

- `search_course_materials(query, num_results=5)` searches the Applied Machine Learning course-material index and returns compact results with metadata and snippets.
- `get_course_material(material_id)` retrieves the full course-material record for a selected source id.

How to run:

1. Add `OPENAI_API_KEY` to your `.env` file.
2. Install dependencies with `uv sync`.
3. Start Jupyter with `uv run jupyter notebook`.
4. Open and run `notebooks/03_agentic_teaching_copilot.ipynb`.

What this adds beyond Week 1 RAG:

The Week 1 notebook used a fixed RAG chain: search, build a prompt, call the LLM, and return an answer. The new notebook wraps the course-material knowledge base in tools and implements a custom OpenAI Responses API loop so the model can decide when to search, when to fetch full source material, and when it has enough grounded context to answer.

## Capstone Preparation 4: Tests and Evaluation

This stage adds a small Python package and pytest-based evaluation suite for the capstone agent.

Tests added:

- Regular pytest tests for the teaching agent in `tests/test_agent.py`
- Shared test helpers in `tests/utils.py`
- An LLM judge using Pydantic structured output in `tests/judge.py`
- One LLM judge test in `tests/test_judge.py`
- Optional token usage reporting in `tests/cost_tracker.py` and `tests/conftest.py`

How to run:

    uv run pytest -s

Scenarios covered:

- MAE vs MSE questions should search the course materials, fetch the full `aml-001` record, compare the metrics, and cite the material id.
- Out-of-scope CNN questions should search, avoid unsupported general explanations, and state that the current course materials are insufficient.
- Decision tree study-guide requests should use course materials and cite relevant material ids.

## Capstone Preparation 5: Monitoring and Observability

This update adds Logfire-based tracing and structured event logging for the teaching copilot agent.

Platform used: Logfire

Why:

- Provides traces for agent runs and tool call sequences
- Captures user queries, tool names, fetched material ids, grounded refusals, and answer length
- Enables future token/cost visibility and evaluation data for capstone readiness

What is monitored:

- agent runs
- user queries
- tool calls
- fetched material ids
- grounded refusals
- answer length
- simulated user feedback

How to run:

    uv run python scripts/run_monitored_sessions.py

How this prepares the project for evaluation next week:

- Adds observability to the core agent path without redesigning the agent
- Makes agent behavior easier to inspect and validate during evaluation
- Provides a reproducible session runner for monitored interactions

## Data

Put your project data in the `data/` folder. See `notebooks/02-rag.ipynb` for how to load it.
