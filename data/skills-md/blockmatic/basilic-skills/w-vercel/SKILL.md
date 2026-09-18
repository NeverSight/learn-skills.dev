---
name: w-vercel
description: Retrieve Vercel build logs, analyze failures, and fix the local build.
disable-model-invocation: true
---

Triage a Vercel build failure for the current branch. Use Vercel MCP when available. Fix the local build. Do not deploy. Follow [git publish](references/git-publish.md).

1. Retrieve build logs for the current branch via Vercel MCP (or the user-supplied log).
2. Parse TypeScript, ESLint, missing deps, env, imports, and config errors.
3. Apply the owning fix. Run the app or package build script from `package.json`. Stop at verified local build. No deployment and no unsolicited commit.
4. Docs: `/w-docs` if behavior or commands changed.
