#!/usr/bin/env python3
"""Estimate how long a video segment should be so its Gemini Omni Flash
voiceover has time to speak the given line naturally, plus enough headroom
for the paper-collage assemble-from-empty motion to read clearly.

Formula (fixed by design, not meant to be tuned per-run):
  zh: char_count / 4.0 chars-per-second   (ad-voiceover pace, not casual reading)
  en: word_count / 2.3 words-per-second
  + 1.5s buffer for the assembly motion to land
  clamped to [5, 10] seconds (5 = minimum for 3-6 paper groups to read clearly,
  10 = Gemini Omni Flash's documented ceiling for a single generation)
  rounded to the nearest whole second (the API only accepts integer seconds)

If the raw (unclamped) estimate exceeds 10s, that line is too long for one
segment and should be split into two segments upstream, before calling this
script — check the "raw_seconds" field in the output for that decision.

Usage:
  python3 estimate_duration.py "台词文本" [--lang zh|en|auto]

Prints a single JSON line: {"seconds": 7, "raw_seconds": 6.8, "lang": "zh", "needs_split": false}
"""

import argparse
import json
import re
import sys

CHARS_PER_SECOND_ZH = 4.0
WORDS_PER_SECOND_EN = 2.3
BUFFER_SECONDS = 1.5
MIN_SECONDS = 5
MAX_SECONDS = 10

CJK_RE = re.compile(r'[一-鿿㐀-䶿]')


def detect_lang(text):
    cjk_count = len(CJK_RE.findall(text))
    return "zh" if cjk_count >= max(1, len(text.strip()) * 0.3) else "en"


def estimate_raw_seconds(text, lang):
    if lang == "zh":
        char_count = len(CJK_RE.findall(text))
        return char_count / CHARS_PER_SECOND_ZH + BUFFER_SECONDS
    words = [w for w in re.split(r'\s+', text.strip()) if w]
    return len(words) / WORDS_PER_SECOND_EN + BUFFER_SECONDS


def main():
    parser = argparse.ArgumentParser(description="Estimate Omni segment duration from voiceover text")
    parser.add_argument("text")
    parser.add_argument("--lang", choices=["zh", "en", "auto"], default="auto")
    args = parser.parse_args()

    lang = detect_lang(args.text) if args.lang == "auto" else args.lang
    raw_seconds = estimate_raw_seconds(args.text, lang)
    needs_split = raw_seconds > MAX_SECONDS
    clamped = max(MIN_SECONDS, min(MAX_SECONDS, raw_seconds))
    seconds = round(clamped)

    print(json.dumps({
        "seconds": seconds,
        "raw_seconds": round(raw_seconds, 2),
        "lang": lang,
        "needs_split": needs_split,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
