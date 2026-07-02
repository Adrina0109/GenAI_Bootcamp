"""Candidate loading and text extraction."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


def load_candidates(path: str | Path) -> Iterable[dict[str, Any]]:
    path = Path(path)
    if path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            yield from data
        return
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def candidate_document(candidate: dict[str, Any]) -> str:
    profile = candidate.get("profile", {})
    parts = [
        profile.get("headline", ""),
        profile.get("summary", ""),
        profile.get("current_title", ""),
        profile.get("current_company", ""),
        profile.get("current_industry", ""),
    ]
    for role in candidate.get("career_history", []):
        parts.extend([
            role.get("company", ""),
            role.get("title", ""),
            role.get("industry", ""),
            (role.get("description", "") or "")[:400],
        ])
    for skill in candidate.get("skills", []):
        parts.append(skill.get("name", ""))
    return " ".join(str(p) for p in parts if p).strip()


def career_text(candidate: dict[str, Any]) -> str:
    chunks: list[str] = []
    for role in candidate.get("career_history", []):
        chunks.append(f"{role.get('title', '')} {role.get('description', '')}")
    return " ".join(chunks).lower()
