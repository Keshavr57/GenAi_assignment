"""
CBSE 10th Grade RAG — Streamlit Frontend
Beautiful Q&A Platform for 10th Grade Students
"""

import streamlit as st
import requests
import time

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CBSE 10th Smart Tutor 🎓",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE = "http://localhost:8000"

SUBJECT_EMOJI = {
    "Mathematics": "📐",
    "Science":     "🔬",
    "English":     "📖",
    "SST":         "🌍",
}

SUBJECT_COLORS = {
    "Mathematics": "#4f8ef7",
    "Science":     "#34d399",
    "English":     "#f59e0b",
    "SST":         "#f87171",
}

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;600;700;800&display=swap');

/* ── Global Reset ── */
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [data-testid="stAppViewContainer"] {
    background: #0d0f1a !important;
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}

/* ── Hide default elements ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12152a 0%, #0d0f1a 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.2) !important;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* ── Main area ── */
[data-testid="stMainBlockContainer"] {
    padding: 2rem 2.5rem !important;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1a1f3c 0%, #0f1629 50%, #1a2040 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(99,102,241,0.15) 0%, transparent 65%);
}
.hero-title {
    font-family: 'Poppins', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    position: relative;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: #94a3b8;
    margin-top: 0.6rem;
    position: relative;
}
.badge-row {
    display: flex;
    justify-content: center;
    gap: 0.8rem;
    margin-top: 1.2rem;
    flex-wrap: wrap;
    position: relative;
}
.badge {
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 40px;
    padding: 0.3rem 1rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: #a78bfa;
}

/* ── Subject pills ── */
.subject-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.5rem 1.2rem;
    border-radius: 30px;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    border: 2px solid transparent;
    transition: all 0.2s;
}

/* ── Answer card ── */
.answer-card {
    background: linear-gradient(135deg, #13182e 0%, #0f1629 100%);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1.5rem;
    position: relative;
}
.answer-card::before {
    content: '🏆 TOPPER\'S SOLUTION';
    position: absolute;
    top: -12px; left: 24px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.25rem 0.9rem;
    border-radius: 20px;
    letter-spacing: 0.06em;
}

/* ── Stats card ── */
.stat-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.stat-number {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-label {
    font-size: 0.8rem;
    color: #64748b;
    margin-top: 0.2rem;
    font-weight: 500;
}

/* ── Source chip ── */
.source-chip {
    display: inline-block;
    background: rgba(52,211,153,0.1);
    border: 1px solid rgba(52,211,153,0.3);
    color: #34d399;
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 0.2rem;
}

/* ── Question input ── */
[data-testid="stTextArea"] textarea {
    background: #1a1f3c !important;
    border: 1.5px solid rgba(99,102,241,0.4) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    resize: none !important;
    padding: 1rem !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}

/* ── Primary button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.75rem 2rem !important;
    width: 100%;
    transition: all 0.3s !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.45) !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #1a1f3c !important;
    border: 1.5px solid rgba(99,102,241,0.4) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ── Answer markdown styling ── */
.answer-content { line-height: 1.8; }
.answer-content h1, .answer-content h2, .answer-content h3 {
    color: #a78bfa;
    margin-top: 1rem;
}
.answer-content strong { color: #60a5fa; }
.answer-content blockquote {
    border-left: 3px solid #6366f1;
    padding-left: 1rem;
    color: #94a3b8;
}
.answer-content code {
    background: rgba(99,102,241,0.15);
    border-radius: 4px;
    padding: 0.1rem 0.4rem;
    color: #a78bfa;
}

/* ── History item ── */
.history-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
    color: #94a3b8;
    cursor: pointer;
}
.history-item:hover {
    border-color: rgba(99,102,241,0.4);
    color: #e2e8f0;
}

/* ── Divider ── */
hr { border-color: rgba(99,102,241,0.15) !important; }

/* ── Info/Warning boxes ── */
[data-testid="stInfo"] {
    background: rgba(99,102,241,0.1) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 10px !important;
    color: #a78bfa !important;
}
[data-testid="stSuccess"] {
    background: rgba(52,211,153,0.1) !important;
    border: 1px solid rgba(52,211,153,0.3) !important;
    border-radius: 10px !important;
}
[data-testid="stError"] {
    background: rgba(248,113,113,0.1) !important;
    border: 1px solid rgba(248,113,113,0.3) !important;
    border-radius: 10px !important;
}
[data-testid="stSpinner"] { color: #a78bfa !important; }

.stMarkdown p { color: #cbd5e1; line-height: 1.8; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #a78bfa; }
.stMarkdown strong { color: #60a5fa; }
.stMarkdown blockquote { border-left: 3px solid #6366f1; padding-left: 1rem; color: #94a3b8; }
.stMarkdown ul li, .stMarkdown ol li { color: #cbd5e1; margin-bottom: 0.3rem; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

# ── HELPER FUNCS ──────────────────────────────────────────────────────────────
def fetch_stats():
    try:
        r = requests.get(f"{API_BASE}/stats", timeout=5)
        return r.json().get("stats", [])
    except:
        return []

def ask(question, subject):
    payload = {"question": question, "subject": subject if subject != "All Subjects" else None}
    r = requests.post(f"{API_BASE}/ask", json=payload, timeout=90)
    r.raise_for_status()
    return r.json()

def check_api():
    try:
        r = requests.get(f"{API_BASE}/", timeout=3)
        return r.status_code == 200
    except:
        return False

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem;">
        <div style="font-size:3rem; margin-bottom:0.5rem;">🎓</div>
        <div style="font-family:'Poppins',sans-serif; font-size:1.3rem; font-weight:800;
                    background:linear-gradient(135deg,#a78bfa,#60a5fa);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">CBSE Smart Tutor</div>
        <div style="font-size:0.75rem; color:#475569; margin-top:0.3rem;">Class 10 Board Exam Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    # API status
    api_ok = check_api()
    if api_ok:
        st.success("✅ Backend Connected")
    else:
        st.error("❌ Backend Offline — Start FastAPI first")

    st.markdown("---")

    # Subject selector
    st.markdown("**📚 Select Subject**")
    subject_options = ["All Subjects", "Mathematics", "Science", "English", "SST"]
    selected_subject = st.selectbox(
        "Subject", subject_options, label_visibility="collapsed"
    )

    st.markdown("---")

    # DB Stats
    st.markdown("**📊 Knowledge Base**")
    stats = fetch_stats()
    if stats:
        total_chunks = sum(s["chunks"] for s in stats)
        st.markdown(f"""
        <div class="stat-card" style="margin-bottom:0.8rem;">
            <div class="stat-number">{total_chunks:,}</div>
            <div class="stat-label">Total Chunks Indexed</div>
        </div>
        """, unsafe_allow_html=True)
        for s in stats:
            emoji = SUBJECT_EMOJI.get(s["subject"], "📄")
            col_color = SUBJECT_COLORS.get(s["subject"], "#6366f1")
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;
                        padding:0.5rem 0.8rem; margin-bottom:0.4rem;
                        background:rgba(255,255,255,0.03);
                        border-left:3px solid {col_color};
                        border-radius:0 8px 8px 0; font-size:0.85rem;">
                <span>{emoji} {s["subject"]}</span>
                <span style="color:{col_color}; font-weight:700;">{s["chunks"]:,}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("💾 Indexing PDFs on first startup…")

    st.markdown("---")

    # History
    st.markdown("**🕐 Recent Questions**")
    if st.session_state.history:
        for item in reversed(st.session_state.history[-5:]):
            st.markdown(f"""
            <div class="history-item">
                {SUBJECT_EMOJI.get(item.get('subject',''), '❓')} {item['question'][:55]}{'…' if len(item['question'])>55 else ''}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#475569; font-size:0.85rem;'>No questions yet</div>", unsafe_allow_html=True)

# ── MAIN AREA ─────────────────────────────────────────────────────────────────

# Hero Banner
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🎓 CBSE Class 10 Smart Tutor</div>
    <div class="hero-subtitle">Ask any question — get a Topper's answer, board-exam ready ✨</div>
    <div class="badge-row">
        <span class="badge">📐 Mathematics</span>
        <span class="badge">🔬 Science</span>
        <span class="badge">📖 English</span>
        <span class="badge">🌍 SST</span>
        <span class="badge">🏆 Marks Strategy</span>
        <span class="badge">📚 NCERT Based</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Question Input Area ───────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    question = st.text_area(
        "Your Question",
        placeholder="💬 Ask your CBSE question here…\ne.g. \"Explain the concept of heredity and variation\" or \"Solve: 2x² + 5x - 3 = 0\"",
        height=120,
        label_visibility="collapsed",
        key="question_input",
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    ask_btn = st.button("🚀 Get Answer", use_container_width=True)
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Example questions
    st.markdown("<div style='font-size:0.78rem; color:#475569; font-weight:600; margin-bottom:0.4rem;'>Try an example:</div>", unsafe_allow_html=True)
    examples = [
        "What is Ohm's Law?",
        "Pythagoras theorem proof",
        "French Revolution causes",
        "Write a formal letter",
    ]
    for ex in examples:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state.question_input = ex
            st.rerun()

# ── Answer Section ────────────────────────────────────────────────────────────
if ask_btn and question.strip():
    if not api_ok:
        st.error("❌ Backend is not running. Please start FastAPI first with: `python3 -m uvicorn backend:app --reload`")
    else:
        subject_param = selected_subject if selected_subject != "All Subjects" else None

        with st.spinner("🤔 Thinking like a CBSE topper…"):
            try:
                start = time.time()
                result = ask(question, subject_param)
                elapsed = time.time() - start

                # Save to history
                st.session_state.last_answer = result
                st.session_state.history.append({
                    "question": question,
                    "subject":  result.get("subject", ""),
                    "answer":   result.get("answer", ""),
                })

                # ── Answer Header ──
                subj = result.get("subject", "General")
                emoji = SUBJECT_EMOJI.get(subj, "📚")
                col_color = SUBJECT_COLORS.get(subj, "#6366f1")

                meta_col1, meta_col2, meta_col3 = st.columns(3)
                with meta_col1:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">{emoji}</div>
                        <div class="stat-label">{subj}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with meta_col2:
                    src_count = len(result.get("sources", []))
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">{src_count}</div>
                        <div class="stat-label">Sources Referenced</div>
                    </div>
                    """, unsafe_allow_html=True)
                with meta_col3:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">{elapsed:.1f}s</div>
                        <div class="stat-label">Response Time</div>
                    </div>
                    """, unsafe_allow_html=True)

                # ── Topper's Answer Card ──
                st.markdown("""
                <div class="answer-card">
                """, unsafe_allow_html=True)

                st.markdown(result["answer"])

                st.markdown("</div>", unsafe_allow_html=True)

                # ── Sources ──
                sources = result.get("sources", [])
                if sources:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("<div style='font-size:0.85rem; color:#64748b; font-weight:600; margin-bottom:0.4rem;'>📎 Referenced Sources:</div>", unsafe_allow_html=True)
                    chips_html = "".join([f'<span class="source-chip">📄 {s}</span>' for s in sources])
                    st.markdown(f"<div>{chips_html}</div>", unsafe_allow_html=True)

            except requests.exceptions.HTTPError as e:
                st.error(f"❌ API Error: {e.response.text if e.response else str(e)}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

elif ask_btn and not question.strip():
    st.warning("⚠️ Please type your question first!")

# ── Tips Section (shown when no answer) ──────────────────────────────────────
if not st.session_state.last_answer:
    st.markdown("<br>", unsafe_allow_html=True)
    tip_col1, tip_col2, tip_col3, tip_col4 = st.columns(4)
    tips = [
        ("📐", "Mathematics", "#4f8ef7", "Quadratic equations, Pythagoras, Trigonometry, Statistics"),
        ("🔬", "Science",     "#34d399", "Electricity, Chemical Reactions, Life Processes, Optics"),
        ("📖", "English",     "#f59e0b", "Letter writing, Grammar, Comprehension, Literature"),
        ("🌍", "SST",         "#f87171", "History, Geography, Political Science, Economics"),
    ]
    for col, (em, subj, color, desc) in zip([tip_col1, tip_col2, tip_col3, tip_col4], tips):
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);
                        border-top:3px solid {color}; border-radius:12px;
                        padding:1.2rem; text-align:center; height:100%;">
                <div style="font-size:2rem; margin-bottom:0.5rem;">{em}</div>
                <div style="font-weight:700; color:{color}; margin-bottom:0.4rem;">{subj}</div>
                <div style="font-size:0.78rem; color:#64748b; line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#1e293b; font-size:0.78rem; padding:1rem;">
    🎓 CBSE Smart Tutor · Powered by Groq LLaMA 3.3 · RAG with NeonDB
</div>
""", unsafe_allow_html=True)
