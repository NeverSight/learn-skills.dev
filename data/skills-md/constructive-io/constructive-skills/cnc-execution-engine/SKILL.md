---
name: cnc-execution-engine
description: Execute GraphQL queries against Constructive APIs using the cnc CLI. Use when asked to "run a query", "execute GraphQL", "set up API context", "configure API token", "manage API endpoints", or when working with Constructive GraphQL APIs.
compatibility: Node.js 18+, cnc CLI (constructive-io/constructive)
metadata:
  author: constructive-io
  version: "1.0.0"
---

# CNC Execution Engine

Execute raw GraphQL queries against Constructive APIs using the `cnc` CLI. Manage multiple API contexts (endpoint + credentials) similar to kubectl contexts.

## When to Apply

Use this skill when:
- Executing GraphQL queries against Constructive APIs
- Setting up API endpoint configurations
- Managing API tokens for authentication
- Switching between multiple API environments (dev, staging, prod)
- Testing GraphQL queries from the command line

## Quick Start

```bash
# Create a context with an endpoint
cnc context create my-api --endpoint https://api.example.com/graphql

# Set your API token (input is masked)
cnc auth set-token

# Execute a query
cnc execute --query 'query { __typename }'
```

## Context Management

Contexts store endpoint URLs and are similar to kubectl contexts. They are stored in `~/.cnc/config/contexts/`.

### Create a Context

```bash
# Interactive mode
cnc context create

# With flags
cnc context create my-api --endpoint https://api.example.com/graphql
```

### List Contexts

```bash
cnc context list
```

Output shows all contexts with authentication status:

```
Contexts:

* my-api [authenticated]
    Endpoint: https://api.example.com/graphql

  staging [no token]
    Endpoint: https://staging.example.com/graphql
```

### Switch Context

```bash
cnc context use staging
```

### Show Current Context

```bash
cnc context current
```

### Delete a Context

```bash
cnc context delete old-api
```

## Authentication

Tokens are stored securely in `~/.cnc/config/credentials.json` with restricted file permissions (0o600).

### Set Token

```bash
# Interactive (input masked with asterisks)
cnc auth set-token

# With token as argument
cnc auth set-token eyJhbGciOiJIUzI1NiIs...

# For a specific context
cnc auth set-token --context staging

# With expiration
cnc auth set-token --expires 2024-12-31T23:59:59Z
```

### Check Auth Status

```bash
cnc auth status
```

Output:

```
Authentication Status:

* my-api
    Status: Authenticated
    Token:  eyJhbG...s5Nw
    Expires: 2024-12-31T23:59:59Z

  staging
    Status: Not authenticated
```

### Logout

```bash
cnc auth logout
cnc auth logout --context staging
```

## Executing Queries

### Inline Query

```bash
cnc execute --query 'query { databases { nodes { id name } } }'
```

### From File

```bash
cnc execute --file query.graphql
```

### With Variables

```bash
cnc execute --query 'query($id: UUID!) { database(id: $id) { name } }' \
  --variables '{"id":"550e8400-e29b-41d4-a716-446655440000"}'
```

### Using a Specific Context

```bash
cnc execute --query 'query { __typename }' --context staging
```

## Output Format

Successful queries return JSON:

```
Context: my-api
Endpoint: https://api.example.com/graphql

Success!

{
  "databases": {
    "nodes": [
      { "id": "...", "name": "my-database" }
    ]
  }
}
```

Failed queries show errors:

```
Failed!

  - Field "nonexistent" not found
    Path: query.nonexistent
```

## Common Workflows

### Setting Up a New Environment

```bash
# Create context for production
cnc context create prod --endpoint https://api.constructive.io/graphql

# Set the API token
cnc auth set-token

# Verify connection
cnc execute --query 'query { __typename }'
```

### Working with Multiple Environments

```bash
# Create contexts for each environment
cnc context create dev --endpoint https://dev-api.example.com/graphql
cnc context create staging --endpoint https://staging-api.example.com/graphql
cnc context create prod --endpoint https://api.example.com/graphql

# Set tokens for each
cnc auth set-token --context dev
cnc auth set-token --context staging
cnc auth set-token --context prod

# Switch between environments
cnc context use dev
cnc execute --query 'query { databases { nodes { id } } }'

cnc context use prod
cnc execute --query 'query { databases { nodes { id } } }'
```

### Scripting with CNC

```bash
#!/bin/bash
# Example: Query all databases and save to file

cnc context use prod
cnc execute --query 'query { databases { nodes { id name createdAt } } }' > databases.json
```

## CLI Reference

### cnc context

| Command | Description |
|---------|-------------|
| `cnc context create <name>` | Create a new context |
| `cnc context list` | List all contexts |
| `cnc context use <name>` | Switch to a context |
| `cnc context current` | Show current context details |
| `cnc context delete <name>` | Delete a context |

**Create Options:**
- `--endpoint <url>` - GraphQL endpoint URL

### cnc auth

| Command | Description |
|---------|-------------|
| `cnc auth set-token [token]` | Set API token (masked input if no token provided) |
| `cnc auth status` | Show authentication status for all contexts |
| `cnc auth logout` | Remove credentials for current context |

**Options:**
- `--context <name>` - Target a specific context
- `--expires <date>` - Token expiration date (ISO format)

### cnc execute

| Option | Description |
|--------|-------------|
| `--query <graphql>` | GraphQL query/mutation string |
| `--file <path>` | Path to file containing GraphQL query |
| `--variables <json>` | Variables as JSON string |
| `--context <name>` | Context to use (defaults to current) |

## File Locations

| Path | Purpose |
|------|---------|
| `~/.cnc/config/contexts/` | Context configuration files |
| `~/.cnc/config/settings.json` | Global settings (current context) |
| `~/.cnc/config/credentials.json` | API tokens (mode 0o600) |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No active context" | Run `cnc context create` or `cnc context use` |
| "No valid credentials" | Run `cnc auth set-token` |
| "Context not found" | Check `cnc context list` for available contexts |
| Token expired | Run `cnc auth set-token` to set a new token |
| Connection refused | Verify endpoint URL with `cnc context current` |

## Environment Variables

The CLI respects standard environment variables but stored context/credentials take precedence:

| Variable | Description |
|----------|-------------|
| `CNC_ENDPOINT` | Override endpoint URL |
| `CNC_TOKEN` | Override API token |

## References

- CLI source: `packages/cli/` in constructive-io/constructive
- Config management uses `appstash` for directory resolution
- Related skill: `constructive-graphql-codegen` for generating typed hooks/ORM
