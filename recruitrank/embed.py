#!/usr/bin/env python3
"""Optional one-time embedding precompute for faster repeated ranking."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from recruitrank.config import ARTIFACTS_DIR, EMBEDDING_MODEL, JD_PATH
from recruitrank.loader import candidate_document, load_candidates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", default="data/candidates.jsonl")
    parser.add_argument("--batch-size", type=int, default=256)
    args = parser.parse_args()

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    model = SentenceTransformer(EMBEDDING_MODEL)
    model.save(str(ARTIFACTS_DIR / "embedding_model"))

    ids: list[str] = []
    docs: list[str] = []
    for candidate in load_candidates(args.candidates):
        ids.append(candidate["candidate_id"])
        docs.append(candidate_document(candidate))

    jd_text = JD_PATH.read_text(encoding="utf-8")[:2500]
    jd_vec = model.encode([jd_text], normalize_embeddings=True)
    doc_vecs = model.encode(docs, batch_size=args.batch_size, normalize_embeddings=True, show_progress_bar=True)

    np.save(ARTIFACTS_DIR / "candidate_ids.npy", np.array(ids))
    np.save(ARTIFACTS_DIR / "candidate_embeddings.npy", doc_vecs)
    np.save(ARTIFACTS_DIR / "jd_embedding.npy", jd_vec)
    (ARTIFACTS_DIR / "meta.json").write_text(
        json.dumps({"model": EMBEDDING_MODEL, "count": len(ids)}),
        encoding="utf-8",
    )
    print(f"Saved embeddings for {len(ids)} candidates to {ARTIFACTS_DIR}")


if __name__ == "__main__":
    main()
