---
name: ai-study-workflow
description: Build AI-assisted study workflows for university learning. Use when the user asks to improve study efficiency, prepare for finals or exams, review a course, learn new material, make a study plan, generate practice questions, diagnose weak points, create Anki/FSRS flashcards, or run AI tutoring without replacing student thinking. Triggers include 期末复习, 备考, 学习效率, 新知识学习, AI 学习助手, 错题, Anki, 间隔复习, and 苏格拉底式辅导.
---

# AI Study Workflow

Use this skill to turn course material into a concrete study loop. Prefer fast, verifiable learning outcomes over broad educational advice.

## Mode Selection

Choose one mode first:

- **Review mode**: The user has already learned the material and wants exam performance, weak-point diagnosis, mock tests, or final-review planning. Read `references/review-mode.md`.
- **Learning mode**: The user is learning new material from scratch or building first-pass understanding. Read `references/learning-mode.md`.
- **Mixed mode**: If the user has both goals, start with review mode for imminent exams; otherwise start with learning mode and schedule review checkpoints.

Before choosing a mode for PDFs, slides, notes, or other source files, read `references/source-ingestion.md` and perform a quick source-quality pass. If the course's AI policy, exam date, or available materials are unclear, state assumptions and proceed with the safest minimal workflow. Do not upload or request restricted exams, private data, or forbidden assessment materials.

## Fast UX Entry

For a source-based first response, prefer a short "front door" instead of a full report:

1. Source card: file type, scope, usable text, visual/uncertain caveats.
2. Mode choice: learning, review, or material generation.
3. One immediate task: for review, a short diagnostic; for first-time learning, a tiny first learning block plus at most 1-2 low-stakes readiness questions.

Do not expand both learning mode and review mode unless the user asks for both. Keep review diagnostics answer-free; in first-time learning, do not make the student answer a long prerequisite quiz before teaching the first chunk.

## Operating Rules

1. Make the student answer first before AI gives a solution.
2. Use AI for explanation, questioning, practice generation, feedback, scheduling, and card formatting.
3. Do not use AI to replace closed-book practice, final answers, or institution policy.
4. Treat AI outputs as drafts until checked against course materials, rubrics, official solutions, or instructors.
5. Convert mistakes into short active-recall cards with source tags.
6. Mark uncertain, sparse, conflicting, or visually extracted source content as `needs human check` instead of presenting it as fact.
7. In interactive sessions, stop at diagnostic, near-transfer, and mock-test steps; ask the student to answer before revealing solutions.

## Standard Outputs

For a full workflow response or requested artifact, produce:

- the chosen mode and assumptions
- a compact plan for today
- a repeatable loop for the next study sessions
- the exact prompts or templates the student should use
- the verification signal that proves learning improved

Use templates from `assets/` when creating files for the user:

- `assets/fast-entry-template.md`
- `assets/course-dashboard.md`
- `assets/daily-review-log.md`
- `assets/knowledge-map.md`
- `assets/anki-card-template.csv`

Use `references/prompt-library.md` when the user asks for prompts or when a workflow step needs a concrete prompt.

Use `references/quality-rubric.md` when deciding whether a workflow is effective.

Use `references/source-ingestion.md` when the user provides PDFs, slides, lecture notes, screenshots, OCR text, or mixed course materials.

For PDF course material, use extraction plus quality inspection before generating study content. For ordinary text PDFs, prefer MarkItDown as the first-pass Markdown extractor when available:

```powershell
& "C:\Users\lenovo\.codex\tools\markitdown\Scripts\markitdown.exe" course.pdf > source-markitdown.md
```

Then run the PDF inspector to check page-level extraction quality:

```bash
python scripts/inspect_pdf_source.py course.pdf --markdown-out source-report.md --json-out source-report.json --text-out source-text.txt
```

Use `source-markitdown.md` for clean first-pass reading only when it is complete and readable. Reject or downgrade MarkItDown output when it has mojibake, many replacement characters (`�`), almost no expected CJK/text content, broken tables/formulas, or obvious scope loss. In those cases, prefer `source-report.md` / `source-text.txt` for page tags, quality flags, and topic mapping.

If the PDF contains formulas, charts, complex tables, scanned pages, or image-heavy content, use Docling as a fallback structured extractor. For large slide-export PDFs or image-heavy course decks, avoid running Docling over the whole file first; run it only on a copied ASCII-path file, a short page range/split PDF, or a small set of critical pages after the inspector identifies them:

```powershell
$env:no_proxy = "127.0.0.1,localhost,127.0.0.0/8"
$env:NO_PROXY = $env:no_proxy
& "C:\Users\lenovo\.codex\tools\docling\Scripts\docling.exe" course.pdf --to md --image-export-mode referenced --enrich-formula --enrich-picture-description --enrich-chart-extraction --output docling-output
```

If Docling fails, is slow, or reports memory/page-count errors, do not block the workflow. Fall back to inspector text plus rendered page images for the flagged pages.

Render pages that still need visual checks:

```bash
python scripts/render_pdf_pages.py course.pdf --from-report source-report.json --flag private_use_symbols --flag image_dependent --max-pages 10 --out-dir rendered-pages --manifest-out rendered-pages/manifest.json
```

Do not treat MarkItDown or Docling output as visually complete. Keep formulas, diagrams, charts, and ambiguous pages as `needs human check` until checked against rendered pages or the original source.

For PPTX course material, prefer the PPTX inspector before generating study content:

```bash
python scripts/inspect_pptx_source.py course.pptx --markdown-out source-report.md --json-out source-report.json --text-out source-text.txt
```

Then render slides that need visual checks:

```bash
python scripts/render_pptx_slides.py course.pptx --from-report source-report.json --flag image_heavy --flag graphic_content --max-slides 10 --out-dir rendered-slides --manifest-out rendered-slides/manifest.json
```

## Optional Anki CSV Script

When the user has card data in JSON or JSONL, use:

```bash
python scripts/make_anki_csv.py cards.json --out anki.csv
```

Input cards should include `front` and `back`; optional fields are `deck`, `tags`, `type`, and `source`.

## Minimal Examples

User: "用 AI 帮我 7 天复习概率论期末。"

Response path: review mode -> course triage -> closed-book diagnostic -> weak-point tutoring -> Anki cards -> timed mock schedule.

User: "我想从零学贝叶斯公式。"

Response path: learning mode -> compact concept skeleton -> first small learning block -> one quick check -> near variant -> transfer problem -> spaced review cards.
