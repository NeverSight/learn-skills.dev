---
name: github-docker-action
description: Create Docker container actions for GitHub Actions with Dockerfile, action.yml metadata, and entrypoint scripts. Use when building custom GitHub Actions with Docker, scaffolding container-based actions, or debugging Docker action workflows.
license: MIT
metadata:
  author: kjanat
  version: "1.0"
---

# GitHub Docker Container Action

Build, package, and test custom GitHub Actions using Docker containers.

> **Not what you need?** For running sidecar services (Redis, PostgreSQL, etc.)
> in CI workflows, see the `github-service-containers` skill.

## Prerequisites

- Repository on GitHub (public, internal, or private)
- Basic understanding of GitHub Actions and Docker
- Self-hosted runners must run Linux with Docker installed

> **Security**: Always treat workflow inputs as untrusted. Avoid script injection
> via `${{ }}` in `run:` blocks.

## Workflow: Creating a Docker Action

### Step 1: Create project structure

```tree
my-action/
├── Dockerfile
├── action.yml
├── entrypoint.sh
└── README.md
```

### Step 2: Write Dockerfile

See [dockerfile-patterns.md](references/dockerfile-patterns.md)

Minimal:

```dockerfile
FROM alpine:3.21
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

### Step 3: Define action metadata

See [action-metadata.md](references/action-metadata.md)

Declare inputs, outputs, and Docker configuration in `action.yml`.

### Step 4: Write entrypoint script

See [entrypoint-scripts.md](references/entrypoint-scripts.md)

Script receives inputs as positional args. Write outputs to `$GITHUB_OUTPUT`.

### Step 5: Make entrypoint executable

```sh
git add entrypoint.sh
git update-index --chmod=+x entrypoint.sh
```

Verify: `git ls-files --stage entrypoint.sh` should show `100755`.

### Step 6: Tag and push

```sh
git add action.yml entrypoint.sh Dockerfile README.md
git commit -m "Initial action release"
git tag -a -m "v1 release" v1
git push --follow-tags
```

### Step 7: Test in a workflow

See [workflow-testing.md](references/workflow-testing.md)

## Quick Reference

| Component       | Purpose                                   |
| --------------- | ----------------------------------------- |
| `Dockerfile`    | Container image definition                |
| `action.yml`    | Action metadata (inputs, outputs, runner) |
| `entrypoint.sh` | Code executed when container starts       |
| `README.md`     | Usage docs for action consumers           |

### Key environment variables

| Variable            | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| `$GITHUB_OUTPUT`    | File to write output key=value pairs                         |
| `$GITHUB_WORKSPACE` | Repo checkout dir (maps to `/github/workspace` in container) |
| `$GITHUB_ENV`       | File to set env vars for later steps                         |

### Container filesystem mapping

The runner maps `GITHUB_WORKSPACE` to `/github/workspace` in the container.
Files written there are available to subsequent workflow steps.

## Reading Order

| Task                     | Files to Read                                  |
| ------------------------ | ---------------------------------------------- |
| Scaffold new action      | SKILL.md (this file)                           |
| Dockerfile questions     | dockerfile-patterns.md                         |
| Configure inputs/outputs | action-metadata.md                             |
| Write entrypoint logic   | entrypoint-scripts.md                          |
| Test in workflow         | workflow-testing.md                            |
| Debug container issues   | dockerfile-patterns.md + entrypoint-scripts.md |

## In This Reference

| File                                                        | Purpose                          |
| ----------------------------------------------------------- | -------------------------------- |
| [dockerfile-patterns.md](references/dockerfile-patterns.md) | Dockerfile templates and gotchas |
| [action-metadata.md](references/action-metadata.md)         | action.yml spec and examples     |
| [entrypoint-scripts.md](references/entrypoint-scripts.md)   | Entrypoint, outputs, permissions |
| [workflow-testing.md](references/workflow-testing.md)       | Workflow YAML for public/private |
