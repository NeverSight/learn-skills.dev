---
name: autoblogwriter-cli
version: 1.0.0
description: Use this skill when the user needs to run or troubleshoot the AutoBlogWriter CLI for auth, workspaces, integrations, ideas, posts, or workflow runs. Prefer machine-readable JSON output and use CLI commands directly instead of re-implementing API logic.
---

# AutoBlogWriter CLI

Use this skill to operate the AutoBlogWriter CLI end-to-end for idea generation, post creation, scheduling, publishing, and run orchestration.

## When To Use

Use this skill when the user asks to:
- Authenticate or fix CLI auth
- Inspect workspaces or integrations
- Generate or apply ideas
- Create, schedule, or publish posts
- Validate, start, or inspect workflow runs

## Environment Requirements

- `AUTOBLOGWRITER_API_KEY` (preferred), or saved key via `autoblogwriter set-key`
- Optional: `AUTOBLOGWRITER_API_URL` (defaults to `https://api.autoblogwriter.app`)

## Operating Rules

- Default CLI output is JSON. Keep JSON output enabled unless the user explicitly asks for text.
- Prefer `--json-file` or `--inline` payloads for deterministic command execution.
- Validate workflow specs before starting runs.
- Report actionable error context from `error` and exit code.

## Quick Verification

1. Confirm CLI is available: `autoblogwriter status`
2. Confirm auth is configured (env var or saved key)
3. Confirm target workspace slug before mutating commands

## Command Reference

### Auth
- `autoblogwriter status`
- `autoblogwriter login --workspace <workspaceSlug>`
- `autoblogwriter set-key --key <value>`
- `autoblogwriter logout`

### Workspaces
- `autoblogwriter workspaces:list`
- `autoblogwriter workspaces:get <workspace>`

### Integrations
- `autoblogwriter integrations:list --workspace <workspace>`
- `autoblogwriter integrations:status --workspace <workspace>`

### Ideas
- `autoblogwriter ideas:generate --workspace <workspace> --json-file payload.json`
- `autoblogwriter ideas:list --workspace <workspace>`
- `autoblogwriter ideas:use-bulk --workspace <workspace> --idea-ids id1,id2`

### Posts
- `autoblogwriter posts:list --workspace <workspace>`
- `autoblogwriter posts:create --workspace <workspace> --inline '{"keywords":["topic"]}'`
- `autoblogwriter posts:schedule-bulk --workspace <workspace> --json-file payload.json`
- `autoblogwriter posts:publish-bulk --workspace <workspace> --post-ids id1,id2`

### Runs
- `autoblogwriter runs:validate -f workflow.json`
- `autoblogwriter runs:validate --inline '{"version":"1",...}'`
- `autoblogwriter runs:start -f workflow.json`
- `autoblogwriter runs:start --inline '{"version":"1",...}'`
- `autoblogwriter runs:status <runId>`
- `autoblogwriter runs:logs <runId>`
- `autoblogwriter runs:list`

## Standard Output Contract

```json
{
  "ok": true,
  "command": "ideas:generate",
  "data": {},
  "meta": {
    "workspace": "workspace-slug",
    "requestId": "optional"
  },
  "error": null
}
```

## Exit Codes

- `0`: success
- `2`: partial success
- `10`: auth/config error
- `11`: validation/spec error
- `12`: API/network failure
- `13`: rate/plan limit error

## Troubleshooting Flow

1. `10` auth/config error:
Re-check `AUTOBLOGWRITER_API_KEY` or run `autoblogwriter set-key --key <value>`.
2. `11` validation/spec error:
Run `autoblogwriter runs:validate` and fix payload/schema issues before retrying.
3. `12` API/network failure:
Retry with same inputs, then verify `AUTOBLOGWRITER_API_URL` and network connectivity.
4. `13` rate/plan limit error:
Reduce batch size, retry later, or switch to an eligible workspace/plan.

## Task-Specific Questions

1. Which workspace should this run against?
2. Do you want to use `--json-file` or `--inline` payloads?
3. Are we generating ideas, creating posts, or executing a run spec?
4. Should I optimize for read-only inspection or mutating actions?
