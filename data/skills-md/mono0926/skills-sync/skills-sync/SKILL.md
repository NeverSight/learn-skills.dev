---
name: skills-sync
description: Provides usage instructions and best practices for the skills_sync CLI tool. Use this to understand how to manage, sync, and configure AI agent skills based on the user's config file.
---

# Skills Sync

A skill for using the `skills_sync` CLI tool, which is used to manage and sync AI agent skills.

## Context

The `skills_sync` tool reads a configuration file and synchronizes the user's local skills directory (typically `~/.agents/skills`) with remote repositories.

**Configuration Precedence**:

1. Project-specific: `./skills.yaml`
2. Global: `~/.config/skills_sync/skills.yaml`

**Crucial Note**: When another skill (like `skills-optimizer`) modifies the `skills.yaml` configuration, those changes are NOT automatically applied. You MUST run `skills_sync sync` to download new skills, remove deleted ones, and apply exclusions.

## Commands

Here are the primary commands for `skills_sync`:

### `skills_sync sync`

Synchronizes the skills based on the configuration file. By default, it performs a "clean" sync by removing existing skills first.

- **When to use**: Immediately after any modifications to `~/.config/skills_sync/skills.yaml` or when the user requests to thoroughly ensure their skills directory matches the config.
- **Options**:
  - `--clean`: (Default: `true`) Deletes existing skills before installation.
  - `--no-clean`: Skips deletion. Faster, but might leave orphaned skills.
  - `--agent <name>`: Target a specific agent (default: `antigravity`). Use `*` for all.
- **Action**: It fetches repositories, applies includes/excludes, and ensures locally installed skills match the configuration.

### `skills_sync update`

Checks for and installs the latest versions of already configured skills without deleting anything first.

- **When to use**: When you want a quick check for skill updates without the overhead of a full sync.
- **Options**:
  - `--agent <name>`: Target a specific agent (default: `antigravity`).
- **Action**: Runs `npx skills update` across all configured target paths.

### `skills_sync list`

Lists the current configuration and locally installed skills.

- **When to use**: To verify what is currently configured vs. what is actually installed, or to show the user their current setup.

### `skills_sync config`

Opens the `skills.yaml` configuration file in the user's default editor (or the editor specified by `$EDITOR`).

- **When to use**: When the user wants to manually edit their configuration rather than having the AI do it.

### `skills_sync init`

Generates the default global configuration file (`~/.config/skills_sync/skills.yaml`) if it does not exist.

- **When to use**: Usually only necessary for first-time setup if the file is missing.

## `skills.yaml` Specification

The `skills.yaml` file defines which skills are installed and where.

### Target Directories (Root Keys)

- `global`: Skills listed here are installed globally to `~/.agents/skills`.
- `<path>` (e.g., `~/Git/my-project`): Skills listed here are installed locally to `.agents/skills` within the specified project directory. If the referenced path does not exist on the user's filesystem, `skills_sync` will skip it without error.

### Skill Sources

Under each target directory, you define the sources to fetch skills from:

- `owner/repo`: A shorthand for a GitHub repository.
- `https://github.com/owner/repo/tree/branch`: A specific branch or folder in a repository.
- `/local/path/to/skills`: A local directory containing skills.

### Skill Selection (Filters)

For each source, you can specify a list of filters to determine which skills to install:

- **Empty / Null**: If no filters are provided (just an empty key), all skills from the source are installed.
- **Specific Names**: Provide the exact name of the skill (e.g., `flutter-expert`).
- **Wildcards (`*`)**: Use wildcards to match multiple skills (e.g., `flutter-*` installs all skills starting with `flutter-`).
- **Exclusions (`!`)**: Prefix a pattern with `!` to exclude matching skills (e.g., `!*-legacy` skips skills ending in `-legacy`). Exclusions take precedence over inclusions.

## Workflow Integration (e.g., with `skills-optimizer`)

If you are modifying the user's `skills.yaml` (e.g., adding or removing skills):

1. **Identify the config file**: Check if a project-local `skills.yaml` exists. If not, use the global `~/.config/skills_sync/skills.yaml`.
2. **Modify the configuration**: Edit the identified `skills.yaml` file according to the user's instructions or your optimization logic.
3. **Apply the changes**: Execute `skills_sync sync` via the command line to ensure the changes take effect.
4. **Verify**: Optionally, run `skills_sync list` to confirm the installation matches expectations.

## Best Practices

- **Do not execute `sync` automatically**: NEVER run `skills_sync sync` without explicit user permission. Always ask the user if they want to apply the changes after you have modified the configuration.
- **Transparency in Configuration**: Do not modify `skills.yaml` silently. Clearly explain which skills you are adding or removing and why, ensuring the user maintains full awareness of their installed skills at all times.
- **Do not guess file paths**: Always rely on the `skills_sync` tool to handle the installation logic, cloning, and copying. Don't try to manually download zip files or clone repos with `git` to `~/.agents/skills` unless specifically requested to bypass the tool.
- **Wait for completion**: `skills_sync sync` might take a moment if it needs to download large repositories. Allow the command to finish.
- **Dry runs**: You can use `--dry-run` to see what commands `skills_sync` would execute without actually performing them.
