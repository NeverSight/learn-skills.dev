---
name: issue-cleaner-master
description: Analyze GitHub repository issues by checking assignee status, linked PRs, and label signals, then filter and rank contributable issues by priority (P0-P5). Outputs machine-readable JSON and human-readable Markdown reports. Use when looking for contributable issues, finding contribution opportunities, searching for good-first-issue, finding help-wanted issues, or discovering beginner-friendly tasks.
---

# Issue Cleaner Master

Analyze GitHub issues in the current repository and filter high-quality issues suitable for contribution.

## Workflow

### Step 1: Get Repository Information

1. Execute the command to retrieve the repository's owner and name:
   ```bash
   gh repo view --json nameWithOwner --jq '.nameWithOwner'
   ```
2. Parse the output into `{owner}` and `{repo}` variables.
3. Validate the output format:
   - IF the output is not in `owner/repo` format OR is empty OR an error occurs, THEN terminate execution and instruct the user to verify they are in a git repository with a GitHub remote.

### Step 2: Fetch Issue Data

1. Fetch all open issues using the GitHub GraphQL API with pagination:
   ```bash
   gh api graphql --paginate -f query='
   query($endCursor: String) {
     repository(owner: "{owner}", name: "{repo}") {
       issues(states: OPEN, first: 100, after: $endCursor) {
         pageInfo { hasNextPage endCursor }
         nodes {
           number
           title
           url
           createdAt
           updatedAt
           labels(first: 20) { nodes { name } }
           assignees(first: 10) { nodes { login } }
         }
       }
     }
   }'
   ```
2. Validate the response:
   - IF `data.repository.issues.nodes` array is not present, THEN
     - IF error is `401` or `403`, THEN instruct the user to run `gh auth status` for authentication check.
     - IF rate limit error occurs, THEN instruct to wait and retry, or reduce the `first` parameter.
     - ELSE, consider it an error and terminate.
   - IF `nodes` array is empty, THEN proceed with an empty issue list.

### Step 3: Detect Issues with Linked PRs

1. Fetch all open pull requests and their linked issues:
   ```bash
   gh api graphql --paginate -f query='
   query($endCursor: String) {
     repository(owner: "{owner}", name: "{repo}") {
       pullRequests(states: OPEN, first: 100, after: $endCursor) {
         pageInfo { hasNextPage endCursor }
         nodes {
           number
           closingIssuesReferences(first: 10) {
             nodes { number }
           }
         }
       }
     }
   }'
   ```
2. Fetch recently merged pull requests and their linked issues:
   ```bash
   gh api graphql -f query='
   {
     repository(owner: "{owner}", name: "{repo}") {
       pullRequests(states: MERGED, first: 100, orderBy: {field: UPDATED_AT, direction: DESC}) {
         nodes {
           number
           closingIssuesReferences(first: 10) {
             nodes { number }
           }
         }
       }
     }
   }'
   ```
3. Aggregate linked issue numbers:
   - Create `issues_with_open_pr` set: Contains issue numbers linked by open PRs.
   - Create `issues_with_merged_pr` set: Contains issue numbers linked by merged PRs.
4. Validate both queries return valid arrays. `closingIssuesReferences` can be empty.

### Step 4: Apply Filtering Rules

Evaluate each issue based on the following conditions for inclusion or exclusion. Each issue must have an `include_reason` or `exclude_reason`.

- **Exclusion Conditions**:
  - IF ( `issue.assignees` is non-empty AND `issue.updatedAt` is within the last 30 days ) THEN exclude (reason: `Assigned and active`).
  - IF `issue.number` is in `issues_with_open_pr` THEN exclude (reason: `Has in-progress PR`).
  - IF `issue.number` is in `issues_with_merged_pr` THEN exclude (reason: `Fixed by merged PR`).
  - IF `issue` is a non-code contribution based on the following rules:
    1. **Label signals**: `issue.labels` contains any of `question`, `support`, `duplicate`, `wontfix`, `invalid`.
    2. **Title patterns**:
       - `issue.title` ends with `?`.
       - `issue.title` starts with "How to", "How do I", "Why does", "What is".
       - `issue.title` contains "[Question]", "[Help]", "[Support]" prefix.
    3. **Combined judgment**:
       - IF only title patterns match without label signals, THEN retrieve the first 500 characters of `issue.body` using `gh issue view {issue.number} --json body` for further judgment.
       - IF determined to be non-code contribution, THEN exclude (reason: `Non-code contribution`).
- **Special Inclusion Condition**:
  - IF (`issue.assignees` is non-empty AND `issue.updatedAt` is older than 30 days AND `issue.number` is NOT in `issues_with_open_pr`) THEN include (reason: `Assigned but stale`). Mark the issue as `[Stale]` in the output.
- **Conservative Principle**: If an issue's status is uncertain, it must be included for user judgment.

### Step 5: Group by Priority

Assign a priority to each *included* issue based on its labels:

- **P0**: IF `issue.labels` contains both `help-wanted` AND `good-first-issue` THEN `P0` (Description: `Reserved for community newcomers`).
- **P1**: ELSE IF `issue.labels` contains `good-first-issue` THEN `P1` (Description: `Beginner-friendly task`).
- **P2**: ELSE IF `issue.labels` contains `help-wanted` THEN `P2` (Description: `Needs community help`).
- **P3**: ELSE IF `issue.labels` contains `kind/bug` OR `bug` THEN `P3` (Description: `Clear problem description`).
- **P4**: ELSE IF `issue.labels` contains `kind/documentation` OR `kind/cleanup` OR `documentation` THEN `P4` (Description: `Small optimization tasks`).
- **P5**: ELSE `P5` (Description: `May need more context`).

### Step 6: Generate Report Files

Generate the following two files in the current working directory:

#### 6.1 `issues-report.json` (Machine-readable)

1. Create a JSON file named `issues-report.json`.
2. Populate the file with complete audit data for all issues, adhering to the schema specified in `references/output-examples.md`.
3. Ensure the `metadata` object contains repository information, scan time, and issue counts.
4. Ensure each issue object in the `issues[]` array includes `included` (boolean), `priority` (string), `status` (string), and either `include_reason` or `exclude_reason` (string).

#### 6.2 `issues-report.md` (Human-readable)

1. Create a Markdown file named `issues-report.md`.
2. Structure the file with sections grouped by priority (P0-P5) using Markdown tables, following the format template in `references/output-examples.md`.
3. Include summary statistics.
4. Include a distribution of exclusion reasons.
5. Omit any priority groups that have no issues.

## Hard Constraints

- Utilize the `gh` CLI GraphQL API exclusively for all data retrieval.
- Scope analysis to the GitHub project corresponding to the current Git repository.
- Operations MUST be read-only; no modifications to issue status are permitted.
- PR linkage detection MUST use the `closingIssuesReferences` field; parsing of PR body text is forbidden for this purpose.
- Both `issues-report.json` and `issues-report.md` files MUST be generated.
- Every issue in the `issues-report.json` MUST include either an `include_reason` or an `exclude_reason` for auditability.

## Error Recovery

- IF `gh` CLI is not installed, THEN prompt the user to install GitHub CLI.
- IF `gh` is not authenticated, THEN instruct the user to run `gh auth login`.
- IF not in a Git repository, THEN prompt the user to navigate to a Git repository.
- IF no GitHub remote is configured, THEN prompt the user to verify the remote URL points to GitHub.
- IF a rate limit is encountered, THEN instruct the user to wait for reset or reduce batch size.
- IF the repository is empty, THEN generate reports with zero issues.