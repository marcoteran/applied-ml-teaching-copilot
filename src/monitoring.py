from __future__ import annotations

import os
from contextlib import AbstractContextManager

import dotenv
import logfire

_monitoring_configured = False
_openai_instrumentation = None


def configure_monitoring() -> None:
    """Load environment config and initialize Logfire instrumentation safely."""
    global _monitoring_configured
    global _openai_instrumentation
    if _monitoring_configured:
        return

    dotenv.load_dotenv()
    logfire.configure(send_to_logfire="if-token-present")
    _openai_instrumentation = logfire.instrument_openai()
    try:
        _openai_instrumentation.__enter__()
    except Exception:
        _openai_instrumentation = None
    _monitoring_configured = True


def log_agent_event(event_name: str, **attributes: object) -> None:
    """Log a structured agent event to Logfire."""
    logfire.info(event_name, **attributes)


def start_session_span(session_name: str, **attributes: object) -> AbstractContextManager[None]:
    """Start a Logfire session span context manager."""
    return logfire.span(session_name, attributes=attributes)
