---
name: shape-actionable-output
description: Use this skill when presenting multi-step work, operational guidance, debugging results, or agent progress that should be easy for a person to act on without holding hidden state in working memory. Put the next relevant action and current state in the foreground, keep tangents out of the active path, and make completed work concrete. Do not use it to compress explanations, reference material, or long-form prose whose primary purpose is understanding rather than immediate action.
---

# Shape Actionable Output

Shape output around the reader's current action without reducing the underlying analysis.

## Core principle

Keep the full reasoning and relevant information available internally, but expose only the working set the reader needs to understand the current state and act next.

The goal is not brevity by itself. A short answer can still be hard to act on, and a longer explanation can still be actionable when the task requires it.

## Workflow

1. **Identify the current state.** Determine what is already complete, what is blocked, and what remains. Prefer harness task state when it already exists instead of reconstructing a parallel checklist in prose.
2. **Foreground the next relevant action.** When the reader needs to do something, put that action before background explanation. Make it specific enough to execute without inferring an intermediate step.
3. **Bound multi-step work.** Present the smallest useful set of ordered actions. Keep each visible step focused on one outcome, and do not expose future steps until they help the current decision or action.
4. **Suppress unrelated branches.** Finish the active path before surfacing secondary issues. Preserve additional findings internally or state them separately only when they materially affect the current task.
5. **Make progress concrete.** State what now works, changed, or was verified in terms the reader can observe. Prefer evidence such as a passing check, changed behavior, produced artifact, or resolved blocker over generic claims of progress.
6. **End at the real boundary.** If user action is still required, finish with one concrete next action. If the requested work is complete, stop without inventing another task, recap, or closing pleasantry.

## State and progress

Do not force the reader to remember hidden conversational state such as “step 3 of 5.” Surface the state that matters now.

When a harness already provides persistent task or plan state, rely on that mechanism and avoid duplicating the whole plan in prose. Restate only the part needed to understand the current transition, blocker, or next action.

For long tasks, make meaningful completed work visible as it happens. Do not turn every tool call or implementation detail into progress narration.

## Working-set discipline

Limit the visible working set when several items compete for attention. This is a presentation constraint, not an analysis constraint.

- Keep relevant alternatives, findings, and future work available internally.
- Show only the subset needed for the present decision or action.
- Expand the set when completeness is itself the task, such as audits, comparisons, inventories, or exhaustive research.
- Do not use an arbitrary fixed item count when the task naturally requires more.

## Errors and debugging

State failures matter-of-factly:

1. what failed,
2. the relevant evidence,
3. the current best-supported cause when known,
4. the next diagnostic or fix.

Do not dramatize routine errors or bury the actionable information behind reassurance.

If repeated fixes fail, stop repeating equivalent actions. Re-examine the assumption that connects the observed evidence to the attempted fix, then choose one discriminating diagnostic step.

## Estimates

Do not invent precise time estimates for agent work.

When the reader is deciding whether to perform work themselves, describe scope using concrete units that are supported by the task: files, commands, migration steps, test suites, manual checks, or known external waits. Give a time estimate only when there is a reasonable basis for one.

## Interaction with other Skills

This Skill governs presentation of active work.

- Let `simplify-change` decide whether implementation complexity is necessary.
- Let `apply-correction` decide how corrected state is rendered into persistent artifacts.
- Let writing Skills govern prose quality, language, and long-form structure.
- Do not override a task that explicitly asks for a complete explanation, reference document, exhaustive list, or other output where immediate action is not the primary purpose.

## Completion criteria

Finish when all of the following hold:

- The reader can identify the current state without reconstructing it from prior turns.
- Any required next action is specific and visible.
- Completed work is described through observable results rather than generic progress language.
- Secondary issues do not crowd the active path.
- The presentation constraint has not removed information required for correctness or completeness.
- The response stops when the requested work is complete.
