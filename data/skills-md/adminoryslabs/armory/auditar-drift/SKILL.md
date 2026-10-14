---
name: auditar-drift
description: Detecta discrepancias entre lo prometido (PRD.md y ADRs) y lo que el código realmente implementa — features fantasma, reglas de negocio omitidas, decisiones de arquitectura no respetadas, deuda técnica. Produce un reporte DRIFT.md con hallazgos evidenciados y, para cada uno, si corresponde corregir el código o actualizar la documentación de forma justificada. Use when the user asks to audit drift, check whether the implementation still matches the PRD/ADRs, or find gaps between documentation and actual code.
---

# Drift Auditor

## Goal

Documentation drifts from code the moment nobody enforces the link between them. This skill closes
that gap: it reads what the project **promised** (`PRD.md`, ADRs) and what it **actually does**
(the real codebase), and reports every place the two disagree — not to blame anyone, but so the
team can decide, item by item, whether the code needs to change or the documentation does.

This skill never edits code or documentation. It reports; the human decides.

## Required Input

- `PRD.md` — required. Without it there's no "promised" side to compare against.
- `adrs/*.md` (or equivalent ADR set) — required if the project has architecture decisions
  recorded. If the project genuinely has none, say so explicitly and skip the architecture-drift
  checks rather than inventing decisions to check against.
- `TECH-DESIGN.md`, if present — useful for component boundaries and data model, not required.
- The actual source code of the project — required, obviously; this is the other half of the
  comparison.

If `PRD.md` is missing, stop and ask for it before proceeding — auditing drift against nothing
produces a report about the code alone, which is a different skill.

## Workflow

### 1. Build the promised model

Read `PRD.md` and every ADR in full. Extract, as concrete, checkable claims:

- Every item in "Alcance" (must exist) and "No alcance" (must **not** exist as a shipped feature).
- Every explicit business rule, edge case, or constraint in the PRD's own text — not just section
  headers.
- Each ADR's `Decisión` — the architecture choice that was actually made — and anything in its
  `Consecuencias` that implies an ongoing constraint (e.g., "toda escritura pasa por la cola" is a
  standing rule, not a one-time fact).

Do not infer promises the documents don't actually make. A feature the model *assumes* would be
nice is not a promise — only what the PRD/ADRs actually state counts as "promised."

### 2. Build the actual model

Explore the real codebase to determine what it actually does. Use whatever code-intelligence
tooling the environment already provides for structural exploration (a code graph, an IDE index,
etc.) before falling back to broad grep/glob — the goal is an accurate map of components, flows,
and rules, not an exhaustive read of every file. For each item extracted in step 1, find the
concrete evidence (file + line, or its clear absence) that confirms or contradicts it.

### 3. Classify each comparison point

For every promise checked against reality, classify it as one of:

- **OK** — matches. Do not report these individually; only count them in the summary.
- **Feature fantasma** — promised in the PRD (in "Alcance") but not implemented, or implemented in
  a materially different way than described.
- **Regla omitida** — a business rule, edge case, or constraint the PRD states, with no
  corresponding handling in the code.
- **Decisión de arquitectura violada** — the code contradicts an ADR's `Decisión` (e.g., the ADR
  says all writes go through a queue, and a code path writes directly).
- **Feature no documentada** — exists and works in the code, but isn't in the PRD or covered by any
  ADR. This is drift too, just in the other direction — the code moved and the docs didn't follow.
- **Deuda técnica ligada a una promesa** — a promised feature or an ADR-backed decision is
  implemented via an explicit workaround, `TODO`/`FIXME`, or a hack that risks breaking the
  guarantee later. Report separately from the two categories above; it's not a broken promise yet,
  but a fragile one.

Every finding needs concrete evidence — a PRD/ADR quote plus a file:line (or explicit absence). "El
código podría no estar cubriendo esto" without a specific check is not a finding.

### 4. Triage — do not resolve the drift yourself

For each drift finding, state both options honestly and let the human choose:

- **CORREGIR CÓDIGO** — the documented promise/decision is still the intent; the code should be
  brought in line with it.
- **ACTUALIZAR PRD/ADR** — the code's current behavior is the actual, justified intent now (a
  deliberate pivot, a constraint that changed); the documentation is what's stale.

This skill has no authority to decide which one is correct — that's a product/architecture call.
Never edit `PRD.md` or any ADR to "fix" a drift found here, even one that looks obviously stale.

### 5. Write the report

Write `DRIFT.md` at the project root, following the structure in
`assets/drift-report-template.md`.

## Output

`DRIFT.md` — nothing else in the project changes. This is a report-only pass.

## Quality Gate

Before returning, silently check:

- Every finding cites a specific PRD/ADR statement and a specific piece of code (or its clear
  absence) — nothing inferred without evidence on both sides.
- "Feature no documentada" findings were actively looked for, not just the promise → code
  direction — reverse drift is easy to skip and just as real.
- Every finding got both triage options stated (`CORREGIR CÓDIGO` / `ACTUALIZAR PRD/ADR`) — none
  were silently resolved by this skill.
- No PRD or ADR file was modified during the audit.
- If `PRD.md` had no ADRs to check against, the report says so explicitly instead of silently
  skipping the architecture section.

## References

- `assets/drift-report-template.md` — the exact structure `DRIFT.md` must follow.
