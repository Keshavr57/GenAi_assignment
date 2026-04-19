"""
agent/groq_agent.py
-------------------
The RAG Agent:
  - Takes a question + retrieved context chunks
  - Builds the perfect board-exam prompt
  - Calls Groq LLaMA-3.3-70B
  - Returns a formatted topper-quality answer
"""

import os
from typing import Optional
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

_groq_client = None


def get_groq_client() -> Groq:
    """Lazy-init Groq client."""
    global _groq_client
    if _groq_client is None:
        api_key = os.getenv("GORQ_API_KEY")
        if not api_key:
            raise ValueError("GORQ_API_KEY is not set in environment!")
        _groq_client = Groq(api_key=api_key)
    return _groq_client


# ── System Prompt ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert CBSE Board Exam Topper Mentor for Class 10 students in India.
Your goal is to help students score MAXIMUM MARKS in their CBSE board exams.

ALWAYS structure your answer EXACTLY like this:

---

## 📌 Quick Concept
*One-line core idea of what this question is asking.*

---

## 📝 Board-Exam Answer

Write a complete, detailed, step-by-step answer exactly as a top student would write in the board exam.
- Use **bold** for key terms and formulas
- Use numbered steps for processes and derivations
- Use bullet points for lists of points
- For Math/Science: show ALL working steps clearly
  - Write formulas like: Area = π × r²
  - Show substitution: Area = 3.14 × (7)² = 153.86 cm²
- For diagrams needed: write [DIAGRAM: describe what to draw]
- Write as if this answer is worth full marks

---

## ✅ Topper's Strategy

> **Chapter/Topic:** [exact chapter name]
> **Typical Marks:** [1 / 2 / 3 / 5 marks]
> **Marks Breakdown:**
> - [Each sub-part and its marks, e.g. "Formula — 1 mark", "Calculation — 2 marks", "Result with units — 1 mark"]

**What toppers do differently:**
- [2-3 specific tips for this question type]

---

## 💡 Remember for Exam
Write 1-2 bullet points of key facts/formulas the student must memorize for this topic.

---

Always be encouraging, precise, and exam-focused.
Answer entirely in the context of CBSE Class 10 syllabus."""


# ── RAG Agent ──────────────────────────────────────────────────────────────────

def generate_answer(question: str, context_chunks: list, subject: str) -> dict:
    """
    Given a question and relevant context chunks from NeonDB,
    call Groq and return a structured answer dict.

    Args:
        question:       The student's question
        context_chunks: List of (subject, source, chunk, dist) tuples from DB
        subject:        The subject label (or empty string)

    Returns:
        { "answer": str, "sources": list[str], "subject": str }
    """
    client = get_groq_client()

    # Build context string from top chunks
    context_text = "\n\n---\n\n".join(
        [row[2] for row in context_chunks]
    )

    # Unique source file names (strip subject prefix)
    sources = list({row[1].split("::")[-1] for row in context_chunks})

    subject_display = subject if subject else "General"

    user_message = f"""Subject: {subject_display}
Student's Question: {question}

Relevant content from CBSE textbooks and previous year solved papers:
────────────────────────────────────────────────────
{context_text}
────────────────────────────────────────────────────

Now provide a complete, board-exam-ready answer following the exact format specified."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
        temperature=0.25,       # Lower = more factual, consistent
        max_tokens=2000,
        top_p=0.9,
    )

    answer_text = response.choices[0].message.content

    return {
        "answer":  answer_text,
        "sources": sources,
        "subject": subject_display,
    }
