---
name: skillmd-cli-skill
description: Use @skillmarkdown/cli to scaffold, validate, publish, discover, install, and operate full v1 skill lifecycle workflows with deterministic command sequences.
compatibility: "Requires Node.js 18+, npm, filesystem write access, and network access for registry/auth operations."
metadata:
  author: "skillmarkdown"
  version: "1.1.2"
license: MIT
---

## Scope

This skill covers end-to-end usage of `@skillmarkdown/cli` for v1 lifecycle operations:
- authoring and validation (`init`, `validate`)
- authentication and identity (`login`, `logout`, `whoami`, `token`)
- publish and release operations (`publish`, `tag`, `deprecate`, `unpublish`)
- discovery (`search`, `view`, `history`)
- consumption and maintenance (`use`, `install`, `list`, `remove`, `update`)
- workspace dependency intent (`skills.json`) and resolved state (`skills-lock.json`)

This skill does not implement backend APIs, CI pipelines, or interactive shell UX.

## When to use

Use this skill when a user asks to:
- scaffold or harden a `SKILL.md` package structure
- run `skillmd` command flows in development or production registries
- diagnose publish/install/update issues with deterministic remediations
- manage dist-tags, deprecations, unpublish events, or token lifecycle operations
- verify v1 command contracts and expected outputs from the CLI

## Inputs

Required inputs:
- working directory of the skill project
- intended registry environment (`development` or `production`)

Optional inputs:
- target version (semver)
- dist-tag (`latest`, `beta`, or custom non-semver tag)
- publish access (`public` or `private`)
- skill identifier (`@owner/skill`)
- agent target (`skillmd`, `claude`, `gemini`, `custom:<slug>`)

Assumptions:
- strict validation is expected prior to publish
- auth precedence is `--auth-token` > `SKILLMD_AUTH_TOKEN` > login session
- token scopes are applied as `read`, `publish`, `admin`

## Outputs

Produce:
- exact commands executed
- concise result summary (success/failure + reason)
- next deterministic command to continue or remediate

For automation flows, prefer `--json` output whenever supported.

## Steps / Procedure

1. Identify intent, registry environment, and whether the flow is one-off (`use`) or workspace-driven (`install`).
2. For authoring flows:
- `skillmd init [--template <minimal|verbose>] [--no-validate]`
- `skillmd validate [path] [--strict] [--parity]`
3. For auth/setup flows:
- `skillmd login [--status|--reauth]`
- `skillmd whoami [--json]`
- `skillmd token ls|add|rm ...`
4. For publish/release flows:
- `skillmd publish [path] --version <semver> [--tag <dist-tag>] [--access <public|private>] [--provenance] [--agent-target <target>] [--dry-run] [--json]`
- `skillmd tag ls|add|rm ...`
- `skillmd deprecate <skill-id>@<version|range> --message "<text>" [--json]`
- `skillmd unpublish <skill-id>@<version> [--json]`
5. For discovery flows:
- `skillmd search [query] [--limit <1-50>] [--cursor <token>] [--scope <public|private>] [--json]`
- `skillmd view <skill-id|index> [--json]`
- `skillmd history <skill-id> [--limit <1-50>] [--cursor <token>] [--json]`
6. For consumption flows:
- one-off install: `skillmd use <skill-id> [--version <semver> | --spec <tag|version|range>] [--agent-target <target>] [--json]`
- workspace install: `skillmd install [--prune] [--agent-target <target>] [--json]`
- inspect installed skills: `skillmd list [--agent-target <target>] [--json]`
- remove installed skill: `skillmd remove <skill-id> [--agent-target <target>] [--json]`
- maintenance: `skillmd update [skill-id ...] [--all] [--agent-target <target>] [--json]`
7. On failure, report exact CLI error and map to one deterministic remediation step (auth, selector/tag correction, lockfile recovery, or retry).

See [the reference guide](references/REFERENCE.md) for canonical command matrix, workflow checklists, and troubleshooting.

## Examples

Example A: scaffold and parity-check
- Input: "Create a new verbose skill for incident summaries"
- Output:
  - `skillmd init --template verbose`
  - `skillmd validate --strict --parity`

Example B: publish private beta with provenance
- Input: "Publish version 1.2.0-beta.1 privately under beta"
- Output:
  - `skillmd publish --version 1.2.0-beta.1 --tag beta --access private --provenance`

Example C: one-off install by selector
- Input: "Use @owner/skill from beta"
- Output:
  - `skillmd use @owner/skill --spec beta`

Example D: workspace install with pruning
- Input: "Install everything declared in skills.json and remove stale installs"
- Output:
  - `skillmd install --prune`

Example E: add publish token for CI
- Input: "Create a 30-day publish token"
- Output:
  - `skillmd token add ci-publish --scope publish --days 30 --json`

## Limitations / Failure modes

- Publish and release writes fail without valid auth and sufficient scope (`publish` or `admin`).
- `use`/`install`/`update` can fail when `selectorSpec` or referenced dist-tags do not resolve.
- `skills-lock.json` schema corruption blocks install/update flows until repaired or regenerated.
- project/registry mismatch can make existing auth/session appear valid but unusable for target operations.
- Registry/network outages block remote read/write commands.

## Security / Tool access

- Never print or persist auth tokens in logs/output.
- Treat signed download URLs as sensitive and short-lived.
- Prefer `--json` for automation pipelines that parse outputs.
- Keep private skill operations authenticated and scoped to owner access only.
