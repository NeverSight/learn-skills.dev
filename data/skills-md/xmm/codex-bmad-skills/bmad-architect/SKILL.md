---
name: bmad-architect
description: Architecture skill for BMAD. Use for bmad:architecture and bmad:gate-check to produce system design and verify requirement coverage.
---

# BMAD Architect

## Trigger Intents

- `bmad:architecture`
- `bmad:gate-check`

## Workflow Variants

1. `architecture`
- Produce architecture decisions, components, interfaces, and data model.

2. `gate-check`
- Validate architecture quality and requirement coverage before implementation.

Mode selection:
- Run `architecture` when `docs/bmad/architecture.md` does not exist or requirements changed materially.
- Run `gate-check` when architecture exists and the team needs a formal implementation-readiness decision.

## Inputs

- planning artifact (`docs/bmad/prd.md` or `docs/bmad/tech-spec.md`)
- architecture artifact (`docs/bmad/architecture.md`) for gate-check mode
- `bmad/project.yaml` level and constraints
- known integration, compliance, and scalability constraints

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

Before executing `architecture` or `gate-check`, read `REFERENCE.md` first.
Treat `REFERENCE.md` as required context, then load relevant resources and templates.

## Output Contract

- `architecture` -> `docs/bmad/architecture.md`
- `gate-check` -> `docs/bmad/gate-check.md`

## Core Workflow

1. Define system boundaries and architecture drivers.
2. Select architecture pattern and justify trade-offs.
3. Design components, APIs, and data model.
4. Map NFRs to concrete controls and design choices.
5. Run gate-check using criteria from `resources/gate-check-criteria.md` and report pass/fail gaps.

## Gate-Check Criteria

Load and apply `resources/gate-check-criteria.md` as the single source of truth for:
- coverage metric formulas
- blocker classification rules
- `PASS` / `CONDITIONAL PASS` / `FAIL` thresholds

## Gate-Check Artifact Format

Always save `docs/bmad/gate-check.md` using `templates/gate-check.template.md`.

Required sections:
- Executive Summary with decision (`PASS`, `CONDITIONAL PASS`, or `FAIL`)
- Requirements Coverage (FR and NFR totals, coverage percentages, missing items)
- Architecture Quality Assessment (checklist score and failed checks)
- Issues (Blockers, Major Concerns, Minor Issues)
- Recommendations
- Gate Decision (threshold comparison and rationale)
- Next Steps
- Appendix with detailed FR/NFR mapping evidence

## Script Selection

- `architecture` mode:
  ```bash
  bash scripts/nfr-checklist.sh
  bash scripts/validate-architecture.sh docs/bmad/architecture.md
  ```
- `gate-check` mode:
  ```bash
  bash scripts/validate-architecture.sh docs/bmad/architecture.md
  bash scripts/nfr-checklist.sh
  ```

## Template Map

- `templates/architecture.template.md`
- Why: full architecture structure with design decisions and NFR mapping.

- `templates/gate-check.template.md`
- Why: deterministic gate-check report format with objective pass criteria.

## Reference Map

- `REFERENCE.md`
- Must read first for architecture workflow details and design decision quality criteria.

- `resources/architecture-patterns.md`
- Use when selecting monolith, modular monolith, microservices, or other patterns.

- `resources/nfr-mapping.md`
- Use to map performance, security, scalability, and reliability requirements.

- `resources/gate-check-criteria.md`
- Use as mandatory criteria source for gate-check scoring and decision thresholds.

## Quality Gates

- architecture decisions trace back to requirements
- interfaces and data model are explicit
- NFR coverage is documented, not implied
- critical risks and mitigations are listed
- implementation can proceed without unresolved blockers
