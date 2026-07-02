"""Structural fit scoring against JD requirements."""

from __future__ import annotations

import math
import re
from typing import Any

from recruitrank.config import (
    CONSULTING_FIRMS,
    EXP_HARD_FLOOR,
    EXP_IDEAL_HI,
    EXP_IDEAL_LO,
    EXP_SOFT_HI,
    EXP_SOFT_LO,
    JD_SKILLS,
    ML_TITLE_TERMS,
    NON_TECH_TITLE_TERMS,
    PENALTY_CONSULTING_ONLY,
    PENALTY_CV_ONLY,
    PENALTY_KEYWORD_STUFFER,
    PENALTY_LANGCHAIN_ONLY,
    PENALTY_NON_CODING_LEAD,
    PENALTY_RESEARCH_ONLY,
    PENALTY_TITLE_CHASER,
    PRODUCTION_EVIDENCE_TERMS,
    RETRIEVAL_EVIDENCE_TERMS,
    STRUCT_WEIGHTS,
    TIER_1_COMPANIES,
)
from recruitrank.behavioral import logistics_score
from recruitrank.integrity import safe_float
from recruitrank.loader import career_text


def _contains(text: str, term: str) -> bool:
    if " " in term or "-" in term:
        return term in text
    return re.search(rf"\b{re.escape(term)}\b", text) is not None


def _count_terms(text: str, terms: tuple[str, ...] | set[str]) -> int:
    return sum(1 for t in terms if _contains(text, t))


def experience_score(years: float) -> float:
    if years < EXP_HARD_FLOOR:
        return 0.1
    if EXP_IDEAL_LO <= years <= EXP_IDEAL_HI:
        return 1.0
    if EXP_SOFT_LO <= years < EXP_IDEAL_LO:
        return 0.72
    if EXP_IDEAL_HI < years <= EXP_SOFT_HI:
        return 0.68
    return max(0.2, math.exp(-((years - 7.0) ** 2) / 18.0))


def title_domain_score(candidate: dict[str, Any]) -> float:
    title = str(candidate.get("profile", {}).get("current_title", "")).lower()
    if any(t in title for t in NON_TECH_TITLE_TERMS):
        return 0.05
    score = 0.0
    if any(t in title for t in ML_TITLE_TERMS):
        score = 0.92
    elif any(t in title for t in ("engineer", "scientist", "developer", "sde", "swe")):
        score = 0.55
    else:
        score = 0.2
    if "senior" in title or "lead" in title:
        score = min(1.0, score + 0.08)
    return score


def career_evidence_score(candidate: dict[str, Any]) -> float:
    text = career_text(candidate)
    retrieval = _count_terms(text, RETRIEVAL_EVIDENCE_TERMS)
    production = _count_terms(text, PRODUCTION_EVIDENCE_TERMS)
    tier_bonus = 0.0
    for role in candidate.get("career_history", []):
        company = str(role.get("company", "")).lower()
        if any(t in company for t in TIER_1_COMPANIES):
            tier_bonus = 0.12
            break
    raw = min(retrieval, 6) * 0.14 + min(production, 4) * 0.1 + tier_bonus
    return min(1.0, raw)


def skills_trust_score(candidate: dict[str, Any]) -> float:
    prof_w = {"beginner": 0.2, "intermediate": 0.5, "advanced": 0.8, "expert": 1.0}
    total = 0.0
    for skill in candidate.get("skills", []):
        name = str(skill.get("name", "")).lower()
        if not any(j in name for j in JD_SKILLS):
            continue
        prof = prof_w.get(skill.get("proficiency"), 0.35)
        dur = min(1.0, safe_float(skill.get("duration_months")) / 36.0)
        end = min(1.0, math.log1p(safe_float(skill.get("endorsements"))) / math.log(40))
        trust = prof * (0.55 + 0.25 * dur + 0.20 * end)
        total += trust
    return min(1.0, total / 4.5)


def evaluation_score(candidate: dict[str, Any]) -> float:
    text = career_text(candidate)
    terms = ("ndcg", "mrr", "map@", "a/b test", "ab test", "offline eval", "ranking metric")
    hits = sum(1 for t in terms if t in text)
    return min(1.0, hits / 2.5)


def consulting_only(candidate: dict[str, Any]) -> bool:
    career = candidate.get("career_history", [])
    if not career:
        return False
    hits = 0
    for role in career:
        company = str(role.get("company", "")).lower()
        industry = str(role.get("industry", "")).lower()
        if any(c in company for c in CONSULTING_FIRMS) or industry in ("it services", "consulting"):
            hits += 1
    return hits == len(career)


def keyword_stuffer(candidate: dict[str, Any]) -> bool:
    title = str(candidate.get("profile", {}).get("current_title", "")).lower()
    if not any(t in title for t in NON_TECH_TITLE_TERMS):
        return False
    ai_skills = sum(
        1 for s in candidate.get("skills", [])
        if any(j in str(s.get("name", "")).lower() for j in JD_SKILLS)
    )
    return ai_skills >= 5


def title_chaser(candidate: dict[str, Any]) -> bool:
    career = candidate.get("career_history", [])
    if len(career) < 4:
        return False
    durations = [safe_float(r.get("duration_months")) for r in career if safe_float(r.get("duration_months")) > 0]
    if not durations:
        return False
    return sum(durations) / len(durations) < 18


def research_only(candidate: dict[str, Any]) -> bool:
    text = career_text(candidate) + " " + str(candidate.get("profile", {}).get("summary", "")).lower()
    if not any(w in text for w in ("research", "phd", "postdoc", "university", "academic")):
        return False
    return _count_terms(text, PRODUCTION_EVIDENCE_TERMS) == 0


def cv_only(candidate: dict[str, Any]) -> bool:
    text = career_text(candidate)
    cv_terms = ("computer vision", "speech recognition", "robotics", "object detection", "tts", "asr")
    nlp_terms = ("nlp", "retrieval", "search", "ranking", "llm", "embedding")
    return any(t in text for t in cv_terms) and not any(t in text for t in nlp_terms)


def langchain_only(candidate: dict[str, Any]) -> bool:
    skills = candidate.get("skills", [])
    wrappers = {"langchain", "chatgpt", "prompt engineering"}
    foundations = {"retrieval", "ranking", "faiss", "embedding", "pytorch", "nlp", "information retrieval"}
    has_wrap = any(any(w in str(s.get("name", "")).lower() for w in wrappers) for s in skills)
    has_base = _count_terms(career_text(candidate), foundations) >= 2
    years = safe_float(candidate.get("profile", {}).get("years_of_experience"))
    return has_wrap and not has_base and years < 5


def non_coding_lead(candidate: dict[str, Any]) -> bool:
    career = candidate.get("career_history", [])
    current = next((r for r in career if r.get("is_current") or r.get("end_date") is None), None)
    if not current:
        return False
    title = str(current.get("title", "")).lower()
    desc = str(current.get("description", "")).lower()
    dur = safe_float(current.get("duration_months"))
    if dur < 18:
        return False
    mgmt = any(w in title for w in ("manager", "director", "architect", "head of", "vp"))
    coding = any(w in desc for w in ("implemented", "built", "coded", "python", "shipped", "deployed"))
    return mgmt and not coding


def structural_score(candidate: dict[str, Any]) -> tuple[float, dict[str, float], float]:
    profile = candidate.get("profile", {})
    years = safe_float(profile.get("years_of_experience"))

    components = {
        "title_domain": title_domain_score(candidate),
        "career_evidence": career_evidence_score(candidate),
        "experience_band": experience_score(years),
        "skills_trust": skills_trust_score(candidate),
        "evaluation": evaluation_score(candidate),
        "logistics": logistics_score(candidate),
    }
    weighted = sum(components[k] * STRUCT_WEIGHTS[k] for k in components)

    penalty = 0.0
    if consulting_only(candidate):
        penalty += PENALTY_CONSULTING_ONLY
    if keyword_stuffer(candidate):
        penalty += PENALTY_KEYWORD_STUFFER
    if title_chaser(candidate):
        penalty += PENALTY_TITLE_CHASER
    if research_only(candidate):
        penalty += PENALTY_RESEARCH_ONLY
    if cv_only(candidate):
        penalty += PENALTY_CV_ONLY
    if langchain_only(candidate):
        penalty += PENALTY_LANGCHAIN_ONLY
    if non_coding_lead(candidate):
        penalty += PENALTY_NON_CODING_LEAD

    skill_ev = components["skills_trust"]
    career_ev = components["career_evidence"]
    if skill_ev > 0.6 and career_ev < 0.2:
        penalty += 0.15

    final = max(0.0, min(1.0, weighted - penalty))
    components["penalty"] = penalty
    return final, components, penalty
