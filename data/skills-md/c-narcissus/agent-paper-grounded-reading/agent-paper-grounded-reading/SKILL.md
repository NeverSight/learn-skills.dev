---
name: agent-paper-grounded-reading
description: Deeply read a computer-science paper from a user-provided PDF, paper title, or LaTeX source. Use when Codex or similar local agent tools need a source-grounded, research-generative reading workflow that produces a deep report, traceability artifacts, a research lens for idea generation, reusable PDF/LaTeX audit artifacts, and a mandatory launched static evidence reader.
---

# Agent Paper Grounded Reading

Use this skill in **local AI agent tools** when the user wants a **deep, paper-grounded, research-generative reading** for one computer-science paper or a small paper batch, starting from any of these inputs:

- a user-provided PDF
- a user-provided LaTeX source tree or `.tex` files
- only the paper title or citation-like paper name

The primary deliverable is a **complete, long-form Markdown report**.
Do not compress the report into a short summary.
The report file has no artificial length cap: it should be long enough that a reader can understand the paper's motivation, method, formulas, experiments, evidence, limitations, and research opportunities without opening the original paper first.
The default secondary deliverables are:

- a **traceability bundle** that maps report claims back to source evidence
- a **research lens artifact** that extracts idea-generating patterns from the paper
- a mandatory **static evidence reader** for interactive PDF/report verification
- an optional **connected cartoon storyboard** when image generation is available and the user has not opted out

## Usage Examples

- "Use `agent-paper-grounded-reading` to deeply read `paper.pdf` and create grounded report artifacts."
- "Use `agent-paper-grounded-reading` to read this paper from LaTeX source, validate every claim, and build the static evidence reader."
- "Use `agent-paper-grounded-reading` to analyze this paper from an author-thinking perspective and extract new research ideas without losing source grounding."

## Runtime Requirements

The bundled deep-reading scripts use Python 3.9+.
PDF extraction, PDF fallback validation, and static reader building require `PyMuPDF>=1.24.0`.
The static reader builder additionally requires `Markdown>=3.6` and `latex2mathml>=3.81.0` from `requirements.txt`.
`latex2mathml` is mandatory for readable formulas and symbols in the static reader; do not accept raw LaTeX fallback as a successful reader build unless the user explicitly asks for fallback behavior.
For LaTeX-to-PDF source highlighting, a TeX distribution that provides `pdflatex` and `synctex` is recommended.
For interactive web viewing, this complete package includes `scripts/build_reader_bundle.py`, `scripts/serve_bundle.py`, and `assets/reader_template/`; no separate reader skill is required.
Bundled scripts write only to user-specified output paths.
This project is designed for Codex, Trae, Claude Code, and similar **local agent workflows**, not browser-only chat products.
The static evidence reader is a mandatory completion artifact for every successful deep-reading run, not an optional add-on.

## Reusable bundled tools

Prefer these scripts instead of rewriting one-off PDF/reader code:

- `scripts/prepare_latex_source.py`
  Prepare a LaTeX-primary run from a `.tar.gz`, `.tgz`, `.zip`, `.tex`, or source directory.
  It safely extracts or copies the source into `<run_dir>/source`, discovers TeX entrypoints such as `main.tex` and `supplementary.tex`, optionally compiles them with `pdflatex -synctex=1`, runs `extract_latex_paragraphs.py`, writes `latex_source_manifest.json`, and creates a starter `reader_artifacts.json` pointing at the compiled PDFs and SyncTeX sidecars.
  Use it at the start of user-provided LaTeX archive/source-tree runs instead of manually unpacking, compiling, and wiring paths.
- `scripts/prepare_pdf_source.py`
  Extract PDF page text, page text blocks, optional rendered page previews, and an optional copied PDF into the run output directory.
  Use it at the start of PDF-primary and PDF-forbidden-LaTeX runs.
- `scripts/validate_pdf_snippets.py`
  Verify that every `locator_snippets` value in `traceability_manifest.json` is searchable in the referenced PDF with PyMuPDF, matching the reader's fallback locator behavior.
  Run it before building the reader for PDF-primary packages.
- `scripts/validate_traceability.py`
  Verify anchored report claims, manifest coverage, evidence rows, and structured/PDF fallback anchor shape.
- `scripts/build_reader_bundle.py`
  Build the static reader from `reader_artifacts.json` or explicit arguments.
  In PDF-primary mode, it no longer needs a fake SyncTeX file when no `latex_paragraphs.json` is supplied.
  It preprocesses report Markdown math delimiters (`$...$`, `$$...$$`, `\(...\)`, `\[...\]`) and math-like inline code into MathML before writing `report.html`.
  It treats bare paper symbols in inline code, such as `N`, `r`, `G_i`, `P_i^t`, `w_ij`, `alpha`, `phi_i`, and `psi_i`, as equations and normalizes Greek names plus multi-character subscripts before rendering.
  It also sanitizes LaTeX-source evidence paragraphs for the reader by converting equation environments to MathML and stripping presentational commands such as `\begin{...}`, `\textbf{...}`, captions, refs, and list markers from visible evidence text.
- `scripts/validate_reader_math.py`
  Verify that the built reader bundle does not expose raw LaTeX math delimiters, common raw LaTeX math commands, math-like code spans, bare `_i`/`^t` style symbols, or `math-fallback` spans in `report.html` and `evidence-map.json`.
- `scripts/build_and_serve_reader.py`
  Build the reader bundle, run `validate_reader_math.py`, launch `serve_bundle.py` in the background, wait for HTTP 200, and write `reader_url.txt`.
  Prefer this wrapper for the final mandatory reader step.

## Scope

This is a **standalone** skill.
Do **not** assume any upstream collection stage, bundle manifest stage, canvas stage, spreadsheet stage, or downstream workflow.
Work directly from the paper materials currently available in the workspace, conversation, or fetchable from the web with the tools already available in the runtime.

## Core source-acquisition policy

Always assemble the **best available reading package** before writing the report.
The preferred evidence order is:

1. **LaTeX source from arXiv**, if available and relevant to the same paper version
2. **User-provided LaTeX source**
3. **User-provided PDF or official paper PDF** from arXiv, OpenReview, proceedings, or author page as the authoritative visual and pagination reference
4. **Supplementary material, appendices, review threads, and rebuttals**

### A. When the user provides LaTeX

Use the provided LaTeX as the primary source.
Also use the compiled PDF if available, because figures, layout, and page-local argument flow are often easier to interpret in PDF form.

### B. When the user provides a PDF but not LaTeX

If the user explicitly says not to read, search, unpack, or use LaTeX/source files, obey that restriction and treat the supplied PDF as the only paper source.
In that case, do not search arXiv source, do not inspect local `.tex` or source archives, and state that the run is PDF-primary because of the user's source constraint.

Treat the PDF as the initial source, but first check whether the same paper has an **arXiv source / LaTeX package** available.
If yes, prefer the arXiv LaTeX as the primary structural source and keep the PDF as a visual and pagination reference.
If no matching arXiv LaTeX is available, continue with the original PDF and explicitly say that the analysis is PDF-primary and that report-point localization uses PDF fallback anchors.

### C. When the user provides only the paper title or a citation-like name

Search for the paper.
Try to obtain:

1. arXiv LaTeX/source package first
2. if no LaTeX is available, the best paper PDF
3. supplementary material if relevant
4. OpenReview thread if the venue is ICLR

When title matching is ambiguous, use authors, year, venue, abstract snippets, or method keywords to disambiguate.
Do not silently analyze the wrong paper.

### D. Matching discipline

When switching from a PDF or title to an arXiv source package, verify that the source corresponds to the same paper by checking as many of the following as possible:

- exact or near-exact title
- author list
- abstract
- venue / year / version notes
- core method names
- section structure

If there is a mismatch or uncertainty, say so explicitly and choose the most reliable source set.

## ICLR / OpenReview policy

If the target paper is an **ICLR paper**, try to retrieve the **same-year OpenReview submission page**.
Use it to collect, when available:

- reviewer comments
- meta-review or area-chair summary
- author rebuttal / response
- revision signals relevant to acceptance

Use these materials to enrich the deep reading report, especially for:

- what reviewers found convincing or weak
- which claims were challenged
- whether the rebuttal resolved those concerns
- how the review discussion changes confidence in the paper's claims

If the OpenReview thread cannot be found, state that clearly and continue with the best grounded report possible.

## Research-generative overlay

This skill does **not** stop at summary or traceability.
It must also help the user discover **new ideas**.

Read the paper as a **hidden design trajectory**, not only as a finished artifact.
Use [references/research-generative-methodology.md](references/research-generative-methodology.md) whenever the user wants an author-perspective reading, research inspiration, idea mining, story-pattern extraction, or boundary-pushing future directions.

The default research-generative questions are:

- What important old success depends on which hidden assumption?
- Which real-world constraint breaks that assumption?
- What tempting imported method almost works, and why does it still fail?
- What unavailable mechanism `Y` did the authors replace with a surrogate `Z`?
- How did the authors map concrete failures into modules, ablations, and claims?
- Why does each key citation appear in the story rather than merely in the bibliography?
- Which hidden assumption can be violated to create the next strong paper?

When there is tension between conservative summarization and idea generation:

- never invent evidence
- keep all report claims grounded in the source package
- distinguish direct evidence, plausible inference, and speculation
- choose the framing that is **most useful for finding new research directions** without overstating certainty

## Output policy

Generate four coordinated output classes by default:

1. a **human-readable Markdown deep-reading report** that is complete enough to teach the paper on its own
2. a **machine-readable grounded artifact set** that lets downstream tools connect report claims back to source evidence
3. a **machine-readable research lens artifact** that captures the paper's idea-generating grammar
4. a **built and launched static evidence reader** served from a local URL so the user can inspect report claims against the source immediately

When LaTeX source or another structured text source is available, generate these artifacts next to the report:

- `latex_source_manifest.json` when `scripts/prepare_latex_source.py` is used
- `latex_paragraphs.json`
- `traceability_manifest.json`
- `reader_artifacts.json`
- `research_lens.json`
- `storyboard_manifest.json` and/or `storyboard_prompts.md` when storyboard output is produced
- `reader_bundle/` built with `scripts/build_reader_bundle.py`
- a local reader URL launched with `scripts/serve_bundle.py`

When the run is PDF-primary, generate these artifacts next to the report:

- a PDF extraction artifact from `scripts/prepare_pdf_source.py`, normally `pdf_pages.json`
- a plain text extraction file such as `<paper_stem>_pdf_text.txt`
- `traceability_manifest.json` with `pdf::...` fallback anchors and robust `locator_snippets`
- `research_lens.json`
- `reader_artifacts.json` that omits `latex_paragraphs.json` and SyncTeX entries
- `reader_bundle/` and a live local reader URL launched with `scripts/build_and_serve_reader.py`

These artifacts are part of the default deliverable for this skill because downstream grounded readers and idea-mining workflows depend on them.
Use:

- [templates/report_template.md](templates/report_template.md) for report shape
- [templates/traceability_manifest.template.json](templates/traceability_manifest.template.json) for claim-evidence mappings
- [templates/reader_artifacts.template.json](templates/reader_artifacts.template.json) for the portable reader manifest
- [templates/reader_artifacts_pdf.template.json](templates/reader_artifacts_pdf.template.json) for PDF-primary reader manifests without SyncTeX or `latex_paragraphs.json`
- [templates/research_lens.template.json](templates/research_lens.template.json) for the structured research-generative summary
- [templates/storyboard_manifest.template.json](templates/storyboard_manifest.template.json) for report-grounded storyboard metadata
- [references/traceability-contract.md](references/traceability-contract.md) for claim rules
- [references/reader-artifact-contract.md](references/reader-artifact-contract.md) for reader packaging rules
- [references/research-lens-contract.md](references/research-lens-contract.md) for the idea-mining artifact schema

The paragraph index must preserve source file paths and line spans so downstream readers can use SyncTeX for precise audit anchors and then expand the visual PDF highlight to the containing paragraph block rather than only thin line slices.
When the reading is PDF-primary and no LaTeX exists, do not block on a synthetic line index.
Instead, keep `traceability_manifest.json` evidence rows on explicit `pdf::...` fallback anchors with strong `locator_snippets`, and require the reader to expand each snippet hit to the containing PDF paragraph or text block rather than a thin line box.

### Report completeness requirement

The report is the main deliverable, not a preview.
Do not optimize it for chat brevity, token economy, or a short executive-summary style.
The static reader must show the full report, and the report itself must preserve enough detail that the user can learn the original paper from the report alone.

Required behavior:

- Write full explanatory prose after anchored claims in every section; do not leave sections as only 1-2 bullets.
- Preserve all key formulas and explain them equation by equation, including symbol meanings and algorithmic roles.
- Explain every major module, figure, table, ablation, and experimental setting that materially supports the paper's claims.
- Include concrete examples for algorithms or pipelines whenever the paper's method is operational rather than purely conceptual.
- State what evidence supports each important judgment and what remains inferential.
- Prefer adding more grounded detail over shortening, unless the user explicitly asks for a concise version.
- Do not reuse an older short report as the final answer for a fresh run unless it is expanded and revalidated against the current source package.
- The final chat message can be concise, but `report.md` must not be simplified.

### Traceability-first requirement

Every user-facing report point must be grounded.
For each major report section, begin with `### Anchored Points` and list one or more claims in the exact form:

- `[C<section>.<index>] claim text`

Every claim ID that appears in the Markdown report must also appear in `traceability_manifest.json`.
Every claim must have at least one evidence row, and the evidence list must be exhaustive for that claim.
Every evidence row must point back to a source anchor:

- preferred: a LaTeX paragraph ID from `latex_paragraphs.json`
- fallback when no LaTeX exists after explicit search: a PDF text-block anchor, clearly marked as fallback
- in PDF-primary mode, the fallback anchor must still support paragraph-level highlighting in the reader by expanding the matched snippet to the containing PDF paragraph or text block

Do not silently leave any claim ungrounded.
Do not omit supporting evidence when one report point depends on multiple original paragraphs, formulas, tables, figures, captions, or supplementary sections.
If a report point depends on several source locations, include one evidence row per materially necessary source location.
If a point actually contains multiple independent claims, split it into multiple anchored claims instead of hiding multiple arguments under one incomplete evidence row.
If a claim is only a plausible reconstruction of the authors' reasoning, still map it to the exact paragraph(s) that motivate the reconstruction and mark the claim as inferential in `traceability_manifest.json`.

### Validation step

Before finishing, run:

- `scripts/extract_latex_paragraphs.py` to build `latex_paragraphs.json`
- `scripts/validate_traceability.py` to verify that every anchored claim in the report is covered by the manifest and that every referenced paragraph ID exists

When the final reading package is PDF-primary and no LaTeX was found, skip `scripts/extract_latex_paragraphs.py`.
In that case, run `scripts/prepare_pdf_source.py` first, write `pdf::...` anchors in `traceability_manifest.json`, keep high-quality `locator_snippets`, run `scripts/validate_pdf_snippets.py`, and run `scripts/validate_traceability.py` without `--paragraphs`.

Also verify manually that every `claim_ids` reference in `research_lens.json` points to a real report claim ID.

### Storyboard output

If an image-generation API or tool is available in the runtime, and the user has not opted out, generate a **small sequence of connected cartoon-style storyboard images** after the report.
Use the completed deep-reading report as the storyboard context, not only the paper abstract.
The storyboard should:

- narrate the author's main idea step by step
- use recurring characters, objects, or visual metaphors across frames
- stay faithful to the report's explanation
- simplify without distorting the method
- avoid adding scientific claims not supported by the paper
- save a `storyboard_prompts.md` or `storyboard_manifest.json` entry when file output is being produced, so the reader artifact set can reference the storyboard

When no image-generation capability is available, do not fail the task.
Instead, include a short Markdown storyboard prompt set that could be used later.

## Language policy

Write the **skill instructions, internal prompts, and template skeletons in English**.
Choose the **report language** from the user's current request language by default.

- if the user's current request is primarily in Chinese, write the report in Chinese
- if the user's current request is primarily not Chinese, write the report in English
- if the user explicitly requests another language, follow that explicit instruction
- if the request is mixed-language, follow the dominant user language in the current request

When writing the report in Chinese:

- keep proper nouns and fixed technical identifiers in English
- this includes paper titles, method names, module names, datasets, baselines, theorem or object names, citation names, equation symbols, claim IDs, filenames, and JSON keys
- translate section headings and explanatory prose into Chinese, but do not translate artifact filenames, schema fields, or claim IDs

## Style policy

Stay close to the actual paper.
Do **not** drift into generic commentary.
Name the actual modules, formulas, assumptions, theorem objects, datasets, baselines, figures, captions, tables, empirical observations, and reviewer comments used in the paper.
Do not be overly brief.
Keep the report specific, evidence-backed, and concrete with paper-local details.

When inferring the author's likely intentions or subjective judgments, distinguish clearly between:

- evidence-backed interpretation
- plausible inference
- speculation

The report should sound like a research mentor reconstructing how the work may have been invented, not like a generic summarizer.

## Grounded workflow

1. Assemble the best source package.
2. If the user forbids LaTeX/source use, do not search or read it; continue with the supplied PDF only and PDF fallback anchors.
3. If only PDF exists and no matching LaTeX can be found, continue with PDF-only analysis and PDF fallback anchors instead of blocking the task.
4. For PDF-primary runs, run `scripts/prepare_pdf_source.py --pdf <paper.pdf> --output <run_dir> --doc-key <doc_key> --copy-pdf` before drafting the report.
5. If LaTeX is available as a source tree or archive, first run `scripts/prepare_latex_source.py --source <source> --output <run_dir> --compile`; if the source is already staged and compiled, at minimum run `scripts/extract_latex_paragraphs.py`.
6. If LaTeX is not available, keep the package PDF-primary and make every evidence row use `pdf::...` fallback anchors plus `locator_snippets` strong enough for PDF search.
7. Draft the report using anchored claim IDs in the Markdown itself.
   Make this a full teaching-grade report, not a shortened digest.
8. Fill `traceability_manifest.json` so each claim points to one or more paragraph IDs or PDF fallback anchors and PDF locator snippets.
9. Fill `research_lens.json` so the paper's research equation, story structure, module logic, citation functions, and future directions are captured in structured form.
10. Fill `reader_artifacts.json` to enumerate the report, traceability manifest, optional paragraph index, research lens artifact, PDFs, SyncTeX sidecars when available, and optional storyboard files.
11. Run `scripts/validate_traceability.py`; for PDF-primary runs, also run `scripts/validate_pdf_snippets.py --traceability traceability_manifest.json --pdf <doc_key>=<paper.pdf>`.
12. If the runtime has image generation and the user has not opted out, generate the connected cartoon storyboard from the completed report context.
13. Always build the static grounded reader before finalizing, preferably with `scripts/build_and_serve_reader.py --artifact-manifest reader_artifacts.json --url-file reader_url.txt`.
14. Ensure `scripts/validate_reader_math.py` passes for the built reader bundle; if it fails, fix the report math markup or install `requirements.txt` before finalizing.
15. Only then finalize the report.

## Interactive reader build requirements

Every successful run must build and serve the bundled static reader. The artifact set must preserve:

- `latex_paragraphs.json` entries with `source_path`, `line_start`, and `line_end`
- compiled PDFs plus `.synctex.gz` or `.synctex` sidecars
- claim IDs in the report that exactly match the traceability manifest
- `reader_artifacts.json` with `schema_version: "paper-reader-artifacts/1.0"`
- `research_lens.json` with `schema_version: "paper-research-lens/1.0"`

When the source package is PDF-primary, the reader may omit `latex_paragraphs.json`, but it must still:

- use `locator_snippets` to find the evidence hit in the PDF
- expand each hit to the containing paragraph or text block
- keep the visible highlight at paragraph granularity rather than line granularity
- launch the local static webpage after bundle generation so the user can open the interactive reader immediately

The bundled reader should then:

- use SyncTeX as the primary locator from LaTeX line spans to PDF coordinates
- expand located line spans or search hits into the containing PDF paragraph block when possible, so the visible highlight covers the whole relevant paragraph
- keep the PDF pane and report pane independently scrollable
- render the complete `report.md`/`report.html` content as the primary right-side pane for every PDF-primary, LaTeX-primary, and mixed-source run
- never replace the right-side report with a shortened claim index, research-lens summary, abstract, or generated digest
- keep research-lens cards and claim-index cards as secondary navigation aids after the full report, not as a substitute for the full report
- make claim clicks from research cards, evidence navigation, or claim-index cards scroll to the matching anchored claim in the full report body whenever that claim exists there
- let users resize the evidence area and PDF viewport vertically inside the left pane
- give the PDF pane substantially more screen width than the report pane under normal desktop layouts
- scale the left PDF viewport so at least one complete PDF page is visible under normal desktop layouts
- allow users to zoom PDF content in or out inside the fixed PDF pane without resizing the surrounding layout
- render report and evidence formulas/symbols as readable MathML instead of raw LaTeX source when the source text contains equations
- convert report-body `$...$`, `$$...$$`, `\(...\)`, `\[...\]`, and math-like inline code spans before Markdown conversion so the full right-side report does not leak raw LaTeX
- render common paper symbols written as inline code (`G_i`, `P_i^t`, `w_ij`, `phi_i`, `psi_i`, `alpha`, single-letter variables such as `N` and `r`) in Word-equation-like form rather than as literal underscore text
- require `validate_reader_math.py` to pass before treating the static reader as complete
- keep report/evidence text compact enough that it does not crowd the PDF
- surface the research equation, replacement mechanism, challenge-to-module logic, and boundary-pushing ideas without hiding the underlying traceability

If `traceability_manifest.json` contains evidence from web pages, review threads, metadata pages, or other sources that the bundled reader cannot highlight directly, keep those rows in the full traceability manifest and create a reader-specific manifest such as `reader_traceability_manifest.json` that keeps at least one local PDF/LaTeX/PDF-fallback evidence row for every report claim. Validate the full manifest and the reader-specific manifest before building the reader.

Serving the reader is part of the default finish condition for **all** source modes, including LaTeX-primary, mixed-source, and PDF-primary packages.
Use `scripts/build_and_serve_reader.py --artifact-manifest reader_artifacts.json --url-file reader_url.txt --open` or an equivalent background launch so the user receives a live local URL instead of only an artifact path.

## Mandatory report requirements

The report must explicitly cover the following whenever the available materials support it.
The detailed heuristics for the author-perspective sections live in [references/research-generative-methodology.md](references/research-generative-methodology.md).

When writing formulas or math symbols in the report, wrap formulas in Markdown math delimiters (`$...$`, `$$...$$`, `\(...\)`, `\[...\]`) or wrap short symbols in inline code so the reader builder can convert them to MathML.
Use inline code for short paper symbols such as `G_i`, `P_i^t`, `w_ij`, `phi_i`, `psi_i`, `alpha`, `N`, and `r`; the builder will render them like Word equations.
Do not leave naked LaTeX commands such as `\alpha`, `\theta`, `\sum`, or `\frac` in ordinary prose.

For every mandatory section below, write the anchored claims first, then add enough non-claim explanatory text, tables, formula walkthroughs, examples, and critique to make the section self-contained.
Do not treat the section checklist as permission to write only one claim and one short paragraph.

### 1. Paper identification and source package used

Report:

- title
- authors if available
- venue / year / status if available
- whether the reading was LaTeX-primary, PDF-primary, or mixed-source
- what sources were actually used
- whether arXiv LaTeX was searched for and whether it was found
- whether OpenReview materials were used

### 2. One-sentence thesis and research equation

State the paper in one compact sentence using the research-generative lens.
When appropriate, express it as:

- an old success that depends on a broken assumption
- a hard setting that invalidates that assumption
- a borrowed tool that almost works
- an unavailable mechanism `Y`
- a surrogate mechanism `Z` that the paper constructs instead

### 3. Title interpretation

Interpret the title term by term.
Explain what each keyword means, why the title is phrased that way, and how the title maps to the actual method, setting, and claims.

### 4. What problem the paper really solves

Explain:

- the direct paper-level problem
- the practical pain point
- the scientific question behind the method
- the upper multi-layer problem ladder

Prefer a continuous ladder such as:

- direction-native problem
- parent-field problem
- broader AI / ML problem

Also discuss upper problems suggested by:

- borrowed algorithm families
- bottlenecks introduced by the proposed method itself

### 5. Scientific problem ladder

Make the problem ladder explicit instead of burying it in prose.
Connect the direct task to broader research pressure and to the larger scientific boundary the paper is trying to move.

### 6. How the authors may have found this direction

Reconstruct the likely discovery path in evidence-backed language such as:

- what dissatisfaction or unrealistic assumption may have triggered the work
- what neighboring method almost transferred
- what blocked direct transfer
- what unavailable mechanism the paper replaced
- why this replacement creates a promising new direction

Never present private author intent as certainty.

### 7. How the authors built the story

Explain the paper's narrative construction.
Map:

- challenge
- failure mode
- design principle
- module
- ablation or evidence

Also explain whether the story forms a coherent loop rather than a bag of modules.

### 8. Related work, key citations, and what was still missing

Do not only list cited papers.
For the key papers repeatedly discussed by the target paper, explain:

- what they solved
- what they still left open
- why the current paper needed to move beyond them
- how each one relates to the current paper
  - inherited
  - contrasted
  - generalized
  - specialized
  - hybridized
  - problem-shifted

Also explain the **narrative role** of each key citation: field anchor, limitation evidence, method ancestor, baseline pressure, protocol justification, or contrast boundary.

### 9. Main idea

Explain the core idea in paper-grounded terms.
Do not stop at module names.
State what conceptual replacement or coordination logic makes the idea coherent.

### 10. Symbols, concepts, and notation

Introduce important symbols, operators, assumptions, and problem-specific concepts before heavily relying on them.
Explain them in beginner-friendly language while remaining faithful to the paper.

### 11. Formula preservation and explanation

Do **not** omit key equations.
Preserve and explain the important:

- objective functions
- update rules
- constraints
- estimators
- bounds
- theorem statements

For each key formula, explain:

- what each symbol means
- why the formula is introduced
- what role it plays in the method
- which algorithm step or system behavior it corresponds to
- why the authors likely used this form rather than a nearby alternative
- whether the formula appears limited, heuristic, fragile, or improvable

### 12. Theory, proof, and practice mapping

If the paper contains theory or proofs, explain:

- what is being proved
- why the authors chose to prove it
- what scientific or reviewer concern the proof addresses
- what practical meaning the theorem has

Then map theory to practice:

- theorem assumptions -> implementation assumptions
- proved objects -> implemented objects
- proof conclusions -> expected practical behavior

Judge whether theory and implementation are:

- exactly aligned
- approximately aligned
- only loosely connected

Also explain where theory stops being faithful to the actual implementation and whether that gap seems acceptable.

### 13. Algorithm or module walkthrough with concrete examples

Do not stop at equations.
Give a step-by-step explanation of the algorithm or module pipeline.
Whenever possible, include at least one concrete mini-example that instantiates:

- inputs
- states
- intermediate quantities
- outputs
- updates

### 14. Method deep reading: the author-thinking behind each module

For every important module, explain:

- the failure being fixed
- the ideal but unavailable solution
- the still-available proxy signal or resource
- the design choice that converts the proxy into a working mechanism
- the hidden assumption that makes the module plausible
- the risk or failure case
- the future research point that appears if that assumption breaks

### 15. Figures from both PDF and LaTeX

For **PDF papers**, explicitly interpret key figures instead of merely summarizing them.
For **LaTeX sources**, also reconstruct and explain important figures from figure environments, captions, labels, referenced text, and included image paths when possible.

For each important figure, explain:

- what the figure is trying to show
- how to read it
- what claim it supports
- whether the figure really supports that claim
- whether anything in the visual presentation is unclear, weak, or potentially misleading

### 16. Experimental design

Explain:

- datasets
- tasks
- baselines
- metrics
- ablations
- implementation details when available

Also connect the compared methods back to the related-work landscape in the introduction and related-work sections.

### 17. Experiments as story evidence and claim alignment audit

For each important table, plot, or result block, explain:

- what claim it is supposed to support
- what counterfactual or alternative explanation it rules out
- what stress condition makes the result meaningful
- whether it strongly supports, partially supports, or fails to support the claim
- whether the ablation really proves the claimed module role
- whether there is any tension or inconsistency between results and claims

### 18. Reviewer-lens audit

Include an explicit reviewer-style audit that comments on:

- novelty
- significance
- technical soundness
- methodology rigor
- reproducibility
- clarity of figures and tables
- results-claims alignment
- missing baselines or controls
- honesty about limitations

If ICLR OpenReview material is available, integrate reviewer concerns and author responses into this audit.

### 19. Innovation points and claim-by-claim support audit

List the paper's main claimed contributions and judge, for each one, whether it is supported by:

- theory
- experiments
- qualitative evidence
- reviewer discussion
- only weak evidence

### 20. Story-making pattern worth learning

Extract a reusable paper-making pattern from the paper.
Possible patterns include:

- replacement story
- three-module story
- closed-loop contribution
- two-axis empty-cell positioning
- boundary-pushing hidden-assumption break

This section should help the reader generate future papers, not only understand the current one.

### 21. Weaknesses, limitations, and improvement room

Discuss:

- unresolved weaknesses
- failure modes
- scope limits
- strong assumptions
- hidden costs
- where the idea might break

### 22. Innovation type and boundary judgment

Judge whether the paper is mainly:

- incremental
- cross-pollinated
- conceptually reframing
- potentially boundary-pushing

Explain why.
Also discuss whether it actually crosses subfield or disciplinary boundaries, or mainly recombines known ideas inside the same lane.

### 23. Future directions and boundary-pushing ideas

Propose future directions inspired by the paper, including:

- native next-step ideas
- cross-domain transfers
- stronger scientific-boundary directions
- alternative formulations or modules
- more decisive experiments

For the strongest future ideas, explicitly connect them to a hidden assumption whose failure would break the current method.

### 24. Simple vivid story summary

End with a simple, vivid, technically faithful story that helps a non-specialist remember the paper's core idea.

### 25. Sources used

End with a short source list stating exactly which materials were used, such as:

- user PDF
- arXiv source package
- paper PDF
- supplementary PDF
- OpenReview thread
- author rebuttal
- screenshots

## Optional final step: storyboard generation

After the Markdown report is finished, check whether image generation is available.

- If yes, create a concise storyboard plan with 4-6 sequential panels and then generate the cartoon-style images.
- If no, provide only the storyboard plan and prompts in Markdown.

The storyboard should stay synchronized with the report's explanation of:

- the original pain point
- the key intuition
- the core mechanism
- the training or inference flow
- the main empirical takeaway
- the research-generative lesson worth reusing

## Failure handling

If some sources cannot be found, do not abort.
State clearly what was attempted, what was found, what was missing, and how that affects confidence.
Then continue with the best grounded report possible.

If LaTeX cannot be found after an explicit search, say so clearly and switch the traceability artifact to PDF-block fallback mode instead of pretending paragraph anchors exist.
