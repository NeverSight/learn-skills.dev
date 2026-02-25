---
name: collabute-mcp
description: Use Collabute MCP for organization-specific context retrieval and proposal-safe actions. Trigger when users ask about meetings, memory, Linear, Slack, or Vercel data from their Collabute workspace, or ask to create tasks from meeting context.
license: MIT
metadata:
  author: collabute
  version: "1.0.0"
  repository: https://github.com/collabute/collabute-agent-skills
  canonical_owner: collabute
  deprecated_owner_paths:
    - muperdev/collabute-agent-skills
---

# Collabute MCP

Use this skill when the task depends on private organizational context stored or indexed by Collabute.

## When to use

Use this skill when requests include:
- Recent meetings, action items, owners, follow-ups, transcript content
- Team memory, prior decisions, historical context
- Linear task lookup from Collabute indexes
- Slack thread/message retrieval from Collabute indexes
- Vercel project/deployment status via Collabute integration
- "Create a task from this meeting" or similar write intent

Do not use this skill for generic coding questions that do not require workspace data.

## Preconditions

1. The MCP server is already configured in the client as `collabute`.
2. Auth is OAuth-first; do not rely on static PAT headers for MCP.
3. Use `tools/list` as the source of truth for currently available tools/scopes.

## Core behavior rules

1. Prefer deterministic retrieval tools before broad memory search.
2. For write intents, use proposal tools only; do not assume direct third-party mutation.
3. If a required tool is missing from `tools/list`, explain missing scope and ask user to re-auth.
4. If a meeting is referenced, keep all lookups scoped to that meeting before broadening.
5. Use transcript pagination for full transcript requests; avoid dumping large transcript output in one response.

## Tool map

- `system.ping`
  - Use for connectivity and tenant sanity checks.
- `meeting.list_recent` (`meeting:read`)
  - Deterministic recent meeting discovery.
- `meeting.get` (`meeting:read`)
  - Structured meeting detail with summary, memory evidence, and cited transcript snippets.
- `meeting.get_transcript` (`meeting:read`)
  - Explicit full transcript access with pagination.
- `memory.search` (`memory:read`)
  - General memory-first retrieval across org context.
- `memory.get_bundle` (`memory:read`)
  - Intent-specific context packaging.
- `linear.search_tasks` / `linear.get_task` (`linear:read`)
  - Linear task lookup.
- `slack.search_threads` / `slack.list_suggestions` (`slack:read`)
  - Slack retrieval.
- `vercel.list_projects` / `vercel.list_deployments` / `vercel.get_deployment` (`vercel:read`)
  - Vercel retrieval.
- `meeting.propose_task_from_meeting` (`write:propose`)
  - Safe task creation proposal derived from meeting evidence.
- `memory.propose_write`, `integration.propose_action` (`write:propose`)
  - Proposal-only write flows.

## Playbooks

### Playbook A: "Fetch my recent meetings and create a task"

1. Call `meeting.list_recent` with a small `limit`.
2. Choose the best candidate meeting.
3. Call `meeting.get` with a focused query, such as `"action items and owners"`.
4. Extract actionable items and corresponding snippet ids.
5. Call `meeting.propose_task_from_meeting` with:
   - `meetingId`
   - clear `title`
   - concise `description`
   - `sourceSnippetIds` when available
6. Tell the user the result is a pending proposal and requires approval.

### Playbook B: "Show full transcript"

1. Call `meeting.get_transcript` with `offset: 0` and bounded `limit`.
2. Continue while `hasMore` is true using `nextOffset`.
3. Summarize as needed and keep raw transcript output scoped to the user request.

### Playbook C: "What changed in Linear/Slack/Vercel?"

1. Start with the provider-specific read tool (`linear.*`, `slack.*`, `vercel.*`).
2. Use `memory.search` only when additional cross-domain context is required.
3. Report results with timestamps/status fields when present.

## Error handling

- `401` or unauthenticated:
  - Instruct user to complete OAuth auth flow for the Collabute MCP server.
- Forbidden scope (missing `meeting:read`, `write:propose`, etc.):
  - Ask user to re-authorize and grant required scopes.
- Not connected integration:
  - Tell user to connect integration in Collabute settings.
- No data found:
  - Suggest narrowing or broadening query by project/channel/time range.

## Response contract for agents

When using Collabute MCP, responses should:
1. State which Collabute tool(s) were used.
2. Distinguish facts from inference.
3. Cite meeting snippet context when proposing meeting-derived tasks.
4. Clearly mark proposal outputs as `pending approval`.
