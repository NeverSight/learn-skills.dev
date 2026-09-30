---
name: extract-template
description: "Decide what an uploaded file is — a deck, a Word document, a PDF document, or artwork — and hand it to the template-extraction guide that matches. Use when asked to extract a template from a deck or document, turn a PDF into a Word template, save an image style as a reusable template, apply a company template to Markdown, or save a file's visual language as a reusable template."
---

# Extract a reusable template from a file

Look at what the file holds, decide what it is, follow that guide to the end.
Run the commands below from the directory containing this guide.

Render a `.pptx` or `.ppt` first. An image is already viewable.

```bash
okou presentation screenshot --input <source.pptx|source.ppt> --out shots
```

Render a PDF or Word document at its own page proportions before judging layout:

```bash
node scripts/render-document.mjs --input <source.pdf|source.docx> --out source-render
```

Use a new output directory for each render. Keep the original as the source;
use the returned PDF and page images for inspection.

| The file is | Go to |
|---|---|
| a deck — `.pptx`, `.ppt`, an image deck, or a `.pdf` whose pages are slides | `presentation/SKILL.md` |
| a Word document — `.docx` | `docx/SKILL.md` |
| a PDF document — pages of prose, not slides | `pdf/SKILL.md` |
| artwork — `.png`, `.jpg`, or several images of one drawing style | `illustration/SKILL.md` |

A page carrying one idea in display type is a slide. A page carrying running
prose under a repeated header, footer, or page number is a document. A picture with no
reading order is artwork.

Re-save a `.doc`, or a `.docx` written by WPS, as `.docx` from Word first.

Four rules override the table:

- A deliverable the user names beats the table. "Turn these slides into a Word
  template" is `docx/`; "save this report's look as a presentation template" is
  `presentation/`.
- Extract from the authoring file when it sits beside an export of itself: `.docx`
  over its PDF, `.pptx` over its PDF.
- One or two pages at a paper size is never slides, however sparse. A resume and
  an invoice carry as little text as a slide and are still documents.
- Several images at once are one style to `illustration/`, not several
  templates. A single image of a page — a scanned document, a screenshot of
  slides — is that page's kind, not artwork.

`cd` into the branch directory; every path inside a branch guide is relative to
it. Both document guides start with
[`document-reuse.md`](document-reuse.md) to choose the reuse scope and package.
