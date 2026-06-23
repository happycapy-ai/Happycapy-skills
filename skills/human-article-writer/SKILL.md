---
name: human-article-writer
description: Generate blog articles and long-form content that reads as genuinely human-written. Evidence-backed by NLP analysis of 1,109 pre-AI-era articles from 19 professional writers. Uses anti-fabrication framework, evidence-backed statistical targets, adversarial committee review, and gold-standard exemplar bank. Use when the user asks to write a blog post, article, thought piece, explainer, or any long-form content.
---

# Human Article Writer v2

Evidence-backed article generation. Calibrated against 1,109 real human articles.

---

## PHASE 0: ANTI-FABRICATION GATE (NON-NEGOTIABLE)

**These rules override everything else in this skill. No exceptions.**

### The 5 Hard Rules

**RULE 1: No constructed scenes.**
Do not write scenes with characters, dialogue, setting, or sensory detail that did not actually occur. A brief experience reference ("in practice, this rarely works") is permitted if the author provided it. A constructed narrative scene is NEVER permitted.

**RULE 2: No unnamed statistics.**
Every specific statistic requires a named source. If the source cannot be named, use directional framing: "research consistently shows..." with a named research tradition. Never invent percentages.

**RULE 3: No vague authority.**
"Many experts," "industry insiders," "a leading company" are fabrication hedges. Name the expert, name the company, or acknowledge the claim is inference from available evidence.

**RULE 4: No false biographical claims.**
Do not claim years of experience, client relationships, or institutional affiliations that do not exist. If writing for an author, use ONLY credentials they provided.

**RULE 5: No performed certainty on uncertain questions.**
Calibrate confidence to evidence. Admission of uncertainty appears in 36.9% of professional articles -- it INCREASES credibility.

### Evidence Base

From corpus analysis of 1,109 articles by 19 professional writers (pre-AI era):

| Metric | Finding |
|---|---|
| Articles with personal stories | 29.5% (70.5% have ZERO stories) |
| Articles using anecdotes as PRIMARY authority | ~0% |
| Declarative openings | 74.8% |
| First-person openings | 8.7% (do NOT default to "I") |
| Substantive analytical endings | 64.4% |

**The fabrication problem**: AI systems default to constructing personal anecdotes because training data rewards narrative engagement. The data shows this is statistically abnormal -- 7 in 10 professional articles contain zero personal narrative.

**See `references/anti-fabrication-framework.md` for the complete framework with replacement strategies.**

---

## PHASE 1: INTAKE

**MANDATORY. Do not skip. Do not assume.**

### 1A: Author Profile

| Question | Why It Matters |
|---|---|
| Professional background | Determines jargon comfort, what they'd explain vs skip |
| Years of experience in this topic | Controls confidence level and opinion strength |
| Opinion stance on this topic | Strong opinions / balanced reporter / curious explorer |
| Cultural/regional context | Determines vocabulary register, currency, cultural references |
| **Real stories/experiences to include (if any)** | Only include stories the author ACTUALLY provides |

**Critical**: If the author provides no personal stories, write WITHOUT stories. 70.5% of professional articles do this successfully.

### 1B: Target Audience

| Question | Why It Matters |
|---|---|
| Expertise level | Determines what to explain vs assume known |
| What they're trying to decide | Shapes the article's implicit promise |
| Where they'd read this | Sets format expectations and formality |

### 1C: Publication Format

| Format | Default Opening | Authority Mechanism |
|---|---|---|
| **Explainer** | Declarative claim about what's misunderstood | Industry knowledge + data citation |
| **Practitioner blog** | Declarative position or data point | Specific examples + experience references (ONLY if author-provided) |
| **Technical deep-dive** | Problem statement | Industry knowledge + specific examples |
| **Thought leadership** | Contrarian claim or tension | Data citation + historical analogy |
| **Comparison/review** | Named options + the tension between them | Specific examples + data citation |
| **Case study** | Outcome data point | Specific examples + credential signaling (author-provided only) |

### 1D: Additional Requirements

- Target word count (default: 1500-2500)
- Key points that MUST be covered
- Points to explicitly AVOID
- Real data/sources to incorporate (strongly encouraged)

---

## PHASE 2: AUTHORITY ARCHITECTURE

**Before writing, choose 2-3 authority mechanisms from this evidence-ranked list.**

### Tier 1 -- Primary (used in 50%+ of professional articles)

1. **Specific Examples (66.2%)** -- Named companies, documented events, real products. "Salesforce's 2023 restructuring" not "a major tech company."
2. **Industry Knowledge (64.6%)** -- Process-level mechanism explanation. "Procurement cycles span 6-18 months because legal, security, and finance sign-off are sequential" not "the process takes time."
3. **Data Citation (55.4%)** -- Named indices, published ratios, verifiable figures. Precision signals research. Round numbers signal fabrication.

### Tier 2 -- Secondary (25-50% of articles)

4. **Historical Analogy (44.6%)** -- Real historical events with accurate dates and outcomes.
5. **Credential Signaling (41.5%)** -- One clause stating role/institution. NOT a constructed scene. ONLY if author-provided.
6. **Experience Reference (40.0%)** -- Brief, non-narrative. "In practice, this rarely works" NOT "I remember sitting in a boardroom..."
7. **Admission of Uncertainty (36.9%)** -- Counterintuitively increases credibility. "The data here is thin" is a credibility signal.

### Tier 3 -- Supporting (<30%)

8. **Counterargument Engagement** -- Address the strongest opposing view.
9. **Hedged Projection** -- "If X, then likely Y" with explicit uncertainty.

**Default combination**: Specific Examples + Industry Knowledge + Data Citation. This covers 90%+ of article types without requiring any personal stories.

---

## PHASE 3: RAW DRAFT

**Do NOT start writing yet.** First, build a reader journey map. Then draft in the order the READER needs, not in outline order.

### 3A: Reader Journey Map (MANDATORY before drafting)

Before writing a single sentence, answer these five questions:

1. **What does the reader already know?** List 3-5 things the target audience takes for granted. These get ONE sentence max, or zero -- never explain what they already understand.
2. **What's their first question?** When the reader sees the topic, what do they immediately want to know? Open with THIS, not with a reframe or thesis statement.
3. **Where will they get confused?** Identify the 1-2 concepts that need plain-English explanation. These get TEACHING paragraphs -- walkthrough, definition, analogy. No argument, just help.
4. **What's the surprising part?** The one insight they didn't expect. This gets 3x depth. Build toward it.
5. **What should they do with this?** The practical takeaway. Not a call to action. Just: what changes in how they think or act.

Draft in the order these questions suggest. The reader's curiosity drives structure, not your outline.

### 3B: Section Shape Diversity (NON-NEGOTIABLE)

**No two consecutive sections may use the same argumentative shape.** This is the #1 anti-AI-detection rule. Structural monotony -- where every section follows the same pattern of claim-reframe-stat-contrast -- is the strongest signal that text is AI-generated.

Choose from these shapes. Each section gets ONE:

| Shape | What it looks like | Example opening |
|---|---|---|
| **Reframe** | Common view is wrong, here's why | "The conventional wisdom says X. It's wrong." |
| **Walkthrough** | Step-by-step explanation, no argument | "Here's how it actually works." |
| **Direct opinion** | Strong claim, then support | "This is a bad idea. Here's why." |
| **Teaching** | Explain a concept the reader needs | "Before we go further, you need to understand X." |
| **Example-first** | Start with a specific case, extract the principle | "When Company X did Y, here's what happened." |
| **Question-driven** | Pose the reader's question, then answer it | "So why does this matter for [audience]?" |
| **Data narrative** | One stat, then unpack what it means in plain English | "That number -- $X billion -- needs context." |

**Constraint:** If section 1 is "Reframe," section 2 MUST be a different shape. If you find yourself writing claim-reframe-stat-contrast again, stop and switch shapes.

**Constraint:** The "Not X, but Y" contrast device may appear at most TWICE in the entire article. This is the single most common AI tell in analytical writing.

### 3C: Conversational Scaffolding (MANDATORY)

The article must contain at least 3 moments where the writer talks TO the reader or manages their attention. These are not transitions. They are the writer acknowledging a human is reading.

Examples:
- "Bear with me on this -- it connects."
- "Now here's the part that matters."
- "You might be wondering why any of this matters for [specific audience]. Fair question."
- "Let's step back for a second."
- "Put all this together and you can see why..."
- "So what does this actually mean in practice?"
- "That sounds abstract. Here's what it looks like."

These must feel natural, not inserted. They work best at transitions between sections or before a complex explanation.

### 3D: Stat Embedding (replaces stat-stacking)

**Max 1 statistic per paragraph.** Every statistic must be EITHER preceded or followed by a plain-English sentence explaining what it means. Statistics exist to help the reader understand, not to signal authority.

BAD (stat-stacking):
> "The LXP sub-segment went from $508.5 million in 2020 to a projected $2.186 billion by 2026, per Mordor Intelligence -- a 25.3% CAGR that is directionally consistent with disclosed growth at Degreed, Cornerstone, and 360Learning."

GOOD (stat-embedding):
> "Learning experience platforms -- think Netflix-style interfaces that recommend courses based on your role -- barely existed five years ago. They were a $500 million niche. Now they're closing in on $2 billion, per Mordor Intelligence. That kind of growth tells you the spending is moving, not just growing."

The first version signals research. The second helps the reader understand.

### 3E: Evidence-Backed Statistical Targets

These are SECONDARY to the rules above. Check these AFTER drafting, not during.

| Metric | Human Average (n=1,109) | AI Average | Target |
|---|---|---|---|
| Mean sentence length | 25.6 words | 20.5 words | 23-28 words |
| Sentence length std dev | 15.7 words | 9.2 words | > 14 words |
| Average word length | 4.74 chars | 5.59 chars | < 5.0 chars |
| Flesch readability | 54.5 | -- | 48-60 |

### 3F: Opening and Closing

**Opening (first 2 sentences):**
- Start with the reader's first question or the most concrete thing about the topic. A number. A company name. A specific event. NOT a reframe, NOT a thesis statement, NOT a definition.
- 74.8% of human articles open declaratively. But "declarative" means a specific claim, not "The X industry is undergoing a transformation."

**Closing (final paragraph):**
- 64.4%: substantive analytical content that advances the argument
- 24.2%: short crystallizing punch (one sentence)
- NEVER: "In conclusion...", "Ultimately...", motivational summary, or call to action

### 3G: Hard Constraints

```
NEVER:
- Use the em dash character "—" anywhere in the article (not in titles, headings, body text, or punctuation). Use a comma, colon, parentheses, or rewrite the sentence instead.
- Fabricate personal stories, anecdotes, or experiences
- Invent statistics or data points without named sources
- Use "many experts believe" or "industry insiders say"
- Claim biographical credentials not provided by the author
- Start a paragraph with a topic sentence that previews its content
- Use Tier 1 banned vocabulary (see references/ai-vocabulary-database.md)
- Cover all subtopics with equal depth
- End with "In conclusion" or any summarizing formula
- Use "Not X, but Y" / "Not X. Y." contrast more than twice in the entire article
- Stack 2+ statistics in a single paragraph without plain-English explanation
- Use the same argumentative shape in consecutive sections
- Write paragraphs that follow: claim -> reframe -> stat -> contrast -> punch line (this is THE AI pattern)

ALWAYS:
- Spend 3x more words on the surprising insight than the expected one
- Include specific, named examples (companies, events, dates)
- Vary sentence length wildly (std dev > 14 words)
- Use simpler words (avg < 5 chars) -- "use" not "utilize"
- Let one section be noticeably longer than others (asymmetric depth)
- Express the author's stance (not balanced hedging)
- Include at least 3 moments of conversational scaffolding (talking TO the reader)
- Include at least 1 teaching paragraph that explains a concept in plain English with no argument
- Precede or follow every statistic with a plain-English sentence explaining what it means
- Let at least 1 section be a walkthrough or teaching section with no thesis
```

---

## PHASE 4: DETECTION & ANTI-FABRICATION SCAN

### 4A: Fabrication Check (MOST CRITICAL)

For each paragraph, ask:
1. Does this contain a personal story? If yes: was it provided by the author? If no: DELETE.
2. Does this contain a specific statistic? If yes: can I name the source? If no: rewrite as directional claim.
3. Does this reference "experts" or "insiders"? If yes: can I name them? If no: rewrite.
4. Does this claim experience or credentials? If yes: were these provided by the author? If no: DELETE.

### 4B: Statistical Scan

| Metric | AI Signature | Human Target |
|---|---|---|
| Sentence length std dev | 4-9 words | > 14 words |
| Average word length | > 5.5 chars | < 5.0 chars |
| Paragraph length variance | Uniform | High (1-sentence to 10-sentence) |
| Section depth ratio | All ~equal | Longest >= 2x shortest |
| Adversative transitions | < 8/article | > 12/article |

### 4C: Vocabulary Scan

**See `references/ai-vocabulary-database.md` for the complete 450+ word database.**

| Category | Flag | Replace With |
|---|---|---|
| Power words | genuinely, comprehensive, robust, crucial | actually, full, solid, important (or delete) |
| Formal verbs | utilize, leverage, facilitate, navigate | use, use, help, deal with |
| Transitions | Furthermore, Moreover, Nevertheless | And, Plus, But, Also (or delete) |
| Hedges | It's worth noting, It's important to consider | [delete -- just state the thing] |

---

## PHASE 5: COGNITIVE TRANSFORMATION

### 5A: Shape Diversity Audit

1. Label each section with its argumentative shape (Reframe / Walkthrough / Direct opinion / Teaching / Example-first / Question-driven / Data narrative)
2. Are any two consecutive sections the same shape? If YES: rewrite one.
3. Count "Not X, but Y" / "Not X. Y." contrasts. If more than 2 in the full article: cut until 2 or fewer.

### 5B: Conversational Scaffolding Check

1. Count moments where the writer talks TO the reader. Minimum 3 required.
2. If fewer than 3: add them at section transitions or before complex explanations.
3. These must feel natural -- not bolted on. If they sound forced, rewrite the surrounding paragraph to accommodate them.

### 5C: Stat Embedding Check

1. Find every paragraph with 2+ statistics. Split them or remove one.
2. For every remaining statistic: is there a plain-English sentence before or after it explaining what it means? If no: add one.
3. If a stat exists only for authority signaling and doesn't help the reader understand: cut it.

### 5D: Asymmetric Depth

1. Identify all subtopics in the draft
2. Which insight is most non-obvious?
3. Expand that to 3x depth. Compress the obvious points.

### 5E: Expertise Calibration

1. For each explanation: would the TARGET AUDIENCE already know this?
2. If yes: DELETE the explanation. Use jargon directly.
3. If partially: compress to a clause, not a paragraph.
4. If the audience does NOT know it: give it a full teaching paragraph. Don't argue -- just explain.

### 5F: Opinion Injection

1. Identify all hedged claims ("it depends," "there are tradeoffs")
2. Does the author have a clear preference?
3. If yes: preferred option gets 3x detail. Compress alternatives.
4. Include at least one strong unhedged claim.

### 5G: Structural Irregularity

- One paragraph starts with an example BEFORE the principle
- One 1-2 sentence paragraph between two long ones
- One tangent that isn't strictly necessary
- Vary paragraph lengths deliberately
- At least one section that is pure teaching/walkthrough with no thesis statement

---

## PHASE 6: ADVERSARIAL COMMITTEE REVIEW

**Each reviewer is a SEPARATE AGENT with its own identity.**

### 8 Permanent Agents + 1 Runtime Domain Expert

| # | Agent ID | Role | Must Find |
|---|---|---|---|
| 1 | `article-statistician` | Burstiness/variance auditor | Most statistically "AI" passage |
| 2 | `article-vocabulary-cop` | AI-marker word hunter | Remaining marker words |
| 3 | `article-cognitive-architect` | Asymmetric attention enforcer | Where coverage is too proportional |
| 4 | `article-fabrication-detector` | **Anti-fabrication enforcer** | **Any fabricated story, stat, or credential** |
| 5 | `article-attention-psych` | Reader engagement modeler | Where reader attention drops |
| 6 | `article-structure-breaker` | Pattern-detection adversary | Most formulaic structural pattern |
| 7 | `article-human-reader` | "Would I share this?" test | Where article stops feeling human |
| 8 | `article-monotony-detector` | **Structural monotony detector** | **Consecutive sections using the same argumentative shape** |
| 9 | *(runtime-generated)* | Domain-specific insider | Terminology a real practitioner wouldn't use |

**Agent #8 is the most critical anti-AI-detection agent.** It reads ONLY the first and last sentence of each section and checks: (a) do consecutive sections follow the same claim-reframe-stat-contrast pattern? (b) does "Not X, but Y" appear more than twice? (c) are statistics stacked without plain-English explanation? (d) is there conversational scaffolding (writer talking to reader)?

### Orchestration: Convergence Loop

```
LOOP:
  Step 1: Parallel review (agents 1-7)
  Step 2: Structural Monotony Detector review (agent 8) -- runs AFTER agents 1-7
  Step 3: Collect findings from agents 1-8 -- any FAIL?
    YES -> Apply fixes, return to Step 1
    NO  -> Proceed to Step 4
  Step 4: Domain Insider review (agent 9)
    FAIL -> Apply fix, return to Step 1
    PASS -> EXIT LOOP
```

**Agent 8 priority:** If the Structural Monotony Detector fails, its fixes take priority over all other agents. Structural monotony is the #1 reason articles get flagged as AI-written.

**Safety valve:** Maximum 5 cycles.

---

## PHASE 7: FINAL VALIDATION

### 7A: Anti-Fabrication Final Check

The article MUST pass all 5 hard rules with zero violations before output.

### 7B: Statistical Re-Scan

| Metric | Must Meet |
|---|---|
| Sentence length std dev | > 14 words |
| AI-marker vocabulary | 0 Tier 1, <= 2 Tier 2 |
| Asymmetric depth ratio | Longest section >= 2x shortest |
| Average word length | < 5.0 chars |
| Adversative transitions | > 12 per article |

### 7C: Human-Feel Score (1-100)

Score on 10 dimensions:
1. Voice consistency
2. Asymmetric depth
3. Expertise markers (audience-appropriate)
4. Emotional commitment (opinions, not hedging)
5. Structural irregularity
6. Vocabulary naturalness
7. **Fabrication absence** (zero fabricated stories/stats/credentials)
8. **Section shape diversity** (no two consecutive sections use the same argumentative shape)
9. **Conversational scaffolding** (at least 3 moments where writer talks TO the reader)
10. **Stat embedding** (every stat has plain-English context, max 1 stat per paragraph)

### 7D: The Replacement Test (Aristotelian)

> "If we replaced this article with a typical AI-generated article on the same topic, what would be LOST?"

If the answer is "nothing specific" -- the article needs more work.

---

## PHASE 8: OUTPUT

### Default Output
```
[Article title]

[Full article body]

---
Word count: X | Human-feel score: X/100 | Format: [type]
Authority mechanisms: [list of 2-3 used]
Fabrication check: PASS (0 violations)
```

### 8B: Downloadable Artifacts (Markdown + HTML)

When the user wants a downloadable artifact — which is the default when this skill is invoked from the HappyCapy `/tools` page — save the final article as both Markdown and a self-contained HTML file.

**Step 1:** Build a JSON metadata file with this exact shape:

```json
{
  "title": "[Article title]",
  "format": "[Explainer | Practitioner blog | Technical deep-dive | Thought leadership | Comparison/review | Case study]",
  "word_count": 0,
  "human_feel_score": 0,
  "authority_mechanisms": ["Specific Examples", "Industry Knowledge", "Data Citation"],
  "fabrication_check": "PASS (0 violations)",
  "body": "[Full article body as plain Markdown string]"
}
```

**Step 2:** Run the artifact script using its absolute path within the skill installation:

```bash
python3 ~/.claude/skills/human-article-writer/scripts/save_artifacts.py \
  --input /tmp/haw-output.json \
  --output-dir ./outputs/human-article-writer \
  --basename article
```

**Step 3:** Confirm the two files exist and report them to the user:

```
Saved Markdown: ./outputs/human-article-writer/article.md
Saved HTML:     ./outputs/human-article-writer/article.html
```

The HTML file is self-contained (inline CSS, no external dependencies) and can be opened directly in a browser, published as a standalone page, or converted further.

---

## REFERENCES

- **Anti-Fabrication Framework:** `references/anti-fabrication-framework.md` (17K chars, evidence-based)
- **Evidence-Backed Principles:** `references/evidence-backed-principles.md` (18 principles from corpus analysis)
- **Exemplar Bank:** `references/exemplar-bank.md` (35 gold-standard articles)
- **AI Vocabulary Database:** `references/ai-vocabulary-database.md` (450+ words/phrases)
- **Committee Personas:** `references/committee-personas.md`
- **AI Detection Research:** `references/ai-detection-research.md`

## CORPUS PROVENANCE

All statistical targets derived from NLP analysis of:
- **1,109 articles** from **19 professional writers** (pre-AI era, 2010s)
- Sources: Paul Graham, Aswath Damodaran, John Hempton, Fred Wilson, Barry Ritholtz, Bill Gurley, Benedict Evans, Cullen Roche, Brooklyn Investor, Safal Niveshak, Asian Century Stocks, China Money Network, Marginal Revolution, Calculated Risk, Tren Griffin, Josh Brown, Philosophical Economics, Interfluidity, Morgan Housel
- Total corpus: 2.18M words
- Contrastive analysis: 60 paired human/AI articles across 2 models
- Rhetorical analysis: 65 articles deep-analyzed by Claude Sonnet
- Principle extraction: 18 evidence-backed principles via multi-round LLM synthesis
- Exemplar curation: 35 gold-standard articles via tournament ranking
