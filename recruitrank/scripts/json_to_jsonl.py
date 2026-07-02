#!/usr/bin/env python3
"""Convert sample JSON array to JSONL for CLI testing."""

import json
import sys
from pathlib import Path


def main() -> None:
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "data/sample_candidates.json")
    dst = Path(sys.argv[2] if len(sys.argv) > 2 else "data/sample_candidates.jsonl")
    data = json.loads(src.read_text(encoding="utf-8"))
    with dst.open("w", encoding="utf-8") as handle:
        for row in data:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(data)} rows to {dst}")


if __name__ == "__main__":
    main()
