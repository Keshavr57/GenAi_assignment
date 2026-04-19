"""
database/neon_db.py
-------------------
All NeonDB (PostgreSQL + pgvector) operations.
- Setup tables
- Insert / search document chunks
"""

import json
import os
from typing import Optional, List
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

# Load .env file if it exists (for local development)
# On Render, environment variables are injected directly
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")


def get_connection():
    """Return a fresh psycopg2 connection to NeonDB."""
    return psycopg2.connect(DATABASE_URL)


def setup_database():
    """
    Create the pgvector extension and documents table if they don't exist.
    Called once at server startup.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id        SERIAL PRIMARY KEY,
                    subject   TEXT        NOT NULL,
                    source    TEXT        NOT NULL,
                    chunk     TEXT        NOT NULL,
                    embedding vector(384) NOT NULL
                );
            """)
            # Index for faster similarity search
            cur.execute("""
                CREATE INDEX IF NOT EXISTS documents_embedding_idx
                ON documents USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 50);
            """)
            conn.commit()
    print("✅ NeonDB ready — pgvector table & index confirmed.")


def source_already_indexed(source_key: str) -> bool:
    """Check if a PDF source has already been ingested to avoid duplicates."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM documents WHERE source = %s LIMIT 1",
                (source_key,)
            )
            return cur.fetchone() is not None


def insert_document_chunk(subject: str, source: str, chunk: str, embedding: list):
    """Insert a single text chunk with its vector embedding."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO documents (subject, source, chunk, embedding)
                VALUES (%s, %s, %s, %s::vector)
                """,
                (subject, source, chunk, json.dumps(embedding))
            )
            conn.commit()


def search_similar_chunks(query_embedding: list, subject: Optional[str], top_k: int = 6) -> list:
    """
    Cosine similarity search using pgvector.
    If subject is provided, filters by subject.
    Returns list of (subject, source, chunk, distance).
    """
    emb_str = json.dumps(query_embedding)
    with get_connection() as conn:
        with conn.cursor() as cur:
            if subject:
                cur.execute(
                    """
                    SELECT subject, source, chunk,
                           embedding <=> %s::vector AS dist
                    FROM documents
                    WHERE subject = %s
                    ORDER BY dist
                    LIMIT %s
                    """,
                    (emb_str, subject, top_k)
                )
            else:
                cur.execute(
                    """
                    SELECT subject, source, chunk,
                           embedding <=> %s::vector AS dist
                    FROM documents
                    ORDER BY dist
                    LIMIT %s
                    """,
                    (emb_str, top_k)
                )
            return cur.fetchall()


def get_indexed_stats() -> List[dict]:
    """Return chunk count per subject for the stats endpoint."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT subject, COUNT(*) as chunks FROM documents GROUP BY subject ORDER BY subject"
            )
            rows = cur.fetchall()
    return [{"subject": row[0], "chunks": row[1]} for row in rows]
