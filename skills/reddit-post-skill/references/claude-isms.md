# Claude-Specific Vocabulary Database

A comprehensive database of vocabulary, phrases, and patterns that are statistically overrepresented in Claude outputs. Use this to detect and humanize AI-generated text.

---

## How Detection Works

AI detection systems measure several statistical properties:

1. **Lexical Fingerprints:** Every LLM has vocabulary preferences—words it uses 2-10x more frequently than humans
2. **Perplexity Patterns:** AI text has unnaturally consistent complexity; humans vary wildly
3. **Burstiness:** Humans write in bursts (short-short-LONG-short); AI tends toward regularity
4. **Semantic Coherence:** AI text is often too coherent—real posts have tangents

This database addresses #1: lexical fingerprints.

---

## CATEGORY 1: Formal Transition Words

Claude over-indexes on formal connectors. Replace with casual alternatives or delete entirely.

| Claude Says | Human Alternatives | Notes |
|-------------|-------------------|-------|
| however | but, though | or just start new sentence |
| therefore | so | or delete entirely |
| furthermore | also, and, plus | or just continue |
| nevertheless | still, but, even so | |
| consequently | so | |
| additionally | also, and, plus, oh and | |
| moreover | also, and | rarely used casually |
| thus | so | or delete |
| hence | so | very rare in casual |
| accordingly | so | delete in casual |
| subsequently | then, after, next | |
| nonetheless | still, but | |
| conversely | but, on the other hand | |
| alternatively | or | |
| specifically | like, basically | or delete |
| particularly | especially | |
| notably | especially | |
| indeed | yeah, totally | or delete |
| certainly | sure, yeah, definitely | |
| undoubtedly | definitely, for sure | |

---

## CATEGORY 2: Filler Hedges (Overly Polite)

Claude hedges excessively. Humans are more direct.

| Claude Says | Human Alternatives | Notes |
|-------------|-------------------|-------|
| I would say that | [just say it] | delete the hedge |
| I think it's worth noting | [just note it] | |
| It's important to mention | [just mention it] | |
| I'd like to point out | [just point it out] | |
| I should mention | [just mention it] | |
| I'd be happy to | [just do it] | never announce willingness |
| Allow me to | [just do it] | |
| Let me explain | [just explain] | |
| I want to share | [just share] | |
| I'd like to share | [just share] | |
| If I may | [just say it] | |
| I believe that | I think, maybe | or delete |
| In my opinion | I think, imo | or just state it |
| From my perspective | to me, I think | |
| It seems to me | I think, feels like | |
| I feel compelled to | [just do it] | |
| I must admit | honestly, ngl | |
| I have to say | honestly, tbh | |

---

## CATEGORY 3: Formal Verb Choices

Claude uses formal verbs. Humans use simpler ones.

| Claude Says | Human Alternatives | Notes |
|-------------|-------------------|-------|
| utilize | use | always |
| implement | do, try, use, set up | |
| facilitate | help, make easier | |
| leverage | use | always |
| navigate | deal with, handle, figure out | |
| demonstrate | show | |
| indicate | show, mean, suggest | |
| possess | have | |
| require | need | |
| obtain | get | |
| acquire | get, pick up | |
| commence | start, begin | |
| terminate | end, stop | |
| endeavor | try | |
| ascertain | find out, figure out | |
| comprehend | understand, get | |
| inquire | ask | |
| purchase | buy | |
| assist | help | |
| reside | live | |
| consume | eat, use | |
| observe | see, notice, watch | |
| accomplish | do, get done, finish | |
| encounter | run into, find, hit | |
| establish | set up, start, make | |
| maintain | keep, keep up | |
| determine | figure out, decide | |
| identify | find, spot | |
| ensure | make sure | |
| provide | give | |
| receive | get | |
| modify | change | |
| eliminate | get rid of, cut, remove | |
| enhance | improve, make better | |

---

## CATEGORY 4: Formal Noun Choices

| Claude Says | Human Alternatives | Notes |
|-------------|-------------------|-------|
| individual | person, someone | |
| individuals | people | |
| methodology | method, way, approach | |
| framework | system, setup, approach | |
| endeavor | try, effort, thing | |
| component | part, piece | |
| implementation | setup, way of doing it | |
| perspective | view, take, way of seeing | |
| assistance | help | |
| residence | place, home | |
| functionality | feature, what it does | |
| correspondence | emails, messages | |
| documentation | docs, paperwork | |
| modification | change | |
| recommendation | suggestion, advice | |
| optimization | improvement, making it better | |
| utilization | use | |
| prioritization | priorities, what matters most | |

---

## CATEGORY 5: Prepositional Phrases (Over-Formal)

| Claude Says | Human Alternatives | Notes |
|-------------|-------------------|-------|
| in order to | to | always |
| due to the fact that | because | always |
| in terms of | with, for, about, re: | |
| with regard to | about, on | |
| in relation to | about, with | |
| for the purpose of | to, for | |
| at this point in time | now, right now | |
| at the present time | now | |
| in the event that | if | always |
| in spite of the fact that | even though | |
| prior to | before | always |
| subsequent to | after | always |
| in conjunction with | with | |
| in the context of | in, with | |
| on the basis of | based on, from | |
| in light of | given, because of | |
| with respect to | about, on | |
| for the duration of | during, for | |
| in close proximity to | near | |
| in the majority of cases | usually, mostly | |
| in a manner that | so that, in a way that | |
| the fact that | that | always delete "the fact" |

---

## CATEGORY 6: Claude Power Words (Overused)

These words appear 3-10x more frequently in Claude outputs than in human Reddit posts.

| Word | Frequency | Human Alternatives |
|------|-----------|-------------------|
| genuinely | Very High | actually, really, for real, honestly |
| straightforward | Very High | simple, easy, obvious, not that hard |
| comprehensive | Very High | full, complete, everything, the whole thing |
| absolutely | High | yeah, definitely, for sure, 100% |
| essential | High | important, key, needed |
| fundamental | High | basic, core, main |
| significant | High | big, major, a lot |
| effectively | High | basically, really | 
| ultimately | High | in the end, eventually |
| particularly | High | especially, really |
| certainly | High | sure, yeah, of course |
| incredibly | High | really, super, so |
| essentially | High | basically | 
| substantial | High | big, major, a lot |
| valuable | High | useful, helpful, good |
| crucial | High | important, key |
| optimal | High | best |
| ideal | Medium | best, perfect |
| seamless | Medium | smooth, easy |
| robust | Medium | solid, strong |
| nuanced | Medium | complicated, detailed |
| holistic | Medium | whole, complete |
| streamlined | Medium | simpler, easier |
| intuitive | Medium | easy, obvious |
| pivotal | Medium | key, important |
| paramount | Medium | most important |

---

## CATEGORY 7: Claude Phrase Patterns

Full phrases that are Claude signatures.

### "Happy To" Patterns (Delete All)
- "I'd be happy to help with..."
- "I'm happy to explain..."
- "I'd be glad to assist..."
- "I'm pleased to..."

**Fix:** Just do the thing. Never announce willingness.

### "Let Me" Patterns (Delete All)
- "Let me explain..."
- "Let me share..."
- "Let me walk you through..."
- "Let me break this down..."

**Fix:** Just explain/share/break it down. No announcements.

### "It's Important To" Patterns
- "It's important to note that..."
- "It's worth mentioning that..."
- "It's crucial to understand that..."
- "It's essential to recognize that..."

**Fix:** Just state the thing. Or: "honestly" / "btw" / "oh and"

### "This Is" Generalizations
- "This is a common problem..."
- "This is understandable..."
- "This is a great question..."

**Fix:** Delete or be specific: "I had this same thing" / "yeah" / [just answer]

### Journey/Process Language
- "on this journey"
- "throughout this process"
- "along the way"
- "as you move forward"

**Fix:** Delete entirely. Real people don't use "journey" for mundane things.

---

## CATEGORY 8: Opening Patterns (Instant Flags)

These openings immediately signal AI:

| Opening | Why It Fails | Fix |
|---------|--------------|-----|
| "I understand..." | Too empathetic upfront | Jump into the story |
| "Great question!" | Sycophantic | [delete] |
| "That's a really good point..." | Sycophantic | [delete] |
| "I appreciate you sharing..." | Overly formal | [delete] |
| "Thank you for..." | Wrong register | [delete] |
| "I can certainly help with..." | Announcing help | [just help] |
| "Absolutely! Here's..." | Too eager | Casual start |
| "Of course!" | Too eager | [delete] |

### Better Openings (Human Style)
- Just start with the topic
- "ok so basically..."
- "honestly..."
- "ngl..."
- "so here's the thing..."
- "yeah so..."
- Story/anecdote first

---

## CATEGORY 9: Closing Patterns (Instant Flags)

| Closing | Why It Fails | Fix |
|---------|--------------|-----|
| "I hope this helps!" | Too formal/eager | [delete] or "hope that makes sense" |
| "Feel free to ask..." | Customer service voice | [delete] |
| "Let me know if..." | Customer service voice | [delete] or "lmk" |
| "Best of luck!" | Too formal | "good luck" or [delete] |
| "Wishing you all the best" | Way too formal | [delete] |
| "Don't hesitate to reach out" | Corporate speak | [delete] |
| Question after wisdom dump | Too formulaic | End on uncertainty |

### Better Closings (Human Style)
- Trail off with uncertainty: "idk if that helps..."
- Self-doubt: "but yeah that's just my experience"
- Casual: "anyway"
- Just stop writing
- "hope this makes sense lol"

---

## CATEGORY 10: Structural Patterns

### Sentence Length
**AI Pattern:** Consistent 15-25 words per sentence
**Human Pattern:** Wild variance (3 words to 40 words)

**Test:** Calculate standard deviation of sentence lengths. Should be > 8 words.

### Paragraph Structure  
**AI Pattern:** 3-4 sentences per paragraph, consistently
**Human Pattern:** 1 sentence, then 5 sentences, then 2 sentences

**Test:** No two consecutive paragraphs should be the same length.

### List Usage
**AI Pattern:** Numbered lists, parallel structure, 3-5 items
**Human Pattern:** Bullet points are rare; when used, inconsistent formatting

**Test:** If you have a list, break it. Vary bullet styles. Don't align.

### Transitions Between Paragraphs
**AI Pattern:** Every paragraph logically connects to the previous
**Human Pattern:** Topic jumps, "oh and I forgot to mention," tangents

**Test:** At least one paragraph should feel like a non-sequitur.

---

## CATEGORY 11: Emotional Language Flags

| Claude Emotion | Human Equivalent |
|----------------|------------------|
| "I completely understand" | "yeah I've been there" or "ugh that sucks" |
| "That must be frustrating" | "that's so annoying" or "wtf" |
| "I can see why you'd feel that way" | "same honestly" |
| "That sounds challenging" | "damn that's rough" |
| "I appreciate your patience" | [delete] |
| "Thank you for your understanding" | [delete] |

---

## CATEGORY 12: Reddit-Specific Humanizers

Add these naturally to pass as human:

### Casual Fillers (Need 3+ per post)
- honestly
- tbh
- like
- idk
- ngl
- or something
- I guess
- maybe
- kinda
- sorta
- basically
- pretty much
- I mean

### Reddit Speech Patterns
- "Edit: ..." (to add something)
- "lol" / "lmao" (for mild humor)
- "idk if this helps but..."
- "might be wrong but..."
- "not sure if this is the right sub but..."

### Uncertainty Markers
- "I think?"
- "maybe?"
- Trailing "..."
- "or maybe not idk"
- "but who knows"

### Self-Deprecation
- "I'm probably doing this wrong but..."
- "feel free to tell me I'm an idiot"
- "this is probably obvious but..."

---

## USAGE INSTRUCTIONS

### During Detection Scan (Phase 4)

1. **Run vocabulary check:** Search for every item in Categories 1-6
2. **Flag and replace:** Use human alternatives
3. **Check phrase patterns:** Search for Category 7-9 patterns
4. **Delete instead of replacing** when in doubt
5. **Add humanizers** from Category 12 if count < 3

### Statistical Targets

| Metric | AI Typical | Human Target |
|--------|------------|--------------|
| Sentence length std dev | 4-6 words | > 8 words |
| Casual fillers per 100 words | 0-1 | 2-4 |
| Claude power words per 100 words | 3-5 | 0-1 |
| Perfect grammar sentences | 95%+ | 80-90% |
| Paragraph length variance | Low | High |

---

## EXPANDING THIS DATABASE

When you notice new Claude-isms:

1. Check frequency in AI vs human text
2. Find 2-3 human alternatives
3. Add to appropriate category
4. Test replacement in context

This is a living document.
