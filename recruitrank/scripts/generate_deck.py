#!/usr/bin/env python3
"""Generate approach deck PDF for FitRank."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def build_pdf(out_path: Path) -> None:
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=landscape(letter),
        rightMargin=48,
        leftMargin=48,
        topMargin=42,
        bottomMargin=42,
    )
    styles = getSampleStyleSheet()
    title = ParagraphStyle("Title", parent=styles["Heading1"], fontSize=28, spaceAfter=16, textColor=colors.HexColor("#0f172a"))
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=18, spaceBefore=12, spaceAfter=8, textColor=colors.HexColor("#1d4ed8"))
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=12, leading=16, spaceAfter=8)
    bullet = ParagraphStyle("Bullet", parent=body, leftIndent=18, bulletIndent=6)

    story = []
    story.append(Paragraph("FitRank AI", title))
    story.append(Paragraph("Intelligent Candidate Discovery &amp; Ranking — India Runs / Redrob Challenge", body))
    story.append(Spacer(1, 0.2 * inch))

    sections = [
        ("Problem", [
            "Recruiters screening 100K profiles miss strong fits because keyword filters reward resume stuffing, ignore career evidence, and cannot weigh availability signals.",
            "The Redrob JD explicitly warns against keyword matching — traps include honeypots, consulting-only careers, research-without-production, and inactive candidates.",
        ]),
        ("Design Philosophy", [
            "Rank like a senior recruiter: understand what the role needs, verify evidence in career history, penalize traps, and down-rank unreachable candidates.",
            "Hybrid scoring: structural fit (65%) + semantic JD alignment (35%), multiplied by behavioral availability and integrity checks.",
        ]),
        ("Architecture", [
            "1. Load candidates.jsonl (100K) in streaming batches.",
            "2. Integrity layer flags honeypots (date contradictions, impossible skill durations).",
            "3. Structural scorer evaluates title domain, retrieval/ranking career evidence, trusted skills, experience band, evaluation exposure, logistics.",
            "4. Semantic scorer uses fast hashing TF vectors (default) or optional MiniLM embeddings.",
            "5. Behavioral multiplier uses last_active, response rate, open-to-work, interview completion.",
            "6. Top-100 selected with deterministic tie-break (score desc, candidate_id asc).",
        ]),
        ("Why Not Keywords Alone?", [
            "Career text is weighted higher than skills[] — a Tier-5 engineer who shipped recommenders without buzzwords outranks a Marketing Manager with perfect AI skill lists.",
            "Skill trust uses proficiency × duration × endorsements — keyword stuffers with zero-duration expert skills score near zero.",
            "Consulting-only, CV-only, LangChain-wrapper-only, and title-chaser penalties mirror JD disqualifiers.",
        ]),
        ("Tech Stack", [
            "Python 3.10+, NumPy, scikit-learn HashingVectorizer, optional sentence-transformers.",
            "CPU-only at ranking time; no external API calls; completes within 5-minute budget on 100K profiles.",
        ]),
        ("Outputs", [
            "submission.csv — 100 rows: candidate_id, rank, score, reasoning.",
            "Validated against official validate_submission.py (monotone scores, unique ranks, CAND_XXXXXXX format).",
        ]),
        ("Reproduction", [
            "pip install -r requirements.txt",
            "Place candidates.jsonl in data/",
            "python rank.py --candidates data/candidates.jsonl --out submission.csv --stream",
            "python data/validate_submission.py submission.csv",
        ]),
    ]

    for heading, lines in sections:
        story.append(Paragraph(heading, h2))
        for line in lines:
            story.append(Paragraph(f"• {line}", bullet))
        story.append(Spacer(1, 0.1 * inch))

    story.append(PageBreak())
    story.append(Paragraph("Scoring Formula", h2))
    formula_data = [
        ["Component", "Weight / Role"],
        ["Structural", "65% — title, career evidence, skills trust, experience, evaluation, logistics"],
        ["Semantic", "35% — JD cosine similarity (hashing or embeddings)"],
        ["Behavioral", "Multiplier 0.35–1.12 — recency, response rate, open-to-work"],
        ["Integrity", "Multiplier — honeypot detection floors bad profiles"],
        ["Penalties", "Consulting-only, keyword stuffer, research-only, CV-only, title chaser"],
    ]
    table = Table(formula_data, colWidths=[1.8 * inch, 7.5 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1d4ed8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("Team: GenAI Bootcamp | Track 1: Intelligent Candidate Discovery", body))

    doc.build(story)


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[1] / "docs" / "FitRank_Approach.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    build_pdf(out)
    print(f"Wrote {out}")
