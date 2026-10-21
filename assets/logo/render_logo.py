#!/usr/bin/env python3
"""Render the Firebat T8 Plus character-art logo to themed SVGs.

Reads two maintainable, aligned source files:
  logo.txt   - the canonical UTF-8 character art (one glyph per cell; the
               plain-text fallback)
  logo.cmap  - the colour map (one code per cell; '.' = transparent)

and writes:
  logo-light.svg  - neutrals tuned for the GitHub light canvas
  logo-dark.svg   - neutrals tuned for the GitHub dark canvas

The README swaps them with <picture> + prefers-color-scheme. Each colour run
is positioned at its start column with textLength + spacingAndGlyphs, so
horizontal alignment is exact regardless of the viewer's monospace metrics.
The background is transparent.

Colour codes:
  G Y O R V B  classic Macintosh six-colour rainbow (the bitten apple)
  c s e        cool-blue / silver / steel silicon (the Intel N100 die)
  W w          ink wordmark / muted sub-label (flip per theme)

Run:  python render_logo.py      (no third-party dependencies)
"""
import os

FS = 16.0
CELL_W = FS * 0.60
CELL_H = FS * 0.92
PAD = FS * 0.5
BASE = FS * 0.78
FONT = ("ui-monospace,SFMono-Regular,Menlo,'Cascadia Mono',"
        "Consolas,'DejaVu Sans Mono',monospace")
BLANKS = {" ", "⠀", "", "."}

PAL_DARK = {
    "G": "#5FB44A", "Y": "#F6B600", "O": "#F07E17",
    "R": "#E23B3B", "V": "#9A52B8", "B": "#2BA3DE",
    "c": "#5AA9E6", "s": "#AEB9C6", "e": "#8795A6",
    "W": "#E6EDF3", "w": "#9DA7B3",
}
PAL_LIGHT = {
    "G": "#4FA83C", "Y": "#E09400", "O": "#E86F0C",
    "R": "#D83232", "V": "#7E3A9A", "B": "#1388C4",
    "c": "#2E86C8", "s": "#8A94A2", "e": "#5E6B7A",
    "W": "#1F2328", "w": "#55606C",
}

HERE = os.path.dirname(os.path.abspath(__file__))


def load_grid():
    g = open(os.path.join(HERE, "logo.txt"), encoding="utf-8").read().split("\n")
    c = open(os.path.join(HERE, "logo.cmap"), encoding="utf-8").read().split("\n")
    while g and g[-1] == "":
        g.pop()
    while c and c[-1] == "":
        c.pop()
    rows = []
    for gi, ci in zip(g, c):
        ci = (ci + "." * len(gi))[:len(gi)]
        rows.append([(gi[i], ci[i]) for i in range(len(gi))])
    return rows


def _runs(row):
    run, start = [], 0
    for i, (ch, code) in enumerate(row):
        if ch in BLANKS or code == ".":
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


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(rows, palette):
    ncols = max((len(r) for r in rows), default=0)
    W = PAD * 2 + ncols * CELL_W
    H = PAD * 2 + len(rows) * CELL_H
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" '
        f'width="{W:.0f}" height="{H:.0f}" font-family="{FONT}" '
        f'font-size="{FS:.2f}" font-weight="600" role="img" '
        f'aria-label="Firebat T8 Plus - macOS Sonoma on an Intel N100 (unofficial community artwork)">',
        f'<style>text{{font-family:{FONT};font-weight:600;font-size:{FS:.2f}px;'
        f'white-space:pre;}}</style>',
    ]
    for r, row in enumerate(rows):
        y = PAD + r * CELL_H + BASE
        for start, run in _runs(row):
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
    rows = load_grid()
    for name, pal in (("light", PAL_LIGHT), ("dark", PAL_DARK)):
        svg = render(rows, pal)
        with open(os.path.join(HERE, f"logo-{name}.svg"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(svg + "\n")
    print(f"rendered logo-light.svg + logo-dark.svg  ({len(rows[0])}x{len(rows)} cells)")


if __name__ == "__main__":
    main()
