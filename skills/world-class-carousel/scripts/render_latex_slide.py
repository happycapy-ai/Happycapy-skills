#!/usr/bin/env python3
"""
World-Class LaTeX Carousel Slide Renderer v6

Production-grade design system: real shadows, gradient fills, grain overlays,
depth hierarchy, and Instagram-optimized post-processing. Every pixel intentional.

Key improvements over v5:
  - Real TikZ drop shadows (shadows + shadows.blur libraries)
  - Gradient label fills via top/bottom shading
  - Grain/noise overlay in post-processing (PIL)
  - Unsharp mask sharpening for Instagram compression
  - Subtle vignette for depth
  - Color grading (saturation + contrast boost)
  - Multi-layer shadow system (ambient + contact)
  - Better decorative elements (subtle patterns, layered geometry)
  - Text shadow behind titles for legibility and polish

Slide Types:
  hook        -- Title + highlighted phrase + subtitle + optional full-bleed AI bg
  tool        -- #N Tool Name + description + screenshot + brand logo
  comparison  -- Multi-column comparison table (up to 3 columns)
  diagram     -- Text + TikZ flow diagram (vertical/horizontal/radial)
  body        -- Title + body text + bullets + optional AI accent
  synthesis   -- Styled numbered points with badges (save-worthy)
  cta         -- Call to action with handle + optional AI background

Usage:
  python3 render_latex_slide.py --type tool --data '{...}' --output slide.png
  python3 render_latex_slide.py --type hook --data '{...}' --brand brand.json --output slide.png
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# === CONSTANTS ===
SLIDE_W_CM = 15.0
SLIDE_H_CM = 18.75
MARGIN_CM = 1.2
DPI = 300
FINAL_W = 1080
FINAL_H = 1350

# === COLOR THEMES (defaults, can be overridden by brand config) ===
THEMES = {
    "warm": {
        "bg_fallback": "F5EFE6",
        "accent": "C1512D",
        "accent_light": "E8A390",
        "dark": "2D1B0E",
        "mid": "6B5B4B",
        "light": "D4CCBF",
        "label_bg": "C1512D",
        "label_text": "FFFFFF",
        "card_bg": "EDE6DA",
        "divider_ornament": True,
    },
    "clean": {
        "bg_fallback": "FFFFFF",
        "accent": "2563EB",
        "accent_light": "93C5FD",
        "dark": "0F172A",
        "mid": "475569",
        "light": "E2E8F0",
        "label_bg": "2563EB",
        "label_text": "FFFFFF",
        "card_bg": "F1F5F9",
        "divider_ornament": False,
    },
    "dark": {
        "bg_fallback": "0D1117",
        "accent": "7C3AED",
        "accent_light": "A78BFA",
        "dark": "E6EDF3",
        "mid": "8B949E",
        "light": "30363D",
        "label_bg": "7C3AED",
        "label_text": "FFFFFF",
        "card_bg": "161B22",
        "divider_ornament": False,
    },
    "earth": {
        "bg_fallback": "F5F0EB",
        "accent": "8B6914",
        "accent_light": "D4A843",
        "dark": "2D2416",
        "mid": "6B5B3E",
        "light": "E8DFD5",
        "label_bg": "8B6914",
        "label_text": "FFFFFF",
        "card_bg": "EDE5D8",
        "divider_ornament": True,
    },
}

# Default brand config
DEFAULT_BRAND = {
    "name": "Your Brand",
    "logo": None,          # Path to brand logo image
    "theme": "warm",
    "texture": None,        # Path to paper texture
    "accent_override": None,  # Override accent color hex
    "font_serif": "newpxtext",  # LaTeX serif package
    "font_sans": None,      # Optional sans package
    "header_style": "italic",  # italic, bold, or plain
    "nav_style": "circle",    # circle, arrow, none
    "divider_style": "line",  # line, ornament, dots, none
    "corner_radius": "5pt",   # Rounded corner radius for labels
}


def load_brand_config(brand_path):
    """Load brand configuration from JSON file."""
    if brand_path and os.path.exists(brand_path):
        with open(brand_path) as f:
            config = json.load(f)
        # Merge with defaults
        merged = DEFAULT_BRAND.copy()
        merged.update(config)
        return merged
    return DEFAULT_BRAND.copy()


def escape_latex(text):
    """Escape special LaTeX characters in user text."""
    if not text:
        return ""
    replacements = [
        ("\\", "\\textbackslash{}"),
        ("&", "\\&"),
        ("%", "\\%"),
        ("$", "\\$"),
        ("#", "\\#"),
        ("_", "\\_"),
        ("{", "\\{"),
        ("}", "\\}"),
        ("~", "\\textasciitilde{}"),
        ("^", "\\textasciicircum{}"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def get_theme(theme_name, brand_config=None):
    """Get theme colors, optionally with brand overrides."""
    theme = THEMES.get(theme_name, THEMES["warm"]).copy()
    if brand_config and brand_config.get("accent_override"):
        theme["accent"] = brand_config["accent_override"]
        theme["label_bg"] = brand_config["accent_override"]
    return theme


def generate_preamble(theme_name="warm", brand_config=None):
    """Generate the LaTeX preamble with all required packages."""
    theme = get_theme(theme_name, brand_config)
    bc = brand_config or DEFAULT_BRAND
    font_pkg = bc.get("font_serif", "newpxtext")
    corner_r = bc.get("corner_radius", "5pt")

    return rf"""\documentclass[border=0pt]{{standalone}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{{font_pkg}}}
\usepackage[protrusion=true,expansion=false]{{microtype}}
\usepackage{{graphicx}}
\usepackage{{tikz}}
\usepackage{{xcolor}}
\usepackage{{calc}}
\usepackage{{ifthen}}
\usepackage{{enumitem}}
\usetikzlibrary{{positioning,arrows.meta,shapes.geometric,backgrounds,fit,calc,decorations.pathreplacing,patterns,shadings,shadows,shadows.blur,fadings}}

% Kill ugly hyphenation
\hyphenpenalty=10000
\exhyphenpenalty=10000
\tolerance=1000
\emergencystretch=3em
\sloppy

\newlength{{\slideW}}\setlength{{\slideW}}{{{SLIDE_W_CM}cm}}
\newlength{{\slideH}}\setlength{{\slideH}}{{{SLIDE_H_CM}cm}}
\newlength{{\slideMargin}}\setlength{{\slideMargin}}{{{MARGIN_CM}cm}}

\definecolor{{bgfallback}}{{HTML}}{{{theme["bg_fallback"]}}}
\definecolor{{accent}}{{HTML}}{{{theme["accent"]}}}
\definecolor{{accentlight}}{{HTML}}{{{theme["accent_light"]}}}
\definecolor{{darktext}}{{HTML}}{{{theme["dark"]}}}
\definecolor{{midtext}}{{HTML}}{{{theme["mid"]}}}
\definecolor{{lightline}}{{HTML}}{{{theme["light"]}}}
\definecolor{{labelbg}}{{HTML}}{{{theme["label_bg"]}}}
\definecolor{{labeltext}}{{HTML}}{{{theme["label_text"]}}}
\definecolor{{cardbg}}{{HTML}}{{{theme["card_bg"]}}}
\definecolor{{shadowcolor}}{{HTML}}{{{theme["dark"]}}}

% Gradient shading for labels (accent top -> darker accent bottom)
\pgfdeclarehorizontalshading{{labelshadebg}}{{100bp}}{{
  color(0bp)=(labelbg);
  color(50bp)=(labelbg!85!black);
  color(100bp)=(labelbg!70!black)
}}
% Subtle top-to-bottom gradient for cards
\pgfdeclareverticalshading{{cardshade}}{{100bp}}{{
  color(0bp)=(cardbg!95!white);
  color(100bp)=(cardbg)
}}
% Vignette-style fading for corners
\pgfdeclarefading{{vignettefade}}{{
  \tikz\fill[shading=radial,inner color=pgftransparent!0,outer color=pgftransparent!40]
    (0,0) rectangle (1,1);
}}
% Title text shadow style
\tikzset{{
  txtshadow/.style={{opacity=0.12, text=shadowcolor}},
  softshadow/.style={{blur shadow={{shadow blur steps=6, shadow xshift=0.6pt, shadow yshift=-0.6pt, shadow blur radius=1.5pt, shadow opacity=18}}}},
  cardshadow/.style={{blur shadow={{shadow blur steps=8, shadow xshift=0.8pt, shadow yshift=-1.2pt, shadow blur radius=2.5pt, shadow opacity=22}}}},
  deepshadow/.style={{blur shadow={{shadow blur steps=10, shadow xshift=1pt, shadow yshift=-1.5pt, shadow blur radius=3.5pt, shadow opacity=28}}}},
}}

\newcommand{{\cornerR}}{{{corner_r}}}
"""


def generate_header(brand_config, slide_num, total_slides):
    """Generate the slide header (brand name/logo + counter)."""
    bc = brand_config or DEFAULT_BRAND
    brand_name = escape_latex(bc.get("name", "Your Brand"))
    logo_path = bc.get("logo")
    style = bc.get("header_style", "italic")

    font_cmd = r"\itshape" if style == "italic" else (r"\bfseries" if style == "bold" else "")

    # Brand logo or text
    if logo_path and os.path.exists(logo_path):
        brand_node = rf"""
\node[anchor=north west, inner sep=0pt] at (\slideMargin, \slideH - 0.4cm) {{%
  \includegraphics[height=0.6cm, keepaspectratio]{{{logo_path}}}%
}};"""
    else:
        brand_node = rf"""
\node[anchor=north west, text=accent, font=\fontsize{{11}}{{13}}\selectfont{font_cmd}]
  at (\slideMargin, \slideH - 0.6cm) {{{brand_name}}};"""

    return rf"""{brand_node}
\node[anchor=north east, text=midtext, font=\fontsize{{11}}{{13}}\selectfont]
  at (\slideW - \slideMargin, \slideH - 0.6cm) {{{slide_num}/{total_slides}}};
"""


def generate_nav_arrow(brand_config=None):
    """Generate the navigation arrow at bottom-right."""
    bc = brand_config or DEFAULT_BRAND
    style = bc.get("nav_style", "circle")
    if style == "none":
        return ""
    return r"""
% Navigation arrow with gradient + shadow
\fill[shadowcolor, opacity=0.1] ($(\slideW - \slideMargin - 0.5cm, 1.2cm) + (0.8pt, -0.8pt)$) circle (0.5cm);
\shade[ball color=accent] (\slideW - \slideMargin - 0.5cm, 1.2cm) circle (0.5cm);
\node[text=white, font=\fontsize{18}{18}\selectfont\bfseries, anchor=center]
  at (\slideW - \slideMargin - 0.5cm, 1.2cm) {$\rightarrow$};
"""


def generate_divider(y_cm, style="line"):
    """Generate a decorative divider."""
    if style == "ornament":
        return rf"""
\draw[lightline, line width=0.5pt]
  (\slideMargin, \slideH - {y_cm}cm) -- (\slideW/2 - 0.8cm, \slideH - {y_cm}cm);
\node[text=accentlight, font=\fontsize{{10}}{{10}}\selectfont] at (\slideW/2, \slideH - {y_cm}cm) {{$\diamond$}};
\draw[lightline, line width=0.5pt]
  (\slideW/2 + 0.8cm, \slideH - {y_cm}cm) -- (\slideW - \slideMargin, \slideH - {y_cm}cm);
"""
    elif style == "dots":
        return rf"""
\foreach \x in {{0,0.3,...,12}} {{
  \fill[lightline] (\slideMargin + \x cm, \slideH - {y_cm}cm) circle (0.5pt);
}}
"""
    elif style == "none":
        return ""
    else:  # line
        return rf"""
\draw[lightline, line width=0.5pt]
  (\slideMargin, \slideH - {y_cm}cm) -- (\slideW - \slideMargin, \slideH - {y_cm}cm);
"""


def generate_bg(texture_path, ai_bg_path=None, overlay_opacity=0.35, bg_style=None):
    """Generate background: texture, AI image, gradient, or flat color.

    bg_style options:
      - "texture"    : AI-generated paper/fabric texture (default if texture_path exists)
      - "gradient"   : TikZ gradient using theme colors (modern/tech look)
      - "solid"      : Flat theme background color
      - "ai_bg"      : Full-bleed AI background with overlay
      - "gradient_mesh" : Subtle multi-stop gradient with geometric accents
      - None         : Auto-detect based on available assets
    """
    if ai_bg_path and os.path.exists(ai_bg_path):
        # Full-bleed AI background with semi-transparent overlay
        return rf"""
% AI background image
\node[anchor=south west, inner sep=0pt] at (0,0) {{%
  \includegraphics[width=\slideW, height=\slideH]{{{ai_bg_path}}}%
}};
% Overlay for text readability
\fill[bgfallback, opacity={overlay_opacity}] (0,0) rectangle (\slideW, \slideH);
"""
    elif bg_style == "gradient":
        # Modern gradient background (great for tech/dark themes)
        return r"""
% Gradient background
\shade[top color=bgfallback, bottom color=bgfallback!85!black]
  (0,0) rectangle (\slideW, \slideH);
% Subtle accent glow at top
\fill[accent, opacity=0.03]
  (0, \slideH - 6cm) -- (\slideW, \slideH - 4cm) -- (\slideW, \slideH) -- (0, \slideH) -- cycle;
"""
    elif bg_style == "gradient_mesh":
        # Multi-stop gradient with geometric accent shapes
        return r"""
% Multi-stop gradient background
\shade[top color=bgfallback!95!white, bottom color=bgfallback!90!black]
  (0,0) rectangle (\slideW, \slideH);
% Geometric accent shapes (subtle)
\fill[accent, opacity=0.04] (0, \slideH) -- (5cm, \slideH) -- (0, \slideH - 5cm) -- cycle;
\fill[accent, opacity=0.03] (\slideW, 0) -- (\slideW - 4cm, 0) -- (\slideW, 4cm) -- cycle;
% Subtle center glow
\fill[accent, opacity=0.02] (\slideW/2, \slideH/2) circle (6cm);
"""
    elif bg_style == "solid":
        return r"""
\fill[bgfallback] (0,0) rectangle (\slideW, \slideH);
"""
    elif texture_path and os.path.exists(texture_path):
        return rf"""
\node[anchor=south west, inner sep=0pt] at (0,0) {{%
  \includegraphics[width=\slideW, height=\slideH]{{{texture_path}}}%
}};"""
    else:
        return r"""
\fill[bgfallback] (0,0) rectangle (\slideW, \slideH);
"""


# ===================================================================
# SLIDE GENERATORS
# ===================================================================

def generate_hook_slide(data, brand_config=None):
    """Generate a hook/cover slide with highlighted title phrase and optional AI bg."""
    title_plain = escape_latex(data.get("title", ""))
    title_highlight = escape_latex(data.get("title_highlight", ""))
    subtitle = escape_latex(data.get("subtitle", ""))
    callout = escape_latex(data.get("callout", ""))
    ai_image = data.get("ai_image", "")
    bc = brand_config or DEFAULT_BRAND
    divider_style = bc.get("divider_style", "line")

    if title_highlight:
        title_node = rf"""
% Title text shadow (subtle depth)
\node[anchor=north west, text width=\slideW - 2*\slideMargin, txtshadow,
      font=\fontsize{{36}}{{42}}\selectfont\bfseries, align=left]
  at (\slideMargin + 0.5pt, \slideH - 2.2cm - 0.5pt) {{{title_plain}}};
% Title plain
\node[anchor=north west, text width=\slideW - 2*\slideMargin, text=darktext,
      font=\fontsize{{36}}{{42}}\selectfont\bfseries, align=left]
  at (\slideMargin, \slideH - 2.2cm) {{{title_plain}}};
% Highlighted label with gradient fill + shadow
\node[anchor=north west, fill=labelbg!85!black, rounded corners=\cornerR,
      inner xsep=12pt, inner ysep=8pt, opacity=0.3]
  at (\slideMargin + 0.8pt, \slideH - 4.8cm - 0.8pt) {{\phantom{{\fontsize{{36}}{{42}}\selectfont\bfseries\itshape {title_highlight}}}}};
\node[anchor=north west, top color=labelbg, bottom color=labelbg!80!black,
      rounded corners=\cornerR,
      inner xsep=12pt, inner ysep=8pt,
      text=labeltext, font=\fontsize{{36}}{{42}}\selectfont\bfseries\itshape]
  at (\slideMargin, \slideH - 4.8cm) {{{title_highlight}}};
"""
        rule_y = 7.2
    else:
        title_node = rf"""
% Title text shadow
\node[anchor=north west, text width=\slideW - 2*\slideMargin, txtshadow,
      font=\fontsize{{34}}{{40}}\selectfont\bfseries, align=left]
  at (\slideMargin + 0.5pt, \slideH - 2.2cm - 0.5pt) {{{title_plain}}};
\node[anchor=north west, text width=\slideW - 2*\slideMargin, text=darktext,
      font=\fontsize{{34}}{{40}}\selectfont\bfseries, align=left]
  at (\slideMargin, \slideH - 2.2cm) {{{title_plain}}};
"""
        rule_y = 6.5

    callout_node = ""
    if callout:
        callout_node = rf"""
% Callout badge with shadow
\node[anchor=north east, top color=accent, bottom color=accent!80!black,
      rounded corners=3pt,
      inner xsep=8pt, inner ysep=4pt, softshadow,
      text=white, font=\fontsize{{10}}{{12}}\selectfont\itshape]
  at (\slideW - \slideMargin, \slideH - 1.8cm) {{{callout}}};
"""

    rule_node = generate_divider(rule_y, divider_style)

    subtitle_y = rule_y + 0.5
    subtitle_node = rf"""
\node[anchor=north west, text width=\slideW - 2*\slideMargin, text=midtext,
      font=\fontsize{{14}}{{19}}\selectfont\itshape, align=left]
  at (\slideMargin, \slideH - {subtitle_y}cm) {{{subtitle}}};
"""

    # Bottom accent image or decorative element
    bottom_node = ""
    if ai_image and os.path.exists(ai_image):
        bottom_node = rf"""
% AI accent image with card shadow
\fill[shadowcolor, opacity=0.08, rounded corners=6pt]
  (\slideMargin + 0.15cm, 1.85cm) rectangle (\slideW - \slideMargin + 0.15cm, 8.85cm);
\begin{{scope}}
  \clip[rounded corners=5pt]
    (\slideMargin, 2.0cm) rectangle (\slideW - \slideMargin, 9.0cm);
  \node[anchor=south, inner sep=0pt] at (\slideW/2, 2.0cm) {{%
    \includegraphics[width=\slideW - 2*\slideMargin, height=7cm, keepaspectratio]{{{ai_image}}}%
  }};
\end{{scope}}
\draw[accent!30, line width=0.4pt, rounded corners=5pt]
  (\slideMargin, 2.0cm) rectangle (\slideW - \slideMargin, 9.0cm);
"""
    else:
        # Layered decorative geometry with gradient
        bottom_node = rf"""
% Layered decorative bottom accent
\shade[top color=accent!3, bottom color=accent!10]
  (0, 0) -- (\slideW, 0) -- (\slideW, 4cm) -- (0, 2cm) -- cycle;
\shade[top color=accent!2, bottom color=accent!6]
  (0, 0) -- (\slideW, 0) -- (\slideW, 2.5cm) -- (0, 1cm) -- cycle;
% Subtle accent line at geometry edge
\draw[accent!15, line width=0.6pt]
  (0, 2cm) -- (\slideW, 4cm);
"""

    return f"{title_node}\n{callout_node}\n{rule_node}\n{subtitle_node}\n{bottom_node}"


def generate_tool_slide(data, brand_config=None):
    """Generate a tool/product slide with prominent screenshot card.

    Layout v2 (Aristotelian redesign):
      - Compact header: #N + Tool Name (2.0cm)
      - Description: concise, max 2 lines (2.5cm)
      - Screenshot card: DOMINANT, 55-60% of slide (10.2cm)
      - Quote: small footer attribution (2.0cm)
      - Total: 16.7cm of 18.75cm used (89% fill)

    Design rules (research-backed):
      - Screenshot occupies 55%+ of slide area
      - Card has prominent border (1.2pt accent) + deep shadow
      - Gradient bg (not texture) behind screenshot slides
      - Dark card bg (#161B22) for contrast with any screenshot
    """
    number = data.get("number", "1")
    name = escape_latex(data.get("name", ""))
    description = escape_latex(data.get("description", ""))
    quote = escape_latex(data.get("quote", ""))
    screenshot = data.get("screenshot", "")
    logo = data.get("logo", "")
    bc = brand_config or DEFAULT_BRAND

    # -- SCREENSHOT CARD (dominant: 55% of slide) --
    # Card spans from 5.8cm to 16.0cm from top = 10.2cm height
    card_top = 5.8       # cm from top of slide
    card_bottom = 16.0   # cm from top of slide
    card_h = card_bottom - card_top  # 10.2cm

    screenshot_node = ""
    if screenshot and os.path.exists(screenshot):
        screenshot_node = rf"""
% === SCREENSHOT CARD (55% of slide) ===
% Deep ambient shadow
\fill[shadowcolor, opacity=0.15, rounded corners=8pt]
  (\slideMargin - 0.05cm + 0.2cm, \slideH - {card_bottom + 0.25}cm)
  rectangle (\slideW - \slideMargin + 0.05cm + 0.2cm, \slideH - {card_top - 0.05}cm);
% Contact shadow (tighter)
\fill[shadowcolor, opacity=0.10, rounded corners=7pt]
  (\slideMargin + 0.1cm, \slideH - {card_bottom + 0.12}cm)
  rectangle (\slideW - \slideMargin + 0.1cm, \slideH - {card_top + 0.02}cm);
% Card background (elevated surface)
\fill[cardbg, rounded corners=6pt]
  (\slideMargin, \slideH - {card_bottom}cm) rectangle (\slideW - \slideMargin, \slideH - {card_top}cm);
% Screenshot image clipped to card
\begin{{scope}}
  \clip[rounded corners=5pt]
    (\slideMargin + 0.12cm, \slideH - {card_bottom - 0.12}cm)
    rectangle (\slideW - \slideMargin - 0.12cm, \slideH - {card_top + 0.12}cm);
  \node[anchor=center, inner sep=0pt]
    at (\slideW/2, \slideH - {card_top + card_h/2}cm) {{%
    \includegraphics[width=\slideW - 2*\slideMargin - 0.24cm, height={card_h - 0.24}cm, keepaspectratio]{{{screenshot}}}%
  }};
\end{{scope}}
% Prominent accent border (visible, not subtle)
\draw[accent!60, line width=1.2pt, rounded corners=6pt]
  (\slideMargin, \slideH - {card_bottom}cm) rectangle (\slideW - \slideMargin, \slideH - {card_top}cm);
"""

    logo_node = ""
    if logo and os.path.exists(logo):
        logo_node = rf"""
% Brand/tool logo (bottom-right of card)
\node[anchor=south east, inner sep=0pt] at (\slideW - \slideMargin - 0.3cm, \slideH - {card_bottom - 0.3}cm) {{%
  \includegraphics[width=2.2cm, height=2.2cm, keepaspectratio]{{{logo}}}%
}};"""

    quote_node = ""
    if quote:
        quote_node = rf"""
% Quote attribution (compact footer)
\node[anchor=north west, text=midtext, font=\fontsize{{11}}{{15}}\selectfont\itshape,
      text width=\slideW - 2*\slideMargin - 0.4cm]
  at (\slideMargin + 0.2cm, \slideH - {card_bottom + 0.4}cm) {{%
    \textcolor{{accentlight}}{{\fontsize{{18}}{{18}}\selectfont\textbf{{``}}}}\hspace{{2pt}}{quote}%
  }};"""

    return rf"""
% === HEADER: #N + Tool Name (compact) ===
\node[anchor=west, txtshadow, font=\fontsize{{32}}{{36}}\selectfont\bfseries]
  at (\slideMargin + 0.5pt, \slideH - 2.6cm - 0.5pt) {{\#{number}}};
\node[anchor=west, text=darktext, font=\fontsize{{32}}{{36}}\selectfont\bfseries]
  at (\slideMargin, \slideH - 2.6cm) {{\#{number}}};

% Tool name label (gradient fill + shadow)
\node[anchor=west, fill=labelbg!85!black, rounded corners=\cornerR,
      inner xsep=10pt, inner ysep=6pt, opacity=0.25]
  at (\slideMargin + 2.0cm + 0.7pt, \slideH - 2.6cm - 0.7pt) {{\phantom{{\fontsize{{26}}{{30}}\selectfont\bfseries\itshape {name}}}}};
\node[anchor=west, top color=labelbg, bottom color=labelbg!80!black,
      rounded corners=\cornerR, inner xsep=10pt, inner ysep=6pt,
      text=labeltext, font=\fontsize{{26}}{{30}}\selectfont\bfseries\itshape]
  at (\slideMargin + 2.0cm, \slideH - 2.6cm) {{{name}}};

% Accent rule
\shade[left color=accent, right color=accent!30!bgfallback]
  (\slideMargin, \slideH - 3.6cm) rectangle (\slideMargin + 4cm, \slideH - 3.55cm);

% Description (concise, 2 lines max)
\node[anchor=north west, text width=\slideW - 2*\slideMargin, text=darktext,
      font=\fontsize{{14}}{{19}}\selectfont, align=left]
  at (\slideMargin, \slideH - 3.9cm) {{{description}}};

{screenshot_node}
{quote_node}
{logo_node}
"""


def generate_body_slide(data, brand_config=None):
    """Generate a content-heavy body slide with title, text, and bullets."""
    title = escape_latex(data.get("title", ""))
    title_highlight = escape_latex(data.get("title_highlight", ""))
    body = escape_latex(data.get("body", ""))
    bullets = data.get("bullets", [])
    ai_image = data.get("ai_image", "")
    bc = brand_config or DEFAULT_BRAND

    if title_highlight:
        title_node = rf"""
% Title text shadow
\node[anchor=north west, txtshadow,
      font=\fontsize{{26}}{{31}}\selectfont\bfseries]
  at (\slideMargin + 0.4pt, \slideH - 2.2cm - 0.4pt) {{{title}}};
\node[anchor=north west, text=darktext,
      font=\fontsize{{26}}{{31}}\selectfont\bfseries]
  at (\slideMargin, \slideH - 2.2cm) {{{title}}};
% Highlighted label with gradient + shadow
\node[anchor=north west, fill=labelbg!85!black, rounded corners=\cornerR,
      inner xsep=10pt, inner ysep=5pt, opacity=0.25]
  at (\slideMargin + 0.1cm + 0.6pt, \slideH - 3.6cm - 0.6pt) {{\phantom{{\fontsize{{26}}{{31}}\selectfont\bfseries\itshape {title_highlight}}}}};
\node[anchor=north west, top color=labelbg, bottom color=labelbg!80!black,
      rounded corners=\cornerR,
      inner xsep=10pt, inner ysep=5pt,
      text=labeltext, font=\fontsize{{26}}{{31}}\selectfont\bfseries\itshape]
  at (\slideMargin + 0.1cm, \slideH - 3.6cm) {{{title_highlight}}};
"""
        rule_y = 5.0
    else:
        title_node = rf"""
\node[anchor=north west, text width=\slideW - 2*\slideMargin, txtshadow,
      font=\fontsize{{24}}{{29}}\selectfont\bfseries, align=left]
  at (\slideMargin + 0.4pt, \slideH - 2.2cm - 0.4pt) {{{title}}};
\node[anchor=north west, text width=\slideW - 2*\slideMargin, text=darktext,
      font=\fontsize{{24}}{{29}}\selectfont\bfseries, align=left]
  at (\slideMargin, \slideH - 2.2cm) {{{title}}};
"""
        rule_y = 3.8

    # Gradient accent rule instead of flat
    rule_node = rf"""
\shade[left color=accent, right color=accent!40!bgfallback]
  (\slideMargin, \slideH - {rule_y}cm) rectangle (\slideMargin + 5cm, \slideH - {rule_y + 0.06}cm);
"""

    body_y = rule_y + 0.6
    body_node = rf"""
\node[anchor=north west, text width=\slideW - 2*\slideMargin, text=darktext,
      font=\fontsize{{15}}{{21}}\selectfont, align=left]
  at (\slideMargin, \slideH - {body_y}cm) {{{body}}};
"""

    bullets_tex = ""
    if bullets:
        bullet_y = body_y + 3.5 if body else body_y + 0.5
        bullet_items = []
        for b in bullets:
            b_esc = escape_latex(b)
            bullet_items.append(rf"    \item {b_esc}")
        items_str = "\n".join(bullet_items)
        bullets_tex = rf"""
\node[anchor=north west, text width=\slideW - 2*\slideMargin - 0.8cm, text=darktext,
      font=\fontsize{{13}}{{19}}\selectfont, align=left]
  at (\slideMargin + 0.3cm, \slideH - {bullet_y}cm) {{%
    \begin{{itemize}}[leftmargin=1.2em, itemsep=8pt, parsep=0pt]
      \renewcommand{{\labelitemi}}{{\textcolor{{accent}}{{\large\textbullet}}}}
{items_str}
    \end{{itemize}}
  }};"""

    ai_image_node = ""
    if ai_image and os.path.exists(ai_image):
        ai_image_node = rf"""
% AI accent card with real shadow
\fill[shadowcolor, opacity=0.08, rounded corners=6pt]
  (\slideMargin + 0.12cm, 1.18cm) rectangle (\slideW - \slideMargin + 0.12cm, 7.18cm);
\fill[cardbg, rounded corners=6pt]
  (\slideMargin, 1.3cm) rectangle (\slideW - \slideMargin, 7.3cm);
\begin{{scope}}
  \clip[rounded corners=5pt]
    (\slideMargin + 0.05cm, 1.35cm) rectangle (\slideW - \slideMargin - 0.05cm, 7.25cm);
  \node[anchor=south, inner sep=0pt] at (\slideW/2, 1.5cm) {{%
    \includegraphics[width=\slideW - 2.5cm, height=5.5cm, keepaspectratio]{{{ai_image}}}%
  }};
\end{{scope}}
\draw[accent!20, line width=0.3pt, rounded corners=5pt]
  (\slideMargin, 1.3cm) rectangle (\slideW - \slideMargin, 7.3cm);
"""

    return f"{title_node}\n{rule_node}\n{body_node}\n{bullets_tex}\n{ai_image_node}"


def generate_diagram_slide(data, brand_config=None):
    """Generate a slide with a professional TikZ flow diagram.

    DESIGN PRINCIPLE: The diagram FILLS the available canvas. Node sizes, fonts,
    and spacing are computed dynamically from node count and available space.
    No half-empty slides. Every pixel intentional.
    """
    title = escape_latex(data.get("title", ""))
    description = escape_latex(data.get("description", ""))
    nodes = data.get("diagram_nodes", [])
    diagram_type = data.get("diagram_type", "vertical")
    bc = brand_config or DEFAULT_BRAND
    n = len(nodes)

    # Available canvas for the diagram (below title+desc area, above nav)
    # Title ends at ~3.6cm, description may wrap to 2 lines (~5.6cm). Nav at ~1.5cm from bottom.
    # Card must start BELOW the description to avoid z-order overlap.
    card_top = SLIDE_H_CM - 5.8   # top of diagram region (below 2-line description)
    card_bottom = 2.0              # bottom of diagram region (above nav arrow)
    card_height = card_top - card_bottom  # ~10.95cm of usable space
    card_width = SLIDE_W_CM - 2 * MARGIN_CM  # ~12.6cm

    diagram_tex = ""
    if nodes:
        node_defs = []
        arrow_defs = []

        if diagram_type == "horizontal":
            # DYNAMIC SIZING: nodes fill the horizontal AND vertical space
            arrow_gap = 0.7
            total_arrows = max(n - 1, 0)
            total_arrow_space = total_arrows * arrow_gap
            node_w = max(2.0, (card_width - total_arrow_space - 0.8) / max(n, 1))
            # Node height: fill most of the card height (nodes are the main content)
            node_h = min(5.5, card_height * 0.55)
            # Font sizes: scale with node width, minimum readable
            label_fs = max(13, min(18, int(node_w * 5.5)))
            label_lh = label_fs + 4
            desc_fs = max(10, min(13, int(node_w * 4)))
            desc_lh = desc_fs + 4

            for i, node in enumerate(nodes):
                label = escape_latex(node.get("label", f"Node {i+1}"))
                desc = escape_latex(node.get("desc", ""))
                # Build node content: label + description stacked inside
                if desc:
                    node_content = (
                        rf"{{\fontsize{{{label_fs}}}{{{label_lh}}}\selectfont\bfseries {label}}}\\[4pt]"
                        rf"{{\fontsize{{{desc_fs}}}{{{desc_lh}}}\selectfont {desc}}}"
                    )
                else:
                    node_content = rf"{{\fontsize{{{label_fs}}}{{{label_lh}}}\selectfont\bfseries {label}}}"

                placement = "" if i == 0 else rf"right={arrow_gap}cm of n{i-1}"
                comma = ", " if placement else ""
                node_defs.append(
                    rf"\node[draw=accent!70, line width=1.2pt, fill=accent!15, rounded corners=\cornerR, "
                    rf"minimum width={node_w}cm, minimum height={node_h}cm, text=accent!90!black, "
                    rf"align=center, text width={node_w - 0.5}cm{comma}{placement}] "
                    rf"(n{i}) {{{node_content}}};"
                )
                if i > 0:
                    arrow_defs.append(
                        rf"\draw[-{{Stealth[length=3.5mm]}}, accent, line width=1.4pt] (n{i-1}) -- (n{i});"
                    )

        else:  # vertical
            # DYNAMIC SIZING: nodes fill the vertical space, descriptions beside them
            arrow_gap = 0.5
            total_arrows = max(n - 1, 0)
            total_arrow_space = total_arrows * arrow_gap
            node_h = max(1.4, min(2.8, (card_height - total_arrow_space - 0.5) / max(n, 1)))
            node_w = min(5.0, card_width * 0.38)  # narrower nodes = more room for descriptions
            desc_w = card_width - node_w - 1.5     # generous width for descriptions
            # Font sizes: readable at mobile
            label_fs = max(14, min(18, int(node_h * 7)))
            label_lh = label_fs + 4
            desc_fs = max(10, min(13, int(node_h * 5)))
            desc_lh = desc_fs + 4

            for i, node in enumerate(nodes):
                label = escape_latex(node.get("label", f"Node {i+1}"))
                desc = escape_latex(node.get("desc", ""))
                placement = "" if i == 0 else rf"below={arrow_gap}cm of n{i-1}"
                comma = ", " if placement else ""
                node_defs.append(
                    rf"\node[draw=accent!70, line width=1.2pt, fill=accent!15, rounded corners=\cornerR, "
                    rf"minimum width={node_w}cm, minimum height={node_h}cm, text=accent!90!black, "
                    rf"font=\fontsize{{{label_fs}}}{{{label_lh}}}\selectfont\bfseries, align=center{comma}{placement}] "
                    rf"(n{i}) {{{label}}};"
                )
                if i > 0:
                    arrow_defs.append(
                        rf"\draw[-{{Stealth[length=3.5mm]}}, accent, line width=1.4pt] (n{i-1}) -- (n{i});"
                    )
                if desc:
                    node_defs.append(
                        rf"\node[right=0.6cm of n{i}, text=midtext, "
                        rf"font=\fontsize{{{desc_fs}}}{{{desc_lh}}}\selectfont, align=left, "
                        rf"text width={desc_w}cm, anchor=west] "
                        rf"(d{i}) {{{desc}}};"
                    )

        all_nodes = "\n    ".join(node_defs)
        all_arrows = "\n    ".join(arrow_defs)

        # Card fills the available space below title/desc, above nav
        diagram_tex = rf"""
% Diagram card with shadow -- fills available canvas
\fill[shadowcolor, opacity=0.07, rounded corners=6pt]
  (\slideMargin + 0.12cm, {card_bottom - 0.12}cm) rectangle (\slideW - \slideMargin + 0.12cm, {card_top + 0.12}cm);
\shade[top color=cardbg, bottom color=cardbg!95!bgfallback, rounded corners=6pt]
  (\slideMargin, {card_bottom}cm) rectangle (\slideW - \slideMargin, {card_top}cm);
\draw[accent!15, line width=0.3pt, rounded corners=6pt]
  (\slideMargin, {card_bottom}cm) rectangle (\slideW - \slideMargin, {card_top}cm);

% Flow diagram -- centered in the card
\node[anchor=center, inner sep=0pt] at (\slideW/2, {(card_top + card_bottom) / 2}cm) {{%
  \begin{{tikzpicture}}[node distance=0.7cm]
    {all_nodes}
    {all_arrows}
  \end{{tikzpicture}}
}};"""

    return rf"""
% Title text shadow
\node[anchor=north west, text width=\slideW - 2*\slideMargin, txtshadow,
      font=\fontsize{{24}}{{29}}\selectfont\bfseries, align=left]
  at (\slideMargin + 0.4pt, \slideH - 2.2cm - 0.4pt) {{{title}}};
% Title
\node[anchor=north west, text width=\slideW - 2*\slideMargin, text=darktext,
      font=\fontsize{{24}}{{29}}\selectfont\bfseries, align=left]
  at (\slideMargin, \slideH - 2.2cm) {{{title}}};

\shade[left color=accent, right color=accent!40!bgfallback]
  (\slideMargin, \slideH - 3.6cm) rectangle (\slideMargin + 5cm, \slideH - 3.54cm);

% Description
\node[anchor=north west, text width=\slideW - 2*\slideMargin, text=darktext,
      font=\fontsize{{15}}{{21}}\selectfont, align=left]
  at (\slideMargin, \slideH - 4.1cm) {{{description}}};

{diagram_tex}
"""


def generate_comparison_slide(data, brand_config=None):
    """Generate a multi-column comparison slide with improved readability."""
    title = escape_latex(data.get("title", ""))
    subtitle = escape_latex(data.get("subtitle", ""))
    columns = data.get("columns", [])
    bc = brand_config or DEFAULT_BRAND
    divider_style = bc.get("divider_style", "line")

    if not columns:
        return generate_body_slide(data, brand_config)

    num_cols = min(len(columns), 3)
    gap = 0.3
    col_width = (SLIDE_W_CM - 2 * MARGIN_CM - gap * (num_cols - 1)) / num_cols

    col_nodes = ""
    for ci, col in enumerate(columns):
        col_name = escape_latex(col.get("name", f"Option {ci+1}"))
        col_items = col.get("items", [])

        x = MARGIN_CM + ci * (col_width + gap)
        top_y = SLIDE_H_CM - 5.5

        # Column header card with gradient + shadow
        col_nodes += rf"""
% Column {ci+1} header with gradient
\fill[shadowcolor, opacity=0.08, rounded corners=5pt]
  ({x + 0.06}cm, {top_y + 1.04}cm) rectangle ({x + col_width + 0.06}cm, {top_y - 0.06}cm);
\shade[top color=accent, bottom color=accent!80!black, rounded corners=4pt]
  ({x}cm, {top_y + 1.1}cm) rectangle ({x + col_width}cm, {top_y}cm);
\node[anchor=center, text=white, font=\fontsize{{13}}{{15}}\selectfont\bfseries]
  at ({x + col_width/2}cm, {top_y + 0.55}cm) {{{col_name}}};
"""
        # Column items
        for ii, item in enumerate(col_items):
            item_label = escape_latex(item.get("label", ""))
            item_value = escape_latex(item.get("value", ""))
            iy = top_y - 0.5 - ii * 2.4

            # Item card background with subtle gradient
            col_nodes += rf"""
\shade[top color=cardbg, bottom color=cardbg!95!bgfallback, rounded corners=3pt]
  ({x}cm, {iy + 0.1}cm) rectangle ({x + col_width}cm, {iy - 1.9}cm);
\draw[accent!12, line width=0.2pt, rounded corners=3pt]
  ({x}cm, {iy + 0.1}cm) rectangle ({x + col_width}cm, {iy - 1.9}cm);
"""
            if item_label:
                col_nodes += rf"""
\node[anchor=north west, text=accent, font=\fontsize{{10}}{{12}}\selectfont\bfseries,
      text width={col_width - 0.3}cm]
  at ({x + 0.15}cm, {iy}cm) {{{item_label}}};
"""
            if item_value:
                label_offset = 0.4 if item_label else 0.0
                col_nodes += rf"""
\node[anchor=north west, text=darktext, font=\fontsize{{10}}{{13}}\selectfont,
      text width={col_width - 0.3}cm]
  at ({x + 0.15}cm, {iy - label_offset}cm) {{{item_value}}};
"""

    return rf"""
% Title text shadow
\node[anchor=north west, text width=\slideW - 2*\slideMargin, txtshadow,
      font=\fontsize{{22}}{{27}}\selectfont\bfseries, align=left]
  at (\slideMargin + 0.4pt, \slideH - 2.2cm - 0.4pt) {{{title}}};
% Title
\node[anchor=north west, text width=\slideW - 2*\slideMargin, text=darktext,
      font=\fontsize{{22}}{{27}}\selectfont\bfseries, align=left]
  at (\slideMargin, \slideH - 2.2cm) {{{title}}};

% Subtitle
\node[anchor=north west, text width=\slideW - 2*\slideMargin, text=midtext,
      font=\fontsize{{12}}{{16}}\selectfont\itshape, align=left]
  at (\slideMargin, \slideH - 3.8cm) {{{subtitle}}};

% Gradient accent rule
\shade[left color=accent, right color=accent!40!bgfallback]
  (\slideMargin, \slideH - 4.6cm) rectangle (\slideMargin + 5cm, \slideH - 4.54cm);

{col_nodes}
"""


def generate_synthesis_slide(data, brand_config=None):
    """Generate a save-worthy synthesis/summary slide with styled numbers."""
    title = escape_latex(data.get("title", ""))
    points = data.get("points", [])
    ai_image = data.get("ai_image", "")
    bc = brand_config or DEFAULT_BRAND

    points_tex = ""
    if points:
        y_start = SLIDE_H_CM - 5.5
        spacing = min(2.0, (SLIDE_H_CM - 8.0) / max(len(points), 1))
        for i, pt in enumerate(points):
            pt_esc = escape_latex(pt)
            y = y_start - i * spacing

            points_tex += rf"""
% Point {i+1} badge with gradient + shadow
\fill[shadowcolor, opacity=0.1, rounded corners=3pt]
  (\slideMargin + 0.06cm, {y - 0.06}cm) rectangle (\slideMargin + 0.81cm, {y - 0.76}cm);
\shade[top color=accent, bottom color=accent!75!black, rounded corners=3pt]
  (\slideMargin, {y}cm) rectangle (\slideMargin + 0.75cm, {y - 0.7}cm);
\node[anchor=center, text=white, font=\fontsize{{12}}{{14}}\selectfont\bfseries]
  at (\slideMargin + 0.375cm, {y - 0.35}cm) {{{i+1}}};
\node[anchor=north west, text=darktext, font=\fontsize{{13}}{{17}}\selectfont,
      text width=\slideW - 2*\slideMargin - 1.2cm]
  at (\slideMargin + 1.0cm, {y + 0.05}cm) {{{pt_esc}}};
"""
            if i < len(points) - 1:
                sep_y = y - spacing + 0.5
                points_tex += rf"""
\draw[lightline!50, line width=0.3pt]
  (\slideMargin + 1.0cm, {sep_y}cm) -- (\slideW - \slideMargin, {sep_y}cm);
"""

    ai_node = ""
    if ai_image and os.path.exists(ai_image):
        ai_node = rf"""
\node[anchor=south, inner sep=0pt] at (\slideW/2, 1.5cm) {{%
  \includegraphics[width=6cm, height=4cm, keepaspectratio]{{{ai_image}}}%
}};"""

    return rf"""
% Title text shadow
\node[anchor=north west, text width=\slideW - 2*\slideMargin, txtshadow,
      font=\fontsize{{24}}{{29}}\selectfont\bfseries, align=left]
  at (\slideMargin + 0.4pt, \slideH - 2.2cm - 0.4pt) {{{title}}};
% Title
\node[anchor=north west, text width=\slideW - 2*\slideMargin, text=darktext,
      font=\fontsize{{24}}{{29}}\selectfont\bfseries, align=left]
  at (\slideMargin, \slideH - 2.2cm) {{{title}}};

\shade[left color=accent, right color=accent!40!bgfallback]
  (\slideMargin, \slideH - 3.6cm) rectangle (\slideMargin + 5cm, \slideH - 3.54cm);

% Save hint with subtle badge
\node[anchor=north east, fill=accent!8, rounded corners=2pt,
      inner xsep=6pt, inner ysep=2pt,
      text=midtext, font=\fontsize{{10}}{{12}}\selectfont\itshape]
  at (\slideW - \slideMargin, \slideH - 3.0cm) {{Save this}};

{points_tex}
{ai_node}
"""


def generate_cta_slide(data, brand_config=None):
    """Generate a call-to-action slide."""
    title = escape_latex(data.get("title", ""))
    cta_text = escape_latex(data.get("cta_text", ""))
    handle = escape_latex(data.get("handle", ""))
    stats = data.get("stats", [])
    ai_image = data.get("ai_image", "")
    bc = brand_config or DEFAULT_BRAND

    stats_tex = ""
    if stats:
        stat_items = []
        for s in stats:
            s_esc = escape_latex(s)
            stat_items.append(rf"\textcolor{{accent}}{{\bfseries\large$\bullet$}} {s_esc}")
        stats_joined = r" \quad ".join(stat_items)
        stats_tex = rf"""
\node[anchor=center, text=midtext, font=\fontsize{{11}}{{14}}\selectfont]
  at (\slideW/2, \slideH/2 + 1.5cm) {{{stats_joined}}};
"""

    # Gradient decorative rules
    deco_top = rf"""
\shade[left color=accent!20!bgfallback, right color=accent, middle color=accent]
  (\slideW/2 - 2.5cm, \slideH - 3.0cm) rectangle (\slideW/2 + 2.5cm, \slideH - 2.94cm);
"""
    deco_bottom = rf"""
\shade[left color=accent, right color=accent!20!bgfallback, middle color=accent]
  (\slideW/2 - 2.5cm, 2.5cm) rectangle (\slideW/2 + 2.5cm, 2.44cm);
"""

    return rf"""
{deco_top}

% Title text shadow
\node[anchor=north, text width=\slideW - 3.5cm, txtshadow,
      font=\fontsize{{28}}{{34}}\selectfont\bfseries, align=center]
  at ($(\slideW/2, \slideH - 3.8cm) + (0.5pt, -0.5pt)$) {{{title}}};
% Title
\node[anchor=north, text width=\slideW - 3.5cm, text=darktext,
      font=\fontsize{{28}}{{34}}\selectfont\bfseries, align=center]
  at (\slideW/2, \slideH - 3.8cm) {{{title}}};

{stats_tex}

% CTA text
\node[anchor=center, text width=\slideW - 4cm, text=midtext,
      font=\fontsize{{14}}{{20}}\selectfont, align=center]
  at (\slideW/2, \slideH/2 - 1.0cm) {{{cta_text}}};

% Handle button with gradient + shadow
\node[anchor=south, fill=accent!85!black, rounded corners=8pt,
      inner xsep=20pt, inner ysep=10pt, opacity=0.2]
  at ($(\slideW/2, 3.5cm) + (1pt, -1pt)$) {{\phantom{{\fontsize{{16}}{{18}}\selectfont\bfseries {handle}}}}};
\node[anchor=south, top color=accent, bottom color=accent!80!black,
      rounded corners=8pt, inner xsep=20pt, inner ysep=10pt,
      text=white, font=\fontsize{{16}}{{18}}\selectfont\bfseries]
  at (\slideW/2, 3.5cm) {{{handle}}};

{deco_bottom}
"""


SLIDE_GENERATORS = {
    "hook": generate_hook_slide,
    "tool": generate_tool_slide,
    "body": generate_body_slide,
    "comparison": generate_comparison_slide,
    "diagram": generate_diagram_slide,
    "synthesis": generate_synthesis_slide,
    "cta": generate_cta_slide,
}


def postprocess_slide(img, theme="warm"):
    """Production-grade post-processing pipeline.

    Applies 4 effects in order:
      1. Subtle grain/noise overlay (prevents flat digital look)
      2. Unsharp mask sharpening (optimized for Instagram compression)
      3. Radial vignette (draws eye to center)
      4. Color grading (slight saturation + contrast boost)
    """
    from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
    import random

    w, h = img.size

    # 1. GRAIN OVERLAY -- subtle noise that prevents "sterile digital" look
    #    Production carousels always have 3-8% opacity noise
    try:
        import numpy as np
        grain_array = np.random.normal(128, 18, (h, w)).astype(np.uint8)
        grain = Image.fromarray(grain_array, mode='L').convert('RGB')
        # Blend at ~4% opacity (subtle but visible at 300dpi)
        img = Image.blend(img, grain, alpha=0.035)
    except ImportError:
        # Fallback: skip grain if numpy unavailable
        pass

    # 2. UNSHARP MASK -- Instagram compresses heavily, so pre-sharpening
    #    compensates. radius=2, percent=120, threshold=3 is the sweet spot
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=120, threshold=3))

    # 3. RADIAL VIGNETTE -- darkens edges by ~8-12%, draws eye to center
    #    This is the #1 micro-detail that separates pro from amateur
    vignette = Image.new('L', (w, h), 255)
    draw = ImageDraw.Draw(vignette)
    cx, cy = w // 2, h // 2
    max_r = (cx**2 + cy**2) ** 0.5
    # Draw concentric ellipses from outside in
    for i in range(int(max_r), 0, -2):
        # Brightness falls off from center: 255 at center -> ~220 at edge
        brightness = int(255 - (1 - (i / max_r)) * 35)
        brightness = max(200, min(255, brightness))
        draw.ellipse(
            [cx - i, cy - i, cx + i, cy + i],
            fill=brightness
        )
    img = Image.composite(img, Image.new('RGB', (w, h), (0, 0, 0)), vignette)

    # 4. COLOR GRADING -- subtle enhancement tuned per theme
    #    warm/earth: slight warmth boost, clean/dark: slight cool crispness
    if theme in ("warm", "earth"):
        img = ImageEnhance.Color(img).enhance(1.06)      # +6% saturation
        img = ImageEnhance.Contrast(img).enhance(1.03)    # +3% contrast
    elif theme == "dark":
        img = ImageEnhance.Color(img).enhance(1.08)       # +8% sat (colors pop on dark)
        img = ImageEnhance.Contrast(img).enhance(1.05)    # +5% contrast
    else:  # clean
        img = ImageEnhance.Sharpness(img).enhance(1.05)   # extra crispness
        img = ImageEnhance.Contrast(img).enhance(1.02)    # +2% contrast

    return img


def render_slide(slide_type, data, output_path, theme="warm", texture_path=None,
                 brand_config=None, dpi=DPI):
    """Render a single carousel slide using LaTeX."""
    bc = brand_config or DEFAULT_BRAND
    brand_name = bc.get("name", "Your Brand")
    slide_num = data.get("slide_num", 1)
    total_slides = data.get("total_slides", 9)
    show_nav = data.get("show_nav", True)
    ai_bg = data.get("ai_bg", "")  # Full-bleed AI background
    overlay_opacity = data.get("overlay_opacity", 0.35)
    bg_style = data.get("bg_style", None)  # gradient, gradient_mesh, solid, texture, or None (auto)

    generator = SLIDE_GENERATORS.get(slide_type)
    if not generator:
        print(f"Error: Unknown slide type '{slide_type}'", file=sys.stderr)
        sys.exit(1)

    # AUTO-FIX: Tool slides with screenshots look terrible with texture backgrounds.
    # Research proves solid/gradient backgrounds maximize screenshot readability.
    # Override texture -> gradient for tool slides unless explicitly set.
    if slide_type == "tool" and not bg_style and not ai_bg and texture_path:
        bg_style = "gradient"

    preamble = generate_preamble(theme, bc)
    header = generate_header(bc, slide_num, total_slides)
    nav = generate_nav_arrow(bc) if show_nav else ""
    content = generator(data, bc)
    bg = generate_bg(texture_path, ai_bg, overlay_opacity, bg_style)

    full_doc = rf"""{preamble}
\begin{{document}}
\begin{{tikzpicture}}
\useasboundingbox (0,0) rectangle (\slideW, \slideH);
{bg}
{header}
{content}
{nav}
\end{{tikzpicture}}
\end{{document}}
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "slide.tex")
        pdf_path = os.path.join(tmpdir, "slide.pdf")

        with open(tex_path, "w") as f:
            f.write(full_doc)

        # Symlink all referenced images
        image_keys = ["screenshot", "logo", "ai_image", "ai_bg"]
        for key in image_keys:
            img_path = data.get(key, "")
            if img_path and os.path.exists(img_path):
                dest = os.path.join(tmpdir, os.path.basename(img_path))
                if not os.path.exists(dest):
                    os.symlink(os.path.abspath(img_path), dest)

        for logo_path in data.get("logos", []):
            if logo_path and os.path.exists(logo_path):
                dest = os.path.join(tmpdir, os.path.basename(logo_path))
                if not os.path.exists(dest):
                    os.symlink(os.path.abspath(logo_path), dest)

        # Brand logo
        brand_logo = bc.get("logo", "")
        if brand_logo and os.path.exists(brand_logo):
            dest = os.path.join(tmpdir, os.path.basename(brand_logo))
            if not os.path.exists(dest):
                os.symlink(os.path.abspath(brand_logo), dest)

        if texture_path and os.path.exists(texture_path):
            tex_dest = os.path.join(tmpdir, os.path.basename(texture_path))
            if not os.path.exists(tex_dest):
                os.symlink(os.path.abspath(texture_path), tex_dest)

        # Rewrite paths as basenames
        with open(tex_path, "r") as f:
            tex_content = f.read()

        for key in image_keys:
            img_path = data.get(key, "")
            if img_path and os.path.exists(img_path):
                tex_content = tex_content.replace(img_path, os.path.basename(img_path))

        for logo_path in data.get("logos", []):
            if logo_path and os.path.exists(logo_path):
                tex_content = tex_content.replace(logo_path, os.path.basename(logo_path))

        if brand_logo and os.path.exists(brand_logo):
            tex_content = tex_content.replace(brand_logo, os.path.basename(brand_logo))

        if texture_path and os.path.exists(texture_path):
            tex_content = tex_content.replace(texture_path, os.path.basename(texture_path))

        with open(tex_path, "w") as f:
            f.write(tex_content)

        # Compile
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "slide.tex"],
            cwd=tmpdir, capture_output=True, text=True, timeout=60
        )

        if not os.path.exists(pdf_path):
            print(f"LaTeX compilation failed!", file=sys.stderr)
            print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout, file=sys.stderr)
            debug_path = output_path.replace(".png", ".tex")
            import shutil
            shutil.copy(tex_path, debug_path)
            print(f"Debug .tex saved to: {debug_path}", file=sys.stderr)
            return False

        # Convert PDF to PNG
        png_prefix = os.path.join(tmpdir, "slide_out")
        subprocess.run(
            ["pdftoppm", "-png", "-r", str(dpi), pdf_path, png_prefix],
            capture_output=True, timeout=30
        )

        raw_png = png_prefix + "-1.png"
        if not os.path.exists(raw_png):
            print("PDF to PNG conversion failed!", file=sys.stderr)
            return False

        from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
        import numpy as np
        img = Image.open(raw_png)
        new_w = FINAL_W
        new_h = int(new_w * img.size[1] / img.size[0])
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        if new_h > FINAL_H:
            top = (new_h - FINAL_H) // 2
            img = img.crop((0, top, FINAL_W, top + FINAL_H))
        elif new_h < FINAL_H:
            theme_data = get_theme(theme, bc)
            bg_hex = theme_data["bg_fallback"]
            bg_rgb = tuple(int(bg_hex[i:i+2], 16) for i in (0, 2, 4))
            canvas = Image.new("RGB", (FINAL_W, FINAL_H), bg_rgb)
            canvas.paste(img, (0, 0))
            img = canvas

        # === POST-PROCESSING PIPELINE (Production-Grade) ===
        img = postprocess_slide(img, theme)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        img.save(output_path, "PNG", quality=95)
        print(f"Rendered: {output_path} ({FINAL_W}x{FINAL_H}, type={slide_type}, theme={theme})")
        return True


def main():
    parser = argparse.ArgumentParser(description="Render world-class carousel slide using LaTeX")
    parser.add_argument("--type", required=True, choices=list(SLIDE_GENERATORS.keys()),
                        help="Slide type")
    parser.add_argument("--data", required=True, help="JSON string or path to JSON file")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--theme", default="warm", choices=list(THEMES.keys()),
                        help="Color theme")
    parser.add_argument("--texture", help="Path to paper texture background image")
    parser.add_argument("--brand", help="Path to brand config JSON file")
    parser.add_argument("--dpi", type=int, default=DPI, help=f"Output DPI (default: {DPI})")

    args = parser.parse_args()

    if os.path.exists(args.data):
        with open(args.data) as f:
            data = json.load(f)
    else:
        data = json.loads(args.data)

    brand_config = load_brand_config(args.brand)
    theme = args.theme or brand_config.get("theme", "warm")

    success = render_slide(
        slide_type=args.type,
        data=data,
        output_path=args.output,
        theme=theme,
        texture_path=args.texture,
        brand_config=brand_config,
        dpi=args.dpi,
    )

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
