// ──────────────────────────────────────────────────────────────────────────────
// client/app.js - Vanilla JS Logic for CBSE Tutor
// ──────────────────────────────────────────────────────────────────────────────

// Set to null to use DEMO MODE with dummy data
const BACKEND_URL = "https://genai-assignment-xpw8.onrender.com"; // Final Render URL

// State
let currentSubject = "All Subjects";
let isGenerating = false;

// DOM Elements
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatContainer = document.getElementById('chatContainer');
const emptyState = document.getElementById('emptyState');
const subjectSelect = document.getElementById('subjectSelect');
const newChatBtn = document.getElementById('newChatBtn');
const suggestionsList = document.getElementById('suggestionsList');
const statsTotal = document.getElementById('statsTotal');
const statsList = document.getElementById('statsList');
const statusIndicator = document.getElementById('statusIndicator');
const statusText = document.getElementById('statusText');

// Mobile sidebar elements
const sidebar = document.getElementById('sidebar');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const sidebarOverlay = document.getElementById('sidebarOverlay');

// Examples dictionary matching streamlits's old logic
const SUBJECT_EXAMPLES = {
    "Mathematics": [
        "Prove the Pythagoras theorem with diagram",
        "Solve: 2x² − 7x + 3 = 0 using the quadratic formula",
        "Find HCF of 96 and 404 using Euclid’s algorithm",
        "Prove that √2 is irrational"
    ],
    "Science": [
        "State and explain Ohm’s Law with derivation",
        "Explain the process of photosynthesis",
        "What is the difference between mitosis and meiosis?",
        "Describe the reaction between acids and bases"
    ],
    "English": [
        "Write a formal letter to the Principal requesting leave",
        "Explain the theme of the poem Fire and Ice",
        "Write a paragraph on the importance of education",
        "What is the central idea of the chapter A Letter to God?"
    ],
    "SST": [
        "What were the causes of the French Revolution?",
        "Explain the concept of federalism in India",
        "What is sustainable development?",
        "Describe the impact of globalisation on Indian economy"
    ]
};

// Setup Markdown parser options
marked.setOptions({
    gfm: true,
    breaks: true,
    highlight: function(code, lang) {
        const language = hljs.getLanguage(lang) ? lang : 'plaintext';
        return hljs.highlight(code, { language }).value;
    }
});

// ──────────────────────────────────────────────────────────────────────────────
// API Polling & Boot
// ──────────────────────────────────────────────────────────────────────────────

async function checkHealth() {
    if (!BACKEND_URL) {
        // DEMO MODE
        statusIndicator.className = "status-indicator online";
        statusText.textContent = "Demo Mode (No Backend)";
        return;
    }
    
    try {
        const res = await fetch(`${BACKEND_URL}/health`);
        if(res.ok) {
            statusIndicator.className = "status-indicator online";
            statusText.textContent = "Backend Connected";
        } else {
            throw new Error("Not OK");
        }
    } catch(e) {
        statusIndicator.className = "status-indicator offline";
        statusText.textContent = "Backend Offline";
    }
}

async function fetchStats() {
    if (!BACKEND_URL) {
        // DEMO MODE - Dummy stats
        const dummyStats = [
            { subject: "Mathematics", chunks: 1250 },
            { subject: "Science", chunks: 980 },
            { subject: "English", chunks: 750 },
            { subject: "SST", chunks: 620 }
        ];
        
        const total = dummyStats.reduce((acc, curr) => acc + curr.chunks, 0);
        statsTotal.textContent = `${total.toLocaleString()} indexed chunks`;
        
        statsList.innerHTML = dummyStats.map(s => {
            const pct = Math.round((s.chunks / total) * 100) || 0;
            return `
            <div class="stat-item">
                <div class="stat-header">
                    <span class="stat-subject">${s.subject}</span>
                    <span class="stat-count">${s.chunks.toLocaleString()}</span>
                </div>
                <div class="stat-bar-bg">
                    <div class="stat-bar-fill" style="width: ${pct}%"></div>
                </div>
            </div>`;
        }).join('');
        return;
    }
    
    try {
        const res = await fetch(`${BACKEND_URL}/stats`);
        const data = await res.json();
        const stats = data.stats || [];
        
        const total = stats.reduce((acc, curr) => acc + curr.chunks, 0);
        statsTotal.textContent = `${total.toLocaleString()} indexed chunks`;
        
        statsList.innerHTML = stats.map(s => {
            const pct = Math.round((s.chunks / total) * 100) || 0;
            return `
            <div class="stat-item">
                <div class="stat-header">
                    <span class="stat-subject">${s.subject}</span>
                    <span class="stat-count">${s.chunks.toLocaleString()}</span>
                </div>
                <div class="stat-bar-bg">
                    <div class="stat-bar-fill" style="width: ${pct}%"></div>
                </div>
            </div>`;
        }).join('');
    } catch(e) {
        statsTotal.textContent = "Indexing / Offline";
        statsList.innerHTML = "";
    }
}

// ──────────────────────────────────────────────────────────────────────────────
// UI Logic
// ──────────────────────────────────────────────────────────────────────────────

function renderSuggestions() {
    const subjForEx = currentSubject === "All Subjects" ? "Science" : currentSubject;
    const examples = SUBJECT_EXAMPLES[subjForEx] || [];
    
    suggestionsList.innerHTML = examples.map(ex => 
        `<button class="suggestion-btn" onclick="prefillAndSend('${ex.replace(/'/g, "\\'")}')">${ex}</button>`
    ).join('');
}

function prefillAndSend(txt) {
    if(window.innerWidth <= 768) toggleSidebar(false);
    chatInput.value = txt;
    handleSend();
}

// Auto-resize Textarea
chatInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
    if(this.value.trim() === '') {
        sendBtn.disabled = true;
    } else {
        sendBtn.disabled = false;
    }
});

chatInput.addEventListener('keydown', function(e) {
    if(e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
    }
});

subjectSelect.addEventListener('change', (e) => {
    currentSubject = e.target.value;
    renderSuggestions();
});

newChatBtn.addEventListener('click', () => {
    // Clear chat
    document.querySelectorAll('.message-wrapper').forEach(e => e.remove());
    emptyState.style.display = 'flex';
    if(window.innerWidth <= 768) toggleSidebar(false);
});

mobileMenuBtn.addEventListener('click', () => toggleSidebar(true));
sidebarOverlay.addEventListener('click', () => toggleSidebar(false));

function toggleSidebar(show) {
    if(show) {
        sidebar.classList.add('open');
        sidebarOverlay.classList.add('open');
    } else {
        sidebar.classList.remove('open');
        sidebarOverlay.classList.remove('open');
    }
}

// ──────────────────────────────────────────────────────────────────────────────
// Demo Response Generator with Real Q&A Matching
// ──────────────────────────────────────────────────────────────────────────────

function findBestMatch(question, subject) {
    const subj = subject !== "All Subjects" ? subject : null;
    
    // If subject is selected, search only in that subject
    const searchSubjects = subj ? [subj] : ["Mathematics", "Science", "English", "SST"];
    
    let bestMatch = null;
    let highestScore = 0;
    
    for (const searchSubj of searchSubjects) {
        const qaList = DEMO_QA_DATABASE[searchSubj] || [];
        
        for (const qa of qaList) {
            // Calculate similarity score
            const score = calculateSimilarity(question.toLowerCase(), qa.q.toLowerCase());
            
            if (score > highestScore) {
                highestScore = score;
                bestMatch = {
                    answer: qa.a,
                    sources: [
                        `NCERT Class 10 ${searchSubj}`,
                        "Solved Paper 2024",
                        "Solved Paper 2023"
                    ],
                    subject: searchSubj
                };
            }
        }
    }
    
    // If good match found (score > 0.3), return it
    if (bestMatch && highestScore > 0.3) {
        return bestMatch;
    }
    
    // Otherwise return generic response
    return generateGenericResponse(question, subj || "General");
}

function calculateSimilarity(str1, str2) {
    // Simple word matching algorithm
    const words1 = str1.split(/\s+/);
    const words2 = str2.split(/\s+/);
    
    let matchCount = 0;
    for (const word1 of words1) {
        if (word1.length < 3) continue; // Skip small words
        for (const word2 of words2) {
            if (word1.includes(word2) || word2.includes(word1)) {
                matchCount++;
                break;
            }
        }
    }
    
    return matchCount / Math.max(words1.length, words2.length);
}

function generateGenericResponse(question, subject) {
    return {
        answer: `## 📌 Quick Concept
*${question}*

This is a demonstration of the CBSE Smart Tutor interface.

---

## 📝 Board-Exam Answer

**Question:** ${question}

In the full version with backend connected, you would receive:

1. **Detailed Answer:** Complete board-exam-ready answer with step-by-step explanation
2. **Relevant Content:** Retrieved from NCERT textbooks and solved papers (2013-2025)
3. **AI-Generated:** Powered by Groq LLaMA-3.3-70B for accurate responses

**Try these sample questions to see real demo answers:**

**Mathematics:**
- Prove that √2 is irrational
- Solve 2x² - 7x + 3 = 0 using quadratic formula
- Find HCF of 96 and 404 using Euclid's algorithm

**Science:**
- State and explain Ohm's Law with derivation
- Explain the process of photosynthesis
- What is the difference between mitosis and meiosis?

**English:**
- Write a letter to the Principal requesting leave
- Explain the theme of the poem Fire and Ice

**SST:**
- What were the causes of the French Revolution?
- Explain the concept of federalism in India

---

## ✅ Topper's Strategy

> **Chapter/Topic:** ${subject}
> **Typical Marks:** 3-5 marks

**What toppers do differently:**
- Read the question carefully and identify keywords
- Structure answers with clear headings
- Include diagrams where applicable
- Show all working steps
- Use proper terminology from NCERT

---

## 💡 Remember for Exam

- Practice previous year papers regularly
- Revise NCERT thoroughly
- Time management is crucial
- Write neat and legible answers

---

*Try the sample questions above to see detailed demo answers!*`,
        sources: [`NCERT Class 10 ${subject}`, "Demo Mode"],
        subject: subject
    };
}

// ──────────────────────────────────────────────────────────────────────────────
// Messaging
// ──────────────────────────────────────────────────────────────────────────────

function autoScroll() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function appendUserMessage(text) {
    emptyState.style.display = 'none';
    const wrapper = document.createElement('div');
    wrapper.className = 'message-wrapper user';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.textContent = text;
    
    wrapper.appendChild(content);
    chatContainer.appendChild(wrapper);
    autoScroll();
}

function appendAIPlaceholder() {
    const wrapper = document.createElement('div');
    wrapper.className = 'message-wrapper assistant';
    wrapper.innerHTML = `
        <div class="ai-avatar">A</div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    chatContainer.appendChild(wrapper);
    autoScroll();
    return wrapper;
}

function updateAIMessage(wrapperDom, data, elapsed) {
    const rawMarkdown = data.answer || "Sorry, I could not generate an answer.";
    const cleanHtml = DOMPurify.sanitize(marked.parse(rawMarkdown));
    
    const sources = data.sources || [];
    const subject = data.subject || "";
    
    let footerHtml = "";
    if(sources.length > 0 || subject || elapsed) {
        let pills = sources.slice(0,3).map(s => `<span class="source-pill">${s}</span>`).join('');
        footerHtml = `
            <div class="message-meta">
                <div class="stats-row">
                    ${subject ? `<span>${subject}</span> • ` : ''}
                    ${elapsed ? `<span>${elapsed}s</span>` : ''}
                </div>
                ${sources.length > 0 ? `<div>Sources: ${pills}</div>` : ''}
            </div>
        `;
    }

    const contentDiv = wrapperDom.querySelector('.message-content');
    contentDiv.innerHTML = `<div class="markdown-body">${cleanHtml}</div>${footerHtml}`;
    
    autoScroll();
}

async function handleSend() {
    if(isGenerating) return;
    const text = chatInput.value.trim();
    if(!text) return;

    // Reset input
    chatInput.value = '';
    chatInput.style.height = 'auto';
    sendBtn.disabled = true;

    // Build Payload
    const payload = {
        question: text,
        subject: currentSubject === "All Subjects" ? null : currentSubject
    };

    appendUserMessage(text);
    const aiWrapper = appendAIPlaceholder();
    isGenerating = true;

    const t0 = performance.now();
    
    // DEMO MODE - Generate dummy response
    if (!BACKEND_URL) {
        setTimeout(() => {
            // Find best matching Q&A from database
            const dummyResponse = findBestMatch(text, currentSubject);
            
            const t1 = performance.now();
            const elapsed = ((t1 - t0)/1000).toFixed(1);
            updateAIMessage(aiWrapper, dummyResponse, elapsed);
            isGenerating = false;
            sendBtn.disabled = (chatInput.value.trim() === '');
        }, 1500); // Simulate API delay
        return;
    }

    try {
        const res = await fetch(`${BACKEND_URL}/ask`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });

        if(!res.ok) {
            const errBase = await res.text();
            throw new Error(`HTTP Error: ${res.status} - ${errBase}`);
        }

        const data = await res.json();
        const t1 = performance.now();
        const elapsed = ((t1 - t0)/1000).toFixed(1);

        updateAIMessage(aiWrapper, data, elapsed);

    } catch (e) {
        aiWrapper.querySelector('.message-content').innerHTML = `
            <div style="color: #ff453a;">
                <b>Error connecting to backend:</b><br/>${e.message}<br/><br/>
                <i>Make sure your FastAPI server is running on port 8000.</i>
            </div>
        `;
        autoScroll();
    } finally {
        isGenerating = false;
        sendBtn.disabled = (chatInput.value.trim() === '');
    }
}

// ──────────────────────────────────────────────────────────────────────────────
// Boot
// ──────────────────────────────────────────────────────────────────────────────
sendBtn.disabled = true;
renderSuggestions();
checkHealth();
fetchStats();
// Poll health every 15s
setInterval(checkHealth, 15000);
