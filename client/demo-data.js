// Demo Q&A Database - Real CBSE Class 10 Questions with Proper Answers

const DEMO_QA_DATABASE = {
    "Mathematics": [
        {
            q: "Prove that √2 is irrational",
            a: `## 📌 Quick Concept
*Proof by contradiction - assume √2 is rational and derive a contradiction*

---

## 📝 Board-Exam Answer

**To Prove:** √2 is an irrational number

**Proof:** (By contradiction method)

**Step 1:** Let us assume, to the contrary, that √2 is rational.

Then, √2 can be written in the form **p/q** where p and q are co-prime integers and q ≠ 0.

**Step 2:** 
\`\`\`
√2 = p/q
Squaring both sides:
2 = p²/q²
p² = 2q²  ... (i)
\`\`\`

**Step 3:** From equation (i), p² is divisible by 2
- Therefore, p is also divisible by 2 (if square is divisible by 2, the number is also divisible by 2)
- Let p = 2m for some integer m

**Step 4:** Substituting p = 2m in equation (i):
\`\`\`
(2m)² = 2q²
4m² = 2q²
q² = 2m²
\`\`\`

**Step 5:** From above, q² is divisible by 2
- Therefore, q is also divisible by 2

**Step 6:** From steps 3 and 5:
- Both p and q are divisible by 2
- This contradicts our assumption that p and q are co-prime

**Conclusion:** Our assumption was wrong. Hence, **√2 is irrational**.

---

## ✅ Topper's Strategy

> **Chapter:** Real Numbers
> **Typical Marks:** 3 marks
> **Marks Breakdown:**
> - Assumption statement — 0.5 mark
> - Algebraic steps — 1.5 marks
> - Contradiction identification — 0.5 mark
> - Conclusion — 0.5 mark

**What toppers do differently:**
- Clearly state "assume to the contrary"
- Show ALL algebraic steps
- Explicitly mention "p and q are co-prime"
- End with proper conclusion statement

---

## 💡 Remember for Exam
- This is a standard 3-mark question
- Practice similar proofs: √3, √5 are irrational
- Don't skip the "co-prime" assumption`
        },
        {
            q: "Solve 2x² - 7x + 3 = 0 using quadratic formula",
            a: `## 📌 Quick Concept
*Use quadratic formula: x = [-b ± √(b² - 4ac)] / 2a*

---

## 📝 Board-Exam Answer

**Given:** 2x² - 7x + 3 = 0

**Step 1:** Identify coefficients
- a = 2, b = -7, c = 3

**Step 2:** Apply quadratic formula
\`\`\`
x = [-b ± √(b² - 4ac)] / 2a
\`\`\`

**Step 3:** Calculate discriminant
\`\`\`
D = b² - 4ac
D = (-7)² - 4(2)(3)
D = 49 - 24
D = 25
\`\`\`

**Step 4:** Substitute values
\`\`\`
x = [-(-7) ± √25] / 2(2)
x = [7 ± 5] / 4
\`\`\`

**Step 5:** Find both roots
\`\`\`
x₁ = (7 + 5)/4 = 12/4 = 3
x₂ = (7 - 5)/4 = 2/4 = 1/2
\`\`\`

**Answer:** x = 3 or x = 1/2

---

## ✅ Topper's Strategy

> **Chapter:** Quadratic Equations
> **Typical Marks:** 3 marks
> **Marks Breakdown:**
> - Writing formula — 0.5 mark
> - Substitution — 1 mark
> - Calculation — 1 mark
> - Final answer — 0.5 mark

**What toppers do differently:**
- Write the formula first
- Show discriminant calculation separately
- Calculate both roots clearly
- Box or underline final answer

---

## 💡 Remember for Exam
- Formula: x = [-b ± √(b² - 4ac)] / 2a
- Check: Sum of roots = -b/a, Product = c/a`
        },
        {
            q: "Find HCF of 96 and 404 using Euclid's algorithm",
            a: `## 📌 Quick Concept
*Euclid's Division Lemma: a = bq + r, where 0 ≤ r < b*

---

## 📝 Board-Exam Answer

**Given:** Find HCF of 96 and 404

**Step 1:** Apply Euclid's division algorithm
Since 404 > 96, divide 404 by 96

\`\`\`
404 = 96 × 4 + 20
\`\`\`

**Step 2:** Now divide 96 by remainder 20
\`\`\`
96 = 20 × 4 + 16
\`\`\`

**Step 3:** Divide 20 by remainder 16
\`\`\`
20 = 16 × 1 + 4
\`\`\`

**Step 4:** Divide 16 by remainder 4
\`\`\`
16 = 4 × 4 + 0
\`\`\`

**Step 5:** Since remainder is 0, the divisor at this stage is the HCF

**Answer:** HCF(96, 404) = **4**

---

## ✅ Topper's Strategy

> **Chapter:** Real Numbers
> **Typical Marks:** 2-3 marks
> **Marks Breakdown:**
> - Each division step — 0.5 mark each
> - Final HCF — 0.5 mark

**What toppers do differently:**
- Write each step clearly with division format
- Continue until remainder becomes 0
- State the final HCF explicitly

---

## 💡 Remember for Exam
- Always divide larger by smaller first
- Continue until remainder = 0
- Last non-zero remainder is the HCF`
        }
    ],
    
    "Science": [
        {
            q: "State and explain Ohm's Law with derivation",
            a: `## 📌 Quick Concept
*Ohm's Law: At constant temperature, current through a conductor is directly proportional to potential difference*

---

## 📝 Board-Exam Answer

**Ohm's Law Statement:**
At constant temperature, the current flowing through a conductor is directly proportional to the potential difference across its ends.

**Mathematical Form:**

**Step 1:** If I is current and V is potential difference, then:
\`\`\`
V ∝ I
V = IR
\`\`\`
where R is the resistance of the conductor (constant)

**Step 2:** Rearranging:
\`\`\`
R = V/I
\`\`\`

**Units:**
- V (Voltage) → Volt (V)
- I (Current) → Ampere (A)
- R (Resistance) → Ohm (Ω)

**[DIAGRAM: Draw V-I graph showing straight line passing through origin]**

**Experimental Verification:**

1. Set up a circuit with battery, ammeter, voltmeter, and resistor
2. Vary voltage using rheostat
3. Note corresponding current values
4. Plot V vs I graph
5. Graph is a straight line through origin, proving V ∝ I

**Conclusion:** The ratio V/I remains constant, which is the resistance R.

---

## ✅ Topper's Strategy

> **Chapter:** Electricity
> **Typical Marks:** 3-5 marks
> **Marks Breakdown:**
> - Statement — 1 mark
> - Mathematical form — 1 mark
> - Diagram/Graph — 1 mark
> - Explanation — 1-2 marks

**What toppers do differently:**
- State the law clearly with "at constant temperature"
- Draw neat V-I graph with labels
- Mention units of all quantities
- Include experimental setup if asked

---

## 💡 Remember for Exam
- Formula: V = IR
- Graph: Straight line through origin
- Ohmic conductors: Follow Ohm's law
- Non-ohmic: LEDs, diodes don't follow`
        },
        {
            q: "Explain the process of photosynthesis",
            a: `## 📌 Quick Concept
*Plants convert light energy into chemical energy (glucose) using CO₂ and water*

---

## 📝 Board-Exam Answer

**Photosynthesis Definition:**
The process by which green plants prepare their own food using carbon dioxide and water in the presence of sunlight and chlorophyll.

**Site:** Chloroplasts in leaf cells

**Raw Materials:**
1. Carbon dioxide (CO₂) - from air through stomata
2. Water (H₂O) - from soil through roots
3. Sunlight - source of energy
4. Chlorophyll - green pigment that traps light

**Process:**

**Step 1: Light Reaction** (in grana)
- Chlorophyll absorbs light energy
- Water molecules split: 2H₂O → 4H⁺ + O₂
- Oxygen is released as by-product

**Step 2: Dark Reaction** (in stroma)
- CO₂ is reduced to glucose using H⁺ ions
- Energy from light reaction is used

**Overall Equation:**
\`\`\`
6CO₂ + 6H₂O + Light Energy → C₆H₁₂O₆ + 6O₂
                Chlorophyll      (Glucose)
\`\`\`

**[DIAGRAM: Draw leaf cross-section showing chloroplast with labeled parts]**

**Products:**
1. **Glucose** - stored as starch, used for energy
2. **Oxygen** - released into atmosphere

**Significance:**
- Provides food for all living organisms
- Maintains oxygen-carbon dioxide balance
- Source of all energy on Earth

---

## ✅ Topper's Strategy

> **Chapter:** Life Processes
> **Typical Marks:** 5 marks
> **Marks Breakdown:**
> - Definition — 1 mark
> - Raw materials — 1 mark
> - Process/Equation — 2 marks
> - Diagram — 1 mark

**What toppers do differently:**
- Write balanced chemical equation
- Draw neat labeled diagram
- Mention both light and dark reactions
- State significance

---

## 💡 Remember for Exam
- Equation: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂
- Site: Chloroplast
- Pigment: Chlorophyll
- By-product: Oxygen`
        },
        {
            q: "What is the difference between mitosis and meiosis?",
            a: `## 📌 Quick Concept
*Mitosis: Growth & repair (2 identical cells). Meiosis: Gamete formation (4 different cells)*

---

## 📝 Board-Exam Answer

**Differences between Mitosis and Meiosis:**

| **Basis** | **Mitosis** | **Meiosis** |
|-----------|-------------|-------------|
| **Definition** | Equational division | Reductional division |
| **Occurs in** | Somatic (body) cells | Germ cells (reproductive) |
| **Number of divisions** | One division | Two divisions (Meiosis I & II) |
| **Daughter cells** | 2 cells | 4 cells |
| **Chromosome number** | Diploid (2n) → Diploid (2n) | Diploid (2n) → Haploid (n) |
| **Genetic variation** | Identical to parent | Genetically different |
| **Purpose** | Growth, repair, asexual reproduction | Sexual reproduction, gamete formation |
| **Crossing over** | Does not occur | Occurs in Prophase I |

**Mitosis:**
- Maintains chromosome number
- Produces identical daughter cells
- Example: Skin cell division, wound healing

**Meiosis:**
- Reduces chromosome number by half
- Produces gametes (sperm, egg)
- Introduces genetic variation
- Example: Formation of pollen, ovum

**[DIAGRAM: Draw simple diagrams showing mitosis (1→2) and meiosis (1→4)]**

---

## ✅ Topper's Strategy

> **Chapter:** Heredity and Evolution
> **Typical Marks:** 3-5 marks
> **Marks Breakdown:**
> - Tabular differences — 3 marks
> - Explanation — 1-2 marks

**What toppers do differently:**
- Present in tabular form for clarity
- Mention chromosome numbers (2n, n)
- Give examples
- Draw simple diagrams if time permits

---

## 💡 Remember for Exam
- Mitosis: 1 division → 2 identical cells (2n)
- Meiosis: 2 divisions → 4 different cells (n)
- Mitosis = Growth, Meiosis = Gametes`
        }
    ],
    
    "English": [
        {
            q: "Write a letter to the Principal requesting leave",
            a: `## 📌 Quick Concept
*Formal letter format with proper structure and polite language*

---

## 📝 Board-Exam Answer

**Format: Formal Letter**

\`\`\`
Sender's Address
123, Green Park
New Delhi - 110016

Date: 15th January, 2025

To,
The Principal
ABC Public School
New Delhi - 110016

Subject: Application for Leave

Respected Sir/Madam,

I am [Your Name], a student of Class 10-A, Roll No. 15. I am writing this letter to request you to grant me leave for three days from 16th January to 18th January, 2025.

I need to attend my cousin's wedding in Jaipur with my family. The wedding ceremony is on 17th January, and we need to travel a day before and return a day after.

I assure you that I will complete all the missed assignments and classwork upon my return. I will also take notes from my classmates to cover the topics taught during my absence.

I request you to kindly grant me leave for the mentioned dates. I shall be highly obliged.

Thanking you,

Yours obediently,
[Your Name]
Class 10-A
Roll No. 15
\`\`\`

---

## ✅ Topper's Strategy

> **Chapter:** Writing Skills
> **Typical Marks:** 5 marks
> **Marks Breakdown:**
> - Format (addresses, date, subject) — 1 mark
> - Content (reason, request) — 2 marks
> - Expression (grammar, vocabulary) — 1.5 marks
> - Conclusion — 0.5 mark

**What toppers do differently:**
- Follow exact format with all elements
- Keep language formal and polite
- State clear reason for leave
- Mention dates specifically
- Use proper salutation and closing

---

## 💡 Remember for Exam
- Format: Sender's address → Date → Receiver's address → Subject → Salutation → Body → Closing
- Word limit: 100-120 words
- Use "Yours obediently" for Principal
- Always mention class and roll number`
        },
        {
            q: "Explain the theme of the poem Fire and Ice by Robert Frost",
            a: `## 📌 Quick Concept
*The poem explores how the world might end - through fire (desire) or ice (hatred)*

---

## 📝 Board-Exam Answer

**Poem: Fire and Ice by Robert Frost**

**Central Theme:**
The poem discusses the two possible ways the world could end - through fire or ice, which symbolize human emotions of desire and hatred.

**Analysis:**

**1. Fire represents Desire:**
- Fire symbolizes passionate emotions like greed, lust, and desire
- The poet has experienced desire and knows its destructive power
- Uncontrolled desires can lead to conflicts and destruction

**2. Ice represents Hatred:**
- Ice symbolizes cold emotions like hatred, indifference, and rigidity
- Hatred makes people insensitive and cruel
- It can be equally destructive as desire

**3. Poet's Opinion:**
- The poet favors fire (desire) as the cause of world's end
- However, he acknowledges that ice (hatred) is also sufficient for destruction
- Both emotions are dangerous when taken to extremes

**Literary Devices:**
- **Symbolism:** Fire = desire, Ice = hatred
- **Rhyme Scheme:** ABAABCBCB
- **Contrast:** Hot vs Cold, Fire vs Ice

**Message:**
The poem warns against extreme human emotions. Both excessive desire and hatred can lead to destruction. We must control our emotions to prevent catastrophe.

**Conclusion:**
Robert Frost uses simple language to convey a profound message about human nature and its potential for self-destruction.

---

## ✅ Topper's Strategy

> **Chapter:** First Flight (Poetry)
> **Typical Marks:** 3-5 marks
> **Marks Breakdown:**
> - Theme identification — 1 mark
> - Explanation of symbols — 2 marks
> - Literary devices — 1 mark
> - Message/Conclusion — 1 mark

**What toppers do differently:**
- Clearly explain symbolism (fire=desire, ice=hatred)
- Quote lines from the poem
- Mention literary devices
- Connect to real-world relevance

---

## 💡 Remember for Exam
- Fire = Desire, passion, greed
- Ice = Hatred, indifference, coldness
- Both can destroy the world
- Message: Control extreme emotions`
        }
    ],
    
    "SST": [
        {
            q: "What were the causes of the French Revolution?",
            a: `## 📌 Quick Concept
*Social inequality, economic crisis, and Enlightenment ideas led to the French Revolution of 1789*

---

## 📝 Board-Exam Answer

**Causes of the French Revolution (1789):**

**1. Social Causes:**

**a) Inequality in Society:**
- French society divided into three estates
- **First Estate:** Clergy (privileged, no taxes)
- **Second Estate:** Nobility (privileged, no taxes)
- **Third Estate:** Common people (90% population, paid all taxes)

**b) Burden on Third Estate:**
- Peasants, artisans, workers paid heavy taxes
- No political rights despite being majority
- Growing resentment against privileges

**2. Economic Causes:**

**a) Financial Crisis:**
- France was bankrupt due to wars
- King Louis XVI lived in luxury at Versailles
- Empty treasury, mounting debts

**b) Taxation System:**
- Only Third Estate paid taxes (taille, tithes)
- Clergy and nobility were exempt
- Unfair and oppressive system

**c) Rising Prices:**
- Bad harvests led to food shortage
- Bread prices increased
- Common people faced starvation

**3. Political Causes:**

**a) Absolute Monarchy:**
- King had unlimited power
- No democracy or representation
- Arbitrary rule and injustice

**b) Weak Leadership:**
- Louis XVI was indecisive
- Failed to solve financial crisis
- Lost support of people

**4. Intellectual Causes:**

**a) Enlightenment Ideas:**
- Philosophers like Rousseau, Voltaire, Montesquieu
- Ideas of liberty, equality, fraternity
- Questioned divine right of kings
- Inspired people to fight for rights

**5. Immediate Cause:**

**a) Calling of Estates-General (1789):**
- King called meeting to impose new taxes
- Third Estate demanded voting by head (not by estate)
- Demand rejected, led to formation of National Assembly
- Sparked the revolution

**[DIAGRAM: Draw pyramid showing three estates with Third Estate at bottom bearing the burden]**

**Conclusion:**
The French Revolution was result of long-term social, economic, and political problems combined with new ideas of Enlightenment.

---

## ✅ Topper's Strategy

> **Chapter:** The French Revolution (History)
> **Typical Marks:** 5 marks
> **Marks Breakdown:**
> - Social causes — 1.5 marks
> - Economic causes — 1.5 marks
> - Political causes — 1 mark
> - Intellectual/Immediate cause — 1 mark

**What toppers do differently:**
- Organize answer with clear headings
- Mention all types of causes
- Give specific examples (Louis XVI, Estates)
- Draw diagram of three estates
- Write proper conclusion

---

## 💡 Remember for Exam
- Three Estates: Clergy, Nobility, Common people
- Economic crisis + Social inequality = Revolution
- Enlightenment thinkers: Rousseau, Voltaire, Montesquieu
- Year: 1789`
        },
        {
            q: "Explain the concept of federalism in India",
            a: `## 📌 Quick Concept
*Federalism: Power shared between Central and State governments with written constitution*

---

## 📝 Board-Exam Answer

**Federalism in India:**

**Definition:**
Federalism is a system of government where power is divided between a central authority and various constituent units (states).

**Key Features of Indian Federalism:**

**1. Two Levels of Government:**
- **Central Government:** Governs entire nation
- **State Governments:** Govern respective states
- Both derive authority from Constitution

**2. Division of Powers:**

**a) Union List (Central):**
- Defence, foreign affairs, currency, railways
- 97 subjects under central government

**b) State List (States):**
- Police, agriculture, irrigation, local government
- 66 subjects under state governments

**c) Concurrent List (Both):**
- Education, forests, marriage, adoption
- 47 subjects - both can make laws
- In case of conflict, central law prevails

**d) Residuary Powers:**
- Subjects not in any list
- Belong to central government
- Example: Computer software, cyber laws

**3. Written Constitution:**
- Constitution is supreme law
- Clearly defines powers of each level
- Cannot be changed easily

**4. Independent Judiciary:**
- Supreme Court acts as umpire
- Resolves disputes between Centre and States
- Protects Constitution

**5. Dual Government:**
- Citizens governed by both levels
- Pay taxes to both
- Follow laws made by both

**Special Features of Indian Federalism:**

**1. More Centralized:**
- Centre has more powers than states
- Called "quasi-federal" system
- Strong centre needed for unity

**2. Single Constitution:**
- Unlike USA, India has one constitution for all
- States don't have separate constitutions

**3. Emergency Provisions:**
- Centre can take over state administration
- During national emergency, becomes unitary

**[DIAGRAM: Draw flowchart showing Central Govt at top, State Govts below, with three lists]**

**Conclusion:**
Indian federalism balances unity and diversity. It gives autonomy to states while maintaining strong centre for national integration.

---

## ✅ Topper's Strategy

> **Chapter:** Federalism (Political Science)
> **Typical Marks:** 5 marks
> **Marks Breakdown:**
> - Definition — 1 mark
> - Division of powers (3 lists) — 2 marks
> - Key features — 1.5 marks
> - Diagram/Conclusion — 0.5 mark

**What toppers do differently:**
- Clearly explain three lists with examples
- Mention number of subjects in each list
- Draw diagram showing power distribution
- Explain why India is "quasi-federal"
- Give current examples

---

## 💡 Remember for Exam
- Union List: 97 subjects (Defence, Railways)
- State List: 66 subjects (Police, Agriculture)
- Concurrent List: 47 subjects (Education, Forests)
- Residuary Powers: Central Government
- India = Quasi-federal (more centralized)`
        }
    ]
};
