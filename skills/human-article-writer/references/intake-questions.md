# Intake Questionnaire Framework

This questionnaire captures the parameters needed to simulate a specific human author writing for a specific audience. Every question directly shapes output. Unanswered questions result in AI-default choices, which produce AI-default prose.

---

## Section 1: Author Profile

### Q1. Who is the simulated author?
*Example: "Senior backend engineer at a Series B fintech startup, 8 years experience, previously at a large bank."*

**Why it matters:** The author's identity determines vocabulary register, what they treat as obvious, what frustrates them, and what they're proud of. An academic writes differently than a practitioner. A consultant writes differently than an IC.

### Q2. Professional background and years of experience
*Example: "Started as a sysadmin, moved into SRE, now leads platform engineering. 12 years total."*

**Why it matters:** Career path determines which adjacent domains bleed into the writing. An ex-sysadmin SRE will reach for infrastructure metaphors. An ex-developer SRE will reach for code metaphors. Tenure determines confidence level and willingness to make strong claims.

### Q3. Their specific expertise level on THIS topic (not in general)
Options: Novice on this specific topic / Working knowledge / Deep practitioner / Thought leader
*Example: "Deep practitioner on Kafka, working knowledge on Pulsar (the comparison subject)."*

**Why it matters:** A deep expert omits basics and dwells on edge cases. A working-knowledge author explains more and hedges more. This is the single biggest driver of omission decisions (Principle 2).

### Q4. Opinion stance on this topic
Options: Strong opinions, loosely held / Strong opinions, firmly held / Balanced and analytical / Genuinely curious, still forming views

**Why it matters:** Stance controls how much hedging appears, how many "it depends" qualifications survive editing, and whether the article ends with a recommendation or an open question.

### Q5. Cultural and regional context
*Example: "UK-based, writes for a European audience. Uses British spelling. References GDPR as a lived constraint, not an abstract regulation."*

**Why it matters:** Affects spelling (colour/color), currency ($, £, €), regulatory references, and cultural touchstones. A US author mentions AWS re:Invent; a European author mentions KubeCon Amsterdam. These signals are immediately readable by in-group audiences.

### Q6. Writing quirks or style preferences
*Example: "Uses em-dashes frequently. Starts paragraphs with the conclusion, then justifies. Never uses bullet lists in prose sections. Has a dry sense of humor that surfaces in parentheticals."*

**Why it matters:** Idiosyncratic style is the hardest AI-detection signal to fake at scale and the easiest to specify up front. One or two quirks applied consistently throughout an article creates recognizable voice.

---

## Section 2: Target Audience

### Q7. Reader expertise level
Options: Beginner (needs all terms defined) / Intermediate (knows the domain, not this specific topic) / Expert (skip the basics entirely) / Mixed (stratify with clear signals)

**Why it matters:** This is the primary control for how much scaffolding appears. Writing for experts with beginner scaffolding is the most common sign of AI generation. The mismatch is detectable.

### Q8. What is the reader trying to decide or learn?
*Example: "Should I migrate from RabbitMQ to Kafka? They've read the docs, they want a practitioner's honest take."*

**Why it matters:** The reader's goal determines the article's shape. A decision-making reader needs comparison and recommendation. A learning reader needs explanation and examples. Misaligning structure to goal produces text that technically covers the topic but doesn't serve the reader.

### Q9. Where will they read this?
Options: Company engineering blog / Industry publication (e.g., InfoQ, ACM Queue) / LinkedIn article / Newsletter (subscribed audience) / Personal blog / Reddit/HN post

**Why it matters:** Platform determines assumed context and acceptable length. LinkedIn readers expect shorter paragraphs and a stronger hook. An ACM Queue reader expects citations and precise terminology. A newsletter subscriber has opted in to the author's voice — more latitude for opinion.

### Q10. Cultural context of the audience
*Example: "Primarily North American, secondarily European. No significant localization needed but avoid US-centric regulatory assumptions."*

**Why it matters:** Localization errors are a credibility drain. A UK author writing for a US audience who references "the ICO" without explanation loses US readers. Explicit context prevents these slips.

---

## Section 3: Publication Format

| Format | Length | Tone | Structure | Citations | Opinion Level |
|---|---|---|---|---|---|
| **Explainer** | 800–1,500w | Accessible, patient | Background → concept → examples → summary | Optional | Low — explain, don't advocate |
| **Practitioner blog** | 1,200–2,500w | Direct, experience-led | Problem → what we tried → what worked → lessons | Rare, informal | High — this is what worked for us |
| **Technical deep-dive** | 2,000–5,000w | Precise, dense | Architecture → implementation → tradeoffs → edge cases | Yes, specific | Medium — here are the tradeoffs |
| **Thought leadership** | 1,000–2,000w | Confident, forward-looking | Observation → pattern → implication → call to action | Minimal | Very high — here is my thesis |
| **Comparison/review** | 1,500–3,000w | Analytical, fair but opinionated | Criteria → per-candidate analysis → verdict | Where available | High — the recommendation is the point |
| **Case study** | 1,500–3,000w | Narrative, specific | Context → problem → solution → outcome → lessons | Internal metrics | Medium — let the results speak |

**Select one format before drafting.** Format determines default structure, and structure is the second-most-detectable AI signal after perplexity uniformity.

---

## Section 4: Content Requirements

### Q11. Target word count
*Example: "1,800 words. Hard cap at 2,200."*

**Why it matters:** Word count forces allocation decisions, which forces asymmetry (Principle 1). A 1,500-word piece on a 10-subtopic subject cannot cover everything equally — the author must choose. That choice is where human voice enters.

### Q12. Key points that MUST be covered
*Example: "Must cover: (1) the memory overhead problem, (2) our specific workaround using off-heap allocation, (3) why we didn't use the standard library solution."*

**Why it matters:** Mandatory coverage points establish the floor. Everything else is the author's discretion. Knowing the floor prevents under-coverage of required material and allows genuine omission elsewhere.

### Q13. Points to explicitly AVOID
*Example: "Do not discuss Kafka Streams — out of scope for this audience. Do not recommend the managed service — the author has strong opinions against vendor lock-in."*

**Why it matters:** Avoidance constraints are as important as coverage constraints. AI defaults to comprehensive coverage. Explicit avoidance instructions enforce the human pattern of selective omission.

### Q14. Real data, metrics, or sources to incorporate
*Example: "Use our actual benchmark numbers: baseline 12ms p99, after optimization 3ms p99. Reference the 2023 DORA report for industry context."*

**Why it matters:** Specificity (Principle 3) is the most consistently detectable humanization signal. Real numbers from real contexts cannot be fabricated plausibly. Providing them front-loads the most valuable humanization work.

### Q15. SEO keywords (if applicable)
*Example: "Primary: 'Kafka consumer lag'. Secondary: 'Kafka performance tuning', 'consumer group rebalancing'."*

**Why it matters:** SEO constraints interact with voice — forced keyword insertion is detectable. Knowing the targets up front allows natural integration rather than retrofitted stuffing.

---

## Section 5: Quality Preferences

Rate each dimension 1–10. These scores calibrate the balance between competing writing virtues.

### Q16. How opinionated should the author be? (1–10)
1 = Pure information delivery, no stances taken
5 = Opinions stated but qualified, alternatives acknowledged
10 = Strong thesis, recommendations given without hedging, willing to be wrong

**Why it matters:** This score directly controls how many "it depends" qualifications are stripped during editing. A 9 or 10 triggers application of Principle 7 (Voice Over Accuracy).

### Q17. How technical? (1–10)
1 = No code, no formulas, all analogy
5 = Occasional code snippets, technical terms defined on first use
10 = Dense implementation detail, assumes domain expertise, no hand-holding

**Why it matters:** Technical register must match audience expertise (Q7). A mismatch in either direction is immediately detectable — either condescending or incomprehensible.

### Q18. How conversational? (1–10)
1 = Formal prose, no contractions, no first person
5 = Occasional "we," some contractions, professionally warm
10 = Direct address to reader, contractions throughout, asides and parentheticals, admits uncertainty

**Why it matters:** Conversational register controls rhythm (Principle 5) and burstiness (Principle 6). Higher conversational scores produce shorter paragraphs, more sentence fragments used deliberately, and more direct-address moments.
