#!/usr/bin/env python3
"""
make_ascii_svg.py
-----------------
Converts a preprocessed image into an animated ASCII art SVG portrait:
1. Loads source-prepped.png.
2. Downscales the image to fit a terminal character grid (e.g., 64x42).
3. Adjusts for character aspect ratio (fonts are taller than they are wide, ~1:2).
4. Maps pixel luminance values (0-255) to an ASCII character ramp.
5. Encapsulates the ASCII text inside a stylized Linux Terminal SVG window.
6. Implements zero-JS pure SVG SMIL animations for a smooth typing reveal effect
   and a blinking terminal cursor.
"""

import os
import sys
from PIL import Image

# ASCII Character Ramp from darkest (densest) to lightest (sparse)
ASCII_RAMP = "@%#*+=-:. "

def image_to_ascii(image_path: str, width: int = 60) -> list[str]:
    """
    Converts image at image_path to a list of ASCII string rows.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image '{image_path}' not found.")
        sys.exit(1)

    img = Image.open(image_path).convert("L")
    
    # Calculate aspect ratio adjustment:
    # Monospace characters are roughly twice as tall as they are wide (font aspect ratio ~ 0.55)
    orig_w, orig_h = img.size
    aspect_ratio = orig_h / orig_w
    height = int(width * aspect_ratio * 0.52)

    # Resize image to ASCII grid dimensions
    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    
    ascii_rows = []
    ramp_length = len(ASCII_RAMP)

    for y in range(height):
        row_chars = []
        for x in range(width):
            pixel_val = img_resized.getpixel((x, y))
            # Map pixel luminance (0..255) to ASCII character ramp index
            index = int((pixel_val / 255.0) * (ramp_length - 1))
            row_chars.append(ASCII_RAMP[index])
        ascii_rows.append("".join(row_chars))

    return ascii_rows

def generate_ascii_svg(ascii_rows: list[str], output_path: str = "avi-ascii.svg"):
    """
    Generates avi-ascii.svg containing animated ASCII text in a terminal window.
    """
    cols = len(ascii_rows[0])
    rows = len(ascii_rows)
    
    # Layout dimensions
    char_width = 7.2
    line_height = 13.0
    
    padding_x = 24
    padding_top = 45
    padding_bottom = 25
    
    svg_width = int(cols * char_width + padding_x * 2)
    svg_height = int(rows * line_height + padding_top + padding_bottom)

    # Escape HTML special characters for raw SVG text insertion
    def xml_escape(text: str) -> str:
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")

    escaped_rows = [xml_escape(row) for row in ascii_rows]

    # Calculate reveal animation delays per line
    total_duration = 2.5 # total seconds for full typing reveal
    delay_per_line = total_duration / max(1, rows)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <!-- Dark Mode Terminal Gradient -->
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>

    <!-- Matrix Green Text Glow Filter -->
    <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.2" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <style>
      .term-bg {{
        fill: url(#bg-grad);
        stroke: #30363d;
        stroke-width: 1.5px;
        rx: 10px;
        ry: 10px;
      }}
      .term-header {{
        fill: #161b22;
        stroke: #30363d;
        stroke-width: 1px;
      }}
      .dot-red {{ fill: #ff5f56; }}
      .dot-yellow {{ fill: #ffbd2e; }}
      .dot-green {{ fill: #27c93f; }}
      
      .term-title {{
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        font-size: 11px;
        fill: #8b949e;
        font-weight: 600;
      }}
      
      .ascii-text {{
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        font-size: 11px;
        line-height: {line_height}px;
        fill: #39d353;
        letter-spacing: 1px;
        white-space: pre;
        filter: url(#neon-glow);
      }}

      .cursor {{
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        font-size: 13px;
        fill: #58a6ff;
        font-weight: bold;
      }}
    </style>
  </defs>

  <!-- Terminal Window Background -->
  <rect class="term-bg" x="0.75" y="0.75" width="{svg_width - 1.5}" height="{svg_height - 1.5}" />

  <!-- Terminal Header Bar -->
  <path class="term-header" d="M 0.75,10 A 10,10 0 0,1 10.75,0.75 L {svg_width - 10.75},0.75 A 10,10 0 0,1 {svg_width - 0.75},10 L {svg_width - 0.75},32 L 0.75,32 Z" />

  <!-- Window Controls -->
  <circle class="dot-red" cx="18" cy="16" r="5.5" />
  <circle class="dot-yellow" cx="34" cy="16" r="5.5" />
  <circle class="dot-green" cx="50" cy="16" r="5.5" />

  <!-- Terminal Title -->
  <text class="term-title" x="{svg_width / 2}" y="20" text-anchor="middle">ascii-portrait.sh — 80x{rows}</text>

  <!-- ASCII Lines Container -->
  <g transform="translate({padding_x}, {padding_top})">
'''

    # Add each line with a SMIL opacity animation delay
    for idx, row in enumerate(escaped_rows):
        y_pos = int(idx * line_height)
        delay = round(idx * delay_per_line, 2)
        svg_content += f'''    <text class="ascii-text" x="0" y="{y_pos}" opacity="0">
      {row}
      <animate attributeName="opacity" to="1" dur="0.15s" begin="{delay}s" fill="freeze" />
    </text>\n'''

    # Add animated blinking terminal cursor at bottom
    last_y = int(rows * line_height) + 5
    svg_content += f'''
    <!-- Animated Blinking Cursor -->
    <text class="cursor" x="0" y="{last_y}">
      &#62;&#160;_
      <animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite" />
    </text>
  </g>
</svg>
'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated ASCII SVG portrait '{output_path}'.")

def main():
    image_input = "source-prepped.png"
    output_svg = "avi-ascii.svg"
    
    if not os.path.exists(image_input):
        print(f"File '{image_input}' missing. Running prep_photo.py first...")
        from prep_photo import prep_photo
        prep_photo()

    ascii_rows = image_to_ascii(image_input, width=54)
    generate_ascii_svg(ascii_rows, output_svg)

if __name__ == "__main__":
    main()
