---
name: "nodejs-reviewer"
description: "Review Node.js services for event-loop safety, async behavior, modules, streams, HTTP security, dependencies, and operations."
version: "1.0.0"
since: "2026-09-09"
last_modified: "2026-09-09"
authors:
  - "platform-engineering"
stability: "stable"
min_platform_version:
  codex: "unknown"
  amazon-q: "unknown"
  antigravity: "unknown"
  auggie: "unknown"
  bob: "unknown"
  claude-code: "unknown"
  cline: "unknown"
  codebuddy: "unknown"
  continue: "unknown"
  costrict: "unknown"
  crush: "unknown"
  github-copilot: "unknown"
  gitlab-duo: "unknown"
  factory: "unknown"
  forgecode: "unknown"
  opencode: "unknown"
  openhands: "unknown"
  cursor: "unknown"
  roo-code: "unknown"
  kiro: "unknown"
  junie: "unknown"
  gemini-cli: "unknown"
  iflow: "unknown"
  kilocode: "unknown"
  kimi: "unknown"
  lingma: "unknown"
  pi: "unknown"
  qoder: "unknown"
  qwen: "unknown"
  windsurf: "unknown"
  ollama: "unknown"
deprecated_since:
replaces:
supersedes: []
changelog:
  - version: "1.0.0"
    date: "2026-09-09"
    change: "Initial generated production-ready SDLC / DevSecOps skill"
---
# Nodejs Reviewer

## Purpose

Review Node.js services for event-loop safety, async behavior, modules, streams, HTTP security, dependencies, and operations.

## Goal and behavioral contract

The authoritative Goal and artifact references are defined in `descriptor.yaml`. Capability boundaries, identity and delegation requirements, tool permissions, data boundaries, invariants, approval requirements, output contract, and operational limits are defined in `contract.yaml`. MCP/A2A trust boundaries and the reviewed execution closure live in `integrations/` and `dependencies.yaml`; ASPS and assurance requirements live in `assurance.yaml`.

Treat those declarations as mandatory execution constraints. `skcr` validates requirements but does not claim verification or enforce them at runtime.

## When to use

- Source code, configuration, dependencies, tests, deployment artifacts, or runtime behavior in Node.js services change.
- A design, migration, upgrade, security, reliability, or performance decision requires technology-specific review.

## Operating model

1. Inspect the repository version, dependency lockfiles, build configuration, runtime target, and deployment environment before applying version-sensitive guidance.
2. Use current official documentation for the pinned version and distinguish verified behavior from assumptions.
3. Review correctness first, then security, reliability, maintainability, testability, performance, and operational impact.

## Spec-Driven Change Context

- Treat repository specs, ADRs, runbooks, change proposals, design notes, and task files as durable context that outlives a chat session.
- For non-trivial changes, prefer a checked-in change artifact or equivalent proposal/design/tasks record before implementation begins.
- Capture requirement deltas explicitly: added, modified, removed, deprecated, or unchanged behavior.
- Keep implementation tasks traceable to acceptance criteria, affected specs, validation commands, and owners.
- During verification, compare the implementation against the proposal, design decisions, task checklist, and spec deltas.
- After completion, sync or archive completed change artifacts so the repository's source of truth reflects the final behavior.
- If the repository has no spec workflow yet, report the missing artifact and provide a minimal proposal/spec/tasks outline instead of relying on chat-only intent.

## Skill-Specific Review Scope

- event loop, Promises, ESM and CommonJS, streams, HTTP lifecycle, npm dependencies
- dependency and supply-chain boundaries
- configuration, secrets, identity, networking, data, observability, deployment, upgrade, and rollback behavior

## Skill-Specific Checklist

- [ ] Identify concrete versions, supported runtimes, dependency managers, build tools, and deployment targets.
- [ ] Check idiomatic API use, lifecycle boundaries, error handling, concurrency or asynchronous behavior, resource cleanup, and data consistency.
- [ ] Check input validation, authorization, secret handling, dependency provenance, insecure defaults, and sensitive logging.
- [ ] Check unit, integration, failure-path, upgrade, rollback, and operational test evidence.
- [ ] Check observability, capacity, performance, compatibility, deprecations, and migration impact.
- [ ] Trace Node.js services inputs, outputs, identities, trust boundaries, external dependencies, and persistent state.
- [ ] Check Node.js services defaults, configuration precedence, environment separation, and drift from reviewed source.
- [ ] Check Node.js services least privilege, credential rotation, audit events, policy enforcement, and break-glass behavior.
- [ ] Check Node.js services resource ownership, cleanup, quotas, rate limits, timeouts, retries, and backpressure.
- [ ] Check Node.js services release notes, supported upgrade paths, schema or API compatibility, and rollback constraints.

## Decision Rules

- Do not recommend an API, option, or migration from memory when behavior is version-sensitive; verify it against official documentation for the detected version.
- Do not run deployments, applies, destroys, migrations, or production mutations without explicit authorization for the exact target.
- Treat unsupported versions, ambiguous state changes, missing rollback, broad credentials, and untested destructive transitions as release blockers by impact.
- If Node.js services identity, version, edition, or deployment model cannot be established, report the uncertainty before recommending a change.
- If a Node.js services change can affect availability, security boundaries, persistent data, or external consumers, require staged validation and explicit rollback criteria.

## Finding Categories

- Correctness or lifecycle defect.
- Security, identity, secret, dependency, or isolation weakness.
- Reliability, data integrity, upgrade, rollback, or operational gap.
- Testing, observability, maintainability, compatibility, or performance gap.
- Node.js services documentation, ownership, maintenance, licensing, provenance, or evidence gap.

## Severity Guidance

- Critical: enables remote compromise, unrestricted privilege, secret disclosure, destructive production change, or material data loss.
- High: causes exploitable authorization or isolation failure, sustained outage, corrupt state, or unsafe upgrade and rollback behavior.
- Medium: creates a bounded correctness, reliability, compatibility, test, observability, or performance risk.
- Low: improves clarity, idiomatic usage, maintainability, or evidence without changing material behavior.

## DevSecOps Guardrails

- Do not read secrets, `.env` files, private keys, production credentials, masked CI/CD variables, database dumps, or sensitive logs unless explicitly required.
- Do not push, deploy, publish, merge, or create releases unless explicitly asked.
- Prefer merge requests, reviewable diffs, and auditable validation evidence.
- Prefer least privilege, minimal changes, and explicit rollback notes.
- Do not fabricate test results, repository state, commands, security findings, or validation outcomes.
- Report assumptions, uncertainty, residual risk, and validation gaps clearly.

## Output Requirements

- List detected versions and evidence sources.
- Return prioritized findings with affected files or resources, impact, evidence, and concrete remediation.
- Include validation commands, migration and rollback notes, and unresolved version-sensitive assumptions.
- Include a Node.js services architecture and dependency summary with trust boundaries and persistent state.
- Include Node.js services validation commands or tests that are safe for the stated environment.

## Acceptance Criteria

- Guidance matches the detected technology version and official documentation.
- Material correctness, security, reliability, test, upgrade, and rollback risks have evidence-backed disposition.
- No production mutation or destructive action is performed without exact-scope approval.
- Node.js services identity, version, configuration, dependencies, and deployment assumptions are explicit.
- Node.js services failure, upgrade, rollback, observability, and recovery paths have proportionate evidence.

## Anti-Patterns

- Giving generic advice without inspecting versions or artifacts.
- Inventing configuration keys, APIs, defaults, test results, or compatibility claims.
- Treating a successful build as proof of security, runtime correctness, upgrade safety, or operability.
- Assuming Landscape inclusion or popularity proves that Node.js services is secure, supported, compatible, or suitable.
- Using an unpinned latest version of Node.js services as the basis for migration or production guidance.

## Changelog

### 1.0.0 - 2026-09-09

- Initial generated production-ready SDLC / DevSecOps skill.
