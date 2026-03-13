---
name: ml-repos
description: Browses TrueFoundry ML repositories and model registry. Lists repos, models, and artifacts with FQNs for use in other skills.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(*/tfy-api.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# ML Repos

Browse TrueFoundry ML repositories and model registry. List ML repos, get repo details, and list models/artifacts within a repo.

## Scope

Browse ML repositories, list models and artifacts, and retrieve FQNs for use with other skills (prompts, llm-deploy).

</objective>

<instructions>

## Step 1: Preflight

Run the `status` skill first to verify `TFY_BASE_URL` and `TFY_API_KEY` are set and valid.

When using direct API, set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

## Step 2: List ML Repos

### Via Tool Call
```
tfy_ml_repos_list()
```

### Via Direct API
```bash
TFY_API_SH=~/.claude/skills/truefoundry-ml-repos/scripts/tfy-api.sh

# List all ML repos
$TFY_API_SH GET /api/ml/v1/ml-repos
```

Present results:
```
ML Repos:
| Name          | ID       | FQN                    |
|---------------|----------|------------------------|
| my-models     | mlr-abc  | ml-repo:my-models      |
| experiment-1  | mlr-def  | ml-repo:experiment-1   |
```

## Step 3: Get ML Repo Details

### Via Tool Call
```
tfy_ml_repos_get(id="REPO_ID")
```

### Via Direct API
```bash
# Get ML repo by ID
$TFY_API_SH GET /api/ml/v1/ml-repos/REPO_ID
```

## Step 4: List Models in a Repo

### Via Tool Call
```
tfy_models_list(ml_repo_id="REPO_ID")
```

### Via Direct API
```bash
# List models (filter by ml_repo_id, name, or fqn)
$TFY_API_SH GET "/api/ml/v1/models?ml_repo_id=REPO_ID"

# Search by name
$TFY_API_SH GET "/api/ml/v1/models?name=my-model"

# Search by FQN
$TFY_API_SH GET "/api/ml/v1/models?fqn=model:my-models:my-model"
```

Present results:
```
Models in "my-models":
| Name        | ID       | FQN                           | Versions |
|-------------|----------|-------------------------------|----------|
| my-model    | mdl-abc  | model:my-models:my-model      | 3        |
| classifier  | mdl-def  | model:my-models:classifier    | 1        |
```

</instructions>

<success_criteria>

## Success Criteria

- The user can list all ML repos and see them in a formatted table
- The user can get details for a specific ML repo by ID
- The user can list models within a repo, filtered by repo ID, name, or FQN
- The agent has provided FQN values that can be used with other skills (prompts, llm-deploy)

</success_criteria>

<references>

## Composability

- **Preflight**: Use `status` skill to verify TFY_BASE_URL and TFY_API_KEY
- **Prompts**: ML repo FQN is needed when creating prompts (`prompts` skill)
- **Fine-tuning**: Fine-tuned model outputs are saved to ML repos
- **Deploy**: Models from the registry can be deployed using `llm-deploy` skill

## API Endpoints

See `references/api-endpoints.md` for the full ML Repos and Models API reference.

</references>

<troubleshooting>

## Error Handling

### ML Repo Not Found
```
ML repo ID not found. List repos first to find the correct ID.
```

### No Models in Repo
```
This ML repo has no models yet. Models appear after logging artifacts via the SDK or fine-tuning.
```

### Permission Denied
```
Cannot access ML repos. Check your API key permissions.
```

### Empty Response
```
No ML repos found. Create one via the TrueFoundry UI or SDK:
  import truefoundry as tfy
  client = tfy.TrueFoundryClient()
  client.create_ml_repo(name="my-repo")
```

</troubleshooting>
