---
name: security-paper-translate
description: Translate cybersecurity and related academic research paper PDFs into professional Chinese while preserving the original PDF layout. Use when Codex is given an English academic paper PDF and asked to produce a Chinese-only version, a Chinese-first English interleaved version, format/font/color/table/figure-preserved translation, terminology table/glossary, or network/security paper translation. Requires Codex to translate itself without external machine translation or other LLM APIs.
---

# Security Paper Translate

## Non-negotiables

- Translate with Codex itself. Do **not** call Google Translate, DeepL, pdf2zh translation mode, OpenAI/Anthropic/Gemini APIs, local LLMs, or any other machine-translation/model service.
- Preserve the original paper's layout: page size, margins, columns, figure/table positions, captions, title hierarchy, color, bold/italic emphasis, and visual density.
- Produce final deliverables under a paper-specific project folder next to the source PDF: `translated-pdfs/<stem>/`. Keep this folder clean after a successful run: only final PDFs, final terminology TSV, and generation statistics should remain.
  - `<stem>-zh.pdf`: Chinese-only content pages, plus final terminology page(s).
  - `<stem>-zh-en-interleaved.pdf`: page 1 Chinese, page 1 English, page 2 Chinese, page 2 English, ..., plus final terminology page(s).
  - `<stem>-terms.tsv`: source-backed terminology and no-translate policy table.
  - `<stem>-generation-stats.json`: machine-readable generation statistics.
  - `<stem>-generation-stats.md`: human-readable generation summary.
  - Use `translated-pdfs/<stem>/.work/` only for temporary inspect, validation, assets, scripts, renders, and page-level intermediates. Delete `.work/` after successful strict validation unless the user asks for debug artifacts.
- The Chinese content page count must match the source PDF page count. Terminology pages are appended after content pages and are exempt from this count.
- Translate title, abstract, section headings, body, figure captions, table captions, table text, footnotes, acknowledgments, and other main content. Do **not** translate appendices or references unless the user explicitly asks.
- Preserve style hierarchy visibly, not merely textually: title fonts, section/subsection headings, table/figure captions, table headers, contribution labels, `Finding#`/`发现#` labels, bold leads, italic leads, colored citations, and colored hyperlinks must remain visually distinguishable in the Chinese PDF. **Missing bold/title hierarchy is a failed output, not a cosmetic issue.**
- Bold hierarchy must be produced by font selection, not by graphic tricks. For Chinese bold/semi-bold text, use a real bold/semi-bold CJK font and draw each label exactly once. Do **not** use stroke/outline text, offset shadows, repeated overprint, duplicate overlays, or “fake bold” made from overlapping copies. If the current PDF already contains overlapped bold text, redact the overlapped cluster first, then redraw one clean real-font run.
- If a local VSCode “PDF Translate” / `pdf2zh` / PDFMathTranslate-style output exists for the same paper, inspect it as a **layout-preservation reference only**. You may reuse its local layout reconstruction method (region detection, text replacement, mono/dual assembly), but you must still supply Codex-written translations and must not call its machine translation service.
- Do not translate code, commands, paths, API names, YAML/JSON keys, action/repository names, identifiers, product names, or source-text spans rendered in code/monospace/special identifier fonts when they function as identifiers. Do not treat every occurrence of a word as frozen merely because the same string appears elsewhere as an identifier; classify by context and ask the user before full translation.
- Preserve code/listing/verbatim regions exactly. For code blocks, algorithms-as-code, YAML/JSON/shell snippets, inline command examples, stack traces, schema listings, and monospace tables, do **not** translate, rewrap, reindent, normalize punctuation, change line breaks, change alignment, or replace the original monospace/code styling. Translate only the surrounding prose and listing captions unless the user explicitly asks otherwise.
- Do not translate English inside images/diagrams. Preserve images as-is, but add important diagram terms to the terminology table with page/figure source.
- If text extraction is broken, try OCR only after reporting it. If OCR is unstable, stop and report rather than fabricating a result.
- Never claim success without validation. If pages overflow, styles are missing, or extraction is unreliable, say exactly what failed and iterate.

## Workflow

1. **Inspect the source PDF**
   - Use the PDF skill if available.
   - Run `python scripts/paper_pdf_tools.py init-workdir <source.pdf>` to create `translated-pdfs/<stem>/` and temporary `.work/` subdirectories.
   - Run `python scripts/paper_pdf_tools.py inspect <source.pdf>` to collect page count, sizes, fonts, colors, text blocks, and sample renders under `.work/inspect/`.
   - Run `python scripts/paper_pdf_tools.py extract-literals <source.pdf>` to pre-detect special-font/code identifiers under `.work/terms/`; merge confirmed entries into final `<stem>-terms.tsv`.
   - Identify whether the paper is single-column or multi-column; preserve it exactly.
   - Create a `.work/style-map.tsv` before rebuilding pages. It must list every visible styled source item that needs preservation: page, source text, target Chinese text, bbox/region, style kind (`title`, `section`, `subsection`, `caption`, `table-header`, `lead-bold`, `finding`, `citation-color`, `link-color`, `code-font`), font size, color, and preservation method.

2. **Preflight classification and user confirmation**
   - Before full translation, build and show a concise preflight report. Do not start full PDF generation until the user confirms or explicitly says to proceed automatically.
   - Include these sections:
     - PDF facts: page count, page size, column style, major fonts, CJK font planned for output.
     - No-translate candidates: term, category, source page, reason, and real Chinese meaning/explanation. Categories should include `literal/code identifier`, `product/project/entity name`, `API/config key`, `dataset/benchmark`, `abbreviation`, and `explain-only`.
     - Translation candidates: key technical terms with proposed Chinese translation and first-use strategy.
     - Ambiguities: strings that may be ordinary prose in some places and identifiers in others. Explain the proposed contextual rule.
     - Code/listing regions: page, caption/anchor, detected font or bbox, and preservation plan. State explicitly that code/listing contents will be frozen and kept visually code-like.
     - Polish mode: ask whether to run a second academic Chinese polishing pass after faithful translation. Default to yes in strict mode.
     - Validation mode: `strict`, `quick`, or `debug`; default to `strict` for final papers.
   - Use the user's confirmation to freeze a term policy for this run. The policy constrains later translation, but can be revised if a better decision emerges; if revised, propagate the change consistently.

3. **Plan translation boundaries**
   - Confirm any ambiguous content classes: appendices, references, code listings, dataset names, product names, figure-internal labels.
   - Default: appendices/references remain English; code/config/API names and special-font identifiers remain English only when functioning as identifiers. Ordinary prose uses may be translated by context.
   - For code/listing/verbatim regions, default to full preservation: keep the original region text, monospace font, indentation, line wrapping, punctuation, and block geometry. Do not feed these regions into normal translation chunks. If `pdf2zh` or another layout engine mutates them, restore the original source region during postprocessing.

4. **Translate professionally**
   - Translate all main prose yourself in polished academic Chinese.
   - Preserve technical precision over literal word order.
   - Use first-occurrence bilingual form for important terms: `中文译名（English Term, ABBR）`.
   - Later occurrences may use the abbreviation or stable Chinese term.
   - Keep necessary English originals when the confirmed term policy says they are de facto names or identifiers: `GitHub Actions`, `workflow`, `runner`, `sink/source`, `permissions`, `env`, `uses`, `WorkflowIR`, `GITHUB_TOKEN`, etc.
   - Translate by context when a string is used as an ordinary English word rather than an identifier.
   - Do not rewrite code blocks/listings for readability. Preserve the source code text exactly, including whitespace-sensitive layout and line breaks. If explanatory prose around the code needs translation, translate that prose separately from the code region.
   - Build a terminology TSV while translating. Merge the `extract-literals` output into it for preserved identifiers that need explanation. See `references/terminology-schema.md`.
   - If the user enabled polishing, run a second pass after faithful translation to make the result natural, rigorous, and readable as Chinese academic prose without changing technical meaning.

5. **Rebuild Chinese pages with layout preservation**
   - Read `references/layout-preservation-notes.md` before implementing the per-paper page builder.
   - If using local `pdf2zh`/PDFMathTranslate or a VSCode PDF Translate extension as the layout engine, read `references/pdf2zh-layout-integration.md` and use the bundled scripts rather than rewriting the monkeypatch workflow from scratch.
   - Before reinforcing headings/captions/bold labels, read `references/font-bold-rendering.md`. Treat its no-overlap bold rules as mandatory.
   - Prefer the successful page-object strategy:
     - Extract text blocks/spans with coordinates, font size, bold/italic/color information.
     - Keep non-text objects, figures, tables, vector graphics, and backgrounds from the original page.
     - Replace/overlay only translated text in the same text regions.
   - Preserve two-column flow and original reading order.
   - Prefer a proven `pdf2zh`/PDFMathTranslate-style layout engine when available locally: monkeypatch or replace its translator layer with Codex-generated translations so the engine handles page geometry, figures, formulas, and table anchors. Do not let it contact Bing/Google/DeepL/LLM APIs for translation.
   - When reusing a local VSCode “PDF Translate” extension, follow this exact successful pattern:
     1. Locate and inspect the extension source, e.g. `~/.vscode-server/extensions/*pdf*translate*/`, to confirm whether it wraps `pdf2zh` and which command/options it uses.
     2. Treat the extension's output PDF only as a visual/layout reference, never as a translation source.
     3. Run the local `pdf2zh`/PDFMathTranslate engine in a controlled way and replace/monkeypatch its translator class so calls return Codex-written Chinese strings from a local mapping. The engine may do layout detection and PDF rewriting; it must not contact Bing/Google/DeepL/other model or MT services.
     4. If needed, first run a capture pass that logs each source text chunk and returns harmless dummy text; then translate those captured chunks yourself and rerun with the local mapping.
     5. Generate the engine's Chinese mono PDF as an intermediate, then postprocess it rather than rebuilding the whole paper from scratch.
     6. Postprocess mandatory items: remove review line numbers or margin artifacts; redraw running headers/footers if damaged; patch tables whose cell text or alignment failed; restore any mutated code/listing/verbatim regions from the source PDF; reinforce headings, subsection titles, table/figure captions, and boxed findings; preserve original images/diagrams.
     7. Build the Chinese-first interleaved PDF from the final Chinese content pages and the original source pages, then append terminology pages.
   - If Chinese is too long for a region, first make the translation more concise; if still needed, slightly reduce font size to keep the original layout unchanged.
   - Map style from source to Chinese:
     - source bold -> corresponding Chinese bold/semi-bold font; never use overlapping copies, stroke text, or offset shadows as a substitute for bold;
     - source italic -> corresponding Chinese italic/weak emphasis where readable;
     - colored citations/cross-references/links -> matching Chinese citation/link color;
     - figure/table colors -> preserved from original objects.
   - Preserve code and listing blocks before touching nearby prose. A correct page builder must either keep the original code/listing region as-is or copy it back from the source page after text replacement. Never let translated prose reflow into a code box, and never let code lines be merged, split, centered, or converted to proportional body font.
   - Draw headings and bold labels as separate styled runs. Do **not** hide section titles, subsection titles, captions, `发现#` labels, contribution labels, or bold lead phrases inside an ordinary paragraph textbox.
   - Enforce heading/emphasis hierarchy after every generation pass. The final PDF must visibly preserve: paper title, abstract title, section titles, subsection titles, paragraph lead labels, table/figure captions, table headers, theorem/definition/algorithm/listing labels, contribution labels, and boxed findings. If any of these look like normal body text, stop and patch them.
   - For ACM/IEEE/USENIX-style compact two-column papers, preserve visual density: no unexpected half-page blank areas, no table/caption drift, no line-number remnants, no headers/footers colliding with translated text, and no “loose” reflow that differs from the source page.
   - Treat title/section/subsection styling as a hard requirement. After generation, render sample pages and verify that `摘要`, numbered section headings, numbered subsection headings, table captions, figure captions, and `发现#/Finding#` boxes are visibly bold or otherwise match the original emphasis. If they render as ordinary body text, regenerate or overlay them before finalizing.
   - For CJK bold, use a real bold/semi-bold CJK font such as Noto/Source Han CJK Bold/SemiBold. Do not simulate bold with offsets, repeated drawing, stroke/outline rendering, or overlapping copies. If no true bold CJK font is available, report the limitation and use the closest real font weight; do not fake it with overlap.
   - When bold-overlaying CJK labels, first test whether the text box accepts the glyphs. If using `insert_textbox` could silently fail due to a tight box, use baseline/point text or expand the box. Never mask an existing heading/label unless the replacement has been confirmed to draw.
   - When replacing a label that already exists, remove the old label region first, then draw the replacement exactly once. Never leave old and new label text occupying the same pixels.
   - If masking old text before redrawing style, use a two-step check: (1) compute/confirm the new styled run fits the region; (2) mask and draw. Never erase a heading/label first and then attempt a draw that may fail.
   - If exact style alignment is impossible, use semantic matching for emphasis, but avoid over-boldening whole paragraphs.

6. **Create final PDFs**
   - Generate `<stem>-zh.pdf` with all Chinese content pages plus terminology pages.
   - Generate `<stem>-zh-en-interleaved.pdf` with Chinese page before matching English page, plus terminology pages.
   - Use `python scripts/paper_pdf_tools.py interleave ...` when a Chinese-only PDF has already been produced.
   - Use `python scripts/paper_pdf_tools.py append-terms ...` to append terminology pages from TSV when needed.

7. **Validate before final response**
   - Run `python scripts/paper_pdf_tools.py validate <source.pdf> <zh.pdf> <interleaved.pdf>`; by default temporary validation artifacts go to `translated-pdfs/<stem>/.work/validation/`.
   - Check at minimum:
     - source content pages == Chinese content pages before glossary;
     - page size is unchanged;
     - interleaved order is correct;
     - no blank pages;
     - no large text overflow or abnormal whitespace;
     - figures/tables are still present and aligned;
     - sample bold and colored citation/link styles are visible on style-heavy pages;
     - section/subsection headings, table titles, figure captions, and boxed findings retain their title/bold style and are not plain body text;
     - bold labels are not duplicated, offset, shadowed, stroked, outlined, or visually ghosted; a programmatic check should report zero near-overlapping same-text bold spans and zero text-rendering-mode stroke markers for the patched pages;
     - code/listing/verbatim regions preserve original text, indentation, line breaks, monospace/code styling, and region geometry; no code has been translated, reflowed, or converted into proportional body prose;
     - every item in `.work/style-map.tsv` is visibly present in the rendered samples; section/subsection headings and captions must not disappear, become ordinary body text, or turn into overbold black blobs;
     - table/figure positions must match the source page anchors; a translated table/caption must not drift into another column, overlap the header/footer, or leave a large blank area that the source page did not have;
     - final terminology table exists in both PDF and TSV;
     - confirmed no-translate identifiers remain present and code-like in the Chinese PDF;
     - ordinary prose occurrences were not blindly frozen when they should be translated.
   - Render and inspect key pages: first page, a dense text page, a figure page, a table page, a code/listing-heavy page, a style-heavy page with colored citations/bold, and the terminology page.
   - If any styled heading, caption, bold label, color, code/listing region, or table/figure anchor fails visual inspection, do not finalize. Regenerate or patch the page and rerun validation.

8. **Finalize and clean up**
   - Run `python scripts/paper_pdf_tools.py finalize <source.pdf> <stem>-zh.pdf <stem>-zh-en-interleaved.pdf <stem>-terms.tsv` to write `<stem>-generation-stats.json` and `<stem>-generation-stats.md`.
   - Record the actual layout method in generation statistics, especially when reusing local `pdf2zh`/PDFMathTranslate: note that layout preservation came from the local engine while translations were supplied by Codex locally without external MT/LLM APIs.
   - Record visual self-check pages in generation statistics. Include first page, dense prose page, figure page, table page, style-heavy/bold page, and terminology page.
   - After successful strict validation, remove temporary `.work/` artifacts by default. Keep them only in `debug` mode or when the user explicitly asks.
   - The final project folder should contain only the two final PDFs, `<stem>-terms.tsv`, and generation stats files.

## Translation standards

Read `references/translation-standards.md` before translating a full paper or building the terminology table. Read `references/layout-preservation-notes.md` before implementing layout reconstruction.
Read `references/pdf2zh-layout-integration.md` when using a local VSCode PDF Translate extension, `pdf2zh`, or PDFMathTranslate-style layout-preservation engine.

## Helper scripts

- `scripts/check_environment.py`: check local `pdf2zh`, PyMuPDF, poppler, CJK fonts, and VSCode PDF Translate extension availability.
- `scripts/paper_pdf_tools.py init-workdir`: create `translated-pdfs/<stem>/` and temporary `.work/` directories.
- `scripts/paper_pdf_tools.py inspect`: audit source PDF structure and render sample pages.
- `scripts/paper_pdf_tools.py extract-literals`: extract code/special-font identifiers that should default to no-translate and produce a mergeable TSV.
- `scripts/paper_pdf_tools.py append-terms`: append terminology table pages to a PDF.
- `scripts/paper_pdf_tools.py interleave`: combine Chinese and English PDFs as Chinese-first page pairs.
- `scripts/paper_pdf_tools.py validate`: validate page counts, sizes, blank pages, render samples, and output a JSON report.
- `scripts/paper_pdf_tools.py finalize`: write final generation stats and remove `.work/` unless debug artifacts are requested.
- `scripts/pdf2zh_capture_chunks.py`: run local `pdf2zh` with its translator monkeypatched to capture source chunks without machine translation.
- `scripts/pdf2zh_codex_driver.py`: run local `pdf2zh` with a Codex-written local translation mapping; the layout engine is used, but external MT/LLM services are not contacted.
- `scripts/pdf_postprocess_template.py`: reusable postprocess scaffold for pdf2zh-produced mono PDFs: remove line numbers, redraw headers, reinforce CJK bold labels with real font-level bold only, color citations, append terminology, and build Chinese-first interleaved PDFs.
- `scripts/check_pdf_bold_integrity.py`: verify that bold-like spans are not duplicated/near-overlapped and that patched pages do not contain stroke/outline text rendering markers.

These scripts do not translate. They support deterministic PDF assembly and validation while Codex performs the actual translation.
