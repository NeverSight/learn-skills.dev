---
name: git-conventional-commits
description: Generates conventional commit messages from staged git changes by analyzing diffs, classifying change types (feat, fix, refactor, docs, test, chore, ci, perf, style, build), and composing structured commit messages with optional scope and breaking change notation. Use when committing code, writing commit messages, preparing git commits, or when the user asks for help with commit messages.
---

# Git Conventional Commits

## Overview

Generate structured commit messages following the
[Conventional Commits](https://www.conventionalcommits.org/) specification. The
format is `type(scope): description` with an optional body and footer. This
skill ensures agents produce consistent, parseable commit messages that work
with semantic versioning tools, changelogs, and CI pipelines.

## When to use

- When committing staged changes to a git repository
- When the user asks for help writing a commit message
- When preparing a commit after implementing a feature, fix, or refactor
- When the user says "commit this", "write a commit message", or similar
- When reviewing staged changes before committing

**Do NOT use when:**

- The user explicitly provides their own commit message and just wants you to
  run `git commit`
- The repository uses a non-conventional commit format (check for
  `.commitlintrc`, `CONTRIBUTING.md`, or prior commit history first)
- There are no staged changes (`git diff --cached` is empty)

## Workflow

### 1. Read the staged diff

Run `git diff --cached` to see exactly what will be committed. If nothing is
staged, tell the user and stop.

Also run `git diff --cached --stat` for a file-level summary. This helps
identify scope.

**Why this matters:** The diff is the ground truth. Never guess what changed —
read it.

### 2. Classify the change type

Analyze the diff and select ONE primary type. Use the first matching rule:

| Type       | When to use                                                                 |
| ---------- | --------------------------------------------------------------------------- |
| `feat`     | Adds new functionality visible to users (new endpoint, UI element, command) |
| `fix`      | Corrects a bug — something that was broken now works                        |
| `refactor` | Restructures code without changing behavior (rename, extract, reorganize)   |
| `docs`     | Only documentation changes (README, JSDoc, comments, docstrings)            |
| `test`     | Only test files changed (adding, updating, or fixing tests)                 |
| `perf`     | Performance improvement with no behavior change                             |
| `style`    | Formatting only (whitespace, semicolons, linting) — no logic changes        |
| `build`    | Build system or dependency changes (package.json, Dockerfile, Makefile)     |
| `ci`       | CI/CD configuration changes (GitHub Actions, Jenkins, CircleCI)             |
| `chore`    | Maintenance tasks that don't fit above (gitignore, editor config)           |

**Decision rules for ambiguous cases:**

- New file with a function → `feat` (new capability), not `chore`
- Bug fix that also refactors → `fix` (the primary intent matters)
- Test added alongside a feature → `feat` (the feature is the main change)
- Dependency update to fix a vulnerability → `fix`, not `build`
- Renaming a public API method → `refactor` with `BREAKING CHANGE` footer

### 3. Identify the scope

The scope is the module, component, or area affected. It goes in parentheses:
`type(scope): ...`

**How to determine scope:**

- If all changes are in one directory/module → use that name (e.g., `auth`,
  `api`, `parser`)
- If changes span a single feature across files → use the feature name (e.g.,
  `login`, `search`)
- If changes are too broad to name → omit the scope: `type: description`

Scope should be a single lowercase word or hyphenated phrase. Never use file
paths as scope.

### 4. Write the subject line

The subject line is the most important part. Follow these rules strictly:

1. **Use imperative mood** — "add feature" not "added feature" or "adds
   feature". Write as if completing the sentence: "If applied, this commit will
   ___."
2. **50 characters or fewer** — Hard limit. Count the ENTIRE first line
   including `type(scope):`. For example, `feat(auth): add login endpoint` is 31
   characters. If you're over 50, shorten the description or move details to the
   body.
3. **No period at the end** — It wastes a character and is unconventional.
4. **Lowercase first letter after the colon** — `feat(auth): add login endpoint`
   not `feat(auth): Add login endpoint`.
5. **Be specific** — "fix null pointer in user lookup" not "fix bug".
6. **Verify before outputting** — Count the characters of your subject line. If
   it's close to 50, recount. It's better to be at 45 than to risk going over.

### 5. Write the body (if needed)

Add a body when the subject line alone doesn't explain WHY the change was made.
Separate from subject with a blank line.

**Include a body when:**

- The change is non-obvious (why this approach?)
- There's important context (related issue, design decision)
- The diff is large (summarize what changed and why)

**Body rules:**

- Wrap at 72 characters per line
- Explain motivation and contrast with previous behavior
- Use bullet points for multiple related changes

**Skip the body when:**

- The change is self-explanatory (e.g., `fix(typo): correct spelling in README`)
- The subject line fully captures the intent

### 6. Add breaking change footer (if needed)

If the commit introduces a breaking change (removes/renames a public API,
changes behavior that consumers depend on), add a footer:

```
BREAKING CHANGE: <description of what breaks and migration path>
```

**Rules:**

- `BREAKING CHANGE` must be uppercase, followed by a colon and space
- Describe what breaks AND how to migrate
- Alternatively, add `!` after the type/scope: `feat(api)!: remove v1 endpoints`
- Both notations can be used together for maximum visibility

## Examples

### Example 1: Simple feature addition

**Diff:**

```diff
diff --git a/src/utils/validators.ts b/src/utils/validators.ts
index 1a2b3c4..5d6e7f8 100644
--- a/src/utils/validators.ts
+++ b/src/utils/validators.ts
@@ -15,6 +15,18 @@ export function validateEmail(email: string): boolean {
   return EMAIL_REGEX.test(email);
 }

+export function validatePhoneNumber(phone: string): boolean {
+  // E.164 format: +[country code][number], 7-15 digits
+  const E164_REGEX = /^\+[1-9]\d{6,14}$/;
+  if (!phone) return false;
+  return E164_REGEX.test(phone);
+}
```

**Output:**

```
feat(validators): add phone number validation

Support E.164 format phone number validation for international
numbers. Returns false for empty strings and invalid formats.
```

### Example 2: Bug fix with breaking change

**Diff:**

```diff
diff --git a/src/api/users.ts b/src/api/users.ts
--- a/src/api/users.ts
+++ b/src/api/users.ts
@@ -8,8 +8,8 @@ import { db } from '../db';
-export async function getUser(id: string): Promise<User | null> {
-  return db.users.findOne({ id });
+export async function getUser(id: string): Promise<User> {
+  const user = db.users.findOne({ id });
+  if (!user) throw new NotFoundError(`User ${id} not found`);
+  return user;
 }
```

**Output:**

```
fix(api): throw NotFoundError instead of returning null

getUser() previously returned null for missing users, which caused
silent failures downstream. Now throws NotFoundError with the user
ID for proper error handling.

BREAKING CHANGE: getUser() no longer returns null. Callers using
null checks must switch to try/catch with NotFoundError.
```

### Example 3: Multi-file refactor

**Diff (abbreviated):**

```diff
diff --git a/src/services/payment.ts b/src/services/payment-processor.ts
similarity index 85%
rename from src/services/payment.ts
rename to src/services/payment-processor.ts

diff --git a/src/services/order.ts b/src/services/order.ts
-import { processPayment } from './payment';
+import { processPayment } from './payment-processor';

diff --git a/src/routes/checkout.ts b/src/routes/checkout.ts
-import { processPayment } from '../services/payment';
+import { processPayment } from '../services/payment-processor';
```

**Output:**

```
refactor(services): rename payment module to payment-processor

Rename for clarity since this module handles payment processing
specifically, not payment models or types. Updated all import
paths across order service and checkout routes.
```

## Common mistakes

| Mistake                                   | Fix                                                                                            |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Using past tense ("added feature")        | Use imperative mood ("add feature") — pretend the sentence starts with "This commit will..."   |
| Subject line over 50 characters           | Shorten aggressively. Move details to the body.                                                |
| Wrong type for ambiguous changes          | Ask: "What is the PRIMARY intent?" A fix that refactors is still a `fix`.                      |
| Using file paths as scope                 | Use the module/feature name instead: `auth` not `src/middleware/auth.ts`                       |
| Missing BREAKING CHANGE footer            | Any public API change (signature, return type, removed method) needs this footer               |
| Vague subject ("fix bug", "update code")  | Be specific: "fix null pointer in user lookup", "update rate limit to 100 req/s"               |
| Capitalizing first word after colon       | Lowercase: `feat: add thing` not `feat: Add thing`                                             |
| Adding a period at the end                | No period. `feat: add thing` not `feat: add thing.`                                            |
| Combining unrelated changes in one commit | Each commit should be one logical change. Suggest splitting if the diff has unrelated changes. |

## Quick reference

```
<type>(<scope>): <subject>     ← 50 chars max for full line
                                ← blank line
<body>                          ← 72 chars per line, explain WHY
                                ← blank line
<footer>                        ← BREAKING CHANGE: description
```

**Types:** `feat` | `fix` | `refactor` | `docs` | `test` | `perf` | `style` |
`build` | `ci` | `chore`

**Imperative mood test:** "If applied, this commit will `<subject>`"

**Scope:** Single lowercase word for the affected module. Omit if too broad.

## Key principles

1. **The diff is the source of truth** — Always read `git diff --cached` before
   writing. Never assume what changed based on conversation context alone.
2. **Imperative mood, always** — "add", "fix", "remove", "update" — never past
   tense or third person. This matches git's own conventions (`Merge branch`,
   `Revert commit`).
3. **One logical change per commit** — If the diff contains unrelated changes,
   suggest the user split them into separate commits before writing the message.
4. **Subject line ≤ 50 characters** — This is a hard limit, not a guideline. It
   ensures readability across all git tooling. Move details to the body.
5. **Breaking changes must be explicit** — Any change to a public API
   (signature, return type, removed export) requires a `BREAKING CHANGE:`
   footer. This drives semantic versioning — missing it causes silent breaking
   releases.
