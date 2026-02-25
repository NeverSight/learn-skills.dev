---
name: eve-repo-upkeep
description: Keep Eve-compatible repos aligned with platform best practices and current manifest conventions.
---

# Eve Repo Upkeep

Keep an app repo current with Eve conventions. The checks are independent — run them in parallel when multiple areas need attention.

## When to Use

- After Eve platform updates or manifest schema changes
- Before a major deploy or release
- When onboarding a new maintainer

## Phase 1: Assess

Quickly determine which areas need attention. Check which of these files exist and whether they look stale — don't deep-read every file, just note which areas need work:

- `.eve/manifest.yaml` — does it exist? Is the schema line `eve/compose/v1`?
- `skills.txt` — does it exist? Are there pinned or obsolete entries?
- `AGENTS.md` / `CLAUDE.md` — do they reference current skills?
- `agents/` directory — do `agents.yaml`, `teams.yaml`, `chat.yaml` exist?
- Codebase — any obvious deprecated CLI patterns or inline secrets?

If only one area needs work, handle it directly. Otherwise, proceed to Phase 2.

## Phase 2: Dispatch Workers

Create one worker per area that needs updating. Each worker description below is self-contained — a worker can execute its area independently without context from the others.

### Worker: Manifest Alignment

Check and fix `.eve/manifest.yaml`:

- Ensure `schema: eve/compose/v1` is present.
- Prefer `services:` over legacy `components:`.
- Keep `x-eve` ingress and pipeline definitions accurate.
- Keep `x-eve.defaults` in sync with harness defaults (harness/profile/options).
- Keep `x-eve.agents` profiles aligned with orchestration policy.
- Ensure `x-eve.agents.config_path` and `x-eve.chat.config_path` point to valid files.
- Confirm `${secret.KEY}` usage for secrets.
- Deploy pipelines should include a `build` step before `release`.
- Services with Docker images should have `build.context` defined.
- Registry auth secrets (`REGISTRY_USERNAME` + `REGISTRY_PASSWORD`) are required only for custom BYO registries.

### Worker: Skills File

Check and fix `skills.txt`:

- Keep Eve skillpack references up to date.
- Remove obsolete packs or pinned versions.

### Worker: Agent Instructions

Check and fix `AGENTS.md`, `CLAUDE.md`, and `agents/` config files:

- Update skill references to include `eve-se-index`.
- Remove stale commands or URLs.
- `agents/agents.yaml` defines agents and skills — verify entries are current.
- `agents/teams.yaml` defines team composition and dispatch — verify structure.
- `agents/chat.yaml` defines chat routing rules and permissions — verify rules.

### Worker: Deprecated Patterns

Search the codebase for deprecated patterns and fix or flag them:

- Old CLI commands (`eve deploy` vs `eve env deploy`)
- Old deploy syntax without `--ref` parameter
- Hardcoded domains in docs or manifests
- Inline secrets in repo files
- Dockerfiles missing `org.opencontainers.image.source` label pointing to the repo URL
- Pipelines missing `build` step before `release`
- Services with Docker images but no `build.context` configuration
- Missing registry authentication secrets for custom registries (`REGISTRY_USERNAME`, `REGISTRY_PASSWORD` or provider-equivalent names)

## Phase 3: Verify

After all workers complete, run final verification:

```bash
# Local validation (Docker Compose)
docker compose up --build

# Staging deploy (requires --ref with 40-char SHA or a ref resolved against --repo-dir)
eve env deploy staging --ref main --repo-dir .

# Use --direct to bypass pipeline if needed
eve env deploy staging --ref main --repo-dir . --direct
```

Track the deploy job with `eve job follow`.
