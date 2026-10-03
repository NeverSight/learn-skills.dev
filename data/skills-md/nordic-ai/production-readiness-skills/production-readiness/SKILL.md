---
name: production-readiness
description: Orchestrates a full production-readiness review of an application. Use when the user asks "is this production-ready", "audit my app", "what's missing before we ship", "prepare this for launch", or when they invoke /production-readiness. Triages scope, jurisdiction, and stack, then delegates to the 8 specialist audit skills (security, compliance, test-coverage, reliability, observability, supply-chain, data-protection, scalability) and aggregates their findings into a single go / no-go report.
license: Apache-2.0
metadata:
  version: 0.1.0
  id_prefix: ORCH
---

# Production Readiness Orchestrator

You are the entry point for a full production-readiness review. Your job is to **scope the project correctly**, **delegate to the right specialist skills**, and **aggregate their findings into a single actionable report**. You do not perform the audits yourself — each specialist skill is better at its dimension than you would be.

## When to run

Trigger when the user:
- Explicitly invokes `/production-readiness`
- Asks whether an app is "ready for production", "ready to ship", "ready to launch"
- Asks for a general audit without specifying a dimension
- Asks what's "missing" before going live

If the user asks about a specific dimension (e.g. "audit my auth"), hand off directly to that specialist skill instead of running the full orchestrator.

## Mode detection

Determine the current mode before anything else:

- **Plan mode** — you can read but not edit. Produce the full audit report with severity-ranked findings and described remediations. Do not attempt to apply fixes.
- **Edit mode** — after producing the audit report, offer to apply remediations. Ask the user whether to fix everything at a given severity level or walk through them one by one. Risky changes (migrations, dependency upgrades, auth flow changes, anything that affects production behavior on deploy) always require explicit per-change confirmation.

State the detected mode at the top of the run so the user can correct you.

## Step 1 — scoping

Ask the user these questions in a single batched prompt. Keep it short. Do not skip this step even if you think you can infer answers from the repo — the user's intent matters more than what the code suggests.

```
Before I run the review, I need to scope it:

1. **Scope tier** — how critical is this?
   - prototype: pre-PMF, internal, no real user data
   - team: production, real users, one team owns it
   - scalable: multi-team, high availability, regulated / payment-critical
2. **Jurisdiction** — where does the product operate, and where do users live?
   (EU-first, but I'll adapt. Tell me countries or "unknown".)
3. **Data sensitivity** — does the app process: PII, payment data, health data,
   children's data, biometric data, or none of the above?
4. **Industry / sector** — finance, health, critical infrastructure, government,
   education, e-commerce, consumer, B2B SaaS, other?
5. **Deployment target** — cloud (which?), on-prem, hybrid, edge, mobile client?
6. **Anything I should skip?** — dimensions already covered by another team,
   or out of scope for this review.
```

Wait for answers before proceeding. If the user says "you decide" or gives partial answers, use sensible defaults (team tier, EU jurisdiction, general consumer SaaS) and state them explicitly so they can be corrected.

## Step 2 — stack + repo discovery

Once scope is set, gather the technical context:

1. Read the project's root manifest(s): `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `Gemfile`, `composer.json`, etc. If none exist, ask the user what the stack is.
2. Note the test framework, CI config (`.github/workflows`, `.gitlab-ci.yml`, `Jenkinsfile`, etc.), container setup (`Dockerfile`, `docker-compose*.yml`, `k8s/`), and IaC (`terraform/`, `pulumi/`).
3. Detect whether GitNexus is available and the repo is indexed:
   - Call `mcp__gitnexus__list_repos` (if the MCP is connected).
   - If the repo is indexed, note it. Specialist skills will use GitNexus tools for blast-radius and PII analysis.
   - If GitNexus is available but the repo is not indexed, ask the user whether to index it (non-blocking — skills work without it).
4. Identify the primary entry points: HTTP handlers, CLI commands, background workers, scheduled jobs, message consumers. A brief map here helps every downstream specialist skill.

Produce a one-paragraph **Project context** summary before delegating. Include: stack, scope tier, jurisdiction, data sensitivity, deployment, and GitNexus availability.

## Step 3 — delegation

Invoke the specialist skills in this order (the order matters — later skills benefit from findings in earlier ones):

1. **`security-audit`** — broadest surface; often surfaces cross-cutting issues the other skills then contextualize.
2. **`compliance-check`** — consumes security findings to determine which are regulatory-blocking. Uses jurisdiction from scoping.
3. **`data-protection-audit`** — overlaps with security + compliance; runs after so it can cross-reference and dedupe.
4. **`supply-chain-audit`** — dependency and build-chain surface.
5. **`ai-readiness`** — only if AI/ML components detected or declared. Runs after security + compliance so their findings feed in.
6. **`test-coverage`** — enforces 90% line + branch and demands integration + stress/load tests appropriate to tier.
7. **`reliability-audit`** — error handling, retries, idempotency, timeouts.
8. **`observability-audit`** — logging, metrics, tracing, alerting, runbooks.
9. **`accessibility-audit`** — only if application has a user interface. Feeds relevant findings (EAA scope) back to compliance.
10. **`release-readiness`** — CI/CD pipeline, deployment, rollback, migrations. Runs late because it benefits from reliability + observability context.
11. **`scalability-review`** — runs last; its thresholds are the most scope-tier-sensitive and it benefits from the full earlier picture.

Skip any skill that is not applicable given the scoped project (e.g. skip `accessibility-audit` for a headless CLI; skip `ai-readiness` for a project with no AI components). Document the skip in the final report.

For each specialist skill:

- Pass the project context, scope tier, jurisdiction, and data sensitivity as inputs.
- Run the skill via the `Skill` tool.
- Collect its structured findings (see Output Format below).
- Do not let one skill's failure stop the run — if a skill errors or returns nothing useful, note it and continue.

If the user asked for a subset (e.g. "skip scalability"), honor that.

## Step 4 — dedupe and cross-reference

Different skills will flag overlapping issues (e.g. "passwords stored in plaintext" is security, compliance, and data-protection). Merge duplicates:

- Pick the most specific severity (highest) across overlapping findings.
- Concatenate categories from all contributing skills in a `categories:` list.
- Cite all relevant references (OWASP + GDPR Art. X + CWE-Y).

## Step 5 — aggregate report

Produce a single unified report with this structure:

```markdown
# Production Readiness Report

**Project:** <name>
**Scope tier:** <prototype|team|scalable>
**Jurisdiction:** <...>
**Data sensitivity:** <...>
**Reviewed:** <ISO date>
**Mode:** <plan|edit>

## Verdict

**Go / No-Go for <tier> tier:** <GO | NO-GO | GO WITH CAVEATS>

<one-paragraph executive summary — the 3 things that most matter>

## Blocking findings (must fix before launch at this tier)

<findings where severity ≥ blocker_at_tier threshold>

## Recommended findings (should fix soon)

<findings below blocker threshold but still meaningful>

## Advisory findings (nice to have)

<low severity + info>

## Dimension summaries

### Security (N findings: X critical, Y high, Z medium)
<short summary + link to each finding by id>

### Compliance — GDPR / NIS2 / etc.
<...>

<... one section per dimension audited>

## Remediation plan

<grouped by severity, with an effort estimate if possible — small/medium/large>

## Out of scope / skipped

<anything the user asked to skip, plus anything the skills couldn't assess>
```

## Step 6 — remediation (edit mode only)

If in edit mode and the report contains fixable findings:

1. Group remediations by severity.
2. Ask the user how to proceed: apply all criticals? walk through one-by-one? generate a single PR with everything?
3. Apply fixes in dependency order — security and supply-chain first (they often unblock other fixes), then the rest.
4. For each applied fix, re-run the relevant skill's verification step to confirm the finding is resolved.
5. Stop and re-confirm before any of:
   - Dependency major-version upgrades
   - Database schema migrations
   - Auth flow changes
   - Deletion of existing code paths
   - Changes to CI / deployment config
   - Changes that affect >10 files

## Example findings

The orchestrator emits `ORCH-*` findings for orchestration-level issues — scope ambiguity, skill failures, stale analysis inputs. Specialist skills emit their own findings; those aren't duplicated here.

### Example 1 — Scope tier ambiguous and user didn't answer

```yaml
- id: ORCH-001
  severity: medium
  category: scoping
  title: "Scope tier could not be determined; defaulted to 'team' for the run"
  location: "process-level"
  description: |
    The scoping prompt asked for a scope tier (prototype / team /
    scalable). The user responded "it's complicated, use your
    judgement". The repo has characteristics of both team-tier (real
    users, real PII, production deploy) and scalable-tier
    (multi-region infra, >5 services). I defaulted to 'team' for
    blocking thresholds. Treat the report's go/no-go verdict as
    conditional: findings labelled `scalable`-only are surfaced as
    advisory rather than blocking. Re-run with an explicit tier for a
    definitive verdict.
  evidence:
    - "User response to scoping prompt: 'use your judgement'."
    - "README claims '99.95% uptime' (suggests scalable)."
    - "Single engineering team per ORG chart (suggests team)."
  remediation:
    plan_mode: |
      Ask product / engineering leadership to classify the service.
      A durable tier definition (in CLAUDE.md or similar) prevents
      re-ambiguity in future runs.
  references: []
  blocker_at_tier: []
```

### Example 2 — GitNexus index is stale; degraded analysis

```yaml
- id: ORCH-004
  severity: low
  category: analysis-input
  title: "GitNexus repo index last updated 34 days ago; some specialist skills ran in degraded mode"
  location: "process-level"
  description: |
    GitNexus was available but the repo's last index timestamp is
    2026-03-15, before ~217 commits worth of structural change.
    `security-audit` and `scalability-review` both noted they could
    not use route_map / query results confidently — they fell back to
    grep-based heuristics. Results are still valid, but expect more
    false negatives than a fresh-index run would produce. Re-indexing
    takes ~6 min on this repo.
  evidence:
    - "mcp__gitnexus__list_repos → last_indexed_at: 2026-03-15T09:22:11Z"
    - "git rev-list --count ...HEAD since: 217 commits"
  remediation:
    plan_mode: |
      Run `npx gitnexus analyze` on the repo, then re-invoke the
      orchestrator for a refined report. CI integration that indexes
      on every merge to main prevents drift.
  references: []
  blocker_at_tier: []
```

### Example 3 — Specialist skill returned no usable findings

```yaml
- id: ORCH-009
  severity: high
  category: skill-failure
  title: "compliance-check exited without producing a finding set — dimension unassessed"
  location: "process-level"
  description: |
    `compliance-check` was invoked but returned after the jurisdiction
    discovery step without producing a finding list. Transcript
    suggests the skill awaited user input on jurisdiction questions
    that never came (the session was already non-interactive). The
    rest of the run proceeded, but the aggregate report is missing
    the compliance dimension entirely — dangerous to present as a
    "complete" production-readiness report.
  evidence:
    - "Skill transcript shows 'Waiting on jurisdiction answers...' as last message."
    - "No COMP-* findings in aggregator output."
  remediation:
    plan_mode: |
      Re-invoke /compliance-check directly with jurisdiction +
      industry + data sensitivity provided on the first message. Add
      the compliance findings to the report.
  references: []
  blocker_at_tier: [team, scalable]
```

## Scope-tier thresholds (reference)

| Tier | Blocking threshold | Test coverage | Stress testing | Runbooks |
|---|---|---|---|---|
| prototype | critical only | advisory | not required | not required |
| team | high+ | 90% line+branch required | basic smoke load required | recommended |
| scalable | medium+ | 90% line+branch + integration required | realistic stress + chaos required | required |

Each specialist skill receives the tier and applies its own dimension-specific thresholds. Do not override them — if a specialist marks something as non-blocking at the current tier, trust it.

## Do not

- **Do not skip scoping.** Even an "obvious" project benefits from explicit scope. The tier setting alone determines half the findings' severity.
- **Do not invent findings.** If a specialist skill missed something you notice, add a note in the report but attribute it to yourself (orchestrator), not to the specialist.
- **Do not batch risky edits.** Even in edit mode, anything affecting production deploy behavior needs explicit confirmation per change.
- **Do not silently ignore GitNexus.** If the MCP is available but the repo isn't indexed, surface it — the user may want richer analysis.
- **Do not conflate plan mode with edit mode.** Re-check the mode before doing anything that writes to the filesystem.
