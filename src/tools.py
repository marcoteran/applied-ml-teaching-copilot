from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from minsearch import Index


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "course_materials.json"


def load_course_materials(data_path: str | None = None) -> list[dict]:
    """Load course material records from JSON."""
    path = Path(data_path) if data_path else DEFAULT_DATA_PATH
    if not path.is_absolute():
        path = PROJECT_ROOT / path

    with path.open("r", encoding="utf-8") as file:
        materials = json.load(file)

    if not isinstance(materials, list):
        raise ValueError("Course materials JSON must contain a list of records.")

    return materials


def build_course_index(materials: list[dict]) -> Index:
    """Build a minsearch index over course material topics and content."""
    index = Index(
        text_fields=["topic", "content"],
        keyword_fields=["module", "lesson", "source_type", "id"],
    )
    index.fit(materials)
    return index


def _make_snippet(text: str, max_chars: int = 260) -> str:
    clean_text = " ".join(str(text).split())
    if len(clean_text) <= max_chars:
        return clean_text
    return clean_text[:max_chars].rsplit(" ", 1)[0] + "..."


class CourseMaterialTools:
    """Tool wrapper around the Applied ML course-material knowledge base."""

    def __init__(self, materials: list[dict] | None = None):
        self.materials = materials if materials is not None else load_course_materials()
        self.index = build_course_index(self.materials)
        self.materials_by_id = {
            material["id"]: material
            for material in self.materials
            if "id" in material
        }
        self.tool_call_history: list[dict[str, Any]] = []

    def reset_history(self) -> None:
        self.tool_call_history.clear()

    def search_course_materials(self, query: str, num_results: int = 5) -> list[dict]:
        safe_num_results = max(1, min(int(num_results), 10))
        results = self.index.search(query, num_results=safe_num_results)

        compact_results = []
        for doc in results:
            compact_results.append(
                {
                    "id": doc["id"],
                    "module": doc["module"],
                    "lesson": doc["lesson"],
                    "topic": doc["topic"],
                    "source_type": doc["source_type"],
                    "content_snippet": _make_snippet(doc["content"]),
                }
            )

        self.tool_call_history.append(
            {
                "tool": "search_course_materials",
                "arguments": {"query": query, "num_results": safe_num_results},
                "result_count": len(compact_results),
                "result_ids": [result["id"] for result in compact_results],
            }
        )

        return compact_results

    def get_course_material(self, material_id: str) -> dict:
        record = self.materials_by_id.get(material_id)

        self.tool_call_history.append(
            {
                "tool": "get_course_material",
                "arguments": {"material_id": material_id},
                "found": record is not None,
            }
        )

        if record is None:
            return {"error": f"No course material found with id '{material_id}'."}

        return record


def create_course_material_tools() -> CourseMaterialTools:
    return CourseMaterialTools()
