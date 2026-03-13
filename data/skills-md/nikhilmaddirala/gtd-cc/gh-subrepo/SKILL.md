---
name: gh-subrepo
description: Stateful bidirectional sync for subtree directories using git-subrepo. Sync monorepo subdirs with standalone GitHub repos and graduate projects from lab to production.
---

# gh-subrepo

## Overview

This skill manages standalone repositories from inside monorepo subdirectories using `git-subrepo`.

It is designed for the write/write topology where:

- You work in `40-code/41-subtrees/<name>` inside the monorepo
- Collaborators work directly in standalone GitHub repositories

`git-subrepo` reduces custom sync logic by tracking per-subdir sync metadata in `.gitrepo` files.

## Sub-skills

You must load the appropriate sub-skill from `sub-skills/` based on user intent.

- `sub-skills/subrepo-status.md`
  - Diagnose subrepo setup and sync health
  - Triggers: subrepo status, check subrepos, subrepo health

- `sub-skills/sync.md`
  - Pull and push changes for an existing subrepo
  - Triggers: sync, pull from remote, push to remote, subrepo pull, subrepo push

- `sub-skills/graduate.md`
  - Move a lab project into `41-subtrees/` and initialize it as a subrepo
  - Triggers: graduate, move to production, publish new project

## Process

- Determine user intent
- Load the matching sub-skill
- Execute the sub-skill process
- Verify expected outcome

## Resources

- `scripts/subrepo-status.sh`: lightweight status helper for `41-subtrees/`
- `sub-skills/`: workflow-specific instructions

## Conventions

- Every directory in `40-code/41-subtrees/` is a candidate project
- Note: Active subrepos during migration may be in `40-code/415-subrepos/`
- A project is subrepo-managed when `<subdir>/.gitrepo` exists
- Remote naming should still follow `remote-<dirname>` for compatibility with existing tooling
- Keep the main branch index unstaged on monorepo `main`
- Get user approval before pushing to remotes
