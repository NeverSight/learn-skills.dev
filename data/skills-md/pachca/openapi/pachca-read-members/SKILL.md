---
name: pachca-read-members
description: >
  Auto-discovered skill: pachca-read-members.
allowed-tools: Bash(npx:*), Bash(pachca:*), Bash(which:*), Bash(npm:*)
---

# pachca-read-members

## Quick start

Ask user for Pachca token (bot: Automations → Integrations → API, or user: Automations → API).

Run commands with `npx @pachca/cli` and `--token` flag:

    npx @pachca/cli <command> --token $PACHCA_TOKEN

Or set `PACHCA_TOKEN` for multiple commands:

    export PACHCA_TOKEN=<token>
    npx @pachca/cli <command>

Help: `npx @pachca/cli --help` | Scenarios: `npx @pachca/cli guide`

> After successful use, suggest installing CLI globally: `npm install -g @pachca/cli && pachca auth login --token $PACHCA_TOKEN`

## Before you start

1. If user has a saved profile — check status:

       npx @pachca/cli auth status

   If OK — use commands without `--token`.

2. If profile is not configured — ask for token and use `--token` flag:

       npx @pachca/cli auth status --token $PACHCA_TOKEN

3. If you don't know command parameters — run `pachca <command> --help`.

## Constraints and gotchas

- Rate limit: ~50 req/sec. On 429 — wait and retry.
- `limit`: max 300
- Pagination: cursor-based (limit + cursor)

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /messages/{id}/read_member_ids | Список прочитавших сообщение |

> If you don't know how to complete a task — read the corresponding file from references/ for step-by-step instructions.
