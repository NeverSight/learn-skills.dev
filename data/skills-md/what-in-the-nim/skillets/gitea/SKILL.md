---
name: gitea
description: Use tea for Gitea repository/login discovery, pull requests, issues, comments, labels, releases, branches, actions, and authenticated API operations.
allowed-tools: Bash, Read, Grep, Glob
---

# Gitea

## Resolve the target

Run `tea` from the target repository so it discovers the repository and login from the Git remote.

- Inspect `git remote -v` when the repository is unclear, and `tea logins list` when login discovery fails.
- Disambiguate multiple targets with supported `--remote`, `--login`, or `--repo` options. Use `tea whoami` when the acting identity matters.
- If no login exists, direct the user to `tea logins add`. Keep credentials in tea's configuration, outside command arguments and repository files.

Proceed when the repository, server, login, and entity are unambiguous.

## Choose the command

Prefer entity commands (`tea pulls`, `tea issues`, etc.). Use `tea api` when they lack the operation. Consult `tea --help` or the command's `--help` for uncertain syntax or fields.

Use YAML or JSON output for downstream processing. Quote API endpoints containing `?` or `&`.

For reviews, fetch the full diff with `tea pulls "$N" --fields diff --output simple`. Use dedicated approve/reject commands for non-interactive verdicts; `tea pulls review` requires interaction. A normal `tea comments add` comment is distinct from a pull-request review. Review submission examples live in [review-pr](../review-pr/SKILL.md).

## Read, change, verify

1. Read the current entity before changing it.
2. Verify the target and requested change from available evidence. Proceed within existing authorization; ask only when the target or authorization remains unclear.
3. Keep long bodies in scratch Markdown or JSON files without credentials. Pass their contents to tea.
4. Perform exactly the requested mutation. Create, edit, close, reopen, approve, reject, merge, delete, comment, and non-GET API calls are mutations.
5. Inspect the response or re-read the entity. Report the verified result or server error; empty output alone does not establish success.

Complete when the requested operation has run against the resolved target and its result has been checked and reported.
