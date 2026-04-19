"""
CBSE 10th Grade RAG Backend
FastAPI + NeonDB (pgvector) + Groq
"""

import os, re, json
from pathlib import Path
from typing import Optional

import numpy as np
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

# ── ENV ──────────────────────────────────────────────────────────────────────
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

DB_URL   = os.getenv("DATABASE_URL")
GROQ_KEY = os.getenv("GORQ_API_KEY")   # note: env uses "GORQ" (typo in .env)

# ── MODELS ───────────────────────────────────────────────────────────────────
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
groq_client = Groq(api_key=GROQ_KEY)

app = FastAPI(title="CBSE 10th RAG API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

RESOURCES_DIR = Path(__file__).parent / "Resources"

# Subject map: display name → folder list
SUBJECT_FOLDERS = {
    "Mathematics": ["Maths Solution", "Maths Ncrt", "Maths Ncrt 2"],
    "Science":     ["Science Solution", "Science ncrt"],
    "English":     ["English Solution", "Englsih Ncrt"],
    "SST":         ["SST Solution", "sst ncrt"],
}

SUBJECT_COLOR = {
    "Mathematics": "🔵",
    "Science":     "🟢",
    "English":     "🟡",
    "SST":         "🔴",
}

# ── DB HELPERS ───────────────────────────────────────────────────────────────
def get_conn():
    return psycopg2.connect(DB_URL)


def setup_db():
    """Create table once (uses pgvector extension in Neon)."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            # Enable vector extension (already available in Neon)
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id        SERIAL PRIMARY KEY,
                    subject   TEXT,
                    source    TEXT,
                    chunk     TEXT,
                    embedding vector(384)
                );
            """)
            conn.commit()
    print("✅ DB ready")


def insert_chunk(subject: str, source: str, chunk: str, embedding: list):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO documents (subject, source, chunk, embedding) VALUES (%s,%s,%s,%s::vector)",
                (subject, source, chunk, json.dumps(embedding))
            )
            conn.commit()


def chunk_exists(source: str) -> bool:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM documents WHERE source=%s LIMIT 1", (source,))
            return cur.fetchone() is not None


def search_chunks(query_emb: list, subject: Optional[str], top_k: int = 6):
    emb_str = json.dumps(query_emb)
    with get_conn() as conn:
        with conn.cursor() as cur:
            if subject:
                cur.execute("""
                    SELECT subject, source, chunk,
                           embedding <=> %s::vector AS dist
                    FROM documents
                    WHERE subject = %s
                    ORDER BY dist
                    LIMIT %s
                """, (emb_str, subject, top_k))
            else:
                cur.execute("""
                    SELECT subject, source, chunk,
                           embedding <=> %s::vector AS dist
                    FROM documents
                    ORDER BY dist
                    LIMIT %s
                """, (emb_str, top_k))
            return cur.fetchall()


# ── PDF INGESTION ─────────────────────────────────────────────────────────────
def extract_text_from_pdf(pdf_path: Path) -> str:
    try:
        reader = PdfReader(str(pdf_path))
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text
    except Exception as e:
        print(f"⚠️  Skipping {pdf_path.name}: {e}")
        return ""


def split_into_chunks(text: str, chunk_size: int = 600, overlap: int = 100) -> list:
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunk = " ".join(words[i : i + chunk_size])
        if len(chunk.strip()) > 50:   # skip tiny fragments
            chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def ingest_all_pdfs():
    """Walk Resources folder and embed every PDF into NeonDB (skip if already done)."""
    total_inserted = 0
    for subject, folders in SUBJECT_FOLDERS.items():
        for folder_name in folders:
            folder = RESOURCES_DIR / folder_name
            if not folder.exists():
                continue
            for pdf_path in folder.glob("**/*.pdf"):
                source_key = f"{subject}::{pdf_path.name}"
                if chunk_exists(source_key):
                    print(f"  ⏭  Already indexed: {pdf_path.name}")
                    continue
                print(f"  📄 Indexing: {pdf_path.name} [{subject}]")
                text = extract_text_from_pdf(pdf_path)
                if not text:
                    continue
                chunks = split_into_chunks(text)
                embeddings = embed_model.encode(chunks, show_progress_bar=False)
                for chunk, emb in zip(chunks, embeddings):
                    insert_chunk(subject, source_key, chunk, emb.tolist())
                    total_inserted += 1
    print(f"✅ Ingestion done — {total_inserted} new chunks inserted.")


# ── GROQ ANSWER ───────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert CBSE Board Exam Topper Mentor for Class 10 students.
Your goal is to give the BEST possible answer to score maximum marks in CBSE board exams.

When answering, ALWAYS follow this structure:
1. 📌 **Quick Concept** – 1-line core idea
2. 📝 **Detailed Explanation** – Step-by-step, well-structured answer as expected in a board exam
3. ✅ **Topper's Tip** – Which section/chapter this belongs to, expected marks, and how a topper would present it
4. 🔢 **If Math/Science** – Show all steps, formulas, and calculations clearly
5. 📊 **Marks Breakdown** – Mention how marks are distributed (e.g. formula=1, working=2, answer=1)

Use proper formatting:
- Use **bold** for key terms
- Use numbered steps for procedures
- Use bullet points for lists
- Use > for important notes/tips
- For math equations, write them clearly like: Area = π × r² 

Always answer in the context of the CBSE Class 10 board exam pattern.
Be encouraging, precise, and exam-focused."""


def build_answer(question: str, context_chunks: list, subject: str) -> dict:
    context = "\n\n---\n\n".join([row[2] for row in context_chunks])
    sources = list({row[1].split("::")[-1] for row in context_chunks})

    subject_display = subject if subject else "General"
    user_msg = f"""Subject: {subject_display}
Student's Question: {question}

Relevant context from CBSE textbooks and solved papers:
{context}

Now give a complete, board-exam-ready answer."""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.3,
        max_tokens=1500,
    )
    answer = response.choices[0].message.content
    return {"answer": answer, "sources": sources, "subject": subject_display}


# ── API ROUTES ─────────────────────────────────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str
    subject:  Optional[str] = None


@app.on_event("startup")
async def startup():
    print("🚀 Starting up...")
    setup_db()
    ingest_all_pdfs()


@app.get("/")
def root():
    return {"message": "CBSE 10th RAG API is running 🎓"}


@app.get("/subjects")
def get_subjects():
    return {"subjects": list(SUBJECT_FOLDERS.keys())}


@app.get("/stats")
def get_stats():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT subject, COUNT(*) FROM documents GROUP BY subject ORDER BY subject")
            rows = cur.fetchall()
    return {"stats": [{"subject": r[0], "chunks": r[1]} for r in rows]}


@app.post("/ask")
def ask_question(req: QuestionRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    query_emb = embed_model.encode([req.question])[0].tolist()
    chunks = search_chunks(query_emb, req.subject, top_k=6)
    if not chunks:
        raise HTTPException(status_code=404, detail="No relevant content found. Please ingest PDFs first.")
    result = build_answer(req.question, chunks, req.subject or "")
    return result


@app.post("/ingest")
def trigger_ingest():
    """Manually trigger re-ingestion."""
    ingest_all_pdfs()
    return {"message": "Ingestion complete"}
