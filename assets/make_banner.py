"""Generates the ops-console banner for the profile README.

The waveform is deterministic (no RNG) so re-running never changes the asset.
Its envelope is shaped like a spoken sentence: attack, sustain, decay, a breath,
then a shorter second clause. That is the whole point of the mark — it is the
signal whisperflow-local listens to and the signal stock-news-monitor scores.
"""

import math

W, H = 1200, 260

BG = "#0B0F16"
EDGE = "#1C2431"
AMBER = "#F5A524"
FG = "#E6EDF3"
MUTED = "#7D8899"
FAINT = "#4E5967"

MONO = "ui-monospace, 'Cascadia Mono', 'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace"


def envelope(i, n):
    """Speech-shaped amplitude in 0..1 for bar i of n."""
    t = i / (n - 1)
    # two clauses separated by a breath around t=0.58
    clause = math.sin(math.pi * min(t / 0.52, 1.0)) if t < 0.52 else 0.0
    if t >= 0.62:
        clause = math.sin(math.pi * ((t - 0.62) / 0.38)) * 0.72
    # syllable texture
    texture = 0.55 + 0.45 * abs(math.sin(t * 22.0 + 0.7))
    return max(0.06, clause * texture)


def waveform():
    x0, x1 = 706, 1144
    pitch, bw = 10, 4
    n = (x1 - x0) // pitch
    mid = 128
    out = []
    for i in range(n):
        a = envelope(i, n)
        h = max(3, a * 84)
        x = x0 + i * pitch
        out.append(
            f'<rect x="{x}" y="{mid - h / 2:.1f}" width="{bw}" height="{h:.1f}" '
            f'rx="1.5" fill="{AMBER}"/>'
        )
    return "\n      ".join(out)


def hairlines():
    """Faint vertical rules — a console grid, not decoration for its own sake."""
    return "\n    ".join(
        f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{EDGE}" stroke-width="1"/>'
        for x in range(120, W, 120)
    )


svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Ankit Keshari — builds AI systems that run without him">
  <defs>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="0.28" stop-color="#fff" stop-opacity="0.85"/>
      <stop offset="0.78" stop-color="#fff" stop-opacity="0.5"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0.08"/>
    </linearGradient>
    <mask id="wavemask">
      <rect x="690" y="0" width="{W - 690}" height="{H}" fill="url(#fade)"/>
    </mask>
  </defs>

  <rect width="{W}" height="{H}" fill="{BG}"/>
  <g opacity="0.5">
    {hairlines()}
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="{EDGE}"/>

  <g mask="url(#wavemask)">
      {waveform()}
  </g>

  <rect x="56" y="60" width="3" height="14" fill="{AMBER}"/>
  <text x="72" y="72" font-family="{MONO}" font-size="13" letter-spacing="4.5" fill="{AMBER}">SYSTEMS ONLINE</text>

  <text x="56" y="146" font-family="{MONO}" font-size="54" font-weight="700" letter-spacing="4" fill="{FG}" textLength="560" lengthAdjust="spacingAndGlyphs">ANKIT KESHARI</text>

  <text x="58" y="184" font-family="{MONO}" font-size="17" letter-spacing="0.4" fill="{MUTED}">builds AI systems that run without him</text>

  <line x1="58" y1="204" x2="640" y2="204" stroke="{EDGE}" stroke-width="1"/>

  <text x="58" y="228" font-family="{MONO}" font-size="12.5" letter-spacing="2.4" fill="{FAINT}">NEW DELHI</text>
  <circle cx="188" cy="224" r="2" fill="{AMBER}"/>
  <text x="204" y="228" font-family="{MONO}" font-size="12.5" letter-spacing="2.4" fill="{FAINT}">NIT DELHI '27</text>
  <circle cx="368" cy="224" r="2" fill="{AMBER}"/>
  <text x="384" y="228" font-family="{MONO}" font-size="12.5" letter-spacing="2.4" fill="{FAINT}">AI INTERN @ EY</text>
</svg>
"""

with open("banner.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("wrote banner.svg")
