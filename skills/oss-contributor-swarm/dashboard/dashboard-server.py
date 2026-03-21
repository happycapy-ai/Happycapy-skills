#!/usr/bin/env python3
"""
OSS Contributor Swarm - PR Dashboard Server

A simple HTTP server that serves the PR dashboard and provides
API endpoints for contribution data.

Usage:
    python dashboard-server.py [--port PORT]

Default port: 8081
"""

import argparse
import json
import os
import sys
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Configuration
DEFAULT_PORT = 8081
DASHBOARD_DIR = Path(__file__).parent.resolve()
SHARED_DIR = DASHBOARD_DIR.parent / "shared"
DATA_FILE = SHARED_DIR / "contribution-history.json"


class DashboardHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for the PR dashboard."""

    def __init__(self, *args, **kwargs):
        # Set the directory to serve files from
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # API endpoints
        if path == "/api/data":
            self.handle_api_data()
        elif path == "/api/stats":
            self.handle_api_stats()
        elif path == "/api/contributions":
            self.handle_api_contributions(parsed_path)
        elif path == "/api/health":
            self.handle_api_health()
        elif path == "/" or path == "":
            # Serve the dashboard HTML
            self.path = "/pr-dashboard.html"
            super().do_GET()
        else:
            # Serve static files
            super().do_GET()

    def handle_api_data(self):
        """Return all contribution data."""
        data = self.load_data()
        self.send_json_response(data)

    def handle_api_stats(self):
        """Return statistics only."""
        data = self.load_data()
        stats = data.get("stats", {})

        # Calculate additional stats
        contributions = data.get("contributions", [])
        if contributions:
            # Language distribution
            lang_counts = {}
            for c in contributions:
                lang = c.get("language", "Unknown")
                lang_counts[lang] = lang_counts.get(lang, 0) + 1
            stats["languages"] = lang_counts

            # Type distribution
            type_counts = {}
            for c in contributions:
                t = c.get("type", "other")
                type_counts[t] = type_counts.get(t, 0) + 1
            stats["types"] = type_counts

            # Status distribution
            status_counts = {"MERGED": 0, "OPEN": 0, "CLOSED": 0}
            for c in contributions:
                status = c.get("status", "").upper()
                if status in status_counts:
                    status_counts[status] += 1
            stats["status_distribution"] = status_counts

        self.send_json_response(stats)

    def handle_api_contributions(self, parsed_path):
        """Return filtered contributions."""
        data = self.load_data()
        contributions = data.get("contributions", [])

        # Parse query parameters
        query = parse_qs(parsed_path.query)

        # Filter by status
        status = query.get("status", [None])[0]
        if status:
            contributions = [c for c in contributions
                          if c.get("status", "").upper() == status.upper()]

        # Filter by type
        type_filter = query.get("type", [None])[0]
        if type_filter:
            contributions = [c for c in contributions
                          if c.get("type", "").lower() == type_filter.lower()]

        # Filter by language
        language = query.get("language", [None])[0]
        if language:
            contributions = [c for c in contributions
                          if c.get("language", "").lower() == language.lower()]

        # Filter by repository (partial match)
        repo = query.get("repo", [None])[0]
        if repo:
            contributions = [c for c in contributions
                          if repo.lower() in c.get("repository", "").lower()]

        # Sort by cycle (most recent first)
        contributions.sort(key=lambda x: x.get("cycle", 0), reverse=True)

        # Pagination
        try:
            offset = int(query.get("offset", [0])[0])
            limit = int(query.get("limit", [100])[0])
        except ValueError:
            offset, limit = 0, 100

        total = len(contributions)
        contributions = contributions[offset:offset + limit]

        response = {
            "contributions": contributions,
            "total": total,
            "offset": offset,
            "limit": limit
        }
        self.send_json_response(response)

    def handle_api_health(self):
        """Health check endpoint."""
        data_exists = DATA_FILE.exists()
        response = {
            "status": "healthy" if data_exists else "degraded",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data_file": str(DATA_FILE),
            "data_exists": data_exists
        }
        self.send_json_response(response)

    def load_data(self):
        """Load contribution data from JSON file."""
        if not DATA_FILE.exists():
            return self.get_empty_data()

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading data file: {e}", file=sys.stderr)
            return self.get_empty_data()

    def get_empty_data(self):
        """Return empty data structure."""
        return {
            "schema_version": "1.0.0",
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "stats": {
                "total_contributions": 0,
                "prs_created": 0,
                "prs_merged": 0,
                "prs_closed": 0,
                "prs_pending": 0,
                "cycles_completed": 0
            },
            "contributions": [],
            "languages_contributed": [],
            "contribution_types": []
        }

    def send_json_response(self, data, status=200):
        """Send a JSON response."""
        response_body = json.dumps(data, indent=2, ensure_ascii=False)
        response_bytes = response_body.encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(response_bytes)

    def log_message(self, format, *args):
        """Custom log formatting."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {args[0]}")


def run_server(port: int = DEFAULT_PORT):
    """Start the HTTP server."""
    server_address = ("", port)
    httpd = HTTPServer(server_address, DashboardHandler)

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  OSS Contributor Swarm - PR Dashboard Server                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Dashboard: http://localhost:{port:<5}                         ║
║                                                              ║
║  API Endpoints:                                              ║
║    GET /api/data          - All contribution data            ║
║    GET /api/stats         - Statistics summary               ║
║    GET /api/contributions - Filtered contributions           ║
║    GET /api/health        - Health check                     ║
║                                                              ║
║  Query Parameters for /api/contributions:                    ║
║    ?status=MERGED|OPEN|CLOSED                                ║
║    ?type=documentation|bug|feature|...                       ║
║    ?language=TypeScript|Python|Go|...                        ║
║    ?repo=partial-match                                       ║
║    ?offset=0&limit=100                                       ║
║                                                              ║
║  Data Source: {str(DATA_FILE)[:40]:<40} ║
║                                                              ║
║  Press Ctrl+C to stop the server                             ║
╚══════════════════════════════════════════════════════════════╝
""")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()
        print("Server stopped.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="OSS Contributor Swarm - PR Dashboard Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dashboard-server.py                 # Start on default port 8081
  python dashboard-server.py --port 8080     # Start on port 8080
  python dashboard-server.py -p 3000         # Start on port 3000
        """
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to run the server on (default: {DEFAULT_PORT})"
    )
    parser.add_argument(
        "--data-file",
        type=str,
        default=None,
        help="Path to contribution history JSON file"
    )

    args = parser.parse_args()

    # Override data file path if specified
    global DATA_FILE
    if args.data_file:
        DATA_FILE = Path(args.data_file).resolve()

    # Validate port
    if not (1 <= args.port <= 65535):
        print(f"Error: Port must be between 1 and 65535", file=sys.stderr)
        sys.exit(1)

    run_server(args.port)


if __name__ == "__main__":
    main()
