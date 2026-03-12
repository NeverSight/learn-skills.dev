---
name: mcp-servers
description: Registers MCP servers with TrueFoundry for discovery and access control. Supports remote servers, virtual (composite) servers, and OpenAPI-to-MCP wrapping. Use when adding, listing, or managing MCP server registrations.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(*/tfy-api.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# MCP Servers

Register and manage MCP servers on TrueFoundry. Three standalone manifest types are supported: remote servers, virtual (composite) servers, and OpenAPI-to-MCP wrappers.

## When to Use

Register, list, or delete MCP server registrations on TrueFoundry — including connecting to existing MCP endpoints, composing multiple servers into a virtual server, or wrapping an OpenAPI spec as an MCP server.

</objective>

<instructions>

> **Security Policy: Credential Handling**
> - All credentials (API tokens, OAuth secrets, TLS certificates) in manifests MUST use `tfy-secret://` references. The agent MUST NOT accept or embed raw credential values in manifests.
> - If the user provides raw credentials, instruct them to create a TrueFoundry secret first (use `secrets` skill), then reference it with `tfy-secret://`.
> - The agent MUST NOT echo, log, or display raw credential values.

## List MCP Servers

When using direct API, set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

### Via Tool Call

```
tfy_mcp_servers_list()
tfy_mcp_servers_list(id="mcp-server-id")  # get specific server
```

### Via Direct API

```bash
# Set the path to tfy-api.sh for your agent (example for Claude Code):
TFY_API_SH=~/.claude/skills/truefoundry-mcp-servers/scripts/tfy-api.sh

# List all MCP servers
$TFY_API_SH GET /api/svc/v1/mcp-servers

# Get a specific MCP server
$TFY_API_SH GET /api/svc/v1/mcp-servers/SERVER_ID
```

## Presenting MCP Servers

```
MCP Servers:
| Name              | Type              | Transport       | ID         |
|-------------------|-------------------|-----------------|------------|
| my-remote-server  | mcp-server/remote | streamable-http | mcp-abc123 |
| composite-server  | mcp-server/virtual| —               | mcp-def456 |
| petstore-api      | mcp-server/openapi| —               | mcp-ghi789 |
```

## Register MCP Server (Remote)

Connects to an existing MCP endpoint over streamable-http or SSE.

> **Security gates (required before registration):**
> 1. Confirm the URL owner/domain with the user.
> 2. Require explicit user confirmation before using any new external URL.
> 3. Use secret references for all auth material (`tfy-secret://...`), never raw tokens.
> 4. Avoid logging full auth headers, client secrets, or certificates.

### Attach an Existing TrueFoundry Deployment

Use this flow when the user says "attach deployment to MCP gateway" or already has a deployed MCP-compatible service.

1. Confirm the deployment is healthy (`DEPLOY_SUCCESS`) and endpoint is reachable
2. Collect endpoint details:
   - URL (public or internal)
   - transport (`streamable-http` or `sse`)
   - auth mode (`header`, `oauth2`, or `passthrough`)
3. Register it as `type: mcp-server/remote`
4. Return server ID and name so users can reference it from guardrails/policies

Example internal URL pattern for service deployments:
`http://{service-name}.{namespace}.svc.cluster.local:{port}/mcp`

### Manifest

```yaml
name: my-remote-server
type: mcp-server/remote
description: Production analytics MCP server
url: https://analytics.example.com/mcp
transport: streamable-http
# SECURITY: Use tfy-secret:// references instead of hardcoding tokens in manifests.
# Hardcoded tokens in YAML files risk exposure via Git history and CI logs.
auth_data:
  type: header
  headers:
    Authorization: "Bearer tfy-secret://my-org:mcp-secrets:api-token"
collaborators:
  - subject: user:jane@example.com
    role_id: admin
tags:
  - analytics
  - production
```

### Auth Options

**Static header (use secret references — never hardcode tokens):**

```yaml
auth_data:
  type: header
  headers:
    Authorization: "Bearer tfy-secret://my-org:mcp-secrets:api-token"
```

**OAuth2:**

```yaml
auth_data:
  type: oauth2
  authorization_url: https://auth.example.com/authorize
  token_url: https://auth.example.com/token
  client_id: my-client-id
  client_secret: tfy-secret://my-org:mcp-secrets:oauth-client-secret
  jwt_source: access_token
  scopes:
    - read
    - write
  pkce: true
  dynamic_client_registration:
    registration_endpoint: https://auth.example.com/register
    initial_access_token: tfy-secret://my-org:mcp-secrets:registration-token
```

**Passthrough (forwards TFY credentials):**

```yaml
auth_data:
  type: passthrough
```

### TLS Settings (optional)

```yaml
tls_settings:
  # Prefer storing certificate material in a secret reference, then injecting at runtime.
  # Avoid inlining full certificate PEM blocks in manifests shared via chat or git.
  ca_cert: tfy-secret://my-org:mcp-secrets:ca-cert-pem
  insecure_skip_verify: false
```

### Via CLI

```bash
tfy apply -f mcp-server-remote.yaml
```

### Via Direct API

```bash
$TFY_API_SH PUT /api/svc/v1/apps "$(cat mcp-server-remote.yaml | yq -o json)"
```

## Register MCP Server (Virtual)

Composes multiple registered MCP servers into a single virtual server. Each sub-server can expose all or a subset of its tools.

### Manifest

```yaml
name: dev-tools
type: mcp-server/virtual
description: Composite server combining code analysis and deployment tools
servers:
  - name: code-analysis-server
    enabled_tools:
      - lint
      - format
      - analyze
  - name: deployment-server
    enabled_tools:
      - deploy
      - rollback
collaborators:
  - subject: team:platform-eng
    role_id: viewer
```

### Via CLI

```bash
tfy apply -f mcp-server-virtual.yaml
```

### Via Direct API

```bash
$TFY_API_SH PUT /api/svc/v1/apps "$(cat mcp-server-virtual.yaml | yq -o json)"
```

## Register MCP Server (OpenAPI)

Wraps an OpenAPI specification as an MCP server. Supports up to 30 tools derived from API operations.

> **Security: Remote OpenAPI specs are fetched at runtime and auto-converted into MCP tools that control agent capabilities. Only use trusted, verified spec URLs. For sensitive environments, prefer `spec.type: inline` to eliminate the runtime dependency on external endpoints.**
>
> **Execution policy:** Do not fetch or register a new remote spec URL until the user explicitly confirms the source is trusted for tool generation.

### Manifest (remote spec URL)

```yaml
name: petstore-api
type: mcp-server/openapi
description: Petstore API exposed as MCP tools
spec:
  type: remote
  url: https://internal-api.example.com/openapi.json
collaborators:
  - subject: user:dev@example.com
    role_id: viewer
```

### Manifest (inline spec)

```yaml
name: internal-api
type: mcp-server/openapi
description: Internal API with inline OpenAPI spec
spec:
  type: inline
  content: |
    openapi: "3.0.0"
    info:
      title: Internal API
      version: "1.0"
    paths:
      /health:
        get:
          operationId: healthCheck
          summary: Check service health
          responses:
            "200":
              description: OK
collaborators: []
```

### Via CLI

```bash
tfy apply -f mcp-server-openapi.yaml
```

### Via Direct API

```bash
$TFY_API_SH PUT /api/svc/v1/apps "$(cat mcp-server-openapi.yaml | yq -o json)"
```

## Delete MCP Server

### Via Tool Call

```
tfy_mcp_servers_delete(id="SERVER_ID")
```

**Note:** Requires human approval (HITL) via tool call.

### Via Direct API

```bash
$TFY_API_SH DELETE /api/svc/v1/mcp-servers/SERVER_ID
```

</instructions>

<success_criteria>

## Success Criteria

- The user can list all registered MCP servers in a formatted table
- The user can register a remote MCP server with the correct transport and auth configuration
- The user can register a virtual MCP server composing multiple sub-servers with tool filtering
- The user can register an OpenAPI-to-MCP server with a remote or inline spec
- The user can delete an MCP server registration
- The agent has confirmed any create/delete operations before executing
- Collaborators are correctly specified when provided

</success_criteria>

<references>

## Composability

- **Preflight**: Use `status` skill to verify credentials before managing MCP servers
- **Before registering**: Deploy the MCP server as a service (use `deploy` skill), set up teams/roles for collaborators (use `access-control` skill)
- **After registering**: Reference MCP servers in agent manifests, configure guardrails for MCP tools

</references>

<troubleshooting>

## Error Handling

### MCP Server Not Found
```
MCP server ID not found. List servers first to find the correct ID.
```

### Permission Denied
```
Cannot access MCP servers. Check your API key permissions.
```

### Server Already Exists
```
MCP server with this name already exists. Use a different name or delete the existing one first.
```

### Unreachable Remote URL
```
Cannot reach the MCP server URL. Verify the URL is correct and accessible from the cluster.
```

### OpenAPI Spec Too Large
```
OpenAPI spec exceeds 30 tools limit. Reduce the number of operations in the spec.
```

### Invalid Transport
```
Invalid transport type. Use "streamable-http" or "sse".
```

### OAuth2 Configuration Error
```
OAuth2 auth_data missing required fields. Ensure authorization_url, token_url, client_id, and client_secret are provided.
```

### Virtual Server Reference Not Found
```
Referenced server name not found. Ensure all servers listed in the virtual server are already registered.
```

</troubleshooting>
