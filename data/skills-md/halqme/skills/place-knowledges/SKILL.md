---
name: place-knowledges
description: Use this skill when deciding where knowledge from a code change, correction, or review belongs—code, tests, comments, documentation, schemas, configuration, examples, decision records, or commit messages. Produce a minimal placement plan before editing when information could be duplicated or lost. Do not use it to draft prose, choose a commit message, or perform edits or Git operations.
---

# Place Knowledge

Decide where each useful piece of knowledge should live so that the current
system remains understandable after the change context is forgotten.

## Contract

- **Input:** the authoritative current behavior or requirement, the relevant
  change or diff, and the artifacts that may need to preserve it.
- **Output:** a concise placement plan identifying each knowledge item, its
  authoritative home, any justified projections, and the action required.
- **Side effects:** none. This skill decides placement; the workflow that owns
  each artifact performs any resulting edit or repository operation.
- **Failure:** if the current state, authority, or intended audience is
  ambiguous, inspect the relevant artifacts and ask or stop rather than
  guessing or duplicating information everywhere.

## Scope

This skill answers **where should this information live?** It does not draft or
edit the chosen artifact, summarize a commit, or execute a repository operation.

## Workflow

1. Establish the current state from the source of truth and the relevant diff.
   Separate stable behavior, user-facing usage, local constraints, regression
   contracts, implementation detail, and historical rationale. For a
   correction, render from the resulting state rather than preserving rejected
   alternatives unless the artifact is explicitly history-sensitive.
2. Find existing homes before creating or editing artifacts. Prefer one
   authoritative home for each fact; note a current artifact that should be
   updated or removed instead of creating a competing explanation.
3. Classify each knowledge item:
   - **Code:** how the system implements behavior and enforces invariants.
   - **Tests:** observable behavior, boundaries, failures, recovery, and
     regression contracts.
   - **Comments:** local, non-obvious constraints that cannot be inferred from
     the surrounding code.
   - **Documentation or examples:** current usage, public contracts, and
     user-facing or architectural guidance.
   - **Schema, configuration, or migration:** the authoritative data or
     compatibility contract for that concern.
   - **Commit message:** the purpose of this commit, its non-obvious rationale,
     and immediate compatibility consequences. It is history, not the sole
     home for stable behavior.
   - **Decision record, changelog, or migration guide:** rationale and
     before/after context that future readers explicitly need as history.
4. Add a projection only when it serves a distinct reader or protects a
   distinct contract. Derive it from the authoritative home, keep wording
   consistent, and omit it when the information is already obvious from the
   source or diff.
5. Produce the placement plan in this shape:

   | Knowledge | Authority | Projection or action | Reason |
   | --- | --- | --- | --- |
   | [fact or rationale] | [one artifact] | [none or distinct artifact] | [reader or contract served] |

6. Validate the plan before handing it off:
   - every necessary stable fact has an authoritative home;
   - no explanation exists only in a commit message when it must survive as
     current usage, behavior, or a contract;
   - duplicated text has a distinct audience or contractual purpose;
   - current-state artifacts contain no accidental correction residue;
   - commit-message input contains only commit-specific what/why;
   - unresolved ownership or audience decisions are surfaced instead of
     silently assigned.

Return the placement plan and any unresolved decision. Do not write prose or
modify files as part of this skill.
