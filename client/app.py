"""
client/app.py
CBSE 10th Smart Tutor — Streamlit Frontend
ChatGPT-style layout: sidebar + fixed bottom input + clean monochrome design.
"""

import streamlit as st
import requests
import time
import os

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CBSE Tutor",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>A</text></svg>",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

SUBJECTS = ["All Subjects", "Mathematics", "Science", "English", "SST"]

SUBJECT_EXAMPLES = {
    "Mathematics": [
        "Prove the Pythagoras theorem with diagram",
        "Solve: 2x\u00b2 \u2212 7x + 3 = 0 using the quadratic formula",
        "Find HCF of 96 and 404 using Euclid\u2019s algorithm",
        "Prove that \u221a2 is irrational",
    ],
    "Science": [
        "State and explain Ohm\u2019s Law with derivation",
        "Explain the process of photosynthesis",
        "What is the difference between mitosis and meiosis?",
        "Describe the reaction between acids and bases",
    ],
    "English": [
        "Write a formal letter to the Principal requesting leave",
        "Explain the theme of the poem Fire and Ice",
        "Write a paragraph on the importance of education",
        "What is the central idea of the chapter A Letter to God?",
    ],
    "SST": [
        "What were the causes of the French Revolution?",
        "Explain the concept of federalism in India",
        "What is sustainable development?",
        "Describe the impact of globalisation on Indian economy",
    ],
}

# ── CSS — ChatGPT Style Monochrome ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: #212121 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #ececec !important;
}

/* ── Hide Streamlit Chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #171717 !important;
    border-right: 1px solid #2f2f2f !important;
    min-width: 260px !important;
    max-width: 260px !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}
[data-testid="stSidebar"] * {
    color: #ececec !important;
}
/* Sidebar scrollbar */
[data-testid="stSidebar"] ::-webkit-scrollbar { width: 4px; }
[data-testid="stSidebar"] ::-webkit-scrollbar-track { background: transparent; }
[data-testid="stSidebar"] ::-webkit-scrollbar-thumb { background: #3f3f3f; border-radius: 4px; }

/* ── Main content area ── */
[data-testid="stMainBlockContainer"] {
    padding: 0 !important;
    max-width: 100% !important;
}
[data-testid="block-container"] {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── All Streamlit buttons ── */
[data-testid="stButton"] > button {
    background: transparent !important;
    border: 1px solid #3f3f3f !important;
    color: #ececec !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 400 !important;
    padding: 0.4rem 0.9rem !important;
    transition: background 0.15s, border-color 0.15s !important;
    text-align: left !important;
    width: 100% !important;
    box-shadow: none !important;
}
[data-testid="stButton"] > button:hover {
    background: #2a2a2a !important;
    border-color: #555 !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > label { display: none !important; }
[data-testid="stSelectbox"] > div > div {
    background: #2a2a2a !important;
    border: 1px solid #3f3f3f !important;
    border-radius: 8px !important;
    color: #ececec !important;
    font-size: 0.85rem !important;
}
[data-testid="stSelectbox"] svg { color: #888 !important; }

/* ── Text area (chat input) ── */
[data-testid="stTextArea"] > label { display: none !important; }
[data-testid="stTextArea"] textarea {
    background: #2f2f2f !important;
    border: 1px solid transparent !important;
    border-radius: 14px !important;
    color: #ececec !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    resize: none !important;
    padding: 14px 18px !important;
    transition: border-color 0.2s !important;
    min-height: 52px !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: #555 !important;
    box-shadow: none !important;
    outline: none !important;
}
[data-testid="stTextArea"] textarea::placeholder { color: #666 !important; }

/* ── Send button (special) ── */
button[kind="primary"],
[data-testid="stButton"] > button[kind="primary"] {
    background: #fff !important;
    color: #000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}
button[kind="primary"]:hover {
    background: #e5e5e5 !important;
}

/* ── Info / Warning / Error ── */
[data-testid="stInfo"]    { background: #1e1e1e !important; border: 1px solid #333 !important; border-radius: 10px !important; color: #aaa !important; }
[data-testid="stSuccess"] { background: #1a2a1a !important; border: 1px solid #2d4a2d !important; border-radius: 10px !important; }
[data-testid="stError"]   { background: #2a1a1a !important; border: 1px solid #4a2d2d !important; border-radius: 10px !important; }
[data-testid="stWarning"] { background: #2a2a1a !important; border: 1px solid #4a4a2d !important; border-radius: 10px !important; }

/* ── Spinner ── */
[data-testid="stSpinner"] p { color: #888 !important; }

/* ── Markdown in answer ── */
.stMarkdown p   { color: #d1d1d1 !important; line-height: 1.8 !important; font-size: 0.95rem !important; }
.stMarkdown h1  { color: #fff !important; font-size: 1.4rem !important; font-weight: 600 !important; margin: 1.4rem 0 0.6rem !important; }
.stMarkdown h2  { color: #fff !important; font-size: 1.15rem !important; font-weight: 600 !important; margin: 1.2rem 0 0.5rem !important; border-bottom: 1px solid #2f2f2f; padding-bottom: 0.3rem; }
.stMarkdown h3  { color: #e5e5e5 !important; font-size: 1rem !important; font-weight: 600 !important; margin: 1rem 0 0.4rem !important; }
.stMarkdown strong { color: #fff !important; }
.stMarkdown em  { color: #aaa !important; }
.stMarkdown blockquote {
    border-left: 3px solid #444 !important;
    padding: 0.5rem 1rem !important;
    margin: 0.8rem 0 !important;
    color: #999 !important;
    background: #1e1e1e !important;
    border-radius: 0 6px 6px 0 !important;
}
.stMarkdown code {
    background: #2a2a2a !important;
    border: 1px solid #3f3f3f !important;
    border-radius: 4px !important;
    padding: 0.15rem 0.45rem !important;
    font-family: 'Menlo', 'Monaco', monospace !important;
    font-size: 0.88rem !important;
    color: #e5e5e5 !important;
}
.stMarkdown pre {
    background: #1e1e1e !important;
    border: 1px solid #2f2f2f !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    overflow-x: auto !important;
}
.stMarkdown ul li,
.stMarkdown ol li { color: #d1d1d1 !important; margin-bottom: 0.4rem !important; line-height: 1.7 !important; }
.stMarkdown hr { border-color: #2f2f2f !important; margin: 1.2rem 0 !important; }
.stMarkdown table { border-collapse: collapse !important; width: 100% !important; }
.stMarkdown th {
    background: #2a2a2a !important;
    border: 1px solid #3f3f3f !important;
    padding: 0.5rem 0.8rem !important;
    color: #fff !important;
    font-weight: 600 !important;
    text-align: left !important;
}
.stMarkdown td {
    border: 1px solid #2f2f2f !important;
    padding: 0.45rem 0.8rem !important;
    color: #d1d1d1 !important;
}

/* ── Divider ── */
hr { border-color: #2f2f2f !important; }

/* ── Scrollbar global ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #3f3f3f; border-radius: 6px; }
::-webkit-scrollbar-thumb:hover { background: #555; }
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────────────────────
if "messages"     not in st.session_state: st.session_state.messages = []
if "q_prefill"    not in st.session_state: st.session_state.q_prefill = ""
if "last_subject" not in st.session_state: st.session_state.last_subject = "All Subjects"

# ── API Helpers ────────────────────────────────────────────────────────────────
def api_alive() -> bool:
    try:
        return requests.get(f"{BACKEND_URL}/health", timeout=3).status_code == 200
    except Exception:
        return False

def fetch_stats() -> list:
    try:
        return requests.get(f"{BACKEND_URL}/stats", timeout=4).json().get("stats", [])
    except Exception:
        return []

def call_ask(question: str, subject) -> dict:
    payload = {"question": question, "subject": subject}
    r = requests.post(f"{BACKEND_URL}/ask", json=payload, timeout=90)
    r.raise_for_status()
    return r.json()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown("""
    <div style="padding: 20px 16px 8px 16px;">
        <div style="font-size: 1rem; font-weight: 600; color: #ececec; letter-spacing: -0.01em;">
            CBSE Smart Tutor
        </div>
        <div style="font-size: 0.72rem; color: #666; margin-top: 2px; font-weight: 400;">
            Class 10 Board Exam Assistant
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # New conversation button
    if st.button("New conversation", key="new_chat"):
        st.session_state.messages = []
        st.session_state.q_prefill = ""
        st.rerun()

    st.markdown("""<hr style='border-color:#2f2f2f; margin: 12px 0;'>""", unsafe_allow_html=True)

    # Subject selector
    st.markdown("""<div style='font-size:0.72rem;color:#666;font-weight:500;padding:0 4px;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.06em;'>Subject</div>""", unsafe_allow_html=True)
    selected_subject = st.selectbox(
        "Subject",
        SUBJECTS,
        index=SUBJECTS.index(st.session_state.last_subject),
        key="subject_sel",
        label_visibility="collapsed",
    )
    st.session_state.last_subject = selected_subject

    st.markdown("""<hr style='border-color:#2f2f2f; margin: 14px 0;'>""", unsafe_allow_html=True)

    # Example questions
    subj_for_ex = selected_subject if selected_subject != "All Subjects" else "Science"
    examples = SUBJECT_EXAMPLES.get(subj_for_ex, [])

    st.markdown(f"""<div style='font-size:0.72rem;color:#666;font-weight:500;padding:0 4px;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.06em;'>Suggestions — {subj_for_ex}</div>""", unsafe_allow_html=True)

    for ex in examples:
        label = ex if len(ex) <= 42 else ex[:40] + "..."
        if st.button(label, key=f"ex_{ex[:25]}"):
            st.session_state.q_prefill = ex
            st.rerun()

    st.markdown("""<hr style='border-color:#2f2f2f; margin: 14px 0;'>""", unsafe_allow_html=True)

    # Stats
    stats = fetch_stats()
    if stats:
        total = sum(s["chunks"] for s in stats)
        st.markdown(f"""
        <div style='font-size:0.72rem;color:#666;font-weight:500;padding:0 4px;margin-bottom:10px;text-transform:uppercase;letter-spacing:0.06em;'>
            Knowledge Base
        </div>
        <div style='font-size:0.78rem;color:#888;padding:0 4px;margin-bottom:8px;'>
            {total:,} indexed chunks
        </div>
        """, unsafe_allow_html=True)
        for s in stats:
            pct = int((s["chunks"] / total) * 100) if total else 0
            st.markdown(f"""
            <div style='padding:5px 4px;margin-bottom:4px;'>
                <div style='display:flex;justify-content:space-between;margin-bottom:3px;'>
                    <span style='font-size:0.78rem;color:#aaa;'>{s["subject"]}</span>
                    <span style='font-size:0.72rem;color:#666;'>{s["chunks"]:,}</span>
                </div>
                <div style='height:2px;background:#2a2a2a;border-radius:2px;overflow:hidden;'>
                    <div style='height:100%;width:{pct}%;background:#555;border-radius:2px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""<div style='font-size:0.78rem;color:#555;padding:0 4px;'>Indexing in progress...</div>""", unsafe_allow_html=True)

    # Bottom status
    alive = api_alive()
    status_color = "#3a7a3a" if alive else "#7a3a3a"
    status_text  = "Connected" if alive else "Offline"
    st.markdown(f"""
    <div style='position:absolute;bottom:20px;left:0;right:0;padding:0 16px;'>
        <div style='display:flex;align-items:center;gap:8px;'>
            <div style='width:7px;height:7px;border-radius:50%;background:{status_color};flex-shrink:0;'></div>
            <span style='font-size:0.75rem;color:#555;'>Backend {status_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Main Area ──────────────────────────────────────────────────────────────────

# Outer wrapper with padding-bottom to clear fixed input bar
st.markdown("""
<div style="
    max-width: 780px;
    margin: 0 auto;
    padding: 60px 24px 160px 24px;
    min-height: 100vh;
">
""", unsafe_allow_html=True)

# ── Empty state ──
if not st.session_state.messages:
    st.markdown("""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 80px 0 40px;
        text-align: center;
    ">
        <div style="
            width: 48px; height: 48px;
            background: #2a2a2a;
            border: 1px solid #333;
            border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            margin-bottom: 20px;
            font-size: 1.5rem;
            font-weight: 700;
            color: #fff;
        ">A</div>
        <h1 style="
            font-size: 1.6rem;
            font-weight: 600;
            color: #fff;
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        ">How can I help you today?</h1>
        <p style="
            font-size: 0.9rem;
            color: #666;
            max-width: 420px;
            line-height: 1.6;
        ">
            Ask any CBSE Class 10 question. Get board-exam-ready answers with
            marks breakdown and topper strategy.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Message thread ──
for msg in st.session_state.messages:
    role    = msg["role"]
    content = msg["content"]

    if role == "user":
        st.markdown(f"""
        <div style="
            display: flex;
            justify-content: flex-end;
            margin-bottom: 24px;
        ">
            <div style="
                background: #2f2f2f;
                border: 1px solid #3a3a3a;
                border-radius: 18px 18px 4px 18px;
                padding: 12px 18px;
                max-width: 75%;
                font-size: 0.95rem;
                color: #ececec;
                line-height: 1.6;
                white-space: pre-wrap;
            ">{content}</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # Assistant message
        sources  = msg.get("sources", [])
        subject  = msg.get("subject", "")
        elapsed  = msg.get("elapsed", "")

        st.markdown("""
        <div style="display: flex; gap: 14px; margin-bottom: 32px; align-items: flex-start;">
            <div style="
                width: 32px; height: 32px;
                background: #fff;
                border-radius: 8px;
                display: flex; align-items: center; justify-content: center;
                flex-shrink: 0;
                margin-top: 2px;
                font-size: 0.8rem;
                font-weight: 700;
                color: #000;
            ">A</div>
            <div style="flex: 1; min-width: 0;">
        """, unsafe_allow_html=True)

        # Answer content rendered as markdown
        st.markdown(content)

        # Meta footer
        if sources or subject or elapsed:
            sources_html = " &nbsp;&middot;&nbsp; ".join(
                f'<span style="color:#555;">{s}</span>' for s in sources[:3]
            )
            meta_parts = []
            if subject:
                meta_parts.append(f'<span>{subject}</span>')
            if elapsed:
                meta_parts.append(f'<span>{elapsed}</span>')
            meta_str = " &nbsp;&middot;&nbsp; ".join(meta_parts)

            st.markdown(f"""
            <div style="
                margin-top: 16px;
                padding-top: 14px;
                border-top: 1px solid #2a2a2a;
                font-size: 0.75rem;
                color: #555;
            ">
                {meta_str}
                {"<br><span style='color:#3f3f3f;'>Sources: </span>" + sources_html if sources else ""}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close outer wrapper

# ── Fixed Bottom Input Bar ─────────────────────────────────────────────────────
st.markdown("""
<div style="
    position: fixed;
    bottom: 0; left: 260px; right: 0;
    background: #212121;
    padding: 16px 24px 24px;
    border-top: 1px solid #2a2a2a;
    z-index: 999;
">
    <div style="max-width: 780px; margin: 0 auto;">
""", unsafe_allow_html=True)

input_col, btn_col = st.columns([11, 1])

with input_col:
    question = st.text_area(
        "Message",
        value=st.session_state.q_prefill,
        placeholder="Ask anything about your CBSE Class 10 syllabus...",
        height=54,
        key="chat_input",
        label_visibility="collapsed",
    )

with btn_col:
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    send = st.button("Send", key="send_btn", type="primary", use_container_width=True)

st.markdown("""
        <div style="text-align:center;margin-top:8px;font-size:0.7rem;color:#444;">
            Powered by Groq LLaMA-3.3-70B &nbsp;&middot;&nbsp; NCERT &amp; Solved Papers 2013–2025
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Handle Send ───────────────────────────────────────────────────────────────
if send and question.strip():
    # Clear prefill
    st.session_state.q_prefill = ""

    # Add user message
    st.session_state.messages.append({"role": "user", "content": question.strip()})

    subject_param = selected_subject if selected_subject != "All Subjects" else None

    with st.spinner(""):
        try:
            t0     = time.time()
            result = call_ask(question.strip(), subject_param)
            elapsed = f"{time.time() - t0:.1f}s"

            st.session_state.messages.append({
                "role":    "assistant",
                "content": result.get("answer", ""),
                "sources": result.get("sources", []),
                "subject": result.get("subject", ""),
                "elapsed": elapsed,
            })
        except requests.HTTPError as e:
            st.session_state.messages.append({
                "role":    "assistant",
                "content": f"Error: {e.response.text if e.response else str(e)}",
                "sources": [],
                "subject": "",
                "elapsed": "",
            })
        except Exception as e:
            st.session_state.messages.append({
                "role":    "assistant",
                "content": f"Could not reach the backend. Make sure the server is running.\n\n`{e}`",
                "sources": [],
                "subject": "",
                "elapsed": "",
            })

    st.rerun()

elif send:
    st.warning("Type a question before sending.")
