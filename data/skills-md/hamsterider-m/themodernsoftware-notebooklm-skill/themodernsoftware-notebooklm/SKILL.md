---
name: themodernsoftware-notebooklm
description: Use when the user wants Codex to crawl weekly resources from https://themodernsoftware.dev/ and generate NotebookLM-based study outputs (bilingual lesson plan, lecture notes, and video overview), especially when the course has syllabus and slides but no public lecture videos.
---

# TheModernSoftware NotebookLM

## Overview

Run an agent-first workflow where Codex is the controller. Crawl weekly course materials from `themodernsoftware.dev`, ingest them into NotebookLM, and produce deep-study outputs without requiring a custom standalone agent service.

The workflow is deterministic through state files and templates:
- Use `templates/course.yaml`, `templates/weeks.json`, and `templates/week-notebooks.json` as the single source of run state.
- Use `agent-browser` for page crawling and link extraction.
- Use `notebooklm` for source ingestion and output generation.

Core principle (read first): `references/principles.md`

## Workflow

### Step 0: Initialize runtime workspace

Create a runtime folder and copy templates:

```bash
./themodernsoftware-notebooklm/scripts/init-workspace.sh ./runtime
```

This creates:
- `./runtime/course.yaml`
- `./runtime/weeks.json`
- `./runtime/week-notebooks.json`
- `./runtime/prompts/*.prompt.md`

### Step 1: Preflight checks

Verify required tools before crawling:

```bash
agent-browser --help
notebooklm status --json
```

If `notebooklm status --json` fails, run `notebooklm login`.

### Step 2: Crawl weekly materials (Curriculum-native)

Extract week-scoped sources from the authoritative course page:

```bash
./themodernsoftware-notebooklm/scripts/crawl-extract.sh "https://themodernsoftware.dev/" ./runtime/weeks-extracted.json
./themodernsoftware-notebooklm/scripts/merge-weeks.py ./runtime/weeks-extracted.json ./runtime/weeks.json ./runtime/weeks-diff.json
./themodernsoftware-notebooklm/scripts/verify-week-state.sh ./runtime/weeks.json ./runtime/week-notebooks.json
```

Notes:
- Crawl rules: `references/crawl-rules.md`
- Merge is incremental: it preserves prior ingest evidence per URL, reclassifies new inputs, and emits a week-level diff (`weeks-diff.json`).
- Non-course assets with `provenance=manual|external-search` are preserved across merges.

### Step 3: Ingest into NotebookLM (Week-scoped + evidence-gated)

Default behavior is **one notebook per week** (prevents cross-week context pollution).

```bash
./themodernsoftware-notebooklm/scripts/notebooklm-per-week.py ./runtime --diff ./runtime/weeks-diff.json
./themodernsoftware-notebooklm/scripts/verify-week-state.sh ./runtime/weeks.json ./runtime/week-notebooks.json
```

What this does:
- Creates/uses a per-week notebook and stores mapping in `week-notebooks.json`.
- Prefers direct URL ingest (web / YouTube).
- Waits until each source is `ready` (evidence gate) and confirms `source_id` appears in `source list`.
- Retries failures with backoff (`course.yaml.retry.*`).
- If direct ingest fails and `download_url` is available, falls back to download+verify (`scripts/verify-file.sh`) then upload as `--type file`.
- Records `ingest_status`, `source_id`, `ingest_attempts`, and `last_error` per asset.

To retry a specific week:
```bash
./themodernsoftware-notebooklm/scripts/notebooklm-per-week.py ./runtime --weeks week-01
```

### Step 4: Generate deep outputs

For each `status: ingested` week:

```bash
./themodernsoftware-notebooklm/scripts/generate-week.py ./runtime --diff ./runtime/weeks-diff.json
./themodernsoftware-notebooklm/scripts/verify-week-state.sh ./runtime/weeks.json ./runtime/week-notebooks.json
```

Outputs are written under `./runtime/outputs/<week_id>/` and paths are recorded back into `weeks.json`:
- `lesson-plan.zh-en.md`
- `lecture-notes.zh-en.md`
- `video-script.zh-en.md` (default)

Optional: generate and download NotebookLM video artifact by setting `course.yaml.outputs.video.mode: artifact|both`.

### Step 5: Failure policy

Apply strict policy from `references/failure-handling.md`:
- If `themodernsoftware.dev` is unreachable: fail the current run immediately.
- No automatic fallback source.
- Keep failure reason in `weeks.json.error` and per-asset `last_error` for the affected week/run.

## Output Contract

Each completed week must include:
- `lesson_plan_path`
- `lecture_notes_path`
- `video_script_path` (when `outputs.video.mode` includes `script`)
- `video_artifact_id` / `video_local_path` (when `outputs.video.mode` includes `artifact`)

Do not mark `completed` if artifact-mode video download is unfinished.

## Resources

- `references/crawl-rules.md`: URL discovery and week classification rules.
- `references/notebooklm-deep-mode.md`: source ingestion, output generation, language and quality requirements.
- `references/failure-handling.md`: stop/retry/error recording policy.
- `references/execution-checklist.md`: runbook checklist.
- `references/principles.md`: abstract operating principle (week-scoped + evidence gated + incremental).
- `templates/course.yaml`: runtime config template.
- `templates/weeks.json`: runtime state template.
- `templates/weeks.schema.json`: structure contract for state validation.
- `templates/week-notebooks.json`: week_id -> notebook_id mapping template.
- `templates/prompts/*.prompt.md`: prompt templates.
- `scripts/init-workspace.sh`: initialize runtime workspace.
- `scripts/crawl-extract.sh`: extract week items via agent-browser.
- `scripts/merge-weeks.py`: merge extracted data into runtime state and emit diffs.
- `scripts/verify-week-state.sh`: validate `weeks.json` structure.
- `scripts/verify-file.sh`: verify downloaded file is a real document (not HTML/login/error).
- `scripts/notebooklm-per-week.py`: ingest per-week sources with retry + evidence gate.
- `scripts/generate-week.py`: generate per-week learning outputs.

## Common mistakes

- Running generation before source processing finishes.
- Marking week as completed before artifact-mode video download succeeds.
- Losing state by not persisting `source_id`s and per-week notebook mapping.
- Mixing unrelated links into week assets.
