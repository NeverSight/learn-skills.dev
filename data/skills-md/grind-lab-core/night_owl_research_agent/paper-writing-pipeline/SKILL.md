---
name: paper-writing-pipeline
description: "Full paper writing pipeline. Orchestrates paper-plan → paper-figure-generate → paper-draft → paper-review-loop → paper-covert to go from upstream research artifacts to a polished, submission-ready manuscript package (Markdown → LaTeX → PDF + DOCX). Use when user says \"write paper pipeline\", \"paper writing\", or wants the complete paper generation workflow."
argument-hint: [narrative-report-path-or-topic]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply
---

# Paper Writing Pipeline

Orchestrate a complete paper writing workflow for: **$ARGUMENTS**

## Overview

This skill chains five sub-skills into a single automated pipeline:

```
/paper-plan → /paper-figure-generate → /paper-draft → /paper-review-loop → /paper-covert
  (outline)       (figures & prompts)     (Markdown)     (review & revise)    (LaTeX + PDF + DOCX)
```

Each phase builds on the previous one's output. The pipeline takes upstream research artifacts and produces a polished, reviewed submission package in `output/submission/`.

### Artifact Flow

```
Upstream artifacts (RESEARCH_PLAN, LIT_REVIEW, IDEA_REPORT, FINAL_PROPOSAL,
                    EXPERIMENT_PLAN, EXPERIMENT_RESULT, NARRATIVE_REPORT)
    ↓ Phase 1: paper-plan
output/PAPER_PLAN.md  (§0–§26: outline, claims matrix, figure plan, citations)
    ↓ Phase 2: paper-figure-generate
output/figures/       (PNGs, PDFs, scripts, prompts, FIGURE_MANIFEST.md, FIGURE_CAPTIONS.md)
    ↓ Phase 3: paper-draft
output/manuscript/    (MANUSCRIPT_DRAFT.md, sections/*.md, CLAIM_SUPPORT_MAP.md, COVERAGE_GAPS.md)
    ↓ Phase 4: paper-review-loop
output/manuscript/    (MANUSCRIPT_REVISED.md, sections_revised/*.md, REVIEW_REPORT.md, CLAIM_RISK_REPORT.md)
    ↓ Phase 5: paper-covert
output/submission/    (latex/, pdf/MANUSCRIPT_SUBMISSION_READY.pdf, docx/, SUBMISSION_MANIFEST.md)
```

---

## Constants

- **TARGET_VENUE = `IJGIS`** — Target venue. Supported: `TGIS`, `RSE`, `ISPRS_JPRS`, `AAG_ANNALS`, `IEEE_TGRS`, `ICLR`, `NeurIPS`, `ICML`, `CVPR`, `ACL`, `AAAI`, `ACM`, `IEEE_JOURNAL` (IEEE Transactions / Letters), `IEEE_CONF` (IEEE conferences). Affects template selection, page limit, citation format, and section structure.
- **MAX_REVIEW_ROUNDS = 2** — Number of review→revise rounds in the review loop (Phase 4).
- **REVIEWER_MODEL = `gpt-5.4`** — Model used via Codex MCP for plan review, figure review, draft review, and review loop.
- **AUTO_PROCEED = true** — Auto-continue between phases. Set `false` to pause and wait for user approval after each phase.
- **HUMAN_CHECKPOINT = false** — When `true`, the review loop (Phase 4) pauses after each round's review to let you see the score and provide custom modification instructions. When `false` (default), the loop runs fully autonomously. Passed through to `paper-review-loop`.
- **DRAFT_MODE** — One of `full`, `partial`, `skeleton`. Determined automatically by `paper-draft` based on evidence readiness. Can be forced via argument.

> Override inline: `/paper-writing-pipeline "NARRATIVE_REPORT.md" — venue: NeurIPS, human checkpoint: true`
> IEEE example: `/paper-writing-pipeline "NARRATIVE_REPORT.md" — venue: IEEE_JOURNAL`

---

## Inputs

This pipeline accepts one of:

1. **`output/NARRATIVE_REPORT.md`** (best) — structured research narrative with claims, experiments, results, figure plans, verified citations. Produced by `generate-report`.
2. **Upstream research artifacts** — the pipeline's `paper-plan` phase will read all available artifacts (`RESEARCH_PLAN.md`, `output/LIT_REVIEW_REPORT.md`, `output/IDEA_REPORT.md`, `output/refine-logs/FINAL_PROPOSAL.md`, `output/EXPERIMENT_PLAN.md`, `output/EXPERIMENT_RESULT.md`, `output/NARRATIVE_REPORT.md`) and build the plan from whatever exists.
3. **Existing `output/PAPER_PLAN.md`** — skip Phase 1, start from Phase 2.
4. **Existing `output/manuscript/MANUSCRIPT_DRAFT.md`** — skip Phases 1–3, start from Phase 4 (review loop).
5. **Existing `output/manuscript/MANUSCRIPT_REVISED.md`** — skip Phases 1–4, start from Phase 5 (conversion).

The more detailed the input (especially figure descriptions, quantitative results, and verified claims in `memory/APPROVED_CLAIMS.md`), the better the output.

### Skip Logic

Before starting, check which artifacts already exist to determine the entry point:

| Artifact exists | Skip to | Condition |
|---|---|---|
| `output/submission/MANUSCRIPT_SUBMISSION_READY.pdf` | Done | Ask user if they want to rebuild |
| `output/manuscript/MANUSCRIPT_REVISED.md` | Phase 5 | Unless user requests re-review |
| `output/manuscript/MANUSCRIPT_DRAFT.md` | Phase 4 | Unless user requests re-draft |
| `output/figures/FIGURE_MANIFEST.md` | Phase 3 | Unless user requests re-generation |
| `output/PAPER_PLAN.md` | Phase 2 | Unless user requests re-planning |
| None of the above | Phase 1 | Full pipeline |

When resuming, always read `handoff.json` first — it records the last completed phase and any pending issues.

---

## Pipeline

### Phase 1: Paper Plan

Invoke `paper-plan` to create the structural outline:

```
Skill: paper-plan "$ARGUMENTS"
```

**What this does:**
- Reads all available upstream artifacts (RESEARCH_PLAN, LIT_REVIEW_REPORT, IDEA_REPORT, FINAL_PROPOSAL, EXPERIMENT_PLAN, EXPERIMENT_RESULT, NARRATIVE_REPORT) — each is optional
- Determines venue and paper type from arguments, RESEARCH_PLAN, or defaults
- Loads venue-specific template from `templates/`
- Builds the full §0–§26 plan per `templates/PAPER_PLAN_TEMPLATE.md`:
  - One-paragraph summary and one-sentence claim
  - Target journal strategy and audience
  - Research gap and contributions (with "not claiming" boundary)
  - Research questions and hypotheses
  - Data and methodological plan
  - Experiment inventory and results summary
  - **Claims-Evidence Matrix** (§12) — the backbone mapping every claim to evidence
  - **Figure & Table Plan** (§13–§14) — with hero figure detail
  - Related work synthesis in themed clusters
  - Discussion, limitations, and future work plan
  - Abstract blueprint and title options
  - Writing instructions for the downstream draft agent
  - Readiness assessment and executive summary
- Scaffolds citation structure from verified sources
- REVIEWER_MODEL reviews the plan for completeness (8 scoring dimensions)
- Runs self-check (10 verification items) before finalizing

**Output:** `output/PAPER_PLAN.md` with the full §0–§26 structure.

**Checkpoint:** Present the plan summary to the user.

```
Paper plan complete:
- Title: [proposed title]
- Venue: [VENUE] | Page limit: [MAX_PAGES]
- Sections: [N] ([list])
- Contributions: [N]
- Claims in evidence matrix: [M] (supported: X, pending: Y)
- Figures planned: [total] (hero: 1, auto: X, manual: Y)
- Missing inputs: [list or "none"]
- Readiness: [full / partial / skeleton]

Shall I proceed with figure generation?
```

- **User approves** (or AUTO_PROCEED=true) → proceed to Phase 2.
- **User requests changes** → adjust plan and re-present.

---

### Phase 2: Figure Generation

Invoke `paper-figure-generate` to produce publication-quality figures:

```
Skill: paper-figure-generate "all"
```

**What this does:**
- Reads the Figure Plan (§13) and Table Plan (§14) from `output/PAPER_PLAN.md`
- Classifies each figure into a **code** pathway (reproducible plots, maps, charts) or **prompt** pathway (architecture diagrams, workflow schematics, conceptual figures)
- For code figures: writes Python scripts to `output/figures/scripts/`, generates PNGs + PDFs at 300 DPI, applies venue-appropriate styling (colorblind-safe palette, print-legible fonts, proper map elements)
- For prompt figures: writes detailed structured prompts to `output/figures/prompts/` with element inventories, style constraints, and negative prompts — ready to paste into an external image model
- Creates specification stubs for figures whose data is missing
- Writes manuscript-ready captions to `output/figures/FIGURE_CAPTIONS.md`
- Maintains `output/figures/FIGURE_MANIFEST.md` with status tracking per figure
- Runs a consistency pass across all figures (numbering, palette, terminology)
- REVIEWER_MODEL optionally reviews figure quality and captions

**Output:** `output/figures/` directory with rendered figures, scripts, prompts, manifest, and captions.

> **Scope:** Code pathway auto-generates data-driven figures (plots, maps, comparison tables). Prompt pathway produces ready-to-paste prompts for architecture diagrams, workflow figures, and graphical abstracts. The user supplies rendered prompt-pathway images before proceeding.

**Checkpoint:** List generated vs. manual figures.

```
Figures complete:
- Code-generated: [list with status]
- Prompt-generated: [list — prompts ready, renders needed from user]
- Stubs (data missing): [list with blockers]
- Manifest: output/figures/FIGURE_MANIFEST.md
- Captions: output/figures/FIGURE_CAPTIONS.md

[If prompt figures need renders]: Please generate images from prompts in output/figures/prompts/ and place renders in output/figures/ before I proceed.
[If all code figures ready]: Shall I proceed with manuscript drafting?
```

- **User provides renders / approves** (or AUTO_PROCEED=true) → proceed to Phase 3.
- **User requests changes** → adjust figures and re-present.

---

### Phase 3: Manuscript Drafting

Invoke `paper-draft` to generate the Markdown manuscript:

```
Skill: paper-draft "all"
```

**What this does:**
- Reads `output/PAPER_PLAN.md` (§0–§26) as the manuscript intent
- Determines `DRAFT_MODE` (full / partial / skeleton) from plan §25 readiness assessment
- Consults evidence files: `memory/APPROVED_CLAIMS.md`, `output/LIT_REVIEW_REPORT.md`, `output/EXPERIMENT_RESULT.md`, `output/figures/FIGURE_MANIFEST.md`
- Selects section structure based on venue and paper type (5–8 sections, flexible)
- Drafts each section following venue-specific academic prose conventions:
  - Introduction with numbered contributions
  - Related work in themed clusters (not a paper list)
  - Methods with spatial/GIScience rigor
  - Results led by strongest approved claim
  - Discussion closing the loop to the gap
  - Limitations mirroring plan §17
- Produces companion artifacts:
  - `CLAIM_SUPPORT_MAP.md` — every claim traced to evidence
  - `COVERAGE_GAPS.md` — missing experiments, figures, citations
  - `CITATION_GAPS.md` — claims needing citations
  - `REVISION_NOTES.md` — items for next pass
- Runs consistency checks (terminology, figure references, contribution closure)
- REVIEWER_MODEL optionally reviews each section
- **Never fabricates** results, citations, or figures — uses `[PLACEHOLDER]` and `[CITE: topic]` markers

**Output:** `output/manuscript/` directory with `MANUSCRIPT_DRAFT.md`, `sections/*.md`, and companion artifacts.

**Checkpoint:** Report draft completion.

```
Manuscript draft complete:
- Mode: [full / partial / skeleton]
- Venue: [TARGET_VENUE]
- Sections: [N] written ([list])
- Word count: [total] (budget: [limit])
- Claims supported: [X] / [total] in evidence matrix
- Coverage gaps: [K] (see output/manuscript/COVERAGE_GAPS.md)
- Citation gaps: [J] (see output/manuscript/CITATION_GAPS.md)

Shall I proceed with the review loop?
```

- **User approves** (or AUTO_PROCEED=true) → proceed to Phase 4.
- **User requests changes** → revise specific sections.

---

### Phase 4: Review and Revision Loop

Invoke `paper-review-loop` to critically review and revise the manuscript:

```
Skill: paper-review-loop "all"
```

**What this does (up to MAX_REVIEW_ROUNDS rounds):**

Each round follows this sequence:

1. **Cold-read evaluation** — REVIEWER_MODEL (gpt-5.4 xhigh) reviews the manuscript as a demanding journal reviewer, scoring 8 dimensions:
   - Gap clarity, novelty precision, methods rigor, results discipline
   - Discussion depth, literature positioning, journal fit, language flow
2. **Claim risk audit** — Cross-checks every claim against `CLAIM_SUPPORT_MAP.md` and `APPROVED_CLAIMS.md`; flags overclaims
3. **Issue classification** — Major (structural, argument, evidence) → Moderate (transitions, terminology) → Minor (polish)
4. **Human checkpoint** (if HUMAN_CHECKPOINT=true) — Present scores and top issues; wait for user guidance
5. **Revision** — Implements fixes ordered by severity (majors first); writes to `sections_revised/*.md` and `MANUSCRIPT_REVISED.md`
6. **Verification** — Checks claim closure, limitation closure, figure closure, contribution closure, terminology consistency

Key artifacts produced:
- `MANUSCRIPT_REVISED.md` — the revised manuscript (basis for next round or conversion)
- `REVIEW_REPORT.md` — structured reviewer report with per-dimension scores and verdict
- `MAJOR_ISSUES.md` / `MINOR_ISSUES.md` — ranked issue lists with resolution status
- `CLAIM_RISK_REPORT.md` — claim-wording-vs-evidence audit
- `JOURNAL_FIT_NOTES.md` — venue-specific alignment assessment
- `REVISION_LOG.md` — what changed and why, keyed to issue IDs
- `REVIEW_LOOP_STATE.json` — round counter, scores, unresolved issues (for resume)

**Generator-evaluator separation enforced:** REVIEWER_MODEL evaluates; Claude Code revises. The reviewer never sees the revision context; the reviser never self-scores. ThreadId persistence ensures reviewer continuity across rounds.

**Output:** Updated `output/manuscript/` with revised manuscript, review artifacts, and loop state.

**Checkpoint:** Report review results.

```
Review loop complete (Round [N]):
- Verdict: [ready / almost / not ready] for [TARGET_VENUE]
- Scores: gap=[X] novelty=[X] methods=[X] results=[X] discussion=[X] lit=[X] fit=[X] language=[X]
- Major issues: [resolved] / [total]
- Unresolved: [list of carry-over issues, if any]

Shall I proceed with LaTeX conversion and PDF generation?
```

- **User approves** (or AUTO_PROCEED=true) → proceed to Phase 5.
- **User requests additional rounds** → run another review-revise cycle.
- **User requests specific fixes** → apply targeted revisions.

---

### Phase 5: Conversion and Submission Package

Invoke `paper-covert` to convert the final manuscript into a submission package:

```
Skill: paper-covert "$VENUE"
```

**What this does:**
- Reads the best available manuscript: `MANUSCRIPT_REVISED.md` (preferred) → `MANUSCRIPT_DRAFT.md` (fallback)
- Resolves venue from argument → `PAPER_PLAN.md` → default; loads venue profile from `profiles/<venue>.yaml`
- Builds modular LaTeX tree in `output/submission/latex/`:
  - `main.tex` (lean entry with `\input` only)
  - `preamble.tex` (venue-specific packages and environments)
  - `metadata.tex` (title, keywords, highlights)
  - `sections/*.tex` (one per manuscript section, Markdown → LaTeX conversion)
  - `references.bib` (from existing .bib or synthesized from paper-cache; never fabricated)
  - `figures/` (copied from `output/figures/` per FIGURE_MANIFEST)
  - `build.sh` (latexmk → pdflatex fallback build script)
- Compiles PDF via `latexmk -pdf` with auto-fix for common errors
- Exports DOCX via Pandoc (LaTeX source preferred, Markdown fallback)
- Writes `SUBMISSION_MANIFEST.md` with:
  - Source manuscript path and readiness level
  - Files generated with paths
  - Bibliography gaps (unresolved citations)
  - Asset gaps (missing figures)
  - Content gaps (remaining `[PLACEHOLDER]` blocks)
  - Build status (PDF pass/fail, DOCX pass/fail)
  - Honest readiness assessment — never marks "submission-ready" with open gaps

**Output:** `output/submission/` with LaTeX source, PDF, DOCX, and manifest.

**Does NOT:**
- Rewrite or restructure prose (that was Phase 4)
- Invent citations or bibliographic entries
- Reference figures not in `FIGURE_MANIFEST.md`
- Modify `output/manuscript/` (read-only)

---

### Phase 6: Final Report

After all phases complete, present a summary report:

```markdown
# Paper Writing Pipeline Report

**Input**: [source artifacts used]
**Venue**: [TARGET_VENUE]
**Date**: [today]

## Pipeline Summary

| Phase | Status | Output |
|-------|--------|--------|
| 1. Paper Plan | [status] | output/PAPER_PLAN.md |
| 2. Figures | [status] | output/figures/ ([N] code + [M] prompt + [K] stubs) |
| 3. Manuscript Draft | [status] | output/manuscript/MANUSCRIPT_DRAFT.md ([mode], [words] words) |
| 4. Review Loop | [status] | output/manuscript/MANUSCRIPT_REVISED.md (Round [N], verdict: [X]) |
| 5. Conversion | [status] | output/submission/ (PDF: [ok/fail], DOCX: [ok/fail]) |

## Review Scores (Final Round)
| Dimension | Score |
|-----------|-------|
| Gap clarity | [X]/10 |
| Novelty precision | [X]/10 |
| Methods rigor | [X]/10 |
| Results discipline | [X]/10 |
| Discussion depth | [X]/10 |
| Literature positioning | [X]/10 |
| Journal fit | [X]/10 |
| Language flow | [X]/10 |

## Deliverables
- output/PAPER_PLAN.md — Manuscript plan (§0–§26)
- output/figures/ — Figures, scripts, prompts, manifest, captions
- output/manuscript/MANUSCRIPT_DRAFT.md — Initial Markdown draft
- output/manuscript/MANUSCRIPT_REVISED.md — Reviewed and revised draft
- output/manuscript/CLAIM_SUPPORT_MAP.md — Claim-to-evidence traceability
- output/manuscript/REVIEW_REPORT.md — Structured review report
- output/submission/latex/ — Modular LaTeX source
- output/submission/pdf/MANUSCRIPT_SUBMISSION_READY.pdf — Compiled PDF
- output/submission/docx/MANUSCRIPT_SUBMISSION_READY.docx — Word document
- output/submission/SUBMISSION_MANIFEST.md — Package manifest with readiness assessment

## Open Issues (if any)
- [unresolved major issues from MAJOR_ISSUES.md]
- [bibliography gaps from CITATION_GAPS.md]
- [asset gaps from SUBMISSION_MANIFEST.md]
- [content gaps — remaining [PLACEHOLDER] blocks]

## Next Steps
- [ ] Visual inspection of PDF
- [ ] Generate renders for prompt-pathway figures (if pending)
- [ ] Resolve any remaining [PLACEHOLDER] blocks
- [ ] Add author information
- [ ] Final venue compliance check (/submit-check)
- [ ] Submit to [venue]
```

---

## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.
- **Don't skip phases.** Each phase builds on the previous one — skipping leads to missing artifacts that downstream phases expect.
- **Checkpoint between phases** when AUTO_PROCEED=false. Present results and wait for approval.
- **Prompt-pathway figures require user renders.** If the paper needs architecture diagrams or conceptual figures produced via image models, the user must provide the rendered images before Phase 3. The pipeline generates the prompts; the user generates the images.
- **Evidence integrity throughout.** The pipeline never fabricates results, citations, or figures at any phase. Missing evidence produces marked placeholders, not inventions.
- **Generator-evaluator separation.** Maintained across the entire pipeline: `paper-draft` writes, `paper-review-loop` evaluates and revises, `paper-covert` converts. No skill self-scores its own output.
- **Preserve all intermediate artifacts.** The user needs the full trail: plan → figures → draft → reviewed → revised → submission package.
- **Document everything.** The final report should be self-contained. Each phase produces its own artifacts (manifests, gap reports, state files).
- **Respect page limits.** If the paper exceeds the venue limit, suggest specific cuts during Phase 4 (review loop) rather than silently truncating during Phase 5 (conversion).
- **Venue consistency.** TARGET_VENUE propagates through all 5 phases via `output/PAPER_PLAN.md`. Do not change venue mid-pipeline without re-running from Phase 1.

---

## Error Handling

| Error | Phase | Response |
|---|---|---|
| No upstream artifacts exist (no RESEARCH_PLAN, no NARRATIVE_REPORT, nothing) | 1 | Halt. Tell the user to run upstream skills first (`lit-review`, `generate-idea`, `experiment-design-pipeline`). |
| PAPER_PLAN.md readiness = skeleton | 2–3 | Continue in skeleton mode. Figures are stubs; draft has extensive placeholders. Report honestly. |
| Figure data missing for code-pathway figures | 2 | Produce specification stubs. Continue to Phase 3 with stubs noted. |
| REVIEWER_MODEL (Codex MCP) unavailable | 1, 3, 4 | Fall back to Claude subagent with fresh context for review. Log the degradation. |
| PDF compilation fails | 5 | Keep LaTeX source intact. Record error in SUBMISSION_MANIFEST.md. Attempt DOCX via Markdown fallback. Report failure. |
| Pandoc unavailable for DOCX | 5 | Record `docx: blocked` in manifest. PDF is the primary deliverable. |
| Context approaching limit mid-phase | Any | Write current state to phase-specific state file. Update `handoff.json`. Tell user to resume in a new session. |

---

## Composing with Other Workflows

```
/idea-discovery-pipeline "direction"     ← Workflow 1: find and refine ideas
/deploy-experiment                       ← Execute experiments
/auto-review-loop "research topic"       ← Adversarial review of research quality
/generate-report                         ← Consolidate into NARRATIVE_REPORT.md
/paper-writing-pipeline "NARRATIVE_REPORT.md"  ← You are here: manuscript to submission
                                              submit!
```

Or use `/full-pipeline` for the end-to-end flow (idea discovery → experiments → review → report), then `/paper-writing-pipeline` for the manuscript production.

### Sub-Skill Reference

| Phase | Skill | Input | Output | Docs |
|---|---|---|---|---|
| 1 | `paper-plan` | Upstream artifacts | `output/PAPER_PLAN.md` | `skills/paper-plan/SKILL.md` |
| 2 | `paper-figure-generate` | `output/PAPER_PLAN.md` | `output/figures/` | `skills/paper-figure-generate/SKILL.md` |
| 3 | `paper-draft` | `output/PAPER_PLAN.md` + figures | `output/manuscript/` | `skills/paper-draft/SKILL.md` |
| 4 | `paper-review-loop` | `output/manuscript/` | `output/manuscript/` (revised) | `skills/paper-review-loop/SKILL.md` |
| 5 | `paper-covert` | `output/manuscript/` (revised) | `output/submission/` | `skills/paper-covert/SKILL.md` |
