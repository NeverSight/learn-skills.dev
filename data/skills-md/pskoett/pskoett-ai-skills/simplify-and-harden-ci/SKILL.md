---
name: simplify-and-harden-ci
description: "CI-only Simplify & Harden workflow for pull requests using gh-aw (GitHub Agentic Workflows). Runs headless scan-and-report checks for simplify/harden/document, posts structured findings, and can block merges on critical or advisory classes. Use when: you want automated quality/security review in CI without interactive approvals."
---

# Simplify & Harden CI

## Install

```bash
npx skills add pskoett/pskoett-ai-skills/simplify-and-harden-ci
```

## Purpose

Run a CI-only variant of Simplify & Harden in pull requests:

- No code mutation in CI
- Review only changed files
- Emit structured findings
- Optionally block merge based on severity gates

Use `simplify-and-harden` for interactive/local coding sessions.

## Context Limitation (Important)

CI agents do **not** have the same peak implementation context as the coding
agent that wrote the change. Treat CI findings as structured review signals,
not as full intent-aware rewrites.

Implications:
- Prefer scan/report and merge gating
- Do not auto-apply code changes in CI
- Escalate ambiguous findings to interactive review

## Prerequisites

1. GitHub Actions enabled for the repository
2. GitHub CLI authenticated (`gh auth status`)
3. `gh-aw` installed locally for authoring/validation:

```bash
gh extension install github/gh-aw
```

4. In GitHub Actions jobs, install the CLI with:

```yaml
- uses: github/gh-aw/actions/setup-cli@main
  with:
    version: v0.2.0-beta
```

## CI Contract

The CI skill must enforce:

1. Scope lock: review only files changed in the PR
2. Headless execution: report findings, do not apply patches/refactors
3. Structured output: emit `simplify_and_harden` summary payload
4. Gate policy:
   - `critical`: fail check when critical harden findings exist
   - `advisory` (optional): fail check when advisory findings are configured to block

## Authoring Workflow (gh-aw)

Example-only template lives in `references/workflow-example.md`.
Keep it outside `.github/workflows` until you explicitly want automation enabled.

When ready to enable:
1. Copy `references/workflow-example.md` template block into `.github/workflows/simplify-and-harden-ci.md`.
2. Compile and validate workflow:

```bash
gh aw compile --validate --strict
```

3. Trigger and push workflow changes:

```bash
gh aw run simplify-and-harden-ci --push
```

4. Check status/logs in GitHub Actions and ensure PR feedback is posted.

## Prompt Template (CI)

Use this prompt body in your gh-aw workflow:

```text
Run Simplify & Harden in CI (headless mode) for this pull request.

Rules:
1) Review only files changed in this PR.
2) Do not modify repository files.
3) Before reporting findings, re-read all changed code with "fresh eyes" and actively look for obvious bugs, errors, confusing logic, brittle assumptions, naming issues, and missed hardening opportunities.
4) Simplify pass: detect dead code, naming clarity issues, control-flow complexity, unnecessary API surface, and over-abstraction.
5) Harden pass: detect input-validation gaps, injection vectors, auth/authz issues, secret exposure, data leaks, and concurrency risks.
6) Document pass: suggest non-obvious rationale comments as findings (do not edit files).
7) Emit structured YAML under key `simplify_and_harden`, including:
   - simplify findings
   - harden findings (critical/advisory split)
   - summary counts
   - `review_followup_required`
   - learning loop candidates for self-improvement ingestion
8) If blocking policy is enabled and matching findings exist, mark the run as failed.
```

## Recommended Outputs

1. PR comment with concise findings and severity ordering
2. Check run summary with pass/fail reason
3. Machine-readable YAML artifact for downstream automation

## Integration with Self-Improvement

Forward `simplify_and_harden.learning_loop.candidates` into
`.learnings/LEARNINGS.md` via the `self-improvement` workflow so recurrent
patterns can be promoted into durable agent context rules.
