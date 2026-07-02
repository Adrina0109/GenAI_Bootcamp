"""Basic pipeline tests."""

from recruitrank.integrity import integrity_multiplier
from recruitrank.pipeline import rank_pool


def test_honeypot_floor():
    candidate = {
        "candidate_id": "CAND_0000999",
        "profile": {"years_of_experience": 5, "current_title": "ML Engineer", "summary": ""},
        "career_history": [{"duration_months": 80, "description": "built search"}],
        "skills": [
            {"name": "FAISS", "proficiency": "expert", "duration_months": 0, "endorsements": 10},
            {"name": "RAG", "proficiency": "expert", "duration_months": 0, "endorsements": 8},
            {"name": "LoRA", "proficiency": "expert", "duration_months": 0, "endorsements": 6},
        ],
        "redrob_signals": {"open_to_work_flag": True, "recruiter_response_rate": 0.9},
    }
    mult, flags = integrity_multiplier(candidate)
    assert mult <= 0.1
    assert flags


def test_ranking_prefers_retrieval_engineer(sample_path="data/sample_candidates.json"):
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / sample_path
    if not path.exists():
        return
    candidates = json.loads(path.read_text(encoding="utf-8"))
    results = rank_pool(candidates, top_k=5)
    assert results[0].candidate_id == "CAND_0000031"
