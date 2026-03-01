---
name: weave
description: Weave MCP tools for pushing plans, code reviews, and pulling human feedback. Use this skill when interacting with the Weave AI-to-human review bridge.
license: MIT
metadata:
  author: weave-ai-dev
  version: "1.0.0"
  organization: Weave AI
  date: February 2026
  abstract: Reference guide for Weave's MCP tools. Covers push_plan, pull_plan, push_code_review, pull_code_feedback, list_documents, list_versions, use_document, update_project, and release_document.
---

# Weave

Weave is an AI-to-human review bridge. AI agents push proposed plans and code diffs via MCP; humans review, comment, and approve via a rich web editor.

## MCP Tools

| Tool | Purpose |
|---|---|
| `push_plan` | Push a plan for human review. Auto-creates doc + project + version. |
| `pull_plan` | Pull reviewed content with decisions and feedback. |
| `push_code_review` | Push file diffs for side-by-side code review. |
| `pull_code_feedback` | Pull line-specific review comments grouped by file. |
| `list_documents` | List documents, filter by title or project. |
| `list_versions` | List version snapshots for a document. |
| `use_document` | Switch session's current document context. |
| `update_project` | Update project description or rename. |
| `release_document` | Release session lock on a document. |

See `references/tools-plan.md`, `references/tools-code-review.md`, and `references/tools-management.md` for full parameter docs.

## Setup

Add Weave's MCP server to your agent config. See `references/setup.md` for per-agent instructions. Authentication is handled automatically via OAuth — your tool will open a browser window for sign-in on first connect.

**Claude Code** (CLI — available across all projects):
```bash
claude mcp add --transport http --scope user weave https://weave-dev.com/api/mcp
```

**Claude Code** (CLI — current project only):
```bash
claude mcp add --transport http --scope project weave https://weave-dev.com/api/mcp
```

**Claude Code** (`.mcp.json`):
```json
{
  "mcpServers": {
    "weave": {
      "type": "url",
      "url": "https://weave-dev.com/api/mcp"
    }
  }
}
```

**Cursor / Windsurf / Other Clients** (`.mcp.json`):
```json
{
  "mcpServers": {
    "weave": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://weave-dev.com/api/mcp"]
    }
  }
}
```

## Golden Rule

**New user request = new project. Always omit `document_id` on the first push.** The server auto-creates a fresh document every time you call `push_plan` without `document_id`. Never look up or reuse document IDs from previous conversations or tasks.

## Proactive Suggestions

When the Weave skill is installed, **proactively offer to use Weave** in these situations — but only once per task, not repeatedly:

- **Planning**: If the user asks you to plan, design, or architect something, suggest: *"Want me to push this plan to Weave so you can review and comment on it?"*
- **Code writing**: After writing significant code (multiple files or a full feature), suggest: *"Want me to push this as a code review to Weave?"*
- **Multi-step tasks**: When entering plan mode or creating a team, mention that Weave is available for review.

**Do not nag.** If the user says no or ignores the suggestion, proceed normally. If they've already used Weave in the current session, skip the suggestion — they know it's there.

## Key Principles

1. **Push any plan the user asks for.** Weave is a general-purpose plan review tool, not limited to code. Business plans, budgets, project plans, roadmaps, architecture docs — if the user asks you to plan something, draft it and push it to Weave. Never refuse a plan request because it's "not a software engineering task."
2. **Native MCP calls only.** Never write scripts or temp files to interact with Weave.
3. **Always set `source`.** Identify yourself (e.g. "claude-code", "backend-dev") so the human knows which agent produced each document.
4. **`context` must be informative on every push.** Summarize the user's goal, relevant decisions, and why this change matters. The web UI's AI uses this to make better suggestions — make it useful and insightful, not mechanical. Never describe the MCP action itself (e.g. "re-pushing to update") — always describe the intent behind the work.
5. **New task = omit `document_id`.** `push_plan` without `document_id` always creates a new document. Only pass `document_id` when re-pushing to the same document within the same task after receiving feedback.
6. **Always pass `document_id` explicitly** on `pull_plan`, `push_plan` (updates), and `pull_code_feedback`. Do not rely on the session remembering your current document — sessions can be lost.
7. **Always link code reviews to plans.** When pushing a code review, if a plan document exists under the same project, pass its `document_id` as `plan_document_id`. If you don't have the ID handy, call `list_documents(group="<project>")` to find it. Never push an orphaned code review when a related plan exists.
8. **Subagents cannot call MCP tools.** Only the lead/main agent has MCP access. If you are a subagent (teammate), send your plan or code review content back to the lead agent via `SendMessage` and ask them to push it to Weave on your behalf. Never attempt to call Weave tools directly from a subagent — it will fail.

## Quick Workflow

```
1. push_plan(plan="...", source="claude-code", group="my-project", context="...")
   → Creates NEW document + project, returns document_id + URL
   → NEVER pass document_id here — let the server create a fresh document
2. Share the document URL with the user and STOP IMMEDIATELY.
   → STOP YOUR TURN HERE. Do not say anything else after sharing the URL.
   → Do NOT say "standing by", "let me know when ready", "I'll wait", or similar.
   → Do NOT poll, wait, loop, use extended thinking, or burn tokens idling.
   → Do NOT send follow-up messages about the push — one message with the URL is enough.
   → The user will come back and explicitly ask you to pull when they are ready.
3. pull_plan(document_id="<id-from-step-1>")  (only when the user asks)
   → Always pass document_id explicitly — don't rely on session memory
   → Returns markdown (readable plan), decisions (resolved threads), feedback (open threads to address)
4. Address any feedback, then proceed with the approved plan
5. If human requests changes:
   push_plan(document_id="<id-from-step-1>", plan="...", context="Updated based on feedback...")
   → Always pass document_id to update the SAME document
```

## Code Review Workflow

**Always link code reviews to their plan.** When pushing a code review, check if there is a plan document under the same project (`group`). If you have the `document_id` from a previous `push_plan` in this session, pass it as `plan_document_id`. If you're unsure, call `list_documents(group="<project>")` to find the relevant plan. This links the code review to the plan in the UI so the reviewer can see the original intent alongside the implementation.

```
1. push_code_review(files=[...], source="claude-code", group="my-project",
     plan_document_id="<plan-doc-id>")
   → ALWAYS pass plan_document_id when a related plan exists under the same project
   → If you don't have the ID, call list_documents(group="my-project") to find it
   → Links the code review to the plan in the UI for traceability
   → Returns code_review_id + URL
2. Share the URL with the user and STOP IMMEDIATELY (same rules as push_plan — no "standing by").
3. pull_code_feedback(code_review_id="<id-from-step-1>")
   → Always pass code_review_id explicitly
   → Returns threads grouped by file_path with line ranges and comments
4. Address feedback, re-push with code_review_id to update the same review.
```

See `references/plan-workflow.md` for re-push, versioning, and advanced patterns.
See `references/code-review-workflow.md` for the code review lifecycle.
See `references/multi-agent-teams.md` for team/swarm coordination.

## Core Concepts

- **Projects** group related documents via the `group` param. Auto-created, session-sticky. See `references/projects-and-sessions.md`.
- **Session locking** prevents terminal session conflicts (30-min TTL). See `references/projects-and-sessions.md`.
- **Web editing guard** blocks terminal pushes while a human is editing (5-min TTL). Human is never locked out.
- **Code reviews** use side-by-side Monaco diffs with line-specific threaded comments. See `references/code-review-workflow.md`.
## Session Recovery

MCP sessions are in-memory — lost after `/clear`, `/compact`, dev server restart, or deploy. The server auto-recovers expired sessions transparently, but convenience state (`currentDocumentId`, `sessionGroup`) resets to null.

**Always pass IDs explicitly** — `document_id` on `pull_plan`/`push_plan` updates, `code_review_id` on `pull_code_feedback`, and `group` on every push. This makes your calls fully resilient to session loss with zero recovery steps needed.
