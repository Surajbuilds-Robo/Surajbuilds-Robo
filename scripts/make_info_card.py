#!/usr/bin/env python3
"""
make_info_card.py
-----------------
Generates an animated Neofetch-style Info Card SVG:
1. Formats profile information (Role, Education, Stack, Languages, Tools, Website) into clean terminal key-value pairs.
2. Applies GitHub dark mode terminal aesthetics (#0d1117 backdrop, #30363d borders, window controls).
3. Adds pure SVG SMIL animations for sequential line-by-line typing/fade-in effects.
4. Generates info-card.svg without requiring any external JavaScript runtime.
"""

import os
import sys

# Profile Information Config (Customizable by User)
PROFILE_DATA = {
    "user": "suraj@developer-box",
    "separator": "----------------------------------------",
    "info": [
        ("OS", "Linux x86_64 (Arch / Fedora)"),
        ("HOST", "GitHub Profile v2.5.0"),
        ("ROLE", "Senior Full-Stack & AI Engineer"),
        ("EDUCATION", "B.S. in Computer Science"),
        ("LANGUAGES", "Python, TypeScript, Rust, C++, SQL"),
        ("FRAMEWORKS", "Next.js, React, FastAPI, PyTorch, Tailwind"),
        ("DATABASE", "PostgreSQL, Redis, VectorDB (Qdrant)"),
        ("TOOLS", "Git, Docker, Kubernetes, Neovim, Linux"),
        ("LEARNING", "LLM Fine-Tuning & Quantization, WebGPU"),
        ("PROJECTS", "AI Agent Framework, Open Source Contributor"),
        ("WEBSITE", "https://alex-dev.portfolio.io"),
        ("STATUS", "🟢 Open for high-impact collaborations")
    ]
}

def generate_info_card_svg(profile: dict = PROFILE_DATA, output_path: str = "info-card.svg"):
    """
    Constructs info-card.svg using clean vector graphics and SMIL animation rules.
    """
    card_width = 540
    line_height = 24
    header_height = 42
    padding_x = 24
    padding_top = 55
    padding_bottom = 25

    total_lines = len(profile["info"]) + 2 # +2 for user string & separator line
    card_height = padding_top + (total_lines * line_height) + padding_bottom

    # Animation timing constants
    delay_step = 0.15 # seconds per line reveal
    start_delay = 0.2 # initial delay

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {card_width} {card_height}" width="{card_width}" height="{card_height}">
  <defs>
    <!-- Dark Mode Terminal Background Gradient -->
    <linearGradient id="card-bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>

    <!-- Accent Cyan Glow Filter -->
    <filter id="cyan-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <style>
      .card-bg {{
        fill: url(#card-bg-grad);
        stroke: #30363d;
        stroke-width: 1.5px;
        rx: 10px;
        ry: 10px;
      }}
      .card-header {{
        fill: #161b22;
        stroke: #30363d;
        stroke-width: 1px;
      }}
      .dot-red {{ fill: #ff5f56; }}
      .dot-yellow {{ fill: #ffbd2e; }}
      .dot-green {{ fill: #27c93f; }}

      .header-title {{
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        font-size: 12px;
        fill: #8b949e;
        font-weight: 600;
      }}

      .user-prompt {{
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        font-size: 14px;
        fill: #58a6ff;
        font-weight: 700;
        filter: url(#cyan-glow);
      }}

      .separator {{
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        font-size: 13px;
        fill: #484f58;
      }}

      .key-label {{
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        font-size: 13px;
        fill: #79c0ff;
        font-weight: 600;
      }}

      .value-text {{
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        font-size: 13px;
        fill: #c9d1d9;
      }}

      .accent-highlight {{
        fill: #39d353;
        font-weight: 600;
      }}
    </style>
  </defs>

  <!-- Card Frame -->
  <rect class="card-bg" x="0.75" y="0.75" width="{card_width - 1.5}" height="{card_height - 1.5}" />

  <!-- Header Bar -->
  <path class="card-header" d="M 0.75,10 A 10,10 0 0,1 10.75,0.75 L {card_width - 10.75},0.75 A 10,10 0 0,1 {card_width - 0.75},10 L {card_width - 0.75},34 L 0.75,34 Z" />

  <!-- Window Dots -->
  <circle class="dot-red" cx="18" cy="17" r="5.5" />
  <circle class="dot-yellow" cx="34" cy="17" r="5.5" />
  <circle class="dot-green" cx="50" cy="17" r="5.5" />

  <text class="header-title" x="{card_width / 2}" y="21" text-anchor="middle">neofetch --sysinfo</text>

  <!-- Content Container -->
  <g transform="translate({padding_x}, {padding_top})">
'''

    current_line = 0

    # Line 1: User Prompt
    d_time = round(start_delay + (current_line * delay_step), 2)
    y_val = current_line * line_height
    svg += f'''    <g opacity="0" transform="translate(0, {y_val})">
      <text class="user-prompt" x="0" y="0">{profile["user"]}</text>
      <animate attributeName="opacity" to="1" dur="0.25s" begin="{d_time}s" fill="freeze" />
      <animateTransform attributeName="transform" type="translate" from="-10, {y_val}" to="0, {y_val}" dur="0.25s" begin="{d_time}s" fill="freeze" />
    </g>\n'''
    current_line += 1

    # Line 2: Separator Line
    d_time = round(start_delay + (current_line * delay_step), 2)
    y_val = current_line * line_height
    svg += f'''    <g opacity="0" transform="translate(0, {y_val})">
      <text class="separator" x="0" y="0">{profile["separator"]}</text>
      <animate attributeName="opacity" to="1" dur="0.25s" begin="{d_time}s" fill="freeze" />
    </g>\n'''
    current_line += 1

    # Lines 3+: Profile Key-Value Items
    for label, val in profile["info"]:
        d_time = round(start_delay + (current_line * delay_step), 2)
        y_val = current_line * line_height
        
        # Calculate key padding offset
        key_str = f"{label}:".ljust(12)
        
        val_class = "value-text"
        if label == "STATUS":
            val_class += " accent-highlight"

        svg += f'''    <g opacity="0" transform="translate(0, {y_val})">
      <text class="key-label" x="0" y="0">{key_str}</text>
      <text class="{val_class}" x="105" y="0">{val}</text>
      <animate attributeName="opacity" to="1" dur="0.2s" begin="{d_time}s" fill="freeze" />
      <animateTransform attributeName="transform" type="translate" from="-8, {y_val}" to="0, {y_val}" dur="0.2s" begin="{d_time}s" fill="freeze" />
    </g>\n'''
        current_line += 1

    svg += '''  </g>
</svg>
'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Successfully generated Neofetch Info Card SVG '{output_path}'.")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "info-card.svg"
    generate_info_card_svg(PROFILE_DATA, out_file)
