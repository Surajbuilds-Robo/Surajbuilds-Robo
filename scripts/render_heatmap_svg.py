#!/usr/bin/env python3
"""
render_heatmap_svg.py
---------------------
Reads data/contributions.json and renders an animated GitHub Contribution Heatmap SVG:
1. Formats 52 calendar weeks (365 days) into an 11x11px grid with 3px gaps and 2px rounded corners.
2. Uses official GitHub Dark Mode contribution color spectrum:
   - Level 0: #161b22 (Empty)
   - Level 1: #0e4429 (Light)
   - Level 2: #006d32 (Medium)
   - Level 3: #26a641 (High)
   - Level 4: #39d353 (Maximum)
3. Incorporates top stats cards (Total Contributions, Current Streak, Longest Streak, Best Day).
4. Renders month headers, weekday labels, and a color legend.
5. Embeds zero-JS pure SVG SMIL animations for sequential week column pop-in effects.
6. Outputs contrib-heatmap.svg.
"""

import os
import sys
import json
from datetime import datetime, timedelta

# Official GitHub Dark Mode Contribution Color Palette
COLOR_MAP = {
    0: {"fill": "#161b22", "stroke": "#21262d"},
    1: {"fill": "#0e4429", "stroke": "#006d32"},
    2: {"fill": "#006d32", "stroke": "#26a641"},
    3: {"fill": "#26a641", "stroke": "#39d353"},
    4: {"fill": "#39d353", "stroke": "#56d364"},
}

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def render_heatmap_svg(json_path: str = "data/contributions.json", output_path: str = "contrib-heatmap.svg"):
    """
    Reads contributions JSON and builds contrib-heatmap.svg.
    """
    if not os.path.exists(json_path):
        print(f"Error: Dataset '{json_path}' not found.")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_contributions = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    best_day = data.get("best_day", {"date": "N/A", "count": 0})
    days = data.get("days", [])

    # Layout dimensions
    box_size = 11
    box_gap = 3
    box_stride = box_size + box_gap # 14px

    grid_x_offset = 35
    grid_y_offset = 115
    month_y_offset = grid_y_offset - 10

    max_weeks = 53
    grid_width = (max_weeks * box_stride)
    
    card_width = grid_x_offset + grid_width + 25
    card_height = grid_y_offset + (7 * box_stride) + 45

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {card_width} {card_height}" width="{card_width}" height="{card_height}">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="heatmap-bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>

    <!-- Glowing Accent Filter -->
    <filter id="green-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <style>
      .heatmap-bg {{
        fill: url(#heatmap-bg-grad);
        stroke: #30363d;
        stroke-width: 1.5px;
        rx: 10px;
        ry: 10px;
      }}
      .stat-card-bg {{
        fill: #161b22;
        stroke: #30363d;
        stroke-width: 1px;
        rx: 6px;
      }}
      .stat-label {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
        font-size: 10px;
        fill: #8b949e;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
      }}
      .stat-value {{
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        font-size: 14px;
        fill: #39d353;
        font-weight: 700;
        filter: url(#green-glow);
      }}
      .axis-label {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
        font-size: 10px;
        fill: #7d8590;
      }}
      .legend-text {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
        font-size: 10px;
        fill: #7d8590;
      }}
    </style>
  </defs>

  <!-- Card Frame -->
  <rect class="heatmap-bg" x="0.75" y="0.75" width="{card_width - 1.5}" height="{card_height - 1.5}" />

  <!-- Top Stat Cards Container -->
  <g transform="translate(18, 16)">
    <!-- Stat 1: Total Contributions -->
    <rect class="stat-card-bg" x="0" y="0" width="170" height="52" />
    <text class="stat-label" x="12" y="18">Total Contributions</text>
    <text class="stat-value" x="12" y="38">{total_contributions:,}</text>

    <!-- Stat 2: Current Streak -->
    <rect class="stat-card-bg" x="182" y="0" width="165" height="52" />
    <text class="stat-label" x="12" y="18">Current Streak</text>
    <text class="stat-value" x="12" y="38">🔥 {current_streak} Days</text>

    <!-- Stat 3: Longest Streak -->
    <rect class="stat-card-bg" x="359" y="0" width="165" height="52" />
    <text class="stat-label" x="12" y="18">Longest Streak</text>
    <text class="stat-value" x="12" y="38">⚡ {longest_streak} Days</text>

    <!-- Stat 4: Best Day -->
    <rect class="stat-card-bg" x="536" y="0" width="200" height="52" />
    <text class="stat-label" x="12" y="18">Best Day</text>
    <text class="stat-value" x="12" y="38">{best_day.get('count', 0)} ({best_day.get('date', 'N/A')})</text>
  </g>

  <!-- Weekday Axis Labels -->
  <g transform="translate({grid_x_offset - 10}, {grid_y_offset})">
    <text class="axis-label" x="0" y="{1 * box_stride + 9}" text-anchor="end">Mon</text>
    <text class="axis-label" x="0" y="{3 * box_stride + 9}" text-anchor="end">Wed</text>
    <text class="axis-label" x="0" y="{5 * box_stride + 9}" text-anchor="end">Fri</text>
  </g>
'''

    # Parse days and organize by (week_idx, day_of_week)
    if not days:
        print("Warning: No day records in JSON.")
        return

    # Calculate month header labels positions
    month_headers = []
    last_month = -1

    # Map dates to grid positions
    # 0 = Sunday, 1 = Monday, ..., 6 = Saturday
    day_0_date = datetime.strptime(days[0]["date"], "%Y-%m-%d")
    start_weekday = day_0_date.weekday() # 0 = Monday, ..., 6 = Sunday
    # Convert Python Monday=0 to Sunday=0
    start_wday = (start_weekday + 1) % 7

    week_idx = 0
    current_wday = start_wday

    rects_svg = ""

    for idx, d in enumerate(days):
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        wday = (dt.weekday() + 1) % 7 # 0 = Sun, 1 = Mon ...
        
        if idx > 0 and wday == 0:
            week_idx += 1

        # Check for month transition label
        if dt.month != last_month:
            if week_idx < max_weeks:
                month_headers.append((week_idx, MONTH_NAMES[dt.month - 1]))
            last_month = dt.month

        # Rect coordinates
        rx_val = grid_x_offset + (week_idx * box_stride)
        ry_val = grid_y_offset + (wday * box_stride)

        lvl = d.get("level", 0)
        c_info = COLOR_MAP.get(lvl, COLOR_MAP[0])

        delay = round(0.1 + (week_idx * 0.03), 2)

        rects_svg += f'''    <rect x="{rx_val}" y="{ry_val}" width="{box_size}" height="{box_size}" rx="2" ry="2" fill="{c_info['fill']}" stroke="{c_info['stroke']}" stroke-width="0.5" opacity="0">
      <title>{d['count']} contributions on {d['date']}</title>
      <animate attributeName="opacity" to="1" dur="0.2s" begin="{delay}s" fill="freeze" />
    </rect>\n'''

    # Add Month Headers SVG
    svg += f'  <!-- Month Headers -->\n  <g transform="translate(0, {month_y_offset})">\n'
    for w_i, m_name in month_headers:
        m_x = grid_x_offset + (w_i * box_stride)
        svg += f'    <text class="axis-label" x="{m_x}" y="0">{m_name}</text>\n'
    svg += '  </g>\n\n'

    # Add Contribution Squares SVG
    svg += f'  <!-- Contribution Heatmap Squares Grid -->\n  <g>\n{rects_svg}  </g>\n\n'

    # Legend & Footer Container
    legend_y = grid_y_offset + (7 * box_stride) + 22
    legend_x_start = card_width - 165

    svg += f'''  <!-- Heatmap Legend Footer -->
  <g transform="translate({legend_x_start}, {legend_y})">
    <text class="legend-text" x="-30" y="10">Less</text>
    <rect x="0" y="0" width="11" height="11" rx="2" fill="{COLOR_MAP[0]['fill']}" stroke="{COLOR_MAP[0]['stroke']}" stroke-width="0.5" />
    <rect x="15" y="0" width="11" height="11" rx="2" fill="{COLOR_MAP[1]['fill']}" stroke="{COLOR_MAP[1]['stroke']}" stroke-width="0.5" />
    <rect x="30" y="0" width="11" height="11" rx="2" fill="{COLOR_MAP[2]['fill']}" stroke="{COLOR_MAP[2]['stroke']}" stroke-width="0.5" />
    <rect x="45" y="0" width="11" height="11" rx="2" fill="{COLOR_MAP[3]['fill']}" stroke="{COLOR_MAP[3]['stroke']}" stroke-width="0.5" />
    <rect x="60" y="0" width="11" height="11" rx="2" fill="{COLOR_MAP[4]['fill']}" stroke="{COLOR_MAP[4]['stroke']}" stroke-width="0.5" />
    <text class="legend-text" x="78" y="10">More</text>
  </g>
</svg>
'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Successfully rendered Animated Heatmap SVG to '{output_path}'.")

if __name__ == "__main__":
    json_in = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    svg_out = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap.svg"
    render_heatmap_svg(json_in, svg_out)
