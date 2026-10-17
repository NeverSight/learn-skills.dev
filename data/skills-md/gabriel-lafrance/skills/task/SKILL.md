---
name: task
description: Stateless end-to-end build loop for one verifiable outcome, with no tests-first phase. Use only when the user types /task or asks to build without tests. Any other build request goes to /task-with-tests.
category: Code
---

# Task

Orchestrate one verifiable outcome end to end. Plans stay inline in chat unless the user requests a saved artifact and approves its destination.

## Read when

- About to search the codebase, read a large file, or wade through long output? Open [main-context.md](../rules/main-context.md).
- About to grill? Open [doctrine.md](doctrine.md) and the [execution context](../rules/planning.md#execution-context).
- About to grill or plan a Feature? Open [strong-foundation.md](../rules/strong-foundation.md). Skip it and the first provider is hardcoded into every caller, so the next ticket is a rewrite.
- At a step that names a section? Open [reference.md](reference.md) (lifecycle, plan contract, behavior locks, ship Questions).
- About to ask the user anything? Open [Asking the user](../rules/writing-style.md#asking-the-user).
- About to write a test? Open [no-unrequested-tests.md](../rules/no-unrequested-tests.md), then [testing.md](../rules/testing.md).
- About to commit, push, or open a PR from this chat? Open [shipping.md](../rules/shipping.md). Skip it and you push to `main`, open a PR nobody approved, or track `origin/main`.

## Process

1. Apply the shared [ready-ticket preflight](../rules/execution.md#ready-ticket-preflight), then establish or refresh the in-chat execution context. If a parent already supplied ticket, lane, Done when, non-goals, rules that must stay true, fixed point, and slice bounds, accept that brief. The parent keeps ticket and branch ownership. For a request to implement a parent ticket's children, use the [whole-stack handoff](doctrine.md#whole-stack-ticket-handoff).
2. Run the [lifecycle](reference.md#lifecycle) in this order:
   1. Reuse the ready ticket lock; grill only unresolved consequential choices.
   2. Plan.
   3. [Behavior-lock suggestion](reference.md#behavior-lock-suggestion). It waits for the user, who can refuse every test.
   4. Implement. Apply [code-quality.md](../rules/code-quality.md) and [code-structure.md](../rules/code-structure.md) before every slice, and [user-experience.md](../rules/user-experience.md) before every user-facing slice.
   5. Gate: apply [verification scope](../rules/execution.md#verification-scope) and review the changed diff. Localized low-risk work can use focused checks and review in this context. Substantial/high-risk work uses independent `/verification` and `/review` agents together when available; judge their handoffs here. Honor explicitly requested independent/full workflows.
   6. Fix mode, as needed.
3. Write a test only for a lock the user accepted, following [testing.md](../rules/testing.md).
4. Announce completion.

Shared [handoffs, remediation and recovery](../rules/execution.md) govern this loop. Progress, lookup, and route-specific steps live in the doctrine and reference.

### If a parent already owns the ticket, branch, and PR

Return a completion summary plus evidence envelope to the parent. The parent handles shipping under the user's existing authorization.

### If this chat owns shipping

After all gates pass, follow [shipping.md](../rules/shipping.md) when the user already authorized shipping, including an explicit request for stacked PRs. Otherwise offer [ship Questions](reference.md#ship-questions) and wait for yes.

## Anti-patterns

- Asking ship Questions, pushing, or opening a PR when a parent owns shipping
- Suggesting a test before the Locked in message, or writing a test the user did not accept
