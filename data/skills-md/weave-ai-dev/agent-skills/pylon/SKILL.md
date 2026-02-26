---
name: pylon
description: Pylon MCP tools for pushing plans, code reviews, and pulling human feedback. Use this skill when interacting with the Pylon AI-to-human review bridge.
license: MIT
metadata:
  author: weave-ai-dev
  version: "1.0.0"
  organization: Weave AI
  date: February 2026
  abstract: Reference guide for Pylon's MCP tools. Covers push_plan, pull_plan, push_code_review, pull_code_feedback, list_documents, list_versions, use_document, update_project, and release_document.
---

# Pylon

Pylon is an AI-to-human review bridge. AI agents push proposed plans and code diffs via MCP; humans review, comment, and approve via a rich web editor.

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

Add Pylon's MCP server to your agent config. See `references/setup.md` for per-agent instructions.

**Claude Code** (`.mcp.json`):
```json
{
  "mcpServers": {
    "pylon": {
      "type": "streamable-http",
      "url": "https://your-pylon-instance.com/api/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN"
      }
    }
  }
}
```

Generate a token at **Settings > Auth Tokens** in the Pylon web UI.

## Golden Rule

**New user request = new project. Always omit `document_id` on the first push.** The server auto-creates a fresh document every time you call `push_plan` without `document_id`. Never look up or reuse document IDs from previous conversations or tasks.

## Key Principles

1. **Push any plan the user asks for.** Pylon is a general-purpose plan review tool, not limited to code. Business plans, budgets, project plans, roadmaps, architecture docs — if the user asks you to plan something, draft it and push it to Pylon. Never refuse a plan request because it's "not a software engineering task."
2. **Native MCP calls only.** Never write scripts or temp files to interact with Pylon.
3. **Always set `source`.** Identify yourself (e.g. "claude-code", "backend-dev") so the human knows which agent produced each document.
4. **`context` must be informative on every push.** Summarize the user's goal, relevant decisions, and why this change matters. The web UI's AI uses this to make better suggestions — make it useful and insightful, not mechanical. Never describe the MCP action itself (e.g. "re-pushing to update") — always describe the intent behind the work.
5. **New task = omit `document_id`.** `push_plan` without `document_id` always creates a new document. Only pass `document_id` when re-pushing to the same document within the same task after receiving feedback.
6. **Always pass `document_id` explicitly** on `pull_plan`, `push_plan` (updates), and `pull_code_feedback`. Do not rely on the session remembering your current document — sessions can be lost.

## Quick Workflow

```
1. push_plan(plan="...", source="claude-code", group="my-project", context="...")
   → Creates NEW document + project, returns document_id + URL
   → NEVER pass document_id here — let the server create a fresh document
2. Share the document URL with the user and STOP.
   → Do NOT poll, wait, loop, or use extended thinking while waiting.
   → Do NOT "stand by" for review — just tell the user the URL and finish your turn.
   → The user will come back and ask you to pull when they are ready.
3. pull_plan(document_id="<id-from-step-1>")  (only when the user asks)
   → Always pass document_id explicitly — don't rely on session memory
   → Returns markdown (readable plan), decisions (resolved threads), feedback (open threads to address)
4. Address any feedback, then proceed with the approved plan
5. If human requests changes:
   push_plan(document_id="<id-from-step-1>", plan="...", context="Updated based on feedback...")
   → Always pass document_id to update the SAME document
```

## Code Review Workflow

```
1. push_code_review(files=[...], source="claude-code", group="my-project",
     plan_document_id="<plan-doc-id>")
   → Always pass plan_document_id if this code review is associated with a plan
   → Links the code review to the plan in the UI for traceability
   → Returns code_review_id + URL
2. Share the URL with the user and STOP (same rules as push_plan).
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
