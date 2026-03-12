---
name: access-tokens
description: Manages TrueFoundry personal access tokens (PATs). List, create, and delete tokens for API auth, CI/CD, and gateway access.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(*/tfy-api.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# Access Tokens

Manage TrueFoundry personal access tokens (PATs). List, create, and delete tokens used for API authentication, CI/CD pipelines, and AI Gateway access.

## When to Use

List, create, or delete personal access tokens for API authentication, CI/CD pipelines, or AI Gateway access.

</objective>

<instructions>

> **Security Policy: Credential Handling**
> - The agent MUST NOT repeat, store, or log token values in its own responses.
> - After creating a token, direct the user to copy the value from the API response output above — do not re-display it.
> - Never include token values in summaries, follow-up messages, or any other output.

## Step 1: Preflight

Run the `status` skill first to verify `TFY_BASE_URL` and `TFY_API_KEY` are set and valid.

When using direct API, set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

## Step 2: List Access Tokens

### Via Tool Call
```
tfy_access_tokens_list()
```

### Via Direct API
```bash
TFY_API_SH=~/.claude/skills/truefoundry-access-tokens/scripts/tfy-api.sh

# List all personal access tokens
$TFY_API_SH GET /api/svc/v1/personal-access-tokens
```

Present results:
```
Personal Access Tokens:
| Name          | ID       | Created At  | Expires At  |
|---------------|----------|-------------|-------------|
| ci-pipeline   | pat-abc  | 2025-01-15  | 2025-07-15  |
| dev-local     | pat-def  | 2025-03-01  | Never       |
```

**Security:** Never display token values. They are only shown once at creation time.

## Step 3: Create Access Token

Ask the user for a token name before creating.

### Via Tool Call
```
tfy_access_tokens_create(payload={"name": "my-token"})
```

**Note:** Requires human approval (HITL) via tool call.

### Via Direct API
```bash
# Create a new personal access token
$TFY_API_SH POST /api/svc/v1/personal-access-tokens '{"name":"my-token"}'
```

**IMPORTANT:** The token value is returned ONLY in the creation response.

> **Security: Token Display Policy**
> - Default to showing only a masked preview (for example: first 4 + last 4 characters).
> - Show the full token only after explicit user confirmation that they are ready to copy it now.
> - If a full token is shown, show it only once, in a minimal response, and never repeat it in summaries/follow-up messages.
> - The agent must NEVER store, log, or re-display the token value after the initial one-time reveal.
> - If the user asks to see the token again later, instruct them to create a new token.

Present the result:
```
Token created successfully!
Name: my-token
Token (masked): tfy_****...****

If user explicitly confirms they are ready to copy it:
One-time token: <full value from API response>

⚠️  Save this token NOW — it will not be shown again.
Store it in a password manager, CI/CD secret store, or TrueFoundry secret group.
Never commit tokens to Git or share them in plain text.
```

## Step 4: Delete Access Token

Ask for confirmation before deleting — this is irreversible and will break any integrations using the token.

### Via Tool Call
```
tfy_access_tokens_delete(id="TOKEN_ID")
```

**Note:** Requires human approval (HITL) via tool call.

### Via Direct API
```bash
# Delete a personal access token
$TFY_API_SH DELETE /api/svc/v1/personal-access-tokens/TOKEN_ID
```

</instructions>

<success_criteria>

## Success Criteria

- The user can list all personal access tokens in a formatted table
- The user can create a new token and receives a masked preview by default
- Full token reveal happens only on explicit confirmation and only once
- The user has been warned to save the token value immediately
- The user can delete a token after confirmation
- The agent has never displayed existing token values — only new tokens at creation time

</success_criteria>

<references>

## Composability

- **AI Gateway**: PATs are used to authenticate AI Gateway requests (`ai-gateway` skill)
- **GitOps / CI/CD**: PATs are needed for automated deployments (`gitops` skill, `deploy` skill declarative apply workflow)
- **Status**: Use `status` skill to verify a PAT is working
- **Secrets**: Store PATs as secrets for deployments (`secrets` skill)

## API Endpoints

See `references/api-endpoints.md` for the full Personal Access Tokens API reference.

</references>

<troubleshooting>

## Error Handling

### Permission Denied
```
Cannot manage access tokens. Check your API key permissions.
```

### Token Not Found
```
Token ID not found. List tokens first to find the correct ID.
```

### Token Name Already Exists
```
A token with this name already exists. Use a different name.
```

### Deleted Token Still In Use
```
If services fail after token deletion, they were using the deleted token.
Create a new token and update the affected services/pipelines.
```

### Cannot Retrieve Token Value
```
Token values are only shown at creation time. If lost, delete the old token
and create a new one, then update all services that used the old token.
```

</troubleshooting>
