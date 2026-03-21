#!/usr/bin/env python3
"""Capy Cortex Observatory - Dashboard Server.
Zero-dependency Python server. Reads cortex.db, serves HTML + JSON API.
"""

import http.server
import json
import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent / "cortex.db"
HTML_PATH = Path(__file__).parent / "dashboard.html"
PORT = 8787


def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA busy_timeout=3000")
    return db


def get_cortex_data():
    db = get_db()
    data = {}

    # Summary counts
    data['summary'] = {
        'rules': db.execute('SELECT COUNT(*) FROM rules').fetchone()[0],
        'principles': db.execute('SELECT COUNT(*) FROM principles').fetchone()[0],
        'anti_patterns': db.execute('SELECT COUNT(*) FROM anti_patterns').fetchone()[0],
        'preferences': db.execute('SELECT COUNT(*) FROM preferences').fetchone()[0],
        'diary_entries': db.execute('SELECT COUNT(*) FROM diary').fetchone()[0],
        'events': db.execute('SELECT COUNT(*) FROM events').fetchone()[0],
        'db_size_kb': round(os.path.getsize(str(DB_PATH)) / 1024),
        'tfidf_dirty': db.execute("SELECT value FROM meta WHERE key='tfidf_dirty'").fetchone()[0] == '1',
    }

    # Compute health score (0-100)
    s = data['summary']
    health = 0
    health += 25 if not s['tfidf_dirty'] else 5
    health += min(25, s['rules'] / 40)  # 25 pts at 1000+ rules
    health += min(25, s['principles'] * 2.5)  # 25 pts at 10+ principles
    health += 25 if s['anti_patterns'] < 100 else 10
    data['summary']['health_score'] = min(round(health), 100)

    # Rules by category
    rows = db.execute('SELECT category, COUNT(*) as cnt FROM rules GROUP BY category ORDER BY cnt DESC').fetchall()
    data['rules_by_category'] = {r['category']: r['cnt'] for r in rows}

    # Rules by maturity
    rows = db.execute('SELECT maturity, COUNT(*) as cnt FROM rules GROUP BY maturity').fetchall()
    data['rules_by_maturity'] = {r['maturity']: r['cnt'] for r in rows}

    # Confidence distribution
    buckets = [(0, 0.2, '0-0.2'), (0.2, 0.4, '0.2-0.4'), (0.4, 0.6, '0.4-0.6'),
               (0.6, 0.8, '0.6-0.8'), (0.8, 1.01, '0.8-1.0')]
    data['confidence_dist'] = {}
    for lo, hi, label in buckets:
        cnt = db.execute('SELECT COUNT(*) FROM rules WHERE confidence >= ? AND confidence < ?', (lo, hi)).fetchone()[0]
        data['confidence_dist'][label] = cnt

    # Events by type
    rows = db.execute('SELECT event_type, COUNT(*) as cnt FROM events GROUP BY event_type ORDER BY cnt DESC').fetchall()
    data['events_by_type'] = {r['event_type']: r['cnt'] for r in rows}

    # Anti-patterns by severity
    rows = db.execute('SELECT severity, COUNT(*) as cnt FROM anti_patterns GROUP BY severity').fetchall()
    data['ap_by_severity'] = {r['severity']: r['cnt'] for r in rows}

    # Events timeline
    rows = db.execute(
        "SELECT strftime('%Y-%m-%d', created_at) as day, event_type, COUNT(*) as cnt "
        "FROM events GROUP BY day, event_type ORDER BY day"
    ).fetchall()
    timeline = {}
    for r in rows:
        day = r['day']
        if day not in timeline:
            timeline[day] = {'date': day, 'total': 0}
        timeline[day]['total'] += r['cnt']
        timeline[day][r['event_type']] = r['cnt']
    data['events_timeline'] = list(timeline.values())

    # Recent events
    rows = db.execute('SELECT event_type, created_at, metadata FROM events ORDER BY created_at DESC LIMIT 20').fetchall()
    data['recent_events'] = [{'type': r['event_type'], 'time': r['created_at'], 'meta': r['metadata'][:200]} for r in rows]

    # Top principles
    rows = db.execute('SELECT content, confidence, occurrences FROM principles ORDER BY confidence DESC, occurrences DESC LIMIT 12').fetchall()
    data['top_principles'] = [{'content': r['content'][:250], 'confidence': r['confidence'], 'occurrences': r['occurrences']} for r in rows]

    # Recent rules
    rows = db.execute('SELECT content, category, confidence, occurrences, created_at FROM rules ORDER BY created_at DESC LIMIT 12').fetchall()
    data['recent_rules'] = [{'content': r['content'][:150], 'category': r['category'],
                             'confidence': r['confidence'], 'occurrences': r['occurrences'],
                             'time': r['created_at']} for r in rows]

    # Anti-patterns list
    rows = db.execute('SELECT content, severity, occurrences FROM anti_patterns ORDER BY severity DESC, occurrences DESC').fetchall()
    data['anti_patterns_list'] = [{'content': r['content'][:250], 'severity': r['severity'],
                                   'occurrences': r['occurrences']} for r in rows]

    # Preferences list
    rows = db.execute('SELECT content, occurrences FROM preferences ORDER BY occurrences DESC').fetchall()
    data['preferences_list'] = [{'content': r['content'][:250], 'occurrences': r['occurrences']} for r in rows]

    # Recent diary
    rows = db.execute('SELECT summary, created_at FROM diary ORDER BY created_at DESC LIMIT 8').fetchall()
    data['recent_diary'] = [{'summary': r['summary'][:300], 'time': r['created_at']} for r in rows]

    db.close()
    return data


class CortexHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self._serve_html()
        elif self.path == '/api/data':
            self._serve_json()
        else:
            self.send_error(404)

    def _serve_html(self):
        try:
            html = HTML_PATH.read_text()
        except FileNotFoundError:
            self.send_error(500, "dashboard.html not found")
            return
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def _serve_json(self):
        try:
            data = get_cortex_data()
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
            return
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass  # Silent


if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', PORT), CortexHandler)
    print(f"Capy Cortex Observatory running on http://0.0.0.0:{PORT}")
    print(f"Database: {DB_PATH} ({os.path.getsize(str(DB_PATH)) / 1024:.0f}KB)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")
        server.server_close()
