---
name: docker-destructive-guardrails
description: Use this skill before running, or recommending, any Docker command that deletes, wipes, resets, or otherwise irreversibly changes state — even if the user just says to "clean up", "clear the cache", "start fresh", "wipe everything", "nuke it", "reset", "force remove", or "tear down" Docker resources. Covers generic Docker CLI destructive operations not owned by a more specific skill — `docker rm`, `docker rm -f`, `docker container prune`, `docker kill`, `docker system prune`, `docker rmi`/`docker image rm`, `docker image prune -a`, `docker network rm`, `docker network prune`, `docker builder prune`, `docker buildx rm`, `docker context rm`, and standalone (non-Compose) `docker volume rm`/`docker volume prune`. Also indexes destructive commands owned by other Docker skills (Compose, sandbox, Desktop). Core rule — state exactly what will be lost and get explicit confirmation first, except narrow, low-friction Tier 1 container cleanup.
license: Apache-2.0
compatibility: Applies to any Docker CLI version. This is a behavioral guardrail skill, not a Dockerfile or Compose authoring skill.
---

# Docker Destructive Command Guardrails

## Overview

This skill provides the cross-product policy for handling destructive or irreversible Docker CLI operations: commands that delete data, remove resources, or otherwise cannot be undone. Use it whenever a task could reasonably lead to running one of these commands, even if the user never names the command directly. It covers the generic Docker CLI commands with no home in a more specific skill, and it indexes where other destructive commands (Compose, sandbox, Desktop) are documented.

## When to use this skill

Activate this skill when:

- The user asks to "clean up", "clear the cache", "start fresh", "wipe everything", "nuke it", "reset", "force remove", or "tear down" Docker resources without naming a specific command
- The agent is considering `docker rm`, `docker rm -f`, `docker container prune`, `docker kill`, `docker stop`, `docker system prune`, `docker rmi`, `docker image rm`, `docker image prune -a`, `docker network rm`, `docker network prune`, `docker builder prune`, `docker buildx rm`, `docker context rm`, or standalone (non-Compose) `docker volume rm`/`docker volume prune` as a fix for an unrelated problem (disk space, a stuck container, a stale network, a broken build cache, an old builder or volume)
- The user wants a cross-product overview of destructive commands across Docker skills

## Do not use this skill when

Do not use this skill when:

- The destructive command in question is Compose-specific (`docker compose down -v`, `docker compose rm -v`, `docker volume rm`/`docker volume prune` in a Compose project) — use `docker-compose-patterns` directly, which owns that guidance in full detail
- The task is authoring or reviewing a Dockerfile or `compose.yaml` with no cleanup or deletion involved
- The operation is non-Docker (git, filesystem, cloud resources) — this skill covers Docker CLI operations only

## Core guidance

The core rule for every command below: **state exactly what will be deleted, stopped, or lost, and get explicit confirmation from the user before running it.** Never run a destructive command as a default troubleshooting or "just clean it up" reflex — disk space, stuck containers, and stale caches almost always have a narrower, non-destructive fix. See `references/docker-cli-destructive-commands.md` for exact flags and the safe, scoped alternative for each.

The container-lifecycle commands — `docker rm`, `docker rm -f`, `docker container prune`, and `docker kill` — don't all carry the same risk, so they're split into two tiers below instead of one flat rule. `docker stop` follows a related but distinct reversible-action rule right after the tiers. Every other command in this list follows the flat rule stated above with no exceptions: state what's lost, get explicit confirmation, and wait for the user's answer before running it.

### Tier 1 — low-friction container cleanup

Applies only to `docker rm <name>` on an already-stopped container and `docker rm -f <name>` on a container the agent itself created and started earlier in the same session purely for testing or debugging — the `-f` carve-out applies even when the container is still running, since that's the only reason `-f` would be needed. All of the following must hold: the container is already stopped, or was created/started by the agent itself this session for testing/debugging; there's no known unpersisted state at risk; the action targets one specific, identified container rather than an unscoped sweep; and the agent is acting on an explicit user ask this session, not its own initiative. When every condition holds, the agent removes the container, states what it did, and proceeds — no blocking confirmation is required first. Tier 2's `docker rm -f` rule below applies to every other case.

### Tier 2 — container commands needing confirmation

`docker kill` is always Tier 2 (see the reference for why no stopped-container exception exists for it). Also Tier 2: `docker container prune` (it always sweeps every stopped container on the host, never just the one the agent is cleaning up), `docker rm -f` on any container that doesn't meet every Tier 1 condition above (in particular, a running container the agent didn't create/start this session, or one it did but is acting on without an explicit user ask), any other unscoped sweep regardless of container state (e.g. `docker rm -f $(docker ps -aq)`, "remove/kill all containers"), a container the agent didn't create and has no context on, and any action taken on the agent's own initiative rather than an explicit user ask. These carry the same confirmation bar as every flat-rule command in this skill: state exactly what will be lost and get explicit confirmation before running anything — no exception carved out.

### `docker stop` — reversible, outside the tier model

`docker stop` doesn't remove anything — the container still exists and can be restarted with `docker start` — so it sits outside the Tier 1/Tier 2 removal model above. It's still in scope for this skill because it interrupts a running process (SIGTERM, then SIGKILL after the timeout) and discards any unpersisted in-container state. On the agent's own test/debug container from this session, treat it like Tier 1: stop it and state what happened, no blocking confirmation required. On any other container, state that it will stop running and any unsaved in-memory state will be lost, then get confirmation first.

- **`docker system prune`** — deletes stopped containers, unused networks, dangling images, and build cache; `-a` also deletes unused tagged images, and `--volumes` also deletes unused *anonymous* volumes (named volumes are untouched — deleting those needs a separate `docker volume rm`).
- **`docker rmi` / `docker image rm`** — deletes a specific image; see the reference for `-f`'s exact (partly unverified) override behavior on multi-tag/referenced images.
- **`docker image prune -a`** — deletes every image not referenced by any container, running or stopped, not just dangling ones.
- **`docker network rm`** — deletes the specifically named network(s) passed as arguments; see the reference for how its `-f` flag differs from `docker context rm -f` below.
- **`docker network prune`** — deletes every custom network not attached to a container.
- **`docker builder prune`** — clears the BuildKit cache; `-a`/`--all` also removes internal helper/frontend images and cache shared with other build outputs, forcing a cold rebuild for anyone using that cache.
- **`docker buildx rm`** — removes a builder *instance*, distinct from the cache `docker builder prune` clears — see the reference for flag details.
- **`docker context rm`** — deletes a context's local connection config; doesn't affect remote resources but may not be trivially reconstructable. Unlike `docker network rm -f` above, `docker context rm -f` genuinely forces removal even if the context is currently in use.
- **`docker volume rm` / `docker volume prune`** (standalone, no Compose project in play) — deletes volume data directly and irreversibly; `docker volume prune -a`/`--all` widens the default anonymous-only scope to named volumes too. For a Compose project's own volumes, use `docker-compose-patterns` instead (see Related skills); for a volume declared `external: true` in a compose.yaml but not managed by that Compose project, this skill's guidance applies since Compose won't touch it via `down -v`.

## Related skills

- For Compose-specific destructive commands (`docker compose down -v`, `docker compose rm -v`, `docker volume rm`/`docker volume prune` in a Compose context), use `docker-compose-patterns` — it owns that guidance in full detail; this skill only indexes it. This skill owns the standalone (non-Compose) case for `docker volume rm`/`docker volume prune` itself — see Core guidance and `references/docker-cli-destructive-commands.md`.
- For Dockerfile internals, build caching, and image size optimization (non-destructive concerns), use `docker-build-strategies`.
- For first-time Docker project scaffolding, use `docker-project-foundations`.
- For sandbox (sbx) destructive commands (`sbx rm`, `sbx prune`), use `docker-sandboxes-lifecycle` — it owns that guidance in full detail; this skill only indexes it. Docker Desktop destructive-command guardrails will live in their own skill once merged (see `references/cross-skill-destructive-command-index.md` for tracking status); do not assume their content until that skill ships.

## References

- `references/docker-cli-destructive-commands.md` — Per-command breakdown of exact flags, what's deleted, and the safe/scoped alternative for each generic Docker CLI destructive command.
- `references/cross-skill-destructive-command-index.md` — Cross-product table of destructive commands across all Docker skills, including a pending placeholder for Docker Desktop.

## Assets

This skill has no bundled assets.

## Checks

- `checks/verification.md` — Manual review runbook, including example bad/good dialogues for handling destructive-command requests.
