---
name: fly-io
description: Deploy, configure, review, troubleshoot, and design Fly.io apps, Machines, networking, and storage, or operate and integrate Sprites persistent execution environments. Use for Fly infrastructure, flyctl/fly.toml, and Sprites CLI/API tasks.
---

# Fly.io and Sprites

Inspect the app's `fly.toml`, Dockerfile, deployment workflow, and relevant
runtime code before choosing changes. For Sprites, identify the organization,
Sprite name, and CLI or SDK integration instead; Sprites uses `sprite`, not
`flyctl` or `fly.toml`.

Use local command help and current official docs for commands, limits, pricing,
and availability. Start with `fly version` and `fly <command> --help`, or
`sprite --help` and its relevant subcommand help. A surviving CLI flag is not
proof that a retired service is available. Do not install tools or create
resources merely to inspect them.

## Read the relevant reference

- [Deploy and configuration](references/deploy-config.md): launch, process groups,
  health checks, scaling, autostop, releases, secrets, and CI/CD.
- [Machines](references/machines.md): API-controlled jobs, workload-specific
  compute, per-user environments, lifecycle, and isolation choices.
- [Networking](references/networking.md): 6PN, DNS, Flycast, public exposure,
  request routing, Fly-Src authentication, custom networks, and static egress.
- [Data and storage](references/data-storage.md): Managed Postgres, volumes,
  snapshots, Tigris, SQLite/Litestream, Redis selection, and LiteFS.
- [Production](references/production.md): availability, tokens, observability,
  backup/restore review, extensions, and cost checks.
- [Sprites](references/sprites.md): product selection, authentication, exec,
  files, persistence, checkpoints, services, networking, and API/SDK contracts.

Use Fly Launch for conventional image-based apps; use Machines directly when
per-instance lifecycle, image, or sizing control is required. Evaluate Sprites
for persistent mutable execution environments and agent sandboxes. Preserve an
explicit user choice. Choose storage from the workload's durability and recovery
needs, not the deployment tool alone.

## Research opportunities, not just syntax

For architecture, difficult troubleshooting, or optimization, search the
[Fly blog](https://fly.io/blog/), [engineering posts](https://fly.io/infra-log/),
[Sprites blog](https://fly.io/sprites-blog/), [community](https://community.fly.io/),
and [official examples](https://github.com/superfly), alongside current docs.
Look for relevant patterns and failure reports; surface verified opportunities
with their applicability and constraints rather than expanding scope silently.

Check dates and the whole discussion, including author corrections and later
releases. Verify a recommendation against current docs, official source/CLI
behavior, or a disposable reproduction. Attribute retained techniques next to
the advice. Treat a report as a diagnostic lead, not a platform guarantee;
omit unresolved workarounds and experimental claims from recommendations.
When sources conflict, state the conflict and use the narrower confirmed
contract. Do not claim a cloud behavior was tested when only help/docs were read.

## Stay within the task

Reviews and investigations are read-only. `fly launch --no-deploy` still creates
an app; it is not an offline validation command. For authorized changes, carry
out the bounded task and verify the resulting behavior. Ask only when a missing
decision affects the task or an irreversible operation remains uncertain.

Report the recommendation or change, relevant config/commands, evidence, and
remaining operational limits. Load only the references needed for that task.
