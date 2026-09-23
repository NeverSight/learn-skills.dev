---
name: agent-handoff
description: Create focused thread-to-thread handoff packets (workspace, goal, locked decisions, relevant files, hard-won context, working agreement, risks, acceptance criteria, verification steps, and next-thread starter prompt). Use when switching tasks, moving from backend to frontend, splitting large work into phases, or asking another agent/thread to continue implementation without context loss.
---

# Agent Handoff

## Overview
Create a clean handoff packet for the next thread instead of compressing context into a lossy summary.

The packet must answer four questions the next thread cannot answer from the code alone:
**where do I work, how do we work here, what would cost me hours to rediscover, and what do I read first.**

## Workflow
1. Define the exact next-thread goal in one sentence.
2. Pin down the workspace: checkout/worktree path, branch, base branch, commits so far, PR state.
3. Collect only relevant context for that goal:
- current implementation state
- API/data contracts and constants
- locked decisions and constraints (with the reason, so the next thread does not undo them)
- environment knowledge that took real time to obtain
- unresolved risks/blockers
- files the next thread must read first
4. State the working agreement: how this project expects work to be done, and which tools/skills are available for it.
5. Link the notes and docs that hold the canonical context.
6. Draft a next-thread starter prompt that is immediately executable.
7. Include acceptance criteria and a dedicated verification section.

## Output Format
Return a single markdown handoff packet with these sections in order:

- `Title`
- `Goal`
- `Workspace`
- `Current State`
- `Locked Decisions`
- `Contracts`
- `Relevant Files`
- `Hard-won Context`
- `Working Agreement`
- `Open Risks`
- `Acceptance Criteria`
- `Verification`
- `Related Docs`
- `Start Prompt`

Keep it concise and decision-complete. Avoid narrative history. Drop any section that would be empty rather than filling it with placeholders.

## Section Rules

### Workspace
Exact values, never paraphrase:
- checkout or git worktree path (the next thread runs commands there, not in the main checkout)
- working branch, and the **base branch** the PR targets — state it explicitly; a wrong base silently carries thousands of commits
- commits made so far (short sha + subject)
- PR number/state if one exists, and the PR title convention this repo enforces

### Locked Decisions
Each decision carries its reason. A decision without a reason gets undone by the next thread.

### Hard-won Context
Only what is expensive to rediscover. Typical entries:
- how to run the thing locally end to end (env file contents, ports to avoid because other sessions hold them, seeded credentials/cookies and the script that mints them)
- traps already hit, with the **symptom** as well as the cause — the next thread recognizes the symptom first
- errors that are normal and unrelated (so they are not chased)
- approaches already tried and rejected, and why
- cleanup the next thread owes (temp scripts, test rows, uncommitted local files)

### Working Agreement
How work is expected to proceed here, in short imperatives: slice size, when to stop and report, what counts as evidence, commit/comment/PR style, ports or data that are off-limits. Then list the tools and skills actually useful for this task (MCP servers, browser automation, doc lookup, symbol search, project skills) and when to reach for each.

### Related Docs
Canonical notes first, code second. Use the project's own linking convention (wikilinks for an Obsidian-style vault). Include personal/team note locations if the context lives there.

## Rules
- Prefer exact values over paraphrases (error codes, endpoint paths, payload shapes, feature flags, ports).
- Include file paths with line numbers when possible.
- Do not include unrelated files.
- If uncertainty remains, state it explicitly under `Open Risks`.
- `Acceptance Criteria` states what must be true when the next thread is done.
- `Verification` states how the next thread proves it, using exact commands or manual checks plus the expected result.
- If no reliable automated check exists, say so explicitly under `Verification` and provide the best manual fallback.
- Write the packet where this project keeps its living context. If the project has a notes vault, write it there and link it from the hub/milestone note; otherwise `docs/handoff/<yyyy-mm-dd>-<slug>.md`.
  - Obsidian-style vault example: `<vault>/projects/<project>/progress/<yyyy-mm-dd>-<slug>-handoff.md`, with the vault's note frontmatter, and add a link line in the milestone note. Follow the repo's writing rules for prose language.

## Starter Prompt Style
Use imperative wording so the next thread can execute immediately. Name the handoff file first, then the workspace, then the task.

Good:
- `Read <handoff path> end to end. Work in <worktree>, branch <x>, base <y>. Implement FE integration for POST /api/orders using the contracts in section 3.`
- `Execute phase 1 of this plan and report only regressions + fixes.`

Avoid:
- vague summaries
- retrospective narrative

## Resources
- Template: `references/handoff-template.md`
- Optional generator script: `scripts/create_handoff.py`

If a user asks for a saved handoff file, use the script first, then fill placeholders with real context.
