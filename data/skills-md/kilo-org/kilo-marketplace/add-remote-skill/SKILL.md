---
name: add-remote-skill
description: This skill should be used when the user wants to add one or more skills from GitHub repositories to the kilo-marketplace. It handles parsing GitHub URLs, cloning skill directories, and updating SKILL.md frontmatter with source metadata.
---

# Add Remote Skill

This skill enables adding skills from GitHub repositories to the kilo-marketplace.

## When to Use

Use this skill when the user provides one or more GitHub URLs pointing to skill directories and wants them added to the marketplace.

## Workflow

### Single Skill

For a single GitHub URL, execute the add-remote-skill script directly:

```bash
npx tsx bin/add-remote-skill.ts <github-url>
```

### Multiple Skills

When the user provides multiple GitHub URLs, switch to orchestrator mode to handle each skill addition as a separate subtask. This ensures proper error handling and progress tracking for each skill.

**To switch to orchestrator mode:**

Request a mode switch to orchestrator with a message like:

> Add the following skills from GitHub:
>
> - [url1]
> - [url2]
> - [url3]
>
> For each URL, create a code subtask that runs:
> `npx tsx bin/add-remote-skill.ts <url>`
>
> after cloning the skill, make sure you give it an appropriate category. Please also check the url main repository for the LICENSE
> and warn the user if it is not Apache 2.0

## Script Details

The [`bin/add-remote-skill.ts`](bin/add-remote-skill.ts) script:

1. Parses GitHub URLs in formats:
   - `https://github.com/owner/repo/tree/branch/path/to/skill`
   - `https://github.com/owner/repo/blob/branch/path/to/file` (extracts parent directory)

2. Uses sparse checkout to clone only the skill directory

3. Copies the skill to `skills/<skill-name>/`

4. Updates SKILL.md frontmatter:
   - Adds `metadata.source.repository` with the GitHub repo URL
   - Adds `metadata.source.path` with the path within the repo
   - Adds `metadata.category: unknown` if not present

## Example Usage

```bash
# Add a single skill
npx tsx bin/add-remote-skill.ts https://github.com/vercel-labs/agent-skills/tree/main/skills/claude.ai/web-design-guidelines

# Add from Gemini CLI
npx tsx bin/add-remote-skill.ts https://github.com/google-gemini/gemini-cli/tree/main/.gemini/skills/pr-creator
```

## Error Handling

The script will fail if:

- The GitHub URL format is invalid
- The skill directory already exists locally
- SKILL.md is not found in the source directory
- The repository or path doesn't exist
