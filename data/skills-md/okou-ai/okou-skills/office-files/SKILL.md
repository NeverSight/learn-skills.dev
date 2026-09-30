---
name: office-files
description: Generate or edit docx, xlsx and PDF deliverables — Word documents, spreadsheets, reports — including editing a file the user uploaded.
---

## Setup — run these two lines first

```bash
pip install --break-system-packages --quiet pypandoc_binary typst openpyxl python-docx
export PATH="$(python3 -c 'import pypandoc,os;print(os.path.dirname(pypandoc.get_pandoc_path()))'):$PATH"
```

Takes about 6 seconds; nothing is preinstalled. Both lines are required — the system Python is PEP 668 externally managed, and the wheel ships the pandoc binary inside the package directory rather than on `PATH`.

**Install only what the flow needs, and know which package is which.** `pypandoc_binary` and `typst` cover the PDF flow and the prose-to-docx render; `openpyxl` is only for **xlsx**; `python-docx` is only for the **docx** steps that build or edit a reference doc. Installing just the first two is fine — until a later docx or xlsx step in the same session dies with `ModuleNotFoundError: No module named 'docx'` (or `openpyxl`). Install all four unless the task certainly never touches docx or xlsx.

**`export PATH` lasts for one shell only, so re-run it in every new shell.** Each Bash call starts a fresh shell, so a single setup at the top of a run does not carry forward and later calls fail with `pandoc: command not found`. Prefix the `export` line to each command that uses pandoc, or re-export it at the start of every shell.

If the install fails, deliver Markdown or a hosted HTML view instead and say the toolchain was unavailable. Never ship a worse format without saying so.

## Pick your flow

Every deliverable is **rendered from a source you author**. You never write a `.docx` or a `.pdf` directly:

```
prose  →  you write doc.md  →  pandoc                →  .docx
                             →  pandoc -t typst  →  .pdf
data   →  you build rows in Python  →  openpyxl  →  .xlsx
```

| Situation | Flow |
| --- | --- |
| Word document, user supplied a template | `pandoc doc.md --reference-doc=theirs.docx -o out.docx` — see **docx** |
| Word document, no template | `pandoc doc.md -o out.docx` — see **docx** |
| Word document needing a header, footer or page number, no template | build a reference doc first — see **docx** |
| PDF, no template | `pandoc doc.md -t typst -s -V papersize=a4` then `typst.compile` — see **PDF** |
| PDF carrying the user's branding | render the docx with `--reference-doc`, then convert that docx — see **PDF** |
| Spreadsheet | openpyxl — see **xlsx** |
| Edit a file the user sent | **Start from the user's file** first, then the matching row above |

Styling never comes from the source you author — it comes from a `.docx` passed to pandoc, or from openpyxl. Never author a spreadsheet as a Markdown table, and never hand-build docx XML.

## Start from the user's file

```bash
pandoc theirs.docx -t markdown --wrap=none > doc.md
```

Edit the Markdown, then render it back with the same `.docx` as `--reference-doc` so their styling survives the round trip. For xlsx, read with openpyxl — pandoc lists xlsx as an input format but fails on many real files.

## docx

**Step 1 — write the content as Markdown into `doc.md`.** Headings become Word heading styles, Markdown tables become Word tables, and `**bold**` becomes bold. This file is the source of truth; the docx is a render of it.

**Step 2 — render it:**

```bash
pandoc doc.md --reference-doc=theme.docx -o out.docx
pandoc doc.md --reference-doc=theme.docx --toc --toc-depth=2 -o out.docx   # with a table of contents
```

`--reference-doc` is where headers, footers, page numbers, margins, paper size, fonts and numbering come from: the output inherits `word/header1.xml` and `word/footer1.xml`, including a live `PAGE` field. **Never write headers, footers or page numbers into the Markdown.**

- **User supplied a Word file** — use it as the reference doc. Their branding comes across for free.
- **No template** — omit the flag. The result is clean but unbranded, with no header, footer or page number. Say that in one line when you deliver it, and offer to match their house style if they send you a Word file.
- **No template, but the request needs a header, footer or page numbers** — build one from pandoc's own default, never from a blank document:

```bash
pandoc --print-default-data-file reference.docx > theme.docx
```

Then open `theme.docx` with python-docx, set `section.header`, add a `PAGE` field to `section.footer`, save, and pass it with `--reference-doc`. A blank `python-docx.Document()` lacks the styles pandoc emits, so Word silently renders them as Normal.

## PDF

Same `doc.md` as the docx flow — write the Markdown first, then render through typst:

```bash
pandoc doc.md -t typst -s -V papersize=a4 -o doc.typ
python3 -c "import typst; typst.compile('doc.typ', output='doc.pdf')"
```

For Chinese, Japanese or Korean text, add the matching font — `-V mainfont="Noto Sans CJK SC"` (use `JP` or `KR` for those languages).

Three things that fail quietly here:

- **`-s` is mandatory for any `-V` to apply.** Without it pandoc emits a fragment whose `.typ` contains no `set page` or `set text` at all, so every variable you pass is silently dropped.
- **Pin `papersize`.** Without `-s` you get typst's own default of A4; with `-s` and no `papersize` you get pandoc's template default of `us-letter`. Same document, different paper.
- **CJK without `mainfont` renders in the wrong script.** Chinese text falls back to `NotoSansCJKjp`, so you get Japanese glyph forms with no error and no missing characters. Verify with `pdffonts doc.pdf` — the embedded name must end in `sc` for Simplified Chinese.

One message from this flow is loud but harmless, and it is the opposite of the three above: `pdfinfo` on a typst-built PDF prints `Syntax Error: Suspects object is wrong type (boolean)` to stderr. It is a poppler bug and not a broken file: poppler mis-reports the valid `/Suspects false` that typst writes for tagged output (fixed upstream after poppler 25.11.0), while PDFs built by LibreOffice omit that key and so stay quiet. The same PDF still reports its page count, page size and fonts correctly and rasterises fine. Do not debug it and do not re-render because of it.

Variable names come from `pandoc --print-default-template=typst`: `mainfont`, `mathfont`, `codefont`, `fontsize`, `papersize`.

**`--reference-doc` does not apply to PDF** — only docx, pptx and ODT support it, so the typst flow above always produces an unbranded PDF. When the user needs their branding on a PDF, render the docx with their reference doc first, then convert that docx:

```bash
soffice --headless -env:UserInstallation=file:///tmp/lo --convert-to pdf --outdir . out.docx 2>&1 | grep -q writer_pdf_Export \
  || { sudo apt-get update -qq && sudo apt-get install -y -qq libreoffice-writer
       soffice --headless -env:UserInstallation=file:///tmp/lo --convert-to pdf --outdir . out.docx; }
```

Convert first and install only on failure. Three things make that ordering necessary:

- **`libreoffice-writer` is absent from the image.** Only `-impress` and `-draw` ship, so the Writer filters do not exist and a bare `soffice` fails with `Error: source file could not be loaded`. Installing it pulls 9 packages. Budget about 180 MB of disk: 52 MB of package files, 13 MB of downloaded debs, and — the part that dominates — 111 MB of package indexes written into `/var/lib/apt/lists/` by the `apt-get update` the line above requires.
- **`apt-get update` has to come first.** `/var/lib/apt/lists/` ships empty, so installing without it reports `Package 'libreoffice-writer' has no installation candidate`, which reads like the package is missing from the archive rather than uncached.
- **The root filesystem can be rolled back mid-run.** Observed in this sandbox: an install that worked earlier in a run was gone later, and `pip --user` packages with it. Only `/home/user/workspace` was unaffected. Re-running the line above recovers.

The install needs passwordless `sudo` and the Ubuntu archive. Where either is missing the convert keeps failing with `Error: source file could not be loaded`; deliver the docx together with the unbranded typst PDF and say the branded export was unavailable, rather than quietly handing over the unbranded one.

Fonts, line spacing and justification all survive the conversion, so the result is good enough to deliver. The `w:header` and `w:footer` offsets in `pgMar` do not: converting a template whose source puts the running head at 47.62pt, LibreOffice placed it at 49.85pt. That is measured against the source document, not against Word — nothing in this section has been checked in Word itself.

## xlsx

```python
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Q3"
ws.append(["Region", "Q2", "Q3", "Delta"])
ws.append(["APAC", 120, 148])
ws["D2"] = "=C2-B2"          # formulas are written as strings
wb.create_sheet("Notes")
wb.save("book.xlsx")
```

Excel evaluates formulas when the file opens, so when the file itself must already carry computed values, compute them yourself and write both the formula and the number.

## Deliver

`okou web upload-file`. When prose is final and being sent onward, attach both the PDF and the docx source: the recipient gets something fixed and something they can still edit.

## Never use

- `soffice` on a docx before installing `libreoffice-writer`, or on an xlsx at all — the image ships only `libreoffice-impress` and `libreoffice-draw`, so the Writer and Calc filters do not exist and the convert fails with `Error: source file could not be loaded`. For docx to PDF, install Writer first — see **PDF**. For spreadsheets, use openpyxl.
- `chromium --headless --print-to-pdf` — produces no file.
- `weasyprint` as a pandoc `--pdf-engine` — exits non-zero.
- `pandoc -o out.xlsx` — pandoc has no xlsx writer.

## Worked example — one report delivered as docx and PDF

```bash
pandoc --print-default-data-file reference.docx > theme.docx
python3 - <<'PY'
import docx
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

d = docx.Document("theme.docx")
s = d.sections[0]
s.header.paragraphs[0].text = "ACME — Internal"
p = s.footer.paragraphs[0]
p.text = "Page "
r = p.add_run()
f = OxmlElement("w:fldSimple")
f.set(qn("w:instr"), "PAGE")
r._r.addnext(f)
d.save("theme.docx")
PY
pandoc report.md --reference-doc=theme.docx --toc --toc-depth=2 -o report.docx
pandoc report.md -t typst -s -V papersize=a4 -o report.typ
python3 -c "import typst; typst.compile('report.typ', output='report.pdf')"
```
