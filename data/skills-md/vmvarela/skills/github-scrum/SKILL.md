---
name: github-scrum
description: Manage software projects with Scrum on GitHub. Plan MVPs, maintain a Product Backlog as Issues, run Sprints as Milestones, and automate setup with GitHub MCP tools (preferred) or gh CLI (fallback). Adapted for solo developers and small teams (1-3 people).
---

# GitHub Scrum

Manage software projects using Scrum on GitHub, adapted for solo developers and small teams (1-3 people). This skill maps Scrum artifacts and events to GitHub primitives (Issues, Milestones, Labels, Releases) and automates project setup and sprint management.

Reference: [The 2020 Scrum Guide](https://scrumguides.org/scrum-guide.html).

---

## Tooling Strategy

**Prefer GitHub MCP tools** (`mcp_github_github_*`) for all operations they support. Fall back to the `gh` CLI **only** when the MCP server does not expose the needed functionality.

### When to use MCP tools (preferred)

The GitHub MCP server supports:

- **Issues:** create, read, update (labels, milestone, state, body), list, search, add comments, sub-issues
- **Pull Requests:** create, read, update, list, search, merge, review
- **Branches:** create, list
- **Releases:** list, get latest, get by tag
- **Labels:** get a single label
- **Files:** create/update, delete, push multiple files
- **Commits:** get, list
- **Repository:** create, search, fork, get file contents

### When to use `gh` CLI (fallback)

The MCP server does **not** support these operations — use `gh` CLI instead:

- **Labels:** create, delete, list all labels
- **Milestones:** create, update, close, list (use `gh api`)
- **Releases:** create new releases
- **Any advanced GitHub API call** not covered by MCP tools

> **IMPORTANT:** Always set `GH_PAGER=cat` when running `gh` commands to prevent interactive pagers from blocking script execution.
>
> ```sh
> GH_PAGER=cat gh issue list ...
> ```

---

## Scrum → GitHub Mapping

| Scrum Concept | GitHub Primitive | Notes |
|---|---|---|
| Product Goal | Repo description + pinned issue | Long-term vision in 1-2 sentences |
| Product Backlog | Issues (open, no milestone) | Ordered by priority labels |
| Sprint | Milestone (with due date) | Fixed-length timebox (1-2 weeks recommended) |
| Sprint Backlog | Issues assigned to a milestone | Selected during Sprint Planning |
| Sprint Goal | Milestone description | Why this sprint is valuable |
| Increment | GitHub Release / tag | Usable product at sprint end |
| Definition of Done | Checklist in issue/PR template | Shared quality standard |
| Sprint Review | Close milestone + release notes | Inspect what was delivered |
| Sprint Retrospective | Issue with label `retrospective` | Inspect how work went |
| Backlog Refinement | Edit issues: add details, resize, reprioritize | Ongoing activity |

No formal role separation. The user acts as Product Owner, Scrum Master, and Developer. The agent assists with planning, tracking, and automation.

---

## Labels System

Use namespaced labels with prefixes for filtering. Create all labels during project initialization.

### Type

| Label | Color | Description |
|---|---|---|
| `type:feature` | `#1D76DB` | New functionality |
| `type:bug` | `#D73A4A` | Something isn't working |
| `type:chore` | `#0E8A16` | Maintenance, refactoring, tooling |
| `type:spike` | `#D4C5F9` | Research or investigation (timeboxed) |
| `type:docs` | `#0075CA` | Documentation only |

### Priority

| Label | Color | Description |
|---|---|---|
| `priority:critical` | `#B60205` | Must fix immediately — blocks everything |
| `priority:high` | `#D93F0B` | Must be in the next sprint |
| `priority:medium` | `#FBCA04` | Should be done soon |
| `priority:low` | `#C2E0C6` | Nice to have, do when possible |

### Size (Relative Estimation)

| Label | Color | Description |
|---|---|---|
| `size:xs` | `#EDEDED` | Trivial — less than 1 hour |
| `size:s` | `#D4C5F9` | Small — 1 to 4 hours |
| `size:m` | `#BFD4F2` | Medium — 4 to 8 hours (half day to full day) |
| `size:l` | `#FBCA04` | Large — 1 to 2 days |
| `size:xl` | `#D93F0B` | Extra large — more than 2 days (should be split) |

### Status

| Label | Color | Description |
|---|---|---|
| `status:ready` | `#0E8A16` | Refined and ready for sprint selection |
| `status:in-progress` | `#1D76DB` | Currently being worked on |
| `status:blocked` | `#B60205` | Waiting on something external |
| `status:review` | `#D4C5F9` | In code review or waiting for feedback |

### Special

| Label | Color | Description |
|---|---|---|
| `mvp` | `#FEF2C0` | Part of the Minimum Viable Product |
| `tech-debt` | `#E4E669` | Technical debt — address proactively |
| `retrospective` | `#C5DEF5` | Sprint retrospective issue |

---

## Project Initialization

When the user wants to start a new project with Scrum, execute this workflow. Ask the user for input at each decision point.

### 1. Define the Product Goal

Ask the user: *"In 1-2 sentences, what is the product and what problem does it solve?"*

Use the answer as:
- The repository description (if creating a new repo)
- A pinned issue titled **Product Goal** with the full vision

**Using MCP (preferred):**

Use `mcp_github_github_issue_write` to create the issue:

```
tool: mcp_github_github_issue_write
params:
  owner: <owner>
  repo: <repo>
  title: "Product Goal"
  body: "## Vision\n\n<user's answer>\n\n## Target Users\n\n<who benefits>\n\n## Success Criteria\n\n- [ ] <measurable outcome>"
  labels: ["type:docs"]
```

Then pin the issue via `gh` CLI (MCP does not support pinning):

```sh
GH_PAGER=cat gh issue pin <issue-number>
```

### 2. Create Labels

Delete GitHub's default labels and create the Scrum label set.

> **Note:** The MCP server does not support label creation or deletion. Use `gh` CLI with `GH_PAGER=cat`.

```sh
# Remove default labels
GH_PAGER=cat gh label list --json name -q '.[].name' | xargs -I {} GH_PAGER=cat gh label delete {} --yes

# Type labels
GH_PAGER=cat gh label create "type:feature" --color "1D76DB" --description "New functionality"
GH_PAGER=cat gh label create "type:bug" --color "D73A4A" --description "Something isn't working"
GH_PAGER=cat gh label create "type:chore" --color "0E8A16" --description "Maintenance, refactoring, tooling"
GH_PAGER=cat gh label create "type:spike" --color "D4C5F9" --description "Research or investigation (timeboxed)"
GH_PAGER=cat gh label create "type:docs" --color "0075CA" --description "Documentation only"

# Priority labels
GH_PAGER=cat gh label create "priority:critical" --color "B60205" --description "Must fix immediately — blocks everything"
GH_PAGER=cat gh label create "priority:high" --color "D93F0B" --description "Must be in the next sprint"
GH_PAGER=cat gh label create "priority:medium" --color "FBCA04" --description "Should be done soon"
GH_PAGER=cat gh label create "priority:low" --color "C2E0C6" --description "Nice to have, do when possible"

# Size labels
GH_PAGER=cat gh label create "size:xs" --color "EDEDED" --description "Trivial — less than 1 hour"
GH_PAGER=cat gh label create "size:s" --color "D4C5F9" --description "Small — 1 to 4 hours"
GH_PAGER=cat gh label create "size:m" --color "BFD4F2" --description "Medium — 4 to 8 hours"
GH_PAGER=cat gh label create "size:l" --color "FBCA04" --description "Large — 1 to 2 days"
GH_PAGER=cat gh label create "size:xl" --color "D93F0B" --description "Extra large — more than 2 days (split it)"

# Status labels
GH_PAGER=cat gh label create "status:ready" --color "0E8A16" --description "Refined and ready for sprint selection"
GH_PAGER=cat gh label create "status:in-progress" --color "1D76DB" --description "Currently being worked on"
GH_PAGER=cat gh label create "status:blocked" --color "B60205" --description "Waiting on something external"
GH_PAGER=cat gh label create "status:review" --color "D4C5F9" --description "In code review or waiting for feedback"

# Special labels
GH_PAGER=cat gh label create "mvp" --color "FEF2C0" --description "Part of the Minimum Viable Product"
GH_PAGER=cat gh label create "tech-debt" --color "E4E669" --description "Technical debt — address proactively"
GH_PAGER=cat gh label create "retrospective" --color "C5DEF5" --description "Sprint retrospective issue"
```

### 3. Identify the MVP

Help the user define the Minimum Viable Product. For each feature idea, apply this filter:

> **"Without this, does the product make no sense?"**
> - **Yes** → label `mvp` + `priority:high` or `priority:critical`
> - **No, but it's important** → `priority:medium`, no `mvp` label
> - **Nice to have** → `priority:low`, no `mvp` label

Guide the user to keep the MVP as small as possible — typically 3-7 features. The MVP is the smallest thing that delivers the core value proposition.

Create each backlog item as an issue:

**Using MCP (preferred):**

```
tool: mcp_github_github_issue_write
params:
  owner: <owner>
  repo: <repo>
  title: "<feature title>"
  body: "## Description\n\n<what and why>\n\n## Acceptance Criteria\n\n- [ ] <criterion 1>\n- [ ] <criterion 2>\n- [ ] <criterion 3>\n\n## Notes\n\n<technical notes, constraints, dependencies>"
  labels: ["type:feature", "priority:high", "size:m", "mvp"]
```

**Using `gh` CLI (fallback):**

```sh
GH_PAGER=cat gh issue create \
  --title "<feature title>" \
  --body "## Description\n\n<what and why>\n\n## Acceptance Criteria\n\n- [ ] <criterion 1>\n- [ ] <criterion 2>\n- [ ] <criterion 3>\n\n## Notes\n\n<technical notes, constraints, dependencies>" \
  --label "type:feature,priority:high,size:m,mvp"
```

Always include **Acceptance Criteria** as a checklist — these are the concrete conditions that must be true for the issue to be considered Done.

### 4. Create the First Sprint

Create a milestone for Sprint 1. Recommend 1-week sprints for solo developers, 2-week for small teams.

> **Note:** The MCP server does not support milestones. Use `gh api` with `GH_PAGER=cat`.

```sh
# Create milestone (Sprint 1)
GH_PAGER=cat gh api repos/{owner}/{repo}/milestones --method POST \
  --field title="Sprint 1" \
  --field description="Sprint Goal: <what makes this sprint valuable>" \
  --field due_on="<ISO 8601 date, e.g. 2026-03-06T23:59:59Z>"
```

Select issues for the sprint based on priority and capacity. For a 1-week sprint, aim for issues totaling roughly 20-30 hours of estimated work (adjust based on available time).

**Using MCP (preferred) — assign issues to the sprint milestone:**

```
tool: mcp_github_github_issue_write
params:
  owner: <owner>
  repo: <repo>
  issue_number: <issue-number>
  milestone: <milestone-number>
```

**Using `gh` CLI (fallback):**

```sh
GH_PAGER=cat gh issue edit <issue-number> --milestone "Sprint 1"
```

### 5. Create Repository Scaffolding

Create the `.github/` directory structure with issue templates, PR template, labeler config, and CI workflows:

```sh
mkdir -p .github/ISSUE_TEMPLATE .github/workflows
```

#### Issue Templates

Create `.github/ISSUE_TEMPLATE/backlog-item.yml`:

```yaml
name: Backlog Item
description: Add a new item to the Product Backlog
title: "[BACKLOG] "
labels: []
body:
  - type: markdown
    attributes:
      value: "## New Backlog Item"
  - type: textarea
    id: description
    attributes:
      label: Description
      description: What needs to be done and why?
      placeholder: "As a user, I want to... so that..."
    validations:
      required: true
  - type: textarea
    id: acceptance-criteria
    attributes:
      label: Acceptance Criteria
      description: Conditions that must be true for this to be Done
      placeholder: |
        - [ ] Criterion 1
        - [ ] Criterion 2
    validations:
      required: true
  - type: dropdown
    id: type
    attributes:
      label: Type
      options:
        - feature
        - bug
        - chore
        - spike
        - docs
    validations:
      required: true
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - critical
        - high
        - medium
        - low
    validations:
      required: true
  - type: dropdown
    id: size
    attributes:
      label: Estimated Size
      options:
        - "xs (< 1 hour)"
        - "s (1-4 hours)"
        - "m (4-8 hours)"
        - "l (1-2 days)"
        - "xl (> 2 days — consider splitting)"
    validations:
      required: true
  - type: textarea
    id: notes
    attributes:
      label: Technical Notes
      description: Dependencies, constraints, implementation ideas
      placeholder: "Depends on #... / Blocked by... / Consider using..."
    validations:
      required: false
```

Create `.github/ISSUE_TEMPLATE/bug-report.yml`:

```yaml
name: Bug Report
description: Report something that isn't working correctly
title: "[BUG] "
labels: ["type:bug"]
body:
  - type: textarea
    id: description
    attributes:
      label: What happened?
      description: Clear description of the bug
      placeholder: "When I do X, Y happens instead of Z"
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: Minimal steps to trigger the bug
      placeholder: |
        1. Go to...
        2. Click on...
        3. See error...
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What should happen instead?
    validations:
      required: true
  - type: textarea
    id: context
    attributes:
      label: Environment / Context
      description: OS, browser, version, relevant config
      placeholder: "macOS 15, Node 22, Chrome 130"
    validations:
      required: false
  - type: dropdown
    id: priority
    attributes:
      label: Severity
      options:
        - "critical — app crashes or data loss"
        - "high — major feature broken, no workaround"
        - "medium — feature broken but workaround exists"
        - "low — cosmetic or minor annoyance"
    validations:
      required: true
```

#### Pull Request Template

Create `.github/PULL_REQUEST_TEMPLATE.md` with the Definition of Done checklist:

```markdown
## Summary

<!-- What does this PR do and why? Reference the issue: Closes #N -->

Closes #

## Definition of Done

- [ ] Code implemented and functional
- [ ] All acceptance criteria from the issue are met
- [ ] Tests written and passing (when applicable)
- [ ] No lint or compilation errors
- [ ] Self-reviewed (read your own diff)
- [ ] Documentation updated (if user-facing behavior changed)
```

#### PR Auto-Labeler

Create `.github/labeler.yml` — rules for `actions/labeler` to auto-label PRs based on changed files. **Adapt the path patterns to the project's actual directory structure.**

```yaml
"type:docs":
  - changed-files:
      - any-glob-to-any-file:
          - "**/*.md"
          - "docs/**"
          - "LICENSE*"
          - "CHANGELOG*"

"type:chore":
  - changed-files:
      - any-glob-to-any-file:
          - ".github/**"
          - "**/Dockerfile"
          - "**/.dockerignore"
          - "**/Makefile"
          - "**/.gitignore"
          - ".editorconfig"
          - ".prettierrc*"
          - ".eslintrc*"
          - "eslint.config.*"
          - "tsconfig*.json"
          - "biome.json"
          - "renovate.json"

# Adapt these to the project's source layout
"type:feature":
  - changed-files:
      - any-glob-to-any-file:
          - "src/**"
          - "lib/**"
          - "app/**"
          - "cmd/**"
          - "internal/**"
          - "pkg/**"
```

When initializing a real project, inspect the directory structure and adjust the glob patterns accordingly. Remove paths that don't exist and add project-specific ones (e.g., `components/**`, `api/**`, `terraform/**`).

#### Release Drafter Config

Create `.github/release-drafter.yml` — auto-generates release notes from merged PRs, categorized by the Scrum labels:

```yaml
name-template: "v$RESOLVED_VERSION"
tag-template: "v$RESOLVED_VERSION"
template: |
  ## What's Changed

  $CHANGES

  **Full Changelog**: https://github.com/$OWNER/$REPOSITORY/compare/$PREVIOUS_TAG...v$RESOLVED_VERSION
categories:
  - title: "🚀 Features"
    labels:
      - "type:feature"
  - title: "🐛 Bug Fixes"
    labels:
      - "type:bug"
  - title: "🧰 Maintenance"
    labels:
      - "type:chore"
      - "tech-debt"
  - title: "📝 Documentation"
    labels:
      - "type:docs"
  - title: "🔬 Spikes & Research"
    labels:
      - "type:spike"
change-template: "- $TITLE (#$NUMBER) @$AUTHOR"
change-title-escapes: '\<*_&'
autolabeler:
  - label: "type:feature"
    title:
      - '/^feat(\(.+\))?!?:/i'
  - label: "type:bug"
    title:
      - '/^fix(\(.+\))?!?:/i'
  - label: "type:docs"
    title:
      - '/^docs(\(.+\))?!?:/i'
  - label: "type:chore"
    title:
      - '/^(chore|refactor|test|build|ci|perf|style)(\(.+\))?!?:/i'
  - label: "type:spike"
    title:
      - '/^spike(\(.+\))?!?:/i'
  - label: "breaking"
    title:
      - '/^[a-z]+(\(.+\))?!:/i'
version-resolver:
  major:
    labels:
      - "breaking"
  minor:
    labels:
      - "type:feature"
  patch:
    labels:
      - "type:bug"
      - "type:chore"
      - "type:docs"
  default: patch
```

> **Note:** `autolabeler` labels PRs automatically from the conventional commit prefix in the title (`feat:` → `type:feature`, `fix:` → `type:bug`, etc.), so no manual labeling is needed for release-drafter to categorize and version PRs correctly.

### 6. Create Workflows

Create the following GitHub Actions workflows during project initialization.

#### Labeler Workflow

Create `.github/workflows/labeler.yml` — auto-labels every PR using the rules from `.github/labeler.yml`:

```yaml
name: Labeler

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write

jobs:
  labeler:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v5
        with:
          sync-labels: true
```

#### Stale Issues Workflow

Create `.github/workflows/stale.yml` — keeps the backlog healthy by flagging inactive issues. Does **not** auto-close — just adds a label so the user can review during refinement:

```yaml
name: Stale Issues

on:
  schedule:
    - cron: "0 9 * * 1" # Every Monday at 9:00 UTC

permissions:
  issues: write

jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v9
        with:
          stale-issue-message: >
            This issue has been inactive for 30 days.
            It will be reviewed in the next backlog refinement.
            If it's still relevant, remove the `stale` label.
          stale-issue-label: "stale"
          days-before-stale: 30
          days-before-close: -1 # Never auto-close
          exempt-issue-labels: "status:in-progress,status:blocked,mvp,priority:critical,priority:high"
          exempt-milestones: true # Don't mark sprint items as stale
```

#### Release Drafter Workflow

Create `.github/workflows/release-drafter.yml` — auto-maintains a draft release that accumulates merged PRs. When the sprint ends, the draft is ready to publish:

```yaml
name: Release Drafter

on:
  push:
    branches: [main, master]
  pull_request_target:
    types: [opened, reopened, synchronize, edited]

permissions:
  contents: write
  pull-requests: write

jobs:
  update-release-draft:
    runs-on: ubuntu-latest
    steps:
      - uses: release-drafter/release-drafter@v6
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### Auto-Assign Workflow

Create `.github/workflows/auto-assign.yml` — for solo/small teams, auto-assigns the PR creator as assignee:

```yaml
name: Auto Assign

on:
  pull_request:
    types: [opened]

permissions:
  pull-requests: write

jobs:
  assign:
    runs-on: ubuntu-latest
    steps:
      - uses: toshimaru/auto-author-assign@v2.1.1
```

---

## Sprint Lifecycle

### Sprint Planning

When the user asks to plan a new sprint or the current sprint's milestone is closed:

1. **Review the backlog.** List issues with `status:ready` that have no milestone:

   **Using MCP (preferred):**

   ```
   tool: mcp_github_github_search_issues
   params:
     q: "repo:<owner>/<repo> is:issue is:open label:status:ready no:milestone"
   ```

   **Using `gh` CLI (fallback):**

   ```sh
   GH_PAGER=cat gh issue list --label "status:ready" --milestone "" --json number,title,labels --jq '.[] | "#\(.number) \(.title) [\(.labels | map(.name) | join(", "))]"'
   ```

2. **Propose a sprint selection.** Recommend issues based on:
   - Priority: `critical` > `high` > `medium` > `low`
   - MVP items first (label `mvp`)
   - Respect capacity — total estimated size should fit the sprint duration
   - Flag dependencies between issues

3. **Define the Sprint Goal.** Ask the user: *"What is the single most important outcome of this sprint?"* Use the answer as the milestone description.

4. **Create the milestone and assign issues:**

   **Create milestone** (MCP does not support milestones — use `gh api`):

   ```sh
   # Get next sprint number
   SPRINT_NUM=$(GH_PAGER=cat gh api repos/{owner}/{repo}/milestones --jq 'length + 1')

   # Create milestone
   GH_PAGER=cat gh api repos/{owner}/{repo}/milestones --method POST \
     --field title="Sprint ${SPRINT_NUM}" \
     --field description="Sprint Goal: <goal>" \
     --field due_on="<due date ISO 8601>"
   ```

   **Assign issues using MCP (preferred):**

   ```
   tool: mcp_github_github_issue_write
   params:
     owner: <owner>
     repo: <repo>
     issue_number: <number>
     milestone: <milestone-number>
   ```

   **Using `gh` CLI (fallback):**

   ```sh
   GH_PAGER=cat gh issue edit <number> --milestone "Sprint ${SPRINT_NUM}"
   ```

5. **Mark issues as in-progress** when work begins:

   **Using MCP (preferred):**

   ```
   tool: mcp_github_github_issue_write
   params:
     owner: <owner>
     repo: <repo>
     issue_number: <number>
     labels: ["status:in-progress", ...other existing labels minus "status:ready"]
   ```

   **Using `gh` CLI (fallback):**

   ```sh
   GH_PAGER=cat gh issue edit <number> --add-label "status:in-progress" --remove-label "status:ready"
   ```

### During the Sprint

The agent can help with these activities at any time:

- **Progress report.** Show sprint burndown:

  **Using MCP (preferred):**

  ```
  tool: mcp_github_github_list_issues
  params:
    owner: <owner>
    repo: <repo>
    milestone: <milestone-number>
    state: "open"
  ```

  ```
  tool: mcp_github_github_list_issues
  params:
    owner: <owner>
    repo: <repo>
    milestone: <milestone-number>
    state: "closed"
  ```

  **Using `gh` CLI (fallback):**

  ```sh
  MILESTONE="Sprint N"
  echo "=== Open ==="
  GH_PAGER=cat gh issue list --milestone "$MILESTONE" --state open --json number,title,labels -q '.[] | "#\(.number) \(.title)"'
  echo "=== Closed ==="
  GH_PAGER=cat gh issue list --milestone "$MILESTONE" --state closed --json number,title,labels -q '.[] | "#\(.number) \(.title)"'
  ```

- **Identify blockers.** List blocked issues:

  **Using MCP (preferred):**

  ```
  tool: mcp_github_github_search_issues
  params:
    q: "repo:<owner>/<repo> is:issue is:open label:status:blocked"
  ```

  **Using `gh` CLI (fallback):**

  ```sh
  GH_PAGER=cat gh issue list --label "status:blocked" --json number,title,body -q '.[] | "#\(.number) \(.title)"'
  ```

- **Update status labels** as issues move through the workflow:
  - Starting work: add `status:in-progress`, remove `status:ready`
  - Submitting PR: add `status:review`, remove `status:in-progress`
  - Blocked: add `status:blocked`, remove `status:in-progress`
  - Done: remove all `status:*` labels, then close the issue (see [Applying the Definition of Done](#applying-the-definition-of-done))

- **Mid-sprint scope change.** If the user wants to add/remove issues from the sprint, update the milestone assignment. Never endanger the Sprint Goal — if adding scope, consider removing equal-sized items.

### Sprint Review

When the sprint ends (milestone due date reached or all issues closed):

1. **List what was completed:**

   **Using MCP (preferred):**

   ```
   tool: mcp_github_github_list_issues
   params:
     owner: <owner>
     repo: <repo>
     milestone: <milestone-number>
     state: "closed"
   ```

   **Using `gh` CLI (fallback):**

   ```sh
   GH_PAGER=cat gh issue list --milestone "Sprint N" --state closed --json number,title,closedAt \
     -q '.[] | "#\(.number) \(.title) (closed \(.closedAt | split("T")[0]))"'
   ```

2. **Identify carryover** — issues not completed move back to the backlog:

   **Using MCP (preferred):**

   ```
   # List uncompleted issues
   tool: mcp_github_github_list_issues
   params:
     owner: <owner>
     repo: <repo>
     milestone: <milestone-number>
     state: "open"

   # Remove milestone and reset status labels (return to backlog)
   tool: mcp_github_github_issue_write
   params:
     owner: <owner>
     repo: <repo>
     issue_number: <number>
     milestone: null
     labels: [<existing labels minus any "status:*" labels, plus "status:ready">]
   ```

   **Using `gh` CLI (fallback):**

   ```sh
   # List uncompleted issues
   GH_PAGER=cat gh issue list --milestone "Sprint N" --state open --json number,title \
     -q '.[] | "#\(.number) \(.title)"'

   # Remove milestone and reset status labels (return to backlog)
   GH_PAGER=cat gh issue edit <number> --milestone "" --remove-label "status:in-progress" --remove-label "status:blocked" --remove-label "status:review" --add-label "status:ready"
   ```

3. **Create a release** if there is a usable Increment:

   > **Note:** The MCP server does not support release creation. Use `gh` CLI.

   ```sh
   GH_PAGER=cat gh release create v<version> --title "Sprint N Release" \
     --notes "## What's New\n\n$(GH_PAGER=cat gh issue list --milestone 'Sprint N' --state closed --json number,title -q '.[] | "- #\(.number) \(.title)"')\n\n## Sprint Goal\n\n<goal summary>"
   ```

4. **Close the milestone:**

   > **Note:** The MCP server does not support milestone operations. Use `gh api`.

   ```sh
   # Get milestone number
   MILESTONE_NUM=$(GH_PAGER=cat gh api repos/{owner}/{repo}/milestones --jq '.[] | select(.title=="Sprint N") | .number')

   # Close it
   GH_PAGER=cat gh api repos/{owner}/{repo}/milestones/${MILESTONE_NUM} --method PATCH --field state="closed"
   ```

### Sprint Retrospective

After closing the sprint, create a retrospective issue:

**Using MCP (preferred):**

```
tool: mcp_github_github_issue_write
params:
  owner: <owner>
  repo: <repo>
  title: "Retrospective: Sprint N"
  body: "## What went well?\n\n- \n\n## What could be improved?\n\n- \n\n## Action items for next sprint\n\n- [ ] \n\n## Metrics\n\n- **Planned:** X issues\n- **Completed:** Y issues\n- **Carried over:** Z issues\n- **Sprint Goal met:** Yes/No"
  labels: ["retrospective"]
```

**Using `gh` CLI (fallback):**

```sh
GH_PAGER=cat gh issue create \
  --title "Retrospective: Sprint N" \
  --label "retrospective" \
  --body "## What went well?\n\n- \n\n## What could be improved?\n\n- \n\n## Action items for next sprint\n\n- [ ] \n\n## Metrics\n\n- **Planned:** X issues\n- **Completed:** Y issues\n- **Carried over:** Z issues\n- **Sprint Goal met:** Yes/No"
```

Ask the user to reflect on:
- What went well? (Keep doing it)
- What could be improved? (Change something)
- Action items — concrete improvements to apply in the next sprint

If the user identifies action items, create issues for them and include in next sprint planning.

---

## Backlog Refinement

Refinement is an ongoing activity, not a one-time event. When the user asks to refine the backlog, or proactively when backlog items lack detail:

### Split Large Issues

Issues labeled `size:xl` should be split. Help the user decompose them:

1. Identify the original issue's acceptance criteria
2. Group criteria into independent, deliverable chunks
3. Create new issues for each chunk (linked to original via "Part of #N")
4. Close the original issue with a comment listing the sub-issues

**Using MCP (preferred):**

```
# Create sub-issue
tool: mcp_github_github_issue_write
params:
  owner: <owner>
  repo: <repo>
  title: "<specific sub-task>"
  body: "Part of #<original-number>\n\n## Description\n\n<details>\n\n## Acceptance Criteria\n\n- [ ] <specific criterion>"
  labels: ["type:feature", "priority:high", "size:m"]

# Close original with comment (remove status:* labels)
tool: mcp_github_github_add_issue_comment
params:
  owner: <owner>
  repo: <repo>
  issue_number: <original-number>
  body: "Split into #<sub1>, #<sub2>, #<sub3>"

tool: mcp_github_github_issue_write
params:
  owner: <owner>
  repo: <repo>
  issue_number: <original-number>
  labels: [<existing labels minus any "status:*" labels>]
  state: "closed"
```

**Using `gh` CLI (fallback):**

```sh
# Create sub-issue
GH_PAGER=cat gh issue create \
  --title "<specific sub-task>" \
  --body "Part of #<original-number>\n\n## Description\n\n<details>\n\n## Acceptance Criteria\n\n- [ ] <specific criterion>" \
  --label "type:feature,priority:high,size:m"

# Close original with reference (remove status:* labels first)
GH_PAGER=cat gh issue edit <original-number> --remove-label "status:ready" --remove-label "status:in-progress" --remove-label "status:blocked" --remove-label "status:review" 2>/dev/null
GH_PAGER=cat gh issue close <original-number> --comment "Split into #<sub1>, #<sub2>, #<sub3>"
```

### Add Missing Details

For each issue that lacks acceptance criteria or has vague descriptions:

1. Read the issue content
2. Propose concrete acceptance criteria based on the description
3. Update the issue with the refined content
4. Add `status:ready` label when fully refined

**Using MCP (preferred):**

```
# Read the issue
tool: mcp_github_github_issue_read
params:
  owner: <owner>
  repo: <repo>
  issue_number: <number>

# Update issue body and labels
tool: mcp_github_github_issue_write
params:
  owner: <owner>
  repo: <repo>
  issue_number: <number>
  body: "<refined body with acceptance criteria>"
  labels: [...existing labels, "status:ready"]
```

**Using `gh` CLI (fallback):**

```sh
# Update issue body with refined content
GH_PAGER=cat gh issue edit <number> --body "<refined body with acceptance criteria>"
GH_PAGER=cat gh issue edit <number> --add-label "status:ready"
```

### Reprioritize

Review the backlog ordering when:
- New information changes priorities
- Dependencies are discovered
- The user's goals shift

List the current backlog sorted by priority:

**Using MCP (preferred):**

```
tool: mcp_github_github_search_issues
params:
  q: "repo:<owner>/<repo> is:issue is:open no:milestone"
  sort: "created"
  order: "desc"
```

**Using `gh` CLI (fallback):**

```sh
GH_PAGER=cat gh issue list --state open --milestone "" --json number,title,labels \
  -q 'sort_by(.labels | map(select(.name | startswith("priority:"))) | .[0].name) | .[] | "#\(.number) \(.title) [\(.labels | map(.name) | join(", "))]"'
```

---

## Definition of Done

Every issue must meet these criteria before closing. The agent validates this checklist before considering work complete:

### Default Definition of Done

- [ ] Code implemented and functional
- [ ] All acceptance criteria from the issue are met
- [ ] Tests written and passing (when applicable)
- [ ] No lint or compilation errors
- [ ] Self-reviewed (read your own diff before closing)
- [ ] Documentation updated (if user-facing behavior changed)
- [ ] All `status:*` labels removed from the issue
- [ ] Issue closed with reference to the commit or PR

### Applying the Definition of Done

When the user says an issue is done, verify:

1. **Check acceptance criteria** — read the issue body, confirm each criterion is checked
2. **Check code quality** — run lint/tests if configured
3. **Remove `status:*` labels and close the issue** with a reference:

   **Using MCP (preferred):**

   ```
   tool: mcp_github_github_add_issue_comment
   params:
     owner: <owner>
     repo: <repo>
     issue_number: <number>
     body: "Done in <commit-sha or PR #>"

   # Remove all status:* labels before closing
   tool: mcp_github_github_issue_write
   params:
     owner: <owner>
     repo: <repo>
     issue_number: <number>
     labels: [<existing labels minus any "status:*" labels>]
     state: "closed"
   ```

   **Using `gh` CLI (fallback):**

   ```sh
   GH_PAGER=cat gh issue edit <number> --remove-label "status:ready" --remove-label "status:in-progress" --remove-label "status:blocked" --remove-label "status:review" 2>/dev/null
   GH_PAGER=cat gh issue close <number> --comment "Done in <commit-sha or PR #>"
   ```

If any criterion is not met, tell the user what's missing before closing.

---

## Reference

### MCP Tools (preferred)

| Operation | MCP Tool | Key Params |
|---|---|---|
| Create issue | `mcp_github_github_issue_write` | `owner`, `repo`, `title`, `body`, `labels` |
| Update issue | `mcp_github_github_issue_write` | `owner`, `repo`, `issue_number`, + fields to update |
| Read issue | `mcp_github_github_issue_read` | `owner`, `repo`, `issue_number` |
| List issues | `mcp_github_github_list_issues` | `owner`, `repo`, `state`, `milestone`, `labels` |
| Search issues | `mcp_github_github_search_issues` | `q` (GitHub search syntax) |
| Add comment | `mcp_github_github_add_issue_comment` | `owner`, `repo`, `issue_number`, `body` |
| Create PR | `mcp_github_github_create_pull_request` | `owner`, `repo`, `title`, `body`, `head`, `base` |
| List PRs | `mcp_github_github_list_pull_requests` | `owner`, `repo`, `state` |
| Merge PR | `mcp_github_github_merge_pull_request` | `owner`, `repo`, `pull_number` |
| List releases | `mcp_github_github_list_releases` | `owner`, `repo` |
| Get label | `mcp_github_github_get_label` | `owner`, `repo`, `name` |
| Create branch | `mcp_github_github_create_branch` | `owner`, `repo`, `ref`, `sha` |
| List branches | `mcp_github_github_list_branches` | `owner`, `repo` |

### `gh` CLI (fallback — always use `GH_PAGER=cat`)

#### Labels

```sh
GH_PAGER=cat gh label create "<name>" --color "<hex>" --description "<text>"
GH_PAGER=cat gh label delete "<name>" --yes
GH_PAGER=cat gh label list
```

#### Issues

```sh
GH_PAGER=cat gh issue create --title "<title>" --body "<body>" --label "<l1>,<l2>" --milestone "<name>"
GH_PAGER=cat gh issue list --milestone "<name>" --state open --label "<label>"
GH_PAGER=cat gh issue edit <number> --add-label "<label>" --remove-label "<label>"
GH_PAGER=cat gh issue edit <number> --milestone "<name>"
GH_PAGER=cat gh issue close <number> --comment "<reason>"
GH_PAGER=cat gh issue view <number>
```

#### Milestones (via API)

```sh
# List milestones
GH_PAGER=cat gh api repos/{owner}/{repo}/milestones --jq '.[] | "\(.number): \(.title) (due: \(.due_on | split("T")[0]))"'

# Create milestone
GH_PAGER=cat gh api repos/{owner}/{repo}/milestones --method POST \
  --field title="Sprint N" \
  --field description="Sprint Goal: ..." \
  --field due_on="2026-03-06T23:59:59Z"

# Close milestone
GH_PAGER=cat gh api repos/{owner}/{repo}/milestones/<number> --method PATCH --field state="closed"

# Update milestone
GH_PAGER=cat gh api repos/{owner}/{repo}/milestones/<number> --method PATCH \
  --field description="Updated goal"
```

#### Releases

```sh
GH_PAGER=cat gh release create v<version> --title "<title>" --notes "<markdown>"
GH_PAGER=cat gh release list
```

---

## When to Apply This Skill

Use this skill when:

- Starting a **new software project** and need to organize work from day one
- The user asks to **plan an MVP** or define what to build first
- Managing a **Product Backlog** — creating, refining, prioritizing issues
- Running **Sprints** — planning, tracking progress, reviewing, retrospecting
- Setting up **labels and milestones** for a Scrum workflow on GitHub
- The user asks for a **progress report** or sprint status
- Performing **backlog refinement** — splitting large issues, adding acceptance criteria
- Closing a sprint and **creating a release**

### Adaptation Guidelines

**Solo developer (1 person):** Skip ceremonies that require multiple people (Daily Scrum). Focus on sprint planning + review. Use 1-week sprints to maintain momentum. The agent acts as a thinking partner for planning and review.

**Small team (2-3 people):** Use all events. Sprint planning is collaborative — the agent proposes, the team decides. Retrospectives become more valuable with multiple perspectives. Use 2-week sprints.

**Existing project:** Skip MVP identification. Start with backlog creation from existing issues/TODO lists. Create labels, then triage existing issues into the label system. Start sprinting from the current state.
