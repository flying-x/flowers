# Berkeley fragrant flower reference

A bilingual (English/Chinese) fragrant-flower calendar for the Berkeley, CA
area. `flowers.md` lists 22 scent plants sorted by bloom start (December →
September), with a climate section, footnotes, and 400×400 photos in
`assets/flowers/`; `flowers.pdf` is its A4 print version.

## Files

- `flowers.md` — the source document. The flower table is a **raw HTML
  `<table>`** (not a GFM pipe table — see below).
- `flowers.pdf` — A4 render of `flowers.md`. It is a **static snapshot** —
  re-render it after any edit to `flowers.md`.
- `render_pdf.py` — the PDF render script (pandoc + headless Chromium).
- `assets/flowers/` — 22 flower photos (source/license per image: the "Image
  credits" section in `flowers.md`).

## Why the table is raw HTML

GFM pipe tables are the only table syntax GitHub renders, but their rows must be
**single lines** — there is no pipe-table syntax to wrap a row, so each of our
rows runs to ~1400 characters (unreadable in an editor). Grid tables wrap, but
GitHub's renderer (cmark-gfm) shows them as raw `+---+` text. A raw HTML
`<table>` satisfies both constraints:

- source lines wrap at ~80 columns (editable, diff-friendly);
- table elements are in the GFM raw-HTML whitelist, so GitHub renders the table
  (it wraps it in `<markdown-accessiblity-table>` with the same styling as GFM
  tables) — verified on this repo's file;
- pandoc passes raw HTML blocks through unchanged, so the same render pipeline
  works;
- mdformat treats raw HTML blocks as atomic, so it cannot shred the table (plain
  mdformat's CommonMark core has no table grammar at all).

## Formatting `flowers.md`

1. Keep the table a raw HTML `<table>`: 22 rows × 6 columns, wrapped at ~80
   columns (the only lines longer are the `<img>` tag lines).
1. Inside cells, use HTML inline tags — `<em>`/`<strong>`, not
   `*em*`/`**strong**` (markdown emphasis does not work inside raw HTML) — and
   escape stray angle brackets (`pH<6` → `pH&lt;6`).
1. Name cells carry raw HTML too: `<br>` +
   `<img src="assets/flowers/..." alt="..." />`. pandoc, GFM and mdformat all
   pass it through; don't convert it to other syntax.
1. The surrounding prose may be formatted with `mdformat --wrap 80 flowers.md` —
   it leaves the raw HTML table block untouched.
1. Keep both ASCII double quotes and the half-width parentheses; the pandoc
   flags below (`-f markdown-smart-...`) are chosen partly to match this
   convention.

## Rendering `flowers.pdf`

Setup (Debian/Ubuntu; macOS: `brew install pandoc` and a CJK font such as
`Noto Sans CJK`):

```
sudo apt-get install pandoc fonts-droid-fallback
pip install playwright pypdf
playwright install chromium
```

Render:

```
python render_pdf.py
```

The script runs exactly two stages:

1. `pandoc -f markdown-smart-tex_math_dollars -t html5 --wrap=preserve flowers.md`
   → HTML fragment (`smart` keeps curly quotes/dashes; `tex_math_dollars` stops
   `$` signs from becoming TeX math), wrapped in a minimal HTML document with
   the print CSS (the same CSS is in `render_pdf.py`),
1. print to A4 with headless Chromium (fixed table column widths, 150 px photo
   width, no page breaks inside rows).

Two CSS details are load-bearing — do not drop them:

- `table { table-layout: fixed }` plus explicit `td:nth-child(n)` column widths
  (17/9/22/16/13/23 %). Without them, pandoc's `<colgroup>` width hints crush
  the narrow "Chinese name" column to ~2 % of the page width.
- `tr { page-break-inside: avoid }` keeps each row (photo included) on one page;
  do not add `emulate_media` or header/footer options to the Chromium call — any
  change to the print options shifts pagination.

Verify the result: the PDF must contain all 22 table rows (with photos),
footnotes [1]–[8], and the Image credits section (7 pages currently).
