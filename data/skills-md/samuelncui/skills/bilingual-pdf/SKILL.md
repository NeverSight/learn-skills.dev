---
name: bilingual-pdf
description: Render or edit side-by-side bilingual PDFs (parallel text) from supplied source and translation pairs, with aligned paragraphs, table rows, lists and figures. Use native LaTeX, structured JSON or reviewed translation JSONL for articles, reports and handouts, including LTR, RTL and CJK scripts. Not for OCR, automatic translation or preserving an existing PDF layout.
license: MIT
compatibility: Requires XeLaTeX, latexmk and document fonts. JSON import and optional PDF checks also need Python packages; see requirements.txt and references/languages.md.
---

# Bilingual PDF

This is a layout tool. Accept the text pairs, rows and document structure supplied by the calling agent; render their corresponding units at aligned positions. Content selection, translation and semantic pairing belong to that agent. Before layout, check the supplied ordered language pair, corresponding units and requested edition; return missing or ambiguous pairings to the caller. Preserve the supplied wording and solve fit problems through the layout choices below.

## Route raw source or supplied pairs

For supplied corresponding texts, continue directly with this skill. For a request that includes translation from raw source, discover the installed `bilingual-translation` skill through the host and use its source-first workflow to prepare one reviewed paired manuscript. Record its tested revision in the working project. If unavailable, report the missing skill and use the host's authorized installation flow; installation is not automatic.

That workflow owns source capture, translation and semantic review. Return its existing reviewed pairs here for layout. Native paired TeX remains a first-class input. Consume the reviewed translation JSONL master directly using the route below. The [translation handoff](references/translation.md) also documents semantic exchange import. Native authoring does not depend on either exchange format.

## Select an input route

Resolve paths relative to this installed skill and start in a fresh working directory. Preserve supplied inputs. Start with the [human guide and dependency checks](README.md#dependencies-checks-and-delivery). In an existing project, read its environment/build instructions and activate the installed toolchain before preflight; tools outside PATH are not evidence that they need installing.

- Native LaTeX: read [the native API and minimal build](references/latex.md#project-and-build-contract). Adapt a worked project in `examples/` or use the minimal native document. Build with XeLaTeX/latexmk without Python.
- Reviewed translation JSONL: read [translation handoff](references/translation.md), discover the installed translation skill, then run `python3 scripts/bilingual_pdf.py render master.jsonl --translation-skill "$TRANSLATION_SKILL" --output new-project`. The master must have current reviewed targets. Use the same input/options with `preflight`, `export` or `build` as needed. Render the JSONL itself; the separate semantic exchange converter is not a prerequisite. No intermediate layout file is required. Tune global settings with `--layout '{"font_size":10.5,"leading":14}'`; sparse overrides use the documented layout schema and leave the master untouched. Split children remain one paragraph with aligned child starts and natural page breaks; shorter sides leave alignment whitespace. Export retains every master record and an ID-to-anchor map. Edit the master through the translation workflow and rebuild.
- Structured JSON: read [the input contract and minimal input](references/input.md#minimal-input) and [JSON Schema](schemas/document.schema.json). Run `python3 scripts/bilingual_pdf.py export input.json --output new-project`, or use `render` to export, compile and mechanically check. For repeated JSON edits, use `build input.json --output managed-project` from the first build onward; rerun that command in the same managed project. Image paths are relative to the input directory unless `--asset-root` is supplied.

Both routes use the one canonical `assets/paralleltext.sty`. Export produces an editable, portable native project. Choose a new output directory for each export/render attempt; existing directories are rejected to preserve earlier work. The separate `build` command safely updates only its recorded generated files, preserves unchanged files and latexmk dependencies, and reruns preflight and mechanical QA. Keep editing the JSON on this route. For direct native edits, keep the exported project and run latexmk plus PDF validation; `build` rejects manually changed generated files. See [incremental builds](references/input.md#incremental-builds). Use the installed package and helpers directly, so the project remains buildable without a repository checkout.

## Map structure to layout

Use `ParallelParagraph` with a global `paragraph-flow=keep|breakable` choice and per-block `[flow=keep|breakable]` override. JSON uses `layout.paragraph_flow` and paragraph `flow`. Explicit `ParallelText` stays bounded; `ParallelProse` permits continuation. The next pair resynchronizes after both sides finish. Table rows and list items align independently. A JSON table stays together as a complete group; native authors can allow breaks between bounded rows. Neither route splits a row automatically.

Use `ParallelWideFigure` (`placement: "shared"`) for one shared full-width image with paired captions. Use `ParallelFigure` (JSON `image: [left, right]`) for localized images. Example photographs and diagrams belong to `examples/shared/`; they are not generic runtime assets.

Language direction and physical column position are independent. Read [language setup](references/languages.md) when changing fonts or scripts, especially RTL/CJK and mixed-script expressions. If a font, image or tool is missing, report its exact name/path and the blocked stage; use the authorized environment workflow to install/retrieve it, or ask the caller to approve an alternative if none is already authorized, then resume that stage.

Trusted native adapters can use the [source-bound text API](references/bound-text.md) to merge exact-source mathematical spans and resolved references with canonical escaping. Keep source review and native trust explicit.

## Configure and validate

Defaults require no setup. Read [configuration](references/configuration.md) for sparse native keys, standard package hooks and the JSON subset. Keep language/font selection, manuscript content and layout settings separate. Fix layout problems in the canonical configuration or implementation rather than changing supplied wording, shrinking individual blocks or duplicating example-specific styles.

Run structured `preflight` when using JSON and the [rendering acceptance checks](references/acceptance.md). Inspect actual PDF pages for aligned starts/rows, continuations, glyphs, RTL shaping, image/caption placement, clipping, references and print geometry. Report passed, failed and unrun checks separately; compiler success alone is insufficient for visual acceptance.

## Deliver and preserve the trust boundary

Deliver the PDF and portable editable native project, plus JSON when used. Include required package/image files and their licenses. The helper does not translate, assess factual correctness or certify accessibility. Supplied native TeX and latexmk configuration execute code; `-no-shell-escape` is not a filesystem sandbox. Use trusted inputs or appropriate isolation. Obtain applicable authorization before external processing or publication, and keep private material out of public examples.
