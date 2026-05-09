# Snippet Library

Copy, paste, adapt. These are starters — not rigid templates. If a snippet doesn't fit cleanly, deviate; don't force it.

Table of contents:

- [Base style block](#base-style-block) — the CSS variables and resets everything else builds on
- [Option grid / side-by-side cards](#option-grid--side-by-side-cards)
- [Annotated diff](#annotated-diff)
- [SVG flowchart starter](#svg-flowchart-starter)
- [SVG timeline](#svg-timeline)
- [Collapsible sections](#collapsible-sections)
- [Tabs](#tabs)
- [Slider driving a CSS variable](#slider-driving-a-css-variable)
- [Copy-as-prompt button (mandatory for editors)](#copy-as-prompt-button-mandatory-for-editors)
- [Draggable cards across columns](#draggable-cards-across-columns)
- [Chips and callouts](#chips-and-callouts)

---

## Base style block

This is already baked into `assets/base-template.html`. The full token set and rationale live in `references/design-language.md` — always read that before deviating. Reproduced here compactly so you can cherry-pick into a different shell.

```html
<style>
  :root {
    --ivory:#FAF9F5; --paper:#FFF; --slate:#141413;
    --clay:#D97757; --clay-d:#B85C3E; --oat:#E3DACC;
    --olive:#788C5D; --rust:#B04A3F;
    --g100:#F0EEE6; --g200:#E6E3DA; --g300:#D1CFC5;
    --g500:#87867F; --g700:#3D3D3A;

    --serif: ui-serif, Georgia, "Times New Roman", Times, serif;
    --sans:  system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    --mono:  ui-monospace, "SF Mono", Menlo, Monaco, monospace;
  }
  *{box-sizing:border-box}
  body{margin:0;padding:56px 24px 120px;background:var(--ivory);color:var(--slate);
       font:15px/1.6 var(--sans);-webkit-font-smoothing:antialiased}
  .page{max-width:860px;margin:0 auto}
  .eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.12em;
           text-transform:uppercase;color:var(--g500);margin-bottom:12px}
  h1{font-family:var(--serif);font-weight:500;font-size:clamp(32px,4.6vw,44px);
     line-height:1.1;letter-spacing:-.015em;margin:0 0 14px;color:var(--slate)}
  h1 em{font-style:italic;color:var(--clay)}            /* signature title accent */
  .subtitle{color:var(--g500);font-size:16px;margin:0 0 40px;max-width:60ch}
  h2{font-family:var(--serif);font-weight:500;font-size:24px;letter-spacing:-.01em;margin:0 0 6px}
  h2 + hr.rule{border:none;border-top:1px solid var(--g300);margin:0 0 22px}
  h3{font-weight:600;font-size:15px;margin:1.2rem 0 .4rem}
  a{color:var(--clay);text-decoration:none;border-bottom:1px dotted transparent}
  a:hover{border-bottom-color:var(--clay)}
  code,pre{font-family:var(--mono);font-size:.9em}
  :not(pre)>code{background:var(--g100);border:1px solid var(--g300);border-radius:4px;padding:.05rem .3rem}
  pre{background:var(--slate);color:#E8E6DE;border-radius:12px;padding:18px 20px;overflow:auto;line-height:1.65}
  button{font:inherit;cursor:pointer;padding:.5rem .95rem;border-radius:8px;
         border:1.5px solid var(--g300);background:var(--paper);color:var(--slate)}
  button:hover{background:var(--g100)}
  button.primary{background:var(--clay);color:var(--paper);border-color:var(--clay)}
  button.primary:hover{background:var(--clay-d);border-color:var(--clay-d)}
  table{width:100%;border-collapse:separate;border-spacing:0;background:var(--paper);
        border:1.5px solid var(--g300);border-radius:12px;overflow:hidden}
  thead th{text-align:left;font-size:11px;font-weight:600;text-transform:uppercase;
           letter-spacing:.06em;color:var(--g500);background:var(--g100);
           padding:12px 16px;border-bottom:1px solid var(--g300)}
  tbody td{padding:13px 16px;border-bottom:1px solid var(--g100);font-size:14px}
  svg{max-width:100%;height:auto}
  @media(max-width:720px){body{padding:32px 18px 96px}}
</style>
```

Key differences from a typical Tailwind/shadcn starter: **ivory (not white) background**, **serif h1 + mono uppercase eyebrow**, **1.5px warm-gray borders**, **single clay accent** (never blue).

---

## Option grid / side-by-side cards

Use for spec explorations, design variant comparisons, anything where the user is choosing between N options.

```html
<section class="grid">
  <article class="card">
    <h3>Option A <span class="chip ok">recommended</span></h3>
    <p class="muted">One-sentence tradeoff: safer but slower to ship.</p>
    <pre><code>// key code decision</code></pre>
    <ul><li>Pro: …</li><li>Con: …</li></ul>
  </article>
  <!-- repeat -->
</section>
<style>
  .grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));margin:1rem 0}
  .card{border:1.5px solid var(--g300);border-radius:12px;padding:20px 22px;background:var(--paper)}
  .muted{color:var(--g500)}
</style>
```

---

## Annotated diff

Two-column before/after with margin notes. The notes are the whole point.

```html
<div class="diff">
  <div class="pair">
    <pre class="before"><code>def charge(user, amount):
    if not user.active:
        return False
    stripe.charge(user.id, amount)
    return True</code></pre>
    <pre class="after"><code>def charge(user, amount):
    if not user.active:
        raise InactiveUserError(user.id)
    result = stripe.charge(user.id, amount)
    return result.ok</code></pre>
  </div>
  <aside class="note">
    <span class="chip warn">behavior change</span>
    Returning <code>False</code> silently was masking failures in prod.
    New code raises so callers see it.
  </aside>
</div>
<style>
  .diff{display:grid;grid-template-columns:1fr 20rem;gap:1rem;margin:1rem 0;align-items:start}
  .diff .pair{display:grid;grid-template-columns:1fr 1fr;gap:.5rem}
  .diff .before code{color:var(--rust)}
  .diff .after code{color:var(--olive)}
  .diff .note{font-size:.9rem;color:var(--g500);border-left:3px solid var(--clay);padding:.4rem .8rem;background:var(--g100);border-radius:0 6px 6px 0}
  @media(max-width:720px){.diff{grid-template-columns:1fr}.diff .pair{grid-template-columns:1fr}}
</style>
```

---

## SVG flowchart starter

The minimum viable SVG flow — three nodes, two arrows, marker-based arrowheads.

```html
<svg viewBox="0 0 620 200" role="img" aria-label="Flow diagram" style="width:100%;max-width:640px">
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#3D3D3A"/>
    </marker>
  </defs>
  <g font-family="system-ui,sans-serif" font-size="13" fill="#141413">
    <rect x="20"  y="70" width="140" height="60" rx="8" fill="#F0EEE6" stroke="#D1CFC5" stroke-width="1.5"/>
    <text x="90"  y="105" text-anchor="middle">Input</text>

    <rect x="240" y="70" width="140" height="60" rx="8" fill="#E3DACC" stroke="#D97757" stroke-width="1.5"/>
    <text x="310" y="105" text-anchor="middle">Process</text>

    <rect x="460" y="70" width="140" height="60" rx="8" fill="#F0EEE6" stroke="#788C5D" stroke-width="1.5"/>
    <text x="530" y="105" text-anchor="middle">Output</text>

    <line x1="160" y1="100" x2="240" y2="100" stroke="#3D3D3A" stroke-width="1.5" marker-end="url(#arr)"/>
    <line x1="380" y1="100" x2="460" y2="100" stroke="#3D3D3A" stroke-width="1.5" marker-end="url(#arr)"/>
  </g>
</svg>
```

For more complex diagrams (branches, loops, swimlanes), extend the same pattern — keep nodes as `<rect>+<text>` groups, lines as `<line>` or `<path>` with the shared `url(#arr)` marker.

---

## SVG timeline

Horizontal timeline with markers for events. Good for incident reports and status updates.

```html
<svg viewBox="0 0 700 120" role="img" aria-label="Timeline" style="width:100%">
  <g font-family="system-ui,sans-serif" font-size="12">
    <line x1="40" y1="60" x2="660" y2="60" stroke="#D1CFC5" stroke-width="2"/>
    <!-- event 1: clay = incident start -->
    <circle cx="90"  cy="60" r="6" fill="#D97757"/>
    <text x="90"  y="40" text-anchor="middle" fill="#141413">09:14</text>
    <text x="90"  y="90" text-anchor="middle" fill="#87867F">Alert fired</text>
    <!-- event 2: clay-dark = mitigation -->
    <circle cx="300" cy="60" r="6" fill="#B85C3E"/>
    <text x="300" y="40" text-anchor="middle" fill="#141413">09:22</text>
    <text x="300" y="90" text-anchor="middle" fill="#87867F">Rollback started</text>
    <!-- event 3: olive = resolved -->
    <circle cx="540" cy="60" r="6" fill="#788C5D"/>
    <text x="540" y="40" text-anchor="middle" fill="#141413">09:41</text>
    <text x="540" y="90" text-anchor="middle" fill="#87867F">All green</text>
  </g>
</svg>
```

---

## Collapsible sections

Built-in `<details>` — no JS needed. Good for "alternatives considered", "raw data", "appendix".

```html
<details>
  <summary>Alternatives considered</summary>
  <p>Option D was rejected because …</p>
  <p>Option E was rejected because …</p>
</details>
```

---

## Tabs

Minimal, no framework, no ARIA bells and whistles — but accessible enough for one-off docs.

```html
<div class="tabs">
  <nav>
    <button class="primary" data-t="py">Python</button>
    <button data-t="ts">TypeScript</button>
    <button data-t="rs">Rust</button>
  </nav>
  <pre data-p="py"><code>print(1)</code></pre>
  <pre data-p="ts" hidden><code>console.log(1)</code></pre>
  <pre data-p="rs" hidden><code>println!("{}", 1);</code></pre>
</div>
<style>
  .tabs nav{display:flex;gap:.25rem;margin-bottom:.25rem}
</style>
<script>
  document.querySelectorAll('.tabs nav button').forEach(btn => {
    btn.onclick = () => {
      const t = btn.dataset.t;
      const root = btn.closest('.tabs');
      root.querySelectorAll('nav button').forEach(b => b.classList.toggle('primary', b === btn));
      root.querySelectorAll('[data-p]').forEach(p => { p.hidden = p.dataset.p !== t; });
    };
  });
</script>
```

---

## Slider driving a CSS variable

The core pattern for design-prototype scenarios. Input → CSS var → visible change.

```html
<label>Duration <input id="dur" type="range" min="100" max="2000" step="50" value="400">
  <span id="durV">400</span>ms
</label>

<div class="demo">Hover me</div>

<style>
  .demo{--dur:400ms;display:inline-block;margin-top:1rem;padding:1rem 1.5rem;background:var(--clay);color:var(--paper);border-radius:8px;transition:transform var(--dur) ease-out}
  .demo:hover{transform:translateY(-6px) scale(1.04)}
</style>

<script>
  const dur = document.getElementById('dur');
  const demo = document.querySelector('.demo');
  const vLbl = document.getElementById('durV');
  dur.oninput = () => { demo.style.setProperty('--dur', dur.value + 'ms'); vLbl.textContent = dur.value; };
</script>
```

---

## Copy-as-prompt button (mandatory for editors)

Every interactive HTML needs at least one of these.

```html
<button class="primary" id="copyBtn">Copy as prompt</button>
<script>
  document.getElementById('copyBtn').onclick = async () => {
    // Gather whatever editor state you need:
    const state = {
      // … e.g., drag-drop positions, form values, tuned slider values
    };
    const prompt = `Apply these values to the component:\n\n\`\`\`json\n${JSON.stringify(state, null, 2)}\n\`\`\`\n\nThen …`;
    await navigator.clipboard.writeText(prompt);
    const btn = document.getElementById('copyBtn');
    const orig = btn.textContent;
    btn.textContent = 'Copied';
    setTimeout(() => (btn.textContent = orig), 1200);
  };
</script>
```

Variants — same pattern, different payload:
- **Copy as JSON** — `navigator.clipboard.writeText(JSON.stringify(state, null, 2))`
- **Copy as Markdown** — build a `| col | col |` table or bulleted list as a template literal
- **Copy as CSS** — `navigator.clipboard.writeText(computedCssString)`

---

## Draggable cards across columns

Minimum viable drag-drop using HTML5 drag events. Works for triage boards, kanban-style editors.

```html
<style>
  .cols{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem;margin:1rem 0}
  .col{background:var(--g100);border:1.5px solid var(--g300);border-radius:12px;padding:.75rem;min-height:220px}
  .col h3{margin:.2rem 0 .5rem;font-size:.95rem}
  .ticket{background:var(--paper);border:1.5px solid var(--g300);border-radius:8px;padding:.5rem .65rem;margin:.25rem 0;cursor:grab;font-size:.9rem}
  .ticket.dragging{opacity:.4}
  .col.hover{outline:2px dashed var(--clay);outline-offset:-4px}
</style>

<div class="cols">
  <div class="col" data-col="now"><h3>Now</h3></div>
  <div class="col" data-col="next"><h3>Next</h3></div>
  <div class="col" data-col="later"><h3>Later</h3></div>
  <div class="col" data-col="cut"><h3>Cut</h3></div>
</div>

<script>
  let dragged = null;

  // Seed tickets (swap in your data)
  const seed = [
    { id: 1, text: 'Fix flaky checkout test', col: 'now' },
    { id: 2, text: 'Migrate auth to OIDC',   col: 'next' },
    { id: 3, text: 'Nice-to-have dashboard', col: 'later' },
  ];
  const cols = Object.fromEntries([...document.querySelectorAll('.col')].map(c => [c.dataset.col, c]));
  for (const t of seed) {
    const el = document.createElement('div');
    el.className = 'ticket'; el.draggable = true; el.dataset.id = t.id; el.textContent = t.text;
    cols[t.col].appendChild(el);
  }

  document.querySelectorAll('.ticket').forEach(t => {
    t.addEventListener('dragstart', e => { dragged = t; t.classList.add('dragging'); });
    t.addEventListener('dragend',   () => { dragged?.classList.remove('dragging'); dragged = null; });
  });
  document.querySelectorAll('.col').forEach(col => {
    col.addEventListener('dragover', e => { e.preventDefault(); col.classList.add('hover'); });
    col.addEventListener('dragleave', () => col.classList.remove('hover'));
    col.addEventListener('drop', () => { col.classList.remove('hover'); if (dragged) col.appendChild(dragged); });
  });
</script>
```

Pair with a Copy-as-prompt button that exports the current column contents.

---

## Chips and callouts

Small semantic affordances that do a lot of work.

```html
<span class="chip">neutral</span>
<span class="chip ok">passed</span>
<span class="chip warn">flaky</span>
<span class="chip err">failing</span>

<div class="callout">Neutral note about something.</div>
<div class="callout warn">Heads-up: this is a common mistake.</div>
<div class="callout err">Blocker: this has to be fixed before merging.</div>

<style>
  .chip{display:inline-block;font-family:var(--mono);font-size:11px;letter-spacing:.04em;
        padding:3px 9px;border-radius:999px;
        background:var(--g100);border:1.5px solid var(--g300);color:var(--g700)}
  .chip.ok  {background:#E8EEDB;border-color:#C8D3B0;color:#4D5E36}
  .chip.warn{background:#F5E4D7;border-color:#E8C6A9;color:#8A4A28}
  .chip.err {background:#F1DBD6;border-color:#E0B2AA;color:#7A2F26}
  .callout{border-left:4px solid var(--clay);background:var(--paper);
           border-top:1.5px solid var(--g300);border-right:1.5px solid var(--g300);
           border-bottom:1.5px solid var(--g300);
           padding:16px 20px;border-radius:0 12px 12px 0;margin:1rem 0}
  .callout.warn{border-left-color:var(--clay-d)}
  .callout.err {border-left-color:var(--rust)}
  .callout.ok  {border-left-color:var(--olive)}
</style>
```
