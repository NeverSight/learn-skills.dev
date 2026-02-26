---
name: npm-updater
description: >
  Step-by-step dependency update workflow for Node.js projects. Use when the user asks to
  update, upgrade, or bump npm/yarn/pnpm/bun dependencies in package.json. Handles minor/patch
  batching, major version analysis with changelog review, migration guide discovery for
  frameworks (Next.js, Prisma, React, etc.), and post-update verification. Supports all
  package managers (npm, yarn, pnpm, bun) with automatic detection.
---

# NPM Updater

Structured workflow for updating all dependencies in a single `package.json`.

## Step 0: Detect Package Manager

Determine package manager from lockfiles and package.json config:

| Lockfile                  | package.json field        | Manager |
|---------------------------|---------------------------|---------|
| `yarn.lock`               | `packageManager: "yarn@"` | yarn    |
| `pnpm-lock.yaml`          | `packageManager: "pnpm@"` | pnpm    |
| `bun.lockb` or `bun.lock` | —                         | bun     |
| `package-lock.json`       | —                         | npm     |

Use `Glob` to check for lockfiles in the project root. If ambiguous, ask the user.

**Install commands**: npm=`npm install`, yarn=`yarn install`, pnpm=`pnpm install`, bun=`bun install`

## Step 1: Discover Verification Commands

Read `package.json` scripts. Identify which exist:
- **Type check**: `type-check`, `typecheck`, `tsc`
- **Lint**: `lint`
- **Build**: `build`
- **Test**: `test`

Store for use in Step 7.

## Step 2: Snapshot Current State

Read `package.json`. Record all `devDependencies` and `dependencies` with current version ranges. Group into:
1. `devDependencies` (update first)
2. `dependencies` (update second)

## Step 3: Check Latest Versions

For each dependency, fetch latest version from the npm registry:

```
WebFetch: https://registry.npmjs.org/{exact-package-name}/latest
Prompt: "Return the version number and the repository URL (from repository.url or homepage)"
```

**SECURITY — Package identity verification:**
- Use the **exact** package name from `package.json`. Never guess or autocomplete names.
- Only use `https://registry.npmjs.org/` — no other registries.
- Extract `repository.url` from the registry response for GitHub lookups. Never construct GitHub URLs by guessing org/repo names.
- If package name looks suspicious or metadata is unexpected, alert the user immediately.

Classify each dependency:
- **Patch/minor**: e.g., `2.1.0` → `2.3.1`
- **Major**: e.g., `2.x` → `3.x`
- **Already latest**: skip

## Step 4: Batch Minor/Patch Updates

### 4a: devDependencies (minor/patch)

Update all devDependency version ranges with minor/patch bumps in `package.json`. Run install. Run verification (Step 7).

If verification fails, bisect: revert and update half at a time to isolate the breaking dep.

### 4b: dependencies (minor/patch)

Same process for production dependencies.

## Step 5: Major Updates — Changelog Analysis

For each major version bump, **before** updating:

### 5a: Fetch Changelog

Try these sources in order, using the `repository.url` obtained in Step 3:

1. **GitHub releases**: `WebFetch` the releases page from the verified repo URL. Prompt: "List breaking changes between v{current} and v{latest}".

2. **CHANGELOG.md**: `WebFetch` the raw CHANGELOG.md from the verified repo. Prompt: "List breaking changes between v{current} and v{latest}".

3. **Context7 MCP**: `resolve-library-id` then `query-docs` with "migration breaking changes version {latest}".

### 5b: Assess Impact

For each major bump determine:
- Breaking API changes that affect this project?
- Code migration needed?
- Is this a "big upgrade" needing a migration guide? (→ Step 6)

If breaking changes are trivial (renamed export, dropped old Node support, etc.), update directly. Apply necessary code changes, run verification.

## Step 6: Major Updates — Migration Guide (User Approval Required)

Applies when:
- Package is a **framework or core tool** (Next.js, React, Prisma, TypeScript, ESLint, Emotion, Tailwind, etc.)
- Changelog references a migration guide
- Breaking changes are substantial

### 6a: Find Migration Guide

1. **Repo docs**: Check verified `repository.url` for migration/upgrade docs.
2. **Official docs**: `WebSearch` for `"{package-name} migration guide v{current} to v{latest}"`.
3. **Context7 MCP**: Query `"{package-name} migration guide version {latest}"`.
4. **Codemods/CLI tools**: Search for automated migration tools (e.g., `npx @next/codemod`, `npx prisma migrate`). Mention these explicitly.
5. **Agent-based migration prompts**: Many migration guides now include dedicated prompts or instructions for AI coding agents (e.g., LLM prompts, `.cursor` rules, agent migration scripts). When a migration guide is found, search within it and the surrounding repo/docs for:
   - Agent-specific migration prompts (often in markdown files, `.cursor/`, or labeled "AI prompt", "LLM prompt", "agent instructions")
   - Automated agent-driven migration workflows or CLI flags (e.g., `--agent`, `--ai`)
   - `WebSearch` for `"{package-name} v{latest} migration AI agent prompt"` or `"{package-name} v{latest} cursor migration"`

   If any agent-based migration prompt or tool is found, **always surface it to the user in Step 6b** — these are the highest-quality migration paths and should be preferred over manual guide-following.

### 6b: Present to User for Approval

**MANDATORY** — before following any migration guide:

```
AskUserQuestion:
"Found migration guide for {package} v{current} → v{latest}:
{link-to-guide}

Key breaking changes:
- {change 1}
- {change 2}

Approach: {describe how you'll follow the guide, mention codemods if available}

Proceed with this migration?"
Options: ["Yes, follow the guide", "Skip this upgrade", "Let me review first"]
```

### 6c: Execute Migration

Only after user approval:
1. Follow migration guide step by step
2. Run codemods if available
3. Update `package.json`, run install
4. Run verification (Step 7)

## Step 7: Verification

Run discovered commands from Step 1 sequentially, stop on first failure:

1. `{manager} install`
2. Type check (if available): `{manager} run {type-check-script}`
3. Lint (if available): `{manager} run lint`
4. Build (if available): `{manager} run build`

On failure:
- Read error output, attempt fix (type errors, renamed imports, etc.)
- Re-run verification
- If stuck after 2 attempts, report failure with error details to user

## Step 8: Summary

Present completion table:

```
| Package        | From    | To      | Type  | Source Changes | Notes           |
|----------------|---------|---------|-------|----------------|-----------------|
| typescript     | 5.3.0   | 5.7.0   | minor | none           | batched         |
| next           | 15.1.0  | 16.0.0  | major | 12 files       | migration guide |
| eslint         | 8.x     | 9.x     | major | 3 files        | flat config     |
| @types/node    | 20.x    | 22.x    | major | none           | types only      |
```

- **Source Changes**: List count of files modified due to the upgrade (excluding package.json/lockfile). If files were changed, briefly list the key files affected.
- Include skipped packages with reasons.

## Security Reminders

- Never install packages by guessing names. Use exact name from existing `package.json`.
- Verify GitHub URLs from npm registry `repository.url`, not manual construction.
- Never run `{manager} add {pkg}@latest` without confirming package name and version from registry first. Prevents typosquatting.
- If anything looks suspicious, alert the user immediately.
