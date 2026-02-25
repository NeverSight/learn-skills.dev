---
name: wp-plugin-changelog
description: Generate a WordPress plugin changelog focused on user value and update readme.txt when requested.
---

# WordPress Plugin Changelog

Use this skill to generate user focused changelogs from git history or diffs.

## Inputs

- Optional: target branch, commit range, version, output format, update readme.
- If version is not provided, try to infer from the plugin header or ask the user.

## Workflow

1. **Determine the range**
   - Prefer a commit range or target branch comparison.
   - If nothing is provided, ask for the desired range.

2. **Collect changes**
   - Use `git log` and `git diff` to gather commits and file changes.
   - Focus on business value and user facing changes.

3. **Classify changes**
   - Categories: breaking, features, fixes, security, performance, UX, API.
   - Ignore low value noise (formatting, refactors, tooling).

4. **Write user friendly entries**
   - Prefer benefits over internal details.
   - Keep bullets short and clear.

5. **Output format**
   - Default: markdown.
   - If the user asks for readme.txt, use the WordPress changelog format.

6. **Update readme.txt (optional)**
   - Only update when the user explicitly requests it.
   - Insert the new entry at the top of the Changelog section.

## Rules

- Ask before modifying files.
- If nothing changed in the range, say so and stop.
