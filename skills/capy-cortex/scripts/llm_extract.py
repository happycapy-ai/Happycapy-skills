#!/usr/bin/env python3
"""Capy Cortex v2 - LLM-powered extraction engine with quality gate.
4-pass extraction: Event -> Causal Analysis -> Rule Synthesis -> Quality Score.
Only rules scoring >= 2/4 are stored. Logs all extractions for audit."""

import json
import os
import sys
import time
import sqlite3
import urllib.request
import urllib.error
from pathlib import Path

# --- Provider-agnostic configuration ---
# Cortex works with ANY LLM provider that exposes an OpenAI-compatible
# chat completions endpoint (the de facto industry standard).
# Supported: OpenAI, Anthropic (via OpenRouter/LiteLLM), Google Gemini,
# xAI Grok, Ollama, Together AI, Fireworks, Azure OpenAI, and more.
#
# Required env vars (set ONE of each group):
#   API URL:  CORTEX_API_URL  or  OPENAI_BASE_URL
#   API Key:  CORTEX_API_KEY  or  OPENAI_API_KEY
#   Models:   CORTEX_SMART_MODEL  and  CORTEX_FAST_MODEL

_raw_url = os.environ.get("CORTEX_API_URL",
           os.environ.get("AI_GATEWAY_URL",
           os.environ.get("OPENAI_BASE_URL", "")))
if _raw_url:
    API_URL = _raw_url.rstrip("/")
    if not API_URL.endswith("/chat/completions"):
        API_URL = API_URL + "/chat/completions"
else:
    API_URL = ""  # Not configured -- LLM calls will be skipped gracefully

API_KEY = os.environ.get("CORTEX_API_KEY",
          os.environ.get("AI_GATEWAY_API_KEY",
          os.environ.get("OPENAI_API_KEY", "")))
DB_PATH = Path(__file__).parent.parent / "cortex.db"

# Model identifiers -- format depends on your provider:
#   OpenRouter:  "anthropic/claude-sonnet-4.6", "google/gemini-2.5-flash", "openai/gpt-4o"
#   OpenAI:      "gpt-4o", "gpt-4o-mini"
#   Ollama:      "llama3", "mistral"
#   Together:    "meta-llama/Llama-3-70b-chat-hf"
CORTEX_FAST = os.environ.get("CORTEX_FAST_MODEL", "")
CORTEX_SMART = os.environ.get("CORTEX_SMART_MODEL", "")

# Backward-compat aliases (used by consolidate.py imports)
HAIKU = CORTEX_FAST
SONNET = CORTEX_SMART
MODELS = [m for m in [CORTEX_FAST, CORTEX_SMART] if m]  # Only non-empty

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "CapyCortex/4.0",
    "Accept": "application/json",
}

QUALITY_THRESHOLD = 2  # Minimum quality score (0-4) to store a rule

# --- Prompts ---

EXTRACT_PROMPT = """Extract the root cause of this tool failure.
Return ONE JSON object: {{"root_cause": "why it failed", "fix": "how to fix", "category": "dependency_error|file_not_found|permission_denied|syntax_error|type_error|compilation_error|network_error|auth_error|git_error|database_error|port_conflict|resource_error|config_error", "actionable": true}}
No markdown. Just JSON.
Tool: {tool_name} | Command: {command}
Error: {error_text}"""

CORRECTION_PROMPT = """Extract the SINGLE most important rule from this user correction.
Return ONE JSON object: {{"rule": "imperative sentence", "category": "correction|preference|anti_pattern", "topic": "git|npm|python|docker|react|api|testing|browser-automation|video-generation|skill-creation|security|database|build|deployment|universal", "actionable": true}}
No markdown. Just JSON.
User said: {user_text}"""

CAUSAL_PROMPT = """Analyze the causal chain for this error. What is the ROOT cause (not symptom)?
Distinguish: correlation vs causation. What SPECIFICALLY caused the failure?
Return ONE JSON: {{"root_cause": "specific technical cause", "causal_chain": ["step1", "step2"], "category": "dependency_error|file_not_found|permission_denied|syntax_error|type_error|network_error|auth_error|git_error|config_error|resource_error", "fix": "specific actionable fix", "entities": ["tool/lib/file names involved"]}}
No markdown. Just JSON.
Context: {context}"""

QUALITY_PROMPT = """Score this rule on 4 dimensions (0 or 1 each):
1. ACTIONABLE: Can an agent act on this immediately? (not vague advice)
2. SPECIFIC: Does it name concrete tools/files/commands? (not generic)
3. NOVEL: Is this non-obvious? (not "check if file exists")
4. DURABLE: Will this be true in 6 months? (not version-specific hack)
Return ONE JSON: {{"actionable": 0, "specific": 0, "novel": 0, "durable": 0, "total": 0, "reason": "brief explanation"}}
No markdown. Just JSON.
Rule: {rule_text}"""

SESSION_PROMPT = """Extract actionable learnings from this coding session.
Return a JSON array of objects (max 3 most important):
[{{"rule": "imperative sentence", "category": "correction|preference|anti_pattern|pattern", "topic": "git|npm|python|api|testing|security|universal", "cause": "why this matters"}}]
Skip obvious/trivial things. Only extract genuinely useful patterns.
No markdown. Just the JSON array.
Session messages:
{messages}"""


def _call_llm(prompt, timeout=15, max_tokens=200, model=None):
    """Call LLM with model fallback. Returns parsed JSON or None."""
    if not API_KEY or not API_URL:
        return None
    if model and not model.strip():
        model = None  # Ignore empty model strings
    models = [model] if model else MODELS
    for m in models:
        try:
            payload = json.dumps({
                "model": m,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens, "temperature": 0,
            }).encode("utf-8")
            headers = {**HEADERS, "Authorization": f"Bearer {API_KEY}"}
            req = urllib.request.Request(API_URL, data=payload, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"].strip()
                if content.startswith("```"):
                    lines = content.split("\n")
                    inner = "\n".join(lines[1:])
                    if "```" in inner:
                        inner = inner[:inner.rfind("```")]
                    content = inner.strip()
                parsed = json.loads(content)
                if isinstance(parsed, list) and len(parsed) > 0:
                    return parsed if model else parsed[0]
                if isinstance(parsed, dict):
                    return parsed
        except Exception as e:
            _log(f"{type(e).__name__} with {m}: {e}")
            continue
    return None


def _log(msg):
    print(f"[cortex-llm] {msg}", file=sys.stderr)


def _log_extraction(session_id, pass_name, model, input_text, output, score, accepted, latency):
    """Log extraction to DB for audit trail."""
    try:
        db = sqlite3.connect(str(DB_PATH))
        db.execute("PRAGMA busy_timeout=2000")
        db.execute("""INSERT INTO extraction_log
            (session_id, pass_name, model, input_text, output_json, quality_score, accepted, latency_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (session_id, pass_name, model, input_text[:500],
             json.dumps(output) if output else None, score, int(accepted), latency))
        db.commit()
        db.close()
    except Exception:
        pass


# --- Backward-compatible functions (used by existing hooks) ---

def extract_root_cause(tool_name, tool_input, error_text, timeout=15):
    """Extract root cause from tool failure. Returns dict or None."""
    command = tool_input.get("command", str(tool_input)[:200]) if isinstance(tool_input, dict) else str(tool_input)[:200]
    prompt = EXTRACT_PROMPT.format(tool_name=tool_name, command=command, error_text=error_text[:500])
    result = _call_llm(prompt, timeout=timeout)
    if result and all(k in result for k in ("root_cause", "fix", "category", "actionable")):
        return result
    return None


def extract_correction(user_text, timeout=15):
    """Extract rule from user correction. Returns dict or None."""
    prompt = CORRECTION_PROMPT.format(user_text=user_text[:500])
    result = _call_llm(prompt, timeout=timeout)
    if result and all(k in result for k in ("rule", "category", "topic", "actionable")):
        return result
    return None


# --- v2: Quality-gated extraction ---

def extract_with_quality_gate(tool_name, tool_input, error_text, session_id=None):
    """2-pass extraction with quality gate.
    Pass 1: Causal analysis (Sonnet) - WHY it failed
    Pass 2: Quality scoring (Haiku) - is it worth storing?
    Returns (rule_dict, quality_score) or (None, 0) if below threshold."""
    command = tool_input.get("command", str(tool_input)[:200]) if isinstance(tool_input, dict) else str(tool_input)[:200]
    context = f"Tool: {tool_name}\nCommand: {command}\nError: {error_text[:800]}"

    # Pass 1: Causal analysis
    t0 = time.time()
    causal = _call_llm(CAUSAL_PROMPT.format(context=context), timeout=15, max_tokens=300, model=SONNET)
    latency1 = int((time.time() - t0) * 1000)
    _log_extraction(session_id, "causal_analysis", SONNET, context, causal, None, False, latency1)

    if not causal or not causal.get("root_cause"):
        return None, 0

    rule_text = f"{causal['root_cause']}. Fix: {causal.get('fix', 'unknown')}"

    # Pass 2: Quality scoring
    t0 = time.time()
    quality = _call_llm(QUALITY_PROMPT.format(rule_text=rule_text), timeout=10, max_tokens=150, model=HAIKU)
    latency2 = int((time.time() - t0) * 1000)
    score = quality.get("total", 0) if quality else 0
    accepted = score >= QUALITY_THRESHOLD
    _log_extraction(session_id, "quality_score", HAIKU, rule_text, quality, score, accepted, latency2)

    if not accepted:
        _log(f"Rule rejected (score={score}/{QUALITY_THRESHOLD}): {rule_text[:80]}")
        return None, score

    return {
        "content": rule_text,
        "category": causal.get("category", "unknown_error"),
        "entities": causal.get("entities", []),
        "causal_chain": causal.get("causal_chain", []),
        "quality_score": score,
        "extraction_method": "llm_v2",
    }, score


def extract_session_learnings(user_messages, session_id=None):
    """Extract learnings from session messages. Returns list of rule dicts.
    Each rule is quality-gated: only score >= 2 returned."""
    if not user_messages:
        return []
    combined = "\n---\n".join(msg[:300] for msg in user_messages[:10])
    t0 = time.time()
    results = _call_llm(SESSION_PROMPT.format(messages=combined[:3000]),
                        timeout=20, max_tokens=500, model=SONNET)
    latency = int((time.time() - t0) * 1000)
    _log_extraction(session_id, "session_extract", SONNET, combined[:500], results, None, False, latency)

    if not results:
        return []
    if isinstance(results, dict):
        results = [results]
    if not isinstance(results, list):
        return []

    accepted = []
    for r in results[:5]:
        rule_text = r.get("rule", "")
        if not rule_text or len(rule_text) < 10:
            continue
        # Quality gate each rule
        t0 = time.time()
        quality = _call_llm(QUALITY_PROMPT.format(rule_text=rule_text), timeout=10, max_tokens=100, model=HAIKU)
        qlat = int((time.time() - t0) * 1000)
        score = quality.get("total", 0) if quality else 0
        ok = score >= QUALITY_THRESHOLD
        _log_extraction(session_id, "session_quality", HAIKU, rule_text, quality, score, ok, qlat)
        if ok:
            accepted.append({
                "content": rule_text,
                "category": r.get("category", "pattern"),
                "topic": r.get("topic", "universal"),
                "cause": r.get("cause", ""),
                "quality_score": score,
                "extraction_method": "llm_v2_session",
            })
    return accepted


def score_existing_rule(rule_text):
    """Score an existing rule. Returns quality score 0-4."""
    result = _call_llm(QUALITY_PROMPT.format(rule_text=rule_text), timeout=10, max_tokens=100, model=HAIKU)
    return result.get("total", 0) if result else 0


if __name__ == "__main__":
    print("=== Capy Cortex v2 LLM Extract - Self-Test ===")
    print(f"API URL:      {'configured' if API_URL else 'MISSING  -- set CORTEX_API_URL'}")
    print(f"API Key:      {'present' if API_KEY else 'MISSING  -- set CORTEX_API_KEY'}")
    print(f"Smart model:  {CORTEX_SMART or 'MISSING  -- set CORTEX_SMART_MODEL'}")
    print(f"Fast model:   {CORTEX_FAST or 'MISSING  -- set CORTEX_FAST_MODEL'}")
    print(f"Quality threshold: {QUALITY_THRESHOLD}/4\n")

    print("Test 1: extract_root_cause (backward compat)")
    r1 = extract_root_cause("Bash", {"command": "npm install"},
        "npm ERR! ERESOLVE peer dep conflict: react@18.2.0", timeout=10)
    print(f"  {'PASS' if r1 else 'FAIL'}: {json.dumps(r1, indent=2) if r1 else 'None'}\n")

    print("Test 2: extract_with_quality_gate (v2)")
    r2, score = extract_with_quality_gate("Bash", {"command": "npm install"},
        "npm ERR! ERESOLVE peer dep conflict: react@18.2.0", session_id="test")
    print(f"  Score: {score}/4 | {'ACCEPTED' if r2 else 'REJECTED'}")
    if r2: print(f"  Rule: {r2['content'][:100]}\n")

    print("Test 3: score_existing_rule")
    s = score_existing_rule("Always use npm ci instead of npm install in CI environments")
    print(f"  Score: {s}/4\n")

    print("Test 4: extract_session_learnings")
    learnings = extract_session_learnings(["no dont use npm install! use npm ci!",
        "also make sure to check the lockfile exists first"], session_id="test")
    print(f"  Extracted: {len(learnings)} rules")
    for l in learnings:
        print(f"  [{l['quality_score']}] {l['content'][:80]}")
