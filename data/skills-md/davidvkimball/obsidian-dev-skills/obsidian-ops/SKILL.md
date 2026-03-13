---
name: obsidian-ops
description: Operations, syncing, versioning, and release management for Obsidian projects. Load when running builds, syncing references, bumping versions, or preparing for release.
---

# Obsidian Operations Skill

This skill covers the operational aspects of maintaining an Obsidian project, including build workflows, sync procedures, and release management.

## Purpose

To ensure reliable builds, consistent reference materials, and safe release processes while strictly following project policies.

## Scope

This skill covers:
- Build and lint workflows
- Syncing reference documentation from external sources
- Version management and release preparation
- Build and environment troubleshooting

## Core Rules

- **NEVER perform automatic git operations**: AI agents must never execute `git commit`, `git push`, or any command that automatically stages or commits changes without explicit user approval for each step.
- **Verify Build**: Always run a build/lint after significant changes to ensure compatibility.
- **Sync Status**: Keep `sync-status.json` updated when updating reference materials.

## Bundled Resources

- `references/build-workflow.md`: Standard build and development commands.
- `references/release-readiness.md`: Checklist for ensuring a project is ready for release.
- `references/sync-procedure.md`: How to pull updates from reference repositories.
- `references/versioning-releases.md`: Workflow for versioning and GitHub releases.
- `references/troubleshooting.md`: Common issues and their resolutions.
- `references/quick-reference.md`: One-page cheat sheet for common operations.
