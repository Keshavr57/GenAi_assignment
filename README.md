# 🎓 CBSE 10th Smart Tutor

A RAG-powered Q&A platform for CBSE Class 10 board exam preparation.
Built with **FastAPI** · **Streamlit** · **Groq LLaMA-3.3-70B** · **NeonDB (pgvector)**

---

## 📁 Project Structure

```
Gen-AI-Final-Project/
├── server/                         # FastAPI backend
│   ├── main.py                     # App entry point (startup + routes)
│   ├── requirements.txt
│   ├── .env                        # DATABASE_URL, GORQ_API_KEY
│   │
│   ├── api/
│   │   └── routes.py               # All API endpoints (/ask, /stats, /ingest…)
│   │
│   ├── agent/
│   │   └── groq_agent.py           # Groq LLM agent + exam-optimized prompt
│   │
│   ├── database/
│   │   └── neon_db.py              # NeonDB / pgvector setup and queries
│   │
│   ├── ingestion/
│   │   └── pdf_loader.py           # PDF → chunk → embed → store pipeline
│   │
│   └── resources/                  # 📂 Place your PDF folders here
│       ├── Maths Solution/
│       ├── Maths Ncrt/
│       ├── Science Solution/
│       ├── Science ncrt/
│       ├── English Solution/
│       ├── Englsih Ncrt/
│       ├── SST Solution/
│       └── sst ncrt/
│
├── client/                         # Streamlit frontend
│   ├── app.py                      # Main UI
│   ├── requirements.txt
│   └── .streamlit/
│       └── config.toml             # Dark theme + server config
│
├── render.yaml                     # Render Blueprint (deploy both services)
└── .gitignore
```

---

## 🚀 Run Locally

### 1. Server (FastAPI)
```bash
cd server
pip install -r requirements.txt

# Add your keys to .env:
# DATABASE_URL=...
# GORQ_API_KEY=...

uvicorn main:app --reload --port 8000
```

The server will **automatically ingest all PDFs** in `server/resources/` on first startup.
Subsequent restarts skip already-indexed files.

API docs: http://localhost:8000/docs

### 2. Client (Streamlit)
```bash
cd client
pip install -r requirements.txt
streamlit run app.py
```

UI: http://localhost:8501

---

## ☁️ Deploy to Render

1. Push repo to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com) → **New Blueprint**
3. Connect your GitHub repo → Render reads `render.yaml` automatically
4. Set environment variables for each service:
   - **Server**: `DATABASE_URL`, `GORQ_API_KEY`
   - **Client**: `BACKEND_URL` = your server's Render URL (e.g. `https://cbse-tutor-server.onrender.com`)

> **Note:** PDFs in `server/resources/` are indexed into NeonDB on startup.
> After first deploy, the data persists in NeonDB — restarts are fast.

---

## 🧠 How It Works (RAG Pipeline)

```
Student Question
       │
       ▼
[Embed with MiniLM-L6-v2]
       │
       ▼
[pgvector similarity search → NeonDB]
       │  (top 6 most relevant chunks from CBSE PDFs)
       ▼
[Groq LLaMA-3.3-70B with exam-optimized prompt]
       │
       ▼
Formatted Answer:
  • Quick Concept
  • Step-by-step board exam answer
  • Marks breakdown + Topper's strategy
  • Key points to remember
```

---

## 📚 Supported Subjects

| Subject      | Sources |
|-------------|---------|
| 📐 Mathematics | NCERT textbook + Solved papers 2013–2025 |
| 🔬 Science     | NCERT textbook + Solved papers 2013–2025 |
| 📖 English     | NCERT Lit/Lang + Solved papers 2013–2025 |
| 🌍 SST         | NCERT textbook + Solved papers 2013–2025 |
