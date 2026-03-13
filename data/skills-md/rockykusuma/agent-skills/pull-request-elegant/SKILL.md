---
name: pull-request-elegant
description: Creates professional pull requests on Azure DevOps using the Azure CLI (`az repos pr`). Handles pushing branches, generating PR titles and descriptions from diffs and commit history, linking work items, adding reviewers, setting auto-complete, and opening the PR in browser. Use this skill when the user wants to create, update, or manage a pull request on Azure DevOps.
---

# Pull Request Elegant — Azure DevOps

A structured workflow for creating clean, professional pull requests on Azure DevOps using the `az repos pr` CLI.

## Prerequisites

- Azure CLI installed with the `azure-devops` extension (auto-installs on first `az repos` command).
- Authenticated via `az login` or a PAT configured with `az devops login`.
- Inside a git repo with an Azure DevOps remote.

Verify setup:
```bash
az devops configure -d organization=https://dev.azure.com/<ORG> project=<PROJECT>
```

## Workflow

1. **Validate state**
   - Run `git status` — ensure working tree is clean. If not, warn the user.
   - Identify the current branch: `git branch --show-current`. Abort if on `main` or the default target branch.
   - Ensure commits exist ahead of target: `git log <target>..<source> --oneline`.

2. **Push branch**
   - If the branch has not been pushed or has unpushed commits, run `git push -u origin <branch>`.

3. **Gather context**
   - Run `git log <target>..<source> --pretty=format:"%s" --reverse` to collect commit subjects.
   - Run `git diff <target>...<source> --stat` to get a file change summary.
   - Check branch name for work item IDs (e.g., `feature/12345-description` → work item `12345`).
   - For each detected work item ID, fetch its title and type:
     ```bash
     az boards work-item show --id <ID> --query "{title:fields.\"System.Title\",type:fields.\"System.WorkItemType\"}" -o json
     ```
   - Construct the direct URL: `https://dev.azure.com/<ORG>/<PROJECT>/_workitems/edit/<ID>`
     (use org/project from `az devops configure --list` or the remote URL)

4. **Generate PR title**

   All PR titles **must** follow the conventional commit format:
   ```
   <type>(<scope>): <description>
   ```

   **Type** — choose the one that best reflects the primary change:
   | Type | Use when |
   |------|----------|
   | `feat` | New feature or capability |
   | `fix` | Bug fix |
   | `test` | Adding or updating tests (e.g. HIL, unit, integration) |
   | `refactor` | Code restructuring without behaviour change |
   | `chore` | Tooling, config, CI, dependency updates |
   | `docs` | Documentation only |
   | `perf` | Performance improvement |

   **Scope** — pick the most specific one available:
   - Use the **work item ID** when one is linked (e.g. `feat(730169): ...`)
   - Use the **domain or subsystem name** when no work item is available (e.g. `test(HIL): ...`, `fix(auth): ...`, `feat(SDK): ...`)

   **Description**
   - Lowercase, imperative mood, no trailing period
   - Describes *what the PR achieves*, not which internal artifact implements it
   - **Never use raw identifiers verbatim** — no test case IDs (e.g. `TC_*`), function names, class names, or enum values. Translate to human-readable intent.
   - Keep the full title ≤ 80 characters
   - **When the PR mixes features, fixes, and chores**, the title reflects the most significant product-facing change — deprioritize tooling/cleanup

   **Title quality checklist:**
   - [ ] Format is `type(scope): description`
   - [ ] Free of raw code identifiers
   - [ ] Lowercase description, imperative mood, ≤ 80 chars total
   - [ ] Meaningful to a reviewer without codebase context

   **Bad → Good title examples:**
   - ❌ `Implement TC_ProgramControl_ChangeProgram HIL test` → ✅ `test(HIL): add program change test with programs list UI support`
   - ❌ `Add getProgramsList and fix getActiveProgram` → ✅ `fix(HIL): correct active program display and expose programs list`
   - ❌ `Update AuthViewModel.swift` → ✅ `fix(auth): resolve token refresh race condition`
   - ❌ `Implement feature/12345` → ✅ `feat(12345): add configurable retry logic for network requests`
   - ❌ `HIL changeVolume test` → ✅ `feat(730169): HIL changeVolume test implementation`

5. **Generate PR description**
   - Use the template in the **PR Description Template** section below.
   - Fill in from the diff, commit log, and any context the user provides.
   - Ask the user for anything that can't be inferred (e.g., testing steps, screenshots).

6. **Create the PR**
   ```bash
   az repos pr create \
     --title "<title>" \
     --description "<description>" \
     --source-branch "<source>" \
     --target-branch "<target>" \
     --work-items <ID> \
     --reviewers "<reviewer1>" "<reviewer2>" \
     --auto-complete true \
     --delete-source-branch true \
     --transition-work-items true \
     --open \
     --output json
   ```
   - `--target-branch` defaults to repo default if not specified.
   - `--work-items` only if a work item ID was detected or provided.
   - `--reviewers` only if the user specifies reviewers.
   - `--auto-complete true` enables auto-complete when all policies pass.
   - `--delete-source-branch true` cleans up after merge.
   - `--transition-work-items true` moves linked work items to next state.
   - `--open` opens the PR in the browser.

7. **Confirm**
   - Parse the JSON output to extract `pullRequestId` and the web URL.
   - Display the PR link to the user.

## Description Quality Guidelines

**Do NOT include:**
- "Test plan" sections with step-by-step manual testing scripts
- Checkbox lists of testing steps
- Redundant summaries that just restate the diff
- Auto-generated file lists (the reviewer can see the diff)
- Raw test case IDs, function names, or internal identifiers without human-readable context
- Tooling/workflow changes listed at the same level as product features — demote them or group under a separate minor bullet

**Do include:**
- Clear explanation of *what* changed and *why*
- Links to relevant work items or tickets (only if available)
- Context that isn't obvious from the code (design decisions, trade-offs, alternatives considered)
- Notes on specific areas that need careful review
- Migration steps or deployment considerations if applicable
- Screenshots or recordings only when UI changes are involved
- Limitations or known gaps (e.g., if a feature is partially implemented, say so and explain why)

**Grouping changes in the description:**
- List primary product/feature changes first
- Group supporting or enabling changes (e.g., new UI helpers, ViewModel additions) together
- Deprioritize or separate chore/tooling changes — add a `<!-- minor -->` comment or group them under a "Minor / Tooling" sub-bullet
- If a change is a bug fix bundled into a feature PR, call it out explicitly so reviewers know to look carefully

## PR Description Template

```markdown
## Summary
<!-- What changed and why. 1-3 sentences. -->

## Changes
<!-- Bulleted list of specific changes, grouped logically -->
- 

## Work Items
- [<Type Emoji> <Type> <ID>: <Work Item Title>](https://dev.azure.com/<ORG>/<PROJECT>/_workitems/edit/<ID>)

## Review Notes
<!-- Optional: areas needing careful review, design decisions, trade-offs, migration steps -->
```

> The template is intentionally lean. Add sections only when they provide value the reviewer can't get from the diff itself.

**Work item type emoji reference:**
- 📖 User Story
- 🐛 Bug
- ✅ Task
- ⚡ Feature / Epic
- 🔧 Impediment / Chore

### Passing multiline descriptions via CLI

The `--description` flag doesn't support `@file` syntax. For multiline markdown, write to a variable or use `$'...'` syntax:

```bash
DESC=$'## Summary\nRefactor auth middleware for clearer error handling.\n\n## Changes\n- Extract token validation into dedicated module\n- Add structured error responses\n\n## Work Items\n- [📖 User Story 4567: Refactor auth middleware error handling](https://dev.azure.com/MyOrg/MyProject/_workitems/edit/4567)\n\n## Review Notes\n- Pay attention to the error code mapping in `auth/errors.ts`'

az repos pr create \
  --title "Refactor auth middleware error handling" \
  --description "$DESC" \
  --source-branch feature/4567-auth-refactor \
  --target-branch main \
  --work-items 4567 \
  --open
```

## Azure DevOps CLI Quick Reference

### Create
```bash
az repos pr create --title "Title" --description "Desc" --source-branch dev --target-branch main
```

### Create as draft
```bash
az repos pr create --title "WIP: Title" --draft true
```

### Update existing PR
```bash
az repos pr update --id <PR_ID> --description "Updated desc" --title "New title"
az repos pr update --id <PR_ID> --status completed       # complete/merge
az repos pr update --id <PR_ID> --status abandoned        # close without merging
az repos pr update --id <PR_ID> --draft false              # publish a draft
az repos pr update --id <PR_ID> --auto-complete true       # enable auto-complete
```

### Add/remove reviewers
```bash
az repos pr reviewer add --id <PR_ID> --reviewers "user@org.com" "Team Name"
az repos pr reviewer remove --id <PR_ID> --reviewers "user@org.com"
```

### Link work items
```bash
az repos pr work-item add --id <PR_ID> --work-items <WORK_ITEM_ID>
az repos pr work-item remove --id <PR_ID> --work-items <WORK_ITEM_ID>
```

### List/show PRs
```bash
az repos pr list --status active --output table
az repos pr show --id <PR_ID>
```

### Set vote
```bash
az repos pr set-vote --id <PR_ID> --vote approve          # approve
az repos pr set-vote --id <PR_ID> --vote reject            # reject
az repos pr set-vote --id <PR_ID> --vote wait-for-author   # request changes
az repos pr set-vote --id <PR_ID> --vote reset             # clear vote
```

### Check policies
```bash
az repos pr policy list --id <PR_ID> --output table
az repos pr policy queue --id <PR_ID> --evaluation-id <EVAL_ID>  # re-queue a check
```

## Branch Naming Convention

When extracting work item IDs from branch names, recognize these patterns:
- `feature/<ID>-description` → work item `<ID>`
- `bugfix/<ID>-description` → work item `<ID>`
- `hotfix/<ID>-description` → work item `<ID>`
- `user/<username>/<ID>-description` → work item `<ID>`

Regex: `(?:feature|bugfix|hotfix|user/[^/]+)/(\d+)`

## Edge Cases

- **No remote**: If no Azure DevOps remote is configured, inform the user and suggest `git remote add origin <URL>`.
- **Auth expired**: If `az repos pr create` fails with 401/403, suggest `az login` or check PAT expiry.
- **Conflicts**: If the source branch has conflicts with target, warn the user to resolve before creating the PR.
- **Repo detection**: If org/project can't be auto-detected, prompt the user for `--org` and `--project` values, or suggest configuring defaults with `az devops configure`.
- **Draft PRs**: If the user says "WIP" or "draft", use `--draft true`.
- **Squash merge**: Use `--squash true` if the user requests squash merge strategy.
- **Multiple work items**: Space-separate IDs: `--work-items 123 456`.

## Anti-Patterns

Avoid these:
```
# No description
az repos pr create --title "Fix stuff"

# Vague title
az repos pr create --title "Updates"

# Missing work item link when branch clearly references one
az repos pr create --title "Feature 12345" (but no --work-items 12345)

# Creating PR on main/default branch
az repos pr create --source-branch main
```

## Examples

Good PR title from single commit (work item in scope):
```
feat(730169): HIL changeVolume test implementation
```

Good PR title from single commit (domain in scope):
```
test(HIL): add hardware-in-the-loop test infrastructure
```

Good PR title synthesized from multiple commits:
```
feat(12345): implement order processing pipeline with validation
```

Good PR title when the PR mixes a HIL test + supporting UI + a bug fix:
```
test(HIL): add program change test with programs list UI support
```
(Not: `Implement TC_ProgramControl_ChangeProgram HIL test` — missing format, uses raw test ID.)

Good draft PR:
```bash
az repos pr create \
  --title "WIP: Migrate database schema to v3" \
  --draft true \
  --source-branch feature/789-db-migration \
  --target-branch main \
  --work-items 789
```

Good PR with full options:
```bash
DESC=$'## Summary\nAdd client and server-side validation for the user registration form.\n\n## Changes\n- Add email format validation with RFC 5322 regex\n- Add password strength requirements (min 8 chars, mixed case, number)\n- Add server-side validation middleware\n\n## Work Items\n- [📖 User Story 4567: Add input validation for user registration form](https://dev.azure.com/MyOrg/MyProject/_workitems/edit/4567)\n\n## Review Notes\n- Password rules are configurable via env vars — see `config/auth.ts`'

az repos pr create \
  --title "Add input validation for registration form" \
  --description "$DESC" \
  --source-branch feature/4567-registration-validation \
  --target-branch main \
  --work-items 4567 \
  --reviewers "alice@company.com" "bob@company.com" \
  --auto-complete true \
  --delete-source-branch true \
  --transition-work-items true \
  --open
```
