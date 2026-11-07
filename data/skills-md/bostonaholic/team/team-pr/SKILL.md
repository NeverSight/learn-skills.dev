---
name: team-pr
description: 'Use for opening PRs only on explicit request. Never infer from passed verification. Includes project terms, evidence, and risk.'
effort: medium
argument-hint: "[docs/plans/<id>/]"
---

# Team PR — Create the Pull Request

Before each consuming step, read its linked shared rules from this installed skill directory.
If a required read fails, stop that step with the exact path. Never use checkout fallback or recursive loading.

Before finalizing prose you author, read the [writing standards](../team/references/writing.md); for the PR body, apply its `## One busy reader` rule and its `## Self-lint`. Preserve exact commands, tokens, and templates.

Two modes:

- **Resume mode** — `$ARGUMENTS/1-task.md` and `$ARGUMENTS/6-design.md` exist. Execution step 3 binds one review status from the newest `review-<n>.md` and one security status from the newest `security-review-<n>.md`.
- **Standalone mode** — no matching artifact directory, but the working tree has commits or staged changes ready to ship. The current branch is the work source.

## Core contracts

Each is detailed in [Execution](references/02-execution.md) at the step named.

1. **Update an existing CHANGELOG.md** after step 3 binds the review and security statuses, and commit before opening any PR; never create one unrequested (step 6).
2. **Open a draft PR automatically — do not stop to ask** (step 7), then report it and how to mark it ready for review.
3. Multi-repo: one draft PR per repo, with `## Companion PRs` links. [Tracking rules](references/tracking.md) own the in-review transition and the home-only closing rule.
4. After each push, refresh the body with exactly one closing line: never duplicated, never dropped (step 10).
5. **A branch that impacts a UI always carries screenshots** (step 4).
6. **Deferred findings and cross-model dispositions are comments on the home PR, never the body**: run [review comments](references/07-review-comments.md) after open and after each refresh; a refresh posts only missing comments.
7. Subagents and inline work split per Execution `## Step dispatch`.

Apply the [body authoring rules](references/03-pr-body-template.md) to initial drafts and every refresh.

## Procedure references

Read each reference completely when reaching that stage, in order.

1. [Input](references/01-input.md)
2. [Execution](references/02-execution.md)
3. [PR Body Template](references/03-pr-body-template.md)
4. [Screenshot Upload](references/04-screenshot-upload.md)
5. [Changelog Update](references/05-changelog-update.md)
6. [Commit Discipline](references/06-commit-discipline.md)
7. [Review Comments](references/07-review-comments.md)

## Applied principles

Read and apply: [focused work rules](../team/principles/focused-work.md).
