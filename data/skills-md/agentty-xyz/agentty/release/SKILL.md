---
name: release
description: Guide for releasing a new version of the project, including version bumping, changelog updates, and tagging.
---

# Release Workflow

This skill guides you through the process of releasing a new version of the project.

## Workflow

1. **Preparation**

   - Ensure the git working directory is clean: `git status`.
   - Pull the latest changes: `git pull origin main`.

1. **Version Selection**

   - Always ask the user which version bump to apply: `major`, `minor`, or `patch`.
   - Do not update versions until the user confirms one of these options.

1. **Version Bump**

   - Update the `version` field in the root `Cargo.toml`.
   - Verify `Cargo.lock` is updated (e.g., run `cargo check` to trigger update).

1. **Verification**

   - Run tests: `cargo test -q`.

1. **Documentation Review**

   - Check if agent models, keybindings, or session states changed since the last release:
     `git diff <previous_tag>..HEAD -- crates/agentty/src/domain/agent.rs crates/agentty/src/domain/session.rs crates/agentty/src/ui/state/help_action.rs`
   - If any of those files changed, verify the corresponding doc pages are up to date:
     - `docs/site/content/docs/agents/backends.md` — agent backends and models.
     - `docs/site/content/docs/usage/workflow.md` — session lifecycle and workflow.
     - `docs/site/content/docs/usage/keybindings.md` — keybindings.
   - Run `zola check --root docs/site` to verify no broken internal links.

1. **Changelog**

   - Update `CHANGELOG.md`.
   - Ensure there is an entry for the new version with the current date: `## [vX.Y.Z] - YYYY-MM-DD`.
   - Ensure content adheres to [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
   - Add a `### Contributors` section under the new release entry with a bullet list of GitHub usernames (example: `- @minev-dev`).
   - Build the contributor list from commits since the previous tag and deduplicate names.

1. **Contributors**

   - Generate the contributor username list from commit emails between tags:
     `git log <previous_tag>..HEAD --format='%ae' | sed -nE 's/.*\\+([^@]+)@users\\.noreply\\.github\\.com/\\1/p' | sort -u | sed 's/^/- @/'`
   - If a contributor does not use a GitHub noreply email, map them manually to their GitHub username.

1. **Commit**

   - Stage changes: `git add Cargo.toml Cargo.lock CHANGELOG.md`.
   - Commit with message: `git commit -m "Release vX.Y.Z"`.

1. **Tagging**

   - Create a git tag **with the 'v' prefix**: `git tag vX.Y.Z`.
   - **Important:** The release workflow depends on the `v` prefix (e.g., `v0.1.4`).

1. **Push**

   - Push the commit: `git push origin main`.
   - Push the tag: `git push origin vX.Y.Z`.

1. **Completion**

   - The GitHub Actions workflow will automatically create the release and publish artifacts.
