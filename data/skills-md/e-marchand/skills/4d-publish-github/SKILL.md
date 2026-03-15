---
name: 4d-publish-github
description: Publish a 4D project to GitHub using gh CLI. Use this skill when the user wants to publish, push, or share a 4D project to GitHub. Creates remote repository, initializes git, adds CI/CD workflows for building and releasing. Supports release-on-tag or release-on-create workflows.
license: Apache 2.0
---

# 4D Publish to GitHub

Publish a 4D project to GitHub with CI/CD workflows.

## Scripts

Two scripts available, both support interactive and non-interactive modes.

### 1. publish.py - Publish to GitHub

Creates GitHub repository from 4D project.

**Interactive mode:**
```bash
python3 "<skill_path>/scripts/publish.py"
```

**Non-interactive mode (with arguments):**
```bash
python3 "<skill_path>/scripts/publish.py" --yes [options]
```

| Argument | Description |
|----------|-------------|
| `--yes`, `-y` | Non-interactive mode |
| `--public` | Create public repository (default: private) |
| `--description "..."`, `-d` | Repository description |

**Examples:**
```bash
# Interactive
python3 publish.py

# Private repo, no questions
python3 publish.py --yes

# Public repo with description
python3 publish.py --yes --public --description "My 4D component"
```

### 2. install_workflows.py - Add CI/CD Workflows

Installs build and release workflows.

**Interactive mode:**
```bash
python3 "<skill_path>/scripts/install_workflows.py"
```

**Non-interactive mode (with arguments):**
```bash
python3 "<skill_path>/scripts/install_workflows.py" --yes [options]
```

| Argument | Description |
|----------|-------------|
| `--yes`, `-y` | Non-interactive mode |
| `--build` | Install build.yml |
| `--release-on-tag` | Install release workflow (triggered on tag push) |
| `--release-on-create` | Install release workflow (triggered on manual release) |
| `--no-push` | Don't commit and push changes |

**Examples:**
```bash
# Interactive
python3 install_workflows.py

# Build workflow only
python3 install_workflows.py --yes --build

# Build + auto-release on tag
python3 install_workflows.py --yes --build --release-on-tag

# Release on manual create only
python3 install_workflows.py --yes --release-on-create
```

## Creating Releases

### With release-on-tag workflow

```bash
git tag v1.0.0
git push origin v1.0.0
```

### With release-on-create workflow

1. Go to repository → Releases → Create new release
2. Fill release details and publish
3. Workflow builds and attaches `.zip` to the release
