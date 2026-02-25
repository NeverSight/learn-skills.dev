---
name: eve-read-eve-docs
description: Load first. State-today index of distilled Eve Horizon system docs with task-based routing for CLI/API usage, manifests, pipelines, jobs, secrets, agents, builds, events, and debugging.
triggers:
  - eve docs
  - eve horizon docs
  - read eve docs
  - eve cli
  - eve manifest
  - eve pipelines
  - eve workflows
  - eve job
  - eve secrets
  - eve auth
  - eve events
  - eve triggers
  - eve agents
  - eve teams
  - eve builds
  - eve releases
  - eve deploy
---

# Eve Read Docs (Load First)

Purpose: provide a compact, public, always-available distillation of Eve Horizon system docs. Use this when private system docs are not accessible.

## When to Use

- Any question about how to use Eve Horizon via CLI or API.
- Any question about `.eve/manifest.yaml`, pipelines, workflows, jobs, or secrets.
- Any question about events, triggers, agents, teams, builds, or deployments.

## How to Use

1. Start with `references/overview.md` for core concepts, IDs, and the reference index.
2. Use the task router below to choose the smallest set of references for the request.
3. Open only the relevant reference files and avoid loading unrelated docs.
4. Ask for missing project or environment inputs before giving prescriptive commands.

## Task Router (Progressive Access)

- Platform orientation, environment URLs, and architecture: `references/overview.md`
- Command syntax, flags, and CLI workflows: `references/cli.md`
- Fine-grained CLI intents:
  - `references/cli-auth.md` (auth + access + policy)
  - `references/cli-org-project.md` (init, org/project setup, docs, fs sync)
  - `references/cli-jobs.md` (jobs and execution controls)
  - `references/cli-pipelines.md` (builds, releases, pipelines, workflows)
  - `references/cli-deploy-debug.md` (deploy, recovery, local stack, CLI troubleshooting)
- Manifest authoring and config structure: `references/manifest.md`
- Pipelines, workflows, triggers, and event-driven automation: `references/pipelines-workflows.md` + `references/events.md`
- Job lifecycle, scheduling, and execution debugging: `references/jobs.md`
- Build, release, and deployment behavior: `references/builds-releases.md` + `references/deploy-debug.md`
- Agents, teams, and chat routing: `references/agents-teams.md` + `references/gateways.md`
- Secrets, auth, access control, and identity providers: `references/secrets-auth.md`
- Skills installation, packs, and resolution order: `references/skills-system.md`
- Harness selection and sandbox policy: `references/harnesses.md`

## Index

- `references/overview.md` -- Architecture, core concepts, IDs, job phases, reference index.
- `references/cli.md` -- CLI quick reference: all commands by category with flags and options.
- `references/manifest.md` -- Manifest v2 spec: services, environments, pipelines, workflows, x-eve extensions.
- `references/events.md` -- **Event type catalog** (all sources + payloads) and **trigger syntax** (github, slack, system, cron, manual).
- `references/jobs.md` -- Job lifecycle, phases, CLI, git/workspace controls, scheduling hints.
- `references/builds-releases.md` -- Build system (specs, runs, artifacts), releases, deploy model, promotion patterns.
- `references/agents-teams.md` -- Agent/team/chat YAML schemas, sync flow, slug rules, dispatch modes, coordination threads.
- `references/pipelines-workflows.md` -- Pipeline steps, triggers, workflow invocation, build-release-deploy pattern.
- `references/secrets-auth.md` -- Secrets scopes, interpolation, auth model, identity providers, OAuth sync, service principals, access visibility, custom roles, policy-as-code.
- `references/skills-system.md` -- Skills format, skills.txt, install flow, discovery priority.
- `references/deploy-debug.md` -- K8s architecture, worker images, deploy polling, ingress/TLS, secrets provisioning, workspace janitor, CLI debugging workflows, real-time debugging, env-specific debugging.
- `references/harnesses.md` -- Harness selection, profiles, auth priority, sandbox flags.
- `references/gateways.md` -- Gateway plugin architecture, Slack + Nostr providers, thread keys.
- `references/cli-auth.md` -- CLI auth, service accounts, access roles, and policy-as-code.
- `references/cli-org-project.md` -- CLI commands for org/project setup, docs, FS sync, and resolver URIs.
- `references/cli-jobs.md` -- CLI job lifecycle: create/list/update, attempt tracking, result/monitoring/attachments.
- `references/cli-pipelines.md` -- CLI build/release/pipeline/workflow command reference.
- `references/cli-deploy-debug.md` -- CLI environment deploy/recover/lifecycle and local k3d stack.

## Intent Coverage Matrix

| Intent | Minimum references | Expected output |
|---|---|---|
| Authenticate or inspect permissions | `references/cli-auth.md`, `references/secrets-auth.md` | Session state, token/permission validation result |
| Bootstrap org/project resources | `references/cli-org-project.md`, `references/manifest.md` | Org/project IDs, members, manifest sync status |
| Submit and monitor work | `references/cli-jobs.md`, `references/jobs.md` | Job IDs, phase transitions, attempt logs |
| Build/deploy a version | `references/cli-pipelines.md`, `references/builds-releases.md`, `references/pipelines-workflows.md` | Pipeline run ID, build/release artifacts, deployment trace |
| Recover from runtime issues | `references/cli-deploy-debug.md`, `references/deploy-debug.md`, `references/cli-jobs.md` | Diagnose output, recovery target, mitigation command plan |
| Inspect platform behavior or events | `references/events.md`, `references/agents-teams.md` | Canonical event stream view, routing path |
| Install/update skills for agents | `references/skills-system.md`, `references/overview.md` | Installed pack/skill set and resolution order |

## Hard Rules

- Eve is **API-first**; the CLI only needs `EVE_API_URL`.
- Do **not** assume URLs, ports, or environment state--ask if unknown.
- These references describe shipped platform behavior only.
- If anything is missing or unclear, ask for the missing inputs.
