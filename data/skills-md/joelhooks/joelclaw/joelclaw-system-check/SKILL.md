---
name: joelclaw-system-check
displayName: Joelclaw System Check
description: "Run a comprehensive health check of the joelclaw system — k8s cluster, worker, Inngest, Redis, Typesense/OTEL, tests, TypeScript, repo sync, memory pipeline, pi-tools, git config, active loops, disk, stale tests. Outputs a 1-10 score with per-component breakdown. Use when: 'system health', 'health check', 'is everything working', 'system status', 'how's the system', 'check everything', or at session start to orient."
version: 1.1.0
author: Joel Hooks
tags: [joelclaw, health, diagnostics, checks, operations]
---

# joelclaw System Health Check

Run `scripts/health.sh` for a full system health report with 1-10 score.

```bash
~/Code/joelhooks/joelclaw/skills/joelclaw-system-check/scripts/health.sh
```

## What It Checks (16 components)

| Check | What | Green (10) | Yellow (5-7) | Red (1-3) |
|-------|------|-----------|-------------|----------|
| k8s cluster | pods in `joelclaw` namespace | 4/4 Running, 0 restarts | partial pods | no pods |
| pds | AT Proto PDS on :2583 | version + collections | pod running, port-forward down | pod not running |
| worker | system-bus on :3111 | 16+ functions | responding, low count | down |
| inngest server | :8288 reachable | responding | — | down |
| redis/gateway | Redis + gateway session queues | connected, low pending queue | connected, backlog rising | unavailable |
| typesense/otel | Typesense health + OTEL query path | healthy + queryable | healthy, query degraded | unavailable |
| tests | `bun test` in system-bus | 0 fail | — | failures |
| tsc | `tsc --noEmit` | clean | — | type errors |
| repo sync | monorepo HEAD vs `origin/main` | in sync | ahead/behind | repo unavailable |
| memory pipeline | `joelclaw inngest memory-health` | healthy checks | degraded checks | failing checks |
| pi-tools | extension deps installed | all 3 deps | — | missing |
| git config | user.name + email set | set | — | missing |
| active loops | `joelclaw loop list` | queryable | query degraded | unavailable |
| gogcli | Google Workspace auth | account authed, token valid | token stored, no password | not configured |
| disk | free space + loop tmp | <80% used | — | >80% |
| stale tests | `__tests__/` + acceptance tests | clean | — | present |

## When to Run

- **Session start** — orient on system state before doing work
- **After loops complete** — verify nothing broke
- **After infra changes** — k8s, worker, Redis config
- **When something feels off** — quick triage

## Fixing Common Issues

**Repo drift**: `cd ~/Code/joelhooks/joelclaw && git fetch origin && git status -sb`

**pi-tools broken**: `cd ~/.pi/agent/git/github.com/joelhooks/pi-tools && bun add @sinclair/typebox @mariozechner/pi-coding-agent @mariozechner/pi-tui @mariozechner/pi-ai`

**PDS unreachable**: `kubectl port-forward -n joelclaw svc/bluesky-pds 2583:3000 &` (or if pod down: `kubectl rollout restart deployment/bluesky-pds -n joelclaw`)

**Worker down**: `joelclaw inngest restart-worker --register`

**Stale tests**: `rm -rf ~/Code/joelhooks/joelclaw/packages/system-bus/__tests__/ && find ~/Code/joelhooks/joelclaw/packages/system-bus/src -name "*.acceptance.test.ts" -delete`

**Loop tmp bloat**: `rm -rf /tmp/agent-loop/loop-*/` (only when no loops are running)

## Inngest Hung-Run Quick Triage

When a run appears stuck after first step:

```bash
joelclaw run <run-id>
```

If trace shows `Finalization` failure with `"Unable to reach SDK URL"`:

1. Verify registration/health:
`joelclaw inngest status`

2. Verify function is present where expected:
`joelclaw functions | rg -i "manifest-archive|<function-name>"`

3. Check for stale app registrations in Inngest UI/API and remove stale SDK URLs.

4. Assume possible handler blocking (not just network):
review recent step code for filesystem/Redis/subprocess blocking before step response.
