# flowers

A fragrant-flower calendar for the Berkeley, CA area: `flower.md` (bilingual
English/Chinese table, sorted by bloom month Dec → Sep, with footnotes and
400×400 photos in `assets/flowers/`) and its rendered A4 print version
`flower.pdf`.

## Files

| File | What it is |
| --- | --- |
| `flower.md` | The source document. The flower table is a **GFM pipe table** (one line per row). |
| `flower.pdf` | A4 render of `flower.md`. It is a **static snapshot** — re-render it after any edit to `flower.md`. |
| `render_pdf.py` | The PDF render script (pandoc + headless Chromium). |
| `assets/flowers/` | 22 flower photos (source/license per image: "Image credits" section in `flower.md`). |

## Formatting `flower.md` (markdown)

Prose is wrapped at 80 columns (one-time pass from PR #14 with
`mdformat --wrap 80`). The flower table is a GFM pipe table; GFM requires
its cells to be **single lines**, so table rows run to ~1400 characters —
that is inherent to the format (it is what makes GitHub render the table).

Rules for keeping the file healthy:

1. If you re-run `mdformat`, it **must have the GFM/table plugins**
   (`mdformat-gfm`, `mdformat-tables`): they recognize pipe tables and
   realign them onto single lines. Plain mdformat (CommonMark core) has no
   table grammar at all and will shred the table into wrapped prose.
2. Keep exactly seven `|` on every table row (header, separator and the 22
   data rows). One row with a missing trailing `|` terminates the table for
   strict parsers and demotes every following row to a paragraph (the PR #13
   bug).
3. The name cells contain raw HTML (`<br>` + `<img ... />`); pandoc, GFM and
   mdformat-gfm all pass it through — don't "tidy" it into other syntax.

## Rendering `flower.pdf`

Setup (Debian/Ubuntu; macOS equivalents: `brew install pandoc`, a CJK font
such as `Noto Sans CJK`):

    sudo apt-get install pandoc fonts-droid-fallback
    pip install playwright
    playwright install chromium

Render:

    python render_pdf.py

The script runs exactly these two stages:

1. `pandoc -f markdown-smart-tex_math_dollars -t html5 --wrap=preserve flower.md`
   → HTML fragment (`smart` keeps curly quotes/dashes; `tex_math_dollars`
   prevents `$` signs and `$...$`-looking text from being treated as TeX
   math), wrapped in a minimal HTML document with the print CSS,
2. prints it to A4 with headless Chromium (fixed table column widths,
   150 px photo width, no page breaks inside table rows).

Verify the result: the PDF must contain all 22 table rows (including the
photos), footnotes [1]–[8], and the Image credits section.
