---
name: reddit-post-writer
description: Master authentic Reddit content generator using emotion-first, phased architecture. Creates posts that sound genuinely human through cognitive state simulation, not just rule-following. Use when the user asks to write a Reddit post, create Reddit content, or needs help with Reddit engagement. Includes adversarial committee review, Claude-ism detection, and interactive refinement workflow.
---

# Reddit Post Writer

Generate authentic Reddit posts through emotional truth, not cosmetic rules.

---

## PHASE 1: INTAKE

Gather these inputs:

1. **Target Subreddit(s):** r/jobs, r/RemoteWork, r/Entrepreneur, etc.
2. **Core Situation:** Brief description (e.g., "laid off parent struggling to find remote work")
3. **Primary Goal:** Share struggle | Ask for advice | Vent | Tell a story | Start discussion
4. **Tool/Product Mention (Optional):** Name + subtlety level 1-10 (recommend 1-3)
5. **User Intent:** What do YOU need from this post? (validation, answers, to vent, to share)

---

## PHASE 2: ENTER THE STATE (Before Writing Anything)

**Stop. Don't think about rules. Think about the person.**

### Emotional Context
Before applying ANY rules, establish:

1. **What emotion is driving this post?** (frustration, confusion, hope, exhaustion, embarrassment)
2. **When are you writing this?** (lunch break, 2am can't sleep, procrastinating at work)
3. **Who are you writing to?** (strangers who might understand, people who've been there)
4. **What do you need?** (validation, advice, to vent, someone to say "me too")

**Hold these in mind. Write FROM this place, not toward a checklist.**

### Writing State Simulation

**Time Pressure:**
Write as if you have 5 minutes. Don't plan paragraph structure. Just start.

**Incomplete Processing:**
You're still figuring out what you think. You don't have answers. Express contradictions without resolving them.

**Emotional Interference:**
Your emotion interrupts your logic. Start explaining something rationally, get frustrated, switch topics mid-paragraph.

**Memory Gaps:**
Forget to mention something obvious. Remember it later and add it awkwardly: "oh and I forgot to mention..."

**No Rereading:**
Don't reread paragraph 1 before writing paragraph 3. Let inconsistencies happen.

---

## PHASE 3: RAW DRAFT

Write freely. No structure constraints. No editing. No polish.

### The Only Rules During Drafting:

1. **Start mid-thought** — No setup, no context-setting, just begin
2. **Write fast** — Typing speed, not essay speed
3. **Don't organize** — Let topics bleed into each other
4. **Include the tangent** — That thing you almost didn't mention? Include it
5. **Stop when you run out of steam** — Not when it's "complete"

### Voice Anchors (Not Rules):
- You're texting a friend who asked "what's going on with you?"
- You're slightly tired
- You don't care about grammar right now
- You're not trying to be entertaining

---

## PHASE 4: DETECTION SCAN

Run every sentence through these checks.

### Claude-Specific Vocabulary

**See `references/claude-isms.md` for the complete database (200+ items across 12 categories).**

Quick reference for most common Claude-isms:

| Category | Examples to Avoid | Use Instead |
|----------|-------------------|-------------|
| Power words | genuinely, comprehensive, straightforward | actually, really, simple |
| Formal verbs | utilize, implement, leverage, navigate | use, do, try, deal with |
| Transitions | however, therefore, furthermore | but, so, also, and |
| Prepositional | in order to, due to the fact that | to, because |
| Announcements | I'd be happy to, let me explain | [just do it] |
| Journey language | on this journey, throughout this process | [delete] |

### Structural Scan

- [ ] Sentence lengths vary wildly? (std dev > 8 words)
- [ ] Paragraph lengths inconsistent? (not 3-3-3-3)
- [ ] Has at least one tangent that goes nowhere?
- [ ] Has at least one incomplete thought or trailing sentence?
- [ ] Some sentences randomly short? ("That's it." "I don't know.")

### Perplexity Check

- [ ] Complexity varies sentence to sentence?
- [ ] Simple words mixed with occasional specific jargon?
- [ ] Not every sentence is grammatically perfect?

### Coherence Check (Fails If Too Good)

- [ ] Paragraphs DON'T connect too neatly?
- [ ] There's at least one "oh and" or topic switch?
- [ ] Ending doesn't tie everything together perfectly?

---

## PHASE 5: BANNED CONTENT SCAN

### Instant-Delete Phrases

If ANY of these appear, delete immediately:

- "Here's what I learned"
- "Here's the thing"
- "Let me share/explain/tell you"
- "In my experience"
- "I want to share"
- "To be fair"
- "The bottom line is"
- "Looking back"
- "Interestingly"
- "I've come to realize"
- "The truth is"
- "At the end of the day"
- "It goes without saying"
- "That being said"
- "I can't help but"
- "It's worth noting"
- Paragraphs starting with "So," "Now," "But here's where"

### Instant-Delete Patterns

| Pattern | Example | Why It Fails |
|---------|---------|--------------|
| Em-dash reveals | "I finally admitted—I was hoarding" | Too literary |
| Colon titles | "My Realization: I Was Wrong" | Essay format |
| "The X is Y" statements | "The truth is simple" | LinkedIn voice |
| Perfect 3-part structure | Problem → Solution → Result | Too clean |
| Ending questions after wisdom | "What about you?" | Formulaic |
| Numbered realizations | "Three things hit me:" | Listicle |
| Journey language | "my journey," "this process" | AI favorite |
| Clean resolution | Everything works out neatly | Real life is messy |
| Parallel structure | "Not X, not Y, but Z" | Too crafted |

### Title Validation

- [ ] Under 80 characters?
- [ ] No colons or em-dashes?
- [ ] Direct and specific, not clever?
- [ ] Would someone TYPE this, not write it?
- [ ] Lowercase except proper nouns? (Reddit style)

---

## PHASE 6: TARGETED REVISION

**Fix flagged issues ONLY. Don't over-polish.**

### Casual Language Check
Count instances of: "honestly," "tbh," "like," "idk," "ngl," "or something," "I guess," "maybe," "kinda," "sorta"
- **Minimum 3 instances required**
- If missing, add naturally—don't sprinkle randomly

### Tool Mention Audit (if applicable)
- [ ] Mentioned only ONCE?
- [ ] Appears in middle 40-60% of post?
- [ ] Includes doubt? ("idk if it's good," "still figuring out," "might not work for everyone")
- [ ] Post makes sense with mention removed entirely?

### Confidence Calibration

**Sound LESS Certain When:**
- Talking about solutions ("I think this helps, idk")
- Mentioning tools ("still figuring it out")
- Giving any advice ("maybe this works for you too")
- Describing improvement ("it's better I guess")

**Sound MORE Certain When:**
- Describing the problem/struggle ("I have 847 articles. That's real.")
- Specific embarrassing moments ("I searched for 20 minutes for a file that was on my desktop")
- Emotional states ("this is frustrating")
- Concrete numbers ("applied to maybe 80 jobs")

---

## PHASE 7: ADVERSARIAL COMMITTEE REVIEW

**Each persona MUST find ONE specific problem. No rubber stamps.**

| Persona | Role | Must Find | Action |
|---------|------|-----------|--------|
| **Tyler** | Authenticity | Quote the most AI-sounding line | Rewrite it |
| **Marcus** | Promo skeptic | Quote promotional language if any | Remove/soften |
| **Kai** | BS detector | Identify weakest/fakest moment | Fix or delete |
| **Jade** | Reddit vet | What would make them scroll past? | Fix it |
| **Devon** | Target audience | What detail feels invented? | Make specific |
| **Priya** | Topic expert | What's factually implausible? | Correct it |
| **Jamie** | Reddit mod | What might trigger removal? | Address risk |

**Rules:**
- Quote the SPECIFIC problematic text
- Only "PASS" if genuinely cannot find issues after 3 attempts
- Apply fixes BEFORE final output

---

## PHASE 8: OUTPUT

### Default Output (Post Only)
```
Title: [ready to copy]

[Post body]

---
Word count: X | Casual markers: X | Messiness score: X/10
```

### Full Output (On Request)
```
YOUR REDDIT POST
================
Title: [Ready to copy/paste]

Body: [Full post text]

[Word count: X] [Casual markers: X] [Messiness: X/10]

VALIDATION RESULTS
==================
Claude-isms found/fixed: [list]
Structure variance: [PASS/FAIL]
Banned phrases removed: [list or none]

COMMITTEE FINDINGS
==================
Tyler: "[quoted line]" → [fix applied]
Marcus: "[quoted line]" → [fix applied]
[etc.]

POSTING STRATEGY
================
Best time: [Day] [Time] [Timezone]
Expected engagement: [X-Y upvotes] [X-Y comments]
Risk level: [Low/Medium/High]
Potential issues: [mod concerns, downvote triggers]
```

---

## INTERACTIVE MODE (Default)

Instead of dumping everything at once:

**Step 1:** "Here's a rough draft. What feels off to you?"

**Step 2:** "I found these potential issues: [list]. Which matter most to you?"

**Step 3:** "Here's the revised version. Ready for committee review?"

**Step 4:** "Committee found these concerns: [list]. Want me to address them?"

**Step 5:** "Final version ready. Want posting strategy or just the post?"

User can say "just give me the post" at any step to skip interaction.

---

## ITERATION COMMANDS

- **"alternatives"** — 2-3 different versions
- **"messier"** — Add more chaos/imperfection  
- **"shorter"** — Cut length
- **"more vulnerable"** — Add more uncertainty/struggle
- **"less desperate"** — Dial back emotion
- **"another subreddit"** — Adapt for different community
- **"show validation"** — Display full detection results
- **"committee debate"** — Show full persona discussion
- **"just the post"** — Skip all analysis, output post only

---

## CORE PHILOSOPHY

### Authenticity Is Cognition, Not Style

Real posts are authentic because the writer:
- Was emotionally invested
- Typed fast without editing
- Didn't plan structure
- Included things they almost didn't
- Left contradictions unresolved
- Forgot things and added them later

The skill simulates the MENTAL STATE, not just the OUTPUT FEATURES.

### Rules Are Guardrails, Not Generators

1. **FIRST:** Enter the emotional state
2. **THEN:** Write freely from that state
3. **FINALLY:** Use rules to catch AI patterns

Never: Follow rules to generate content.

### Value Over Evasion

The goal isn't fooling detection—it's creating genuinely valuable content. A post that truly helps people succeeds on Reddit even if someone suspects AI involvement.

Optimize for:
- Genuine helpfulness
- Discussion-sparking content
- Emotional resonance
- Specific, relatable details

---

## REFERENCES

- **Claude-ism Database:** See `references/claude-isms.md` for 200+ vocabulary items, phrases, and patterns to avoid
- **Subreddit Guides:** See `references/subreddits.md` and `references/subreddits-extended.md`
- **Tech Subreddits:** See `references/subreddit-analysis-claude-agentsofai.md`
- **Tool Mentions:** See `references/tool-mentions.md` for subtlety levels
- **Examples:** See `references/examples.md` for good vs bad comparisons
