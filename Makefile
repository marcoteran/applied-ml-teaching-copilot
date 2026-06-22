install:
	uv sync

test:
	uv run pytest -s

app:
	uv run streamlit run app.py

monitor:
	uv run python scripts/run_monitored_sessions.py

eval-smoke:
	uv run python evals/run_evals.py --limit 5 --output evals/results_smoke.json

eval:
	uv run python evals/run_evals.py

label:
	uv run python evals/label_evals_cli.py

judge:
	uv run python evals/judge.py
	uv run python evals/compare_alignment.py --judged evals/results_judged.json --output evals/alignment_report.json

judge-improved:
	uv run python evals/judge_improved.py
	uv run python evals/compare_alignment.py --judged evals/results_judged_improved.json --output evals/alignment_report_improved.json

summary:
	uv run python evals/summarize_capstone6.py

demo:
	uv run python scripts/run_monitored_sessions.py
	uv run python evals/summarize_capstone6.py
