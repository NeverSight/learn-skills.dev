---
name: pr
description: Create a Pull Request (GitHub) or Merge Request (GitLab) with a well-crafted title and description. Use when the user asks to create a PR, MR, open a pull request, submit a merge request, or says something like "open a PR".
model: haiku
allowed-tools: Bash(git:*), Bash(gh:*), Bash(glab:*), Read
---

# Pull Request / Merge Request

Create PRs/MRs with descriptions that help:
- **Reviewers** understand the context and approach quickly
- **Maintainers** decide if it's ready to merge

## Workflow

### 1. Detect platform

```bash
git remote get-url origin
```

- Contains `github.com` → GitHub, use `gh`
- Contains `gitlab` → GitLab, use `glab`

### 2. Gather branch info

```bash
git branch --show-current
```

Abort if on a protected branch (main, master).

Get the default branch:
- GitHub: `gh repo view --json defaultBranchRef`
- GitLab: `glab repo view`

### 3. Check for existing PR/MR

- GitHub: `gh pr view --json url`
- GitLab: `glab mr view`

If one already exists, show the URL and ask the user if they want to update its title and description. If yes, continue the workflow and update the existing PR/MR at the end instead of creating a new one.

### 4. Get commits and diff

```bash
git fetch origin <default-branch>
git log --oneline origin/<default-branch>..HEAD
```

If ≤ 10 commits, get per-commit diffs for better context:
```bash
git show <sha> --format="commit %H%n%n    %s%n    %b"
```

If > 10 commits, use a global diff:
```bash
git diff origin/<default-branch>...HEAD
```

### 5. Decide: ask or skip

**Skip questions if the context is clear from commits and conversation.**

**Ask up to 3-4 questions if you need to clarify:**

1. **Context/motivation** — if the "why" isn't obvious from commits
2. **How to review** — for large PRs: suggested review order, key files
3. **How to test** — if tests are not obvious or missing
4. **TODO** — if draft mode: what's left to do
5. **Out of scope** — to clarify what's NOT in this PR

Questions must be **specific to the commits** — cite what you observe:
- "I see 3 refactoring commits on auth — was this in preparation for a feature or to improve maintainability?"
- "You're migrating from REST to GraphQL on the users endpoint — are there frontend clients to migrate?"
- "The config changes timeout from 30s to 5s — was this after an observed issue?"

Never ask vague questions like "Why these changes?" or "How to test?".

Also ask for **linked issues** if the user hasn't mentioned any.

### 6. Generate title and description

#### Title

- Short and descriptive (< 72 characters)
- Optional conventional commit style: `feat:`, `fix:`, `refactor:`, etc.
- English, lowercase (except proper nouns)

#### Description structure

Use **only the relevant sections** — skip empty ones:

```markdown
<!-- Only if the user provided a real issue number -->
Closes #NN

## Context
Why this change exists. 1-2 sentences + bullet points.

## Proposal
Summary of the approach and technical choices.

### Breaking changes
<!-- if applicable -->

### Design decisions
<!-- if non-obvious choices were made -->

## How to review
<!-- for large PRs -->
- Start with `file1.ts` which contains the main logic
- Then `file2.ts` for adaptations

## How to test
<!-- if not obvious -->
1. Step 1
2. Step 2

## TODO
<!-- ONLY if user asked for a draft -->
- [ ] Remaining task 1
- [ ] Remaining task 2

## Out of scope
<!-- if useful to set boundaries -->
- What is NOT included in this PR
```

#### Rules

- Focus on the **why** and **how to review**, not the what (the diff is there for that)
- Only include sections that have meaningful content
- Only include TODO section if the user explicitly asked for a draft
- Only include `Closes #NN` if the user provided a real issue number — never use placeholders like `#XXXXX` or `#NN`

### 7. Push branch if needed

```bash
git branch -r
```

If the branch isn't on the remote yet:
```bash
git push -u origin <branch>
```

### 8. Create or update the PR/MR

**Create (new PR/MR):**

- GitHub: `gh pr create --title "<title>" --body "<body>"`
- GitLab: `glab mr create --title "<title>" --description "<body>"`

Add `--draft` if the user asked for a draft.

**Update (existing PR/MR):**

- GitHub: `gh pr edit --title "<title>" --body "<body>"`
- GitLab: `glab mr update --title "<title>" --description "<body>"`

Show the PR/MR URL when done.
