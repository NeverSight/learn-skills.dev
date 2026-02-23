---
name: github-actions
description: >
  GitHub Actions workflow authoring for CI/CD pipelines. Covers workflow syntax,
  triggers, jobs, steps, matrix strategies, caching, artifacts, reusable workflows,
  composite actions, secrets management, OIDC authentication, and permissions hardening.

  Use when creating workflows, configuring jobs, setting up caching, or automating releases.
  Use for github-actions, workflow, ci, cd, actions, jobs, steps, matrix, cache, artifact,
  secrets, reusable-workflow.
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://docs.github.com/en/actions'
---

# GitHub Actions

## Overview

GitHub Actions is a CI/CD platform that automates build, test, and deployment pipelines directly from GitHub repositories. Workflows are YAML files in `.github/workflows/` triggered by events like pushes, pull requests, schedules, or manual dispatch. Each workflow contains one or more jobs that run on GitHub-hosted or self-hosted runners.

**When to use:** Automated testing, continuous deployment, release automation, scheduled tasks, multi-platform builds, dependency updates, container publishing, code quality checks, security scanning.

**When NOT to use:** Long-running services (use a proper hosting platform), heavy compute tasks exceeding runner limits (6-hour job timeout), tasks requiring persistent state between runs (use external storage), real-time event processing (use webhooks with a server).

## Quick Reference

| Pattern             | Syntax / Action                                  | Key Points                                  |
| ------------------- | ------------------------------------------------ | ------------------------------------------- |
| Push trigger        | `on: push: branches: [main]`                     | Filter by branch, path, or tag              |
| PR trigger          | `on: pull_request: types: [opened, synchronize]` | Defaults to opened, synchronize, reopened   |
| Scheduled trigger   | `on: schedule: - cron: '0 6 * * 1'`              | UTC only, minimum 5-minute interval         |
| Manual trigger      | `on: workflow_dispatch: inputs:`                 | Define typed inputs for manual runs         |
| Job dependencies    | `needs: [build, test]`                           | Run jobs in sequence or parallel            |
| Conditional job     | `if: github.ref == 'refs/heads/main'`            | Expression-based job/step filtering         |
| Matrix strategy     | `strategy: matrix: node: [18, 20, 22]`           | Generates jobs for each combination         |
| Dependency cache    | `actions/cache@v4`                               | Hash-based keys with restore-keys fallback  |
| Setup with cache    | `actions/setup-node@v4` with `cache: 'pnpm'`     | Built-in caching for package managers       |
| Upload artifact     | `actions/upload-artifact@v4`                     | Share data between jobs or preserve outputs |
| Download artifact   | `actions/download-artifact@v4`                   | Retrieve artifacts from earlier jobs        |
| Reusable workflow   | `uses: ./.github/workflows/reusable.yml`         | Called with `workflow_call` trigger         |
| Composite action    | `action.yml` with `using: composite`             | Bundle multiple steps into one action       |
| Concurrency         | `concurrency: group: ${{ github.ref }}`          | Cancel or queue duplicate runs              |
| Environment secrets | `${{ secrets.API_KEY }}`                         | Scoped to repo, org, or environment         |
| OIDC authentication | `permissions: id-token: write`                   | Short-lived tokens for cloud providers      |
| Step outputs        | `echo "key=value" >> "$GITHUB_OUTPUT"`           | Pass data between steps and jobs            |
| Service containers  | `services: postgres: image: postgres:16`         | Sidecar containers for integration tests    |
| Timeout             | `timeout-minutes: 30`                            | Fail fast on hung jobs or steps             |
| Attestations        | `actions/attest-build-provenance@v3`             | SLSA build provenance for supply chain      |

## Expressions and Contexts

| Context   | Example                         | Description                               |
| --------- | ------------------------------- | ----------------------------------------- |
| `github`  | `github.ref_name`, `github.sha` | Event metadata, repo info, actor          |
| `env`     | `env.NODE_ENV`                  | Environment variables at current scope    |
| `secrets` | `secrets.API_KEY`               | Encrypted secrets (masked in logs)        |
| `inputs`  | `inputs.environment`            | Workflow dispatch or reusable inputs      |
| `matrix`  | `matrix.node`                   | Current matrix combination values         |
| `steps`   | `steps.build.outputs.version`   | Outputs from previous steps               |
| `needs`   | `needs.prepare.outputs.tag`     | Outputs from dependent jobs               |
| `runner`  | `runner.os`, `runner.arch`      | Runner environment info                   |
| `vars`    | `vars.DEPLOY_URL`               | Repository or org configuration variables |

## Common Mistakes

| Mistake                                      | Correct Pattern                                                            |
| -------------------------------------------- | -------------------------------------------------------------------------- |
| Using `actions/checkout@v4` or older tags    | Pin to current major version (`@v6`) or commit SHA                         |
| Missing `persist-credentials: false`         | Set on checkout when using custom tokens or OIDC                           |
| Broad `permissions` at workflow level        | Set `permissions: {}` at workflow level, grant per-job                     |
| Cache key without dependency file hash       | Include `hashFiles('**/pnpm-lock.yaml')` in cache key                      |
| Secrets in `if:` conditions                  | Secrets cannot be used in `if:` expressions directly                       |
| Using `pull_request_target` carelessly       | Never run PR code with write permissions from `pull_request_target`        |
| Not cancelling stale runs                    | Use `concurrency` with `cancel-in-progress: true`                          |
| Storing structured data as a single secret   | Create individual secrets per value for proper log redaction               |
| Referencing action tags without SHA pinning  | Pin third-party actions to full commit SHA for supply chain safety         |
| Hardcoding runner OS in scripts              | Use `runner.os` context for cross-platform compatibility                   |
| Using `actions/cache` without `restore-keys` | Always provide restore-keys for partial cache matches                      |
| Interpolating user input in `run:` blocks    | Pass untrusted values through `env:` to prevent script injection           |
| No `timeout-minutes` on jobs                 | Set explicit timeouts to fail fast on hung processes                       |
| Using `always()` without scoping             | Combine with status checks: `if: always() && steps.x.outcome == 'success'` |

## Delegation

- **Workflow debugging**: Use `Explore` agent to inspect workflow run logs
- **Security auditing**: Use `Task` agent to review permissions and secret usage
- **Code review**: Delegate to `code-reviewer` agent for workflow PR reviews

## References

- [Workflow syntax, triggers, jobs, steps, and concurrency](references/workflow-syntax.md)
- [Caching strategies and artifact management](references/caching-and-artifacts.md)
- [Matrix strategies, reusable workflows, and composite actions](references/matrix-and-reusable.md)
- [Security, secrets, OIDC, and permissions hardening](references/security-and-secrets.md)
