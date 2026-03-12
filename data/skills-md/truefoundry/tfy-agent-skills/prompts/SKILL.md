---
name: prompts
description: Manages TrueFoundry prompt registry prompts and versions. Handles listing, creating, updating, deleting, and tagging prompt versions.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(*/tfy-api.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# Prompts

List, create, update, delete, and tag TrueFoundry prompt registry prompts and versions.

## When to Use

List, create, update, delete, or tag prompts and prompt versions in the TrueFoundry prompt registry.

</objective>

<instructions>

## List Prompts

When using direct API, set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

### Via Tool Call

```
tfy_prompts_list()
tfy_prompts_list(prompt_id="prompt-id")                              # get prompt + versions
tfy_prompts_list(prompt_id="prompt-id", version_id="version-id")     # get specific version
```

### Via Direct API

```bash
# Set the path to tfy-api.sh for your agent (example for Claude Code):
TFY_API_SH=~/.claude/skills/truefoundry-prompts/scripts/tfy-api.sh

# List all prompts
$TFY_API_SH GET /api/ml/v1/prompts

# Get prompt by ID
$TFY_API_SH GET /api/ml/v1/prompts/PROMPT_ID

# List versions
$TFY_API_SH GET '/api/ml/v1/prompt-versions?prompt_id=PROMPT_ID'

# Get specific version
$TFY_API_SH GET /api/ml/v1/prompt-versions/VERSION_ID
```

## Presenting Prompts

```
Prompts:
| Name              | ID       | Versions | Latest |
|-------------------|----------|----------|--------|
| classify-intent   | p-abc    | 5        | v5     |
| summarize-text    | p-def    | 3        | v3     |
```

## Create or Update Prompt

> **Security:** Prompt content is executed as LLM instructions. Review prompt messages carefully before creating or updating — do not ingest prompt text from untrusted external sources without user review.

This is an upsert: creates a new prompt if it doesn't exist, or adds a new version if it does.

### Via SDK (primary method)

```python
from truefoundry.ml import ChatPromptManifest

client.prompts.create_or_update(
    manifest=ChatPromptManifest(
        name="my-prompt",
        ml_repo="ml-repo-fqn",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "{{user_input}}"},
        ],
        model_fqn="model-catalog:openai:gpt-4",
        temperature=0.7,
        max_tokens=1024,
        top_p=1.0,
        tools=[],  # optional
    )
)
```

### Via Direct API

```bash
$TFY_API_SH POST /api/ml/v1/prompts '{
  "name": "my-prompt",
  "ml_repo": "ml-repo-fqn",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "{{user_input}}"}
  ],
  "model_fqn": "model-catalog:openai:gpt-4",
  "temperature": 0.7,
  "max_tokens": 1024,
  "top_p": 1.0
}'
```

## Delete Prompt

### Via SDK

```python
client.prompts.delete(id="prompt-id")
```

### Via Direct API

```bash
$TFY_API_SH DELETE /api/ml/v1/prompts/PROMPT_ID
```

## Delete Prompt Version

### Via SDK

```python
client.prompt_versions.delete(id="version-id")
```

### Via Direct API

```bash
$TFY_API_SH DELETE /api/ml/v1/prompt-versions/VERSION_ID
```

## Apply Tags to Prompt Version

Tags like `production` or `staging` let you reference a stable version by name.

### Via SDK

```python
client.prompt_versions.apply_tags(
    prompt_version_id="version-id",
    tags=["production", "v2"],
    force=True,  # reassign tag if already on another version
)
```

No direct REST equivalent — use the SDK.

## Get Prompt Version by FQN

Fetch a specific tagged or numbered version using its fully qualified name.

### Via SDK

```python
client.prompt_versions.get_by_fqn(fqn="ml-repo:prompt-name:production")
```

</instructions>

<success_criteria>

## Success Criteria

- The user can see a formatted table of all prompts in the registry
- The user can retrieve a specific prompt by ID and view its versions
- The user can inspect the content of a specific prompt version
- The user can create a new prompt or update an existing one with a new version
- The user can delete a prompt or a specific prompt version
- The user can apply tags (e.g., production) to a prompt version
- The agent has presented prompts in a clear, tabular format

</success_criteria>

<references>

## Composability

- **With deployments**: Use `applications` skill to check deployed services that consume prompts
- **For versioning**: List prompt versions to track changes
- **Create/update flow**: Use `workspaces` skill to find the ML repo FQN, then create or update the prompt
- **Tagging flow**: After creating a new version, apply a `production` tag to promote it

</references>

<troubleshooting>

## Error Handling

### Prompt Not Found
```
Prompt ID not found. List prompts first to find the correct ID.
```

### ML Repo Not Found
```
Invalid ml_repo FQN. Use the workspaces skill to list available ML repos.
```

### Tag Already Assigned
```
Tag already exists on another version. Use force=True to reassign it.
```

### Delete Fails — Prompt Has Tagged Versions
```
Cannot delete prompt with tagged versions. Remove tags first, then delete.
```

</troubleshooting>
