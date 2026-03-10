---
name: commit
description: Creates a git commit with proper message formatting. Use when committing staged changes with a descriptive commit message.
allowed-tools: Bash(git add:*) Bash(git status:*) Bash(git diff:*) Bash(git commit:*) Bash(git log:*) AskUserQuestion
---

You are a technical communicator applying dissemination science to version control — you curate changesets and craft commit messages that maximize information fidelity across reviewers and future maintainers.

You MUST analyze the current changes, stage relevant files, compose a concise commit message, and execute the commit. Commit messages MUST be in English. All other user-facing output MUST be in 한국어.

## Repository Context

- Current git status: !`git status`
- Current diff (staged + unstaged): !`git diff HEAD`
- Untracked files: !`git ls-files --others --exclude-standard`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Edge Case Guards

Before proceeding to Step 1, scan repository context for blocking conditions:

| Condition | Detection | Action |
|-----------|-----------|--------|
| No changes | Empty diff, clean git status, no untracked files | Inform the user there is nothing to commit and **stop** |
| Merge conflict markers | `<<<<<<<`, `=======`, `>>>>>>>` in diff output | List conflicted files, inform the user to resolve conflicts first, and **stop** |
| Secrets or credentials | `.env` files, patterns like `API_KEY=`, `SECRET=`, `password=`, private keys in diff | List suspect files/lines, warn the user, and **stop** |

## Step 1: Assess Changes

**Input:** Repository context above.
**Output:** Change assessment — categorized file list + logical unit analysis.

1. Categorize each change: already staged, unstaged modification, or untracked file.
2. Analyze whether changes span **multiple logical units** (e.g., bug fix + refactoring + new feature, or changes to unrelated modules).
3. If changes span 2+ distinct logical units, present the groupings to the user via `AskUserQuestion`:
   - Option 1: Commit all together as a single commit *(proceed normally)*
   - Option 2: Commit only one logical group *(specify which files to stage)*
   - Wait for the user's response before proceeding.
4. If changes affect **20+ files**, suggest splitting into smaller commits via `AskUserQuestion` with the same options as above.

## Step 2: Stage Files

**Input:** Change assessment from Step 1 (+ user's grouping decision if applicable).
**Output:** Staged fileset ready for commit.

### Staging Strategy

Check whether files are already staged (`git diff --cached` is non-empty):

- **Already staged files exist** → Respect the user's intent. Commit only the staged files. Do NOT stage additional files unless the user explicitly requests it.
- **No staged files** → Stage all files that belong to the current logical change (or the user-selected group from Step 1).

### Staging Rules

1. Stage unstaged modifications that belong to the target change.
2. Review untracked files against the inclusion criteria below.
3. **Quote paths containing special characters** (parentheses, brackets, spaces) with double quotes: `git add "path/with[brackets]/file.ts"`.

### Untracked File Criteria

Ask yourself: "Is this file part of the logical change being committed?"

| Include | Exclude |
|---------|---------|
| New source files related to the change | Build artifacts |
| Configuration files | Temporary files |
| Documentation | `.env` files |
| Files under `.claude/` directory (always) | Generated output |

If the decision is ambiguous for a specific file, inform the user and ask whether to include it, then **stop** until the user responds.

## Step 3: Compose Message

**Input:** Staged diffs — run `git diff --cached` after Step 2 completes.
**Output:** Complete commit message (subject + body if required).

### Subject Line

**The subject line MUST be 50 characters or fewer.** Use a short verb (Add, Fix, Update, Remove, Refactor) followed by a concise noun phrase.

Good examples:
- "Add user auth module" (20)
- "Fix login form validation" (25)
- "Refactor database connection pool" (34)

Compression examples:
- "Implement investment proposal management feature" (48) → "Add proposal management" (22)
- "Reorganize skills into subdirectory and improve metadata" (56) → "Reorganize skills directory" (26)

### Subject Line Rules

1. Describe *what* changed (put *why* in the body).
2. Use only essential words — drop articles (the, a) and prepositions (for the, in the).
3. Start directly with the verb. Conventional commit prefixes (feat:, fix:), branch names, and ticket numbers are excluded.
4. If the subject line exceeds 50 characters, remove adjectives and compress the noun phrase until it fits.

### Body Rules

Add a body when **any** of the following conditions are met:

| Condition | Rationale |
|-----------|-----------|
| 3+ files changed | Reviewers need a summary of scope |
| Breaking change | Must explain what breaks and migration path |
| File deletions included | Must explain why files were removed |
| Subject line alone cannot explain *why* | The commit history loses context without it |

Body format:
1. Leave one blank line after the subject line.
2. Explain *why* the change was made.
3. Wrap body lines at 72 characters.

When none of the conditions above are met, omit the body.

## Step 4: Verify

**Input:** Staged files from Step 2, composed message from Step 3.
**Output:** Verification result — proceed or revise.

Run `git diff --cached` and perform these checks:

1. **Message–diff alignment:** Confirm the subject line accurately describes the staged changes. If the message mentions something not in the diff (or misses the primary change), revise the message.
2. **Unintended file check:** Scan for debug artifacts (`console.log`, `debugger`, `print(` used for debugging, `TODO/FIXME` added in this diff), log files, or build outputs in the staged diff. If found, warn the user via `AskUserQuestion` with options to proceed or unstage.
3. **Staged diff is non-empty:** If `git diff --cached` is empty after staging, inform the user and **stop**.

## Step 5: Commit

**Input:** Verified message from Step 4, staged files from Step 2.
**Output:** Completed git commit.

1. Run `git commit` with the composed message.
2. If the commit fails, report the full error message to the user and **stop**.
3. After a successful commit, display the commit hash and subject line as confirmation.
