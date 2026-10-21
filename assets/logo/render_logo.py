#!/usr/bin/env python3
"""Render the rainbow-Apple x blue-intel character-art logo to themed SVGs.

Single source of truth: `logo.txt` -- the canonical UTF-8 character matrix
(the plain-text fallback). Colours are DERIVED from it by deterministic rules,
so editing the art is enough (no separate colour file to keep in sync):

  * the Intel oval + lowercase `intel` wordmark use the glyphs `@` and `*`, plus
    the edge glyphs `. : +` that fall between the first and last `@`/`*` on a
    row -> electric blue (code `I`);
  * every other apple-body glyph (`# & % + : .`) -> one of six horizontal
    rainbow bands by row (green at the top, cyan/blue at the bottom), per BANDS.

Writes `logo-light.svg` and `logo-dark.svg`; the README swaps them with
`<picture>` + prefers-color-scheme. Each colour run is positioned at its start
column with textLength + spacingAndGlyphs, so alignment is exact regardless of
the viewer's monospace metrics. Background is transparent.

Run:  python render_logo.py      (no third-party dependencies, no network)
"""
import os

FS = 16.0
CELL_W = FS * 0.60
CELL_H = FS * 0.92
PAD = FS * 0.5
BASE = FS * 0.78
FONT = ("ui-monospace,SFMono-Regular,Menlo,'Cascadia Mono',"
        "Consolas,'DejaVu Sans Mono',monospace")

# six-colour rainbow band start rows (inclusive), tuned so all six show around
# the central Intel oval; green at top -> cyan/blue at bottom.
BANDS = [(0, "G"), (4, "Y"), (8, "O"), (11, "R"), (24, "V"), (28, "B")]
OVAL_CHARS = set("@*")
EDGE_CHARS = set(".:+")

PAL_DARK = {
    "G": "#5FB44A", "Y": "#F6B600", "O": "#F07E17",
    "R": "#E23B3B", "V": "#9A52B8", "B": "#3566D6",
    "I": "#33CFFF",   # electric Intel blue
}
PAL_LIGHT = {
    "G": "#4FA83C", "Y": "#E09400", "O": "#E86F0C",
    "R": "#D83232", "V": "#7E3A9A", "B": "#2A4FC0",
    "I": "#0AA3E8",
}

HERE = os.path.dirname(os.path.abspath(__file__))


def band(row):
    code = BANDS[0][1]
    for start, c in BANDS:
        if row >= start:
            code = c
    return code


def load_cells():
    lines = open(os.path.join(HERE, "logo.txt"), encoding="utf-8").read().split("\n")
    while lines and lines[-1] == "":
        lines.pop()
    cells = []
    for r, line in enumerate(lines):
        cols = [c for c, ch in enumerate(line) if ch in OVAL_CHARS]
        lo, hi = (min(cols), max(cols)) if cols else (1, 0)
        row = []
        for c, ch in enumerate(line):
            if ch == " " or ch == "":
                row.append((" ", None))
            elif ch in OVAL_CHARS or (ch in EDGE_CHARS and lo <= c <= hi):
                row.append((ch, "I"))
            else:
                row.append((ch, band(r)))
        cells.append(row)
    return cells


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def runs(row):
    run, start = [], 0
    for i, (ch, code) in enumerate(row):
        if code is None:
            if run:
                yield start, run
                run = []
            continue
        if not run:
            start, run = i, [(ch, code)]
        elif code == run[-1][1]:
            run.append((ch, code))
        else:
            yield start, run
            start, run = i, [(ch, code)]
    if run:
        yield start, run


def render(cells, palette):
    ncols = max((len(r) for r in cells), default=0)
    W = PAD * 2 + ncols * CELL_W
    H = PAD * 2 + len(cells) * CELL_H
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" '
        f'width="{W:.0f}" height="{H:.0f}" font-family="{FONT}" '
        f'font-size="{FS:.2f}" font-weight="600" role="img" '
        f'aria-label="Rainbow Apple silhouette with a blue intel wordmark across its centre '
        f'-- macOS on Intel N100 (unofficial community artwork)">',
        f'<style>text{{font-family:{FONT};font-weight:600;font-size:{FS:.2f}px;'
        f'white-space:pre;}}</style>',
    ]
    for r, row in enumerate(cells):
        y = PAD + r * CELL_H + BASE
        for start, run in runs(row):
            text = esc("".join(ch for ch, _ in run))
            x = PAD + start * CELL_W
            tl = len(run) * CELL_W
            out.append(
                f'<text x="{x:.2f}" y="{y:.2f}" fill="{palette[run[0][1]]}" '
                f'textLength="{tl:.2f}" lengthAdjust="spacingAndGlyphs" '
                f'xml:space="preserve">{text}</text>'
            )
    out.append("</svg>")
    return "\n".join(out)


def main():
    cells = load_cells()
    for name, pal in (("light", PAL_LIGHT), ("dark", PAL_DARK)):
        with open(os.path.join(HERE, f"logo-{name}.svg"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(render(cells, pal) + "\n")
    print(f"rendered logo-light.svg + logo-dark.svg  ({len(cells[0])}x{len(cells)} cells)")


if __name__ == "__main__":
    main()
