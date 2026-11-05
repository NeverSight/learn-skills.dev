---
name: sdlc-verify
description: >-
  Independent review of a finished intent, in fresh context, against the
  accepted outcome. Writes a short report.md. Use after sdlc-apply for every
  intent, or when the user asks for an independent check. Does not edit source
  or tests.
license: MIT
metadata:
  author: acourtiol
  version: "3.0"
---

# sdlc-verify

Default after `sdlc-apply` for every intent: an implementer who checks its own work is lenient and misses what a fresh reader catches. The user may waive it for an intent or a run; otherwise do not go from apply straight to close.

The reviewer must not have seen the implementation conversation. Use a fresh subagent (same model is fine) or a separate fresh session; a role name or default dispatch does not prove isolation, so confirm it. The implementer cannot pass its own work. The reviewer edits nothing except `report.md`. If no independent route exists: tier `critical` writes a `blocked` report; tier `change` says "not independently reviewed" in `## Result` and the user decides whether to accept.

Tier `change` is a lite review: acceptance items, the diff and the affected checks only. Tier `critical` adds the Spec, migration and failure-path checks below.

## Handoff

Give the reviewer only: repo path, slug, the committed candidate (`reviewed_head`), the `base` from `intent.md`, the path of `intent.md`, and the user's decisive request wording. No summary of what was done or why.

## What the reviewer does

1. Check the snapshot: `HEAD` equals `reviewed_head`, no uncommitted change touches a file in the diff (other people's unrelated dirty files are ignored), steps are ticked, `## Result` is filled. Otherwise `blocked`.
2. Compare the user's wording, intent and diff in both directions: every requested outcome is delivered for real (not as a manual fallback or test double), and nothing was added that the user did not ask for.
3. Read the whole diff `base..reviewed_head`: logic, trust boundaries, error handling, regressions in callers of any changed shared contract, fit with existing patterns.
4. Run the affected checks itself. Reuse an earlier result only if it inspects the raw output and the code, config and command match; never take a claim on trust.
5. Exercise every Acceptance item. For UI, drive the main path and an error path in the running local app. For pipelines, look at the consumer or outgoing request, not only stored values. For stateful flows, look at persisted state after failure and retry. For migrations, confirm the upgrade from the applied history on a disposable database preserves data.
6. Never touch production or a shared default database. For tier `critical`, or when unrelated files are dirty, run the checks in a detached checkout of `reviewed_head` (`git worktree add --detach <tmp> <reviewed_head>`), and remove it afterwards.
7. Stop at the first CRITICAL. Do not re-run what retained raw output already proves.

Scope verification to this change and its real blast radius. Do not replay unrelated features' journeys or recertify the whole product.

## Report

Write `intent/<slug>/report.md`, 40 lines or fewer:

```markdown
---
slug: example-slug
reviewed_head: <full commit hash>
verdict: pass   # pass | fail | blocked
---

# Report: short name

## Checked
- PASS | <acceptance item or requirement> | <command or action> | <what was observed, evidence path>

## Findings
None. Or: - CRITICAL | WARNING | SUGGESTION: <file:line> what, and what evidence would settle it.

## Not checked
None. Or what and why. For `blocked`: Reason and Recovery lines instead.
```

`pass` needs evidence for every Acceptance item, a committed candidate, and no CRITICAL finding. Leave the report uncommitted; the close commit never needs it (the folder is deleted); read it before that. A change to the reviewed files after `reviewed_head` makes the report stale and needs a fresh review. A fix after a `fail` is made by `sdlc-apply`; the new fresh reviewer reads the findings and the fix commits, not the whole change again. A second `fail` stops the loop: report it to the user with the narrow repro.
