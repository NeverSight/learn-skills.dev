---
name: plan-work
description: Read-only planning for an issue on the project issue tracker. Fetches the issue (and any linked parent), explores relevant code, then enters Plan Mode with a structured plan that declares an explicit Approach (RGR or direct). Use when user types /plan-work with an issue reference, or when planning an issue before implementing it manually.
---

# Plan an issue

`$ARGUMENTS` should be an issue reference (issue number, URL, or path) on the project issue tracker. If none is provided, stop and ask the user to link or pass one.

The issue tracker conventions (GitHub, Jira, local markdown under `.scratch/`, etc.) and triage label vocabulary should have been provided to you — run `/setup-imick-skills` if not.

## Workflow

1. **Read the issue**: fetch the referenced issue from the issue tracker and read its full body and comments (e.g. `gh issue view`, the Jira MCP, or the linked markdown file).
2. **Read the parent** if the issue references one — a PRD, epic, or parent issue. Follow whatever pointer the issue uses (`## Parent` heading, relative link, parent field, etc.).
3. **Recent context**: `git log -n 10 --oneline` to know what landed recently.
4. **Explore relevant code**: locate the files, tests, and modules the issue touches. Read them to understand current behaviour before planning a change.
5. **Enter Plan Mode** and present a plan with these sections:
   - **Understanding** — one paragraph in your own words: what the issue asks for.
   - **Files to touch** — concrete paths.
   - **Approach** — exactly one of:
     - `**Approach: RGR**` (red-green-refactor; this is the default)
     - `**Approach: direct (<rationale>)**` — only if RGR doesn't fit (config-only change, dependency bump, doc edit, UI tweak with no testable behaviour, etc.). State the rationale.
   - **Test ordering** — if RGR, list the tests to write first, second, third. Each is a tracer bullet for one behaviour. Do not list all tests up front.
   - **Key decisions** — design choices where you went with one option over another, and why.
   - **Risks / edge cases** — what could go wrong; what to watch for during implementation.

## Invariants

- This skill is **read-only**. Plan Mode enforces this — never attempt to edit or write files.
- Do not modify the issue's triage state on the issue tracker (status field, labels, inline `Status:` line, comments). The user manages triage state manually.
- Do not create the branch. The user creates branches manually before implementing.
- Do not commit, do not push, do not modify git state.

## Handoff

After Plan Mode approval, the user invokes `/do-work` in the same session. The approved plan — including the resolved issue reference and title — stays in conversation context for the next skill to read; no file persistence.
