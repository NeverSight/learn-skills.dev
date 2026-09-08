---
name: docx-template-translator
description: Adaptive conversion of LaTeX, PDF, or Markdown sources into a complete Word .docx that follows a user-supplied .docx template. Use when pandoc --reference-doc alone is not enough — for thesis, dissertation, report, or institutional Word formatting that needs cover pages, declarations, TOC, heading numbering, captions, three-line tables, equations, citations, and visual verification.
---

# DOCX Template Translator

## Core Idea

Treat the input file as the content source and the Word template as the formatting source. Do not expect pandoc or PDF import to infer template semantics. Build a project-specific Python postprocessor after inspecting the template and the converted body document.

Do not treat the bundled starter pipeline or a preset JSON file as a finished converter for institutional templates. For thesis/dissertation templates, you must create or patch a project-specific pipeline for the concrete template and source project before claiming success.

## Workflow

1. Identify inputs:
   - Source: `.tex` project, `.pdf`, `.md`, or an existing rough `.docx`.
   - Template: required `.docx`.
   - Output location and document metadata.
2. Inspect the template with the real CLI form:
   - `python scripts/inspect_docx_template.py template.docx --out template_report.json`
3. Create a rough body `.docx`:
   - LaTeX/Markdown: use pandoc when available.
   - PDF: try Word COM import or `pdf2docx`; prefer PDF only when the original source is unavailable.
   - Existing DOCX: use it as the rough body source.
4. Write or patch a project-specific Python pipeline:
   - Start from `scripts/adaptive_docx_pipeline.py`.
   - Copy it into the run/output directory or project workspace before patching; do not edit the bundled script in place for a one-off conversion.
   - Decide, from the template inspection, which template paragraphs/tables/sections are reusable and which are sample placeholders to delete.
   - Mark protected native-template regions before coding. For thesis templates, cover pages, English cover pages, originality/declaration pages, authorization pages, signatures, and their section breaks are protected by default until the first generated abstract/body marker.
   - Replace or fill template front matter such as cover pages, declarations, abstracts, keywords, TOC placeholders, headers, footers, page numbering, and section breaks when the source provides those fields.
   - In protected regions, replace text inside existing paragraphs/runs/tables without deleting and rebuilding the paragraph. Preserve paragraph styles, run fonts/sizes/bold, alignment, spacing, and page breaks unless the user explicitly asks to alter the template.
   - Insert the rough body at the real body start or rebuild the document around the template parts. Do not blindly append the rough body to the end of the template.
   - Copy template front matter if needed.
   - Append rough body content while remapping DOCX relationships.
   - Remap copied style IDs by visible style name before applying formatting; otherwise `Heading 1/2/3` can silently become an unrelated template style when source and template style IDs collide.
   - Remap styles to the template's real body, heading, caption, reference, and TOC styles.
   - Scope global formatting passes to generated content only, for example with `formatting_start_marker`. Never run body-style remapping across native cover/declaration pages.
   - Clean or rebuild section header/footer references when deleting sample template sections; stale back-matter headers such as `致谢` must not appear on body pages.
   - Add or repair figure/table captions, table borders, hyperlinks, bookmarks, citations, and page breaks.
5. Finalize with Microsoft Word when available:
   - Use `scripts/finalize_word_docx.py` to update fields/TOC and export a PDF preview.
6. Automated and visual verification:
   - Use `scripts/validate_docx_conversion.py final.docx --template template.docx --protected-until "中 文 摘 要" --pdf final.pdf --out validation.json` for placeholder/order/header/image/table checks plus protected-front-matter format checks. Choose the real first generated marker for non-Zhengzhou templates.
   - Then run `scripts/validate_docx_render.py final.docx --pdf final.pdf --out validation_render.json` for render-level checks: TOC field presence, numId↔abstractNum consistency, multilevel heading format, reference-counter independence, body-header static-text leakage, and PDF field-error strings. The structural validator can return PASS while the document is visibly broken; the render validator is what catches "empty TOC", "chapters not auto-numbered", "references start at [47]", "body header still says 致谢", and "STYLEREF prints 错误!使用'开始'选项卡…".
   - Use `scripts/render_pdf_preview.py` to inspect cover pages, abstracts, TOC, representative tables, figures, formulas, and references.

## Mandatory Quality Gate

Before reporting success, run an automated and visual QA pass. If any check fails, patch the project-specific pipeline and rerun; do not present the output as complete.

- Confirm the rough body is not appended after a back-matter placeholder such as `致谢`, `Acknowledgements`, `参考文献`, or sample appendices.
- Confirm template placeholder text is gone or intentionally preserved. Common failures include names like `李四`, `王五`, `张三`, red formatting instructions, lorem ipsum, sample chapter headings, and template-only reference lists.
- Confirm source metadata and source front matter replaced the template placeholders: title, author, advisor, major/department, date, Chinese abstract, English abstract, keywords, declarations when applicable.
- Confirm protected front matter still matches the template's formatting. Content may change, but cover/declaration/signature pages must preserve paragraph styles, run-level fonts/sizes/bold, spacing, alignment, and page-break structure unless explicitly modified.
- Confirm TOC entries point to the generated source chapters, not only to the template's sample chapters.
- Confirm heading paragraphs are still heading styles after OOXML insertion; style ID collisions must not break TOC generation.
- Confirm body pages use the intended body style and do not inherit the last template section's header/footer.
- Confirm representative images, formulas, tables, captions, references, and citations survive the reconstruction.
- Record failures in the run report with PASS/FAIL/PARTIAL wording and concrete evidence.

## Render-level Quality Gate (`validate_docx_render.py`)

The structural quality gate above checks **counts and presence**. It can return
`PASS` while the rendered Word/PDF is visibly broken because pandoc-derived
DOCX bodies often ship with a TOC paragraph that has no field, a Heading 1
style with no `<w:numPr>`, a `numId` rebound to a single-level abstract during
reference repair, or a body section header whose static text is "致谢". Run
`validate_docx_render.py` after `validate_docx_conversion.py` to catch those:

- **TOC field presence**: `<w:fldChar w:fldCharType="begin">` plus `<w:instrText> TOC `. If absent, Word's "update fields" cannot populate a non-existent TOC. Use `scripts/inject_toc_field.py` to add one before finalization.
- **numId ↔ abstractNum consistency**: every `(numId, ilvl)` pair used by a paragraph or by a style's `<w:numPr>` must resolve to a defined `<w:lvl ilvl=N>` inside the bound abstract numbering. Missing levels silently fall back to level 0 — that is how `1.1` / `1.1.1` headings collapse to `[1]` after a reference repair re-points `numId=1` at a single-level abstract.
- **Multilevel heading format**: the abstract numbering bound to Heading 1 (whether at style level or via inline numPr on body H1 paragraphs) must have `lvlText` matching the user-supplied chapter prefix pattern (default `第%1章` or `Chapter %1`) at level 0 and a multilevel pattern (default contains both `%1` and `%2`) at levels 1/2. Configure with `--chapter-prefix-pattern` and `--multilevel-pattern` for non-default templates.
- **Reference counter independence**: any non-heading paragraph appearing after the last `参考文献` / `References` Heading 1 must not reuse a `numId` already used by Heading 1/2/3. This is the bug where 33 references render as `[47]`–`[79]` because their counter was shared with H2/H3 paragraphs upstream.
- **Body header is not a back-matter literal**: for every body section that uses a `<w:headerReference>`, the referenced `headerN.xml` must either contain a Word field (`<w:fldChar>`) or its static text must not equal `致谢` / `Acknowledgements` / `参考文献` / `附录` / `攻读学位期间…`. The recommended fix is `scripts/set_styleref_header.py --style-id 1` so the header dynamically shows the current chapter title.
- **PDF field errors absent**: scan the exported PDF for the localized field-error strings (`错误!`, `Error!`, `!Reference source not found`, `!未找到引用源`). These appear when STYLEREF/PAGEREF/REF can't resolve their target and are an immediate FAIL.
- **Figure count vs source** (`--source-latex-dir <dir>` or `--min-figures <N>`): rendered `<w:drawing>` count must be ≥ the LaTeX project's `\includegraphics` count. Pandoc silently drops figures whose path lacks an explicit extension (e.g. `\includegraphics{thesis_structure}`) when the basename also matches a vector file (`.pdf` / `.vsdx`). The structural validator counts what *was* embedded; this check tells you what *should have been* embedded.
- **Table border style** (`--expected-table-style three-line` for Chinese-thesis templates, default `any`): every data table must classify as a recognizable three-line layout (top heavy, header-row bottom thin, last-row bottom heavy, vertical edges nil) or a `tblStyle` that may carry borders. A docx that contains 20 borderless tables when the template requires three-line tables is the failure mode this catches. Layout/wrapper tables (≤ `--table-min-data-rows` rows) are skipped.
- **Citation coverage** (`--source-latex-dir <dir>` or `--min-citations <N>`): the docx must contain at least as many `<w:hyperlink w:anchor="ref_*">` elements as the source has `\cite{}` calls. Pandoc's default behavior is to render `\cite{key}` as `(Author Year)` — a *visible* author-year token but **without** an internal hyperlink. For GB/T 7714 thesis style every citation must render as numeric `[N]` superscript hyperlinking to the bibliography entry; missing this is invisible to image-count / paragraph-count validators.
- **Caption count vs source** (`--source-latex-dir <dir>` or `--min-figure-captions <N>` / `--min-table-captions <N>`): count caption-style paragraphs (`图 X.Y` / `表 X.Y` lead, excluding inline body mentions like `图 4.4 与图 4.3 分别给出…`) and require at least the source `\begin{figure}+\caption` / `\begin{table}+\caption` env count. The pandoc rough-conversion for Chinese theses commonly drops captions onto a plain body style **without** the chapter-relative number prefix; the structural validator counts `<w:drawing>` and `<w:tbl>` but never checks whether each has a labeled caption beside it.
- **Caption numbering** (default on): every paragraph that *looks* like a caption attempt — i.e. starts with `图`/`表`/`Figure`/`Table` followed by a digit — must match the strict form `图 X.Y  说明文字` / `表 X.Y  说明文字` (with non-empty trailing description). The candidate filter must require a digit after the heading character so body sentences like `表格型 Q-learning…` or `表中的实验配置…` are not mistaken for captions. Inline body mentions like `图 4.4 与图 4.3 分别给出…` are skipped via a verb-list pattern.
- **Caption centering** (default on): every recognized caption paragraph must have `w:jc="center"`. Off-center captions are the first thing a thesis reviewer flags and signal a pandoc-only conversion that did not run a caption-formatter pass.
- **Caption untagged near figure/table** (default on): every body `<w:drawing>` paragraph must be followed (within one step, after collapsing adjacent drawing paragraphs into a single subfigure group) by a caption-pattern paragraph, and every data `<w:tbl>` (≥2 rows, ≥2 cells in the header row) must be preceded by one. Front-matter drawings before the first body Heading 1 (cover-page logos, school crests, declaration page emblems) are excluded — they are not captioned figures. This catches pandoc-converted figures whose caption was emitted as a plain body paragraph without the `X.Y` prefix.

Demote any single check to a warning with `--allow <check-name>` when a project intentionally omits a TOC, intentionally shares a counter, etc.

## Required Engineering Rules

- Prefer deterministic Python and OOXML operations over manual Word edits.
- Preserve content first; only change formatting unless the user explicitly asks to edit text.
- Treat native cover/declaration/signature pages as protected regions. Do not use delete-and-recreate paragraph replacement there; mutate existing runs/cells or use a project-specific OOXML placeholder replacement that preserves formatting.
- Any all-document style, table, hyperlink, heading-page-break, or font pass must have an explicit scope. If the template has front matter, start the scope after the protected marker rather than iterating over every `doc.paragraphs` / `doc.tables`.
- Keep a generated PDF preview beside the final DOCX.
- After copying OOXML between DOCX files, remap `w:pStyle`, `w:rStyle`, and `w:tblStyle` IDs by visible style name unless you have a stronger project-specific mapping.
- If the template contains sample back matter, explicitly inspect or remove section `headerReference` / `footerReference` entries after deleting sample sections.
- For LaTeX, extract structured information from `.tex`, `.aux`, `.bbl`, `.toc`, and source captions when pandoc loses numbering or labels.
- For equations, preserve pandoc-generated OMML when possible; avoid touching paragraphs containing `m:oMath` unless necessary.
- For hyperlinks, explicitly set black/no-underline styling if the target template requires print-style links.
- For references, add bookmarks at bibliography entries before converting in-text numeric citations into internal hyperlinks. **Allocate a fresh `numId` (and a matching `<w:abstractNum>` with level 0 = `[%1]`) for the reference list — do not reuse the heading `numId`. Sharing the counter is what produces "33 references rendered as `[47]…[79]`" because the counter accumulates through every Heading 2/3 paragraph upstream.**
- For institutional templates, avoid generic style names like `Body Text`; inspect the template because those names may be repurposed.
- For finalization, always run with macros disabled. The bundled `finalize_word_docx.py` sets `Word.Application.AutomationSecurity = msoAutomationSecurityForceDisable` before opening the document; do not loosen this for inputs of unknown provenance.
- Three-line table coercion is opt-in (`--three-line-tables` or `enable_three_line_tables` in config). Don't enable it unless the target template actually requires that layout. **When you do enable it, also write the borders through the raw `<w:tc>` elements inside the last `<w:tr>` — python-docx's `row.cells` wrappers silently no-op on `vMerge="continue"` cells, leaving a gap in the bottom heavy line at the end of any column whose final cell is a vertical-merge continuation.**
- For figures, when running pandoc on LaTeX sources, pre-process every `\includegraphics{name}` to `\includegraphics{name.png}` (or whichever raster extension exists alongside) before invoking pandoc. Pandoc resolves bare basenames against the cwd, prefers vector extensions (`.pdf`, `.vsdx`), and silently drops the figure when it cannot embed the vector. Always cross-check the rendered `<w:drawing>` count against the source `\includegraphics` count via `validate_docx_render.py --source-latex-dir`.

## Common Pitfalls (with concrete fixes)

These are recurring failures observed when running this skill on real
institutional templates. Each line names what to look for and which script
or rule fixes it.

- **Empty TOC paragraph.** The rough body has a "目录 / Table of Contents" heading but no `<w:fldChar>` field after it. Word's "update fields" pass does nothing. → Run `scripts/inject_toc_field.py final.docx --in-place` before finalization, or detect via the `toc-field` check in `validate_docx_render.py`.
- **Chapters do not auto-number.** The Heading 1 style has no `<w:numPr>` and the body H1 paragraphs also have no inline `numPr`. → Either add `<w:numPr><w:ilvl w:val="0"/><w:numId w:val="N"/></w:numPr>` to the Heading 1 style, or insert paragraph-level `numPr` on every body H1 (skip the unnumbered front/back-matter titles like 摘要/ABSTRACT/参考文献/附录/致谢/攻读…). Detected by the `multilevel-headings` check.
- **Section numbers render as `[1]`, not `1.1` / `1.1.1`.** A reference repair re-pointed `numId=1` at a single-level abstract list. Heading 2/3 paragraphs use `(numId=1, ilvl=1/2)` and fall back to level 0 = `[%1]`. → Restore the multilevel binding (the abstractNum whose level 0 is `第%1章` and level 1/2 contain `%1.%2` / `%1.%2.%3`) and assign references their **own** `numId`. Detected by the `numbering-consistency` check.
- **References start at `[47]` instead of `[1]`.** The reference list shares `numId=1` with body Heading 2/3 paragraphs, so the counter has already advanced through 46 sections before it reaches `[1]`. → Allocate a fresh `numId` for the reference list. Detected by the `ref-counter-independence` check.
- **Body running header reads "致谢".** Body and back-matter were collapsed into one section, and that section uses a `headerReference` whose target `headerN.xml` has the static text `致谢`. → Run `scripts/set_styleref_header.py final.docx --header headerN.xml --style-id 1 --in-place` to replace the static text with a `STYLEREF` field that resolves to the current chapter heading. Detected by the `body-header-non-back-matter` check.
- **Header prints `错误!使用'开始'选项卡…` or `Error! No text of specified style…`.** A `STYLEREF "Heading 1"` field references the **display name** of the heading style; on localized templates the actual style name is "heading 1" (lowercase) or "标题 1", and the field cannot resolve. → Use `STYLEREF 1` (the numeric `styleId`); `set_styleref_header.py` defaults to this. Detected by the `pdf-field-errors` check when `--pdf` is supplied.
- **Body page numbers don't restart at 1.** The body section has no `<w:pgNumType>` and silently inherits whichever format the previous (Roman) section used. → Set `<w:pgNumType w:fmt="decimal" w:start="1"/>` on the body section's `sectPr`. For thesis templates that demand a **separate** Roman TOC section and Arabic body section, insert a section break between TOC and the first body chapter and give each its own `pgNumType`.
- **3 figures missing from a 25-figure thesis.** Pandoc dropped them because the LaTeX `\includegraphics{name}` reference omits the extension and the basename also matches a vector file (`name.pdf` / `name.vsdx`) which pandoc cannot embed. → Either preprocess the LaTeX to add `.png` to every `\includegraphics`, or post-process the rough DOCX to insert the missing images at their caption paragraphs (`from docx import Document; new_p.add_run().add_picture(...)`). Detected by the `figure-count-vs-source` check when `--source-latex-dir` is supplied.
- **Tables render as borderless instead of three-line.** A project pipeline forgot to call `format_three_line_tables`, or only ran `set_cell_border` through python-docx's `cell` wrappers (which silently no-op on `vMerge="continue"` cells whose wrappers collapse onto the merge-start cell above). → Call `format_three_line_tables` from `adaptive_docx_pipeline.py`, or fall back to writing `<w:tcBorders>` directly into the raw `<w:tc>` elements inside `<w:tr>`. Detected by the `table-border-style` check with `--expected-table-style three-line`.
- **Citations rendered as `(Author Year)` instead of GB/T-7714 `[N]` superscript.** Pandoc with default `--citeproc` (or no citeproc at all when the source uses `\cite`) emits `(Zhu et al. 2025)`-style author-year tokens — visible but **not** a Word hyperlink and **not** the numeric format Chinese thesis templates require. The structural validator counts paragraphs and reference bookmarks; it does not see that the in-text mark format is wrong. → After pandoc, parse `main.bbl` for `\bibitem{key}` order to build a `cite_key → number` map and a per-key `(first_surname, year)` token; walk every paragraph in `document.xml` looking for `(Author Year[; Author Year]*)` patterns; replace each with `[N1, N2]` wrapped in `<w:hyperlink w:anchor="ref_N">` runs that carry `<w:vertAlign w:val="superscript"/>`. **Disambiguate same-(surname,year) collisions** (e.g. two `Lozano-Cuadra 2024` or two `Lu 2025` entries) by combining the bbl opt's secondary author list **and** the first author's initial from the bbl author line — pandoc emits `(W. Lu et al. 2025)` vs `(J. Lu et al. 2025)` exactly to disambiguate. Use word-boundary `\b<initial>\b` matching so single letters do not accidentally match inside `et al.`. Detected by the `citation-coverage` check.
- **Captions missing the `图 X.Y` / `表 X.Y` number prefix and not centered.** Pandoc maps `\caption{}` to a plain body style without the chapter-relative number; `\begin{figure}` / `\begin{table}` envs that contain no embeddable visual (e.g. complex multirow tables) are dropped entirely, taking their captions with them. → Walk the docx body, advance a chapter counter on every body H1, count drawings (collapsing adjacent drawing paragraphs into one figure-group) and data `<w:tbl>` elements per chapter, and insert a centered caption paragraph after each figure-group / before each table. Source captions for the text content come from re-parsing each chapter's `.tex` for `\begin{figure}…\caption{…}` and `\begin{table}…\caption{…}` envs in document order. If pandoc dropped a table entirely, the missing caption surfaces as a `caption-count-vs-source` FAIL — re-render the lost `<w:tbl>` from `\begin{tabular}` separately rather than masking the gap. The three render-check pieces (`caption-numbering`, `caption-centering`, `caption-untagged-near-figure-table`) each enforce a different invariant; do not collapse them into one "caption format" check, because each can hide the others (e.g. centering everything that *happens to be* a numbered caption is meaningless if the numbering itself is missing on half the captions).

## Validator-authoring discipline

When you add or change a check inside `validate_docx_render.py` (or any
text-pattern rule that disambiguates between candidates), follow these two
rules. Both come from real regressions on this skill.

1.  **Translate every user-visible requirement into its own enforcement, not
    just its own detection.** When the template demands "captions must be
    `图 X.Y 说明` AND centered", that is *two* requirements. A single
    `check_caption_format` that filters paragraphs to "those already
    matching `图 X.Y …`" and then checks `w:jc=center` only enforces the
    centering half — captions that lost the `图 X.Y` prefix are silently
    dropped from the candidate set and never reported. Split such checks
    into one per requirement (in this skill: `caption-numbering`,
    `caption-centering`, `caption-untagged-near-figure-table`) and make sure
    the candidate filter for each does not depend on the other requirements
    being met. The candidate filter for the "numbering" check must accept
    paragraphs whose lead is `图`/`表` *with a digit follow* (so body
    sentences like `表格型 Q-learning…` or `表中的实验配置…` are excluded
    by the `\d` requirement, not by accidentally matching the numbering
    pattern).

2.  **Disambiguation rules need a unit test before commit.** When a citation
    or anchor disambiguator picks one of N candidates by a heuristic
    ("with `et al.` → the one with more secondary authors"), write the
    minimal unit test first:
    `assert disambig("(Lozano-Cuadra et al. 2024)") == "lozano2024"`. The
    fall-back direction (`keys_sorted[0]` vs `keys_sorted[-1]`) is
    coin-flip easy to write backwards from the comment, and the only
    cheap way to catch the inversion is a fixture-driven test, not code
    review. For the GB/T 7714 citation rewriter specifically: when two
    bbl entries share `(surname, year)` and both carry `et al.`, prefer
    the one whose secondary-author set or first-author initial matches
    the rendered author-year token; use word-boundary `\b<initial>\b`
    matching so a single-letter initial does not accidentally match
    inside `et al.` itself.



When a user files a list of complaints (e.g. "red text / double numbering /
reference numbers / wrong header"), treat the list as a **sample**, not as an
exhaustive bug catalog. Before reporting completion, run an explicit
"source vs output" content audit at minimum:

1.  Count `\includegraphics` (or equivalent figure references) in the source
    project and compare to `<w:drawing>` in the final docx.
2.  Count `\caption` directives and compare to caption-styled paragraphs.
3.  Count `\begin{table}` and compare to `<w:tbl>` count *with three-line
    borders applied* if the template requires three-line tables.
4.  Walk the contact-sheet preview PNG of the exported PDF and look at every
    page where a body chapter starts; compare visible figure count and
    visible table border style against the source.

Concretely, do not declare success based only on a structural validator's
`PASS`. Run the render validator with `--source-latex-dir`,
`--expected-table-style`, and `--pdf`, and fix anything they surface.


## Script Guide

- `scripts/inspect_docx_template.py`: dumps template styles (including those defined but unused in the body), paragraphs, tables, section settings, numbering hints, and hyperlink colors.
- `scripts/adaptive_docx_pipeline.py`: reusable starter pipeline for template-based reconstruction. It is a code base to copy and patch, not a final institutional-template converter. Behavior is config-driven (`--config`). It remaps copied DOCX style IDs by visible style name by default, provides run-preserving replacement helpers for protected regions, and can scope formatting with `formatting_start_marker` / `formatting_end_marker`. Optional config keys include `clear_header_references`, `clear_footer_references`, and `heading_1_page_breaks`. Three-line tables and other Chinese-thesis-specific tweaks are opt-in.
- `scripts/finalize_word_docx.py`: updates Word fields/TOC and optionally exports PDF through Word COM. Disables macros for safety, bootstraps missing Windows environment variables, and falls back through `EnsureDispatch`, `DispatchEx`, and `Dispatch`; use `--prefer-dispatch-ex` when an existing Word instance is unreliable.
- `scripts/validate_docx_conversion.py`: structural QA for common failures, including template placeholders, body/back-matter ordering, heading-style preservation, inherited section headers, image/table counts, and protected front-matter format drift against the original template.
- `scripts/validate_docx_render.py`: render-level QA that complements the structural validator. Twelve checks (TOC field, numbering consistency, multilevel heading format, reference-counter independence, body-header literal, figure-count-vs-source, table-border-style, citation-coverage, caption-count-vs-source, caption-numbering, caption-centering, caption-untagged-near-figure-table) plus the `pdf-field-errors` check when `--pdf` is supplied; each can be demoted with `--allow`. Run after Word COM finalization.
- `scripts/inject_toc_field.py`: idempotently insert a `{ TOC \o "1-3" \h \z \u }` field after the 目录 / Contents / Table of Contents heading. Use when a rough conversion produced a TOC heading without a TOC field. Word's "update fields" cannot populate a TOC that isn't there.
- `scripts/set_styleref_header.py`: rewrite a single `headerN.xml` so its first paragraph contains a `STYLEREF <styleId> \* MERGEFORMAT` field that resolves to the current chapter title. Use `--style-id 1` (numeric form) for portability — the display-name form fails on localized templates and prints `错误!使用'开始'选项卡…` in the rendered header.
- `scripts/render_pdf_preview.py`: renders selected PDF pages into contact sheets for visual QA.
- `presets/zhengzhou_thesis.json`: style/table/hyperlink config for the Zhengzhou-University case study. It does not delete sample pages, fill cover fields, replace abstracts, rebuild TOC, or repair section headers by itself.

## References

- Read `references/pandoc-limitations.md` when explaining why this workflow differs from pandoc defaults.
- Read `references/zhengzhou-case-study.md` when building or adapting a university-thesis pipeline.
