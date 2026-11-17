---
name: codex-pdf-reader
description: Prepare evidence packages from specified PDF files, inspect text, figures, tables, captions, and page structure with Codex, then write prompt-driven Markdown reading notes and Zettelkasten cards to .md files. Use when Codex needs to read a PDF, analyze a paper or report, create a PDF evidence package, apply a user-provided prompt to PDF content, create saved Markdown reading notes, or generate atomic Zettelkasten cards with source-grounded page, figure, and table references.
---

# Codex PDF Reader

**Version:** 0.9

## Overview

Use this skill to read one specified PDF, or a small explicitly listed set of PDFs, and produce saved Markdown reading notes with Zettelkasten cards from the PDF content. This is an evidence-package workflow: use local PDF tools to expose metadata, page text indexes, page renders, and figure/table locations, then use Codex to interpret the paper from the PDF evidence. Do not summarize from extracted text alone, and do not use the Gemini batch pipeline from `batch-pdf-reading-notes` unless the user explicitly asks for that older batch/API behavior.

## Workflow

1. Resolve the target PDF path or attachment. If multiple PDFs are provided, process them independently and avoid mixing evidence across files.
2. Prepare an evidence package with `scripts/prepare_pdf_evidence.py` unless the user explicitly asks for chat-only reading or the environment cannot run Python. The script creates `evidence_manifest.json`, `evidence_overview.md`, per-page text indexes, thumbnails, and selected high-resolution page renders.
3. Use extracted text only as a navigation/search index. Treat the original PDF and rendered pages as the evidence source for scientific claims, especially for figures, tables, captions, equations, layouts, axis labels, error bars, statistical marks, controls, and image panels.
4. Read the evidence package in layers: metadata and table of contents first, section/text index second, rendered figure/table/result pages third, then synthesize the paper-level argument.
5. Apply the user's prompt as the governing instruction. If the user does not provide a prompt or output schema, use `references/default-zettelkasten-prompt.md` and load `references/few-shot-examples.md` to calibrate the output style.
6. Choose a Markdown output path before writing the final note. Use the user's requested path when provided. Otherwise save one `.md` file beside each PDF using a clear name such as `<pdf-stem>.reading-notes.md`; if the PDF directory is not writable, use the current workspace directory.
7. Produce Markdown file content with the requested schema. For the default scientific-literature output, include a public audit block, source metadata, evidence package path, evidence map, a cohesive summary, and 3 to 6 source-grounded Zettelkasten cards.
8. Write the final Markdown to the chosen `.md` file. In the chat response, report the saved file path, evidence package path, and a concise completion summary; do not paste the full note unless the user explicitly asks for inline content.
9. Verify the final cards against the PDF evidence: every factual claim should be traceable to PDF text, figures, tables, captions, or equations, or clearly marked as an inference.

## Evidence Package Tool

Run from the skill directory or use an absolute script path:

```bash
python scripts/prepare_pdf_evidence.py <paper.pdf>
```

Useful options:

- `--out-dir <dir>`: write the evidence package to a specific directory.
- `--render-pages auto|all|none|1,3-6`: choose high-resolution rendered pages. Use `all` for short papers or figure-heavy PDFs when feasible.
- `--dpi 180`: set high-resolution render DPI.
- `--max-auto-pages 24`: cap automatically selected high-resolution pages for long PDFs.

The script requires PyMuPDF (`scripts/requirements.txt`). If it is unavailable and cannot be installed, fall back to any available PDF viewer or rendering tool, but keep the same evidence-package logic.

## Prompt Handling

- Treat the user's prompt, requested language, card count, section names, and output format as higher priority than the default reference prompt.
- Load `references/default-zettelkasten-prompt.md` when the user asks for paper reading notes, scientific literature analysis, or Zettelkasten cards without a custom prompt.
- Load `references/few-shot-examples.md` with the default prompt so the final Markdown follows the demonstrated summary/card density and style.
- Load `references/zettelkasten-output-format.md` only when the user asks for a compact generic Zettelkasten format instead of the scientific-literature default.
- Save the final Markdown even when the user does not explicitly ask for a file, unless the user explicitly requests chat-only output.
- Include the evidence package path in source metadata when one was created.
- Keep source-backed content separate from inference. Use `TBD` or `Not stated in the PDF` for missing bibliographic fields, methods, figures, tables, or results.
- Include page, section, figure, table, equation, or supplementary-material references whenever they are available.
- If a card depends on visual evidence, explicitly anchor it to the relevant figure, panel, image, table, or legend.
- Do not include private hidden reasoning, scratch work, or conversational filler. If the selected prompt requires a `<thinking>` block, make it a concise public methodology/evidence audit, not an exhaustive chain-of-thought transcript.

## Quality Checks

- Confirm the PDF title, year, authors, and citation fields are not guessed.
- Confirm every card is atomic: one durable idea, one evidence chain, and one note-worthy implication.
- Confirm important claims were checked against rendered pages or the original PDF, not only against extracted text.
- Prefer the paper's actual data, observations, definitions, arguments, or examples over broad author claims.
- Check figures and tables when they are central to the claim; do not treat captions as a substitute for visual evidence when the figure itself matters.
- For empirical papers, separate observed results from interpretation.
- For review, theoretical, or conceptual papers, separate cited background from the author's own synthesis or framework.
- Preserve exact sample names, gene names, strain names, equations, and technical terms from the PDF.

## Resources

- `scripts/prepare_pdf_evidence.py`: Build a PDF evidence package with metadata, page text indexes, thumbnails, selected high-resolution page renders, JSON manifest, and Markdown overview.
- `scripts/requirements.txt`: Python dependency list for the evidence package script.
- `references/default-zettelkasten-prompt.md`: Default prompt for paper summaries and Zettelkasten cards.
- `references/few-shot-examples.md`: Two calibrated examples showing the expected public audit block, Chinese summary, and evidence-chain cards.
- `references/zettelkasten-output-format.md`: Compact Markdown output schema to use when the user does not provide one.
