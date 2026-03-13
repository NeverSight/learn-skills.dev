---
name: create-mcp-integration
description: Interactive initialization script that scaffolds a new Model Context Protocol (MCP) server integration setup. Use when adding native code tools to an agent's environment.
disable-model-invocation: false
allowed-tools: Bash, Read, Write
---
# MCP Integration Scaffold Generator

You are tasked with generating the scaffolding required to integrate a new Model Context Protocol (MCP) server.

## Execution Steps:

1. **Gather Requirements:**
   Ask the user for:
   - The name of the MCP server.
   - The command/executable required to run it (e.g. `npx -y @modelcontextprotocol/server-postgres`).
   - Any required environment variables (e.g. database URLs, API Keys).

2. **Scaffold the Integration:**
   Using bash file creation tools:
   - If this is going into a Claude Code environment, update the `claude.json` configuration file to include the new server definition under the `mcpServers` object.
   - Ensure you properly map any provided environment variables in the configuration.
   - Scaffold a `CONNECTORS.md` file alongside the integration. This file should map the MCP server's required tool targets to an abstract tag (e.g. mapping `literature_search` tool to the abstract tag `~~literature`), ensuring that plugins remain portable and resilient against underlying MCP server swaps.
   - Create a basic testing script or prompt (perhaps leveraging `create-skill`) that the agent can use to test the new MCP tools once attached. Inform the testing scripts to utilize the abstract `~~tag` rather than hardcoding the actual MCP tool namespace. Ensure this test workflow applies **Conditional Step Inclusion** (e.g., explicitly stating "If Connected" in the header) so it degrades gracefully rather than failing silently if the server isn't running.

3. **Confirmation:**
   Print a success message showing the modified configuration. Instruct the user that they may need to restart their agent environment to pick up the new MCP handles.


## Next Actions
- Offer to run `audit-plugin` to validate the generated artifacts.
