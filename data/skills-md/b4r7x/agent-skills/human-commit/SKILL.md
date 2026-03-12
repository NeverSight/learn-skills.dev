---
name: human-commit
description: Generates human-like git commit messages based on staged or unstaged changes. Reads git diff, analyzes what changed, and outputs 3 natural commit message options that sound like they were written by a developer — not AI. This skill should be used when the user wants a commit message, asks "what should I write for commit", "generate commit message", "human like commit", "wiadomość do commita", or just asks for help committing.
metadata:
  author: b4r7x
  version: "1.0.0"
---

# Human Commit

Reads git changes and generates commit messages that sound like a real developer wrote them.

## Workflow

### Step 1 — Read the diff

```bash
git diff --cached 2>/dev/null
```

If output is empty (nothing staged), fall back to:

```bash
git diff HEAD 2>/dev/null
```

Also check what files are involved:

```bash
git status --short 2>/dev/null
```

**If the diff is longer than ~500 lines**, don't try to analyze it raw. First identify the top changed files:

```bash
git diff --cached --stat 2>/dev/null || git diff HEAD --stat 2>/dev/null
```

Then focus analysis on the most-changed files and the overall theme, not every line.

### Step 1b — Detect repo commit style

```bash
git log --oneline -5 2>/dev/null
```

Look at the last 5 commits. If most follow Conventional Commits format (`type(scope): subject` or `type: subject`), the repo uses CC. If they're plain lowercase sentences, stick to plain style. Match the existing style — don't introduce a new one.

### Step 2 — Analyze the changes

Identify:
- What files changed and in what area (auth, UI, deps, config, tests, etc.)
- The nature of the change (fix, add, remove, move, update, refactor)
- Whether there's an obvious "why" (bug, cleanup, new feature, maintenance)
- **Scope** (for monorepos): if changed files are under `packages/`, `apps/`, or named workspaces, infer scope from the directory name (e.g., `packages/auth/` → scope `auth`)
- **Breaking changes**: if the diff removes exported functions, renames public interfaces, changes function signatures, or bumps a major version, flag it — the message may need a `BREAKING CHANGE` footer

### Step 3 — Generate 3 options

Output exactly 3 commit message options. Each on its own line, in a code block.

**Style rules (adapt to repo style detected in Step 1b):**

If the repo uses **Conventional Commits** (detected in Step 1b):
- Use `type(scope): subject` format — `fix`, `feat`, `refactor`, `chore`, `docs`, `test`, `build`
- Scope is optional; include it if changed files suggest a clear scope
- Subject lowercase, imperative mood, ≤72 chars
- If a breaking change was detected: add blank line + `BREAKING CHANGE: <what changed>`

If the repo uses **plain style** (or no clear pattern):
- **Lowercase** subject line
- **Subject ~50 chars** (up to 72 is fine)
- **No conventional commit prefixes** — `fix tokens not expiring` not `fix: resolve token expiry`
- **Imperative mood** — "fix X" not "fixed X" or "fixes X"

**Both styles:**
- Skip obvious filler — not "update code to fix the issue with the login"
- Optional body — add a blank line + 1-2 lines only if the change genuinely needs explanation (lines ≤72 chars)

Anti-patterns to avoid:
- ❌ `implement JWT token validation middleware with expiry checking`
- ❌ `refactor: extract authentication logic into separate service module`
- ❌ `fix: resolve issue with user authentication token expiration handling`
- ✅ `fix tokens not expiring`
- ✅ `move auth to its own file`
- ✅ `bump deps`
- ✅ `add dark mode toggle`
- ✅ `fix login redirect on mobile`

## Output Format

Plain style:
```
Option 1: fix tokens not expiring
Option 2: auth middleware wasn't checking expiry
Option 3: fix expired jwt tokens still passing through
```

Conventional Commits style:
```
Option 1: fix(auth): tokens not expiring on check
Option 2: fix(auth): jwt expiry not validated
Option 3: fix: expired tokens still passing auth middleware
```

With a body (when useful):
```
Option 2: reorganize auth module

pulled jwt logic out, the file was getting too long
```

With a breaking change footer:
```
Option 1: refactor(api): rename user endpoints

BREAKING CHANGE: /users/:id renamed to /users/:userId
```

Pick the best option as Option 1.
