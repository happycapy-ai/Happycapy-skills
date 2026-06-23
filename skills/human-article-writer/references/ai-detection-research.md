# AI Text Detection: Research Summary

Dense reference document. Intended for use in calibrating humanization decisions against the actual mechanisms detectors use.

---

## 1. The 5 Mathematical Signatures of AI Text

### 1.1 Low Perplexity
Perplexity measures how surprised a language model is by a sequence of tokens:

```
PPL(x) = exp(-1/N * Σ log P(xᵢ | x₁...xᵢ₋₁))
```

LLMs generate text by selecting high-probability continuations. The result is text where each token is highly predictable given its context — low perplexity. Human writers make unexpected word choices, introduce domain-specific jargon unpredictably, and produce higher mean perplexity scores. GPTZero and most commercial detectors use per-sentence perplexity as their primary feature.

### 1.2 Low Burstiness (Perplexity Standard Deviation)
Human text has high variance in perplexity across sentences. Some sentences are very predictable (transitions, closings); others are highly surprising (novel claims, technical specifics). AI text has low perplexity variance — every sentence is roughly equally probable. Burstiness is measured as:

```
Burstiness = std(PPL(s₁), PPL(s₂), ..., PPL(sₙ))
```

A high burstiness score is the strongest single signal of human authorship. This is the mathematical basis for Principle 6 (Burstiness Over Smoothness).

### 1.3 Negative Log-Probability Curvature (DetectGPT)
Mitchell et al. (2023) showed that AI-generated text tends to occupy local maxima in the model's probability landscape. Given a passage x, if you sample perturbations x̃ (minor rewrites), AI text satisfies:

```
log p(x) - E[log p(x̃)] > 0
```

Human text does not reliably satisfy this. The intuition: AI text is already at a local high-probability peak, so perturbations make it less probable. Human text is not at a peak, so perturbations may improve or worsen probability roughly equally.

### 1.4 Top-Rank Token Clustering (GLTR)
Gehrmann et al. (2019) introduced the Green-Light-Red visualization. Each token is classified by its rank in the model's probability distribution at that position: top-10 (green), top-100 (yellow), top-1000 (red), other (purple). AI text is predominantly green — it selects top-ranked tokens. Human text has a more uniform distribution across ranks, with frequent red and purple tokens representing unexpected choices.

### 1.5 Proportional Coverage (Information Structure)
AI text exhibits uniform information density: each paragraph contributes roughly equal amounts of new information. This manifests as proportional section lengths, balanced treatment of subtopics, and consistent lexical diversity across the document. Human experts write asymmetrically — dense on their specialization, thin on adjacent areas they consider obvious. This structural signature is harder to quantify but underlies most "it feels like AI" human judgments.

---

## 2. Key Papers and Findings

| Paper | Year | Key Finding |
|---|---|---|
| Gehrmann et al., "GLTR: Statistical Detection and Visualization of Generated Text" | 2019 | Top-rank token analysis achieves ~73% detection accuracy; humans can detect AI text at ~54% without tool assistance |
| Mitchell et al., "DetectGPT: Zero-Shot Machine-Generated Text Detection" | 2023 | Curvature-based method achieves AUROC 0.95+ on same-model detection without training data |
| Liang et al., "GPT Detectors Are Biased Against Non-Native English Writers" | 2023 | Commercial detectors flag non-native English essays as AI-generated at 61.3% rate vs. 5.9% for native speakers; TOEFL essays misclassified at near-100% rate by some tools |
| Sadasivan et al., "Can AI-Generated Text Be Reliably Detected?" | 2023 | Proves theoretical ceiling: as LLM quality improves, total variation distance between human and AI distributions shrinks; reliable detection may be impossible asymptotically |
| Kobak et al., "Delving into ChatGPT Usage in Academic Writing" | 2024 | Analyzed 14M abstracts; found 454 words with statistically excess frequency post-ChatGPT release (notably: "commendable," "meticulous," "pivotal," "intricate," "underscore"); estimates 10% of 2024 abstracts contain AI-generated text |
| Hans et al., "Binoculars: Zero-Shot Detection of LLM-Generated Text" | 2024 | Cross-model perplexity ratio (observer model / scorer model) achieves AUROC 0.99 at 0.01% FPR; significantly outperforms DetectGPT |
| Krishna et al., "Paraphrasing Evades Detectors of AI-Generated Text" (DIPPER) | 2023 | Paraphrasing attack using a 11B-parameter model drops DetectGPT detection rate from 70.3% to 4.6%; watermarking schemes similarly broken |

---

## 3. How Major Detectors Work

### GPTZero
Primary signals: mean perplexity (called "perplexity" in their UI) and burstiness (called "burstiness"). Scores each sentence individually, flags documents where mean sentence perplexity falls below a threshold (~15-20 on their internal scale) AND burstiness is low. Uses a fine-tuned version of a GPT-2-class model as the scoring model. Known to struggle with domain-specific technical writing where legitimate jargon artificially inflates perplexity. Reports a per-sentence probability score and a document-level classification.

### Turnitin
Added AI detection in April 2023. Uses an ensemble approach combining perplexity scoring, stylometric features, and a classifier trained on confirmed AI/human pairs. Reports a percentage score (0–100% "AI-written"). Turnitin's published false positive rate is <1% at their default threshold, but Liang et al.'s findings on non-native English suggest this claim does not generalize. Turnitin does not publish their model architecture.

### Originality.ai
Claims to be calibrated specifically for GPT-4 and Claude outputs. Uses perplexity + burstiness + an undisclosed third signal they call "readability pattern analysis." Marketed to publishers and content agencies rather than academics. Published accuracy claims: 94% on GPT-4 text, 96% on GPT-3.5. No independent replication of these figures.

### Binoculars (Academic)
Hans et al.'s method uses two separate models: a "scorer" and an "observer." The key metric is:

```
Binoculars score = log P_scorer(x) / log P_observer(x)
```

When both models agree a sequence is highly probable, the ratio is ~1 (AI-generated). When the scorer finds it probable but the observer does not (genuine human idiosyncrasy), the ratio diverges. This cross-model approach is more robust than single-model perplexity and achieves state-of-the-art performance. Currently only available as a research tool.

---

## 4. Known Weaknesses of Current Detectors

**Non-native English bias:** Liang et al. (2023) found commercial detectors misclassify non-native English writing as AI-generated at 61.3%, versus 5.9% for native speakers. TOEFL essays from genuine test-takers were flagged as AI at rates approaching 100% by some tools. The mechanism: non-native speakers use more conservative, higher-frequency vocabulary — the same pattern as LLM output.

**Paraphrasing attack:** The DIPPER system (Krishna et al.) demonstrates that controlled paraphrasing drops DetectGPT's detection rate from 70.3% to 4.6% and Watermark detection from 97.5% to 23.2%. Paraphrasing preserves semantics while redistributing token probabilities away from the AI-generation peak. This is the most practically significant weakness for adversarial use.

**Literary style reduction:** Studies applying GPT-4 to generate text in the style of literary fiction (complex syntax, non-standard structures, deliberate ambiguity) reduce detection rates from ~100% on standard AI prose to ~13%. Literary register inflates perplexity and burstiness by design.

**Domain-specific technical text:** High-density technical writing (code-adjacent prose, mathematical descriptions, formal specifications) has naturally low perplexity because the vocabulary and syntax are highly constrained. Legitimate expert technical writing is frequently misclassified as AI-generated.

**Theoretical ceiling:** Sadasivan et al. (2023) prove that as generative model quality approaches human distribution quality, the total variation distance between the two distributions approaches zero. Any classifier's error rate is lower-bounded by this distance. As models improve, reliable detection becomes mathematically impossible at low false-positive rates.

---

## 5. Practical Implications for This Skill

**Target burstiness, not just perplexity.** Most humanization advice focuses on "making text less predictable" (perplexity). But burstiness — the variance in predictability — is the stronger signal and less discussed. A piece that is uniformly surprising is still detectable. The goal is alternating dense/simple passages (Principle 6).

**The Kobak 454 words are a checklist of what to avoid.** Words like "commendable," "meticulous," "pivotal," "intricate," "underscore," "delve," "tapestry," "nuanced," and "testament" are statistically overrepresented in post-ChatGPT academic text. Their presence is a near-certain AI fingerprint. They should be treated as banned vocabulary.

**Structural uniformity is detectable without NLP.** Proportional section lengths, consistent paragraph sizes, and balanced topic coverage are visible to human editors and pattern-matched by some detectors. Asymmetric structure (Principle 1) defeats this class of detection.

**Specificity defeats perplexity scoring.** Real names, real numbers, and real dates are low-frequency tokens in training corpora — they register as surprising to perplexity scorers. "The us-east-1 outage on December 7, 2021" is more perplexity-inflating than "a major cloud outage." This is why Principle 3 (Specificity) is both a humanization technique and an anti-detection technique simultaneously.

**The paraphrasing attack is not our model.** DIPPER-style paraphrasing produces grammatically correct but semantically thin prose. Our approach is to write human-authentically from the start, not to launder AI output. The research confirms that surface paraphrasing is brittle (detectors are catching up); building voice and asymmetry in at the generation stage is more durable.

**No detector is reliable enough to treat as ground truth.** Liang et al.'s non-native speaker finding means a 61% false positive rate on a large population of legitimate human writers. Any pipeline that uses detector output as a pass/fail gate will produce unacceptable false positive rates. Use detector scores as diagnostic feedback, not binary classification.
