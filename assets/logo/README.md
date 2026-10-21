# Logo — character-art source

An original, unofficial community emblem for this project: a classic-Macintosh
six-colour **rainbow apple** rendered in Braille halftone, wired to an **Intel
N100** silicon die drawn in box-drawing glyphs, inside an ANSI/BBS-style title
frame. Inspired by classic text-mode / BBS character art — **not** an official
Apple or Intel mark, and not a claim of any partnership.

| File | Role |
|---|---|
| `logo.txt` | Canonical character art — one glyph per cell (the plain-text fallback). |
| `logo.cmap` | Colour map — one code per cell, aligned to `logo.txt` (`.` = transparent). |
| `render_logo.py` | Deterministic generator: `logo.txt` + `logo.cmap` → the two SVGs. No dependencies. |
| `logo-light.svg` | Colourised render tuned for the GitHub **light** canvas. |
| `logo-dark.svg` | Colourised render tuned for the GitHub **dark** canvas. |

Colour codes: `G Y O R V B` = the six-colour rainbow (apple); `c s e` =
cool-blue / silver / steel (silicon); `W w` = wordmark / muted sub-label.

Rebuild after editing the source:

```sh
python render_logo.py
```

The README swaps the two SVGs with `<picture>` + `prefers-color-scheme`, so the
wordmark/silicon neutrals stay legible on both themes while the rainbow (vivid
in both) and the transparent background carry across. Each colour run is
positioned with `textLength` + `spacingAndGlyphs`, so alignment is exact
regardless of the viewer's monospace font.
