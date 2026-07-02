#!/usr/bin/env python3
"""CLI entry point for FitRank candidate ranking."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from recruitrank.pipeline import rank_file, rank_file_streaming, write_submission


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rank candidates for the Redrob Senior AI Engineer JD.",
    )
    parser.add_argument(
        "--candidates",
        default="data/candidates.jsonl",
        help="Path to candidates.jsonl or sample_candidates.json",
    )
    parser.add_argument("--out", default="submission.csv", help="Output CSV path")
    parser.add_argument("--top-k", type=int, default=100, help="Number of ranked rows")
    parser.add_argument(
        "--embeddings",
        action="store_true",
        help="Use sentence-transformer embeddings (slower, higher quality)",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream large JSONL files in batches (recommended for 100K pool)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    path = Path(args.candidates)
    if not path.exists():
        raise SystemExit(
            f"Candidate file not found: {path}\n"
            "Place the organizer-provided candidates.jsonl in data/ and retry."
        )

    started = time.perf_counter()
    if args.stream and path.suffix == ".jsonl":
        results = rank_file_streaming(
            path, top_k=args.top_k, use_embeddings=args.embeddings,
        )
    else:
        results = rank_file(path, top_k=args.top_k, use_embeddings=args.embeddings)

    write_submission(results, args.out)
    elapsed = time.perf_counter() - started
    print(f"Wrote {len(results)} candidates to {args.out} in {elapsed:.2f}s")
    if results:
        top = results[0]
        print(f"Top: {top.candidate_id} score={top.score:.6f}")


if __name__ == "__main__":
    main()
