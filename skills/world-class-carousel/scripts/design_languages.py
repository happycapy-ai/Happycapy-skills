#!/usr/bin/env python3
"""
10 Category Design Languages -- 7-Axis Perceptual Differentiation System

Each design language varies across 7 independent axes:
  1. COLOR PALETTE (bg, text, accent, secondary, gradient)
  2. LAYOUT GEOMETRY (alignment, margins, card style)
  3. TYPOGRAPHY (font family, weight, size ratios, spacing)
  4. DECORATIVE GRAMMAR (corners, borders, patterns, dividers)
  5. INFORMATION DENSITY (spacing, whitespace ratio)
  6. DEPTH MODEL (flat, shadows, glass, layered)
  7. VISUAL RHYTHM (grid, organic, progressive, alternating)

Constraint: No two categories share values on more than 2 of 7 axes.
"""

DESIGN_LANGUAGES = {
    # ============================================================
    # 1. PAPER DECODER -- Academic journal / Nature / Science
    # Precedent: Scientific journal articles
    # ============================================================
    "paper_decoder": {
        "name": "Paper Decoder",
        "theme": {
            "bg_fallback": "F8F5F0",      # Warm ivory
            "accent": "1A3A5C",            # Deep navy
            "accent_light": "4A7BA7",      # Steel blue
            "dark": "1A1A2E",              # Near-black text
            "mid": "5C6370",              # Scholarly gray
            "light": "E8E2D8",            # Warm light
            "label_bg": "1A3A5C",
            "label_text": "FFFFFF",
            "card_bg": "FFFEF8",          # Paper white
        },
        "brand": {
            "font_serif": "newpxtext",     # Palatino-like serif
            "corner_radius": "3pt",        # Small, academic
            "header_style": "italic",      # Journal style
            "divider_style": "line",       # Thin rules
            "nav_style": "circle",
        },
        "bg_pattern": "dots",             # Subtle dot grid (lab paper)
        "bullet_style": "square",         # Academic square bullets
        "title_treatment": "underline",   # Thin rule under title
        "depth": "flat",                  # Clean, no shadows
        "density": "airy",               # Generous whitespace
    },

    # ============================================================
    # 2. TOOL SHOWDOWN -- ESPN Scorecard / Competition broadcast
    # Precedent: Sports analytics, match broadcasts
    # ============================================================
    "tool_showdown": {
        "name": "Tool Showdown",
        "theme": {
            "bg_fallback": "0A0A14",       # Near-black
            "accent": "FF6B2C",            # Hot orange
            "accent_light": "FF9966",
            "dark": "F0F0F5",              # White text
            "mid": "9CA3AF",
            "light": "1E1E2E",
            "label_bg": "FF6B2C",
            "label_text": "FFFFFF",
            "card_bg": "141420",           # Dark card
        },
        "brand": {
            "font_serif": "roboto",        # Bold geometric sans
            "corner_radius": "0pt",        # SHARP angular
            "header_style": "bold",
            "divider_style": "none",       # No dividers, pure contrast
            "nav_style": "arrow",
        },
        "bg_pattern": "diagonal_stripes",  # Sport energy
        "accent_secondary": "8B5CF6",     # Purple for versus
        "bullet_style": "arrow",          # Competitive arrows
        "title_treatment": "boxed_accent",
        "depth": "layered",               # Heavy shadows
        "density": "dense",               # Packed info
    },

    # ============================================================
    # 3. BREAKING NEWS -- CNN Ticker / BBC News
    # Precedent: News broadcast, urgency alerts
    # ============================================================
    "breaking_news": {
        "name": "Breaking News",
        "theme": {
            "bg_fallback": "0C0C0C",       # Pure dark
            "accent": "DC2626",            # Urgent red
            "accent_light": "F87171",
            "dark": "FFFFFF",              # Pure white text
            "mid": "A1A1AA",
            "light": "27272A",
            "label_bg": "DC2626",
            "label_text": "FFFFFF",
            "card_bg": "18181B",
        },
        "brand": {
            "font_serif": "helvet",        # Helvetica / condensed
            "corner_radius": "0pt",        # Sharp -- news style
            "header_style": "bold",
            "divider_style": "line",       # Horizontal rules like ticker
            "nav_style": "none",           # No nav -- urgency, no time
        },
        "bg_pattern": "scanlines",        # Broadcast scan lines
        "bullet_style": "dash",           # News-style dashes
        "title_treatment": "uppercase",   # ALL CAPS headlines
        "depth": "flat",                  # Clean broadcast
        "density": "tight",              # Dense news
    },

    # ============================================================
    # 4. TOOL TUTORIAL -- Notion / Apple HIG / Friendly guide
    # Precedent: iOS design, children's textbook, Duolingo
    # ============================================================
    "tool_tutorial": {
        "name": "Tool Tutorial",
        "theme": {
            "bg_fallback": "F0FDF4",       # Mint cream
            "accent": "16A34A",            # Fresh green
            "accent_light": "86EFAC",
            "dark": "14532D",              # Forest dark
            "mid": "4B7A5B",
            "light": "DCFCE7",
            "label_bg": "16A34A",
            "label_text": "FFFFFF",
            "card_bg": "FFFFFF",           # Pure white cards
        },
        "brand": {
            "font_serif": "cabin",         # Friendly humanist sans
            "corner_radius": "12pt",       # LARGE pill radius
            "header_style": "bold",
            "divider_style": "dots",       # Friendly dots
            "nav_style": "circle",
        },
        "bg_pattern": "none",             # Clean, no pattern
        "bullet_style": "checkmark",      # Tutorial checkmarks
        "title_treatment": "pill_badge",  # Rounded pill highlight
        "depth": "subtle",               # Light shadows
        "density": "generous",           # Lots of breathing room
    },

    # ============================================================
    # 5. HOT TAKE -- Protest poster / Warning sign / Punk zine
    # Precedent: Saul Bass, Barbara Kruger, punk rock design
    # ============================================================
    "hot_take": {
        "name": "Hot Take",
        "theme": {
            "bg_fallback": "1C1917",       # Charcoal warm
            "accent": "EAB308",            # Warning yellow
            "accent_light": "FDE047",
            "dark": "FAFAF9",              # Off-white text
            "mid": "A8A29E",
            "light": "292524",
            "label_bg": "EAB308",
            "label_text": "000000",        # BLACK on yellow
            "card_bg": "292524",
        },
        "brand": {
            "font_serif": "avant",         # Heavy avant-garde geometric
            "corner_radius": "0pt",        # SHARP -- confrontational
            "header_style": "bold",
            "divider_style": "none",
            "nav_style": "arrow",
        },
        "bg_pattern": "diagonal_warning",  # Warning stripe
        "bullet_style": "exclamation",    # ! marks
        "title_treatment": "reversed_bar", # White-on-yellow reversed
        "depth": "flat",                  # Bold graphic design
        "density": "medium",
    },

    # ============================================================
    # 6. PROMPT PLAYBOOK -- Terminal / Recipe card / Moleskin
    # Precedent: Code editors, recipe cards, field notebooks
    # ============================================================
    "prompt_playbook": {
        "name": "Prompt Playbook",
        "theme": {
            "bg_fallback": "FDF6E3",       # Solarized cream
            "accent": "B45309",            # Warm amber/rust
            "accent_light": "D97706",
            "dark": "3C2415",              # Dark sepia
            "mid": "78716C",
            "light": "E7E0D5",
            "label_bg": "B45309",
            "label_text": "FFFFFF",
            "card_bg": "F5EDDF",           # Warm card
        },
        "brand": {
            "font_serif": "inconsolata",   # Monospace / terminal
            "corner_radius": "2pt",        # Minimal
            "header_style": "plain",       # No italic -- practical
            "divider_style": "dots",       # Dotted notebook lines
            "nav_style": "circle",
        },
        "bg_pattern": "ruled_lines",       # Notebook ruled paper
        "bullet_style": "number",         # Numbered steps
        "title_treatment": "code_block",  # Terminal-style box
        "depth": "subtle",               # Light notebook shadow
        "density": "reference",          # Dense reference material
    },

    # ============================================================
    # 7. INDUSTRY MAP -- Bloomberg / Situation room / Dashboard
    # Precedent: Financial terminal, military CIC, McKinsey decks
    # ============================================================
    "industry_map": {
        "name": "Industry Map",
        "theme": {
            "bg_fallback": "0F1729",       # Dark navy
            "accent": "3B82F6",            # Signal blue
            "accent_light": "93C5FD",
            "dark": "E2E8F0",              # Light gray text
            "mid": "64748B",
            "light": "1E293B",
            "label_bg": "3B82F6",
            "label_text": "FFFFFF",
            "card_bg": "1E293B",
        },
        "brand": {
            "font_serif": "opensans",      # Clean technical sans
            "corner_radius": "2pt",        # Tiny -- technical
            "header_style": "plain",
            "divider_style": "line",       # Grid lines
            "nav_style": "none",
        },
        "accent_secondary": "10B981",     # Green for data
        "accent_tertiary": "F59E0B",      # Amber for highlights
        "bg_pattern": "grid",             # Data grid background
        "bullet_style": "dot_colored",    # Multi-color dots
        "title_treatment": "thin_caps",   # Small caps, thin
        "depth": "layered",              # Dashboard layers
        "density": "dense",              # Packed data
    },

    # ============================================================
    # 8. BUILD THIS -- Blueprint / Architecture portfolio
    # Precedent: Technical drawing, Figma, wireframe
    # ============================================================
    "build_this": {
        "name": "Build This",
        "theme": {
            "bg_fallback": "F8FAFC",       # Near-white
            "accent": "0D9488",            # Teal
            "accent_light": "5EEAD4",
            "dark": "0F172A",              # Dark text
            "mid": "64748B",
            "light": "E2E8F0",
            "label_bg": "0D9488",
            "label_text": "FFFFFF",
            "card_bg": "FFFFFF",
        },
        "brand": {
            "font_serif": "charter",       # Clean geometric charter
            "corner_radius": "4pt",
            "header_style": "bold",
            "divider_style": "line",
            "nav_style": "circle",
        },
        "bg_pattern": "blueprint_grid",   # Blueprint grid lines
        "bullet_style": "arrow_right",    # Forward arrows
        "title_treatment": "badge_teal",  # Teal badge
        "depth": "subtle",               # Clean with light shadow
        "density": "balanced",
    },

    # ============================================================
    # 9. FOUNDERS & MONEY -- Financial Times / WSJ / Bloomberg
    # Precedent: Financial press, annual reports, investor decks
    # ============================================================
    "founders_money": {
        "name": "Founders & Money",
        "theme": {
            "bg_fallback": "FFFBF0",       # Financial off-white
            "accent": "166534",            # Money green
            "accent_light": "4ADE80",
            "dark": "1A1A1A",              # True black text
            "mid": "525252",
            "light": "E5E5E5",
            "label_bg": "166534",
            "label_text": "FFFFFF",
            "card_bg": "FEF9EF",           # Cream card
        },
        "brand": {
            "font_serif": "newpxtext",     # Elegant serif (FT style)
            "corner_radius": "1pt",        # Hairline
            "header_style": "italic",      # Classic editorial
            "divider_style": "ornament",   # Ornamental dividers
            "nav_style": "circle",
        },
        "accent_secondary": "CA8A04",     # Gold accent
        "bg_pattern": "none",             # Clean -- luxury
        "bullet_style": "diamond",        # Diamond bullets
        "title_treatment": "serif_rule",  # Thin rule, serif
        "depth": "flat",                  # Elegant flat
        "density": "balanced",
    },

    # ============================================================
    # 10. FUTURE SCENARIO -- Planetarium / Apple keynote / Cosmos
    # Precedent: Space documentary, Apple product launches
    # ============================================================
    "future_scenario": {
        "name": "Future Scenario",
        "theme": {
            "bg_fallback": "0C0A1D",       # Deep space purple
            "accent": "A78BFA",            # Soft violet
            "accent_light": "C4B5FD",
            "dark": "F5F3FF",              # Lavender white
            "mid": "8B8CA0",
            "light": "1E1B3A",
            "label_bg": "7C3AED",
            "label_text": "FFFFFF",
            "card_bg": "1A1740",           # Deep indigo card
        },
        "brand": {
            "font_serif": "bookman",       # Elegant readable serif
            "corner_radius": "10pt",       # Soft, rounded
            "header_style": "plain",       # Minimal
            "divider_style": "none",       # No dividers -- floating
            "nav_style": "circle",
        },
        "accent_secondary": "2DD4BF",     # Teal accent
        "bg_pattern": "aurora",           # Gradient aurora
        "bullet_style": "circle_glow",    # Glowing circles
        "title_treatment": "glow_text",   # Subtle text glow
        "depth": "glass",                # Glass morphism
        "density": "airy",               # Maximum breathing room
    },
}

# Perceptual distance verification matrix
AXES = ["bg_tone", "font_style", "card_shape", "corners", "density", "depth", "accent_hue"]
AXIS_VALUES = {
    "paper_decoder":   ["warm-light", "serif",     "outlined",   "small",   "airy",      "flat",     "navy"],
    "tool_showdown":   ["dark",       "bold-sans",  "angular",    "none",    "dense",     "layered",  "orange"],
    "breaking_news":   ["dark",       "condensed",  "ruled",      "none",    "tight",     "flat",     "red"],
    "tool_tutorial":   ["light-mint", "rounded",    "pill-card",  "large",   "generous",  "subtle",   "green"],
    "hot_take":        ["warm-dark",  "heavy",      "reversed",   "none",    "medium",    "flat",     "yellow"],
    "prompt_playbook": ["warm-cream", "mono",       "terminal",   "tiny",    "reference", "subtle",   "amber"],
    "industry_map":    ["dark-navy",  "light-sans", "grid",       "tiny",    "dense",     "layered",  "blue"],
    "build_this":      ["near-white", "geometric",  "outlined",   "small",   "balanced",  "subtle",   "teal"],
    "founders_money":  ["off-white",  "elegant-serif","bordered", "hairline","balanced",  "flat",     "green-gold"],
    "future_scenario": ["deep-space", "light-airy", "glass",      "large",   "airy",      "glass",    "violet"],
}

def verify_distance():
    """Check no two categories share more than 2 axis values."""
    cats = list(AXIS_VALUES.keys())
    violations = []
    for i in range(len(cats)):
        for j in range(i+1, len(cats)):
            shared = sum(1 for a, b in zip(AXIS_VALUES[cats[i]], AXIS_VALUES[cats[j]]) if a == b)
            if shared > 2:
                violations.append((cats[i], cats[j], shared))
    return violations

if __name__ == "__main__":
    violations = verify_distance()
    if violations:
        print("DISTANCE VIOLATIONS:")
        for a, b, n in violations:
            print(f"  {a} <-> {b}: {n} shared axes")
    else:
        print("ALL PAIRS: max 2 shared axes -- PASS")

    print(f"\n{len(DESIGN_LANGUAGES)} design languages defined")
    for key, dl in DESIGN_LANGUAGES.items():
        print(f"  {key}: {dl['theme']['accent']} accent, {dl['brand']['font_serif']} font, "
              f"r={dl['brand']['corner_radius']}, depth={dl['depth']}, density={dl['density']}")
