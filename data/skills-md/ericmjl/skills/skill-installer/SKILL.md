---
name: skill-installer
description: Install or update Agent Skills (skill folders with SKILL.md) across agent harnesses. Use when the user says install a skill, add this skill to my machine or repo, update a skill, move a skill between harnesses, or update a skill from a URL.
license: MIT
---

# Skill installer

## Usage

Use this skill when the user asks to install, update, or migrate a skill so that it is discoverable by a specific agent harness.

Typical requests:

- "Install this skill from a URL"
- "Add this skill to my machine"
- "Add this skill to this repo"
- "Update this skill from this URL"

## Requirements

- File system access to the destination directories
- Network access if installing from a URL
- `git` if installing from a git repository URL
- A tool for fetching URLs (`curl`, `wget`, or a built-in web fetch tool)

## What it does

This skill helps you do three things safely:

1. Decide whether a skill is repo-specific or machine-specific.
2. Install the full skill folder into one or more harness-specific locations.
3. Update an existing installed skill while keeping a backup.

## How it works

### Clarify scope and targets

Ask these questions if the user has not already specified the answers:

1. Is this skill repo-specific or machine-specific?
2. Which harnesses should be able to discover it?
3. What is the source of truth?

   - local folder path
   - git repo URL
   - zip URL
   - raw `SKILL.md` URL

If the user is unsure about repo versus machine scope, use this heuristic:

- Repo-specific: only useful in one repo, depends on that repo’s structure or conventions.
- Machine-specific: reusable across many repos.

### Choose destinations

Use `references/harness-locations.md` to map harness and scope to install paths.

### Install

1. Confirm the skill directory name matches `name` in frontmatter.
2. Confirm `SKILL.md` contains valid frontmatter (`name`, `description`).
3. Copy the entire skill folder into each destination.

### Update

When updating an already installed skill:

1. Create a timestamped backup of the existing installed folder.
2. Replace the installed folder with the new version.
3. Confirm the harness can discover the updated skill.

Do not delete user files unless they explicitly ask.

### Notes on distribution

Some ecosystems distribute a packaged `.skill` file, which is a zip container. Treat that as a distribution artifact, not the canonical source.
