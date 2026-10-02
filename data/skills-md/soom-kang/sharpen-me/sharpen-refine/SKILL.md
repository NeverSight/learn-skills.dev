---
name: sharpen-refine
license: MIT
description: Improve existing code or technical documentation within an authorized boundary. Use for behavior-preserving refactors and requested documentation corrections, including code examples and tables; exclude feature work and unrelated cleanup.
---

# Sharpen Refine

Improve the requested artifact while preserving its required behavior or meaning. A justified no-op is successful.

## Inputs and mode

Required: target and requested improvement. Optional: allowed paths, protected regions, contracts, canonical sources, and validation commands. Use code mode for behavior-preserving refactors and documentation mode for explicitly in-scope technical documents. Ask only when the request leaves a material behavior or scope decision unresolved.

## Procedure

1. Read the target, project instructions, and current changes. Identify protected regions and unrelated user work. Adjacent files may supply evidence without becoming editable.
2. Establish invariants. Code includes relevant returns, errors, effect counts, ordering, public interfaces, and persisted shapes. Documents include requirements, decisions, uncertainty, provenance, and intended audience.
3. Make the smallest revision serving the request using existing conventions. Remove obsolete scaffolding, superseded deltas, redundant narration, or retired content only where the request covers them; retain history when it is the artifact's purpose or necessary evidence.
4. In documentation, verify changed claims against governing sources. Explicitly requested changes to fenced code, commands, tables, quotations, or user-authored text are allowed. Preserve their unaffected formatting and every separately protected region. Authorship alone does not prohibit an authorized edit.
5. For prose-only cleanup, leave formatted blocks unchanged unless correcting them is also requested. Preserve deliberate examples and look-alikes. Do not convert an unresolved decision into fact.
6. Use precise located edits; verify targets exist and report a missed replacement. Use a language-aware tool or a reviewed script for complex moves. Preserve unrelated bytes, Unicode, and line endings; avoid blanket replacements.
7. Run meaningful existing checks and inspect the final diff, references, and relevant behavior. In documentation mode, reread the complete affected document in context to catch stale explanations and broken references outside the edited lines. Do not alter tests to conceal behavior changes. Report unavailable or failed checks accurately.

## Output and stopping

Use the caller's format. Otherwise report the actual improvement, why it meets the request, executed checks, and material limits. Explain a no-op without creating changes.

Stop after the bounded verified change, or stop only the dependent part when it requires a behavior change, excluded files, missing evidence, or separate approval. Describe partial edits accurately and preserve existing work. Do not create extra files unless the authorized improvement requires and permits them. Authorization does not imply commit, push, deployment, secrets, or production-setting changes. In read-only contexts return a proposal.

## Examples

- Extract an internal helper while preserving error behavior and call order, then run existing module checks.
- Correct a requested command and version table while preserving an explicitly protected paragraph byte-for-byte.
