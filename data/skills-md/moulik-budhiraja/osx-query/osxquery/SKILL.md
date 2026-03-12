---
name: osxquery
description: Use OSXQuery when an agent must interact with desktop UIs, web apps, or browser workflows via the `osx` CLI. Apply it for querying UI element trees, resolving stable references, and executing actions with verification; also use it in automated tests where UI interaction is required to validate other systems or end-to-end behavior. Enforce screenshot-first verification for meaningful state changes and non-undoable actions.
---

# OSXQuery

## Purpose

Use OSXQuery as a computer-use tool when an agent must interact with desktop UIs, browser/web workflows, or UI-driven test flows used to validate other systems.
When browser interaction is required, use the user's default browser unless the user explicitly asks for a specific browser.

## Mandatory Pre-Read (Do Not Skip)

Read both documents in full before executing any `osx` command:
- [OSXQuery Query Usage](references/osxquery-query-usage.md)
- [OSXQuery Actions Usage](references/osxquery-actions-usage.md)

If either file is missing at these relative paths, stop and locate them first. Do not execute `osx` until both are read completely.
Treat those two usage docs as the source of truth for all command syntax, workflow sequencing, and troubleshooting details.

## Screenshot-First Policy (Required)

Screenshot verification is mandatory for OSXQuery workflows with meaningful state transitions.
Do not continue action execution when required screenshots are missing.

Capture screenshots at these checkpoints:
- Before the first action in any new page/view/dialog context.
- After every action that is expected to change UI state meaningfully.
- Both before and after non-undoable, high-impact, or destructive actions (delete, submit, close, overwrite, send).
- Before acting when selector results are ambiguous or multiple candidates look similar.

Screenshot file handling:
- Use the macOS `screencapture` CLI to take required screenshots.
- Save screenshots to temporary directories by default (for example, under `/tmp`).
- Clean up screenshot files after verification is complete.
- Keep screenshots only when the user explicitly asks to retain them.

Execution blockers:
- If screenshot evidence does not clearly confirm the intended target, stop and re-query before acting.
- If post-action screenshots do not match expected outcomes, stop, reassess, and do not chain further actions blindly.

## Query Output Guidance

Prefer compact tree output first when tree structure is useful:
- Use `--tree` by default to show only matched nodes.
- In compact tree output, `├●─` / `└●─` mean unmatched intermediate nodes were collapsed.

Treat full tree output as an escalation path, not a default:
- Use `--tree-full` only when the compact view is insufficient and you are stuck on ancestor/containment ambiguity.
- Do not reach for `--tree-full` just to browse. It adds a lot of unmatched wrapper noise and should be reserved for cases where the extra context is necessary to unblock targeting or verification.
