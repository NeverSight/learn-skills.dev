---
name: software-design-doc
description: Draft, review, and update Software Design Descriptions using an IEEE 1016-2009-inspired structure with explicit architecture/views/elements formalization and output structure validation. Use this whenever a user asks to write an SDD, assess SDD quality/completeness, align design docs to IEEE 1016 concepts, map PRD requirements to design, produce architecture/interface/data design sections, generate a gap report with remediation actions, perform SDD review-only gap analysis, or update an SDD after architecture changes.
license: MIT
metadata:
  author: RJTPP
  version: 0.3.3
---

# Software Design Description

Create or review an SDD using an IEEE 1016-inspired structure while staying pragmatic for project context.

## Resources

- Use [references/sdd-completeness-checklist.md](references/sdd-completeness-checklist.md) for completeness gates and required content coverage.
- Use [references/sdd-template.md](references/sdd-template.md) as the default SDD structure.
- Use [references/sdd-template-implementation-deep.md](references/sdd-template-implementation-deep.md) when detail profile is `implementation-deep`.
- Use [references/viewpoint-mapping.md](references/viewpoint-mapping.md) to choose viewpoints and map them to concrete views.
- Use [references/copyright-safety.md](references/copyright-safety.md) for copyright/standards guardrails.
- Use [references/quality-attribute-scenarios.md](references/quality-attribute-scenarios.md) for quality-attribute scenario patterns.
- Use [scripts/check_sdd_structure.py](scripts/check_sdd_structure.py) to validate required headings and core formalization sections.
- Use [scripts/count_text_size.py](scripts/count_text_size.py) to inspect file size quickly (`chars`, `words`, `lines`) and optional Markdown heading breakdown (`--by-heading`).

Mandatory preflight sequence:

1. Read available context first (PRD/SDD/repo docs relevant to the request).
2. Optionally run a size check for large docs: `python3 scripts/count_text_size.py <path> --by-heading` or scan all docs: `python3 scripts/count_text_size.py --glob "**/*.md"`.
3. Recommend mode, detail profile, and interaction option from that context.
4. Ask for user confirmation before drafting.

Do not start drafting until preflight confirmation is received, unless user explicitly uses `/fast` or `/assume`.

## Copyright and Standards Safety (Mandatory)

- Treat IEEE 1016-2009 as a conceptual reference only.
- Use original wording in all generated outputs.
- Do not reproduce or closely paraphrase any copyrighted standard text, tables, or figures.
- Do not provide clause text on request; provide section-alignment guidance and ask the user to consult their licensed standard copy for normative wording.
- When referring to IEEE structure, cite section identifiers only (for example `Clause 4`), not normative text.
- If a disclaimer is needed, include one concise line only (for example, `IEEE 1016-inspired internal guidance, unofficial.`).

## Defaults

- Mode: `draft+review`.
- Completeness strictness: `pragmatic`.
- Detail profile: `ieee-pragmatic`.
- Codebase inspection: enabled when repository context is available.
- Output files:
  - `docs/SDD.md`
  - `docs/SDD-gap-report.md`

If the user specifies a different mode, follow the user preference.
If the user specifies a different output path, only accept a safe relative path inside the project folder.

Mode shortcuts accepted in user prompts:

- `/de` or `/draft+review` -> `draft+review`
- `/d` or `/draft-only` -> `draft-only`
- `/r` or `/review-only` -> `review-only`

Mode resolution precedence:

1. Explicit shortcut token in the prompt (`/de`, `/d`, `/r`, or long form)
2. Clear natural-language intent (for example `review only`)
3. Default to `draft+review`

Interaction options:

- `/ask` (default): confirm scope/mode/inputs before drafting and request missing critical info.
- `/fast`: proceed immediately with reasonable assumptions, then list assumptions in the output.
- `/assume`: proceed with assumptions even if inputs are incomplete, and clearly mark assumption-based sections.

Detail profile options:

- `ieee-pragmatic` (default): strict base structure with concise implementation guidance.
- `implementation-deep`: keep all base sections and add deeper implementation sections.

If user asks for `detailed`, `implementation handoff`, `architecture deep dive`, `ERD/data dictionary`, or `full design package`, use `implementation-deep`.

## Output Path Safety (Mandatory)

- Only write outputs within the repository root (project folder).
- Allow custom subpaths when they remain inside the repository (for example `docs/reviews/v2/SDD.md`).
- Reject absolute paths and any path containing parent traversal (`..`).
- Never write to sensitive paths (for example `.git/`, `.github/workflows/`, `/etc/`, home directories).
- Never build shell commands by interpolating user-provided paths.

## Input Contract

Expect at least one of:

- project requirements/PRD context, or
- an existing SDD to review/update.

If neither is available, stop and ask for missing inputs before drafting.
Do not invent project-specific architecture details.

Useful optional inputs:

- architecture constraints,
- technology stack constraints,
- required viewpoints,
- completeness strictness override,
- explicit output path inside the project folder.

Before drafting, perform an intake check:

1. Confirm mode, detail profile, and output path.
2. Confirm whether repository inspection should be used.
3. Identify missing critical inputs (PRD context, existing SDD, key constraints).

If critical inputs are missing, ask concise clarification questions first.
Only skip clarification when user explicitly uses `/fast` or `/assume`.

## Modes

### `draft+review` (default)

1. Draft or update `docs/SDD.md`.
2. Run completeness/gap analysis.
3. Write both SDD and gap report files.

### `draft-only`

1. Draft or update `docs/SDD.md`.
2. Skip gap report unless requested.

### `review-only`

1. Do not rewrite source SDD unless user asks.
2. Produce `docs/SDD-gap-report.md` with concrete remediation actions.

## Required Workflow

1. Discover context

- Inspect repository docs and key code structure by default.
- Identify available artifacts: PRD, existing SDD, architecture notes, APIs, schemas.

2. Identify stakeholders and concerns

- Extract explicit and implied design stakeholders.
- Convert requirements/risks/NFRs into design concerns.

3. Select viewpoints

- Choose only viewpoints that address identified concerns.
- Mark omitted viewpoints as `Not Applicable` with justification.

4. Draft or update SDD

- Use section order from `references/sdd-template.md` (or deep template) as the canonical default.
- Use original wording; do not quote or mirror copyrighted standards text.
- Preserve required headings; reordering is allowed when it improves clarity for the project context.
- Keep core architecture sections at the architectural abstraction level (layers/components/responsibilities), not file-by-file implementation listings.
- Put concrete file/module paths in implementation-oriented sections (`12.*`, appendices, or traceability mappings) when needed.
- Include Mermaid diagrams when they improve clarity.
- Always include the core-3 formal artifacts:
  - `## 4. Architecture Overview`
  - `### 5.1 Viewpoint-to-View Mapping`
  - `### 6.1 Design Element Catalog (Formal Definitions)` with fields: `Component`, `Responsibility`, `Inputs`, `Outputs`, `Dependencies`, `Public Functions`
- Optional enhancements:
  - Include quality-attribute scenarios using `Stimulus`, `Environment`, `Response`, `Measurement` when quality concerns are material.
  - Include a short future-evolution note in `6.5` and/or `11.x` when persistent data is currently absent/static.
  - If optional enhancements are omitted, add a concise `N/A rationale`.
- If detail profile is `implementation-deep`, include extension sections:
  - `## 11. Data Design`
  - `## 12. Component Design`
  - `## 13. Human Interface Design`
  - `## 14. Requirements Traceability Matrix`
  - `## 15. Appendices`
  - `## 16. Design Decisions (Locked)`

5. Run pragmatic completeness pass

- Check coverage against core IEEE-inspired structure themes without reproducing standard text.
- Check concern-to-view coverage and missing decisions.
- Ensure architecture/viewpoint/element formalization is explicit and reviewable.
- Check consistency of terminology, component names, version references, and cited artifacts across the document.
- Allow justified simplification for project scale.

6. Write outputs

- Ensure parent directory exists.
- Resolve output paths safely inside repository root only.
- For `draft+review` or `draft-only`, write `docs/SDD.md` by default.
- For `draft+review` or `review-only`, write `docs/SDD-gap-report.md` by default.
- In `review-only`, do not modify source SDD unless explicitly requested.

7. Validate generated outputs

- Run `python3 scripts/check_sdd_structure.py --mode <draft+review|draft-only|review-only> --docs-dir <output-dir> --profile <ieee-pragmatic|implementation-deep>`.
- For evals/CI strictness, run with `--require-all-subsections`.
- Section completeness is strict by default; use `--allow-soft-sections` only when section checks should be advisory.
- In `review-only`, use `--allow-input-sdd` if source SDD is colocated with generated gap report.
- Treat checker hard-fail results as blockers and revise outputs before finalizing.

## Canonical Base Section Set (Template Order)

Use these headings as the default template sequence:

1. `## Document Control`
2. `## 1. Introduction`
3. `## 2. System Overview`
4. `## 3. Stakeholders and Design Concerns`
5. `## 4. Architecture Overview`
6. `## 5. Viewpoints and Views`
7. `## 6. Design Elements and Constraints`
8. `## 7. Traceability`
9. `## 8. Design Rationale`
10. `## 9. Risks and Mitigations`
11. `## 10. Summary`

## Gap Report Format

Use these headings in order:

1. `# SDD Gap Report`
2. `## Scope and Inputs`
3. `## Missing Required Content`
4. `## Weak or Implicit Rationale`
5. `## Traceability Gaps`
6. `## Recommended Fixes (Priority Ordered)`
7. `## Coverage Summary`

## Pragmatic Completeness Rules

- Treat mapped core content areas as required unless genuinely out of scope.
- Treat core architecture/view/element formalization (`4`, `5.1`, `6.1` with formal fields) as required.
- Treat quality scenarios and future-evolution notes as recommended enhancements; allow omission with concise `N/A rationale`.
- If an item is omitted, provide a short `N/A rationale`.
- Favor correctness and implementability over ceremonial detail.
- Keep terminology consistent with the project domain.
- Prefer `UX consistency` / `visual design constraints` over vague labels such as `aesthetics`.
- Prefer `single consolidated stylesheet` over `monolithic stylesheet`.
- If the user asks for exact IEEE wording, decline and provide a non-verbatim summary.

## Output Quality Bar

- SDD sections are complete enough for implementation handoff.
- Architecture overview is explicit and includes logical plus deployment/runtime depiction.
- Viewpoint choices are explicit with viewpoint-to-view mapping.
- Design elements are formally defined with component fields.
- Terminology, component names, and version/references are internally consistent across sections.
- Gap report recommendations are actionable and prioritized.
- No machine-specific assumptions or absolute local-only dependencies in document content.

## Example Requests That Should Trigger This Skill

- "Write an SDD with an IEEE 1016-inspired structure from this PRD and repo structure."
- "Review this SDD and list standards gaps with fixes."
- "Update our SDD after moving from monolith to microservices."
- "Map PRD requirements to design sections and identify missing architecture details."
