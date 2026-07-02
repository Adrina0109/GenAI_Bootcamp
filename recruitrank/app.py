"""Streamlit sandbox for recruiter demo."""

from __future__ import annotations

import io
import json
import tempfile
from pathlib import Path

import streamlit as st

from recruitrank.pipeline import rank_pool, write_submission

st.set_page_config(page_title="FitRank AI", layout="wide")
st.title("FitRank AI — Candidate Ranking Sandbox")
st.caption("Upload up to 200 candidate profiles and get an instant ranked shortlist.")

uploaded = st.file_uploader("Upload candidates JSON or JSONL", type=["json", "jsonl"])
use_embeddings = st.checkbox("Use sentence-transformer embeddings (slower)", value=False)
top_k = st.slider("Top K", min_value=5, max_value=100, value=min(100, 50))

if uploaded:
    raw = uploaded.read().decode("utf-8")
    if uploaded.name.endswith(".jsonl"):
        candidates = [json.loads(line) for line in raw.splitlines() if line.strip()]
    else:
        data = json.loads(raw)
        candidates = data if isinstance(data, list) else [data]

    st.write(f"Loaded **{len(candidates)}** candidates")
    if st.button("Rank candidates"):
        with st.spinner("Scoring..."):
            results = rank_pool(candidates[:200], use_embeddings=use_embeddings, top_k=min(top_k, len(candidates)))
        rows = [
            {
                "rank": i + 1,
                "candidate_id": r.candidate_id,
                "score": r.score,
                "reasoning": r.reasoning,
                **{f"_{k}": v for k, v in r.breakdown.items()},
            }
            for i, r in enumerate(results)
        ]
        st.dataframe(rows, use_container_width=True)

        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as tmp:
            write_submission(results, tmp.name)
            csv_bytes = Path(tmp.name).read_bytes()
        st.download_button("Download CSV", csv_bytes, file_name="submission.csv", mime="text/csv")
