---
name: inspect-role-naming
description: "Audit codebase identifiers and architectural role suffixes for load-bearing responsibility mismatches and boundary collisions."
disable-model-invocation: true
---

# inspect-role-naming — Architectural Role & Nomenclature Auditor

## Domain Rubric

### 1. Scope & Tolerability Guardrails (What to Ignore)

- **Confine to Load-Bearing Risks**: Focus exclusively on dangerous architectural misrepresentations, runtime collisions, or boundary schema leaks.
- **Tolerate Benign Code**: Tolerate minor local helpers (< 3 methods), internal variable brevity, benign metrics/logging in accessors, and cosmetic style differences; never force refactoring on working, cohesive code.
- **Governing Reference**: Evaluate naming and role alignment strictly against `references/role-naming-rubric.md` (or the host repository's authoritative naming specifications, which always take precedence).

### 2. Decision Bifurcation: [RENAME] vs. [REFACTOR]

- `[RENAME]` (Pure Nomenclature Drift): The underlying responsibility is singular and sound; only the identifier/suffix drifted from `references/role-naming-rubric.md`. Fix is localized and low-risk.
- `[REFACTOR]` (Role Dishonesty / Responsibility Leak): The symbol name conceals multiple disparate responsibilities or makes false promises (e.g., repository calling external APIs). Structural extraction must occur before renaming.

## Canonical Output Contract

```markdown
# Role & Naming Audit Dossier: <Target Scope>

## 1. Executive Summary
- **Target Inspected**: `<directory_or_file_path>`
- **Health Rating**: <PRISTINE | LOCALIZED_DRIFT | SYSTEMIC_DEBT>
- **Primary Bottleneck**: <Single-sentence summary of greatest role or boundary hazard>

## 2. Load-Bearing Defect Catalog
### [<CRITICAL | MAJOR>] [<RENAME | REFACTOR>] <Dimension>: `<Target Symbol>`
- **Offending Code**: [<file>#L<N>](file:///path/to/file#L<N>)
- **Violated Rubric**: [<spec_or_rubric>](references/role-naming-rubric.md#anchor)
- **Smell**: <Observable contract mismatch or dangerous collision>
- **Action**: <[RENAME] New Identifier OR [REFACTOR] Minimal Separation Path>

*(Emit 'No load-bearing role or naming defects observed' if clean)*
```

### Routing

- Localized symbol renames or minor boolean cleanup within a single file → (via /simplify-audit).
- Multi-file symbol migrations or structural role extractions → (via /changeset).

## Execution Protocol

1. **Intake & Reference Grounding**:
   - Ingest target path (`directory` or `files`).
   - Ground in the host repository's naming standards if present (project authority takes priority); otherwise read and apply `references/role-naming-rubric.md`.

2. **In-Turn Pragmatic Audit**:
   - Audit target code directly in-turn against rubric dimensions.
   - Enforce Section 1 Tolerability Guardrails: strictly ignore benign idioms, local brevity, and working helpers.
   - For every finding, classify the remediation explicitly as either `[RENAME]` or `[REFACTOR]`.

3. **Synthesis & Turn-Halt Gate**:
   - Consolidate findings into the Canonical Output Contract.
   - Assign definitive Health Rating (`PRISTINE`, `LOCALIZED_DRIFT`, or `SYSTEMIC_DEBT`).
   - Present completed dossier into conversation stream and halt turn immediately.
