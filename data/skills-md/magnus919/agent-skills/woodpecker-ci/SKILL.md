---
name: woodpecker-ci
description: >-
  Operate Woodpecker CI from installation through production troubleshooting: configure
  servers and agents, connect Forgejo/Gitea or another forge, write and validate
  pipelines, manage secrets and plugins, use Docker or Kubernetes backends, run the CLI,
  and diagnose failed builds. Use when setting up, administering, or debugging Woodpecker
  CI. Do not use this skill for unrelated requests; route to the nearest named specialist.
license: MIT
compatibility: Requires access to a Woodpecker instance for administration; Docker Compose, Kubernetes, or woodpecker-cli are optional depending on the backend.
metadata:
  source: https://woodpecker-ci.org/docs
  research: GroktoCrawl plus official Woodpecker documentation and repository sources
---

# Woodpecker CI

Use this skill as an operating playbook, not as a substitute for checking the documentation for the installed major version. Prefer explicit SemVer image tags, verify the resolved configuration before starting services, and verify runtime health after every change.

> **Scope boundary:** This skill configures and operates **Woodpecker CI** (the server, agents, workflows, and integrations). It does not install or administer Forgejo/Gitea itself, and it does not configure Forgejo Actions runners. When a task mentions Forgejo, treat it as the forge Woodpecker connects to unless forge administration is explicitly requested.

## Operating loop

1. Identify the Woodpecker major version, forge, backend, deployment files, database, public URL, and whether the task is a setup, pipeline, or incident.
2. Read the matching reference below before changing configuration.
3. Render and lint configuration before starting the server or agent.
4. Make the smallest change at the layer that owns the problem: forge/OAuth, server, agent/backend, or repository workflow.
5. Verify the result at the next boundary: server health, agent connected state, repository webhook, pipeline scheduling, step logs, and external deployment endpoint.
6. Record the exact version and relevant environment variables without recording secret values.

## Choose the entry point

| If the task is... | Start here |
|---|---|
| New server/agent or forge connection | `references/setup.md` |
| Workflow YAML, services, conditions, secrets, or plugins | `references/pipeline-syntax.md` |
| Upgrade, backup, metrics, CLI, or capacity | `references/operations.md` and `references/advanced-patterns.md` |
| A failed login, queued pipeline, clone, step, or backend | `references/troubleshooting.md` and `references/failure-signatures.md` |
| A trust or multi-tenant decision | `references/security.md` and the backend section of `references/setup.md` |
| Local lint/exec or CLI installation | `references/cli.md` |

Then load `references/source-index.md` when a version-sensitive command or variable needs confirmation.

## Quick command card

```bash
# Generate a shared server/agent secret
openssl rand -hex 32

# Compose Woodpecker server + agent (not Forgejo itself)
cp templates/docker-compose.yml compose.yaml
cp templates/forgejo.env.example .env
# edit .env, then:
docker compose config --quiet
docker compose up -d
docker compose ps
docker compose logs -f --tail=100 woodpecker-server woodpecker-agent

# Local workflow checks
woodpecker-cli lint .woodpecker.yml
woodpecker-cli exec .woodpecker.yml

# Pipeline and secret administration
woodpecker-cli repo info --repository OWNER/REPO
woodpecker-cli repo secret add --repository OWNER/REPO --name NAME --value @/path/to/value
```

`woodpecker-cli exec` is useful for local command and metadata checks, but it is not a complete substitute for a server run: server-managed secrets and forge events may not be available locally.

## Core defaults

- Use the Docker backend for isolated container steps. The Docker socket is powerful: treat an agent host as a CI trust boundary.
- Use the Kubernetes backend for pod-per-step isolation and cluster scheduling; review service accounts, namespace boundaries, pull secrets, PVC/storage, and resource requests before allowing repository authors to set backend options.
> **Multi-tenant default:** For untrusted repositories, prefer Kubernetes with namespace/RBAC/ServiceAccount controls when the cluster is already operated as a security boundary. Docker is a viable simpler default only with dedicated agents and trust-tier separation because the Docker socket controls the host daemon. Never use the Local backend for untrusted repositories.
- The agent needs `WOODPECKER_SERVER` and the same `WOODPECKER_AGENT_SECRET` as the server. The server registers an agent on first contact; persist the agent config file so its generated identity survives restarts.
- Keep `WOODPECKER_OPEN=false` unless open registration is intentional. Grant admin access explicitly and protect the OAuth client secret and agent secret.
- Do not expose secrets to untrusted pull requests by default. If a secret must be available there, restrict its events and plugin images and document the threat model.
- `depends_on` is for workflow ordering and parallelism; it is not a readiness check for service containers. Add a real wait/backoff or health probe for databases and caches.
- A step's `when` list is OR across entries and AND within one entry. Branch filters also affect pull-request target branches; combine `event` and `branch` when you mean pushes to a branch only.
- A passing `docker compose config` or CLI lint proves syntax/model validity, not that the agent can reach the forge, the image can pull, or the pipeline is safe.

## Reference routing

| Load when | Reference |
|---|---|
| Installing with Docker Compose, configuring Forgejo/Gitea, or choosing a backend | `references/setup.md` |
| Writing workflow YAML, events, conditions, matrices, services, plugins, or multi-workflow projects | `references/pipeline-syntax.md` |
| Designing parallel workflows, concurrency, caching, registries, reusable YAML, or autoscaling | `references/advanced-patterns.md` |
| Managing secrets, registries, CLI operations, upgrades, backups, and metrics | `references/operations.md` |
| A pipeline, clone, agent, OAuth, Docker, or Kubernetes run is failing | `references/troubleshooting.md` |
| You need a compact symptom-to-evidence map during an incident | `references/failure-signatures.md` |
| Reviewing trust boundaries, pull requests, plugins, local backend, or Kubernetes permissions | `references/security.md` |
| Using or installing `woodpecker-cli` | `references/cli.md` |
| Checking source URLs and version-sensitive claims | `references/source-index.md` |

## Included artifacts

- `templates/docker-compose.yml` — minimal server plus Docker agent deployment.
- `templates/woodpecker.yml` — conservative build/test/deploy workflow skeleton.
- `templates/forgejo.env.example` — placeholder environment contract for Forgejo.
- `assets/troubleshooting-checklist.md` — incident handoff checklist.
- `scripts/woodpecker-doctor.py` — dependency-free connectivity/configuration probe with text or JSON output.

## Available Scripts

| Script | Purpose | Invocation |
|---|---|---|
| `scripts/woodpecker-doctor.py` | Dependency-free connectivity/configuration probe for a Woodpecker deployment: checks the server HTTP URL and the agent gRPC endpoint, with text or JSON output. Run it as step one of any "is it the CI or is it me" diagnosis, after deployment changes to verify health, and before deeper troubleshooting. | `python3 scripts/woodpecker-doctor.py --url https://ci.example.com --server agent-host:9000 --json` |

## Prerequisites

- Network reachability from where you run the probe to the Woodpecker server URL and, when checking agents, the agent's gRPC host:port.
- Python 3 only — the probe uses the standard library and no third-party packages; it never mutates the Woodpecker instance.
- For actual administration beyond probing (per `compatibility`): access to the Woodpecker instance, and Docker Compose, Kubernetes, or `woodpecker-cli` depending on the backend in use — see references/setup.md and references/cli.md.

## Limitations

- The doctor probe reports connectivity and configuration signals only; a green probe does not prove forge OAuth works, pipelines schedule, or steps can pull images — verify at those boundaries separately (see Common failure boundaries).
- It reads nothing about repository-level state (webhooks, secrets, queue depth); use the server API/UI and references/troubleshooting.md for that.
- The skill documents operating patterns, not a pinned version: always confirm version-sensitive commands and variables against the installed major version via references/source-index.md.

## Common failure boundaries

- Server starts but repositories do not appear: inspect forge OAuth URL, callback URL, scopes, and server logs before changing pipeline YAML. For a push with no pipeline, inspect the Forgejo repository's **Settings → Webhooks → Recent Deliveries** first and record the delivery status.
- Agent is connected but never picks up work: compare labels/backend, maximum workflows, repository visibility/trust, and agent logs.
- A clone fails: first test network/DNS and credentials from an intentionally paused step; do not debug application commands until checkout works.
- A service is running but tests fail to connect: use the service hostname and container port, then add readiness handling.
- A secret is empty: check secret scope, event filters, plugin-image filters, and expression escaping (`$${NAME}` when Woodpecker must pass the variable to the shell).

## When not to use

Use a forge-specific skill for installing or administering Forgejo/Gitea itself, a Kubernetes operations skill for cluster lifecycle, and a Docker security skill for host hardening. This skill covers Woodpecker's integration points and CI behavior.
