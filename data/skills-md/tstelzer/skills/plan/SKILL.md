---
name: plan
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Plan

## Overview

Write comprehensive implementation plans assuming the engineer has zero context
for our codebase and questionable taste. Document everything they need to know:
which files to touch for each task, code, testing, docs they might need to
check, how to test it. Give them the whole plan as bite-sized tasks.

Assume they are a skilled developer, but know almost nothing about our toolset
or problem domain. Assume they don't know good test design very well.
Plans must be standalone documents that do not rely on the prior chat.

**Announce at start:** "I'm using the plan skill to create the implementation plan."

**Save plans to:** `<repository-root>/plans/YYYY-MM-DD_HH:MM_<plan-name>.md`

## Plan Structure

```markdown
# Plan: <Feature Name>

## Summary
<One paragraph describing what this builds>

## Prerequisites
<Only task-specific setup/deps/docs not already implicit from repo context or `AGENTS.md` — skip if none>

## Open Questions
<Unknowns or decisions to resolve before/during implementation — skip if none>

## Out of Scope
<What this plan explicitly does NOT cover>

## Overview
<A couple of paragraphs about approach>

## Task <n>: <name>
**Files:** `path/to/file.ts:42`, ...
**Depends on:** Task <m> (if any)
**Details:** <What to do and why>
**Code Changes:** <Code changes in fenced blocks or patch-style hunks; full-ish for non-trivial edits, abbreviated only for trivial/safe edits>

**Verify:** <How to confirm this task is done — command, test, manual check>
```

## Standalone Plan Rules

- You MUST write a standalone plan; you MUST NOT reference the chat (e.g., "as discussed above").
- You MUST restate all assumptions, constraints, definitions, and goals inside the plan body (Summary/Overview/Prerequisites/Open Questions).
- You MUST NOT include redundant global context in **Prerequisites** (for example: repo root path, generic workspace commands already documented in `AGENTS.md`, or a list of skills used to write the plan).

## Open Questions Discipline

- All unknowns/decisions MUST appear only in **Open Questions**.
- Tasks MUST be concrete and decision-free; you MUST NOT propose alternatives inside tasks.
- If a task depends on an unanswered question, you MUST explicitly block it and mark the dependency.
- You MUST NOT use ambiguous language in tasks (e.g., "could", "might", "maybe", "either/or", "TBD", "figure out").
- If an open question is answered while drafting, you MUST remove it from **Open Questions** and integrate the answer into Summary/Overview/Prerequisites/Tasks before finalizing.
- Tasks MUST NOT reference **Open Questions** unless the question is still unresolved and the task is explicitly marked blocked.

## Remember

- You MUST include exact file paths (line numbers if relevant).
- You MUST provide concrete, verbose implementation steps (code when useful), not vague directives.
- Code-in-plan policy:
  - If a change is extremely trivial and low-risk (for example: a one-line rename, import addition, or obvious constant tweak), you MAY describe it with an abbreviated inline snippet or short example.
  - Otherwise, you MUST include the full or near-full code that should be added/changed for the task (enough for the implementer to apply it without inventing missing logic).
  - Prefer full function/component/type definitions or patch-style hunks over dumping entire files when only part of a large file changes.
  - For large files, include only the changed regions plus enough surrounding context to apply the edit safely.
  - Do not include generated artifacts or bulky machine-produced diffs (e.g., lockfiles, snapshots, build output) unless they are the core subject of the task.
  - Do not hide substantive edits behind placeholders like "..." when that omits important logic, control flow, types, or error handling.
- You MUST format non-trivial code changes in fenced code blocks (preferred) or patch-style hunks, and identify the target file/path near each snippet.
- For each task, the `**Files:**` list MUST match the files referenced in that task's code snippets/hunks (no extra or missing files).
- You MUST include exact verification commands and expected output when deterministic; otherwise include the exact command/check and the expected observable result/assertion.
- You MUST NOT include meta process notes in the plan (for example, which plan skill(s) you used to produce the plan). Only mention external docs/tools when they are actual implementation inputs.
- You MUST order tasks by dependency, call out blocking relationships, and make each task independently verifiable.
- If behavior changes, you MUST include test additions/updates in the same task or a dependent task; if not adding tests, explain why.
- Prerequisites and open questions MUST be resolved and integrated before any dependent implementation task begins, or the task MUST be explicitly marked blocked.
- Before finalizing, you MUST run a "standalone + no-open-questions-in-tasks + answered-questions-cleanup" pass.
