from __future__ import annotations

import asyncio
import inspect
import json
import os
import re
from typing import Any

import streamlit as st


def _bridge_streamlit_secrets_to_env() -> None:
    try:
        for key in ("OPENAI_API_KEY", "LOGFIRE_TOKEN", "LOGFIRE_READ_TOKEN"):
            if key in st.secrets and not os.getenv(key):
                os.environ[key] = str(st.secrets[key])
    except Exception:
        return


_bridge_streamlit_secrets_to_env()

from src.teaching_agent import run_teaching_copilot


EXAMPLE_PROMPTS = [
    "When should I use MAE instead of MSE in a regression problem?",
    "Give me a short study guide about decision trees.",
    "Why can accuracy be misleading for an imbalanced classification dataset?",
    "Can you explain convolutional neural networks using the course materials?",
]


def _call_agent(prompt: str) -> dict[str, Any]:
    result = run_teaching_copilot(prompt)
    if inspect.isawaitable(result):
        try:
            return asyncio.run(result)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(result)
            finally:
                loop.close()
    return result


def _material_ids(result: dict[str, Any], answer: str) -> list[str]:
    ids: set[str] = set(re.findall(r"aml-\d{3}", answer or ""))
    for call in result.get("tool_call_history", []):
        for material_id in call.get("result_ids", []) or []:
            ids.add(material_id)
        arguments = call.get("arguments", {}) or {}
        if arguments.get("material_id"):
            ids.add(arguments["material_id"])
    return sorted(ids)


def _is_insufficient(answer: str) -> bool:
    text = answer.lower()
    return "insufficient" in text and "course material" in text


st.set_page_config(
    page_title="Applied ML Teaching Copilot",
    page_icon="",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; }
    .copilot-card {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        background: #ffffff;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        margin-bottom: 1rem;
    }
    .material-id {
        display: inline-block;
        border: 1px solid #cbd5e1;
        border-radius: 999px;
        padding: 0.18rem 0.55rem;
        margin: 0.1rem 0.2rem 0.1rem 0;
        font-size: 0.85rem;
        background: #f8fafc;
        color: #0f172a;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Applied ML Teaching Copilot")
st.caption("A grounded AI assistant for Applied Machine Learning course materials.")

with st.sidebar:
    st.header("Project")
    st.markdown(
        """
        This capstone agent searches a small Applied ML course-material knowledge
        base, fetches source records, and answers only from retrieved material.
        """
    )

    st.header("Try a Prompt")
    selected_prompt = st.selectbox("Example prompts", EXAMPLE_PROMPTS, label_visibility="collapsed")
    if st.button("Use selected prompt", use_container_width=True):
        st.session_state.pending_prompt = selected_prompt

    st.header("Local Usage")
    st.code(
        "uv sync\n"
        "uv run pytest -s\n"
        "uv run streamlit run app.py\n"
        "uv run python evals/run_evals.py --limit 5",
        language="bash",
    )

    st.header("Grounding")
    st.info(
        "The agent should cite material ids when it answers. If retrieved course "
        "materials are insufficient, it should say so instead of filling gaps with "
        "general model knowledge."
    )

for key, default in {
    "messages": [],
    "last_result": None,
    "pending_prompt": None,
}.items():
    st.session_state.setdefault(key, default)

st.markdown(
    """
    <div class="copilot-card">
    Ask a course-grounded Applied ML question. The reviewer panels below expose
    tool calls, fetched material ids, and the raw agent result for reproducibility.
    </div>
    """,
    unsafe_allow_html=True,
)

cols = st.columns(4)
for index, prompt in enumerate(EXAMPLE_PROMPTS):
    with cols[index]:
        if st.button(prompt, use_container_width=True):
            st.session_state.pending_prompt = prompt

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.session_state.pending_prompt or st.chat_input("Ask about the course materials")
st.session_state.pending_prompt = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching course materials and composing a grounded answer..."):
            try:
                result = _call_agent(prompt)
                answer = result.get("final_answer", "")
            except Exception as exc:
                result = {"error": str(exc), "final_answer": ""}
                answer = f"Agent run failed: {exc}"

        if _is_insufficient(answer):
            st.warning(answer)
        else:
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.last_result = result

last_result = st.session_state.last_result
if last_result:
    answer = last_result.get("final_answer", "")
    ids = _material_ids(last_result, answer)

    with st.expander("Tool calls", expanded=True):
        st.json(last_result.get("tool_call_history", []))

    with st.expander("Fetched material ids", expanded=True):
        if ids:
            st.markdown(" ".join(f'<span class="material-id">{material_id}</span>' for material_id in ids), unsafe_allow_html=True)
        else:
            st.write("No material ids were returned.")

    with st.expander("Raw result"):
        st.code(json.dumps(last_result, indent=2, default=str), language="json")
