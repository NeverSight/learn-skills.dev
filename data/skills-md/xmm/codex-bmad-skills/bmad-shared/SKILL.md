---
name: bmad-shared
description: Shared state and template helper skill for BMAD. Provides reusable YAML contracts and deterministic scripts used by orchestrator and phase skills.
---

# BMAD Shared

## Purpose

Provide shared workflow state contracts and helper scripts for all BMAD skills.

## Language Guard (Mandatory)

Enforce language selection separately for chat responses and generated artifacts.

Chat language (`communication_language`) fallback order:

1. `language.communication_language` from `bmad/project.yaml`
2. `English`

Rules for chat responses:

- Use the resolved chat language for all assistant responses (questions, status updates, summaries, and handoff notes).
- Do not switch chat language unless the user explicitly requests a different language in the current thread.

Artifact language (`document_output_language`) fallback order:

1. `language.document_output_language` from `bmad/project.yaml`
2. `English`

Rules for generated artifacts:

- Use the resolved artifact language for all generated BMAD documents and structured artifacts.
- write prose and field values in the resolved document language
- avoid mixed-language requirement clauses with English modal verbs (for example, `System shall` followed by non-English text)
- allow English acronyms/abbreviations in non-English sentences (for example, `API`, `SLA`, `KPI`, `OAuth`, `WCAG`)
- Keep code snippets, CLI commands, file paths, and identifiers in their original technical form.

## Mandatory Reference Load

Before executing shared helper workflows, read `REFERENCE.md` first.
Treat `REFERENCE.md` as required context for state semantics and update rules.

## Workflow Variants

1. `config-read`
- Read project or global configuration safely.

2. `status-update`
- Update workflow state after completion.

3. `next-recommendation`
- Compute next intent from workflow state.

## YAML Contract Files

- `workflows.registry.yaml`
- `REFERENCE.md`
- Shared script semantics and state rules.

- `helpers.md`
- Shared implementation conventions and migration notes.

## Script Selection

Current scripts:

- Read project config:
  ```bash
  bash scripts/load-project-config.sh bmad/project.yaml
  ```
- Read global config:
  ```bash
  bash scripts/load-global-config.sh
  ```
- Update workflow state:
  ```bash
  bash scripts/update-workflow-status.sh --workflow product_brief --status-file bmad/workflow-status.yaml
  ```
- Recommend next workflow:
  ```bash
  bash scripts/next-workflow.sh bmad/workflow-status.yaml
  ```

Compatibility wrappers:

- `scripts/load-config.sh` -> wrapper to `load-project-config.sh`
- `scripts/update-status.sh` -> wrapper to `update-workflow-status.sh`
- `scripts/check-phase.sh` -> wrapper to `next-workflow.sh`

## Usage Rules

- prefer `yq` v4+ for all YAML reads and writes
- keep updates deterministic and idempotent where possible
- avoid ad-hoc parsing for nested YAML values

## Quality Gates

- YAML contract files remain backward-compatible within this branch
- scripts return explicit errors for missing files or tools
- state transitions update metrics and phase status consistently
