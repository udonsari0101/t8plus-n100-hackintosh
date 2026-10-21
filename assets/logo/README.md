# Logo — character-art source

An original, unofficial community emblem for this project: a classic six-colour
**rainbow Apple** silhouette (bitten, with a leaf) rendered as a dense ASCII /
Unicode character matrix, with a bright-blue lowercase **`intel`** wordmark and
oval crossing horizontally through its centre and protruding on both sides.
Inspired by classic text-mode / ANSI art — **not** an official Apple or Intel
mark, and not a claim of any partnership.

| File | Role |
|---|---|
| `logo.txt` | **Canonical source** — the editable UTF-8 character matrix (also the plain-text fallback). |
| `render_logo.py` | Deterministic generator: derives colours from `logo.txt` and writes the two SVGs. No dependencies, no network. |
| `logo-light.svg` | Colourised render tuned for the GitHub **light** canvas. |
| `logo-dark.svg` | Colourised render tuned for the GitHub **dark** canvas. |

**Colour rules** (applied by `render_logo.py`, so editing `logo.txt` is enough):

- The Intel oval + `intel` wordmark use the glyphs `@` and `*` (plus the edge
  glyphs `. : +` that fall between the first and last `@`/`*` on a row) →
  electric blue.
- Every other apple-body glyph (`# & % + : .`) → one of six horizontal rainbow
  bands by row (green at the top → cyan/blue at the bottom), per `BANDS`.

Rebuild after editing the art:

```sh
python render_logo.py
```

The README swaps the two SVGs with `<picture>` + `prefers-color-scheme`. The
background is transparent and every colour run is positioned with `textLength` +
`spacingAndGlyphs`, so alignment is exact regardless of the viewer's monospace
font.
