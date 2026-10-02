---
name: xlsx-to-markdown
description: Convert a multi-tab Excel workbook with embedded images, flow diagrams, and text into faithful Markdown — one Excel-fidelity PNG per sheet plus searchable extracted text (strikethrough preserved). Use when the user wants to read, extract, render, or convert an .xlsx (especially with mixed text+images, screenshots, flow/swimlane diagrams across many tabs), when images come out blurry or split across pages, or when a spreadsheet must be turned into clear images or markdown.
---

# xlsx → faithful Markdown

Turns a workbook where **text and images are laid out together across many tabs**
into: per-sheet PNGs that look exactly like Excel (sharp, not split) + the cell
text as searchable Markdown.

## Quick start

```bash
python3 scripts/xlsx_to_md.py "INPUT.xlsx" OUTDIR [--dpi 200]
```
Produces `OUTDIR/<name>.md` and `OUTDIR/render/tab1.png … tabN.png`.
Each tab section = the rendered image + a `<details>` block of extracted text.

## How it works (and the core lesson)

A flow diagram's meaning lives in its **2D layout + arrows + labels** — extracting
the embedded sprite images individually loses that. So render the whole sheet.

Fidelity = **render at 100% scale (no fit-to-page) on a huge page so nothing is
split, then trim whitespace.** It is NOT about DPI:
- **Text/arrows/shapes** are vector → DPI helps, no ceiling.
- **Embedded screenshots** are raster with fixed source pixels → cranking DPI just
  interpolates (stays blurry). Shrinking them (fit-to-page) is what causes blur.
- So never `fitToHeight=1`/fit-to-page for fidelity; keep `scale=100`. 200 dpi is
  plenty to capture native pixels; higher only sharpens vector text.

The script (see `scripts/xlsx_to_md.py`):
1. Unzip xlsx; read `workbook.xml` (sheet order), `sharedStrings.xml`.
2. Extract text per sheet in row order. Strip furigana (`<rPh>`); render
   strikethrough runs (`<strike/>`) as `<del>…</del>` (= author's "delete" intent).
3. Inject `<pageSetup paperWidth/Height="3000mm" scale="100" orientation="landscape"/>`
   + `pageSetUpPr fitToPage="0"` into each sheet.
4. Rewrite every requested font that isn't installed on this machine to an installed
   CJK-capable one (see **Fonts** below); re-zip.
5. `soffice --headless --convert-to pdf` (one big page per sheet, nothing split).
6. Probe content size per page at 50 dpi (`magick -trim`), then `pdftoppm` each page
   cropped to content at target dpi, `magick -trim` the result.
7. Emit Markdown: per tab → image + collapsible extracted text.

## Fonts — the #1 cause of garbled output

Symptom: **adjacent runs in one cell overlap** (`URLが~~SMS~~LINEWORKS` renders as
`SMSLINEWORKS` collided) and words get spurious gaps (`LI NEWORKS`).

Cause: the workbook asks for a font that isn't installed (Japanese workbooks almost
always want `Meiryo UI` / `游ゴシック` / `Yu Gothic` / `MS Pゴシック`). LibreOffice
falls back to whatever covers the glyphs — on macOS often `Hiragino Sans GB` (Chinese)
or `AquaKana` — whose advance widths differ from the requested font, so run-by-run
layout drifts and collides. It is **not** a DPI or rendering-quality issue.

Fix: the script rewrites unavailable font names to an installed fallback before
conversion (prefers `Noto Sans JP`, then `Noto Sans CJK JP`, `BIZ UDPGothic`,
`BIZ UDGothic`, `Hiragino Sans`, …). It prints what it substituted:
```
     fonts: Aptos Display, Meiryo UI, 游ゴシック -> "Noto Sans JP" (9 xml files)
```
Install at least one CJK font so a fallback exists:
```bash
brew install --cask font-noto-sans-jp font-biz-udgothic
```
- `--font-fallback "BIZ UDPGothic"` to pick the substitute yourself.
- `--no-font-substitution` to keep original names (only if the real fonts are installed).
- Availability is probed with `fc-list`; without it substitution is skipped with a warning.
- Substitution changes metrics slightly, so line wrapping (and thus PNG height) can
  differ a little from Excel on Windows. Correct glyphs beat exact wrapping.
- Per-script theme fonts (`<a:font script="Thai" …/>`) are left untouched.

## Dependencies

Needs three CLIs: `soffice` (LibreOffice), `pdftoppm` (poppler), `magick` (ImageMagick).
```bash
brew install poppler imagemagick
```

**LibreOffice install** — try `brew install --cask libreoffice` first. If it fails
with a macOS-version error (stale cask on a new OS), install the official dmg:
```bash
# pick arch: aarch64 (Apple Silicon) or x86-64 (Intel)
V=$(curl -fsSL https://download.documentfoundation.org/libreoffice/stable/ \
    | grep -oE '[0-9]+\.[0-9]+\.[0-9]+/' | sort -V | tail -1 | tr -d /)
curl -fL -o /tmp/LO.dmg \
  "https://download.documentfoundation.org/libreoffice/stable/$V/mac/aarch64/LibreOffice_${V}_MacOS_aarch64.dmg"
hdiutil attach /tmp/LO.dmg -nobrowse -quiet
cp -R "/Volumes/LibreOffice/LibreOffice.app" ~/Applications/   # /Applications needs admin
hdiutil detach "/Volumes/LibreOffice" -quiet
xattr -dr com.apple.quarantine ~/Applications/LibreOffice.app
```
The script auto-detects soffice in PATH, `/Applications`, and `~/Applications`
(or pass `--soffice /path/to/soffice`).

## Notes & gotchas

- One PNG per sheet covers the **entire used range** (tables + diagrams + screenshots),
  so text-heavy and image-heavy tabs both render completely.
- `--paper-mm` (default 3000) must exceed the widest sheet at 100% scale, else that
  sheet splits across pages. Bump it for unusually wide workbooks.
- `--dpi 200` default; raise to 300 only if vector text needs to be sharper (bigger files).
- Need the absolute sharpest single screenshot? The originals are in `xl/media/`
  inside the unzipped xlsx — that's the native-resolution ceiling.
- To isolate just a diagram, set a print area (defined name `_xlnm.Print_Area`) to its
  cell range before step 4; otherwise the whole sheet is rendered.
