---
name: github-issues
description: Triage and resolve repository GitHub issues using the bundled CLI. Use when asked to read issue state, discuss issue scope, implement issue-driven code changes, post comments, or close issues.
---

# GitHub Issues

Use the installed skill script directly:

```bash
node "$SKILL_DIR/scripts/github-issues.mjs" <command> [options]
```

`SKILL_DIR` is the directory containing this `SKILL.md`.

## Inputs

- `.env` with:
  - `GITHUB_API_KEY=<token>`
  - `GITHUB_REPOSITORY=<owner/repo>`
- Target issue number, or use worklist mode when unspecified

## Steps

1. Read issue details and comments:
   - `node "$SKILL_DIR/scripts/github-issues.mjs" read -n <issue-number> --comments`
2. Classify issue type:
   1. Code-change request
   2. Brainstorm/open discussion
   3. Irrelevant to this repository
3. Execute by type:
   1. Code-change request:
      1. Create branch `issue-<number>-<topic>`.
      2. Implement and validate changes.
      3. Commit and push branch.
      4. Post summary comment including commit ID.
      5. Close only when fully resolved.
   2. Brainstorm/open discussion:
      1. Post concise, constructive response grounded in repository context.
      2. Ask only unblocker questions when needed.
   3. Irrelevant issue:
      1. Post a short polite response.
      2. Keep response brief.
4. Address one issue end-to-end per skill call.
5. After completion, ask whether to continue with the next issue.

## CLI Reference

- Work queue: `node "$SKILL_DIR/scripts/github-issues.mjs" worklist`
- List open issues: `node "$SKILL_DIR/scripts/github-issues.mjs" read -s open -l 20`
- Read one issue: `node "$SKILL_DIR/scripts/github-issues.mjs" read -n <issue-number>`
- Read issue + comments: `node "$SKILL_DIR/scripts/github-issues.mjs" read -n <issue-number> --comments`
- Add comment: `node "$SKILL_DIR/scripts/github-issues.mjs" comment -n <issue-number> -b "<text>"`
- Close issue: `node "$SKILL_DIR/scripts/github-issues.mjs" close -n <issue-number> -b "<resolution note>"`

## Conventions

- Keep comments concise, explicit, and status-oriented.
- Include assumptions when proceeding with incomplete issue details.
- Ask focused numbered follow-up questions only when required to unblock implementation.
