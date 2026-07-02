"""Generate recruiter-facing reasoning strings."""

from __future__ import annotations

from typing import Any

from recruitrank.integrity import safe_float
from recruitrank.structural import consulting_only


def strongest_skills(candidate: dict[str, Any], limit: int = 3) -> list[str]:
    rank = {"expert": 4, "advanced": 3, "intermediate": 2, "beginner": 1}
    skills = sorted(
        candidate.get("skills", []),
        key=lambda s: (
            rank.get(s.get("proficiency"), 0),
            safe_float(s.get("duration_months")),
            safe_float(s.get("endorsements")),
        ),
        reverse=True,
    )
    return [str(s.get("name")) for s in skills[:limit] if s.get("name")]


def build_reasoning(
    candidate: dict[str, Any],
    components: dict[str, float],
    semantic: float,
) -> str:
    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})
    title = profile.get("current_title", "Candidate")
    years = safe_float(profile.get("years_of_experience"))
    location = profile.get("location", "unknown location")
    skills = strongest_skills(candidate)
    skill_text = ", ".join(skills) if skills else "relevant technical skills"
    response = safe_float(signals.get("recruiter_response_rate"))
    notice = int(safe_float(signals.get("notice_period_days")))
    open_flag = "open to work" if signals.get("open_to_work_flag") else "not marked open to work"

    strengths: list[str] = []
    if components.get("career_evidence", 0) >= 0.55:
        strengths.append("strong retrieval/ranking career evidence")
    elif components.get("career_evidence", 0) >= 0.3:
        strengths.append("some search/ML systems experience")
    if components.get("evaluation", 0) >= 0.4:
        strengths.append("ranking evaluation exposure")
    if semantic >= 0.35:
        strengths.append("high semantic alignment to JD")
    if not strengths:
        strengths.append("adjacent technical profile")

    concerns: list[str] = []
    if consulting_only(candidate):
        concerns.append("consulting-only background")
    if notice >= 90:
        concerns.append(f"{notice}-day notice")
    if response < 0.2:
        concerns.append(f"low response rate ({response:.2f})")
    if components.get("penalty", 0) >= 0.2:
        concerns.append("JD trap penalties applied")

    sentence = (
        f"{title} with {years:.1f} years in {location}; top skills include {skill_text}. "
        f"Fit driven by {', '.join(strengths[:2])}; {open_flag}, response rate {response:.2f}, notice {notice} days."
    )
    if concerns:
        sentence += f" Concern: {', '.join(concerns[:2])}."
    text = sentence.replace("\n", " ")
    if len(text) > 300:
        text = text[:297].rsplit(" ", 1)[0] + "..."
    return text
