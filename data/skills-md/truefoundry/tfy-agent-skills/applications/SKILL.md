---
name: applications
description: Lists, inspects, and manages TrueFoundry application deployments. Shows status, health, and details for services, jobs, and Helm releases. Also handles requests to delete, remove, or destroy applications by directing users to the TrueFoundry UI.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(*/tfy-api.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# Applications

List, inspect, and manage applications and deployments on TrueFoundry.

## When to Use

List, inspect, or manage deployed applications and their deployment history. Also supports creating deployments via API manifest for pre-built images.

## When NOT to Use

- User wants to deploy local code → prefer `deploy` skill; ask if the user wants another valid path
- User wants workspace/cluster info → prefer `workspaces` skill; ask if the user wants another valid path
- User wants to delete an application → guide them to the TrueFoundry UI (see "Deleting Applications" below)

</objective>

<instructions>

## Execution Priority

For simple read/list operations in this skill, always use MCP tool calls first:
- `tfy_applications_list`
- `tfy_applications_list_deployments`

If tool calls are unavailable because the MCP server is not configured, or a tool is missing, fall back automatically to direct API via `tfy-api.sh`.

## IMPORTANT: Deleting Applications

**Deletion is NOT supported via CLI, API, or any agent tool. Do NOT call any delete endpoint or attempt to delete applications programmatically.**

When a user asks to delete, remove, or destroy an application, **do NOT list apps for selection**. Instead, immediately respond with:

```
To delete an application, use the TrueFoundry dashboard:

1. Open your TrueFoundry dashboard (TFY_BASE_URL in your browser)
2. Navigate to **Deployments** → select the workspace
3. Find the application you want to delete
4. Click the **three-dot menu (⋮)** on the application card → **Delete**
5. Confirm the deletion when prompted

⚠️ This action is irreversible — all pods, endpoints, and deployment history for this application will be permanently removed.
```

**Do NOT attempt to call any delete API on behalf of the user. Do NOT list applications to ask which one to delete. Simply provide the UI instructions above.**

---

## List Applications

When using direct API, set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

### Via Tool Call

```
tfy_applications_list()
tfy_applications_list(filters={"workspace_fqn": "my-cluster:my-workspace"})
tfy_applications_list(filters={"application_name": "my-app"})
tfy_applications_list(app_id="app-id-here")
```

### Via Direct API

```bash
# Set the path to tfy-api.sh for your agent (example for Claude Code):
TFY_API_SH=~/.claude/skills/truefoundry-applications/scripts/tfy-api.sh

# List all
$TFY_API_SH GET /api/svc/v1/apps

# Filter by workspace
$TFY_API_SH GET '/api/svc/v1/apps?workspaceFqn=my-cluster:my-workspace'

# Filter by name
$TFY_API_SH GET '/api/svc/v1/apps?applicationName=my-app'

# Get by ID
$TFY_API_SH GET /api/svc/v1/apps/APP_ID
```

### Filter Parameters

| Parameter | API Key | Description |
|-----------|---------|-------------|
| `workspace_fqn` | `workspaceFqn` | Filter by workspace FQN |
| `application_name` | `applicationName` | Filter by app name |
| `cluster_id` | `clusterId` | Filter by cluster |
| `application_type` | `applicationType` | Filter: service, job, etc. |
| `name_search_query` | `nameSearchQuery` | Search by name substring |

## Presenting Applications

Show as a table. Use `updatedAt` from the API response for "Last Deployed" (ISO 8601 timestamp — format as date/time for readability). Use `kind` for Type and `status` for Status.

```
Applications in my-cluster:my-workspace:
| Name           | Type    | Status   | Last Deployed      |
|----------------|---------|----------|--------------------|
| tfy-tool-server | service | RUNNING  | 2026-02-10 14:30   |
| data-pipeline  | job     | STOPPED  | 2026-02-08 09:15   |
```

## List Deployments

### Via Tool Call

```
tfy_applications_list_deployments(app_id="app-id")
tfy_applications_list_deployments(app_id="app-id", deployment_id="dep-id")
```

### Via Direct API

```bash
# List deployments for an app
$TFY_API_SH GET /api/svc/v1/apps/APP_ID/deployments

# Get specific deployment
$TFY_API_SH GET /api/svc/v1/apps/APP_ID/deployments/DEPLOYMENT_ID
```

## Create Deployment (API)

For creating a deployment via API manifest (advanced — most users should use the `deploy` skill).

**Use this section when:**
- User has their own manifest/JSON and wants direct API deployment
- User explicitly requests API-based deployment instead of SDK/Python
- User wants to deploy from a pre-built image (not local code)

**For deploying local code, use the `deploy` skill instead.**

### Service Manifest Structure

A basic TrueFoundry service manifest looks like this:

```json
{
  "manifest": {
    "kind": "Service",
    "name": "my-app",
    "image": {
      "type": "image",
      "image_uri": "nginx:latest"
    },
    "ports": [
      {
        "port": 8000,
        "protocol": "TCP",
        "expose": false
      }
    ],
    "resources": {
      "cpu_request": 0.25,
      "cpu_limit": 0.5,
      "memory_request": 256,
      "memory_limit": 512
    },
    "env": {
      "APP_MODE": "production",
      "THIRD_PARTY_API_KEY": "tfy-secret://my-org:my-app-secrets:THIRD_PARTY_API_KEY"
    },
    "replicas": {
      "min": 1,
      "max": 1
    }
  },
  "workspaceId": "ws-id-here"
}
```

**Key Fields:**
- `kind` — "Service" for long-running services, "Job" for batch jobs
- `name` — Unique application name
- `image.image_uri` — Docker image (e.g., `nginx:latest`, `ghcr.io/org/app:v1.0`)
- `ports` — Array of port configs (port, protocol, expose flag)
- `resources` — CPU (cores) and memory (MB) requests/limits
- `env` — Environment variables as key-value pairs. **Security:** Never include raw secret values (passwords, API keys, tokens) in manifests. Use `tfy-secret://` references for all sensitive environment variables. See the `secrets` skill.
- `replicas` — Min/max replica count (for autoscaling)
- `workspaceId` — Workspace ID (not FQN) where the app will be deployed

### Before Submitting

> **Security: Credential Handling**
> - NEVER embed raw API keys, passwords, or tokens in manifest `env` fields.
> - Always use `tfy-secret://` references for sensitive environment variables.
> - If the user provides a raw credential, warn them and suggest creating a TrueFoundry secret group first (use the `secrets` skill).
> - Never ask the user to paste secret values directly into the conversation.

**ALWAYS confirm with the user before creating a deployment:**

1. **Service name** — What should the app be called?
2. **Image** — Full image URI (e.g., `nginx:latest`, `ghcr.io/user/app:tag`)
3. **Resources** — CPU request/limit (cores), memory request/limit (MB)
4. **Ports** — Which ports to expose, protocols (TCP/UDP), expose to internet?
5. **Environment variables** — Any env vars needed? (For sensitive values, only accept `tfy-secret://` references — never inline credentials in manifests)
6. **Replicas** — How many instances? (min/max for autoscaling)
7. **Workspace ID** — Which workspace to deploy to?

Present this summary and ask for confirmation before making the API call.

### Via Tool Call

```
tfy_applications_create_deployment(
    manifest={
        "kind": "Service",
        "name": "my-app",
        "image": {"type": "image", "image_uri": "nginx:latest"},
        "ports": [{"port": 8000, "protocol": "TCP", "expose": false}],
        "resources": {"cpu_request": 0.25, "cpu_limit": 0.5, "memory_request": 256, "memory_limit": 512},
        "env": {"APP_MODE": "production", "THIRD_PARTY_API_KEY": "tfy-secret://my-org:my-app-secrets:THIRD_PARTY_API_KEY"},
        "replicas": {"min": 1, "max": 1}
    },
    options={"workspace_id": "ws-id-here", "force_deploy": true}
)
```

**Note:** This requires human approval (HITL) when using tool calls.

### Via Direct API

```bash
$TFY_API_SH PUT /api/svc/v1/apps '{
  "manifest": {
    "kind": "Service",
    "name": "my-app",
    "image": {"type": "image", "image_uri": "nginx:latest"},
    "ports": [{"port": 8000, "protocol": "TCP", "expose": false}],
    "resources": {"cpu_request": 0.25, "cpu_limit": 0.5, "memory_request": 256, "memory_limit": 512},
    "env": {"APP_MODE": "production", "THIRD_PARTY_API_KEY": "tfy-secret://my-org:my-app-secrets:THIRD_PARTY_API_KEY"},
    "replicas": {"min": 1, "max": 1}
  },
  "workspaceId": "ws-id-here"
}'
```

### Common Deployment Patterns

**Web service (exposed to internet with public URL):**

The `host` must match one of the cluster's `base_domains`. Look up base domains first:
```bash
$TFY_API_SH GET /api/svc/v1/clusters/CLUSTER_ID
# → look for base_domains, pick the wildcard one (e.g., "*.ml.your-org.truefoundry.cloud")
# → strip "*." to get the base domain: "ml.your-org.truefoundry.cloud"
# → construct host: "{service-name}-{workspace-name}.{base_domain}"
```

```json
{
  "ports": [{
    "port": 8080,
    "protocol": "TCP",
    "expose": true,
    "host": "my-app-dev-ws.ml.your-org.truefoundry.cloud",
    "app_protocol": "http"
  }],
  "replicas": {"min": 2, "max": 5}
}
```

**If `host` does not match a cluster base domain, deploy will fail with: "Provided host is not configured in cluster".**

**Internal service (not exposed):**
```json
{
  "ports": [{"port": 8000, "protocol": "TCP", "expose": false}],
  "replicas": {"min": 1, "max": 1}
}
```

**Resource-intensive service:**
```json
{
  "resources": {
    "cpu_request": 1.0,
    "cpu_limit": 2.0,
    "memory_request": 2048,
    "memory_limit": 4096
  }
}
```

</instructions>

<success_criteria>

## Success Criteria

- The user can see the status of their deployed applications in a clear, formatted table
- Unhealthy or stopped deployments are identified with actionable next steps (check logs, redeploy)
- The agent has filtered results by the correct workspace when the user specified one
- The user can find a specific application by name, ID, or workspace
- Deployment details (replicas, resources, image, ports) are surfaced when the user asks for more info

</success_criteria>

<references>

## Composability

- **After listing apps**: Use `logs` skill to check logs, `deploy` skill to redeploy
- **After deploy**: Use this skill to verify the deployment succeeded
- **Check jobs**: Use `jobs` skill for job-specific run details
- **Find workspace first**: Use `workspaces` skill to get workspace FQN for filtering

</references>

<troubleshooting>

## Error Handling

### No Applications Found
```
No applications found. Check:
- Workspace FQN is correct
- You have apps deployed in this workspace
- Your API key has access to this workspace
```

### Application Not Found
```
Application ID not found. List apps first to find the correct ID.
```

### Permission Denied
```
Cannot access this application. Check your API key permissions.
```

</troubleshooting>
