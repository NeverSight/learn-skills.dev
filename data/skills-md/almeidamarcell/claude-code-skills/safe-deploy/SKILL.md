---
name: safe-deploy
description: Enforces safe deployment practices. Use before any production deploy to prevent overwriting newer code. Activated when deploying, pushing to production, or running deploy commands.
---

# Safe Deploy

## Core Rule

**NEVER deploy to production without first verifying the branch includes all commits from `origin/main`.**

This prevents the critical bug where a feature branch deploys older code that overwrites recently merged PRs.

## Before Every Deploy

Run these checks in order:

1. **Fetch latest main**
   ```bash
   git fetch origin main
   ```

2. **Check if branch is up-to-date**
   ```bash
   git merge-base --is-ancestor origin/main HEAD
   ```
   - Exit code 0 = safe to deploy
   - Exit code 1 = STOP, branch is behind main

3. **If behind, show missing commits**
   ```bash
   git log --oneline origin/main ^HEAD
   ```

4. **Merge before deploying**
   ```bash
   git merge origin/main
   ```

5. **Run tests after merge**
   ```bash
   npx vitest run
   ```

6. **Only then deploy**

## Automated Enforcement

Projects should have a `predeploy` npm script that runs `scripts/pre-deploy-check.mjs` automatically before `npm run deploy`. If the project has this script, always use `npm run deploy` instead of calling the deploy tool directly.

## When This Applies

- Running `npm run deploy`
- Running `wrangler pages deploy` directly
- Any command that pushes code to production
- When the user asks to "deploy", "push to production", or "ship it"

## What To Do

1. Always check branch status against `origin/main` first
2. If behind, inform the user and merge before proceeding
3. Run tests after merge to catch conflicts
4. Only deploy after tests pass
5. Never skip this check, even if the user says "just deploy"
