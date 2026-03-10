---
name: git-commit
description: "Create well-formatted atomic git commits with conventional commit messages and emoji. Use when making git commits, splitting large changesets into logical units, or crafting commit messages."
allowed-tools: Bash(git *), Read
---

# Git Commit

Create atomic, well-formatted commits with emoji conventional commit messages.

## Workflow

### Step 1: Assess

Run `git status`. Then check:

**Abort if:**
- Unresolved merge conflicts exist → inform the user and STOP
- No modified, staged, or untracked files exist → inform the user and STOP

**Gather context:**
1. `git log --oneline -5` — learn the project's existing commit style
2. `git diff --staged` if files are already staged; otherwise `git diff` for tracked files
3. For untracked files shown in `git status`, use `Read` to view their content

**If files are already staged**: work with ONLY those files. Do NOT stage additional files.

### Step 2: Classify and Group

For each changed file, determine its **type** (feat/fix/refactor/docs/...) and **concern** (which subsystem or feature it belongs to).

Group into **logical units** — each one a single coherent purpose that stands alone as a `git log` entry. Apply keep-together rules first to form atomic units, then evaluate split rules between those units.

**Split when ANY apply:**
1. Changes serve different purposes (bug fix + new feature)
2. Changes touch unrelated subsystems (backend API + frontend CSS)
3. Source code changes mixed with unrelated documentation
4. Diff exceeds ~200 lines with separable concerns
5. Formatting/style changes mixed with logic changes

**Keep together:**
- Feature/fix + its tests
- Code + its type definitions
- Multi-file rename of the same symbol
- Code + documentation describing that same code

### Step 3: Stage

**Single logical unit** → `git add <file1> <file2> ...`, proceed to Step 4.

**Multiple logical units** →
1. Present the plan: `N logical groups: 1. [type]: [desc] (files) 2. ...`
2. STOP and wait for the user to confirm — do not proceed until they respond
3. For each group (foundational changes first): stage → commit (Step 4) → loop back

**Rules:**
- ALWAYS use explicit file paths — NEVER `git add -A` or `git add .`
- NEVER stage secret files (.env, credentials, keys, tokens) — warn the user and skip

### Step 4: Commit

**Format:** `<emoji> <type>: <description>`

**Rules:**
- Imperative mood, present tense ("add" not "added")
- Subject line under 72 characters
- Lowercase after colon ("feat: add..." not "feat: Add...")
- No co-authorship footer
- Match project's commit style observed in Step 1

| Type     | Emoji | When to use                                |
|----------|-------|--------------------------------------------|
| feat     | ✨    | New user-facing or API-facing functionality |
| fix      | 🐛    | Corrects incorrect behavior                |
| docs     | 📝    | Documentation-only changes                 |
| style    | 💄    | Formatting, whitespace, semicolons         |
| refactor | ♻️    | Restructures without changing behavior      |
| perf     | ⚡️   | Measurable performance improvement          |
| test     | ✅    | Test-only changes                           |
| chore    | 🔧    | Build, tooling, dependencies, config        |
| ci       | 🚀    | CI/CD pipeline changes                      |
| revert   | ⏪️   | Reverts a previous commit                   |

**Critical overrides** (always use instead of the base emoji):
- `💥` for ANY breaking change → `💥 feat: ...`
- `🚑️` for production-critical hotfixes → `🚑️ fix: ...`
- `🔒️` for security vulnerability fixes → `🔒️ fix: ...`

For other specialized sub-types, read [references/emoji-mapping.md](references/emoji-mapping.md) for 50+ emoji.

**Add a body** (blank line after subject) when the "why" isn't obvious, breaking changes need explanation, or the commit closes an issue (`Closes #NNN`).

**Use direct `git commit` flags:**
```bash
# Subject only
git commit -m "<emoji> <type>: <description>"

# Subject + body
git commit -m "<emoji> <type>: <description>" -m "<optional body>"

# Multiple body paragraphs
git commit -m "<emoji> <type>: <description>" -m "<paragraph 1>" -m "<paragraph 2>"
```

### Step 5: Verify

1. `git log --oneline -3` — confirm the commit message matches the expected format
2. If groups remain from Step 3, return to Step 3
3. After all commits: `git status` to confirm no unintended changes remain

**If commit failed** (pre-commit hook, etc.): inform the user of the error and STOP. Do NOT use `--amend` — the failed commit was never created. On re-invocation, create a NEW commit.

## Edge Cases

- **Binary files**: Note in commit context; do not analyze diff content
- **Large changesets (>500 lines)**: Always propose splitting, even if changes appear to be a single logical unit
- **User-described intent**: If the user describes the purpose of changes in the conversation, use that as primary guide but validate against the actual diff — adjust if it doesn't match

## Examples

**Single commit:**
```
✨ feat: add user authentication with JWT tokens
```

**With body:**
```
💥 feat: migrate API response format to v2

The old format nested data under `response.data`. The new format puts it
at the top level. This is a breaking change for all API consumers.

Closes #234
```

**Split commits** (refactored shared module + added feature with tests + unrelated docs):
1. `♻️ refactor: extract validation logic into shared module`
2. `✨ feat: add email format validation with unit tests`
3. `📝 docs: update project setup guide`
