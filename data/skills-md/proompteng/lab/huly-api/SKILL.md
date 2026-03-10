---
name: huly-api
description: 'Use Huly platform APIs for swarm communication across tasks, channels, and documents.'
---

# Huly API

## Overview

Use this skill whenever swarm agents need durable communication in Huly:

- `tracker` tasks board (issues)
- `chunter` channels (chat messages)
- `document` teamspaces (mission docs)

Every autonomous mission should update all three surfaces.
Default destinations for this workspace:

- Tracker issues board: `DefaultProject` (`https://huly.proompteng.ai/workbench/proompteng/tracker/tracker%3Aproject%3ADefaultProject/issues`)
- Documents teamspace: `PROOMPTENG`
- Chat channel URL: `https://huly.proompteng.ai/workbench/proompteng/chunter/chunter%3Aspace%3AGeneral%7Cchunter%3Aclass%3AChannel?message`

## Required Environment

Load credentials from the `huly-api` Kubernetes secret via AgentRun `spec.secrets`.

- `HULY_API_BASE_URL` (should target transactor, for example `http://transactor.huly.svc.cluster.local`)
- `HULY_BASE_URL` (optional human-facing base URL, often `http://front.huly.svc.cluster.local`)
- `HULY_API_TOKEN` (bearer token)
- Optional:
  - `HULY_WORKSPACE` (workspace slug for operator context)
  - `HULY_WORKSPACE_ID` (workspace UUID; helper can also infer from JWT)
  - `HULY_PROJECT` (task board project identifier/name/id)
  - `HULY_TEAMSPACE` (document teamspace name/id)
  - `HULY_CHANNEL` (chat channel name/id)
  - per-agent tokens: `HULY_API_TOKEN_<SWARM_AGENT_IDENTITY>` or `HULY_API_TOKEN_<SWARM_AGENT_WORKER_ID>`

## Helper Script

Use `scripts/huly-api.py`.

### Mandatory channel interaction loop

For every mission stage, run this in order:

1. Read recent channel history:

```bash
python3 skills/huly-api/scripts/huly-api.py \
  --operation list-channel-messages \
  --worker-id "${SWARM_AGENT_WORKER_ID}" \
  --worker-identity "${SWARM_AGENT_IDENTITY}" \
  --require-worker-token \
  --channel "${ACTIVE_HULY_CHANNEL}" \
  --limit 30
```

2. React to at least one relevant teammate message by posting a natural direct reply with decision impact in-thread:

```bash
python3 skills/huly-api/scripts/huly-api.py \
  --operation post-channel-message \
  --worker-id "${SWARM_AGENT_WORKER_ID}" \
  --worker-identity "${SWARM_AGENT_IDENTITY}" \
  --require-worker-token \
  --channel "${ACTIVE_HULY_CHANNEL}" \
  --reply-to-message-id "${RELEVANT_MESSAGE_ID}" \
  --message "Thanks for the context. I picked this up and I am implementing X next."
```

3. Post a worker-authored stage update after completing the mission action:

```bash
python3 skills/huly-api/scripts/huly-api.py \
  --operation post-channel-message \
  --worker-id "${SWARM_AGENT_WORKER_ID}" \
  --worker-identity "${SWARM_AGENT_IDENTITY}" \
  --require-worker-token \
  --channel "${ACTIVE_HULY_CHANNEL}" \
  --message "${OWNER_UPDATE_MESSAGE}"
```

### Mission-level sync (recommended)

```bash
python3 skills/huly-api/scripts/huly-api.py \
  --operation upsert-mission \
  --worker-id "${SWARM_AGENT_WORKER_ID}" \
  --worker-identity "${SWARM_AGENT_IDENTITY}" \
  --mission-id jangar-discover-20260302 \
  --title "Jangar discover cycle" \
  --summary "Top platform risks and next actions" \
  --details "Includes evidence, risk deltas, and PR links" \
  --stage discover \
  --status running \
  --swarm-agent-worker-id "${SWARM_AGENT_WORKER_ID}" \
  --swarm-agent-identity "${SWARM_AGENT_IDENTITY}" \
  --message "${OWNER_UPDATE_MESSAGE}" \
  --project "DefaultProject" \
  --teamspace "PROOMPTENG" \
  --channel "general"
```

This creates/updates:

- one task-board issue
- one mission document
- one channel message

### Single-surface operations

```bash
python3 skills/huly-api/scripts/huly-api.py --operation create-issue --title "..." --mission-id "..."
python3 skills/huly-api/scripts/huly-api.py --operation create-document --title "..." --mission-id "..."
python3 skills/huly-api/scripts/huly-api.py --operation repair-project-issues --project "DefaultProject" --limit 500
python3 skills/huly-api/scripts/huly-api.py --operation repair-project-issues --project "DefaultProject" --limit 500 --fill-empty-issue-descriptions
python3 skills/huly-api/scripts/huly-api.py --operation dedupe-project-mission-issues --project "DefaultProject" --limit 1000 --dry-run
python3 skills/huly-api/scripts/huly-api.py --operation repair-teamspace-documents --teamspace "PROOMPTENG" --limit 500
python3 skills/huly-api/scripts/huly-api.py --operation post-channel-message --message "..."
python3 skills/huly-api/scripts/huly-api.py --operation post-channel-message --channel "general" --reply-to-message-id "<parent-message-id>" --message "In-thread reply"
python3 skills/huly-api/scripts/huly-api.py --operation list-channel-messages --channel "general" --limit 30
python3 skills/huly-api/scripts/huly-api.py --operation account-info --worker-id "${SWARM_AGENT_WORKER_ID}" --require-worker-token
python3 skills/huly-api/scripts/huly-api.py --operation verify-chat-access --worker-id "${SWARM_AGENT_WORKER_ID}" --worker-identity "${SWARM_AGENT_IDENTITY}" --require-worker-token --channel "general" --message "Hi team, I am starting this stage and will post progress here."
```

### Raw HTTP mode (debug)

```bash
python3 skills/huly-api/scripts/huly-api.py --operation http --method GET --path /api/v1/account/<workspace-id>
```

## Operating Rules

- Every mission stage must publish artifacts to all three Huly modules: tasks, channels, and docs.
- Each swarm agent should authenticate with its own Huly organization account (no shared actor credentials).
- Always target Tracker `DefaultProject` issues and Docs `PROOMPTENG` teamspace unless a run explicitly overrides them.
- Resolve `ACTIVE_HULY_CHANNEL` dynamically from runtime context (prefer `swarmRequirementChannel`, then `HULY_CHANNEL`, then default).
- Read channel history before taking action, then react to relevant teammate messages with explicit in-thread follow-up replies using `--reply-to-message-id`.
- Use `--require-worker-token` for dedicated-account checks so shared fallback tokens are rejected.
- For strict identity mapping, set per-worker `HULY_EXPECTED_ACTOR_ID_<SWARM_AGENT_IDENTITY>` and use `--require-expected-actor-id`.
- Run `verify-chat-access` before autonomous delivery stages with a worker-authored `--message`.
- Include `swarmAgentWorkerId` and `swarmAgentIdentity` in issue/document artifacts.
- Keep channel messages human-readable by default; avoid appending metadata blocks.
  - If you need metadata in chat for a specific audit/debug flow, use `--append-channel-metadata`.
  - `upsert-mission` automatically infers these fields from `--worker-id/--worker-identity` (or
    `SWARM_AGENT_WORKER_ID`/`SWARM_AGENT_IDENTITY`) if explicit `--swarm-agent-worker-id`/
    `--swarm-agent-identity` flags are not provided.
- Keep channel updates concise, written by the worker, and linked to issue/doc/PR/deploy evidence.
- Issue descriptions must be long-form and knowledge-base quality. The helper now stores issue descriptions through
  collaborator refs (not raw inline markdown) so tracker descriptions reliably render and persist.
- `upsert-mission` now reuses existing mission issues by mission id prefix (`[mission:<id>]`) to avoid duplicate ticket creation.
- Use `repair-project-issues` to migrate legacy issues that still have inline markdown/plain text in `Issue.description`.
- Use `repair-project-issues --fill-empty-issue-descriptions` when historical issues have truly empty description fields.
- Use `dedupe-project-mission-issues` to move older duplicate mission issues to `Canceled` while keeping the most recent active issue.
- Document content must be long-form and knowledge-base quality. The helper now stores mission document bodies through
  collaborator content refs (not raw inline markdown) so Huly editor/collaborator consistently loads and renders content.
- Use `repair-teamspace-documents` to migrate legacy docs that still have inline markdown in `Document.content`.
- If Huly auth fails, stop and return a clear unblock request instead of silently continuing.
