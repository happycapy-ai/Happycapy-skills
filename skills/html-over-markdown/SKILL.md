---
name: html-over-markdown
description: Generate rich, self-contained HTML documents instead of Markdown when output needs visual hierarchy, diagrams, or interactivity. Use for specs, implementation plans, side-by-side design comparisons, PR writeups and code explainers, research and status and incident reports, slide decks, SVG flowcharts, and throwaway editors like triage boards, feature-flag editors, and prompt tuners. Prefer this skill whenever the user asks for a report, plan, or explainer they'll actually want to read — even if they don't explicitly say "HTML".
---

# HTML Over Markdown

Produce a single self-contained `.html` file as the primary output format instead of Markdown.

## Why this exists

Markdown flattens spatial information — diffs, dependency graphs, side-by-side comparisons — into linear text. It has no color, no diagrams, no interaction, and people rarely read past ~100 lines. HTML trades a document the user would skim for one they would actually read.

Concrete wins over Markdown:
- **Information density**: tables, SVG, CSS, scripts, images — all in one file
- **Visual clarity**: tabs, collapsible sections, responsive layout, typographic hierarchy
- **Sharing**: one link, any browser, no special viewer
- **Two-way interaction**: sliders, toggles, editors, and a copy-back-to-prompt loop
- **Expressiveness**: no more ASCII diagrams or unicode color approximations

## When to use vs. skip

Use this skill when the user asks for:
- A spec, plan, proposal, brainstorm, or multi-option exploration
- A PR writeup, code review, or code/feature explainer
- A report — status, research, incident, weekly
- A side-by-side comparison of designs, approaches, or benchmarks
- A slide deck or visual walkthrough
- A throwaway interactive editor (triage board, feature flags, prompt tuner)
- Anything they'd "actually want to read" — even without the word HTML

Do NOT use this skill when:
- The deliverable is a real `.pdf` / `.docx` / `.pptx` / `.xlsx` file → use those skills
- The user wants a production web app (multi-file React/Vue/Next) → use `frontend-design` or `artifacts-builder`
- The spec is Git-tracked and teammates need clean diffs → keep Markdown
- The user wants a poster or visual artwork → use `canvas-design`
- The answer is a one-paragraph reply → just answer

If unsure, read `references/principles.md` → "What this skill is NOT for".

## Workflow

1. **Identify the scenario** from the 5 families in the table below.
2. **Read the matching section in `references/playbook.md`** for patterns and a prompt template.
3. **Pull reusable snippets from `references/snippets.md`** (grids, diffs, SVG, sliders, export buttons).
4. **Start from `assets/base-template.html`** — it has the default style already wired up. Copy it, then fill in.
5. **Write the result to `./outputs/<descriptive-kebab-case>.html`** and declare it in the `<attachments>` block as `<file type="static">outputs/<name>.html</file>`.
6. **Only if the HTML needs a real server** (e.g., `fetch`, complex event handlers that fail on `file://`), run `python -m http.server 8080 --directory outputs` and `/app/export-port.sh 8080`. For plain static pages, skip this.

## The 5 scenarios

| # | Scenario | Typical trigger | Signature patterns |
|---|---|---|---|
| 1 | **Spec, Planning & Exploration** | "Help me plan…", "explore approaches…", "compare options" | Side-by-side grid, labeled tradeoffs, mockups, data-flow SVG |
| 2 | **Code Review & PR** | "Explain this PR", "review this code", "help onboard a reviewer" | Annotated diff with margin notes, severity chips, module graph |
| 3 | **Design & Prototype** | "Design system", "component variants", "prototype an animation" | Variant matrix, color swatches, tunable sliders + Copy-as-CSS |
| 4 | **Report, Research & Explainer** | "Status report", "explain how X works", "incident writeup" | TL;DR, collapsible sections, tabbed samples, SVG diagrams, timeline |
| 5 | **Custom Editor** | "Let me reorder…", "tune this config", "edit this prompt with live preview" | Drag-drop or forms, live preview, **required**: Copy-as-{JSON,Prompt,Markdown} button |

Open `references/playbook.md` and jump to the matching scenario for full patterns, structural templates, and prompt seeds.

## The 5 principles (keep these in mind throughout)

1. **Self-contained**: one `.html`, all CSS/JS/SVG inline. CDN links are OK; build steps are not.
2. **SVG, never ASCII**: any diagram — flow, sequence, architecture, dependency — must be SVG.
3. **Spatial, not linear**: if you'd use a bullet list for it in Markdown, think again. Options go in a grid, diffs go inline with margins, dependencies go in a graph.
4. **Export-to-prompt**: any interactive control must have a button that writes something to the clipboard (JSON, Markdown, or a natural-language prompt) so the loop closes back into Claude Code.
5. **Readable at a glance**: responsive, quiet palette, obvious hierarchy. Optimize for "opens file → understands in 10 seconds".

Full rationale, reasoning, and the default style blueprint are in `references/principles.md`.

## Default style and output conventions

The default aesthetic is **Anthropic warm-editorial** — ivory `#FAF9F5` background, clay `#D97757` as the single accent, serif headings with mono uppercase eyebrows, 1.5px warm-gray borders. Full tokens, typography, and signature patterns live in **`references/design-language.md`** — read it before producing output.

The starter template in `assets/base-template.html` has the full palette wired up (`--ivory`, `--clay`, `--oat`, `--olive`, `--rust`, warm grays `--g100…--g700`, serif/sans/mono stacks, h1 with `<em>` in clay, callouts with clay stripe, mono chips).

Prefer adapting this template over writing new CSS from scratch. If the user references a design system of their own, mirror its tokens. If they ask explicitly for Anthropic brand styling, optionally combine with `brand-guidelines`.

File naming: `./outputs/<descriptive-kebab-case>.html`. Pick a name that would make sense six months later — `rate-limiter-explainer.html`, not `output.html`.

## A note on philosophy

The author of the underlying methodology deliberately warned against turning this into a rigid `/html` template skill, because the *knowing-when-and-what* matters more than the generation mechanics. This skill honors that: it teaches decision-making and patterns, bundles copy-paste snippets rather than generators, and trusts you to compose. Don't over-engineer — most of the time, the right move is to start from the base template, pick a scenario pattern, and write the thing.
