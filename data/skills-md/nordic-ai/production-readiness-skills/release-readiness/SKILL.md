---
name: release-readiness
description: Reviews the path from code commit to running production — CI/CD pipeline quality, deployment strategy (rolling, blue-green, canary), rollback procedures, database migration patterns, feature-flag discipline, environment parity, release versioning, smoke tests after deploy, deployment observability hooks, and change management. Complements supply-chain-audit (build integrity) and reliability-audit (runtime behavior) by focusing on the release event itself. Use when the user asks about "releases", "deployments", "CI/CD", "rollback", "canary", "blue-green", "feature flags", "migrations", invokes /release-readiness, or when the orchestrator delegates. Stack-agnostic, mode-aware, scope-tier-aware.
license: Apache-2.0
metadata:
  version: 0.1.0
  id_prefix: REL-R
---

# Release Readiness Audit

You review whether changes can reach production safely and be reversed safely when they shouldn't. Most production incidents happen *at* or *shortly after* release — release readiness is about making that event boring.

This skill follows the library-wide rules in [`docs/CONVENTIONS.md`](../../docs/CONVENTIONS.md). Read that first.

## Inputs

From orchestrator: `scope_tier`, `stack_summary`, `gitnexus_indexed`, deployment target.

If user invokes directly, gather: CI/CD platform, deployment target (k8s, ECS, serverless, bare VMs, etc.), release cadence, rollback expectations (how fast do incidents need to be reversible).

## Finding ID prefix

`REL-R` — see `CONVENTIONS.md` §4.

## Tier thresholds

| Tier | Automated CI | Automated deploy | Rollback mechanism | Feature flags | Canary/gradual | Migration safety |
|---|---|---|---|---|---|---|
| prototype | tests run | manual OK | documented procedure OK | optional | optional | review required |
| team | **tests + lint + security scans gating** | **automated from main** | **single command / button** | **required** for risky changes | **recommended** | **online-compatible required** |
| scalable | **required + artifact signing** | **required + progressive** | **automatic on SLO burn** | **required + per-segment** | **required** | **required + tested on prod-scale replica** |

## Review surface

### 1. CI pipeline quality

A PR landing on main without green CI is an immediate red flag.

- **Required status checks on main**:
  - Unit tests
  - Lint
  - Type check (where applicable)
  - Build
  - Security scans (cross-reference `supply-chain-audit`, `security-audit`)
  - Skill-specific: e2e tests for user-facing apps, eval regression for AI apps
- **Branch protection** enforces the checks (the checks existing without enforcement is the most common false-sense-of-security pattern).
- **Flaky-test tolerance**: flake rate measured; retries permitted but not infinite. Flaky tests quarantined with an owner and deadline, not ignored.
- **Speed**: CI feedback time measured. Target <10 min to first failure signal at team+ tier; <20 min to full green. Slow CI means skipped CI.
- **Parallelization** used — test sharding, matrix builds.
- **Caching** — dependency cache, build cache, layer cache. Speeds CI without sacrificing correctness.
- **No "emergency skip"** merge button without at least a paper trail and post-merge verification.
- **Secrets in CI** scoped to jobs that need them; not exposed in logs (see `supply-chain-audit`).

### 2. Artifact management

- **Immutable build artifacts** — same artifact promoted from staging to prod; don't rebuild for prod.
- **Artifact storage**: container registry / package registry / S3 — versioned, retention matches rollback window.
- **Digest pinning** — deploy by digest, not by tag (tags are mutable).
- **Artifact signing** at team+ tier (`cosign`, Sigstore, signed npm packages) — ties back to `supply-chain-audit`.
- **Provenance attestation** at scalable tier (SLSA level ≥2).

### 3. Environment parity

- **Dev / staging / prod use the same**:
  - Runtime versions (pinned).
  - Dependencies (same lockfile).
  - Container base images (same digest).
  - Database engine + major version.
  - Managed services (where possible).
- **Differences documented** where parity can't be met (e.g. staging uses a smaller cluster).
- **Config via environment**, not baked into the artifact. Twelve-factor applies.
- **Secrets per environment**, never shared across dev/staging/prod.
- **Staging traffic characteristics** approximate prod at team+ tier; shadow traffic / synthetic load at scalable.
- **Data parity considerations** — staging needs representative *schema + scale*, but anonymized data (see `data-protection-audit`).

### 4. Deployment strategy

By tier:

- **Prototype**: direct deploy acceptable. One-command script.
- **Team**: rolling deploy with readiness probes. No "stop-the-world" restarts. Automated, no shell access required.
- **Scalable**: progressive — canary (1-5% traffic), gradual rollout based on SLO adherence, automatic halt on error budget burn. Blue-green where stateful coordination makes canary hard.

Specific checks:

- Readiness probes correctly configured (see `reliability-audit` §9); deploys wait for probes.
- Startup probes for slow-booting services (Kubernetes 1.18+).
- `maxSurge` / `maxUnavailable` tuned to absorb deployment without capacity drop.
- Old pods/tasks drained gracefully (SIGTERM handling, connection draining).
- Deployment is idempotent — same artifact + same config re-applied = no-op.
- No SSH-and-edit in production; everything through deployment pipeline.

### 5. Rollback

The test of a good release pipeline is: *can you roll back in under 5 minutes, without fear?*

- **Rollback mechanism exists** — GitOps revert, `kubectl rollout undo`, ArgoCD sync to previous, Terraform apply previous, platform-specific (ECS service revision, Lambda version alias).
- **Rollback tested** periodically (not just documented). A rollback procedure that's never been exercised is a tech-debt claim.
- **One-command / one-click** at team+ tier. Cognitive load during an incident is the enemy.
- **Forward-compatible / backward-compatible changes**:
  - DB migrations are backward-compatible (expand / contract — rollout adds, later rollout removes).
  - API changes don't break existing clients for the rollback window.
  - Feature behind a flag so rollback = flag flip, not full redeploy.
- **Rollback window** documented — how long can you still roll back to version N? Governed by schema change compatibility.
- **Rollback observability** — rollback itself is a significant event and should be logged, announced (status page update), and followed by a post-incident review regardless of whether an incident was formally declared.

### 6. Database migrations

Release-readiness applies migration safety heavily.

- **Online migrations** (don't block writes on large tables):
  - Add column: nullable or with safe default (Postgres 11+ handles this well; older versions rewrite the table).
  - Rename column: use expand/contract pattern (add new, backfill, dual-write, switch reads, stop writing old, drop old — across multiple releases).
  - Drop column: remove from code first, wait for deploy stabilization, then drop.
  - Add index on large table: `CREATE INDEX CONCURRENTLY` (Postgres), online index (MySQL 8+), avoid full-table lock.
  - Change column type: expand/contract via a new column.
- **Migration tooling** in use: Flyway, Liquibase, Alembic, Prisma Migrate, Rails migrations, Django migrations, Sequelize, migrate-go, Goose, sqlx-migrate, Atlas. Verify migrations are versioned and ordered.
- **Migrations tested on prod-scale replica** at scalable tier before merge.
- **Migrations idempotent** — re-running doesn't corrupt (most tools handle this via version tracking, but custom SQL can violate).
- **Long-running migrations gated** — don't run a 4-hour migration as part of the deploy step; run separately with monitoring.
- **Rollback path** for every migration explicit. "We never roll back migrations" is a finding — they're rare but sometimes necessary.
- **Data migration vs schema migration** separated — schema changes deploy as code; data migrations (backfills) run as managed jobs with restart capability.

### 7. Feature flags

Feature flags separate deploy from release, which is critical at team+ tier.

- **Feature-flag system** in use: LaunchDarkly, Unleash, Flipper, GrowthBook, Flagsmith, Statsig, or a simple in-house implementation. Not hardcoded `if (FEATURE_X)` constants.
- **Flag types used appropriately**:
  - Release flags — new feature gated until ready. Short-lived.
  - Experiment flags — A/B tests. Medium-lived.
  - Permission flags — per-user / per-tenant enablement. Long-lived.
  - Operational flags / kill switches — for dependencies or non-critical features that can be disabled during incidents. Long-lived.
- **Flag lifecycle**:
  - Every release flag has an owner and a removal date.
  - Flag cleanup tracked (`stale-flags` reports, orphaned flag alerts).
  - Flag debt measured — old flags accumulating are a sign of neglect.
- **Targeting** capability — flag on by user/tenant/region/percentage for progressive rollout.
- **Flag audit log** — who changed what, when. Especially for kill switches.
- **Flag defaults safe** — default off for new behavior, default on for existing behavior.
- **Tests run both paths** for critical flags.

### 8. Release observability

A deploy event is a high-risk signal that should be wired to observability.

- **Deploy markers** in metrics dashboards — correlate deploy events with error rate / latency changes.
- **Automatic error-rate / latency SLI monitoring** for a defined window after deploy (15-30 min typical).
- **Alert routing** during deploys — deploys shouldn't silently raise the error threshold; they should raise sensitivity.
- **Release tag** in error tracker (Sentry, Rollbar) — regressions are attributable to releases.
- **Automatic deploy announcement** to ops channel (#releases, #ops) — human awareness of what just changed.
- **Version endpoint** (`/version`, `/healthz`, `/build-info`) exposes git SHA + build time so on-call can verify what's deployed without logging into the platform.

### 9. Smoke tests and post-deploy verification

- **Smoke test** runs after deploy — a thin slice of integration tests against the new deployment verifying core endpoints work. If smoke fails, automatic rollback at scalable tier.
- **Health checks vs smoke tests** distinguished: health check = "process alive"; smoke test = "critical flow works end-to-end".
- **Synthetic monitoring** at scalable tier — continuous smoke tests running from outside-in against prod, alerting on SLO breach.

### 10. Change management / approval

- **PRs require review** — branch protection enforces at least one approval.
- **Code owners** for critical paths (auth, payments, schema migrations) — automatic reviewer assignment.
- **Change categorization** at scalable tier — normal / standard / emergency — different approval paths.
- **Emergency-change process** documented: who approves, how it's logged, how it's reviewed after.
- **Changes outside CI/CD** logged — kubectl patches, manual database edits, console changes. Any "broke glass" usage audited.

### 11. Release versioning

- **SemVer** for libraries and packages; date-based or SemVer for services depending on convention.
- **Changelog** generated or maintained — what's in this release?
- **Release notes** for user-visible changes (API, UI).
- **Breaking changes** called out with migration path.
- **Tag** a signed release in git at scalable tier.

### 12. Rollout coordination for breaking changes

- **API versioning** (cross-reference `api-design-review` when it exists):
  - Backward-compatible changes preferred.
  - Versioned URLs / headers for incompatible changes.
  - Deprecation window documented and enforced.
- **Client ↔ server coordination** — can the new server handle old clients and vice versa during rollout? At scalable tier, every change is assumed to roll out asymmetrically.
- **Cross-service coordination** — service A depending on service B's new contract deploys *after* service B.

### 13. Release scheduling

- **Merge freezes** before high-impact business periods (peak traffic, regulatory deadlines) documented.
- **Time-of-day** — avoid deploying right before off-hours unless fully on-call coverage is set up.
- **Weekend / holiday deploys** require explicit approval.
- **Multiple concurrent deploys** across services — coordinated or lockstep-deployable.

### 14. Dev ergonomics (affects reliability indirectly)

- **Local dev matches CI matches prod** as closely as reasonable.
- **Bootstrap time** for a new developer to get a working env is manageable (measured in hours, not days).
- **Reproducing production bugs locally** is possible — sample data, recorded traces, test fixtures.

### 15. Infrastructure as code

Cross-reference `iac-review` (future skill). Release-readiness cares about:
- Infra changes reviewed and deployed through the same gates as app code.
- Drift detection — manual console changes surfaced.
- State backed up.

## Category enum (for findings)

- `ci-quality`
- `artifact`
- `environment-parity`
- `deploy-strategy`
- `rollback`
- `migration`
- `feature-flag`
- `release-observability`
- `smoke-test`
- `change-management`
- `versioning`
- `coordination`
- `scheduling`
- `dev-ergonomics`

## Severity guidance

| Level | Examples |
|---|---|
| critical | No way to roll back. Manual steps required for deploy with no documentation. Migrations run with table locks on large tables. Any deploy requires human judgement to execute. |
| high | Rollback untested / multi-step. No feature flags for risky changes. Environment drift between staging and prod. No deploy observability. |
| medium | CI runs but doesn't gate. Flaky tests auto-retried indefinitely. Long-lived feature flags without cleanup process. |
| low | Nice-to-have: SLSA attestation, tag signing, synthetic monitoring. |
| info | Observation on cadence / practice. |

## Example findings

### Example 1 — No automated rollback; rollback requires manual redeploy from prior tag

```yaml
- id: REL-R-002
  severity: critical
  category: rollback
  title: "Rollback is manual: re-tag and re-run the full build/deploy pipeline (~25 min)"
  location: "process-level"
  description: |
    The deploy pipeline builds a Docker image on merge to main, tags it
    `:latest`, and runs `kubectl set image`. There's no version-tagged
    registry entry, no GitOps revert target, and no one-command rollback.
    Rolling back requires: revert PR → wait for CI build (~15 min) → wait
    for deploy (~8 min) → verify. During an incident, that's 20-30
    minutes of degraded service minimum. The last two incidents recorded
    in `docs/post-mortems/` both had rollback-time >30 min as a
    contributing factor to user-visible impact.
  evidence:
    - |
      # .github/workflows/deploy.yml — tags as :latest
      - run: docker tag app:${{ github.sha }} ghcr.io/org/app:latest
      - run: docker push ghcr.io/org/app:latest
      - run: kubectl set image deploy/app app=ghcr.io/org/app:latest
    - "docs/runbooks/rollback.md does not exist."
    - "docs/post-mortems/2026-02-fraud-false-positives.md cites 27 min rollback."
  remediation:
    plan_mode: |
      1. Tag images by git SHA (not :latest). Retain prior image in
         registry for the rollback window.
      2. Store manifests in git (GitOps via ArgoCD / Flux) so rollback is
         `git revert` of the manifest commit — triggers automatic sync.
      3. Add a documented one-command rollback (`make rollback` or equiv).
      4. Rehearse a rollback every quarter during game day.
  references:
    - "Google SRE Workbook — Release Engineering"
  blocker_at_tier: [team, scalable]
```

### Example 2 — Migration adds NOT NULL column without default to a 40M-row table

```yaml
- id: REL-R-009
  severity: high
  category: migration
  title: "Migration 0042 will block writes for ~18 min on production table"
  location: "db/migrations/0042_add_tenant_id.sql"
  description: |
    The migration adds a `tenant_id UUID NOT NULL` column to `events` (40M
    rows on prod, benchmarked from staging-scaled-replica). In Postgres
    15 this requires a full table rewrite holding an ACCESS EXCLUSIVE
    lock, estimated ~18 minutes based on staging. During that window, no
    reads or writes succeed. Staging lacks realistic row count and so the
    issue wasn't surfaced in normal testing.
  evidence:
    - |
      -- db/migrations/0042_add_tenant_id.sql
      ALTER TABLE events ADD COLUMN tenant_id UUID NOT NULL;
    - "prod events table: 40,118,000 rows, 14 GB"
  remediation:
    plan_mode: |
      Multi-release expand-contract:
      1. Release N: Add `tenant_id UUID NULL` (nullable). No rewrite.
      2. Release N+1: Start writing tenant_id in application code for all
         new rows; background backfill for old rows (chunked, with
         progress tracking + restart capability).
      3. Release N+2: After backfill completes and verifies (no NULL),
         add NOT NULL constraint via `NOT VALID` + `VALIDATE CONSTRAINT`
         (avoids full lock).
      Test the backfill job on a production-scale replica first.
    edit_mode: |
      Proposed: replace migration 0042 with three migrations across three
      releases; add backfill script. Significant scope — requires
      explicit confirmation and coordination with the data team.
  references:
    - "Strong Migrations (github.com/ankane/strong_migrations)"
    - "Postgres docs — ALTER TABLE locking semantics"
  blocker_at_tier: [team, scalable]
```

### Example 3 — Feature flags accumulate without cleanup; one from 18 months ago still live

```yaml
- id: REL-R-015
  severity: medium
  category: feature-flag
  title: "Flag debt: 47 flags in codebase, 12 older than 12 months"
  location: "src/flags.ts"
  description: |
    The flag registry at `src/flags.ts` lists 47 active flags. Per git
    blame, 12 were introduced >12 months ago. Manual inspection shows at
    least 3 are dead code paths (the "on" branch has been 100% traffic
    for ~8 months). Flag debt compounds: each flag adds branching, test
    combinations, and cognitive load, and stale flags can be accidentally
    flipped with unpredictable effect. No documented cleanup process
    exists; no owner or removal date is associated with any flag.
  evidence:
    - |
      // src/flags.ts — flag 'new_checkout_flow' defined 2025-03-12,
      // still conditional in 14 files, 100% rollout confirmed via
      // LaunchDarkly since 2025-08-01.
  remediation:
    plan_mode: |
      1. Adopt a flag lifecycle policy: each flag declaration must have
         an `owner:` and `removal_by:` field.
      2. Add a CI lint that fails when a flag is older than its removal
         date.
      3. Retire the 12 stale flags across the next two release cycles:
         remove conditional, delete flag from LaunchDarkly, update tests.
      4. Surface flag inventory in the release dashboard.
  references:
    - "Feature Toggles (martinfowler.com)"
  blocker_at_tier: [team, scalable]
```

### Example 4 — No post-deploy smoke test; deploys complete with pods in a crash loop undetected for minutes

```yaml
- id: REL-R-021
  severity: high
  category: smoke-test
  title: "Deploy marks success based on readiness-probe alone; no post-deploy verification"
  location: ".github/workflows/deploy.yml:64"
  description: |
    The deploy job runs `kubectl rollout status` and exits on success.
    But the readiness probe at `/health` is a liveness-equivalent check
    (process alive, not dependencies reachable). In the last incident
    (see `docs/post-mortems/2026-03-02`), a config change broke the
    upstream payments API connection; pods passed readiness and served
    500s for 7 minutes before monitoring alerts fired. A smoke test
    exercising `POST /checkout` would have caught this pre-cutover.
  evidence:
    - |
      # .github/workflows/deploy.yml:64
      - run: kubectl rollout status deploy/app --timeout=300s
      # no post-deploy smoke run
    - "docs/post-mortems/2026-03-02-checkout-500s.md"
  remediation:
    plan_mode: |
      1. Add a post-deploy smoke-test job that runs 5-10 critical
         integration checks against the new deployment (not against a
         mock): signup, login, list primary resource, create primary
         resource, call payments happy path.
      2. On smoke failure: automatic `kubectl rollout undo` at scalable
         tier, pager at team tier, halt progressive rollout.
      3. Wire smoke-test results to the deploy dashboard.
      4. Add synthetic monitoring running the same suite every 5 min in
         prod (independent of deploys).
    edit_mode: |
      Proposed: add `smoke-test` job calling existing `tests/smoke/`
      suite against the deployed URL. Requires adding a run token and
      production smoke credentials — coordination with security.
  references:
    - "Google SRE Workbook — Canarying Releases"
  blocker_at_tier: [team, scalable]
```

## Dimension summary template

```markdown
## Release Readiness Summary

CI provider: <...>
Deploy target: <...>
Deploy strategy: <rolling | blue-green | canary | manual>
Rollback mechanism: <one-command | manual | none>
Rollback last exercised: <date or never>
Feature-flag system: <...>
Active flags: <count>, stale (>90d): <count>
Migration tooling: <...>
Release cadence: <per day / per week / per sprint / ad-hoc>

Findings: <N critical, N high, N medium, N low, N info>
Top 3 release risks:
  1. ...
  2. ...
  3. ...

Not assessed: <list with reasons>
```

## Edit-mode remediation guidance

Safe:
- Adding deploy markers to metrics / error tracker.
- Adding a `/version` endpoint exposing git SHA.
- Adding flag lifecycle metadata to the flag registry.
- Adding post-deploy smoke test scaffolds (config for existing test suite).
- Documenting rollback procedure (when a procedure effectively exists but isn't written down).

Require confirmation:
- Changing deploy strategy (rolling → canary, etc.).
- Adopting GitOps / new deploy tooling (significant scope).
- Refactoring migrations into expand/contract pattern (touches releases).
- Enabling branch protection / required-checks (affects contributor workflow).
- Introducing feature-flag system where none exists (new dependency + process).
- Changing CI gating rules that currently pass.

## Skill-specific do-nots

- Do not approve "we can deploy weekly and that's fine" at a scalable tier without verifying rollback and feature-flag discipline — low frequency + slow rollback is the highest-risk combination.
- Do not confuse "automated deploy" with "safe deploy". A fully-automated pipeline pushing breaking changes to prod in 90 seconds is still dangerous without observability and rollback.
- Do not accept "we don't do rollbacks; we roll forward" as a complete answer. Roll-forward can be the default, but a roll-back path still needs to exist for the worst cases.
- Do not treat CI green as proof of release readiness. CI proves the code can *build and pass tests*; release readiness is about what happens at and after deploy.
- Do not advocate adding canaries / blue-green to prototype-tier apps — complexity before it's needed.
- Do not leave flag debt un-addressed. Stale flags are a quiet source of bugs and a cognitive load tax.
