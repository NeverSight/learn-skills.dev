---
name: shunk031-manage-public-private-dotfiles
description: Coordinate work across the public dotfiles source at ~/.local/share/chezmoi and the private dotfiles source at ~/.local/share/chezmoi-private. Use when a request explicitly mentions public and private dotfiles, or when configuration ownership may be split across them, especially for agent guidance, Codex or Claude configuration, shell setup, authentication helpers, profiles, launchers, and shared versus internal settings. Inspect both repositories before deciding where to change files, then update only the authoritative source or sources.
---

> [!NOTE]
> After reading this `SKILL.md`, say: `🏠 I read shunk031-manage-public-private-dotfiles.`

# Manage Public and Private Dotfiles

Treat the public and private chezmoi sources as related but separate management domains. Establish their current ownership boundary before proposing or making changes.

Skill content is not one of those domains any more. It lives in `shunk031/skills` and `shunk031/skills-private`, and the dotfiles repositories hold only the subscription allowlist that installs it. Use the `shunk031-manage-public-private-skills` skill for anything that adds, edits, or removes a skill, and use this one for the configuration around it.

## Workflow

1. Read the applicable instructions before investigating.

   - Read `~/.agents/AGENTS.md`, then read `~/.agents/AGENTS-private.md` when it is readable.
   - Treat `~/.agents/AGENTS-private.md` as the stable user-level path. Its canonical content is `~/.local/share/chezmoi-private/home/dot_config/codex/AGENTS-private.md`, while its symlink wiring is managed by the public dotfiles source.
   - Keep the private content in `home/dot_config/codex/AGENTS-private.md` and change the public repository only for its symlink wiring. Do not duplicate the content.
   - Read the root `AGENTS.md` in both dotfiles repositories. Follow each repository's rules for changes made there.

2. Inspect both repositories before choosing an edit target.

   - Public source: `~/.local/share/chezmoi`, using `~/.config/chezmoi/chezmoi.yaml`.
   - Private source: `~/.local/share/chezmoi-private`, using `~/.config/chezmoi-private/chezmoi.yaml`.
   - Check `git status --short --branch` in both repositories and preserve all existing changes.
   - Search both sources for the relevant applied path, command, setting, identifier, and documentation. Use `chezmoi source-path` with the corresponding source and config when the source mapping is unclear.
   - Inspect relevant history in both repositories when ownership, intent, or a previous migration cannot be determined from the current files alone.

3. Determine the current source of truth from evidence.

   - Prefer the public repository for portable, shareable configuration and shared agent guidance.
   - Prefer the private repository for credentials, internal infrastructure, private profiles, authentication helpers, internal endpoints, and private launchers.
   - Treat these as defaults, not a substitute for reading the current repository instructions and implementation.
   - Do not copy a setting into both repositories merely to make it available in both contexts. Preserve adapters and symlinks that expose one canonical source.

4. Make only the required source changes.

   - Edit chezmoi source state rather than applied files under the home directory.
   - Change only the authoritative repository when the task belongs to one management domain.
   - When both repositories require coordinated changes, keep their worktrees, commits, and pull requests separate and explain the dependency between them.
   - Create a clean task worktree for each affected repository when required by its instructions. Never mix unrelated local changes into the task.

5. Validate and report each affected domain independently.
   - Run the checks required by each affected repository and report which repository owns each change.
   - Keep credentials and secret values out of command output, diffs quoted in chat, and summaries.
   - Do not run `chezmoi apply`, change runtime state, push, open or update pull requests, or merge unless the user's request explicitly authorizes that operation.

## Expected Outcome

Report the evidence used to select each source of truth, the files changed in each repository, the validation performed, and any ordering required between public and private changes. If investigation shows that only one repository needs modification, say that explicitly.
