"""Behavioral and availability scoring from Redrob platform signals."""

from __future__ import annotations

import math
from typing import Any

from recruitrank.config import BEHAVIORAL_CEILING, BEHAVIORAL_FLOOR, REFERENCE_DATE
from recruitrank.integrity import parse_date, safe_float


def behavioral_multiplier(candidate: dict[str, Any]) -> float:
    signals = candidate.get("redrob_signals", {})
    last_active = parse_date(signals.get("last_active_date"))
    if last_active:
        days_inactive = max(0, (REFERENCE_DATE - last_active).days)
        recency = max(0.35, 1.0 - days_inactive / 200.0)
    else:
        recency = 0.2

    response = safe_float(signals.get("recruiter_response_rate"))
    response_score = 0.55 + 0.45 * min(response, 1.0)

    open_to_work = 1.0 if signals.get("open_to_work_flag") else 0.55
    interview = safe_float(signals.get("interview_completion_rate"), 0.5)
    profile_complete = safe_float(signals.get("profile_completeness_score"), 70) / 100.0
    saved = min(1.0, math.log1p(safe_float(signals.get("saved_by_recruiters_30d"))) / math.log(6))
    apps = 1.0 if safe_float(signals.get("applications_submitted_30d")) > 0 else 0.0

    raw = (
        0.24 * recency
        + 0.22 * response_score
        + 0.18 * open_to_work
        + 0.12 * interview
        + 0.10 * profile_complete
        + 0.08 * saved
        + 0.06 * apps
    )
    return max(BEHAVIORAL_FLOOR, min(BEHAVIORAL_CEILING, raw))


def logistics_score(candidate: dict[str, Any]) -> float:
    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})
    location = str(profile.get("location", "")).lower()
    country = str(profile.get("country", "")).lower()
    notice = safe_float(signals.get("notice_period_days"), 90)

    if country == "india":
        if any(c in location for c in ("pune", "noida")):
            loc = 1.0
        elif any(c in location for c in ("delhi", "gurgaon", "gurugram", "mumbai", "hyderabad", "bangalore", "bengaluru")):
            loc = 0.85
        elif signals.get("willing_to_relocate"):
            loc = 0.72
        else:
            loc = 0.45
    elif signals.get("willing_to_relocate"):
        loc = 0.25
    else:
        loc = 0.12

    if notice <= 30:
        notice_s = 1.0
    elif notice <= 60:
        notice_s = 0.78
    elif notice <= 90:
        notice_s = 0.55
    else:
        notice_s = 0.25

    mode = signals.get("preferred_work_mode", "")
    mode_s = {"hybrid": 1.0, "flexible": 0.9, "onsite": 0.8, "remote": 0.5}.get(mode, 0.65)
    return 0.5 * loc + 0.35 * notice_s + 0.15 * mode_s
