---
name: stackone-cli
description: Build and deploy custom StackOne connectors using the CLI and Connector Engine. Use when user asks to "build a custom connector", "deploy my connector", "use the StackOne AI builder", "set up CI/CD for connectors", "test my connector locally", or "install the StackOne CLI". Covers the full connector development workflow from init through deployment. Do NOT use for using existing connectors (use stackone-connectors) or building AI agents (use stackone-agents).
license: MIT
compatibility: Requires Node.js and npm. Requires network access to fetch live documentation from docs.stackone.com.
metadata:
  author: stackone
  version: "2.0"
---

# StackOne CLI — Connector Development

## Important

The CLI is actively developed and commands change between versions. Before providing CLI guidance:
1. Fetch `https://docs.stackone.com/guides/connector-engine/cli-reference` for the current command reference
2. Fetch `https://www.npmjs.com/package/@stackone/cli` for the latest version

Do not guess CLI commands or flags — always verify against live docs.

## Instructions

### Step 1: Install the CLI

```bash
npm install -g @stackone/cli
```

This installs the global `stackone` command. Verify with `stackone --version`.

### Step 2: Understand when to build a custom connector

Custom connectors are for platforms that StackOne doesn't natively support. Before building one:
- Check if the provider already exists: use the `stackone-connectors` skill or browse https://docs.stackone.com/connectors/introduction
- If the provider exists but is missing specific actions, you may not need a full custom connector — check the Actions RPC endpoint first

### Step 3: Initialize a connector project

Fetch the connector structure guide for the current project layout:
`https://docs.stackone.com/guides/connector-engine/connector-structure`

The Connector Engine provides:
- Project scaffolding
- Local development server for testing
- Type-safe action definitions
- Deployment tooling

### Step 4: Use the AI Builder (optional)

The AI Builder can generate connector scaffolding from API documentation. Fetch the guide:
`https://docs.stackone.com/guides/connector-engine/ai-builder`

This accelerates development by generating boilerplate from an OpenAPI spec or API docs URL.

### Step 5: Test locally

Run the connector locally to test against the target API before deploying. Fetch the CLI reference for the exact test commands:
`https://docs.stackone.com/guides/connector-engine/cli-reference`

### Step 6: Deploy

Deploy to StackOne's infrastructure. For automated deployments, set up CI/CD:
`https://docs.stackone.com/guides/connector-engine/github-workflow`

## Examples

### Example 1: User wants to build a connector for an internal API

User says: "We have an internal HR system. Can I connect it to StackOne?"

Actions:
1. Confirm the internal API has a REST/GraphQL endpoint
2. Install the CLI: `npm install -g @stackone/cli`
3. Fetch the connector structure guide for the scaffolding command
4. If they have an OpenAPI spec, suggest the AI Builder for faster scaffolding
5. Walk through the init → develop → test → deploy flow

Result: Custom connector project initialized with the right structure.

### Example 2: User wants to set up CI/CD for connector deployment

User says: "How do I auto-deploy connectors from GitHub?"

Actions:
1. Fetch `https://docs.stackone.com/guides/connector-engine/github-workflow`
2. Walk through the GitHub Actions workflow configuration
3. Explain the deployment stages (dev → staging → production)

Result: Working GitHub Actions pipeline for connector deployment.

## Troubleshooting

### CLI command not found after install
**Cause**: Global npm bin directory not in PATH.
- Run `npm config get prefix` to find the install location
- Add `{prefix}/bin` to your PATH
- Alternatively, use `npx @stackone/cli` instead of the global command

### Authentication failures in CLI
**Cause**: Missing or invalid credentials.
- The CLI requires a StackOne API key
- Fetch the CLI reference for the current auth setup command
- Verify the key is active at https://app.stackone.com

### Connector deployment fails
**Cause**: Various — check the error message.
- Fetch the CLI reference for deployment troubleshooting
- Common issues: missing required fields in connector config, network timeouts
- For CI/CD failures, check that secrets are correctly configured in GitHub Actions
