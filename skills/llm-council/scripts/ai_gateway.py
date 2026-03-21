"""AI Gateway client module for the LLM Council dashboard.

Handles all communication with the AI Gateway API using only Python stdlib.
Supports single queries, parallel multi-model queries, streaming results,
and response synthesis.
"""

import json
import os
import queue
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://ai-gateway.happycapy.ai/api/v1"
CHAT_ENDPOINT = f"{BASE_URL}/chat/completions"
DEFAULT_TIMEOUT = 120
SYNTHESIS_MODEL = "anthropic/claude-sonnet-4.5"


def _log(msg: str) -> None:
    """Log a timestamped message to stderr."""
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{ts}] ai_gateway: {msg}", file=sys.stderr, flush=True)


def _build_headers(api_key: str) -> dict:
    """Return the required headers for the AI Gateway API."""
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Origin": "https://trickle.so",
        "User-Agent": "Mozilla/5.0 (compatible; AI-Gateway-Client/1.0)",
    }


def _make_request(model_id: str, messages: list, api_key: str,
                  stream: bool = False, max_tokens: int = 4096) -> dict:
    """Send a chat completion request and return the parsed JSON response.

    For streaming requests, reassembles the SSE chunks into a single result
    dict matching the non-streaming shape.
    """
    body = json.dumps({
        "model": model_id,
        "messages": messages,
        "stream": stream,
        "max_tokens": max_tokens,
    }).encode("utf-8")

    req = urllib.request.Request(
        CHAT_ENDPOINT,
        data=body,
        headers=_build_headers(api_key),
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
        if not stream:
            return json.loads(resp.read().decode("utf-8"))

        # Streaming: reassemble SSE chunks
        content_parts = []
        for raw_line in resp:
            line = raw_line.decode("utf-8").strip()
            if not line.startswith("data: "):
                continue
            payload = line[len("data: "):]
            if payload == "[DONE]":
                break
            chunk = json.loads(payload)
            delta = chunk.get("choices", [{}])[0].get("delta", {})
            if "content" in delta:
                content_parts.append(delta["content"])

        return {
            "choices": [{"message": {"content": "".join(content_parts)}}],
            "usage": {"completion_tokens": 0},
        }


def query_model(prompt: str, model_id: str, api_key: str,
                system_prompt: str = None, stream: bool = False) -> dict:
    """Query a single model and return a standardised result dict.

    Returns:
        {
            "model":       model_id,
            "content":     str,
            "status":      "success" | "error",
            "duration":    float (seconds),
            "token_count": int,
        }
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    t0 = time.monotonic()
    try:
        _log(f"querying {model_id} (stream={stream})")
        data = _make_request(model_id, messages, api_key, stream=stream)
        duration = time.monotonic() - t0

        content = data["choices"][0]["message"]["content"]
        token_count = data.get("usage", {}).get("completion_tokens", 0)
        _log(f"{model_id} responded in {duration:.2f}s ({token_count} tokens)")
        return {
            "model": model_id,
            "content": content,
            "status": "success",
            "duration": round(duration, 3),
            "token_count": token_count,
        }
    except urllib.error.HTTPError as exc:
        duration = time.monotonic() - t0
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        msg = f"HTTP {exc.code}: {body[:300]}"
        _log(f"{model_id} HTTP error: {msg}")
        return {"model": model_id, "content": msg, "status": "error",
                "duration": round(duration, 3), "token_count": 0}
    except urllib.error.URLError as exc:
        duration = time.monotonic() - t0
        msg = f"URL error: {exc.reason}"
        _log(f"{model_id} URL error: {msg}")
        return {"model": model_id, "content": msg, "status": "error",
                "duration": round(duration, 3), "token_count": 0}
    except (json.JSONDecodeError, KeyError, IndexError) as exc:
        duration = time.monotonic() - t0
        msg = f"Parse error: {exc}"
        _log(f"{model_id} parse error: {msg}")
        return {"model": model_id, "content": msg, "status": "error",
                "duration": round(duration, 3), "token_count": 0}
    except Exception as exc:
        duration = time.monotonic() - t0
        msg = f"{type(exc).__name__}: {exc}"
        _log(f"{model_id} unexpected error: {msg}")
        return {"model": model_id, "content": msg, "status": "error",
                "duration": round(duration, 3), "token_count": 0}


def query_models_parallel(prompt: str, model_ids: list, api_key: str,
                          system_prompt: str = None) -> list:
    """Query multiple models in parallel and return all results.

    Each model runs in its own thread via ThreadPoolExecutor.
    Returns a list of result dicts (same shape as query_model output).
    """
    results = []
    with ThreadPoolExecutor(max_workers=len(model_ids)) as pool:
        futures = {
            pool.submit(query_model, prompt, mid, api_key, system_prompt): mid
            for mid in model_ids
        }
        for future in as_completed(futures):
            results.append(future.result())
    return results


def query_models_stream(prompt: str, model_ids: list, api_key: str,
                        system_prompt: str = None):
    """Generator that yields per-model status events as models complete.

    Yields dicts of the form:
        {"model": id, "status": "started"}
        {"model": id, "status": "complete", "content": ..., "duration": ..., "token_count": ...}
        {"model": id, "status": "error",    "content": error_msg}
    """
    q: queue.Queue = queue.Queue()

    def _worker(model_id: str) -> None:
        q.put({"model": model_id, "status": "started"})
        result = query_model(prompt, model_id, api_key, system_prompt)
        if result["status"] == "success":
            q.put({
                "model": model_id,
                "status": "complete",
                "content": result["content"],
                "duration": result["duration"],
                "token_count": result["token_count"],
            })
        else:
            q.put({
                "model": model_id,
                "status": "error",
                "content": result["content"],
            })

    total = len(model_ids)
    completed = 0

    with ThreadPoolExecutor(max_workers=total) as pool:
        for mid in model_ids:
            pool.submit(_worker, mid)

        # We expect exactly 2 events per model: started + complete/error
        expected = total * 2
        received = 0
        while received < expected:
            event = q.get()
            yield event
            received += 1
            if event["status"] in ("complete", "error"):
                completed += 1


def anonymous_model_vote(prompt: str, responses: list, api_key: str) -> dict:
    """Have each model anonymously judge every other model's response.

    Args:
        prompt:    The original user prompt.
        responses: List of dicts [{"model": id, "content": text}, ...].
        api_key:   AI Gateway API key.

    Returns:
        {
            "votes": { model_id: {"score": int, "voters": [{"voter": id, "points": int, "reason": str}]} },
            "winner": model_id,
            "details": [ {"voter": id, "rankings": [...]} ]
        }
    """
    if len(responses) < 2:
        return {"votes": {}, "winner": "", "details": []}

    # Build anonymised labels
    labels = "ABCDEFGHIJKLMNOP"
    model_ids = [r["model"] for r in responses]

    # Initialise vote tallies
    votes = {mid: {"score": 0, "voters": []} for mid in model_ids}
    details = []

    def _judge(voter_id: str) -> dict:
        """One model judges all OTHER responses."""
        others = []
        label_to_model = {}
        label_idx = 0
        for r in responses:
            if r["model"] == voter_id:
                continue
            lbl = labels[label_idx] if label_idx < len(labels) else f"R{label_idx}"
            label_to_model[lbl] = r["model"]
            others.append(f"Response {lbl}:\n{r['content']}")
            label_idx += 1

        if not others:
            return {"voter": voter_id, "rankings": []}

        system = (
            "You are an impartial judge in an LLM evaluation council. "
            "You are given a prompt and several anonymous responses labelled with letters. "
            "Score each response from 1 to 10 based on accuracy, helpfulness, and quality. "
            "Reply ONLY with valid JSON (no markdown fences) in this exact format:\n"
            '[{"label": "A", "score": 8, "reason": "brief reason"}, ...]'
        )
        user_content = (
            f"Original prompt: {prompt}\n\n"
            + "\n\n".join(others)
            + "\n\nScore each response. Reply ONLY with a JSON array."
        )

        result = query_model(
            prompt=user_content,
            model_id=voter_id,
            api_key=api_key,
            system_prompt=system,
            stream=False,
        )

        rankings = []
        if result["status"] == "success":
            raw = result["content"].strip()
            # Strip markdown fences if present
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[-1]
                if raw.endswith("```"):
                    raw = raw[:-3]
                raw = raw.strip()
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, list):
                    for entry in parsed:
                        lbl = entry.get("label", "")
                        score = int(entry.get("score", 0))
                        reason = entry.get("reason", "")
                        target_model = label_to_model.get(lbl)
                        if target_model:
                            rankings.append({
                                "label": lbl,
                                "target": target_model,
                                "score": score,
                                "reason": reason,
                            })
            except (json.JSONDecodeError, ValueError, TypeError) as e:
                _log(f"Judge {voter_id} returned unparseable response: {e}")

        return {"voter": voter_id, "rankings": rankings}

    # Run all judges in parallel
    judge_results = []
    with ThreadPoolExecutor(max_workers=len(model_ids)) as pool:
        futures = {
            pool.submit(_judge, mid): mid for mid in model_ids
        }
        for future in as_completed(futures):
            judge_results.append(future.result())

    # Aggregate
    for jr in judge_results:
        details.append(jr)
        for ranking in jr.get("rankings", []):
            target = ranking["target"]
            if target in votes:
                votes[target]["score"] += ranking["score"]
                votes[target]["voters"].append({
                    "voter": jr["voter"],
                    "points": ranking["score"],
                    "reason": ranking.get("reason", ""),
                })

    # Determine winner
    winner = max(votes.keys(), key=lambda k: votes[k]["score"]) if votes else ""

    _log(f"Vote complete: winner={winner}, scores={[(k, v['score']) for k, v in votes.items()]}")
    return {"votes": votes, "winner": winner, "details": details}


def synthesize_responses(prompt: str, responses: list, api_key: str) -> str:
    """Synthesize multiple model responses into a single analysis.

    Args:
        prompt:    The original user prompt.
        responses: List of result dicts from query_model / query_models_parallel.
        api_key:   AI Gateway API key.

    Returns:
        The synthesised analysis as a plain string.
    """
    model_sections = []
    for r in responses:
        label = r.get("model", "unknown")
        content = r.get("content", "(no content)")
        model_sections.append(f"[{label}]: {content}")

    system = (
        "You are a synthesis engine for an LLM Council. Multiple AI models "
        "were asked the same question. Analyze their responses and provide:\n"
        "1. CONSENSUS: What all models agree on\n"
        "2. DIVERGENCE: Where models disagree and why\n"
        "3. SYNTHESIS: The best combined answer, taking the strongest points "
        "from each\n"
        "4. CONFIDENCE: Rate 1-10 how confident you are in the synthesized "
        "answer"
    )

    user_content = (
        f"Original prompt: {prompt}\n\n"
        f"Model responses:\n" + "\n\n".join(model_sections)
    )

    result = query_model(
        prompt=user_content,
        model_id=SYNTHESIS_MODEL,
        api_key=api_key,
        system_prompt=system,
    )

    if result["status"] == "error":
        _log(f"synthesis failed: {result['content']}")
        return f"[Synthesis error] {result['content']}"

    return result["content"]


def chairman_review(prompt: str, responses: list, vote_results: dict,
                    chairman_model: str, api_key: str) -> str:
    """Chairman model reviews all responses and voting results, writes a final answer.

    Args:
        prompt:          The original user prompt.
        responses:       List of dicts [{"model": id, "content": text}, ...].
        vote_results:    Dict from anonymous_model_vote: {"votes": {...}, "winner": id, "details": [...]}.
        chairman_model:  Model ID to act as chairman.
        api_key:         AI Gateway API key.

    Returns:
        The chairman's final definitive answer as a plain string.
    """
    # Build context with all model responses
    model_sections = []
    for r in responses:
        label = r.get("model", "unknown")
        content = r.get("content", "(no content)")
        model_sections.append(f"[{label}]:\n{content}")

    # Build voting summary
    votes = vote_results.get("votes", {})
    winner = vote_results.get("winner", "")
    details = vote_results.get("details", [])

    vote_summary = f"WINNER: {winner}\n\nSCORES:\n"
    for model_id, vote_data in sorted(votes.items(), key=lambda x: x[1]["score"], reverse=True):
        score = vote_data.get("score", 0)
        voters = vote_data.get("voters", [])
        vote_summary += f"- {model_id}: {score} points\n"
        for voter in voters:
            vote_summary += f"  * {voter.get('voter', '?')}: +{voter.get('points', 0)} ({voter.get('reason', '')})\n"

    critique_summary = "\nDETAILED CRITIQUES:\n"
    for judge in details:
        voter_id = judge.get("voter", "unknown")
        rankings = judge.get("rankings", [])
        if rankings:
            critique_summary += f"\n{voter_id}'s evaluations:\n"
            for rank in rankings:
                critique_summary += (
                    f"  - {rank.get('target', '?')}: {rank.get('score', 0)}/10"
                    f" - {rank.get('reason', '')}\n"
                )

    system = (
        "You are the CHAIRMAN of an LLM Council. You have reviewed all model responses "
        "to the original prompt, AND you have access to the anonymous voting results where "
        "each model scored the others.\n\n"
        "Your role is NOT to summarize or find consensus. Instead, you must:\n"
        "1. Read ALL responses carefully\n"
        "2. Consider the voting scores and critiques from peer models\n"
        "3. Write a NEW, DEFINITIVE answer that incorporates the best elements\n"
        "4. Make executive decisions where models disagree\n"
        "5. Provide your reasoning for key choices\n\n"
        "Be authoritative. This is YOUR final answer as chairman, not a synthesis."
    )

    user_content = (
        f"ORIGINAL PROMPT:\n{prompt}\n\n"
        f"MODEL RESPONSES:\n{'=' * 60}\n" + "\n\n".join(model_sections) + "\n\n"
        f"VOTING RESULTS:\n{'=' * 60}\n{vote_summary}\n{critique_summary}\n\n"
        f"As chairman, provide your final definitive answer to the original prompt, "
        f"informed by all responses and voting results."
    )

    _log(f"chairman review by {chairman_model}")
    result = query_model(
        prompt=user_content,
        model_id=chairman_model,
        api_key=api_key,
        system_prompt=system,
        stream=False,
    )

    if result["status"] == "error":
        _log(f"chairman review failed: {result['content']}")
        return f"[Chairman review error] {result['content']}"

    _log(f"chairman review complete by {chairman_model} in {result['duration']}s")
    return result["content"]
