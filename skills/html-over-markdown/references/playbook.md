# Use-Case Playbook

Five scenarios, each with: when it fits, signature patterns, a structural template, and an example prompt seed you can offer back to the user or use to steer your own output.

Jump to the matching scenario:

- [1. Spec, Planning & Exploration](#1-spec-planning--exploration)
- [2. Code Review & PR Writeups](#2-code-review--pr-writeups)
- [3. Design & Prototyping](#3-design--prototyping)
- [4. Reports, Research & Explainers](#4-reports-research--explainers)
- [5. Custom Editors](#5-custom-editors)

---

## 1. Spec, Planning & Exploration

**When it fits**: the user is still choosing between approaches, hasn't committed to a direction, or wants to brainstorm several options before picking one. Also good for implementation plans once a direction is picked.

**Signature patterns**:
- **Option grid** — N cards in a CSS grid, each labeled with the tradeoff it's making ("heavier but safer", "simpler but locks us in later")
- **Mockup strip** — small inline SVG or styled divs showing the visual shape of each option
- **Data-flow SVG** — boxes and arrows for the flow being proposed
- **Inline code snippets** — the 2–3 key decisions rendered in `<pre><code>`
- **Collapsible "alternatives considered"** section at the bottom for the options that didn't make the cut

**Structural template**:
```
<header> Decision / Topic + 1-line framing </header>
<section class="grid"> [ option-card × N ] </section>
<section> Data flow <svg/> </section>
<section> Key decisions <pre><code/></pre> </section>
<details> Alternatives considered </details>
```

**Example prompt seed**:
> "Generate 6 distinctly different approaches — vary layout, tone, and density — and lay them out as a single HTML file in a grid so I can compare them side by side. Label each with the tradeoff it's making."

> "Create a thorough implementation plan as an HTML file. Include mockups, a data-flow diagram, and the 3 code snippets I'd want to review before approving."

**Anti-pattern**: writing a plan as a long vertical list of sections. If the user asked for "options", default to a grid. If they asked for a "plan", still use layout — TOC sidebar, tabbed code samples, a timeline.

---

## 2. Code Review & PR Writeups

**When it fits**: explaining a PR to a reviewer, onboarding someone to tricky code, writing up a postmortem on a code change, or generally making a diff legible.

**Signature patterns**:
- **Annotated diff** — two columns (before/after) with inline margin notes pointing at specific lines, and severity chips (`info`, `warn`, `error`)
- **Module graph** — small SVG showing which files changed and how they connect
- **"What to look at first" nav** — 3-item TOC at the top pointing reviewers at the critical sections
- **Callout boxes** — for backpressure cases, perf notes, security concerns

**Structural template**:
```
<header> PR: <title> — 1-line summary </header>
<nav> Look at these 3 things first </nav>
<section> Module graph <svg/> </section>
<section class="diff"> [ file blocks with inline margin notes ] </section>
<section> Edge cases & gotchas </section>
```

**Example prompt seed**:
> "Create an HTML artifact describing this PR. I'm not familiar with the streaming/backpressure logic, so focus on that. Render the actual diff with inline margin annotations, color-code findings by severity, and add a small module graph at the top."

**Anti-pattern**: embedding the diff as one giant `<pre>` block with no annotations — that's just a GitHub diff without the GitHub. The whole point is the margin notes and structure.

---

## 3. Design & Prototyping

**When it fits**: designing a component, exploring visual variants, tuning an animation, picking colors or easings, comparing layouts. Also good for sketching out a design system fragment.

**Signature patterns**:
- **Variant matrix** — grid of the same component in every state and prop combo (default/hover/disabled × sm/md/lg)
- **Live sliders** — controls that drive CSS custom properties in real time, so the user sees changes as they tune
- **Copy-as-CSS / Copy-as-props button** — export the values that felt right
- **Color/contrast chart** — if picking colors, auto-compute WCAG contrast ratios
- **Side-by-side mode** — show the component in light and dark, or next to a reference

**Structural template**:
```
<section class="preview"> [ live component driven by CSS vars ] </section>
<section class="controls"> [ sliders, color pickers, toggles ] </section>
<button class="primary" id="copy"> Copy as CSS </button>
<section class="variants"> [ matrix of variants ] </section>
```

**Example prompt seed**:
> "Prototype a new checkout button: when clicked, a play animation then turns purple quickly. Create an HTML file with sliders for duration, easing, and color, plus a copy button that gives me the final CSS."

> "Generate a variant matrix for this card component — default/hover/active × info/success/warning — as a single HTML file."

**Anti-pattern**: building a prototype with no controls, or with controls that don't affect the preview. The point of HTML over Markdown here is specifically the feedback loop of tweaking and seeing results.

---

## 4. Reports, Research & Explainers

**When it fits**: synthesizing information from multiple sources (codebase + git history + web); status updates for a team; incident postmortems; onboarding docs for a concept; feature explainers.

**Signature patterns**:
- **TL;DR at the top** — 3 bullets max, before any heavy content
- **Collapsible sections** — for depth on demand, so readers can skim the headers
- **Tabs** — for alternative code samples or perspectives on the same thing
- **SVG diagrams** — flow, architecture, sequence, timeline
- **Callout boxes** — gotchas, action items, critical dates
- **TOC / sidebar nav** — on wide screens, keep the structure visible

**Structural template**:
```
<header> <h1> + TL;DR bullets </header>
<aside class="toc"> [ section nav ] </aside>
<main>
  <section> How it works <svg/> </section>
  <section> Key code <tabs/> </section>
  <section> Timeline / status </section>
  <section class="gotchas"> Gotchas </section>
</main>
```

**Example prompt seed**:
> "I don't understand how our rate limiter actually works. Read the relevant code and produce a single HTML explainer: a diagram of the token-bucket flow, the 3–4 key code snippets annotated, and a 'gotchas' section at the bottom. Optimize for someone reading it once."

> "Prepare an in-depth research file in HTML on all the changes to prompt caching in this repo. Read the git history. Use SVG for diagrams."

**Anti-pattern**: the wall-of-text report with no diagrams. Any explainer longer than one screen needs a picture somewhere.

---

## 5. Custom Editors

**When it fits**: the user wants to do something text can't express well — reorder cards, tune a config, annotate a document, curate a dataset, pick values that are painful to type (colors, easing curves, crop regions, cron schedules). Always throwaway — one HTML file, purpose-built for this one piece of data.

**Signature patterns**:
- **Drag-drop columns or reorderable lists** (HTML5 drag API)
- **Form-based config** with inline dependency warnings ("you can't enable X while Y is off")
- **Live preview pane** showing the result of the current state
- **REQUIRED: Copy-as-{JSON | Markdown | Prompt} button** — this is non-negotiable. Without it the editor produces nothing.

**Structural template**:
```
<header> <tool name> — what you'll export </header>
<main class="editor"> [ columns / form / editor UI ] </main>
<aside class="preview"> [ live-rendered result ] </aside>
<footer>
  <button class="primary" id="copy-json"> Copy as JSON </button>
  <button id="copy-prompt"> Copy as Prompt </button>
</footer>
```

**Example prompt seeds**:
> "I need to reprioritize these 30 Linear tickets. Make an HTML file with each ticket as a draggable card across Now / Next / Later / Cut columns. Pre-sort by your best guess. Add a 'copy as markdown' button that exports the final ordering with a one-line rationale per bucket."

> "Here's our feature flag config. Build a form-based editor — group flags by area, show dependencies, warn me if I enable a flag whose prerequisite is off. Add a 'copy diff' button that gives me just the changed keys."

> "I'm tuning this system prompt. Make a side-by-side editor: editable prompt on the left with variable slots highlighted, three sample inputs on the right that re-render the filled template live. Character counter + copy button."

**Use this pattern for**:
- Reordering, triaging, or bucketing anything (tickets, test cases, feedback)
- Editing structured config (feature flags, env vars, JSON/YAML with constraints)
- Tuning prompts, templates, or copy with live preview
- Curating datasets — approve/reject rows, tag examples, export the selection
- Annotating a document, transcript, or diff and exporting the annotations
- Picking values that are painful to express in text: colors, easing curves, crop regions, cron schedules, regexes

**Anti-pattern** (repeated for emphasis): shipping an editor without an export button. The loop has to close.

---

## Cross-scenario notes

- **Mixing scenarios is normal.** A PR writeup often contains a report section (`how does this system work?`); an explainer might include a custom editor at the end. Pick the primary scenario by the dominant artifact and borrow patterns from others.
- **Don't over-stuff.** A spec doesn't need 6 SVG diagrams just because SVG is available. Use the sections the content needs and nothing more.
- **Offer prompt seeds.** If the user is ambiguous about what they want, quote the relevant seed back to them and ask if that shape matches their intent. It's faster than generating the wrong thing.
