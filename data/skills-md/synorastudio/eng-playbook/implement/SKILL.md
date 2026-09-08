---
name: implement
description: Implement an accepted slice of work as verified production code.
disable-model-invocation: true
---

# Implement accepted work

Turn an accepted slice into working, verified production code. Make local engineering decisions inside that slice without creating new product commitments.

## Establish the implementation contract

Start from the most specific accepted source available:

- An accepted Spec.
- One or more selected Feature Issues.
- Scope accepted in the current conversation.

A Spec or Feature Issue is useful, not mandatory. A draft Spec is not accepted work. When sources conflict or leave a blocking product decision unresolved, pause for the user. Suggest `grill` when the missing decision has dependent branches that need a fuller design discussion.

Read the target repo's Agent Guidance and only the Language, ADRs, Living Docs, tracker context, Project Guardrails, and code relevant to the slice. Include external controls such as required checks, protected integration paths, deployment gates, and tracker states when they affect delivery. Use the current implementation to discover constraints. Do not use it to expand the accepted scope.

Before editing, identify the observable outcome, the acceptance criteria that apply, and how the result can be verified. If the requested body of work contains several independent or dependency-ordered slices, start with the smallest dependency-ready slice unless the user asked to complete the whole set.

## Work inside the accepted slice

Choose reversible implementation details autonomously. Pause when the work requires:

- A product-scope change.
- A hard-to-reverse architecture decision.
- A new paid service, external vendor, or hosted dependency.
- Risk to persisted data or a migration whose effects are not already accepted.
- A change to authentication, permissions, secrets, or other security-sensitive behavior.
- A broad refactor outside the accepted slice.

Preserve unrelated work already present in the repo. When the accepted outcome conflicts with the current implementation or cannot be completed as written, report the conflict instead of quietly changing the contract.

Follow applicable Engineering Conventions and Project Guardrails. Prefer preserving a constraint through architecture or code, then automated checks, then concise guidance. Never bypass or weaken a guardrail merely to make the slice pass.

Use this deviation rule exactly:

> Any deliberate failure to meet an applicable Engineering Convention requires explicit approval.

## Implement and verify

Keep the feedback loop tight. Use focused checks while working and run the broadest relevant project checks before finishing. Discover those checks from Agent Guidance, project configuration, and existing conventions rather than assuming a stack.

Add or update tests at stable, behavior-relevant boundaries when the repo supports them and the change warrants coverage. Use manual verification when automated coverage is unavailable or disproportionate, and state exactly what was checked.

Before finishing:

1. Verify each applicable acceptance criterion.
2. Inspect the full diff for scope drift, accidental changes, weak error handling, and missing coverage.
3. Run the broadest relevant checks available.
4. Separate failures caused by the change from unrelated failures that already existed. Fix only failures inside the accepted slice and report the rest.
5. Confirm that changed Project Guardrails and their documentation or external configuration still agree.

## Keep durable knowledge true

Update an existing durable artifact when the implementation changes the truth it owns:

- `LANGUAGE.md` for recurring project vocabulary.
- ADRs for accepted, hard-to-reverse, surprising trade-offs.
- Living Docs for current system shape, operations, onboarding, or project guidance.

Do not create speculative documentation or turn implementation notes into long-lived artifacts. Use `handoff` when unfinished work must continue in another session.

Change tracker state or commit only when the user asks or the repo's Agent Guidance makes that part of the workflow. Attribute agent-generated work at the durable boundary that records it. Use commit attribution for repository changes and visible attribution for agent-authored pull request descriptions, reviews, comments, and tracker artifacts, following the project's established format.

## Follow the repository's integration workflow

Tracker hierarchy does not imply Git hierarchy. When the target repo uses branches and pull requests, create them around coherent repository changes rather than Decision Maps, Specs, or issue nesting.

Every commit that enters integration history uses `<type>[optional scope][!]: <description>`. Allowed types are `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `ci`, `chore`, `perf`, `style`, and `revert`. Write an imperative, lowercase description without a trailing period. Use `!` for a breaking change and explain the break and migration path in the body when they are not obvious. Keep the scope optional, split work that needs more than one primary type, and preserve required reference and attribution footers.

A squash workflow applies the rule to the pull request title or final squash message. A merge or rebase workflow applies it to every commit entering the integration branch. Follow the project's stronger local guardrails when present.

Target the repo's normal integration branch unless the accepted Spec or Agent Guidance requires a Milestone integration branch. Use that exception only when several changes must be verified atomically and their intermediate states cannot safely reach the normal integration branch. Use stacked branches only for real code dependencies, not because one tracker item is another item's child.

## Finish

Report the implemented outcome, verification performed, Project Guardrails added or changed, any departure from the accepted source, and remaining blockers or follow-up work.

Finish when the accepted slice works, every applicable acceptance criterion has evidence, applicable conventions and Project Guardrails are satisfied or have an approved deviation, the final diff has been reviewed, relevant durable knowledge matches the implementation, and any unresolved failure is reported with its effect.
