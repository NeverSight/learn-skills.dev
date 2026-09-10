---
name: agent-session-resume
description: Use when continuing, resuming, locating, reading, inspecting, auditing, or reviewing a previous AI coding-agent session, handoff transcript, chat log, exported conversation, saved artifact set, or session summary, on any platform (Claude Code, Codex, Cursor, Antigravity, OpenCode) or across several platforms in one ask, such as reviewing threads across Claude and Codex.
---

# Agent Session Resume

## Purpose

Resume or audit prior coding-agent work with continuity. Reconstruct what happened before acting, then continue from the real stopping point.

## Core Workflow

1. Run a provenance self-check.
   - Run `python3 skills/agent-session-resume/scripts/skill-provenance.py` when available.
   - Otherwise compare the loaded SKILL.md path and size against the known install paths under `$HOME/.claude` and `${CODEX_HOME:-$HOME/.codex}`.
   - Report staleness on the `Loaded skill` line of the resume report. Details: `references/evidence-and-provenance.md`.

2. Identify the source. If the user names a platform, read the matching file in `references/`; if the ask spans platforms, read `references/cross-platform.md`. Otherwise inspect the workspace for session folders, exports, summaries, and artifacts. When a session title is given, prefer exact or fuzzy title matches over recency.

3. Locate the transcript or best substitute. Prefer full transcripts over summaries, workspace-local session data over global history, and explicit user-provided paths over discovered paths.

4. Read the full available session record before acting. For large transcripts, inventory files, event types, and timestamps first, then read the evidence-bearing slices until the record is accounted for. Full coverage means no relevant evidence skipped; bounded searches and slices are fine for giant records, but say so and name the file/event. Do not edit files or repeat prior work before this pass is complete.

5. Record loaded-skill provenance in the report: path and source/version marker, or `unknown`, never a guess. Details: `references/evidence-and-provenance.md`.

6. Reconstruct context. Summarize the goal, decisions, constraints, and preferences; identify completed work, changed files, commands and tests run; pin the exact stopping point. Every work-state claim carries an evidence ref (`src/file.ts:L20-L35`, transcript lines, command output, or explicit "not checked yet"). Prior resume reports, summaries, and handoffs are claims, not primary evidence: re-verify against transcripts, files, git state, or command output, or label them unverified. Preserve explicit user deferrals ("skip", "park", "not now", "hold") with evidence, scope, and reopen condition.

7. Extract tasks. Capture explicit TODOs, plans, and open questions; infer implicit tasks from failing tests, unfinished edits, and "next step" language. Keep specific unfinished tasks specific. Track deferred work separately from `NOT DONE`. Classify: `DONE` (completed and verified, or no longer needed), `PARTIALLY DONE` (started but missing implementation, tests, review, commit, push, or confirmation), `NOT DONE` (not started or only discussed).

8. Validate against the workspace. Inspect git status before editing and mention it in the checkpoint; read files the prior session touched. Preserve unrelated user changes in a dirty worktree; use a separate worktree or ask before colliding work. If transcript claims conflict with current files, trust current files and report the mismatch.

9. Continue from the first unfinished step. Do not repeat completed work; follow the established approach and style unless clearly broken. Ask the user only when blocked by missing information or an unsafe choice.

## Resume Modes

Decide from the user's prompt how far to go after the checkpoint:

- `Report-only`: the ask is what happened, done versus pending, or to check/audit/review a prior session without edits. Stop after the resume report and clear next action.
- `Continue-edit`: the ask is to continue, fix, implement, open a PR, or run tests. Report first, then continue from the first unfinished safe step.
- `Quick resume`: status report or task breakdown. Prefer a compact source inventory, task classification, and next action.
- `Deep resume`: implementation continues, the source is ambiguous, or files may have drifted. Read the full record and current git state, then continue.

## Platform References

- Claude Code: `references/claude-code.md`
- Codex: `references/codex.md`
- Cursor: `references/cursor.md`
- Antigravity: `references/antigravity.md`
- OpenCode: `references/opencode.md`
- GitHub Copilot: `references/github-copilot.md`
- Cross-platform / multi-agent asks: `references/cross-platform.md`

## Required Response Shape

Before continuing execution, report:

```markdown
## Brief context summary

- Goal: <prior session goal>
- Loaded skill: path=<loaded SKILL.md path or "unknown">; source/version=<version marker or "unknown">
- Source reviewed: <transcript/export/artifact refs>
- Current workspace check: <git status summary and touched-file refs, or why not checked>
- Transcript/current repo mismatches: <none found | claim, transcript ref, current-repo ref, action>
- User deferrals: <none found | deferred scope, user wording, evidence ref, reopen condition>
- Stopping point: <last command, edit, failure, or user pause instruction with evidence>

## Task status breakdown

- DONE: <task> - evidence: <implementation refs>; verification: <test/tool refs or "not recorded">.
- PARTIALLY DONE: <task> - evidence: <started-work refs>; missing: <remaining gap refs>.
- NOT DONE: <task> - evidence: <TODO, failing test, absent artifact, or transcript gap refs>.

## Clear next action

- Next: <first unfinished step to take now>
- Blocked: <no | yes - reason and evidence>
```

Then continue immediately unless blocked. Evidence rules and the static idempotency contract: `references/evidence-and-provenance.md`.

## Guardrails

- Never assume the newest file is the right transcript when the user supplied a title or path.
- Never summarize from filenames alone or treat a compact summary as equivalent to an available full transcript.
- Never reset, revert, or discard existing changes unless the user explicitly asks.
- Never mark a task `DONE` or `PARTIALLY DONE` from a plan alone; status requires evidence of completion or started work.
- Never omit transcript/current-repo mismatches when the transcript and checked files disagree.
- Never unpark deferred scope from a vague "proceed" or "continue"; confirm the user wants that parked work reopened.
