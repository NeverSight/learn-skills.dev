---
name: pr-document-writer
description: Generate a Pull Request title and description by analyzing the current branch's diff against the base branch. Use this skill whenever the user wants to create a PR description, fill out a PR template, write PR details, generate a pull request, open a PR, update a PR description, or asks anything related to pull request descriptions, titles, or templates — even if they just say "write a PR" or "describe my changes" or "open a pull request" or "update the PR".
---

# PR Description Generator

Generate a well-crafted PR title (conventional commit format) and a filled-out PR description template by analyzing the git diff of the current branch.

## Workflow

### Step 1: Identify the base branch

Determine the base branch that the current branch will be merged into.

Run these git commands to gather context:

```bash
git branch --show-current
git remote show origin | grep "HEAD branch"
git log --oneline -5
```

Use `git remote show origin` to find the default branch (usually `main` or `master`). If the repo has a common base like `develop` or `staging`, infer from the branch naming convention or recent merge targets.

If the base branch cannot be confidently determined (e.g., ambiguous remote setup, multiple candidates), ask the user which branch they intend to merge into. Don't guess — getting the base branch wrong means the diff will be wrong, which means the entire PR description will be wrong.

### Step 2: Get the latest commit and full diff

Fetch the diff between the current branch and the base branch, along with the latest commit info:

```bash
git log -1 --format="%H %s"
git diff <base-branch>...HEAD --stat
git diff <base-branch>...HEAD
```

Use the three-dot diff (`...`) because it shows only the changes introduced on the current branch since it diverged from the base — this is what a PR reviewer will actually see.

If the diff is extremely large (thousands of lines), use `--stat` first to understand the scope, then read the most important changed files selectively. For very large diffs, focus on:

- New files (they tell the story of what was added)
- Modified core files (business logic, not config/lock files)
- Deleted files (what was removed and why)

Skip noisy files like lock files, auto-generated code, or minified assets — they add nothing to the description.

### Step 3: Analyze the diff thoroughly

Before writing anything, take time to actually understand what the changes do. This is the most important step — a PR description is only as good as the understanding behind it.

Think through:

- **What** changed? (files, functions, components, APIs)
- **Why** might it have changed? (bug fix, new feature, refactor, performance)
- **How** do the changes work together? (trace the logic across files)
- **What's the scope?** (is this a small targeted fix or a broad refactor?)
- **Are there any breaking changes?** (API changes, schema migrations, removed exports)
- **Are there side effects?** (dependency updates, config changes)

Group related changes into logical chunks. A PR that touches 15 files might really be doing 2-3 things — identify those themes so the description tells a coherent story rather than listing every file.

### Step 4: Find the PR template

Check whether the project already has a PR template. Look in these common locations:

```bash
# Check all common PR template locations
ls -la .github/pull_request_template.md .github/PULL_REQUEST_TEMPLATE.md .github/PULL_REQUEST_TEMPLATE/ docs/pull_request_template.md PULL_REQUEST_TEMPLATE.md 2>/dev/null
```

Common locations to check:

- `.github/pull_request_template.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/PULL_REQUEST_TEMPLATE/` (directory with multiple templates)
- `docs/pull_request_template.md`
- `PULL_REQUEST_TEMPLATE.md` (repo root)

If the project has its own template, read it and use it.

If no project template exists, use the default template bundled with this skill at `assets/default-template.md` (relative to this skill's directory).

### Step 5: Generate the PR title

Create a PR title using conventional commit format:

```
<type>(<scope>): <short summary>
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

**Guidelines:**

- The type should reflect the primary purpose of the PR (if there are mixed changes, use the dominant one)
- The scope is optional but helpful — use the module, component, or area of the codebase affected
- The summary should be imperative mood ("add" not "added"), lowercase, no period at the end
- Keep it under 72 characters total
- It should make immediate sense to someone scanning a list of PRs

**Examples:**

- `feat(auth): add JWT refresh token rotation`
- `fix(api): handle null response in user endpoint`
- `refactor(dashboard): extract chart components into shared module`
- `chore(deps): bump express from 4.18 to 4.19`

### Step 6: Fill the template

Fill in the PR template based on your analysis from Step 3. Be specific and useful:

- **What does this PR do?** — Describe the changes in plain language. Lead with the "why" (the problem or goal), then explain the "what" (what was done). Use bullet points for multiple changes. Don't just restate the diff — add context that isn't obvious from the code.
- **Testing steps** — Write concrete steps a reviewer can follow to verify the changes. Include specific URLs, commands, inputs, or scenarios to test. If there are edge cases, mention them.
- **Checklists** — Check off items that are true based on what you can observe from the code. Leave items unchecked if you can't verify them or if they don't apply. If an item is clearly not applicable, you can note `N/A` with a brief reason.

Don't fabricate information. If you can't determine something from the diff (like whether manual testing was done), leave it for the author to fill in. It's better to leave a checkbox unchecked than to check it incorrectly.

### Step 7: Present the output

Output exactly two markdown code blocks in the chat:

First block — the PR title:

````
```markdown
<generated-title>
```
````

Second block — the filled template:

````
```markdown
<filled-template>
```
````

This format makes it easy for the user to copy-paste into their PR.

### Step 8: Offer to create or update the PR via GitHub tools

After presenting the output, check whether any GitHub MCP tools are available (e.g., tools matching patterns like `github`, `pull_request`, `create_pull_request`, `update_pull_request`).

**If GitHub tools are available:**

First, check if a PR already exists for the current branch:

- Search for open PRs where the head branch matches the current branch
- If a PR exists: ask the user if they'd like to update the existing PR's title and description with the generated content
- If no PR exists: ask the user if they'd like to create a new PR with the generated title and description

**If no GitHub tools are available:**

Let the user know the output is ready for them to copy-paste. No further action needed — don't suggest installing tools or extensions, just move on gracefully.

Always wait for user confirmation before creating or updating anything. Never auto-create or auto-update a PR without explicit approval.
