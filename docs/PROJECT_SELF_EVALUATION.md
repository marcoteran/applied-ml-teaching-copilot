# Project Self-Evaluation

## Problem Description

Satisfied. The project addresses a clear teaching and learning problem: students and instructors need a reliable assistant that answers from Applied Machine Learning course materials instead of hallucinating unsupported content.

## Knowledge Base and Retrieval

Satisfied. The project includes a structured course-material knowledge base and retrieval tools over that knowledge base. Retrieval behavior is tested and evaluated through targeted scenarios. Future work includes expanding the corpus with a larger set of real course materials and comparing retrieval ranking approaches.

## Agents and LLM

Satisfied. The project implements an agent loop using the OpenAI Responses API and documented tools. The agent can search course materials, fetch exact material records, and decide when the available material is insufficient.

## Code Organization

Satisfied. The repository is organized as a Python project with `src/`, `tests/`, `scripts/`, `evals/`, `docs/`, notebooks, and data.

## Testing

Satisfied. The project includes unit tests and LLM judge tests that check tool usage, grounding, citations, and out-of-scope behavior.

## Evaluation

Satisfied. The evaluation design includes 60 hand-crafted scenarios, 33 manual labels, and LLM judge alignment metrics. The current known labeled set contains 32 good responses and 1 bad response, with the bad case categorized as incomplete.

## Monitoring

Satisfied. The monitoring workflow is designed around Logfire instrumentation with session spans, agent run spans, and feedback events. The local monitoring script remains optional so the project can still run for reviewers without cloud credentials.

## Reproducibility

Satisfied. The project uses `uv`, includes a Makefile, documents local commands, and provides `.env.example` for required environment variables.

## Best Practices

Satisfied. The project uses `uv`, a modular Python package structure, a Makefile for common workflows, tests, evaluation scripts, and documentation that keeps reviewer setup straightforward.

## Additional Bonus

Satisfied. The project now includes a Streamlit UI that exposes the agent answer, tool calls, fetched material ids, and raw result for reviewer inspection.
