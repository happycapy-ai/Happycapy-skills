#!/usr/bin/env python3
"""LLM Council Dashboard - HTTP Server

Main entry point. Serves the dashboard UI and proxies requests
to multiple LLM providers via the ai_gateway module.
"""

import json
import os
import signal
import sys
import threading
import time
from functools import partial
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from queue import Empty, Queue
from urllib.parse import urlparse

from ai_gateway import query_models_parallel, query_models_stream, synthesize_responses, anonymous_model_vote, chairman_review

STATIC_DIR = Path(__file__).resolve().parent / "static"

AVAILABLE_MODELS = [
    {"id": "anthropic/claude-sonnet-4.5", "name": "Claude Sonnet 4.5", "provider": "Anthropic"},
    {"id": "anthropic/claude-opus-4.5", "name": "Claude Opus 4.5", "provider": "Anthropic"},
    {"id": "openai/gpt-4o", "name": "GPT-4o", "provider": "OpenAI"},
    {"id": "openai/gpt-5.1", "name": "GPT-5.1", "provider": "OpenAI"},
    {"id": "google/gemini-2.5-flash", "name": "Gemini 2.5 Flash", "provider": "Google"},
    {"id": "google/gemini-2.5-pro", "name": "Gemini 2.5 Pro", "provider": "Google"},
    {"id": "x-ai/grok-4", "name": "Grok 4", "provider": "xAI"},
    {"id": "moonshotai/kimi-k2.5", "name": "Kimi K2.5", "provider": "Moonshot"},
    {"id": "deepseek/deepseek-r1", "name": "DeepSeek R1", "provider": "DeepSeek"},
]

MIME_TYPES = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".json": "application/json",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
}


class CouncilRequestHandler(SimpleHTTPRequestHandler):
    """Handles all HTTP requests for the LLM Council dashboard."""

    def __init__(self, *args, api_key: str = "", **kwargs):
        self.api_key = api_key
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    # -- Response helpers --------------------------------------------------

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send_json(self, data, status=HTTPStatus.OK):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, status, message):
        self._send_json({"error": message}, status=status)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return None
        return json.loads(self.rfile.read(length))

    def _serve_static(self, filepath: Path):
        if not filepath.is_file():
            self._send_error_json(HTTPStatus.NOT_FOUND, "File not found")
            return
        mime = MIME_TYPES.get(filepath.suffix, "application/octet-stream")
        body = filepath.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    # -- Route dispatch ----------------------------------------------------

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/" or path == "/index.html":
            self._serve_static(STATIC_DIR / "index.html")
        elif path.startswith("/static/"):
            safe_name = Path(path.split("/static/", 1)[1]).name
            self._serve_static(STATIC_DIR / safe_name)
        elif path == "/api/models":
            self._send_json({"models": AVAILABLE_MODELS})
        elif path == "/health":
            self._send_json({"status": "ok", "version": "1.0"})
        else:
            self._send_error_json(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self):
        path = urlparse(self.path).path

        if path == "/api/council":
            self._handle_council()
        elif path == "/api/council/stream":
            self._handle_council_stream()
        elif path == "/api/council/synthesize":
            self._handle_synthesize()
        elif path == "/api/council/vote":
            self._handle_vote()
        elif path == "/api/council/chairman":
            self._handle_chairman()
        else:
            self._send_error_json(HTTPStatus.NOT_FOUND, "Not found")

    # -- Endpoint handlers -------------------------------------------------

    def _handle_council(self):
        body = self._read_json_body()
        if not body or "prompt" not in body or "models" not in body:
            self._send_error_json(HTTPStatus.BAD_REQUEST, "Missing 'prompt' or 'models'")
            return

        prompt = body["prompt"]
        models = body["models"]
        system_prompt = body.get("system_prompt")

        try:
            results = query_models_parallel(
                prompt, models, self.api_key, system_prompt=system_prompt
            )
            self._send_json({"prompt": prompt, "responses": results})
        except Exception as exc:
            self._send_error_json(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    def _handle_council_stream(self):
        body = self._read_json_body()
        if not body or "prompt" not in body or "models" not in body:
            self._send_error_json(HTTPStatus.BAD_REQUEST, "Missing 'prompt' or 'models'")
            return

        prompt = body["prompt"]
        models = body["models"]
        system_prompt = body.get("system_prompt")

        # Set up SSE response
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self._set_cors_headers()
        self.end_headers()

        # query_models_stream is a sync generator that internally uses threads.
        # Run it in a background thread and relay events via queue.
        result_queue: Queue = Queue()
        sentinel = object()

        def _produce():
            try:
                for event in query_models_stream(
                    prompt, models, self.api_key, system_prompt=system_prompt
                ):
                    result_queue.put(event)
            except Exception as exc:
                result_queue.put({"model": "system", "status": "error", "content": str(exc), "token_count": 0})
            finally:
                result_queue.put(sentinel)

        thread = threading.Thread(target=_produce, daemon=True)
        thread.start()

        try:
            while True:
                item = result_queue.get(timeout=120)
                if item is sentinel:
                    break
                line = f"data: {json.dumps(item)}\n\n"
                self.wfile.write(line.encode())
                self.wfile.flush()
            # Send explicit done marker so the frontend knows the stream is finished
            self.wfile.write(b"data: {\"status\":\"done\"}\n\n")
            self.wfile.flush()
            # Give TCP stack time to send the final packets before socket closes
            time.sleep(0.2)
        except (Empty, BrokenPipeError, ConnectionResetError):
            pass
        finally:
            thread.join(timeout=5)

    def _handle_synthesize(self):
        body = self._read_json_body()
        if not body or "prompt" not in body or "responses" not in body:
            self._send_error_json(HTTPStatus.BAD_REQUEST, "Missing 'prompt' or 'responses'")
            return

        try:
            synthesis = synthesize_responses(
                body["prompt"], body["responses"], self.api_key
            )
            self._send_json({"synthesis": synthesis})
        except Exception as exc:
            self._send_error_json(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    def _handle_vote(self):
        """Run anonymous model vote via SSE stream to avoid proxy timeouts.

        Sends keepalive pings every 5 seconds while the voting runs in a
        background thread.  The final event contains the full result JSON.
        """
        body = self._read_json_body()
        if not body or "prompt" not in body or "responses" not in body:
            self._send_error_json(HTTPStatus.BAD_REQUEST, "Missing 'prompt' or 'responses'")
            return

        prompt = body["prompt"]
        responses = body["responses"]

        if len(responses) < 2:
            self._send_error_json(HTTPStatus.BAD_REQUEST, "Need at least 2 responses to vote")
            return

        # Set up SSE response so the proxy sees data flowing
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self._set_cors_headers()
        self.end_headers()

        # Run the vote in a background thread
        result_holder = {"result": None, "error": None}

        def _do_vote():
            try:
                result_holder["result"] = anonymous_model_vote(prompt, responses, self.api_key)
            except Exception as exc:
                result_holder["error"] = str(exc)

        vote_thread = threading.Thread(target=_do_vote, daemon=True)
        vote_thread.start()

        # Send keepalive pings every 5 seconds until the vote finishes
        try:
            while vote_thread.is_alive():
                self.wfile.write(b": keepalive\n\n")
                self.wfile.flush()
                vote_thread.join(timeout=5)

            # Send the final result
            if result_holder["error"]:
                event = {"status": "error", "error": result_holder["error"]}
            else:
                event = {"status": "done", "result": result_holder["result"]}
            self.wfile.write(f"data: {json.dumps(event)}\n\n".encode())
            self.wfile.flush()
            time.sleep(0.2)
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            vote_thread.join(timeout=5)

    def _handle_chairman(self):
        """Run chairman review via SSE stream to avoid proxy timeouts."""
        body = self._read_json_body()
        if not body or "prompt" not in body or "responses" not in body or "vote_results" not in body or "chairman_model" not in body:
            self._send_error_json(HTTPStatus.BAD_REQUEST, "Missing required fields")
            return

        prompt = body["prompt"]
        responses = body["responses"]
        vote_results = body["vote_results"]
        chairman_model = body["chairman_model"]

        # Set up SSE response
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self._set_cors_headers()
        self.end_headers()

        result_holder = {"result": None, "error": None}

        def _do_chairman():
            try:
                result_holder["result"] = chairman_review(
                    prompt, responses, vote_results, chairman_model, self.api_key
                )
            except Exception as exc:
                result_holder["error"] = str(exc)

        chairman_thread = threading.Thread(target=_do_chairman, daemon=True)
        chairman_thread.start()

        try:
            while chairman_thread.is_alive():
                self.wfile.write(b": keepalive\n\n")
                self.wfile.flush()
                chairman_thread.join(timeout=5)

            if result_holder["error"]:
                event = {"status": "error", "error": result_holder["error"]}
            else:
                event = {"status": "done", "result": result_holder["result"]}
            self.wfile.write(f"data: {json.dumps(event)}\n\n".encode())
            self.wfile.flush()
            time.sleep(0.2)
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            chairman_thread.join(timeout=5)

    # -- Suppress default logging noise ------------------------------------

    def log_message(self, format, *args):
        sys.stderr.write(f"[council] {args[0]} {args[1]} {args[2]}\n")


def run_server(port: int, api_key: str):
    """Start the HTTP server and block until interrupted."""
    handler = partial(CouncilRequestHandler, api_key=api_key)
    server = ThreadingHTTPServer(("0.0.0.0", port), handler)

    def _shutdown(signum, _frame):
        print(f"\nReceived signal {signum}, shutting down...")
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    print(f"LLM Council server running on http://localhost:{port}")
    print(f"Static files: {STATIC_DIR}")
    print(f"API key configured: {'yes' if api_key else 'NO (set AI_GATEWAY_API_KEY)'}")

    try:
        server.serve_forever()
    finally:
        server.server_close()
        print("Server stopped.")


if __name__ == "__main__":
    port = int(os.environ.get("COUNCIL_PORT", "8787"))
    api_key = os.environ.get("AI_GATEWAY_API_KEY", "")
    run_server(port, api_key)
