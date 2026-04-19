// ──────────────────────────────────────────────────────────────────────────────
// client/app.js - Vanilla JS Logic for CBSE Tutor
// ──────────────────────────────────────────────────────────────────────────────

// Set to null to use DEMO MODE with dummy data
const BACKEND_URL = null; // Change to your backend URL when ready

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
// Demo Response Generator
// ──────────────────────────────────────────────────────────────────────────────

function generateDemoResponse(question, subject) {
    const subj = subject !== "All Subjects" ? subject : "General";
    
    // Detect question type
    const isMath = question.toLowerCase().includes('solve') || 
                   question.toLowerCase().includes('prove') || 
                   question.toLowerCase().includes('find') ||
                   question.toLowerCase().includes('calculate') ||
                   subj === "Mathematics";
    
    const isScience = question.toLowerCase().includes('explain') || 
                      question.toLowerCase().includes('state') ||
                      question.toLowerCase().includes('describe') ||
                      subj === "Science";
    
    const isEnglish = question.toLowerCase().includes('write') || 
                      question.toLowerCase().includes('letter') ||
                      question.toLowerCase().includes('poem') ||
                      subj === "English";
    
    // Generate appropriate response
    if (isMath) {
        return {
            answer: `## 📌 Quick Concept
*${question}*

This question tests your understanding of fundamental mathematical concepts and problem-solving skills.

---

## 📝 Board-Exam Answer

**Given:** ${question}

**Step 1:** Identify the given information and what needs to be found

Let's break down the problem systematically:
- First, we analyze the given data
- Then, we identify the appropriate formula or theorem

**Step 2:** Apply the relevant formula

For this type of problem, we use:
\`\`\`
Formula: [Relevant mathematical formula]
\`\`\`

**Step 3:** Substitute values and solve

Substituting the given values:
- Calculation step 1
- Calculation step 2
- Final result with proper units

**[DIAGRAM: Draw a neat labeled diagram showing the geometric representation]**

**Answer:** The final result is **[calculated value]** with appropriate units.

---

## ✅ Topper's Strategy

> **Chapter/Topic:** ${subj}
> **Typical Marks:** 3-4 marks
> **Marks Breakdown:**
> - Correct formula — 1 mark
> - Substitution of values — 1 mark
> - Calculation steps — 1 mark
> - Final answer with units — 1 mark

**What toppers do differently:**
- Always write the formula first before substituting
- Show ALL working steps clearly
- Draw diagrams wherever applicable
- Write the final answer in a box or underline it
- Don't forget units in the final answer

---

## 💡 Remember for Exam

- Practice similar problems from NCERT Exercise and Examples
- Remember key formulas and theorems
- Time management: Spend 3-4 minutes on 3-mark questions`,
            sources: ["NCERT Class 10 Mathematics", "Solved Paper 2024", "Exemplar Problems"],
            subject: subj
        };
    } else if (isScience) {
        return {
            answer: `## 📌 Quick Concept
*${question}*

This question requires a clear explanation with scientific reasoning and proper terminology.

---

## 📝 Board-Exam Answer

**${question}**

**Definition:**
The concept can be defined as [clear, concise definition using NCERT terminology].

**Explanation:**

1. **Key Point 1:** Detailed explanation of the first aspect
   - Supporting detail
   - Scientific reasoning

2. **Key Point 2:** Explanation of the second aspect
   - Chemical/Physical process involved
   - Real-world application

3. **Key Point 3:** Additional important information
   - Observations or characteristics
   - Significance in daily life

**[DIAGRAM: Draw a neat labeled diagram showing the process/structure]**

**Example:**
A practical example to illustrate the concept:
- Real-world scenario
- How the principle applies

**Conclusion:**
Summary statement reinforcing the main concept.

---

## ✅ Topper's Strategy

> **Chapter/Topic:** ${subj}
> **Typical Marks:** 3-5 marks
> **Marks Breakdown:**
> - Definition — 1 mark
> - Explanation with points — 2-3 marks
> - Diagram (if required) — 1 mark
> - Example/Application — 1 mark

**What toppers do differently:**
- Start with a clear definition from NCERT
- Use bullet points or numbering for clarity
- Include well-labeled diagrams
- Mention real-life applications
- Use scientific terminology correctly

---

## 💡 Remember for Exam

- Underline key terms and definitions
- Practice drawing diagrams neatly
- Learn chemical equations and formulas
- Revise NCERT intext questions and exercises`,
            sources: ["NCERT Class 10 Science", "Solved Paper 2023", "Lab Manual"],
            subject: subj
        };
    } else if (isEnglish) {
        return {
            answer: `## 📌 Quick Concept
*${question}*

This question tests your writing skills, comprehension, and ability to express ideas clearly.

---

## 📝 Board-Exam Answer

**${question}**

**Format to follow:**

[Sender's Address]
[Date]

[Receiver's Address]

Subject: [Clear, concise subject line]

Salutation,

**Opening Paragraph:**
Introduce the purpose of your writing clearly and politely.

**Body Paragraph 1:**
- Main point or argument
- Supporting details
- Relevant examples

**Body Paragraph 2:**
- Additional information
- Further explanation
- Logical flow of ideas

**Closing Paragraph:**
Conclude with a polite request or summary of your main points.

Thanking you,
Yours sincerely/faithfully,
[Name]

---

**OR (For Literature Questions):**

**Theme/Central Idea:**
The main theme of the text is [explanation of the central message].

**Analysis:**
- **Point 1:** Literary device or character analysis
- **Point 2:** Significance of events or symbols
- **Point 3:** Author's message or moral

**Conclusion:**
The text effectively conveys [summary of the message].

---

## ✅ Topper's Strategy

> **Chapter/Topic:** ${subj}
> **Typical Marks:** 5-8 marks
> **Marks Breakdown:**
> - Format/Structure — 1-2 marks
> - Content/Ideas — 2-3 marks
> - Expression/Grammar — 1-2 marks
> - Coherence — 1 mark

**What toppers do differently:**
- Follow the exact format prescribed
- Use formal/appropriate language
- Organize ideas in clear paragraphs
- Check grammar and spelling
- Write neatly and legibly

---

## 💡 Remember for Exam

- Practice different formats (letter, article, notice, etc.)
- Read sample answers from previous years
- Maintain word limit (usually 100-150 words)
- Leave proper margins and spacing`,
            sources: ["NCERT Class 10 English", "Solved Paper 2024", "Writing Skills Guide"],
            subject: subj
        };
    } else {
        // General/SST response
        return {
            answer: `## 📌 Quick Concept
*${question}*

This question requires analytical thinking and understanding of key concepts.

---

## 📝 Board-Exam Answer

**${question}**

**Introduction:**
Brief introduction to the topic providing context.

**Main Points:**

**1. First Major Point**
   - Detailed explanation
   - Historical context or significance
   - Impact or consequences

**2. Second Major Point**
   - Supporting information
   - Examples or case studies
   - Connections to other concepts

**3. Third Major Point**
   - Additional analysis
   - Contemporary relevance
   - Critical evaluation

**[MAP/DIAGRAM: If applicable, draw a labeled map or flowchart]**

**Conclusion:**
Summarize the key points and their overall significance.

---

## ✅ Topper's Strategy

> **Chapter/Topic:** ${subj}
> **Typical Marks:** 3-5 marks
> **Marks Breakdown:**
> - Introduction — 1 mark
> - Main points (3-4 points) — 2-3 marks
> - Conclusion — 1 mark

**What toppers do differently:**
- Structure answers with clear headings
- Use point-wise format for clarity
- Include relevant dates, names, and facts
- Draw maps/diagrams where required
- Connect concepts across chapters

---

## 💡 Remember for Exam

- Revise NCERT thoroughly - most questions are direct
- Practice map work regularly
- Remember key dates and events
- Use flowcharts for complex processes`,
            sources: ["NCERT Class 10 " + subj, "Solved Paper 2024", "Previous Year Papers"],
            subject: subj
        };
    }
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
            // Generate dynamic response based on question
            const dummyResponse = generateDemoResponse(text, currentSubject);
            
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
