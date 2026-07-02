"""Ranking pipeline orchestration."""

from __future__ import annotations

import csv
import heapq
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from recruitrank.behavioral import behavioral_multiplier
from recruitrank.config import W_SEMANTIC, W_STRUCTURAL
from recruitrank.integrity import integrity_multiplier
from recruitrank.loader import candidate_document, load_candidates
from recruitrank.reasoning import build_reasoning
from recruitrank.semantic import embedding_semantic_scores, hash_semantic_scores
from recruitrank.structural import structural_score


@dataclass(frozen=True)
class RankedCandidate:
    candidate_id: str
    score: float
    reasoning: str
    breakdown: dict[str, float]


def _reverse_id_key(candidate_id: str) -> str:
    return "".join(chr(255 - ord(c)) for c in candidate_id)


def composite_score(structural: float, semantic: float, behavioral: float, integrity: float) -> float:
    base = W_STRUCTURAL * structural + W_SEMANTIC * max(0.0, semantic)
    return max(0.0, min(1.0, base * behavioral * integrity))


def rank_pool(
    candidates: list[dict[str, Any]],
    *,
    use_embeddings: bool = False,
    top_k: int = 100,
) -> list[RankedCandidate]:
    documents = [candidate_document(c) for c in candidates]
    if use_embeddings:
        semantic_scores = embedding_semantic_scores(documents)
    else:
        semantic_scores = hash_semantic_scores(documents)
    if semantic_scores.size:
        lo, hi = semantic_scores.min(), semantic_scores.max()
        if hi > lo:
            semantic_scores = (semantic_scores - lo) / (hi - lo)
        else:
            semantic_scores = np.zeros_like(semantic_scores)

    results: list[RankedCandidate] = []
    for idx, candidate in enumerate(candidates):
        struct, components, _ = structural_score(candidate)
        behavior = behavioral_multiplier(candidate)
        integrity, _ = integrity_multiplier(candidate)
        sem = float(semantic_scores[idx]) if len(semantic_scores) else 0.0
        score = composite_score(struct, sem, behavior, integrity)
        reasoning = build_reasoning(candidate, components, sem)
        breakdown = {**components, "semantic": sem, "behavioral": behavior, "integrity": integrity}
        results.append(
            RankedCandidate(
                candidate_id=candidate["candidate_id"],
                score=round(score, 6),
                reasoning=reasoning,
                breakdown=breakdown,
            )
        )

    results.sort(key=lambda r: (-r.score, r.candidate_id))
    return results[:top_k]


def rank_file(
    candidates_path: str | Path,
    *,
    top_k: int = 100,
    use_embeddings: bool = False,
) -> list[RankedCandidate]:
    candidates = list(load_candidates(candidates_path))
    return rank_pool(candidates, use_embeddings=use_embeddings, top_k=top_k)


def rank_file_streaming(
    candidates_path: str | Path,
    *,
    top_k: int = 100,
    use_embeddings: bool = False,
) -> list[RankedCandidate]:
    """Memory-efficient top-k for large JSONL files."""
    heap: list[tuple[float, str, RankedCandidate]] = []
    batch: list[dict[str, Any]] = []
    batch_size = 5000

    def flush(batch_candidates: list[dict[str, Any]]) -> None:
        for item in rank_pool(batch_candidates, use_embeddings=use_embeddings, top_k=len(batch_candidates)):
            key = (item.score, _reverse_id_key(item.candidate_id), item)
            if len(heap) < top_k:
                heapq.heappush(heap, key)
            elif key > heap[0]:
                heapq.heapreplace(heap, key)

    for candidate in load_candidates(candidates_path):
        batch.append(candidate)
        if len(batch) >= batch_size:
            flush(batch)
            batch = []
    if batch:
        flush(batch)

    ranked = [item[2] for item in heap]
    ranked.sort(key=lambda r: (-r.score, r.candidate_id))
    return ranked


def write_submission(results: list[RankedCandidate], out_path: str | Path) -> None:
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        for rank, result in enumerate(results, start=1):
            writer.writerow([result.candidate_id, rank, f"{result.score:.6f}", result.reasoning])
