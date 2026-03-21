# LLM Council

A multi-model consensus engine that queries multiple AI models simultaneously, displays their responses side-by-side in a live dashboard, and lets the models anonymously judge each other's answers.

Built with zero external dependencies — Python stdlib server + vanilla JavaScript frontend.

![Dashboard Preview](https://img.shields.io/badge/Models-6-coral) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![License](https://img.shields.io/badge/License-MIT-green)

---

## What It Does

1. **Send one prompt to multiple AI models at once** — Claude Sonnet 4.5, Claude Opus 4.5, GPT-4o, GPT-5.1, Gemini 2.5 Flash, and Gemini 2.5 Pro
2. **Watch responses stream in real-time** via Server-Sent Events (SSE)
3. **Compare answers side-by-side** in a responsive card grid
4. **Run anonymous model voting** — each model scores every other model's response (1-10) without knowing whose response it's judging. The highest aggregate score wins.
5. **Synthesize consensus** — an AI-powered analysis of what models agree on, where they diverge, and a best combined answer

---

## Features

- **Parallel Streaming** — All models are queried simultaneously using ThreadPoolExecutor. Responses stream to the browser as each model completes.
- **Model Selector Dropdown** — Choose any combination of 2-6 models via an interactive checkbox dropdown.
- **Anonymous Model-to-Model Voting** — Each model acts as an impartial judge, scoring anonymized versions of every other model's response. Aggregate scores determine the winner.
- **Consensus Synthesis** — Claude Sonnet 4.5 analyzes all responses and produces: consensus points, divergence analysis, a synthesized best answer, and a confidence rating (1-10).
- **Session History** — Previous council sessions are saved in browser localStorage for quick recall.
- **Dark/Light Theme** — Capybara-inspired design system (HappyCapy) with warm coral, teal, and sandy tones.
- **Zero Dependencies** — Python stdlib `http.server` backend, vanilla JS frontend. No npm, no pip install, no build step.

---

## Available Models

| Model | Provider | Model ID |
|-------|----------|----------|
| Claude Sonnet 4.5 | Anthropic | `anthropic/claude-sonnet-4.5` |
| Claude Opus 4.5 | Anthropic | `anthropic/claude-opus-4.5` |
| GPT-4o | OpenAI | `openai/gpt-4o` |
| GPT-5.1 | OpenAI | `openai/gpt-5.1` |
| Gemini 2.5 Flash | Google | `google/gemini-2.5-flash` |
| Gemini 2.5 Pro | Google | `google/gemini-2.5-pro` |

---

## Quick Start

### Prerequisites

- Python 3.9+
- An AI Gateway API key (set as environment variable)

### Run

```bash
export AI_GATEWAY_API_KEY="your-api-key-here"

cd scripts
python3 server.py
```

The server starts on `http://localhost:8787` by default. Open it in your browser.

### Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `COUNCIL_PORT` | `8787` | HTTP server port |
| `AI_GATEWAY_API_KEY` | *(required)* | API key for the AI Gateway |

---

## How It Works

### Architecture

```
llm-council/
├── SKILL.md                        # Claude Code skill definition
├── README.md                       # This file
└── scripts/
    ├── server.py                   # Python HTTP server (ThreadingHTTPServer)
    ├── ai_gateway.py               # AI Gateway client module
    └── static/
        ├── index.html              # Dashboard HTML + CSS
        └── app.js                  # Client-side JavaScript
```

### Request Flow

```
Browser                    Server (Python)              AI Gateway
  │                            │                            │
  │── POST /council/stream ──>│                            │
  │                            │── query model 1 ────────>│
  │                            │── query model 2 ────────>│
  │                            │── query model 3 ────────>│
  │                            │   (parallel threads)      │
  │                            │                            │
  │<── SSE: model 2 started ──│                            │
  │<── SSE: model 1 complete ─│<── response 1 ────────────│
  │<── SSE: model 3 complete ─│<── response 3 ────────────│
  │<── SSE: model 2 complete ─│<── response 2 ────────────│
  │<── SSE: {"status":"done"} │                            │
  │                            │                            │
```

### Anonymous Voting Flow

```
Browser                    Server                       AI Gateway
  │                            │                            │
  │── POST /council/vote ────>│                            │
  │                            │── judge: model 1 ───────>│
  │<── SSE: keepalive ────────│── judge: model 2 ───────>│
  │<── SSE: keepalive ────────│── judge: model 3 ───────>│
  │<── SSE: keepalive ────────│   (parallel, 5s pings)    │
  │                            │                            │
  │                            │<── scores from model 1 ──│
  │                            │<── scores from model 2 ──│
  │                            │<── scores from model 3 ──│
  │                            │                            │
  │                            │── aggregate scores        │
  │                            │── determine winner        │
  │<── SSE: {result} ─────────│                            │
```

Each model judges all OTHER responses anonymously (labelled A, B, C...) and scores them 1-10 on accuracy, helpfulness, and quality. The response with the highest aggregate score wins.

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Dashboard HTML |
| `GET` | `/api/models` | List available models |
| `GET` | `/health` | Health check |
| `POST` | `/api/council/stream` | Query models (SSE streaming) |
| `POST` | `/api/council` | Query models (batch, non-streaming) |
| `POST` | `/api/council/synthesize` | Synthesize consensus from responses |
| `POST` | `/api/council/vote` | Anonymous model-to-model vote (SSE with keepalive) |

---

## Technical Details

### Server

- Uses Python's `ThreadingHTTPServer` for concurrent request handling (critical for SSE streams + keepalive pings during voting)
- Static files served with `Cache-Control: no-store, no-cache` headers to prevent stale JS
- SSE streams send an explicit `{"status":"done"}` event so the frontend doesn't depend on connection close (which can be delayed by reverse proxies)
- Vote endpoint sends `: keepalive` SSE comments every 5 seconds to prevent Cloudflare/proxy 524 timeout errors

### Frontend

- Vanilla JavaScript, no framework, no build step
- SSE stream parsing via `ReadableStream` reader with manual `data:` line extraction
- Dropdown model selector with click-outside-to-close via document `mousedown` listener
- Basic Markdown rendering for model responses (headings, bold, code blocks, lists)
- Cache-busting via versioned script tag: `app.js?v=...`

### AI Gateway

- All model requests go through `https://ai-gateway.happycapy.ai/api/v1`
- Requires Bearer token auth and `Origin: https://trickle.so` header
- Supports both streaming and non-streaming chat completions
- Model IDs use dot notation: `anthropic/claude-sonnet-4.5` (not hyphens)

---

## Claude Code Skill

This project is also a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill. Install it to `~/.claude/skills/llm-council/` and it will be available via the `/llm-council` command or triggered by phrases like "start the LLM council", "compare models", or "convene council".

---

## License

MIT
