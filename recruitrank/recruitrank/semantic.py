"""Semantic similarity scoring."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer

from recruitrank.config import ARTIFACTS_DIR, JD_PATH, JD_QUERY


def build_hash_vectorizer() -> HashingVectorizer:
    return HashingVectorizer(
        n_features=2**18,
        alternate_sign=False,
        norm="l2",
        ngram_range=(1, 2),
        stop_words="english",
    )


def hash_semantic_scores(documents: Sequence[str]) -> np.ndarray:
    vectorizer = build_hash_vectorizer()
    matrix = vectorizer.transform(documents)
    query = vectorizer.transform([JD_QUERY])
    return np.asarray(matrix.dot(query.T).todense()).ravel()


def load_jd_text() -> str:
    if JD_PATH.exists():
        return JD_PATH.read_text(encoding="utf-8")
    return JD_QUERY


def embedding_semantic_scores(documents: Sequence[str], batch_size: int = 256) -> np.ndarray:
    """Optional higher-quality semantic scores using sentence-transformers."""
    from sentence_transformers import SentenceTransformer

    model_path = ARTIFACTS_DIR / "embedding_model"
    model_name = str(model_path) if model_path.exists() else "sentence-transformers/all-MiniLM-L6-v2"
    model = SentenceTransformer(model_name)
    jd = load_jd_text()[:2000]
    jd_vec = model.encode([jd], normalize_embeddings=True)
    doc_vecs = model.encode(list(documents), batch_size=batch_size, normalize_embeddings=True, show_progress_bar=False)
    return np.dot(doc_vecs, jd_vec.T).ravel()
