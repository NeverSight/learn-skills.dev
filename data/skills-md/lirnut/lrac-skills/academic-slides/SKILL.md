---
name: academic-slides
description: Create and revise evidence-grounded academic presentations in single-paper, multi-paper, or review/survey mode. Use for journal clubs, research talks, field overviews, paper selection, scientific storylines, original figure explanations, source audits, editable Typst/Touying slides, Chinese speaker notes, and rendered-slide quality checks. 用于单篇精读、多篇论文汇报、通用综述、学术幻灯片及逐页讲稿。
---

# Academic slides

Build a traceable scientific argument, not merely a polished deck. Prefer source fidelity, understandable experiments, and editable source over narrative elegance or decorative layouts.

## Defaults and boundaries

- Follow explicit user requirements first. Otherwise use English audience text with original technical terminology, Chinese oral scripts retaining English technical terms, and a restrained academic layout. Impose no default duration, page limit, or seconds-per-slide rule.
- Default to `@preview/sci-brain-slides:0.1.0`, `academic`, with simple Touying heading-based source. Keep content in `main.typ`, appearance in `theme.typ`, and notes in per-page `#speaker-note[...]` blocks.
- Treat language, package, and layout as overridable defaults, not scientific rules. Only apply a duration constraint when the user supplies one; otherwise organize by the evidence and explanation needed. Do not invent a timed schedule.
- Read the existing project and preserve user work before editing. Do not modify library records or source PDFs merely to prepare slides.
- Keep local edits local: change layout without changing scientific meaning; do not delete content to merge pages or reorganize an agreed storyline without approval. Follow the scope and preservation rules in [production-workflow.md](references/production-workflow.md).

## Choose the talk mode

Before creating a new deck, ask which mode the user wants unless already explicit. Do not infer it from the number of PDFs alone. Record the choice in the working brief and read only the selected mode reference in addition to the global workflow:

| Mode | Explanatory job | Reference |
|---|---|---|
| Single paper | Explain one paper in depth: question, method, evidence, interpretation, and limits. | [single-paper.md](references/single-paper.md) |
| Multiple papers | Explain a bounded set of papers and their complementary or contrasting roles. | [multi-paper.md](references/multi-paper.md) |
| Review/survey | Synthesize a topic's research landscape, approaches, progress, debates, and evidence boundaries. | [review-slides.md](references/review-slides.md) |

For revisions, retain the established mode; do not restart intake for a spacing or wording change. A review is not necessarily a proposal defense or a systematic review. Do not require a personal research proposal or a gap-driven ending.

## OpenCode and self-contained operation

Read [opencode.md](references/opencode.md) for discovery, invocation, and resource resolution. Resolve bundled paths from this skill's base directory supplied by OpenCode, not from the active deck directory. The instructions, template, and scripts here must work in a new project without previous conversations, neighboring slide files, private PDFs, personal virtual environments, other installed skills, or a particular MCP server. Other skills may supplement this one but are never required.

Distinguish **independence from previous project data** from **scientific evidence**: acquire the current task's papers/data from user-provided files or verifiable authorized sources. Never generate empirical evidence to fill a missing source. If only a topic is given, find and inspect candidate full texts; if research access fails, report missing sources and produce an explicitly incomplete outline instead of fictional findings.

Read [production-workflow.md](references/production-workflow.md) and follow its planning fields, acceptance checks, and repair loop. Populate the bundled empty audit template from the current task rather than copying a previous deck's claims.

## Workflow and quality gates

### 1. Establish the question before selecting papers

Determine audience, purpose, available full texts, and output format. Record a duration only if supplied. Reuse known preferences rather than re-asking settled questions; proceed with stated assumptions for nonblocking choices.

Read [paper-selection.md](references/paper-selection.md). Record the actual question, task, evidence, and role of each selected study: a single-paper brief, a multi-paper selection matrix, or a theme-based review map. Connect papers through their evidenced roles, not a forced common mechanism. Get agreement on a materially changed paper selection before building the whole deck.

### 2. Audit evidence before writing claims

Read [evidence-and-figures.md](references/evidence-and-figures.md). Use abstracts for screening only. Inspect methods, figure captions, results, discussion, conclusions, and relevant supplements for final claims.

Create a separate `claim-sources.md`: slide/claim, exact source version and location, experimental conditions, metric/unit/denominator, evidence type, and interpretation boundary. Distinguish observation, author interpretation, modeling assumption, fitted statistical explanation, and validated causal evidence. Never upgrade one category into another.

When a source is unavailable, flag the gap; omit or qualify unsupported claims. Do not fabricate quotes, numbers, figures, or cross-paper conclusions.

### 3. Plan the explanation, not a fixed number of pages

Use **Problem → Approach → Results** for studies explained in depth; close with author-attributed interpretation and scope. For multi-paper and review decks, follow the selected mode's comparison or thematic structure rather than repeating a full study presentation for every source. Use short paper titles in overview tables and study headings, preserving published capitalization within titles.

Explain the task before showing effect sizes. For complex studies, include the actual process: setup → observed example → individual/group trajectories → aggregate results → model validation. Do not delete essential update-process figures just to meet a page target.

If the user supplies a duration, allocate it by explanation burden and rebalance after adding evidence. Label estimates as estimates. Otherwise omit timed schedules and do not truncate essential evidence to an assumed length.

### 4. Assemble readable, editable slides

For Typst, read [typst-workflow.md](references/typst-workflow.md). The bundled starter and reference are sufficient; optionally load `typst-touying` if available for features beyond the starter. Use `assets/typst-template/` as a starter in a **new** output directory; do not overwrite an existing presentation with the template.

- Keep a neutral background, restrained accent colors, consistent type scale, and minimal decoration. Prefer original paper figures and useful experimental details over ornamental cards.
- Give each page one explanatory job and choose its summary function: result, thematic synthesis, progress-and-limit, or transition. Do not force every summary to claim a gap. Keep slide titles visible and center body content vertically when appropriate. Try space and layout repairs before proposing a split; preserve content and ask before making substantive cuts.
- Put concise author/year/section/figure/page references in a fixed footer. Keep extraction explanations and labels such as “Verbatim” or “Paraphrase” out of audience slides.
- Preserve original figure data. Use rectangular PDF crops with provenance; inspect axes, legends, and neighboring-panel fragments visually.
- Write a complete, editable Chinese oral script per page. Explain axes, units, colors, sample/trajectory denominator, task/model conditions, takeaway, and limits. Do not merely translate bullets.
- Export readable scripts and presenter metadata from source notes; never maintain conflicting copies manually.

### 5. Build, inspect, and iterate

Use the bundled tools; run `--help` for options:

```sh
python <skill-dir>/scripts/build.py <deck-dir>
python <skill-dir>/scripts/extract_figures.py <manifest.json> --output-dir <asset-dir>
```

Check Python and dependencies before running; create an isolated environment if needed using the Typst reference rather than assuming a personal installation. The build checks page count, dimensions, text bounds, note coverage, and common unfinished placeholders and generates PDF, pdfpc metadata, Markdown scripts, and previews. Use `--draft` only for instructional-template/intermediate builds. It does **not** certify scientific correctness or visual quality.

During local iterations, inspect changed pages, affected neighbors, and the contact sheet; check numbering and notes after structural changes. Before final delivery, inspect every page, especially cropped figures and dense/table/formula pages. Check readability, real fonts, footer clearance, unexpected blank/overflow pages, cropping, and note leakage. Read the final talk against the source audit. Fix defects and rebuild in a new output directory. Stop only after no blocking defects remain; otherwise explicitly deliver a draft with outstanding blockers. Do not claim visual inspection from compilation alone.

## Delivery

Provide editable source, audience PDF, original-figure provenance manifest, source audit, per-page notes, and previews as applicable. Keep delivery links and artifacts consistent with the final source; do not repackage every intermediate spacing test unless requested. Report the outcome, important tradeoffs or blockers, and current links briefly. When answering “what does page N mean?”, confirm physical PDF page versus displayed slide number; explain the actual figure before revising the deck unasked.
