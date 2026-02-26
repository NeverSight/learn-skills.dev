---
name: upgrade-pegasus
description: Upgrade to the latest version of SaaS Pegasus. Use when the user mentions 'upgrade pegasus,' or 'pegasus upgrade.'
---

# Upgrading Pegasus

## Instructions

This skill helps users upgrade their SaaS Pegasus codebase.

Use the `pegasus-cli` to trigger the upgrade. It can be called via the `pegasus` command in the project's python environment.

You first need to list the user's project and find the right one.

```
pegasus projects list
```

You should be able to compare the project names to what's defined `pegasus-config.yaml` to find the right id.

You may need to prompt the user to authenticate first. If necessary, do that via the CLI (`pegasus auth`).

### Before pushing

1. **Ensure main is up to date**: Run `git checkout main && git pull` before starting the upgrade. The merge will be against main, so it must have the latest changes.

### Pushing

Use the CLI flags to avoid interactive prompts:

```
# Upgrade to latest stable version (non-interactive):
pegasus projects push <project_id> --upgrade

# Upgrade to latest dev version (non-interactive):
pegasus projects push <project_id> --dev
```

**Important**: Always pass `--upgrade` or `--dev` to avoid interactive prompts that require stdin.
Without these flags, the CLI will show an interactive menu that doesn't work well in non-interactive environments.

If the user doesn't specify stable vs dev, default to `--upgrade` (stable).

### After the push completes

1. Run `git fetch origin` to see the new branch
2. The branch name will be in the format `pegasus-<version>-<timestamp>` (e.g. `pegasus-2026.2.1.3-1771252378.779356`)
3. `git checkout <branch-name>` to switch to it (it will already be up to date from the push)
4. Merge the user's default branch (usually `main`) into the upgrade branch using your "resolve pegasus conflicts" skill
