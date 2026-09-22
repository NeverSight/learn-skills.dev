---
name: baselinedocs-save
description: Capture durable baseline documentation in the middle of an existing brownfield conversation or implementation task. Use explicitly when the user wants to preserve current context for later reuse without restarting the workflow from initialization.
---

# Baseline Docs Save

Capture the current truth without pretending the work started with Baseline Docs.

Read `references/pack-contract.md` in full before creating or editing any pack file, every time. It is the only definition of which document owns which content; do not infer that from a filename, from an earlier session, or from memory.

Read `references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

## Workflow

1. Inspect the conversation, repository, current diff, existing docs, and relevant decisions.
2. Locate a matching pack and the repository's established baseline root before creating anything. Update a pack when its scope matches.
3. Use the established baseline root; when none exists, default to `docs/baseline`. Store a new pack at `<docs_dir>/<prefix>/`.
4. Choose a single-pack or multi-pack layout from `references/pack-contract.md`.
5. Separate confirmed implementation, explicit decisions, open questions, and unverified claims.
6. Write the smallest useful pack:
   - always create or update `introduction`, `roadmap`, and `hallucination`
   - add `sourcecode` only when architecture or implementation flow is reusable
   - add `useguide` only when a consumer contract or repeatable procedure exists
7. Preserve the exact continuation point and final evidence available now.
8. Report what was captured, what remains unverified, and where work should resume.

## Brownfield Rules

- Describe earlier work as observed history, not as work performed by this run.
- Do not reconstruct missing details from inference.
- Prefer current code and explicit user decisions over conversation summaries.
- Record `unknown` when the applicable commit cannot be established.
- Do not force empty extension documents merely to reach five files.

## Writing Rules

- Store outcomes, not a transcript of attempts.
- Keep one final verification result per claim or phase.
- Retain a failed attempt only when it explains a remaining risk, changes the chosen approach, or is needed to reproduce a defect.
- A lesson entry is not a transcript of an attempt. `references/pack-contract.md` states what it is and how long it stays.
- When an outcome needs its reasoning explained (a defect's cause, a rejected alternative), record that once in `hallucination` and link to it from `roadmap`. Do not restate the reasoning in both documents.
- Link reusable guidance to the project wiki instead of duplicating it inside the pack.

## Output

Create or update files. Do not return only a proposed outline.
