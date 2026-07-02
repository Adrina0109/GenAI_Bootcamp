"""Central configuration for FitRank — Redrob India Runs candidate ranker."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ARTIFACTS_DIR = ROOT / "artifacts"
JD_PATH = DATA_DIR / "job_description.txt"

REFERENCE_DATE = dt.date(2026, 6, 1)

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# Final score: structural dominates because the JD is rule-heavy.
W_SEMANTIC = 0.35
W_STRUCTURAL = 0.65

STRUCT_WEIGHTS = {
    "title_domain": 0.28,
    "career_evidence": 0.32,
    "experience_band": 0.12,
    "skills_trust": 0.14,
    "evaluation": 0.08,
    "logistics": 0.06,
}

EXP_IDEAL_LO = 5.0
EXP_IDEAL_HI = 9.0
EXP_SOFT_LO = 4.0
EXP_SOFT_HI = 11.0
EXP_HARD_FLOOR = 3.0

BEHAVIORAL_FLOOR = 0.35
BEHAVIORAL_CEILING = 1.12

INTEGRITY_FATAL = 0.02
INTEGRITY_HARD = 0.08
INTEGRITY_SOFT_DECAY = 0.88

PENALTY_CONSULTING_ONLY = 0.22
PENALTY_RESEARCH_ONLY = 0.28
PENALTY_TITLE_CHASER = 0.55
PENALTY_CV_ONLY = 0.45
PENALTY_KEYWORD_STUFFER = 0.08
PENALTY_LANGCHAIN_ONLY = 0.20
PENALTY_NON_CODING_LEAD = 0.18

JD_SKILLS = {
    "embedding", "embeddings", "sentence-transformers", "bge", "e5",
    "vector", "pinecone", "weaviate", "qdrant", "milvus", "faiss",
    "opensearch", "elasticsearch", "bm25", "retrieval", "semantic search",
    "hybrid search", "ranking", "learning to rank", "ltr", "reranking",
    "recommendation", "recommender", "nlp", "llm", "fine-tuning", "lora",
    "qlora", "peft", "rag", "python", "pytorch", "transformers",
    "ndcg", "mrr", "a/b testing", "xgboost",
}

RETRIEVAL_EVIDENCE_TERMS = (
    "retrieval", "ranking", "search", "recommendation", "recommender",
    "embedding", "vector", "semantic", "relevance", "bm25", "elasticsearch",
    "opensearch", "faiss", "pinecone", "weaviate", "qdrant", "milvus",
    "information retrieval", "learning to rank", "rerank", "two-tower",
    "ndcg", "personalization", "query understanding", "matching engine",
)

PRODUCTION_EVIDENCE_TERMS = (
    "production", "shipped", "deployed", "launched", "real users", "scale",
    "latency", "a/b", "monitoring", "served", "in prod", "rollout",
)

ML_TITLE_TERMS = (
    "machine learning", "ml engineer", "ai engineer", "data scientist",
    "applied scientist", "nlp", "search", "relevance", "recommendation",
    "information retrieval", "deep learning", "llm",
)

NON_TECH_TITLE_TERMS = (
    "marketing", "sales", "hr manager", "human resources", "recruiter",
    "accountant", "finance", "operations manager", "customer support",
    "business analyst", "project manager", "product manager", "graphic designer",
    "content writer", "civil engineer", "mechanical engineer", "teacher",
)

CONSULTING_FIRMS = (
    "tcs", "tata consultancy", "infosys", "wipro", "accenture", "cognizant",
    "capgemini", "hcl", "tech mahindra", "mindtree", "ltimindtree", "mphasis",
    "ibm global services", "dxc", "ntt data", "genpact", "deloitte",
)

TIER_1_COMPANIES = frozenset({
    "google", "meta", "microsoft", "amazon", "salesforce", "nvidia",
    "zomato", "swiggy", "phonepe", "razorpay", "flipkart", "freshworks",
    "postman", "browserstack", "observe.ai", "sarvam", "yellow.ai",
})

LOCATION_PREFERRED = ("pune", "noida")
LOCATION_WELCOME = (
    "hyderabad", "mumbai", "delhi", "gurgaon", "gurugram", "bangalore", "bengaluru",
)

JD_QUERY = (
    "senior ai engineer machine learning embeddings retrieval ranking recommendation "
    "relevance vector search hybrid search semantic search nlp information retrieval "
    "learning to rank ndcg mrr evaluation a/b test production deployed at scale python "
    "sentence transformers bge e5 faiss pinecone qdrant elasticsearch fine-tuning llm "
    "reranking recsys founding team product engineering"
)
