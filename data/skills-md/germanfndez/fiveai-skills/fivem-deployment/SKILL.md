---
name: fivem-deployment
description: "Trigger: server artifacts, FXServer, txAdmin, server.cfg, gamebuild, sv_enforceGameBuild, update server, deploy, EOL, recommended build. Pick, pin and deploy a supported FXServer build."
license: MIT
metadata:
  author: germanfndez
  version: "1.0.0"
---

# FiveM Deployment

Choosing an FXServer artifact, keeping it inside its support window, and writing a server.cfg that starts.

## Activation Contract

Load this skill when the user asks which artifact to run, how to update FXServer or txAdmin, why clients cannot connect after an update, what `sv_enforceGameBuild` should be, or how to write or audit `server.cfg`.

## Hard Rules

- Never state a build number from memory. Read `recommended` and `latest` from the changelogs API before answering.
- Ignore the `critical` and `optional` fields. They are stale-pinned to build 7290 and are not maintained.
- EOL is rolling and per build. A build that works today can expire next week; check `support_policy_eol` for the exact build in use.
- `sv_replaceExeToSwitchBuilds` is deprecated as of build 35245. Never emit it.
- On Enhanced, `sv_enforceGameBuild` accepts only `1` (base game, no DLC); numeric build values are Legacy-only.
- `sv_enforceGameBuild` can only be set at startup, never at runtime.
- Never recommend `sv_scriptHookAllowed true`. It makes the server vulnerable.
- Resource load order in `server.cfg` is literal: dependencies must be `ensure`d before dependents.

## Decision Gates

| Situation | Build to pick |
|---|---|
| Production server | `recommended` from the API |
| Testing a new game DLC | `latest` |
| Currently below 35245 | Upgrade to 35245 or later before October 15 2026 |
| Build's `support_policy_eol` date has passed | Upgrade now; it is out of support |

| Symptom | Read |
|---|---|
| Clients cannot join after an update | rules/compatibility-window.md |
| Choosing or verifying a build | rules/artifacts.md |
| Server will not start / bad convar | rules/server-cfg.md |
| Updating artifacts in place | rules/txadmin.md |

## Execution Steps

1. Fetch the lifecycle JSON for the platform (`linux` or `win32`) and read `recommended`, `latest`, `support_policy`, `support_policy_eol`.
2. Compare the user's current build against `recommended` and against its own `support_policy_eol` entry.
3. If the current build is older than 35245, flag the October 15 2026 compatibility cutoff.
4. Set `sv_enforceGameBuild` per the Legacy/Enhanced rule above, or omit it to take the default.
5. Audit `server.cfg` against rules/server-cfg.md before deploying.
6. Restate the build number, its EOL value, and the source URL in the answer.

## Output Contract

Return the chosen build number, its EOL timestamp, and the API URL you read it from. Emit `server.cfg` lines as runnable `cfg` blocks with `ensure` order intact. Never invent a build number, convar, or txAdmin menu path.

## References

- rules/artifacts.md — changelogs API, recommended vs latest, rolling EOL, picking a build.
- rules/compatibility-window.md — October 15 2026 cutoff, upgrade path, deprecations.
- rules/server-cfg.md — server.cfg essentials, gamebuild, security convars.
- rules/txadmin.md — txAdmin's role in artifact updates and version pairing.

Upstream docs: https://docs.fivem.net/docs/server-manual/setting-up-a-server/
