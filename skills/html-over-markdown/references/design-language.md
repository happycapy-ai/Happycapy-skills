# Design language — Anthropic warm-editorial

The default visual style for every document produced by this skill. This is **not**
a generic Tailwind/shadcn look — it is deliberately warm, print-editorial, close to
Anthropic's own documentation surfaces. If the user asks for a different aesthetic,
switch freely. Otherwise, start here.

Source of truth: the case library at `thariqs.github.io/html-effectiveness/` — every
example in that library uses the tokens below.

---

## Color tokens

Copy this block into every document's `:root`.

```css
:root {
  --ivory:  #FAF9F5;   /* page background — NEVER pure white */
  --paper:  #FFFFFF;   /* cards and panels sit on ivory */
  --slate:  #141413;   /* primary text */

  --clay:   #D97757;   /* terracotta — the single accent color */
  --clay-d: #B85C3E;   /* hover / pressed */

  --oat:    #E3DACC;   /* warm fill, callout bg, timeline band */
  --olive:  #788C5D;   /* success / positive signal */
  --rust:   #B04A3F;   /* danger / error / critical */

  --g100:   #F0EEE6;   /* warmest gray — table header, code inline bg */
  --g200:   #E6E3DA;
  --g300:   #D1CFC5;   /* default border color */
  --g500:   #87867F;   /* muted text, captions, eyebrow */
  --g700:   #3D3D3A;   /* body secondary */
}
```

Use **one** accent. Clay is the accent. Olive and rust are reserved for
semantic states (ok / danger). Never introduce blues, purples, or teals.

---

## Typography

```css
--serif: ui-serif, Georgia, "Times New Roman", Times, serif;
--sans:  system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
--mono:  ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace;
```

| Element        | Family | Weight | Size                          | Notes |
|----------------|--------|--------|-------------------------------|-------|
| `h1`           | serif  | 500    | `clamp(32px, 4.6vw, 44px)`    | `letter-spacing: -0.015em`, `line-height: 1.1`. Hero pages may go to 62px. |
| `h1 em`        | serif  | 500    | same                          | `font-style: italic; color: var(--clay)` — the signature title accent. |
| `h2`           | serif  | 500    | 24px                          | `letter-spacing: -0.01em`. Often followed by `<hr class="rule">`. |
| `h3`           | sans   | 600    | 15px                          | Used inside cards and sections. |
| Body           | sans   | 400    | 15px / 1.6                    | Color `var(--slate)` or `var(--g700)`. |
| Subtitle       | sans   | 400    | 16px                          | `color: var(--g500)`. |
| Eyebrow        | mono   | 400    | 12px                          | `letter-spacing: 0.12em; text-transform: uppercase; color: var(--g500)`. |
| Chip / tag     | mono   | 400    | 11px                          | `letter-spacing: 0.04em`. |
| Caption        | sans   | 400    | 12px                          | `color: var(--g500)`. |
| Code inline    | mono   | 400    | 0.9em                         | bg `var(--g100)`, border `var(--g300)`. |
| Code block     | mono   | 400    | 12.5–13px / 1.65              | bg `var(--slate)`, text `#E8E6DE`. |

The serif-for-headings + mono-for-eyebrows contrast is the strongest signal of
the style. Skip it and the document loses its heritage.

---

## Borders, radii, spacing

- **Border:** `1.5px solid var(--g300)` — never 1px, never 2px.
- **Panel radius:** `12px`. **Row / chip radius:** `8px`. **Pill radius:** `999px`.
- **Page padding:** `56px 24px 120px` (desktop) → `32px 18px 96px` (≤720px).
- **Max content width:** `860px` for reports/docs, up to `1360px` for
  multi-column exploration grids.
- **Section spacing:** `margin-bottom: 52px` between major sections.
- **Card padding:** `20px 22px` typical, `24px 28px` for hero callouts.

---

## Signature patterns

**Eyebrow + serif title**

```html
<div class="eyebrow">Exploration · Birchline web client</div>
<h1>Three ways to implement <em>debounced search</em></h1>
<p class="subtitle">One-line framing of why this doc exists.</p>
```

**Callout with clay stripe**

```html
<div class="callout">
  <strong>TL;DR.</strong> One sentence of the point.
</div>
```

Variants: `.callout.warn` (clay-d), `.callout.err` (rust), `.callout.ok` (olive).

**Stat card with warn stripe**

```html
<div class="stat-card warn">
  <div class="stat-num">1</div>
  <div class="stat-label">Incidents</div>
  <div class="stat-delta">SEV-2 · 47m</div>
</div>
```

Stat numbers are serif, weight 500, 44px, tight line-height.

**Risk dot in table rows**

Solid 9px circle, colors `olive / clay / rust` for low / med / high. Always
paired with a short label to the right.

**Hand-drawn feel (use sparingly)**

Occasionally rotate a card `transform: rotate(-2.5deg)` for prototypes or
sketch-mode layouts. Never rotate text blocks the user needs to read linearly.

---

## Decorations that DO belong here

- Monospace uppercase eyebrows and "auto-generated" pills.
- Serif italics in the accent color inside a heading.
- Warm gray gridlines in SVG charts (`#F0EEE6` for minor, `#D1CFC5` for axis).
- Dotted underlines on links on hover.
- Oat-colored warm panels for carryover / appendix sections.

## Decorations that DO NOT belong

- Gradients, shadows, glassmorphism.
- Pure `#FFFFFF` backgrounds behind body text.
- Cold-gray Tailwind palettes (`slate-*`, `zinc-*`, `neutral-*`, `gray-*` cool tones).
- System-only sans-serif for headings.
- Multiple accent colors in a single document.
- Emoji as decoration (user hasn't asked for them).

---

## When to deviate

- User explicitly asks for another brand (Apple, Stripe, Linear, etc.) — follow the brief.
- Doc is primarily a chart/dashboard where strong color coding wins over editorial warmth — tone down the serif and chrome, keep the ivory background.
- Dark mode requested — invert to `--slate` body, `#1E1C19` panels, keep clay accent.
