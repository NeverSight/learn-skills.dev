---
name: review-ci
description: Review the CI status of a GitHub Pull Request using GitHub CLI (`gh`). Use when the user asks to check CI status, investigate failing checks, or understand why a PR pipeline is failing.
disable-model-invocation: true
metadata:
  author: Saurabh Daware (https://srbh.dev)
  version: 0.0.1
---

Your job is to check the CI status of the given Pull Request and explain whether checks are passing or failing, and why.

## Arguments

- **PR_URL**: GitHub Pull Request URL (preferred)

Use AskQuestion to get PR URL / PR Number / Repository if not provided in prompt.

## Variables

Extract following variables from {{PR_URL}}. We'll use them ahead

- **REPO**: '{{owner}}/{{reponame}}'
- **PR_NUMBER**: {{number}}

E.g. in PR_URL: https://github.com/saurabhdaware/agent-toolkit/pull/123, REPO=saurabhdaware/agent-toolkit and PR_NUMBER=123

## Steps to Review CI

### Step 1: Getting status of all CI pipelines

Run the following command

```sh
gh pr checks {{PR_NUMBER}} --json name,state,description,link,event,bucket,workflow,startedAt,completedAt --repo {{REPO}}
```

- If error in authentication or command installation, refer to [gh installation and authentication guide](references/gh-installation.md)

### Step 2: Print a table with overall CI status

Print a table with following columns-

- Workflow and Name ("workflow: name" format)
- State (Use ✅, ❌, ⚠️ emojis for ease of reading)
- Link
- Description (if any)

### Step 3: Deep dive on failures (if there are any failures)

Now we'll find the logs to see why CI checks are failing.

For each failing github actions CI checks (run it as separate subagents if possible),

- Extract RUN_ID and JOB_ID from the Link
- Command to get full logs `gh run view {{RUN_ID}} --job {{JOB_ID}} --log --repo {{REPO}}` (Logs can be large so smartly use `grep` to filter errors and their reasons)
- You can also use `{{PR_URL}}.diff` to get diff of PR and see the changes in code that could be responsible for failures (diffs can be large too. Use `grep` to ignore snapshots, lock file changes, or similar irrelevant changes. Do not fetch diff again if it was already done in earlier chat)

### Step 4: Print errors and their reasons (if there are any failures)

List down your findings on why each check is failing, what code change is responsible (if known), how to fix (if known)
