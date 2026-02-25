---
name: azdevops
description: Manages Azure DevOps projects, repos, branches, pull requests, pipelines, and work items via the azdevops CLI. Use when searching, creating, updating work items, managing PRs, triggering pipelines, or listing repos/branches. Triggers on phrases like "Azure DevOps", "work item", "pull request", "pipeline", "create a bug", "list repos", "trigger build".
compatibility: Requires azdevops CLI installed (npm install -g @billpeet/azdevops-cli) and configured (azdevops setup --org <org> --token <token>), or AZDEVOPS_ORG, AZDEVOPS_TOKEN, and optionally AZDEVOPS_PROJECT environment variables set.
---

# Azure DevOps

Interact with Azure DevOps Services using the `azdevops` CLI. All commands output JSON by default for reliable parsing.

## Setup

Configure once (credentials saved to `~/.config/azdevops-cli/config.json`):

```bash
azdevops setup --org myorg --token <personal-access-token> --project MyProject
```

Or use environment variables (these take priority over the config file):

```bash
export AZDEVOPS_ORG=myorg
export AZDEVOPS_TOKEN=<personal-access-token>
export AZDEVOPS_PROJECT=MyProject
```

The `--project` / `AZDEVOPS_PROJECT` is optional — it sets a default project so you don't need to pass `--project` on every command.

## Projects

```bash
azdevops project list --format json --pretty
```

## Repositories

```bash
azdevops repo list --project MyProject --format json --pretty
```

## Branches

```bash
azdevops branch list --repo my-repo --format json
azdevops branch list --repo my-repo --filter "feature/" --format json
```

## Pull Requests

### List PRs

```bash
azdevops pr list --repo my-repo --format json --pretty
azdevops pr list --repo my-repo --status active --top 10 --format json
```

Status options: `active`, `completed`, `abandoned`, `all` (default: `active`).

### Get a single PR

```bash
azdevops pr get --repo my-repo --id 42 --format json --pretty
```

### Create a PR

```bash
azdevops pr create --repo my-repo --source feature/login --target main --title "Add login page" --description "Details here" --format json
azdevops pr create --repo my-repo --source feature/login --target main --title "Add login page" --reviewers "id1,id2" --format json
```

### Update a PR

```bash
azdevops pr update --repo my-repo --id 42 --status completed --format json
azdevops pr update --repo my-repo --id 42 --title "Updated title" --format json
```

### List reviewers

```bash
azdevops pr reviewers --repo my-repo --id 42 --format json --pretty
```

Reviewer vote codes: 10=Approved, 5=Approved with suggestions, 0=No vote, -5=Waiting for author, -10=Rejected.

## Pipelines

### List pipelines

```bash
azdevops pipeline list --format json --pretty
```

### Trigger a pipeline run

```bash
azdevops pipeline run --pipeline-id 5 --format json
azdevops pipeline run --pipeline-id 5 --branch feature/login --format json
```

### List runs for a pipeline

```bash
azdevops pipeline runs --pipeline-id 5 --top 10 --format json --pretty
```

### Get a specific run

```bash
azdevops pipeline run-get --pipeline-id 5 --run-id 123 --format json --pretty
```

## Work Items

### Get a work item

```bash
azdevops work-item get --id 1234 --format json --pretty
azdevops work-item get --id 1234 --expand relations --format json
```

Expand options: `none`, `relations`, `fields`, `links`, `all`.

### Create a work item

```bash
azdevops work-item create --type Bug --title "Login fails on timeout" --description "Steps to reproduce..." --format json
azdevops work-item create --type Task --title "Update dependencies" --assigned-to "John Smith" --format json
```

Common types: `Bug`, `Task`, `User Story`, `Feature`, `Epic`.

### Update a work item

```bash
azdevops work-item update --id 1234 --state "In Progress" --format json
azdevops work-item update --id 1234 --title "New title" --assigned-to "Jane Doe" --format json
```

### Query work items (WIQL)

```bash
azdevops work-item query --wiql "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.State] = 'Active' AND [System.AssignedTo] = @Me" --format json --pretty
azdevops work-item query --wiql "SELECT [System.Id] FROM WorkItems WHERE [System.WorkItemType] = 'Bug' AND [System.State] <> 'Closed'" --top 20 --format json
```

## Output format

All commands support `--format json` (compact) or `--format text` (human-readable tables). Add `--pretty` for indented JSON.

Exit codes: `0` = success, `1` = error. Errors are written to stderr as JSON.

## Common workflows

**Triage a bug:**
```bash
azdevops work-item query --wiql "SELECT [System.Id] FROM WorkItems WHERE [System.WorkItemType] = 'Bug' AND [System.State] = 'New'" --top 5 --format json
azdevops work-item update --id 1234 --state "Active" --assigned-to "Jane Doe"
```

**Create a PR and trigger a build:**
```bash
azdevops pr create --repo my-repo --source feature/x --target main --title "Feature X" --format json
azdevops pipeline run --pipeline-id 5 --branch feature/x --format json
```
