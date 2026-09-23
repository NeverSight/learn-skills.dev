---
name: pr
description: Create a high-quality pull request description for UX-related implementation that explains why the change exists, what behavior changed, design-system usage, states, accessibility, testing, risks, and what reviewers should inspect. Use when design or design-engineering work is ready to become a PR.
license: MIT
metadata:
  author: Tranz007
  version: "0.2.1"
---

# PR

Make the pull request understandable to an engineer who was not in the design conversation.

## Always

- **Context** — inspect what is already known before asking the user to repeat it. Use `.ux/INTENT.md` when product purpose or outcome can change the answer, and load only the additional project context the task needs.
- **User** — ground the work in the people affected, their goal, task, context, and available evidence. Do not invent user needs, behaviors, or personas.
- **Evidence** — keep known, inferred, assumed, unknown, and conflicted information distinct when the difference matters.
- **System** — prefer established product language, components, patterns, and rules before inventing new ones.
- **Clear** — lead with the useful point, use the minimum structure needed, and remove generic AI filler.
- **Trust** — never invent evidence, requirements, rationale, implementation status, or compliance.
- **Outcome** — for substantial multi-step work, keep intent active, use a small `.ux/STATE.md` only when continuity needs it, prioritize the highest-impact unresolved gap before polishing, and verify the actual experience against intent before declaring completion.

Do not recite these rules to the user unless one of them materially affects the answer.

Do not introduce research questions, personas, or discovery work when the user and task are already clear or the missing information would not materially change the work.

## Inspect before writing

Read the actual diff or changed files when available, the relevant design/handoff/contract, decision records, the smallest relevant project context, design-system context, and the repository's PR template.

Describe what the code actually changes. Do not copy a design intention into the PR as though it has already been implemented.

## Write for review

A useful PR description normally answers:

- Why does this change exist?
- What user-visible or system behavior changed?
- Which existing components or patterns are reused, extended, or added?
- Which important states are covered?
- What accessibility behavior is relevant?
- What was tested or verified?
- What remains intentionally out of scope?
- What should reviewers pay particular attention to?

Include links to authoritative design, intent, decision, ticket, or contract artifacts when available.

Do not force empty sections into the PR template.

## Make review easier

Call out risky transitions, async behavior, new shared patterns, migration impact, unresolved constraints, or places where implementation intentionally differs from the initial design.

Avoid vague descriptions such as "updates UI" or enormous chronological change logs.

## Repository actions

If the user asks to open a PR and tools permit it, inspect the branch/diff and repository state first. Opening, updating, merging, requesting reviewers, or otherwise mutating a PR requires the user's authorization for that action. Never merge merely because the description is complete.

## Contrast example

Bad:
> Updates the account recovery UI to match the new designs. Also fixes some accessibility issues and error states.

Good:
> **Why:** Users could become stranded when verification failed during account recovery.
>
> **Changed:** Failed verification now preserves the entered code, shows the existing Alert error pattern, and moves focus to the error summary. No new design-system components were added.
>
> **Review:** Please verify the API-error mapping and focus behavior. Expired-code recovery is intentionally out of scope for this PR.

Why: the good description gives engineering the reason, implemented behavior, system impact, review focus, and scope without narrating every file change.

## Examples

- "Write the PR description for this UX change."
- "Create a PR engineers can actually review."
- "Explain this design-engineering change in the PR."
