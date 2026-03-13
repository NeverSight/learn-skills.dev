---
name: transcript-pipeline
description: This skill should be used when the user asks to "process this transcript", "convert lecture to notes", "run transcript pipeline", "generate class tutorial from Zoom captions", "validate transcript coverage", or "enrich class resources" (Notion/Canva/Drive links) for bootcamp notes.
version: 0.2.0
---

# Transcript Pipeline Skill

Run a deterministic, auditable transcript-to-tutorial workflow with optional resource enrichment.

## Purpose

Use this skill to convert raw class captions into high-quality study notes while preserving accountability through ledger + validation artifacts.

Use scripts for deterministic work. Use chat/stage prompts for language-heavy transformation.

## Core Contract

1. Keep stage order: ingest -> refine -> synthesize -> enhance -> validate -> publish.
2. Run deterministic gates with scripts, never with LLM self-certification.
3. Preserve traceability in `.pipeline/*` artifacts.
4. Keep learner-facing notes readable and sanitized.
5. Treat validation status as PASS/FAIL source of truth.

## Scripts

Use these scripts from `scripts/`:

- `ingest_zoom_captions.py` - deterministic ingestion and segment ledger creation
- `run_chat_pipeline.py` - guided orchestration for stage handoffs and validation
- `validate_coverage.py` - hard-gate coverage validation
- `publish_tutorial_notes.py` - learner-facing file naming and sanitization
- `merge_chunks.py` - merge chunk outputs for large transcripts
- `run_colab_notebook_pipeline.py` - AI/ML Colab appendix and code explainer pipeline
- `update_ai_notes_with_resources_and_colab.py` - AI/ML notes enrichment utility
- `resource_enrichment.py` - authenticated enrichment for Notion/Canva/Drive resources

## Stage Workflow

### Stage 0: Ingest (Deterministic)

Run:

```bash
python scripts/ingest_zoom_captions.py "<transcript_or_session_path>"
```

Required outputs:

- `.pipeline/segment_ledger.jsonl`
- `.pipeline/segment_manifest.jsonl`

### Stage 1: Refine (Chat Stage)

Load `references/stage1-refine.md`.

Produce:

- `.pipeline/refined_transcript.md`
- `.pipeline/topic_inventory.json`
- `.pipeline/corrections_log.csv`
- `.pipeline/uncertainty_report.json`

### Stage 2: Synthesize (Chat Stage)

Load `references/stage2-synthesize.md`.

Produce:

- `.pipeline/structured_notes.md`
- `.pipeline/coverage_matrix.json`

### Stage 3: Enhance (Chat Stage)

Load:

- `references/stage3-enhance.md`
- `references/tutorial-tech-bar-raiser.md`

Produce:

- `.pipeline/enhanced_notes.md`
- `final_notes.md`
- `bootcamp_index.md`

### Stage 4: Validate (Deterministic)

Run:

```bash
python scripts/validate_coverage.py --pipeline-dir .pipeline
```

Validation guidance: `references/stage4-validate.md`.

Hard gates:

1. Segment coverage accountability
2. Uncertainty retention
3. No orphan claims

### Stage 5: Publish

Run:

```bash
python scripts/publish_tutorial_notes.py --root "<sessions_root>" --session-dir "<session_dir>"
```

Result:

- Published tutorial filename in canonical format
- Learner-safe note without noisy source tags
- Updated course index links

## One-Command Guided Mode

Use guided runner for chat-window workflows:

```bash
python scripts/run_chat_pipeline.py run "<transcript_or_session_path>" --deep-pass
```

This enforces required handoffs and deep quality gates.

## Optional Resource Enrichment Stage

Run when class notes include external links (Notion/Canva/Drive):

```bash
python scripts/resource_enrichment.py --all-sessions
```

Single session:

```bash
python scripts/resource_enrichment.py --session-dir "<session_dir>"
```

Auth options:

- Notion: `NOTION_TOKEN_V2`, `NOTION_ACTIVE_USER`
- Canva: `RESOURCE_PLAYWRIGHT_STORAGE_STATE`

Reference: `references/resource-enrichment-authenticated-flow.md`.

## Optional AI/ML Colab Enrichment

Run for Colab-backed AI/ML classes:

```bash
python scripts/run_colab_notebook_pipeline.py
```

Reference: `references/colab-notebook-explainer-pipeline.md`.

## Large Transcript Handling

If input exceeds context comfort:

1. Run Stage 1 by chunks.
2. Merge chunk artifacts:

```bash
python scripts/merge_chunks.py --chunk-dirs "<chunkA/.pipeline>" "<chunkB/.pipeline>" --output-dir "<session/.pipeline>"
```

3. Continue Stage 2 onward on merged artifacts.

## Required Outputs Checklist

Learner-facing:

- `final_notes.md`
- `<Domain> Class <NN> [DD-MM-YYYY] - <Topic>.md`
- `bootcamp_index.md`

Pipeline/audit:

- `.pipeline/segment_ledger.jsonl`
- `.pipeline/segment_manifest.jsonl`
- `.pipeline/refined_transcript.md`
- `.pipeline/topic_inventory.json`
- `.pipeline/corrections_log.csv`
- `.pipeline/uncertainty_report.json`
- `.pipeline/structured_notes.md`
- `.pipeline/coverage_matrix.json`
- `.pipeline/enhanced_notes.md`
- `.pipeline/validation_report.md`
- `.pipeline/exceptions.json` (if fail)

Quality gates:

- `.pipeline/deep_pass_report.md` (when `--deep-pass`)
- `.pipeline/deep_pass_exceptions.json` (when `--deep-pass`)

Resource enrichment (optional):

- `.resources/resource_enrichment_report.json`

## Execution Rules

- Fail fast on missing required artifacts.
- Report missing outputs explicitly by file path.
- Retry only from earliest failing stage.
- Keep resource extraction status explicit (success/fallback/blocked).
