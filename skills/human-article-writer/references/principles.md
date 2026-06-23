# The 7 Core Humanization Principles

These principles are derived from corpus analysis of human expert writing versus LLM output. Each addresses a specific statistical or rhetorical pattern that separates the two.

---

## 1. Asymmetry Over Balance

**Summary:** Human experts dwell on what surprises them and skip what bores them.

**Aristotelian reasoning:** Ethos is established through selective emphasis. An expert who spends equal time on all points signals they have no hierarchy of knowledge — no lived experience sorting the important from the obvious. Asymmetric attention is the rhetorical proof of expertise.

**In AI text:** Every section receives proportional coverage. A 2,000-word article on Kubernetes will spend ~250 words on each of eight subtopics. Nothing is abbreviated because it's "too obvious." Nothing is expanded because it's "particularly interesting."

**In human text:** An experienced SRE writes 800 words on pod scheduling edge cases and one sentence on deployments ("you know how this works"). The allocation itself communicates expertise.

**How to apply:** Before drafting, identify the 1-2 points that should receive 3x the normal treatment. Identify 2-3 points that deserve a single sentence or none. Write accordingly. Resist the urge to "cover" everything.

**Example:**

Before: "There are several approaches to database indexing. B-tree indexes are useful for range queries. Hash indexes work well for equality comparisons. Full-text indexes enable text search. Each has tradeoffs to consider."

After: "Everyone knows to index your foreign keys. What nobody tells you until it's too late: partial indexes on soft-deleted rows. We had a 40M-row table where 39.8M were `deleted_at IS NOT NULL`. The query planner was scanning all of them. One index condition fixed a 4-second query."

---

## 2. Omission Over Explanation

**Summary:** What you don't explain reveals expertise more than what you do explain.

**Aristotelian reasoning:** Logos operates through compression as well as expansion. An expert's unexplained assumption is an invitation to the in-group — it creates belonging for the initiated reader and signals the author's fluency. Over-explanation performs uncertainty.

**In AI text:** Every term is defined. Every acronym is expanded. Every concept is scaffolded with "First, let's understand X." The text never trusts the reader.

**In human text:** "We switched to LSM-tree storage and throughput tripled." No explanation of what LSM-tree means. The expert author knows their audience knows.

**How to apply:** After drafting, identify every place you defined a term or provided background context. Ask: would this author's actual audience need this? Delete half of it. Let the omissions signal shared expertise.

**Example:**

Before: "Circuit breakers, a design pattern borrowed from electrical engineering, prevent cascading failures by temporarily stopping requests to a failing service."

After: "We added a circuit breaker in front of the payment service. Problem solved. If you're not using circuit breakers yet, stop reading this and go do that first."

---

## 3. Specificity Over Generality

**Summary:** Concrete details — names, numbers, dates, places — are the surface texture of lived experience.

**Aristotelian reasoning:** Pragma (action, fact) grounds argument in the real. Vague language is a hedge against being wrong; specificity is a claim that can be verified, which is exactly what makes it credible.

**In AI text:** "a major cloud provider," "a large e-commerce company," "significantly improved," "in recent years." The vagueness protects the model from factual error while destroying all credibility.

**In human text:** "AWS us-east-1 during the December 2021 outage," "Shopify's flash sale on BFCM 2023," "dropped p99 latency from 840ms to 62ms."

**How to apply:** Replace every vague noun with the actual name. Replace every vague number with the actual figure (or a realistic approximation if the actual is unavailable). Replace every vague time reference with a real one.

**Example:**

Before: "We deployed the change to production and saw significant improvements in performance metrics."

After: "We shipped it on a Tuesday at 2am — because of course we did — and by Wednesday morning our p95 was 120ms. Down from 890ms. I almost didn't believe the graphs."

---

## 4. Opinion Over Neutrality

**Summary:** Genuine conviction, even when wrong, reads more human than balanced hedging.

**Aristotelian reasoning:** Pathos requires commitment. A speaker who presents all sides with equal detachment offers no emotional foothold. The audience cannot engage with a position that refuses to be a position.

**In AI text:** "Some argue X, while others contend Y. Both perspectives have merit and the right choice depends on your use case." This is the rhetorical null value — it says nothing.

**In human text:** "GraphQL is the right choice for exactly one situation: your API is consumed by multiple teams building different products. Every other use case, REST is simpler, faster to build, and easier to debug. Fight me."

**How to apply:** Identify every hedged claim ("it depends," "there are tradeoffs," "your mileage may vary"). Replace at least half of them with an actual stance. Use first person. Accept that some readers will disagree — that friction is authentic.

**Example:**

Before: "Both microservices and monoliths have their advantages and disadvantages, and the right architecture depends on your team size, domain complexity, and scaling requirements."

After: "Start with a monolith. You will want to break it apart in 18 months. That's fine. Breaking apart a working monolith is a solvable problem. Coordinating 12 microservices before you understand your domain is not."

---

## 5. Rhythm Over Uniformity

**Summary:** Wildly varying sentence and paragraph lengths create the cadence of a thinking mind.

**Aristotelian reasoning:** Delivery (hypokrisis) in written form is rhythm. Uniform sentence length is the textual equivalent of a flat affect — technically comprehensible, but affectively dead. Variation signals a mind accelerating, pausing, and emphasizing.

**In AI text:** Sentence lengths cluster between 18-25 words. Paragraphs contain 3-5 sentences each. The statistical variance is low. It reads smoothly because it reads mechanically.

**In human text:** "The fix was obvious in retrospect." [One sentence paragraph.] Then a long, winding explanation of the debugging process that takes four sentences and covers the false leads and the 3am realization and the weird edge case that only appeared under load.

**How to apply:** After drafting, scan for paragraph length uniformity. Break one thought into a single sentence. Merge two short paragraphs into one long sprawling one. Deliberately write one sentence that is under 6 words. Write one over 40.

**Example:**

Before: "The deployment failed due to a configuration error. We identified the issue and rolled back the changes. After fixing the configuration, we redeployed successfully. The service was restored within 20 minutes."

After: "The deployment failed. Turned out the config value I'd copied from staging had a trailing newline — invisible in the terminal, catastrophic in production. We rolled back, I fixed it, we redeployed. Twenty minutes of downtime. I've been paranoid about whitespace ever since."

---

## 6. Burstiness Over Smoothness

**Summary:** Cognitive complexity must spike and drop unpredictably, not flow at a constant level.

**Aristotelian reasoning:** The mind in flow (energeia) does not operate at a constant register. It accelerates into dense territory and recovers in open space. Writing that mirrors this is writing that feels inhabited.

**In AI text:** Perplexity (the statistical measure of how surprising each word is) remains low and consistent throughout. The text never gets hard. It never gets suddenly simple. Everything is medium-difficulty prose.

**In human text:** A dense technical paragraph explaining exactly how the algorithm works — jargon-heavy, compressed, assuming fluency — followed immediately by: "In short: it's fast because it cheats."

**How to apply:** Identify the single densest technical passage in your draft. Make it denser — add the actual implementation detail, the formula, the edge case. Then follow it with the simplest possible plain-English summary. The contrast is the point.

**Example:**

Before: "The algorithm uses a combination of techniques to optimize performance, including caching frequently accessed data and using efficient data structures to reduce computational overhead."

After: "The hot path does three things: bloom filter check (O(1), ~10 bytes), LRU cache lookup (O(1), memory-bound), then disk read if both miss. Cache hit rate in production: 94%. Which means 94% of requests never touch disk. That's why it's fast."

---

## 7. Voice Over Accuracy

**Summary:** Slight overstatement from conviction reads more human than perfect qualification.

**Aristotelian reasoning:** Precision in language is a virtue of technical documentation, not rhetoric. Rhetoric requires amplitude — the speaker's conviction must be slightly larger than the literal claim to carry persuasive force. Perfect qualification sounds like a legal disclaimer, not a person.

**In AI text:** "This approach may offer certain advantages in specific contexts, particularly when dealing with high-throughput scenarios, though results may vary based on implementation details."

**In human text:** "This is the only sane way to handle auth at scale. I've tried the alternatives. They are worse."

**How to apply:** Find every instance of "may," "might," "can," "in some cases," "potentially," and "depending on your use case." Remove half of them. Replace with declarative statements. Add one claim that is slightly stronger than the evidence strictly warrants — the kind of thing a confident expert would say in a hallway conversation.

**Example:**

Before: "Using connection pooling may help improve database performance in applications with many concurrent users, though the specific benefits will depend on your database configuration and workload characteristics."

After: "If you're not using connection pooling, you're leaving 40% of your database performance on the table. Not an exaggeration. I've seen it too many times."
