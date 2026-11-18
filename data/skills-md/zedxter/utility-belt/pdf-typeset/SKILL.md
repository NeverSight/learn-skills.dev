---
name: pdf-typeset
description: Typesets Markdown or JSON into a professional-looking PDF with Typst - report with cover and contents, document or memo, business letter, invoice with exact totals, CV/resume from JSON Resume, one-pager, 16:9 slide deck - in three themes, with Cyrillic and other scripts, then checks the result (missing glyphs, text running into the margins, overlapping text, fonts, metadata, blank, overflowing or nearly empty pages) and renders PNG pages to look at. Use when the user wants a PDF made or wants something as a PDF - a report, memo, letter, invoice, CV or resume, one-pager, handout or slides as PDF, Markdown exported to PDF, or a PDF that looks more professional ("сделай PDF", "экспортируй в PDF", "счёт", "резюме", "отчёт в PDF"). Not for reading, merging, splitting, filling, signing or editing existing PDFs, or extracting text or tables from them.
license: MIT
compatibility: Python 3.12+ with uv (preferred) or pip; macOS, Linux, Windows. The first run downloads about 90 MB of packages (Typst itself is about 77 MB); rendering is offline (Typst package downloads are blocked) and needs no LaTeX, browser or system libraries. Chinese, Japanese, Korean, Arabic and Indic text need a font installed on the system or passed with --font-dir.
metadata:
  author: zedxter
  version: "1.0.0"
  source: https://github.com/zedxter/utility-belt
---

# PDF Typeset

You write the content; the templates do the typesetting. `scripts/pdf.py` turns
Markdown (or JSON for an invoice or CV) into a PDF through Typst. The Typst
engine is a Python package, so there is nothing else to install. Then it
checks what came out, because Typst fails quietly: a missing font prints empty
boxes, and a wide table runs off the page, with no error. Every render also
writes PNG pages so you can see the result before the user does.

## When to use

- "Make a PDF report / memo / handout from these notes", "export this Markdown
  as a PDF" → `report` or `document`.
- "Write a letter to … as a PDF" → `letter`.
- "Invoice for …" → `invoice` (JSON). "Turn my CV into a nice PDF" → `cv`
  (JSON Resume).
- "A one-page summary", "a flyer" → `onepager`. "Slides as PDF" → `slides`.
- "This PDF looks amateurish" → rebuild it from its content with a template.
  "Is this PDF OK?" → `check`.

Not for: editing, merging, splitting, filling or signing existing PDFs, or
pulling text out of them. Not for pixel-exact brand layouts either: there are
three themes, not a design tool.

## Quick start

The script is `scripts/pdf.py` relative to this skill. `uv` installs Typst,
the Markdown parser, pypdf, pypdfium2 and Pillow on the first run.

```bash
uv run scripts/pdf.py render notes.md -o report.pdf -t report --png preview/
uv run scripts/pdf.py render memo.md -o memo.pdf --theme modern --png preview/
uv run scripts/pdf.py render invoice.json -o invoice.pdf --png preview/
uv run scripts/pdf.py render cv.json -o cv.pdf --theme minimal --png preview/
uv run scripts/pdf.py check existing.pdf --png preview/      # the same checks on any PDF
uv run scripts/pdf.py templates                               # templates and themes
uv run scripts/pdf.py schema invoice                          # the JSON an invoice takes
```

Without `uv`: `python -m pip install typst markdown-it-py mdit-py-plugins pyyaml pypdf pypdfium2 pillow`,
then `python scripts/pdf.py …`.

The report ends with the checks and the PNG paths:

```
report.pdf: 3 pages, template report
fonts: LibertinusSerif-Regular-Identity-H, LibertinusSerif-Semibold-Identity-H, DejaVuSansMono
checks: all passed
png: preview/page-01.png preview/page-02.png preview/page-03.png preview/contact-sheet.png
look at the PNG pages before handing the PDF over
```

## Workflow for the agent

1. **Content first.** Get the facts from the user or their files. Never invent
   them: names, numbers, dates, VAT IDs, IBANs, addresses. If a field is missing,
   leave it out or ask. An invoice needs a number and a date: ask for the number,
   and use today's date only when the user says so. For text meant for people
   to read, the `human-writing` skill helps.
2. **Pick the template** (table below) and write **Markdown with front matter**,
   or JSON for `invoice` and `cv`. Don't write Typst: the converter escapes
   everything, so the Markdown can't break the layout.
3. **Render with `--png DIR`.** Use `-f json` when you need the findings as data.
4. **Fix every `error` finding**, then re-render. Fix `warning`s when you can.
   Each finding has a hint.
5. **Look at the pages** with your image-viewing or file-reading tool: every
   `page-NN.png` (the contact sheet only shows balance, not text), against
   `references/design.md`. The checks catch broken output; only looking catches
   a wrong emphasis, a bad break or a cramped page. If you cannot view images,
   say so to the user: the visual check was not done.
6. **Deliver** the PDF path, the page count, any warnings left and anything
   unresolved, such as a missing logo or a font the system lacks. Stop after
   three render rounds and report what is left rather than looping.

For an invoice, give line items, quantities, prices and the VAT rate. **Never
compute totals yourself**: the script computes them exactly with `Decimal`,
rounds half up to the currency's minor unit, and reports them (`totals:` line;
`"totals"` in JSON) so you can quote them.

## Templates

| Template | Input | Layout |
|---|---|---|
| `report` | Markdown | Cover page, contents (on by default with 4+ sections), numbered headings, running header with the current section, "Page X of Y", footnotes |
| `document` | Markdown | Memo, article or note. Title block, no cover, unnumbered headings. The default |
| `letter` | Markdown | Sender top right, recipient where a window envelope shows it, date, subject, closing, signature |
| `onepager` | Markdown | Title band, key-figure cards, then the body as large as still fits: one column with generous spacing for a short text, two columns of smaller type for a long one. More than one page is an error |
| `slides` | Markdown | 16:9. Title slide from the metadata; each `#` (section) or `##` (slide) heading starts a page. A slide that spills is an error |
| `invoice` | JSON | Seller, buyer, invoice facts, line table, subtotal, VAT per rate, total band, payment details, notes |
| `cv` | JSON Resume | Name, contacts, summary, experience, education, projects, skills, languages, certificates, awards. ISO dates (`2021-03`) print as "Mar 2021"; a short CV gets more air between sections instead of an empty half page |

Themes: `classic` (Libertinus Serif, justified and hyphenated; the default for
`report`, `document` and `letter`), `modern` (Source Sans 3, ragged right; the
default for `onepager`, `slides`, `invoice` and `cv`),
and `minimal` (serif body, sans headings, near-black). Labels such as
"Contents", "Page 2 of 5", "Invoice", "Total due" and "Experience" follow
`lang` in English, Russian, Ukrainian, German, French and Spanish (others
fall back to English).

### Front matter (Markdown)

```yaml
---
title: Quarterly platform report      # or start the file with "# Title"
subtitle: Q3 2026
author: Platform team
org: Example Ltd
date: 2026-10-30
lang: en          # hyphenation, quotes, labels; ISO 639 code
template: report  # or -t
theme: classic    # classic | modern | minimal
toc: true         # report and document
numbered: true    # heading numbers; report default true, document false
paper: a4         # a4 | us-letter | a5 | us-legal
highlights:       # key-figure cards (onepager, document, report cover); only figures the user gave
  - value: 41 min
    label: Nightly export
    note: was 9 hours
# letter only:
from: [Studio Nord GmbH, Torstraße 12, 10119 Berlin]
to: [Acme Ltd, 1 King St, London EC2V 8AU]
subject: Offer for the UX audit
closing: Kind regards
signature: Anna Becker
---
```

Markdown support: headings, paragraphs, **bold**, *italic*, ~~strike~~,
`code`, fenced code with syntax highlighting, links (bare `https://` URLs are
clickable too), images (`![alt](file.png "Caption")` becomes a figure with a
caption), lists, task lists, tables (number columns align right on their own),
block quotes, `---` rules and footnotes.

- **Images** must be local files (PNG, JPEG, GIF, SVG, WebP) in the Markdown
  file's folder or below; `--allow-images-from DIR` adds another folder. This
  keeps Markdown from elsewhere from pulling arbitrary files into the PDF. A
  URL prints its alt text, because rendering is offline.
- **Raw HTML** is left out, with a note.
- **Math** is not converted. Typst math is different from LaTeX: write a
  `.typ` file if you need it.

### JSON templates

`uv run scripts/pdf.py schema invoice` (or `cv`) prints the JSON Schema.

- **Invoice:** `number`, `date`, `due`, `service_date` (date or period of the
  service), `currency` (ISO code), `seller` and `buyer` (`name`, `address`,
  `vat_id`, `email`, `iban`, `bic`…), `lines` (`description`, `qty`, `unit`,
  `unit_price`, optional `vat_rate`), `vat_rate`, `payment_terms`,
  `reference` (defaults to the number), `notes`.
- **CV:** standard JSON Resume (`basics`, `work`, `education`, `skills`,
  `languages`, `projects`, `certificates`, `awards`).
- **Both** may carry `lang`, `theme` and `paper`.

## Options

| Flag | Default | Meaning |
|------|---------|---------|
| `-o FILE.pdf` | — | Output (required for `render`). |
| `-t, --template` | `document`, or by JSON shape | `report`, `document`, `letter`, `onepager`, `slides`, `invoice`, `cv`. |
| `--theme`, `--lang`, `--paper` | `classic`, `en`, `a4` | Override the front matter. |
| `--title`, `--subtitle`, `--author`, `--org`, `--date` | — | Override the front matter. |
| `--toc / --no-toc` | auto | Table of contents. |
| `--png DIR`, `--dpi N` | —, 110 | PNG of every page plus `contact-sheet.png`. |
| `--font-dir DIR` | — | Extra fonts (repeatable), e.g. a brand font or Noto Sans CJK. |
| `--no-system-fonts` | off | Only bundled and built-in fonts: the same result on every machine. |
| `--pdf-standard` | — | `a-2b`, `a-3b`, `ua-1`, … Typst enforces the standard's rules. Full conformance still needs a validator such as veraPDF. |
| `--keep-typ DIR` | — | Keep the generated Typst sources in a new or empty folder (debugging). |
| `--allow-images-from DIR` | — | Also read Markdown images from DIR (repeatable). |
| `--root DIR` | input's folder | For `.typ` input: the folder it may read and import from. |
| `--allow-packages` | off | Let a `.typ` input import Typst packages (downloads them). |
| `-f text\|json`, `-q` | text | Report format; `-q` hides `note:` lines. |

`check PDF [--source FILE] [-t TEMPLATE] [--png DIR]` runs the checks on any
PDF. `--source` adds the text the PDF should contain, so characters that
vanished are named. `-t` enables the margin, runt-page and one-pager checks for
one of these templates (the heading and slide checks need `render`).
`fonts --sample TEXT` names every character no available font covers.

Page numbers in findings count physical pages, cover included. The contact
sheet is written for documents of two or more pages.

`render` also takes a `.typ` file, compiled in its own folder and then
checked, and `-` for Markdown on stdin. A `.typ` file is a program: it can
read any file in its folder. Render only `.typ` files the user wrote or
trusts.

## Checks

| Rule | Severity | Meaning → fix |
|---|---|---|
| `missing-glyph` | error | Characters drawn as empty boxes, named with code points → install or `--font-dir` a font that has them. |
| `unknown-font` | error | A font name Typst does not know → `fonts` lists the names. |
| `overflow` | error | Text runs into the margin or off the page → shorten the URL or code line, give the table fewer or narrower columns. |
| `overlap` | error | Text drawn over other text → check the PNG; usually a too-wide table or a hand-placed element. |
| `blank-page` | error | An empty page → remove the extra page break. |
| `slide-overflow` | error | A page continues the previous slide → split the slide. |
| `too-long` | error | A one-pager on two pages → cut, or use `document`. |
| `font-not-embedded` | error | (any PDF) A font not embedded in the file. |
| `runt-page` | warning | The last page holds 1–2 lines → tighten the text. |
| `stranded-heading` | warning | A heading at the very bottom of a page. |
| `low-res-image` | warning | An image prints under 120 dpi → use a larger file. |
| `no-title`, `no-author`, `no-lang`, `untagged`, `no-outline` | warning | Missing metadata, tagging or bookmarks. Templates set them from the front matter. |
| `typst-warning` | warning | Anything else Typst reported. |

## Exit codes

One `error:` line on stderr with a hint after `—`.

| Exit | Meaning | What to do |
|------|---------|------------|
| 0 | PDF written, no error findings (warnings possible). | Look at the PNGs. |
| 1 | PDF written, but checks found errors. | Fix them and render again. |
| 2 | Bad input: file missing, invalid JSON, front matter or schema field, unknown template or theme, malformed language code, image outside the input's folder, missing dependency, output not writable. | Fix the input; `schema` shows the JSON fields. |
| 3 | Typst compile error (with file:line:column for `.typ` input), or a `.typ` that tried to import a package. | Fix the `.typ`. With Markdown or JSON input it is a converter bug: simplify the construct named in the error, then report it. |
| 5 | An image, font folder or file the document names was not found. | Fix the path. |
| 7 | Anything else. | Report it with the command line. |
| 130 | Interrupted. | — |

## Limitations

- CJK, Arabic, Hebrew and Indic text need a system font, which most systems
  have, or `--font-dir` with one such as Noto. `missing-glyph` reports it
  when the font is not there.
- Right-to-left layout has not been tested.
- Typst math only, from `.typ` input.
- Rendering never touches the network: templates import no Typst packages, and
  package downloads are blocked unless `--allow-packages` is given.
- Three themes; brand colours and fonts mean editing `templates/lib.typ`.

## Chaining

- `human-writing` for the text of a report, memo or letter, then this skill to
  typeset it.
- `web-extract` and `web-search` to gather sources first; keep the URLs in the
  document.
