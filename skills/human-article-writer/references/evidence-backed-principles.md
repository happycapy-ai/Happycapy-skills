# Evidence-Backed Writing Principles
## Extracted from NLP analysis of 1,109 human articles (pre-AI era)

```json
[
  {
    "id": 1,
    "principle": "Establish authority through specific examples, industry knowledge, and data citation as primary mechanisms — personal anecdotes are supplementary, not foundational",
    "evidence": "Top authority mechanisms are specific_example (66.2% of articles), industry_knowledge (64.6%), and data_citing (55.4%). Personal anecdotes appear as a rhetorical device in 55.4% of analyses but only 29.5% of all 1,109 articles contain any extended narrative. These figures measure different things: anecdotes appear briefly in many articles but rarely anchor the authority claim.",
    "category": "anti_fabrication",
    "implementation": "In the first 100 words, cite a named company, documented event, or published data point to establish domain credibility. Personal anecdotes may appear as illustration but must never be the primary credibility mechanism. If you cannot name a real example, use industry knowledge framing ('In enterprise SaaS procurement cycles...') rather than inventing a personal story.",
    "confidence": "high",
    "source": "model_a"
  },
  {
    "id": 2,
    "principle": "Never fabricate a personal story, lived experience, or first-person anecdote to manufacture credibility or relatability",
    "evidence": "70.5% of human articles establish full authority with zero narrative whatsoever. The dominant human credibility pattern is domain demonstration, not personal testimony. Fabricated anecdotes are structurally unnecessary in the majority of professional writing contexts.",
    "category": "anti_fabrication",
    "implementation": "Before writing any first-person story ('I remember when...', 'Years ago I...', 'I once worked with...'), ask: does this event actually exist in verifiable memory or record? If the answer is uncertain, replace with a documented third-party example. The test is not 'does this sound plausible' but 'did this happen.'",
    "confidence": "high",
    "source": "both"
  },
  {
    "id": 3,
    "principle": "Never fabricate statistics, percentages, or quantitative claims — cite real sources or omit the number",
    "evidence": "Data-citing appears in 55.4% of human articles as an authority mechanism, meaning readers and editors expect cited figures to be traceable. Invented statistics that cannot be verified undermine the entire credibility architecture that data-citation is meant to build.",
    "category": "anti_fabrication",
    "implementation": "Every numerical claim must have a traceable origin: a named study, a named organization's report, a named dataset, or a named publication. If you cannot identify the source, write 'research suggests' or 'evidence indicates' without a specific figure, rather than generating a plausible-sounding percentage. Never round a fabricated number to make it look researched (e.g., '67.3% of companies...').",
    "confidence": "high",
    "source": "critique"
  },
  {
    "id": 4,
    "principle": "Never fabricate named individuals, quotes, or attributed statements",
    "evidence": "Quote openings appear in only 0.1% of human articles — the near-total absence of opening quotes suggests human writers treat attributed speech as high-risk, high-verification content. Fabricated quotes from real people constitute defamation risk; fabricated quotes from invented people constitute deception.",
    "category": "anti_fabrication",
    "implementation": "Any quote must be traceable to a specific public record, interview transcript, published book, or documented speech. Do not paraphrase a real person's general position and present it as a direct quote. Do not invent a composite expert ('a senior engineer at a major tech firm told me...') unless clearly labeled as a composite. When in doubt, use indirect attribution: 'researchers at [Institution] have argued that...'",
    "confidence": "high",
    "source": "critique"
  },
  {
    "id": 5,
    "principle": "Never fabricate case studies, company outcomes, or organizational events",
    "evidence": "Specific examples appear in 66.2% of articles as the top authority mechanism. The power of this mechanism depends entirely on the example being real and verifiable. A fabricated case study that mimics the form of a real one is more dangerous than an obvious generalization because it appears authoritative.",
    "category": "anti_fabrication",
    "implementation": "When using a company or organization as an example, name it specifically and ensure the described event is documented in public record. If you cannot name the company (due to confidentiality), explicitly signal this: 'A mid-sized logistics firm (name withheld)...' rather than inventing a plausible company name. Never construct a narrative around a real company name and fictional events.",
    "confidence": "high",
    "source": "critique"
  },
  {
    "id": 6,
    "principle": "Never fabricate expert consensus or field-wide agreement that does not exist",
    "evidence": "Industry knowledge (64.6%) and data-citing (55.4%) are high-frequency authority mechanisms, creating strong incentive to overstate how settled or universal a finding is. Fabricated consensus ('experts universally agree...', 'the research is clear that...') is a form of epistemic fraud even when individual supporting studies exist.",
    "category": "anti_fabrication",
    "implementation": "Qualify the scope of any consensus claim precisely: 'Several large-scale RCTs suggest...' not 'science has proven...'; 'Many practitioners in this field favor...' not 'everyone in the industry knows...'. When genuine disagreement exists in a field, represent it. Adversative transitions (see principle 9) are the structural tool for doing this honestly.",
    "confidence": "high",
    "source": "critique"
  },
  {
    "id": 7,
    "principle": "Open with a declarative statement of position or fact as the default — not a question, quote, or temporal scene-setter",
    "evidence": "74.8% of 1,109 articles open with a declarative statement. First-person openings account for only 8.7%, questions 6.6%, short declaratives 5.0%, and data-point openings 4.9%. Quotes and temporal openings are nearly absent at 0.1% each.",
    "category": "opening",
    "implementation": "Default opening form: a direct declarative claim about the topic's current state or a key tension in the field (e.g., 'The market is mispricing this risk.' / 'Most onboarding programs solve the wrong problem.'). Reserve question openings for fewer than 1 in 10 pieces. Never open with a quote. Never open with 'In today's fast-paced world...' or any temporal scene-setter. Never open with a definition ('Webster's defines X as...').",
    "confidence": "high",
    "source": "model_a"
  },
  {
    "id": 8,
    "principle": "End with substantive analytical content that advances the argument — not a motivational summary or call to action",
    "evidence": "64.4% of articles end with a 'substantive_end' continuing the analytical argument to the final sentence. Only 24.2% use a short punchy close, 6.8% forward-looking, 2.4% a closing question, and 2.3% a call to action. The dominant human close is more analysis, not a wrap-up.",
    "category": "closing",
    "implementation": "The final paragraph should introduce or resolve the last analytical point, not restate what was already argued. Avoid closing formulas: 'In conclusion...', 'Ultimately...', 'As we have seen...'. If using a short punch close (appropriate ~24% of the time), make it a single crystallizing sentence, not a platitude. Never end with 'The future is [adjective].' or 'Now is the time to act.'",
    "confidence": "high",
    "source": "model_a"
  },
  {
    "id": 9,
    "principle": "Use adversative transitions as the dominant connective tissue of argument — human writing is structurally built on contrast and qualification, not accumulation",
    "evidence": "Adversative transitions (however, but, yet, although, despite) have the highest mean frequency at 17.214 per article, exceeding causal transitions (13.69 mean) and sequential transitions (7.54 mean). This is the highest per-article transition frequency of any category.",
    "category": "argument",
    "implementation": "Actively audit drafts for transition type. If a paragraph contains three or more additive transitions ('also', 'furthermore', 'additionally', 'in addition') with no adversative counterweight, revise to introduce a qualification, exception, or counter-consideration. The goal is not a fixed ratio but a structural habit of complicating claims rather than only stacking support for them.",
    "confidence": "high",
    "source": "model_a"
  },
  {
    "id": 10,
    "principle": "Write with high sentence-length burstiness: deliberately mix very short and very long sentences within the same piece",
    "evidence": "Human sentence-length standard deviation averages 16.26 words, which is 41.3% higher than AI-generated text (AI std = 9.224). Human mean sentence length is 25.3 words but ranges from p10=18.22 to p90=32.96, confirming deliberate variation rather than uniform cadence.",
    "category": "structure",
    "implementation": "After every 2-3 sentences averaging 30+ words, insert a sentence under 10 words. Never write 5 consecutive sentences of similar length. Target a within-article sentence-length standard deviation above 15 words. Note: the human mean std of 16.26 represents typical human performance; targeting above 15 is a realistic floor, not an aspirational ceiling.",
    "confidence": "high",
    "source": "model_a"
  },
  {
    "id": 11,
    "principle": "Use shorter, simpler words than formal or academic defaults — average word length should be under 5 characters",
    "evidence": "Human average word length is 4.742 characters, measurably shorter than AI-generated text defaults which trend toward polysyllabic vocabulary. Simpler word choice correlates with higher readability and lower detection as non-human writing.",
    "category": "vocabulary",
    "implementation": "Prefer the shorter synonym when two words mean the same thing: 'use' over 'utilize', 'show' over 'demonstrate', 'help' over 'facilitate', 'start' over 'commence', 'end' over 'terminate'. Reserve technical vocabulary for terms with no simpler equivalent. Audit any sentence where three or more words exceed 3 syllables — rewrite at least one.",
    "confidence": "high",
    "source": "model_a"
  },
  {
    "id": 12,
    "principle": "Maintain a consistent analytical voice throughout — do not shift register between formal argument and casual aside within the same paragraph",
    "evidence": "The dominance of declarative openings (74.8%), substantive endings (64.4%), and adversative transitions (17.214 mean) collectively describe a writing mode that is analytically continuous. Register shifts — sudden informality, sudden elevation — disrupt this continuity and signal non-human assembly of parts.",
    "category": "voice",
    "implementation": "Read each paragraph aloud. If the tone of one sentence sounds like a different writer than the sentence before it, revise for consistency. This does not mean monotone — sentence length variation (principle 10) provides rhythm — but the analytical stance (confident, specific, qualified) should be stable throughout.",
    "confidence": "medium",
    "source": "critique"
  },
  {
    "id": 13,
    "principle": "Demonstrate industry knowledge through precise domain vocabulary and process-level specificity, not generic field references",
    "evidence": "Industry knowledge appears in 64.6% of articles as a top authority mechanism. Generic references ('in the tech industry', 'in healthcare') do not constitute industry knowledge — they constitute category labeling. Authority comes from process-level specificity that only practitioners would know.",
    "category": "authority",
    "implementation": "Replace category labels with process specifics: not 'in software development' but 'in sprint retrospectives'; not 'in financial services' but 'in ISDA master agreement negotiations'. If you cannot supply the process-level detail, you do not have the industry knowledge to claim that authority mechanism — use a different one (specific example, data citation) instead.",
    "confidence": "high",
    "source": "critique"
  },
  {
    "id": 14,
    "principle": "Qualify claims with appropriate epistemic hedges — but use hedges that specify uncertainty rather than hedges that merely soften tone",
    "evidence": "The high frequency of adversative transitions (17.214 mean) and the dominance of analytical endings (64.4%) together indicate that human expert writing is comfortable with complexity and uncertainty. Vague softeners ('somewhat', 'rather', 'quite') are stylistic hedges; epistemic hedges ('under conditions X', 'in studies using Y methodology', 'among populations with Z characteristic') are analytical ones.",
    "category": "argument",
    "implementation": "Replace vague softeners with scope qualifiers. Instead of 'This approach is somewhat effective', write 'This approach shows consistent effects in B2B contexts but limited evidence in consumer settings.' The hedge should tell the reader what the claim does and does not cover, not merely signal that the writer is being cautious.",
    "confidence": "high",
    "source": "critique"
  },
  {
    "id": 15,
    "principle": "Use paragraph length variation analogously to sentence length variation — avoid uniform paragraph sizing",
    "evidence": "The high sentence-length standard deviation (16.26) in human writing reflects a broader structural principle of deliberate variation. Uniform paragraph length (every paragraph 4-6 sentences) is as much a signal of mechanical production as uniform sentence length.",
    "category": "structure",
    "implementation": "Allow single-sentence paragraphs for emphasis at key argumentative moments. Allow longer paragraphs (8-10 sentences) when developing a complex analytical point that should not be interrupted. The rhythm of paragraph breaks should follow argumentative logic, not a formatting template. Avoid the pattern of: intro paragraph, three equal body paragraphs, conclusion paragraph.",
    "confidence": "medium",
    "source": "critique"
  },
  {
    "id": 16,
    "principle": "Introduce the central tension or problem in the opening — not background, not context, not history",
    "evidence": "74.8% declarative openings and near-zero temporal openings (0.1%) indicate that human expert writers do not build up to their point through contextual scaffolding. The declarative opening is a tension-first structure: state what is wrong, contested, or underappreciated before explaining why.",
    "category": "opening",
    "implementation": "The first sentence should name a problem, contradiction, or underappreciated fact — not provide background. Background and context belong in the second or third paragraph, after the reader has a reason to want them. Test: if your opening paragraph could be deleted without losing the argument, it is context, not tension.",
    "confidence": "high",
    "source": "critique"
  },
  {
    "id": 17,
    "principle": "Use causal transitions to build explanatory chains — not just to list reasons",
    "evidence": "Causal transitions have a mean frequency of 13.69 per article, the second-highest category after adversative. This indicates that human expert writing is heavily invested in explaining mechanisms ('because', 'therefore', 'as a result', 'which means that'), not merely asserting conclusions.",
    "category": "argument",
    "implementation": "For every major claim, include at least one causal chain: the claim, the mechanism by which it operates, and the observable consequence. Avoid the pattern of assertion followed only by examples — examples illustrate but do not explain. The causal transition ('this happens because...', 'the result is that...') is the signal that explanation, not illustration, is occurring.",
    "confidence": "high",
    "source": "model_a"
  },
  {
    "id": 18,
    "principle": "Avoid opening with first-person framing — reserve 'I' openings for fewer than 1 in 10 pieces",
    "evidence": "First-person openings account for only 8.7% of articles despite personal anecdotes appearing in 55.4% of rhetorical analyses. This means writers use first-person voice within articles but rarely lead with it — the opening establishes the topic's importance, not the writer's relationship to it.",
    "category": "opening",
    "implementation": "If you find yourself drafting an opening like 