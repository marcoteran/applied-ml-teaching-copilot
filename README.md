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

## Data

Put your project data in the `data/` folder. See `notebooks/02-rag.ipynb` for how to load it.
