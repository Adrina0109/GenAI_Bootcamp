"""Honeypot and profile integrity checks."""

from __future__ import annotations

import re
from datetime import date
from typing import Any

from recruitrank.config import REFERENCE_DATE


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def integrity_multiplier(candidate: dict[str, Any]) -> tuple[float, list[str]]:
    """Return (multiplier, flags). Lower multiplier = worse integrity."""
    profile = candidate.get("profile", {})
    career = candidate.get("career_history", [])
    skills = candidate.get("skills", [])
    signals = candidate.get("redrob_signals", {})
    flags: list[str] = []
    hard = 0
    soft = 0

    expert_zero = sum(
        1 for s in skills
        if s.get("proficiency") == "expert" and safe_float(s.get("duration_months")) <= 1
    )
    if expert_zero >= 3:
        hard += 1
        flags.append("expert_skills_zero_duration")

    years = safe_float(profile.get("years_of_experience"))
    total_months = sum(safe_float(r.get("duration_months")) for r in career)
    if total_months > years * 12 + 24:
        hard += 1
        flags.append("career_span_exceeds_yoe")

    for role in career:
        dur = safe_float(role.get("duration_months"))
        if dur > years * 12 + 6:
            hard += 1
            flags.append("role_longer_than_career")
            break

    signup = parse_date(signals.get("signup_date"))
    last_active = parse_date(signals.get("last_active_date"))
    if signup and last_active and signup > last_active:
        hard += 1
        flags.append("signup_after_last_active")

    for role in career:
        start = parse_date(role.get("start_date"))
        end = parse_date(role.get("end_date"))
        if start and end and end < start:
            hard += 1
            flags.append("role_end_before_start")
            break
        if start and start > REFERENCE_DATE:
            hard += 1
            flags.append("future_start_date")
            break

    summary = (profile.get("summary") or "").lower()
    for role in career:
        desc = (role.get("description") or "").lower()
        company = (role.get("company") or "").lower()
        blob = f"{company} {desc} {summary}"
        founding_year = None
        match = re.search(r"founded\s+(?:in\s+)?(\d{4})", blob)
        if match:
            founding_year = int(match.group(1))
        else:
            ago = re.search(r"founded\s+(\d+)\s+years\s+ago", blob)
            if ago:
                founding_year = 2026 - int(ago.group(1))
        if founding_year and role.get("start_date"):
            try:
                start_year = int(str(role["start_date"]).split("-")[0])
                if start_year < founding_year:
                    hard += 1
                    flags.append("role_before_company_founded")
                    break
            except ValueError:
                pass

    for skill in skills:
        dur = safe_float(skill.get("duration_months"))
        if dur / 12.0 > years + 2.0:
            soft += 1
            flags.append("skill_duration_exceeds_career")
            break

    if hard >= 2:
        return 0.02, flags
    if hard == 1:
        return 0.08, flags
    if soft:
        return 0.88 ** soft, flags
    return 1.0, flags
