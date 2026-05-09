# Design Principles

The five principles that keep HTML-over-Markdown outputs actually useful instead of just longer.

## 1. Self-contained

One `.html` file. All CSS, JavaScript, SVG, and data go inline. No `node_modules`, no build step, no separate `styles.css`.

Acceptable external dependencies (use sparingly, and only when the content genuinely needs them):
- Google Fonts — one family maximum
- Tailwind Play CDN (`https://cdn.tailwindcss.com`) — for dense UIs where utility classes save real code
- D3 / Chart.js from a CDN — only when a chart would be painful in hand-rolled SVG

Why: the user should be able to double-click the file and have it work in any browser, today and five years from now. External dependencies are a fragility tax — pay it only when the gain is obvious.

## 2. SVG, never ASCII

Never emit ASCII diagrams, box-drawing characters, or unicode color approximations.

If you catch yourself writing `│ ▼ └─` or `🟩🟥🟦` to "show" something, stop and write SVG. The base template includes an SVG pattern in `assets/base-template.html`; `references/snippets.md` has a flowchart starter.

Why: ASCII diagrams exist precisely *because* Markdown can't render real ones. Once you have HTML, there's no reason to keep the workaround.

## 3. Spatial, not linear

A list in Markdown is often a grid, graph, or timeline in HTML. Before writing bullets, ask: *does this information have spatial structure I'm flattening?*

| Markdown habit | HTML alternative |
|---|---|
| Numbered list of options | CSS grid, one card per option with labeled tradeoffs |
| "Before" / "after" code blocks | Two-column diff with inline annotations |
| "Here are the modules" list | SVG box-and-arrow graph |
| Timeline described in prose | Horizontal timeline with markers |
| Status bullets | Chips colored by state |
| "Pros vs cons" list | Two-column table or side-by-side cards |
| Dependency tree as nested bullets | Tree diagram or indented card stack |

Why: spatial layout is the single biggest reason HTML beats Markdown for dense information. If the output reads top-to-bottom like a Markdown file did, you've wasted the format.

## 4. Export-to-prompt loop

Any interactive HTML — slider, drag-drop board, form editor, prompt tuner — is half-finished without an export button. The loop must close:

```
User tweaks in HTML → clicks Copy → pastes back into Claude Code → Claude acts on it
```

Minimum viable export: a button that writes a string to the clipboard. Choose the format based on what the user will do next:
- **JSON** — when the state is structured and another tool will parse it
- **Markdown** — when the state is a list/table the user will paste into a doc or PR
- **Natural-language prompt** — when the state will feed the next Claude turn

See `references/snippets.md` → "Copy-as-prompt button". Ship every interactive HTML with at least one.

Why: shipping an editor with no export is worse than not shipping it — the user fiddled, then has nothing to take away.

## 5. Readable at a glance

Optimize for "opens file → understands in 10 seconds". That means:

- **Hierarchy**: one `<h1>`, clear `<h2>/<h3>`, generous spacing between sections
- **Palette**: warm neutrals + one accent (clay). Reserve olive and rust for semantic states (success, error) — not decoration. See `design-language.md`.
- **Width**: max 860px for prose reports; up to 1360px for multi-column exploration grids
- **Mobile**: content must reflow; use flex/grid, avoid fixed pixel widths
- **Chrome**: minimal. A status report doesn't need a landing-page hero

Why: density without clarity is just noise. The value of HTML comes from making information *easier* to absorb than Markdown, not harder.

## Output conventions

- **Filename**: `./outputs/<descriptive-kebab-case>.html`. Pick a name that would make sense six months later (`rate-limiter-explainer.html`, not `output.html`).
- **Attachments declaration**: always include `<file type="static">outputs/<name>.html</file>` in the `<attachments>` block at the end of the reply.
- **Local server** (only when needed): if the page uses `fetch`, loads JSON, or has interactivity that fails on `file://`, run `python -m http.server 8080 --directory outputs` and `/app/export-port.sh 8080`. For plain static pages, skip the server — `<file type="static">` handles preview on its own.

## What this skill is NOT for

A quick checklist before you commit:

| Situation | Correct skill |
|---|---|
| User wants a real `.pdf` / `.docx` / `.pptx` / `.xlsx` file | `pdf` / `docx` / `pptx` / `xlsx` |
| User wants a production web app (multi-file, needs routing/state/build) | `frontend-design`, `artifacts-builder` |
| User wants a React Native / Swift / native artifact | `frontend-design` as sketch, then port |
| User wants a poster, artwork, or purely visual piece | `canvas-design` |
| Team spec that will live in Git and needs clean text diffs | Plain Markdown |
| One-paragraph answer to a direct question | Just answer inline |
| Instagram carousel / marketing asset | `world-class-carousel` |
| Video, email template, slideshow `.pptx` | their dedicated skills |

The right failure mode here is "skipped this skill even though it might have fit" — not "used it for a task that belonged somewhere else". When in doubt and the output is long-form content the user will *read*, lean in. When the deliverable is a concrete file format with its own skill, defer.

## Style blueprint

The default style is **Anthropic warm-editorial** — a deliberate aesthetic, not a neutral fallback. It mirrors the author's own case library at `thariqs.github.io/html-effectiveness/` and the surfaces of Claude's product docs. Full tokens, typography, signature patterns, and anti-patterns live in **`references/design-language.md`** — read that file before deviating.

Quick summary (see `design-language.md` for the full story):

- **Background:** ivory `#FAF9F5` — never pure white
- **Accent:** clay `#D97757` — one accent only, never introduce blues/purples
- **Semantic:** olive `#788C5D` (ok), rust `#B04A3F` (danger), oat `#E3DACC` (warm fill)
- **Text:** slate `#141413` on warm grays `#F0EEE6 → #D1CFC5 → #87867F`
- **Type:** serif (Georgia) for `h1/h2` at weight 500 with tight tracking; sans (system-ui) body; mono (SF Mono) for uppercase letter-spaced eyebrows and chips
- **Signature move:** `<h1>Title with <em>italic accent</em></h1>` in clay
- **Borders:** `1.5px solid #D1CFC5`, panel radius `12px`, row radius `8px`

When to deviate:
- User references a design system of their own → mirror their tokens.
- User asks for an explicit brand (Apple, Stripe, Linear) → follow their brief.
- User wants a pure dashboard where color coding matters more than editorial warmth → keep ivory bg, tone down the serif chrome, lean into data ink.
- User pairs this skill with `brand-guidelines` → defer to those tokens.
