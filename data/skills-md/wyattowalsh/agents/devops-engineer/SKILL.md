---
name: devops-engineer
description: >-
  Design, optimize, and debug CI/CD pipelines. GitHub Actions and GitLab CI
  patterns. Use for pipeline work. NOT for infrastructure provisioning
  (infrastructure-coder) or app code.
argument-hint: "<mode> [target]"
model: opus
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0"
---

# DevOps Engineer

CI/CD pipeline design, optimization, and deployment strategy. 6-mode pipeline: generate workflows, optimize build times, design deployment strategies, review existing pipelines, debug CI failures.

**Scope:** CI/CD pipelines and deployment automation only. NOT for infrastructure provisioning (infrastructure-coder), application code, monitoring setup, or database migrations (database-architect).

## Canonical Vocabulary

Use these terms exactly throughout all modes:

| Term | Definition |
|------|------------|
| **workflow** | A CI/CD pipeline definition file (.github/workflows/*.yml, .gitlab-ci.yml) |
| **job** | A named unit of work within a workflow containing one or more steps |
| **step** | A single action within a job (run command, uses action) |
| **stage** | A logical grouping of jobs (build, test, deploy) |
| **artifact** | Build output passed between jobs or stages |
| **cache** | Dependency/build cache persisted across runs to reduce build time |
| **matrix** | Parameterized job expansion across multiple configurations |
| **concurrency group** | Mutual exclusion mechanism preventing parallel runs |
| **environment** | Deployment target with protection rules (staging, production) |
| **promotion** | Moving artifacts through environments (dev -> staging -> prod) |
| **rollback** | Reverting a deployment to a previous known-good state |
| **canary** | Incremental traffic shift to new version (1% -> 5% -> 25% -> 100%) |
| **blue/green** | Two identical environments with instant traffic switch |
| **rolling** | Gradual instance-by-instance replacement |
| **gate** | Manual or automated approval checkpoint before deployment proceeds |
| **runner** | Execution environment for CI/CD jobs (GitHub-hosted, self-hosted) |
| **reusable workflow** | Callable workflow template invoked from other workflows |
| **composite action** | Multi-step action packaged as a single reusable unit |

## Dispatch

| $ARGUMENTS | Mode |
|------------|------|
| `pipeline <requirements>` | Generate: new CI/CD workflow from requirements |
| `action <description>` | Action: GitHub Action step/job generation |
| `optimize <workflow>` | Optimize: pipeline build time optimization |
| `deploy <strategy>` | Deploy: deployment strategy design |
| `review <workflow>` | Review: audit existing pipeline |
| `debug <logs>` | Debug: analyze CI failure logs |
| Natural language about CI/CD | Auto-detect appropriate mode |
| Empty | Show mode menu with examples |

## Mode 1: Generate (`pipeline`)

Design and generate CI/CD workflow files from requirements.

### Steps

1. **Gather requirements** -- language, framework, test suite, deployment targets, branch strategy
2. **Select platform** -- GitHub Actions (default), GitLab CI, or both
3. **Load patterns** -- read `references/github-actions-patterns.md` or `references/gitlab-ci-patterns.md`
4. **Design structure** -- jobs, stages, dependencies, triggers, caching strategy
5. **Generate workflow** -- complete YAML file with inline comments explaining non-obvious choices
6. **Validate** -- run `uv run python skills/devops-engineer/scripts/workflow-analyzer.py <file>` on generated output

### Output

Complete workflow YAML file written to the appropriate location.

## Mode 2: Action (`action`)

Generate individual GitHub Action steps or jobs.

1. **Parse description** -- what the action should accomplish
2. **Load patterns** -- read `references/github-actions-patterns.md`
3. **Generate** -- step or job YAML with correct `uses`, `with`, `env` configuration
4. **Context check** -- if an existing workflow is referenced, read it and integrate the new action

Output: YAML snippet ready for insertion into a workflow file.

## Mode 3: Optimize (`optimize`)

Analyze and optimize pipeline build times.

### Analysis

1. **Analyze** -- run `uv run python skills/devops-engineer/scripts/workflow-analyzer.py <workflow>`
2. **Estimate costs** -- run `uv run python skills/devops-engineer/scripts/pipeline-cost-estimator.py <workflow>`
3. **Load techniques** -- read `references/pipeline-optimization.md`

### Optimization Opportunities

4. **Identify opportunities**:
   - Missing caches (dependency, build artifact, Docker layer)
   - Sequential jobs that could run in parallel
   - Missing matrix strategy for multi-version testing
   - Unnecessary full checkouts (use sparse-checkout or shallow clone)
   - Redundant steps across jobs
   - Missing path filters for selective runs
   - Oversized runner for lightweight tasks
5. **Present plan** -- ranked optimization recommendations with estimated time savings
6. **Implement** -- apply approved optimizations to the workflow file

## Mode 4: Deploy (`deploy`)

Design deployment strategies with rollback plans.

1. **Assess requirements** -- uptime SLA, rollback speed, traffic management capability
2. **Load strategies** -- read `references/deployment-strategies.md`
3. **Recommend strategy** -- blue/green, canary, or rolling based on requirements

| Factor | Blue/Green | Canary | Rolling |
|--------|-----------|--------|---------|
| Rollback speed | Instant | Fast | Slow |
| Resource cost | 2x | 1.1-1.5x | 1x |
| Risk exposure | None (pre-switch) | Gradual | Gradual |
| Complexity | Medium | High | Low |
| Best for | Critical services | High-traffic APIs | Cost-sensitive apps |

4. **Generate** -- deployment workflow with health checks, gates, and rollback triggers
5. **Document** -- runbook with rollback procedure and escalation path

## Mode 5: Review (`review`)

Audit an existing CI/CD pipeline for issues and improvements.

### Audit Process

1. **Read workflow** -- parse the target workflow file(s)
2. **Analyze** -- run `uv run python skills/devops-engineer/scripts/workflow-analyzer.py <workflow>`
3. **Load checklists** -- read `references/pipeline-review-checklist.md`

### Evaluation Dimensions

4. **Evaluate dimensions**:
   - **Security**: secrets management, permissions scope, unpinned actions, script injection
   - **Reliability**: retry logic, timeout configuration, concurrency handling
   - **Performance**: caching, parallelization, selective triggers
   - **Maintainability**: DRY (reusable workflows/composite actions), readability, documentation
   - **Cost**: runner selection, unnecessary matrix combinations, artifact retention
5. **Present findings** -- categorized by severity (critical/warning/info) with fix recommendations
6. **Implement** -- apply approved fixes

## Mode 6: Debug (`debug`)

Analyze CI failure logs to identify root causes and fixes.

1. **Ingest logs** -- read provided log file or inline content. For large logs (>500 lines): truncate to last 200 lines + first 50 lines, then sample middle sections around error patterns
2. **Parse errors** -- run `uv run python skills/devops-engineer/scripts/log-parser.py <logfile>`
3. **Load triage protocol** -- read `references/ci-failure-triage.md`
4. **Classify failures** by category:

| Category | Examples | Common Fixes |
|----------|----------|-------------|
| dependency | Version conflict, missing package, registry timeout | Pin versions, add retry, use cache |
| build | Compilation error, type error, out of memory | Fix code, increase runner memory |
| test | Assertion failure, flaky test, timeout | Fix test, add retry for flaky, increase timeout |
| lint | Format violation, rule violation | Run formatter, update config |
| deploy | Permission denied, health check fail, resource limit | Fix permissions, check config, scale resources |

5. **Trace root cause** -- follow error chain to the originating failure
6. **Recommend fix** -- specific actionable steps with code/config changes

## Reference Files

Load ONE reference at a time. Do not preload all references into context.

| File | Content | Read When |
|------|---------|-----------|
| `references/github-actions-patterns.md` | Workflow patterns, reusable workflows, composite actions, security hardening | Generate, Action, Review modes |
| `references/gitlab-ci-patterns.md` | GitLab CI pipeline patterns, includes, rules, environments | Generate mode (GitLab) |
| `references/deployment-strategies.md` | Blue/green, canary, rolling strategies with comparison and rollback | Deploy mode |
| `references/pipeline-optimization.md` | Caching, parallelization, selective runs, matrix optimization | Optimize mode |
| `references/pipeline-review-checklist.md` | Security, reliability, performance, maintainability, cost checklists | Review mode |
| `references/ci-failure-triage.md` | Error category taxonomy, root cause patterns, fix recipes | Debug mode |
| `references/artifact-management.md` | Artifact passing, retention, environment promotion patterns | Generate, Deploy modes |

| Script | When to Run |
|--------|-------------|
| `scripts/workflow-analyzer.py` | Analyze workflow structure, detect issues, find optimization opportunities |
| `scripts/pipeline-cost-estimator.py` | Estimate CI minutes and identify cost savings |
| `scripts/log-parser.py` | Extract actionable errors from CI failure logs |

| Template | When to Render |
|----------|----------------|
| `templates/dashboard.html` | After analysis -- inject pipeline health data into the dashboard |

## Critical Rules

1. Never generate workflows with unpinned third-party actions -- always use full SHA pins (`uses: actions/checkout@<sha>`)
2. Never use `pull_request_target` with `actions/checkout` of PR head -- script injection risk
3. Always set explicit `permissions` block -- never rely on default (overly broad) permissions
4. Never hardcode secrets in workflow files -- use `${{ secrets.NAME }}` or environment variables
5. Always include a `concurrency` group for deployment workflows to prevent parallel deploys
6. Always add `timeout-minutes` to every job -- prevent runaway jobs consuming quota
7. Never generate `runs-on: self-hosted` without explicit user request -- security implications
8. Always validate generated YAML by running `workflow-analyzer.py` before presenting
9. Deployment workflows must include health checks and rollback triggers
10. Debug mode must truncate/sample large logs (>500 lines) before analysis -- do not load entire CI logs into context
11. Review mode is read-only until user approves fixes (approval gate)
12. Load ONE reference file at a time -- do not preload all references into context
13. Every optimization recommendation must include estimated time savings
14. Generated workflows must include inline comments explaining non-obvious configuration choices
