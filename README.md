# GenAI Bootcamp

This repository contains bootcamp session work and the **FitRank AI** candidate ranking system for the India Runs / Redrob Data & AI Challenge.

## FitRank AI (Track 1 — Intelligent Candidate Discovery)

See [`recruitrank/README.md`](recruitrank/README.md) for full documentation.

```bash
cd recruitrank
pip install -r requirements.txt
python rank.py --candidates data/candidates.jsonl --out submission.csv --stream
```

**Deliverables:**
- Code: `recruitrank/`
- Approach deck: `recruitrank/docs/FitRank_Approach.pdf`
- Ranked output: `recruitrank/submission.csv` (generate with organizer `candidates.jsonl`)

## Session materials

Historical bootcamp sessions are in `session*/` folders.
