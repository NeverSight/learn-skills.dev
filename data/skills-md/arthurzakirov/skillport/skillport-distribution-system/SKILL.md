---
name: skillport-distribution-system
description: Use when packaging, publishing, or updating a public agent-skill repository so it can be installed across machines, repos and harnesses including Codex, Claude Code and OpenCode, using shared local skill storage.
---

# SkillPort Distribution System

## Purpose

Package reusable agent skills once so they can be installed and shared across machines, people, repos and harnesses including Codex, Claude Code and OpenCode, using shared local skill storage.

## Use This Workflow

For a new skill-pack repo:

1. Pick the repo product name, slug, and promise before packaging files.
2. Run `scripts/create-agent-skill-repo.sh` from the SkillPort repo when starting a new skill pack.
3. Inspect generated placeholders, plugin manifests, README, examples, schemas, and setup script.
4. Add or update the real skills.
5. Add the GitHub repo shorthand to a SkillPort manifest, usually `config/skill-repos.local.yaml`.
6. Validate locally with:

```bash
npx skills add /path/to/generated/repo --list
```

7. Push to GitHub.
8. Validate from GitHub:

```bash
npx skills add https://github.com/OWNER/REPO --list
```

For normal cross-machine syncing, use:

```bash
./scripts/skillport-sync.sh
```

This reruns `npx skills add <repo> --skill '*' -a codex -g -y` for every repo listed in the selected manifest, then runs `npx skills update -g -y`.

Keep personal repo lists in ignored local files such as `config/skill-repos.local.yaml`, or pass a separate manifest with `--repos-file`. The public SkillPort repo should only ship a neutral example manifest.

Use the sync script for normal machine setup. Use local symlink scripts only for active local development where live edits should be visible before pushing.

## GitHub Template Rule

GitHub template repositories copy an entire repo. They do not directly template a subdirectory.

Use the generator for normal SkillPort workflows. Create a separate minimal GitHub template repo only if you need the GitHub UI or `gh repo create --template` flow.

## Harness-neutral installation and global rules

Use `npx skills add <repo> --skill '*' -a codex claude-code opencode -g -y` for the configured baseline. Inspect the CLI output and `npx skills ls -g -a codex claude-code opencode`: Codex and OpenCode use `~/.agents/skills` directly; Claude's paths are aliases to that per-OS tree. Never add an editable content copy per harness.

Keep one canonical repository checkout shared by Windows and WSL through Windows paths and `/mnt/c`. Generated installs may remain per OS so each installer can maintain its own paths without disturbing unrelated skills. Other physical devices use separate Git-synced checkouts.

Global rules are separate from skills. Keep one private common layer plus one platform overlay and use `scripts/bootstrap-agent-guidance.py` to atomically render the concrete global Codex `AGENTS.md`. It also configures Claude imports and OpenCode's global JSON `instructions` without duplicating editable rules. The first migration requires comparison and explicit replacement; prior effective content is backed up. See `docs/cross-device-maintenance.md` for preservation and verification steps. Do not assume arbitrary harnesses support the same global path or import syntax.

For unattended refresh, set `SKILLPORT_ROOT` and the cross-tool `PRIVATE_CONTEXT_ROOT`, then use the macOS LaunchAgent installer or native Windows Task Scheduler installer with a private machine configuration. Derive the registry and guidance layers from `PRIVATE_CONTEXT_ROOT`; do not duplicate repository inventories, machine paths, or shell-startup assumptions. macOS runs at login/load and wake-coalesced quarter hours. Windows runs at logon and every 15 minutes with `StartWhenAvailable`; this avoids a fragile audit-policy-dependent unlock-event subscription. Both refresh only registry-selected canonical checkouts, compose the correct platform guidance, and reinstall the explicit remote skill subset. GitHub CLI is optional for these core operations and is used only for live push-visibility verification. Missing or failed metadata skips pushes without blocking refresh. Optional pushes remain registry-scoped and fail closed: private repositories require verified private visibility and credential scans; public repositories also require an exact reviewed-HEAD approval and personal-data scan. The automation never stages or commits files.

When a workflow's instructions and supporting facts belong together, package them as one installable skill with any reference inside its skill directory. Choose public or private visibility through a harm-and-benefit review, sanitize public material, and avoid a cross-repository runtime dependency or a second authoritative sidecar.
