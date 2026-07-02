# FitRank AI — Intelligent Candidate Discovery & Ranking

Hybrid AI ranker for the **India Runs / Redrob Data & AI Challenge** (Track 1). Ranks 100,000 candidate profiles against the Senior AI Engineer JD using semantic understanding, structural JD rules, behavioral signals, and honeypot detection — not keyword matching.

## What it does

- **Understands the JD** — extracts must-haves (retrieval, embeddings, vector search, evaluation) and explicit disqualifiers (consulting-only, research-only, keyword stuffing).
- **Reads the full profile** — career history evidence outweighs skills-list buzzwords.
- **Weighs behavioral signals** — inactive or low-response candidates are down-ranked even if the resume looks perfect.
- **Produces a trusted shortlist** — `submission.csv` with rank, score, and grounded reasoning per candidate.

## Quick start

```bash
cd recruitrank
pip install -r requirements.txt

# Place organizer dataset (not in repo due to size ~487MB)
# cp /path/to/candidates.jsonl data/

python rank.py --candidates data/candidates.jsonl --out submission.csv --stream
python data/validate_submission.py submission.csv
```

### Sandbox (50 sample candidates)

```bash
python scripts/json_to_jsonl.py data/sample_candidates.json data/sample_candidates.jsonl
python rank.py --candidates data/sample_candidates.jsonl --out output/sample_ranking.csv --top-k 50
```

### Optional: higher-quality semantic embeddings

```bash
python embed.py --candidates data/candidates.jsonl   # one-time precompute
python rank.py --candidates data/candidates.jsonl --out submission.csv --embeddings --stream
```

### Streamlit demo

```bash
streamlit run app.py
```

## Architecture

```
candidates.jsonl
      │
      ▼
┌─────────────────────────────────────┐
│  Integrity (honeypots, date traps)  │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│  Structural score (65%)             │
│  title · career evidence · skills   │
│  experience · evaluation · logistics│
│  + JD trap penalties                │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│  Semantic score (35%)               │
│  HashingVectorizer or MiniLM        │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│  × Behavioral multiplier            │
│  × Integrity multiplier             │
└─────────────────┬───────────────────┘
                  ▼
           submission.csv (top 100)
```

## Scoring highlights

| Signal | Why it matters |
|--------|----------------|
| Career evidence | Catches plain-language fits who shipped search/reco without trendy keywords |
| Skill trust | `proficiency × duration × endorsements` defeats keyword stuffers |
| Trap penalties | Consulting-only, CV-only, LangChain-only, title-chaser per JD |
| Behavioral | `last_active`, `recruiter_response_rate`, `open_to_work_flag` |
| Honeypots | Date contradictions and impossible durations → near-zero score |

## Project structure

```
recruitrank/
├── rank.py                 # CLI — produce submission CSV
├── embed.py                # Optional embedding precompute
├── app.py                  # Streamlit sandbox
├── recruitrank/            # Core scoring modules
├── data/
│   ├── job_description.txt
│   ├── sample_candidates.json
│   └── validate_submission.py
├── docs/FitRank_Approach.pdf
├── submission.csv          # Generated after running on full dataset
└── submission_metadata.yaml
```

## Deliverables

1. **GitHub repo** — this repository (`recruitrank/`)
2. **Approach PDF** — `docs/FitRank_Approach.pdf` (regenerate: `python scripts/generate_deck.py`)
3. **Ranked output** — `submission.csv` (requires `data/candidates.jsonl` from hackathon organizers)

## Compliance

- CPU-only at ranking time
- No network/API calls during `rank.py`
- Deterministic tie-breaking: higher score first, then `candidate_id` ascending
- Validates against official `validate_submission.py`

## Team

GenAI Bootcamp — Sera, Adrina, Rahul, Senorita, Alan
