#!/usr/bin/env python3
"""Render flowers.md to flowers.pdf (US Letter) via pandoc + headless Chromium.

Requires: pandoc (3.x), the `playwright` Python package with Chromium
installed (`playwright install chromium`), and a CJK font for the Chinese
text (e.g. Debian/Ubuntu `fonts-droid-fallback`; on macOS any CJK font
such as "Noto Sans CJK SC" or PingFang works).

Usage:  python render_pdf.py
Output: flowers.pdf (flowers.html is left behind as a build artifact)
"""
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
MD, HTML, PDF = HERE / "flowers.md", HERE / "flowers.html", HERE / "flowers.pdf"

CSS = """
@page { size: Letter; margin: 14mm 12mm; }
body { font-family: "DejaVu Sans","Droid Sans Fallback",sans-serif; font-size: 11px; color:#1a1a1a; line-height:1.45; }
h1 { font-size: 20px; border-bottom: 2px solid #444; padding-bottom: 6px; }
h2 { font-size: 15px; margin-top: 22px; color: #2c5f2d; }
table { border-collapse: collapse; width: 100%; table-layout: fixed; }
th, td { border: 1px solid #bbb; padding: 5px 6px; vertical-align: top; word-wrap: break-word; font-size: 10px; }
th { background: #eef3ee; font-size: 10.5px; }
tr { page-break-inside: avoid; }
img { width: 150px !important; height: auto !important; display: block; margin: 4px auto 0; border-radius: 4px; }
code { background:#f0f0f0; padding: 1px 3px; }
blockquote { border-left: 3px solid #ccc; margin-left: 0; padding-left: 10px; color:#444; }
strong { color: #111; }
td:nth-child(1),th:nth-child(1) { width:17% }
td:nth-child(2),th:nth-child(2) { width:9% }
td:nth-child(3),th:nth-child(3) { width:22% }
td:nth-child(4),th:nth-child(4) { width:16% }
td:nth-child(5),th:nth-child(5) { width:13% }
td:nth-child(6),th:nth-child(6) { width:23% }
"""

body = subprocess.run(
    ["pandoc", "-f", "markdown-smart-tex_math_dollars", "-t", "html5",
     "--wrap=preserve", str(MD)],
    capture_output=True, check=True, text=True,
).stdout
html = (f'<!DOCTYPE html><html><head><meta charset="utf-8">'
        f"<style>{CSS}</style></head><body>{body}</body></html>")
HTML.write_text(html, encoding="utf-8")

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page()
    pg.goto(HTML.as_uri(), wait_until="networkidle", timeout=60000)
    pg.evaluate("document.fonts.ready.then(()=>{})")
    pg.pdf(path=str(PDF), format="Letter", print_background=True,
           margin={"top": "14mm", "bottom": "14mm", "left": "12mm", "right": "12mm"})
    b.close()

from pypdf import PdfReader
print("pages:", len(PdfReader(str(PDF)).pages))
print("pdf bytes:", PDF.stat().st_size)
