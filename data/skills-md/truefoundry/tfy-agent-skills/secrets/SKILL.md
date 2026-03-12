---
name: secrets
description: Manages TrueFoundry secret groups and secrets. Handles listing, creating, updating, and deleting secret groups and individual key-value secrets.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(*/tfy-api.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# Secrets

Manage TrueFoundry secret groups and secrets. Secret groups organize secrets; individual secrets hold key-value pairs.

## When to Use

List, create, update, or delete secret groups and individual secrets on TrueFoundry, including pre-deploy secret setup and value rotation.

</objective>

<instructions>

> **Security Policy: Credential Handling**
> - The agent MUST NOT accept, store, log, echo, or display raw secret values in any context.
> - Always instruct the user to set secret values as environment variables before running commands.
> - If the user provides a raw secret value directly in conversation, warn them and refuse to use it. Instruct them to set it as an env var instead.
> - When displaying secrets, show only "(set)" or the first 4 characters followed by "***".

## List Secret Groups

When using direct API, set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

### Via Tool Call

```
tfy_secrets_list()
tfy_secrets_list(secret_group_id="group-id")  # get group + secrets
tfy_secrets_list(secret_id="secret-id")        # get one secret
```

### Via Direct API

```bash
# Set the path to tfy-api.sh for your agent (example for Claude Code):
TFY_API_SH=~/.claude/skills/truefoundry-secrets/scripts/tfy-api.sh

# List all secret groups
$TFY_API_SH GET /api/svc/v1/secret-groups

# Get a specific group
$TFY_API_SH GET /api/svc/v1/secret-groups/GROUP_ID

# List secrets in a group
$TFY_API_SH POST /api/svc/v1/secrets '{"secretGroupId":"GROUP_ID","limit":100,"offset":0}'

# Get a specific secret
$TFY_API_SH GET /api/svc/v1/secrets/SECRET_ID
```

## Presenting Secrets

```
Secret Groups:
| Name          | ID       | Secrets |
|---------------|----------|---------|
| prod-secrets  | sg-abc   | 5       |
| dev-secrets   | sg-def   | 3       |
```

**Security:** Never display secret values in full. Show only the first few characters or indicate "(set)". The agent must NEVER log, echo, or output raw secret values in any context.

## Create Secret Group

> **Security: Credential Handling**
> - The agent must NEVER accept, echo, or transmit raw secret values inline.
> - Never ask the user to paste secret values in chat.
> - Always instruct the user to store secret values in environment variables first, then reference those variables.
> - If the user provides a raw secret value directly, warn them and suggest using an env var instead.

### Via Tool Call

```
# Prompt user to set secret values as environment variables first
tfy_secret_groups_create(payload={"name": "my-secrets", ...})
```

**Note:** Requires human approval (HITL) via tool call.

### Via Direct API

```bash
# SECURITY: Never hardcode secret values in commands — they will appear in shell
# history and process listings. Read from environment variables or files instead.
# User must set: export DB_PASSWORD="..." before running this command.
payload=$(jq -n \
  --arg name "my-secrets" \
  --arg integration "INTEGRATION_ID" \
  --arg db_password "$DB_PASSWORD" \
  '{
    name: $name,
    integrationId: $integration,
    secrets: [{key: "DB_PASSWORD", value: $db_password}]
  }')
$TFY_API_SH POST /api/svc/v1/secret-groups "$payload"
```

## Update Secret Group

Updates secrets in a group. A new version is created for every secret with a modified value. Secrets omitted from the array are deleted. At least one secret is required.

### Via Tool Call

```
# Instruct user to set env vars with new values, then reference them.
# The agent must NEVER accept raw secret values — always use indirection.
tfy_secret_groups_update(
  id="GROUP_ID",
  payload={"secrets": [{"key": "DB_PASSWORD", "value": "<secure-input-from-env>"}, {"key": "API_KEY", "value": "<secure-input-from-env>"}]}
)
```

**Note:** Requires human approval (HITL) via tool call.

### Via Direct API

```bash
# SECURITY: Read secret values from environment variables, not inline.
payload=$(jq -n \
  --arg db_password "$DB_PASSWORD" \
  --arg api_key "$NEW_API_KEY" \
  '{
    secrets: [
      {key: "DB_PASSWORD", value: $db_password},
      {key: "API_KEY", value: $api_key}
    ]
  }')
$TFY_API_SH PUT /api/svc/v1/secret-groups/GROUP_ID "$payload"
```

## Delete Secret Group

### Via Tool Call

```
tfy_secret_groups_delete(id="GROUP_ID")
```

**Note:** Requires human approval (HITL) via tool call.

### Via Direct API

```bash
$TFY_API_SH DELETE /api/svc/v1/secret-groups/GROUP_ID
```

## Finding the Integration ID

Before creating a secret group, you need the secret store integration ID for the workspace's cloud provider:

### Via Direct API

```bash
# List all secret store provider accounts and their integrations
bash $TFY_API_SH GET '/api/svc/v1/provider-accounts?type=secret-store'
```

From the response, look for integrations with `type: "secret-store"`. Each provider account contains an `integrations` array -- pick the integration matching the workspace's cloud provider:
- AWS: `integration/secret-store/aws/secrets-manager` or `integration/secret-store/aws/parameter-store`
- Azure: `integration/secret-store/azure/vault`
- GCP: `integration/secret-store/gcp/secret-manager`

Use the `id` field of the matching integration as the `integrationId` when creating secret groups.

## Using Secrets in Deployments

After creating a secret group, reference individual secrets in deployment manifests using the `tfy-secret://` format:

```
tfy-secret://<TENANT_NAME>:<SECRET_GROUP_NAME>:<SECRET_KEY>
```

- `TENANT_NAME`: The subdomain of `TFY_BASE_URL` (e.g., `my-org` from `https://my-org.truefoundry.cloud`)
- `SECRET_GROUP_NAME`: The name you gave the secret group when creating it
- `SECRET_KEY`: The key of the individual secret within the group

### Example: Manifest with Secret References

Given a secret group named `my-app-secrets` with keys `DB_PASSWORD` and `API_KEY`:

```yaml
name: my-app
type: service
image:
  type: image
  image_uri: docker.io/myorg/my-app:latest
ports:
  - port: 8000
    expose: false
    app_protocol: http
resources:
  cpu_request: 0.5
  cpu_limit: 1
  memory_request: 512
  memory_limit: 1024
  ephemeral_storage_request: 1000
  ephemeral_storage_limit: 2000
env:
  LOG_LEVEL: info
  DB_PASSWORD: tfy-secret://my-org:my-app-secrets:DB_PASSWORD
  API_KEY: tfy-secret://my-org:my-app-secrets:API_KEY
workspace_fqn: cluster-id:workspace-name
```

### Workflow: Secrets Before Deploy

1. Identify sensitive env vars (passwords, tokens, keys, credentials)
2. Find the secret store integration ID (see above)
3. Create a secret group with all sensitive values
4. Reference secrets in the manifest `env` using `tfy-secret://` format
5. Deploy with `tfy apply -f manifest.yaml`

## Delete Individual Secret

### Via Tool Call

```
tfy_secrets_delete(id="SECRET_ID")
```

**Note:** Requires human approval (HITL) via tool call.

### Via Direct API

```bash
$TFY_API_SH DELETE /api/svc/v1/secrets/SECRET_ID
```

</instructions>

<success_criteria>

## Success Criteria

- The user can list all secret groups and see their contents in a formatted table
- The user can create a new secret group with a specified name
- The user can update secrets in a group (rotate values, add/remove keys)
- The user can delete a secret group or an individual secret
- The agent has never displayed full secret values — only masked or "(set)" indicators
- The user can inspect individual secrets within a group by ID
- The agent has confirmed any create/update/delete operations before executing

</success_criteria>

<references>

## Composability

- **Before deploy**: Create secret groups, then reference in deployment config
- **After listing**: Get individual secrets by ID for inspection
- **With applications**: Reference secret groups in application env vars

</references>

<troubleshooting>

## Error Handling

### Secret Group Not Found
```
Secret group ID not found. List groups first to find the correct ID.
```

### Permission Denied
```
Cannot access secrets. Check your API key permissions.
```

### Secret Already Exists
```
Secret group with this name already exists. Use a different name.
```

### At Least One Secret Required
```
Cannot update secret group with zero secrets. Include at least one secret in the payload.
```

### No Secret Store Configured
```
No secret store configured for this workspace. Contact your platform admin.
```

### Key Name Restrictions (Azure Key Vault)
```
Key name does not support underscores (_)
```
Azure Key Vault does not allow underscores in secret key names. Use hyphens (`DB-PASSWORD`) or choose a different secret store integration (AWS Secrets Manager supports underscores).

### Azure Key Vault: Secret Stuck in Soft-Delete State
```
Error: Secret <name> is already in a deleted state / conflict with soft-deleted resource
```
Azure Key Vault has a default 90-day soft-delete retention. The TrueFoundry API cannot purge soft-deleted secrets — only the Azure portal or CLI can.

**Recovery options:**
1. **Purge via Azure Portal:** Go to Key Vault → Manage deleted secrets → Purge
2. **Purge via Azure CLI:** `az keyvault secret purge --vault-name <vault> --name <secret-name>`
3. **Use a different name:** Create a new secret group with a different name (fastest workaround)

> **Note:** If the platform's Key Vault has soft-delete protection but not purge protection, options 1/2 work. If purge protection is also enabled, you must wait out the retention period (up to 90 days).

### Missing Required Fields
```
Unprocessable entity. Ensure all secrets have both "key" and "value" fields.
```

</troubleshooting>
