---
name: code-review
description: Review PRs, MRs, and Gerrit changes with focus on security, maintainability, and architectural fit. Leverages github, gitlab, or gerrit skills based on repository context. Use when asked to review my code, check this PR, review a pull request, look at a merge request, review a patchset, or provide code review feedback.
metadata:
  author: odyssey4me
  version: "0.2.0"
  category: development
  tags: "review, security, maintainability, pr, mr"
  type: workflow
  complexity: orchestration
  requires: "github, gitlab, gerrit"
license: MIT
---

# Code Review

Orchestrates code review across GitHub PRs, GitLab MRs, and Gerrit changes. Auto-detects the platform from git remote configuration and provides focused review feedback on security, maintainability, and architectural fit.

This is a **workflow skill** -- it contains no scripts and instead guides the agent through a multi-step review process using the appropriate platform skill.

## Authentication

This skill delegates authentication to the underlying platform skill:

- **GitHub**: Requires `gh auth login` (see the github skill)
- **GitLab**: Requires `glab auth login` (see the gitlab skill)
- **Gerrit**: Requires `git-review` configuration (see the gerrit skill)

Ensure the relevant platform skill is authenticated before using code-review.

## Commands

### review

Review a change by number or URL.

**Usage:**
```
Review PR #123
Review this MR: https://gitlab.com/org/repo/-/merge_requests/42
Review Gerrit change 456789
```

The agent follows the [Workflow](#workflow) steps: detects the platform from git remotes or the provided URL, fetches the change metadata, CI status, and diff, then provides structured review feedback. Optionally posts review comments.

### remember

Save additional context for the current repository's reviews. This persists information that should be considered in future reviews of the same repo.

**Usage:**
```
Remember that this repo follows the Google Python Style Guide
Remember: authentication changes must be reviewed by the security team
Remember https://internal-docs.example.com/api-conventions as a reference for API design
Remember that the data layer uses the Repository pattern, not Active Record
```

**Keyword**: The word **remember** at the start of a message triggers saving. The context is stored in `~/.config/agent-skills/code-review.yaml` under the current repository's remote URL.

**What to save**: Coding standards, architectural decisions, external documentation links, team conventions, review policies, or any context that should inform future reviews.

### forget

Remove previously saved context for the current repository.

**Usage:**
```
Forget the note about the Google Python Style Guide
Forget all saved context for this repo
```

### show context

Display all saved context for the current repository.

**Usage:**
```
Show review context for this repo
```

### check

Verify that the required platform skill is available and authenticated.

```bash
# For GitHub repos
skills/github/scripts/github.py check

# For GitLab repos
skills/gitlab/scripts/gitlab.py check

# For Gerrit repos
skills/gerrit/scripts/gerrit.py check
```

## Repository Context

Per-repository context is persisted in `~/.config/agent-skills/code-review.yaml`, keyed by the remote fetch URL from `git remote get-url origin`. This context is loaded at the start of every review (see Step 0 in [Workflow](#workflow)).

```yaml
# ~/.config/agent-skills/code-review.yaml
repositories:
  "git@github.com:myorg/myrepo.git":
    references:
      - "https://internal-docs.example.com/api-conventions"
      - "https://google.github.io/styleguide/pyguide.html"
    standards:
      - "All API endpoints must validate input with Pydantic models"
      - "Authentication changes require security team review"
    notes:
      - "Data layer uses Repository pattern, not Active Record"
      - "Legacy modules in src/compat/ are exempt from new style rules"
  "https://gitlab.com/myorg/other-repo.git":
    references:
      - "https://docs.example.com/other-repo/architecture"
    standards: []
    notes:
      - "Migrating from REST to GraphQL -- new endpoints should use GraphQL"
```

When the user provides out-of-repo context during a review, suggest using the **remember** command to persist it.

## Workflow

### Step 0: Load Repository Context

Before starting the review, check for saved context:

```bash
git remote get-url origin
```

Read `~/.config/agent-skills/code-review.yaml` and look up the remote URL. If context exists, load it and keep it in mind throughout the review:

- **references**: Consult these when evaluating architectural decisions
- **standards**: Actively check compliance with each standard
- **notes**: Factor these into review feedback

If no context file exists or the repo has no entries, proceed without additional context.

### Step 1: Detect Platform

Determine the code hosting platform from the repository context:

```bash
# Check git remotes
git remote -v
```

- If remote contains `github.com` -> use the **github** skill
- If remote contains `gitlab` -> use the **gitlab** skill
- If `.gitreview` file exists -> use the **gerrit** skill
- If a URL is provided, detect from the URL hostname

### Step 2: Fetch Change Metadata and CI Status

**GitHub:**
```bash
skills/github/scripts/github.py prs view <number> --repo OWNER/REPO
skills/github/scripts/github.py prs checks <number> --repo OWNER/REPO
```

**GitLab:**
```bash
skills/gitlab/scripts/gitlab.py mrs view <number> --repo GROUP/REPO
skills/gitlab/scripts/gitlab.py pipelines list --repo GROUP/REPO
```

**Gerrit:**
```bash
skills/gerrit/scripts/gerrit.py changes view <change-number>
```

### Step 3: Assess CI/Test Status

Before reviewing, check whether CI/tests have passed:

- If CI is **passing**: proceed with full review
- If CI is **failing**: note the failures, skip reviewing concerns that would be caught by tests, and focus on issues tests cannot catch (security, architecture, design)
- If CI is **pending**: note it and proceed with review

### Step 4: Fetch the Diff

**GitHub:**
```bash
gh pr diff <number>
```

**GitLab:**
```bash
glab mr diff <number>
```

**Gerrit:**
```bash
git diff HEAD~1
```

### Step 5: Review the Changes

Focus review feedback on these areas, in priority order. See [references/review-checklist.md](references/review-checklist.md) for the full checklist.

1. **Security concerns**: injection vulnerabilities, authentication/authorization gaps, data exposure, unsafe deserialization, hardcoded secrets
2. **Maintainability**: excessive complexity, poor naming, missing separation of concerns, code duplication that harms readability
3. **Good coding practices**: error handling gaps, resource leaks, race conditions, missing input validation at system boundaries
4. **Architectural fit**: consistency with existing codebase patterns, appropriate abstraction level, dependency direction

**Do not flag:**
- Style/formatting issues (leave to linters)
- Minor naming preferences without clear readability impact
- Test coverage gaps (leave to CI coverage tools)
- Issues already caught by failing CI

### Step 6: Present Findings

Format findings as a structured review:

```markdown
## Code Review: PR #<number> - <title>

### Summary
<1-2 sentence summary of the change and overall assessment>

### CI Status
<passing/failing/pending -- note any failures>

### Findings

#### Security
- [ ] <finding with file:line reference>

#### Maintainability
- [ ] <finding with file:line reference>

#### Coding Practices
- [ ] <finding with file:line reference>

#### Architecture
- [ ] <finding with file:line reference>

### Verdict
<APPROVE / REQUEST_CHANGES / COMMENT -- with brief rationale>
```

If the user requests it, post the review as comments on the PR/MR using the platform skill:

**GitHub:**
```bash
gh pr review <number> --comment --body "<review>"
# Or approve/request changes:
gh pr review <number> --approve --body "<review>"
gh pr review <number> --request-changes --body "<review>"
```

**GitLab:**
```bash
glab mr note <number> --message "<review>"
# Or approve:
glab mr approve <number>
```

## Examples

### Review a GitHub PR

```
Review PR #42
```

The agent will run `git remote -v`, detect GitHub, fetch the PR with `skills/github/scripts/github.py prs view 42`, check CI with `skills/github/scripts/github.py prs checks 42`, fetch the diff with `gh pr diff 42`, and provide structured review feedback.

### Review a GitLab MR by URL

```
Review https://gitlab.com/myorg/myrepo/-/merge_requests/15
```

### Review with Posting Comments

```
Review PR #42 and post your findings as a review comment
```

### Review Focusing on Security Only

```
Review PR #42, focus only on security concerns
```

### Save Context for Future Reviews

```
Remember that this repo uses the Twelve-Factor App methodology
Remember https://wiki.example.com/team/coding-standards as a reference
Remember: all database migrations must be backwards-compatible
```

### Show Saved Context

```
Show review context for this repo
```

## Model Guidance

This skill coordinates multiple sub-skills and requires reasoning about multi-step workflows. A higher-capability model is recommended for best results.

## Troubleshooting

### Platform not detected

Ensure you are running from within a git repository with a remote configured:
```bash
git remote -v
```

### Authentication errors

Verify the underlying platform skill is authenticated:
```bash
# GitHub
gh auth status

# GitLab
glab auth status
```

### No diff available

Ensure the PR/MR number is correct and the change exists:
```bash
# GitHub
skills/github/scripts/github.py prs view <number>

# GitLab
skills/gitlab/scripts/gitlab.py mrs view <number>
```
