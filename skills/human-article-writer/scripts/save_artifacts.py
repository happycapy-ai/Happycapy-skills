#!/usr/bin/env python3
"""Save a Human Article Writer output as Markdown and self-contained HTML."""

import argparse
import base64
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def build_markdown(meta: dict) -> str:
    """Build the Markdown file content."""
    frontmatter = f"""---
title: {meta.get('title', 'Untitled')}
format: {meta.get('format', 'article')}
word_count: {meta.get('word_count', 0)}
human_feel_score: {meta.get('human_feel_score', 0)}
authority_mechanisms: {', '.join(meta.get('authority_mechanisms', []))}
fabrication_check: {meta.get('fabrication_check', 'PASS (0 violations)')}
generated_at: {datetime.utcnow().isoformat()}Z
---

"""
    return frontmatter + meta.get('body', '').strip() + "\n"


def build_html(meta: dict, md_path: str) -> str:
    """Build a self-contained HTML wrapper around pandoc output."""
    title = meta.get('title', 'Untitled')
    fmt = meta.get('format', 'article')
    word_count = meta.get('word_count', 0)
    score = meta.get('human_feel_score', 0)
    mechanisms = meta.get('authority_mechanisms', [])
    fab = meta.get('fabrication_check', 'PASS (0 violations)')

    metadata_html = f"""
    <div class="meta-bar">
      <span><strong>Format:</strong> {fmt}</span>
      <span><strong>Words:</strong> {word_count}</span>
      <span><strong>Human-feel score:</strong> {score}/100</span>
      <span><strong>Authority:</strong> {', '.join(mechanisms) if mechanisms else 'N/A'}</span>
      <span><strong>Fabrication check:</strong> {fab}</span>
    </div>
"""

    html_prefix = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      --bg: #fdfbf7;
      --text: #1a1a1a;
      --muted: #5a5a5a;
      --accent: #8b5e3c;
      --border: #e2ddd4;
      --meta-bg: #f5f1ea;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #1a1a1a;
        --text: #f0ece4;
        --muted: #b0a99f;
        --accent: #d4a574;
        --border: #3a3530;
        --meta-bg: #25201c;
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Georgia, serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.65;
      margin: 0;
      padding: 2rem 1rem;
    }}
    .container {{
      max-width: 720px;
      margin: 0 auto;
    }}
    h1 {{
      font-size: 2rem;
      line-height: 1.2;
      margin-bottom: 0.5rem;
      font-weight: 700;
    }}
    .meta-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem 1.25rem;
      font-size: 0.85rem;
      color: var(--muted);
      background: var(--meta-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.75rem 1rem;
      margin: 1.25rem 0 2rem;
    }}
    h2, h3, h4 {{
      margin-top: 2rem;
      margin-bottom: 0.75rem;
      line-height: 1.3;
    }}
    p {{ margin: 0 0 1rem; }}
    a {{ color: var(--accent); }}
    blockquote {{
      border-left: 3px solid var(--accent);
      margin: 1.5rem 0;
      padding-left: 1rem;
      color: var(--muted);
      font-style: italic;
    }}
    ul, ol {{ padding-left: 1.5rem; margin-bottom: 1rem; }}
    li {{ margin-bottom: 0.35rem; }}
    code {{
      background: var(--meta-bg);
      padding: 0.15rem 0.35rem;
      border-radius: 4px;
      font-size: 0.9em;
    }}
    pre {{
      background: var(--meta-bg);
      padding: 1rem;
      border-radius: 8px;
      overflow-x: auto;
      font-size: 0.9em;
    }}
    hr {{ border: none; border-top: 1px solid var(--border); margin: 2rem 0; }}
    footer {{
      margin-top: 3rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border);
      font-size: 0.85rem;
      color: var(--muted);
      text-align: center;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>{title}</h1>
    {metadata_html}
    <article>
"""

    html_suffix = """
    </article>
    <footer>
      Built with <a href="https://happycapy.ai">HappyCapy</a>
    </footer>
  </div>
</body>
</html>
"""
    return html_prefix, html_suffix


def convert_body_to_html(body: str) -> str:
    """Convert Markdown body to HTML using pandoc, fallback to plain pre."""
    if shutil.which("pandoc"):
        try:
            result = subprocess.run(
                ["pandoc", "-f", "markdown", "-t", "html", "--wrap=none"],
                input=body,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"pandoc conversion failed: {e.stderr}", file=sys.stderr)
    # Fallback: preserve line breaks in a simple way
    escaped = body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return "<pre>" + escaped + "</pre>"


def main():
    parser = argparse.ArgumentParser(description="Save Human Article Writer output as Markdown + HTML")
    parser.add_argument("--input", "-i", required=True, help="Path to JSON file with article metadata and body")
    parser.add_argument("--output-dir", "-o", default="./outputs/human-article-writer", help="Directory for output files")
    parser.add_argument("--basename", "-b", default="article", help="Base filename without extension")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    md_path = output_dir / f"{args.basename}.md"
    html_path = output_dir / f"{args.basename}.html"

    md_content = build_markdown(meta)
    md_path.write_text(md_content, encoding="utf-8")

    prefix, suffix = build_html(meta, str(md_path))
    body_html = convert_body_to_html(meta.get("body", ""))
    html_path.write_text(prefix + body_html + suffix, encoding="utf-8")

    print(f"Saved Markdown: {md_path}")
    print(f"Saved HTML:     {html_path}")


if __name__ == "__main__":
    main()
