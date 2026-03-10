---
name: linear-release-setup
description: Generate CI/CD configuration for Linear Release. Use when setting up
  release tracking, configuring CI pipelines for Linear, or integrating deployments
  with Linear releases. Supports GitHub Actions, GitLab CI, CircleCI, and other platforms.
---

# Linear Release Setup

## Interactive Workflow

### Step 1: Preflight

Before generating config, confirm:

1. **Pipeline exists in Linear** — the user must have created a release pipeline in Linear first (Settings → Releases). Each pipeline has its own access key.
2. **Detect CI platform** — look for `.github/workflows/*.yml` (GitHub Actions), `.gitlab-ci.yml` (GitLab CI), `.circleci/config.yml` (CircleCI), or other CI config.
3. **Detect default branch** — check `git symbolic-ref refs/remotes/origin/HEAD` or the CI config. Don't assume `main`.

### Step 2: Ask the user

Gather the following information (skip questions you can infer from the codebase):

1. **CI platform** — if not auto-detected
2. **Pipeline type** — continuous (every deploy = a completed release) or scheduled (releases collect changes over time, then move through stages)
3. **Monorepo?** — if the repo has multiple apps/services, ask which paths to track (e.g. `apps/web/**`)

For scheduled pipelines, always ask these explicitly (don't infer — they significantly affect the generated config):

4. **Branch model** — just `main`, or `main` + release branches (e.g. `release/*`)?
5. **Release versioning** — calendar-based (e.g. `2026.05`), semver (e.g. `1.2.0`), or default (commit SHA)? Where does the version come from — branch name, CI variable, file, git tag?
6. **Release stages** — what stages before completion (e.g. "code freeze", "qa")?
7. **Automation level** — all manual (via workflow_dispatch), or some automated (e.g. branch creation → code freeze)?

### Step 3: Generate the CI configuration

Select the right example template, read it, adapt it (branch patterns, stage names, paths, version format), and add it to an existing workflow or create a new one.

| Platform       | Pipeline Type | Example                                                                                                                      |
| -------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| GitHub Actions | Continuous    | [`github-actions-continuous.yml`](https://github.com/linear/linear-release/blob/main/examples/github-actions-continuous.yml) |
| GitHub Actions | Scheduled     | [`github-actions-scheduled.yml`](https://github.com/linear/linear-release/blob/main/examples/github-actions-scheduled.yml)   |
| GitLab CI      | Continuous    | [`gitlab-ci-continuous.yml`](https://github.com/linear/linear-release/blob/main/examples/gitlab-ci-continuous.yml)           |
| GitLab CI      | Scheduled     | [`gitlab-ci-scheduled.yml`](https://github.com/linear/linear-release/blob/main/examples/gitlab-ci-scheduled.yml)             |
| CircleCI       | Continuous    | [`circleci-continuous.yml`](https://github.com/linear/linear-release/blob/main/examples/circleci-continuous.yml)             |
| CircleCI       | Scheduled     | [`circleci-scheduled.yml`](https://github.com/linear/linear-release/blob/main/examples/circleci-scheduled.yml)               |

For GitHub Actions, prefer the official action (`linear/linear-release-action@v0`). For other platforms, download the CLI binary and refer to the [README](https://github.com/linear/linear-release#commands) for the full command reference:

```bash
curl -sL https://github.com/linear/linear-release/releases/latest/download/linear-release-linux-x64 -o linear-release
chmod +x linear-release
```

Each scheduled example includes a **monorepo** note in the header explaining how to split workflows for path filtering per platform.

### Step 4: Remind about secrets

Tell the user to add the `LINEAR_ACCESS_KEY` secret to their CI environment:

- **GitHub Actions**: Repository Settings → Secrets and variables → Actions → New repository secret
- **GitLab CI**: Settings → CI/CD → Variables
- **CircleCI**: Project Settings → Environment Variables

The access key is created in Linear from the pipeline's settings page. Each pipeline has its own access key.

## Key Concepts

### Pipelines

A **release pipeline** in Linear represents a deployment lane — e.g. "iOS", "Android", "Web". Each product or environment you ship independently should be its own pipeline. Don't confuse this with CI pipelines — a Linear pipeline is the release tracking unit, and your CI config calls the CLI to update it.

### Pipeline Types

**Continuous**: Every deploy creates a completed release. One `sync` call on push.

**Scheduled**: An ongoing release collects changes, then moves through stages before completion. Three commands:

- `sync` — adds issues from new commits to the current release
- `update --stage=<stage>` — moves the release to a stage (e.g. "code freeze")
- `complete` — marks the release as shipped

The typical scheduled flow uses **release branches**: `main` collects changes, a `release/*` branch is cut for stabilization, and branch creation auto-promotes to a stage. Version is derived from the branch name (e.g. `release/1.2.0` → `1.2.0`). On `main`, `sync` runs without `--release-version` so issues land on the current started release. On release branches, `sync` runs with `--release-version` to target the specific release.

### Stages

Stages are phases a scheduled release moves through — e.g. "code freeze", "in review", "qa". They represent process steps, not environments. Different environments (staging, production) should be separate pipelines.

Stages can be **frozen** in Linear. A frozen stage makes `sync` (without `--release-version`) skip that release and target the next one — a safety net for code freezes.

### Commands

| Command    | Purpose                            | Key flags                                        |
| ---------- | ---------------------------------- | ------------------------------------------------ |
| `sync`     | Create/update release from commits | `--name`, `--release-version`, `--include-paths` |
| `update`   | Move release to a stage            | `--stage` (required), `--release-version`        |
| `complete` | Mark release as complete           | `--release-version`                              |

### GitHub Action Inputs

When using `linear/linear-release-action@v0`, inputs map to CLI flags as follows:

| CLI flag             | Action input                         |
| -------------------- | ------------------------------------ |
| (command positional) | `command`                            |
| `--name`             | `name`                               |
| `--release-version`  | `version` (alias: `release_version`) |
| `--stage`            | `stage`                              |
| `--include-paths`    | `include_paths`                      |

### Path Filtering (Monorepos)

Path filters can be configured in Linear's pipeline settings or via the CLI's `--include-paths` flag (CLI takes precedence if both are set). If the user has already configured paths in Linear, the CLI flag is optional.

For **monorepos with release branches**, CI platforms often can't path-filter differently per branch. The solution is two workflow/job definitions: `main` with path filtering, release branches without. Each scheduled example includes platform-specific instructions.

### Requirements

- **Full git history**: `fetch-depth: 0` or equivalent — shallow clones miss commits between releases.
- **`LINEAR_ACCESS_KEY`**: Per-pipeline access key from Linear, stored as a CI secret.

### Checklist

- [ ] Full clone / `fetch-depth: 0`
- [ ] `LINEAR_ACCESS_KEY` set as a secret (one per pipeline)
- [ ] Correct binary platform (`linux-x64`, `darwin-arm64`, or `darwin-x64`)
- [ ] Triggers on the correct branches (`main` for continuous; `main` + `release/*` for scheduled)
- [ ] Monorepo: path filters set (in Linear config or via `--include-paths`), and separate workflows if using release branches
