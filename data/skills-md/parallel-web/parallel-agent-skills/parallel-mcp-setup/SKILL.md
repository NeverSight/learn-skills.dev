---
name: parallel-mcp-setup
description: Use when installing, configuring, or troubleshooting an authenticated Parallel Search MCP connection in Bifrost, including gateway-level search settings and downstream tool access.
---

# Set up Parallel MCP

Configure and verify authenticated Parallel MCP connections. The first supported setup path is Parallel Search MCP through Bifrost; the steps below apply to that path. Tool descriptions supplied by the MCP server govern search and fetch usage; this skill covers installation and gateway configuration.

## 1. Inspect the deployment

Identify the target Bifrost instance, its configuration source (dashboard or `config.json`), and the intended downstream agent or virtual key. Inspect existing MCP clients before changing anything; update the matching Parallel connection instead of adding duplicates. Preserve unrelated clients, access rules, and tool approval settings.

Confirm access to Bifrost management and a Parallel account credential. These are separate from the downstream agent's Bifrost credential. If access or a secret is missing, prepare the configuration and report what is needed without claiming installation succeeded. Keep secrets in the deployment's secret manager or environment; never put them in skill files, source control, prompts, or tool arguments.

## 2. Configure the authenticated connection

Use `https://search.parallel.ai/mcp-oauth`, which requires authentication. Choose Headers auth for a shared Parallel API key, or Bifrost's OAuth flow when that is the deployment's chosen authentication method. Do not change an authentication failure into an unauthenticated connection.

For shared-key configuration, provision `PARALLEL_MCP_AUTHORIZATION` in the **Bifrost server environment** with the complete value `Bearer <Parallel API key>`. The `env.` reference substitutes the whole header value; it does not prepend `Bearer`.

In **MCP Gateway → New MCP Server**, choose HTTP, the URL above, and Headers auth. Set `Authorization` to the environment-variable reference using the UI's env-var picker. Allow `web_search` and `web_fetch` for this connection.

For a file-managed deployment, merge this client entry into the existing `mcp.client_configs` array:

```json
{
  "name": "parallel-search",
  "connection_type": "http",
  "connection_string": "https://search.parallel.ai/mcp-oauth",
  "auth_type": "headers",
  "headers": {
    "Authorization": "env.PARALLEL_MCP_AUTHORIZATION"
  },
  "is_ping_available": false,
  "tools_to_execute": ["web_search", "web_fetch"]
}
```

For OAuth, use the same endpoint with Bifrost's OAuth auth type and complete its admin verification/sign-in flow. Use per-user authentication only when each caller should use their own Parallel account. See [Bifrost authentication](https://docs.getbifrost.ai/mcp/auth/overview) for the chosen flow.

Respect the deployment's reload procedure. Existing connection URL/auth-type changes may require replacing the client because Bifrost treats those fields as immutable; plan that replacement without deleting a working client first. File-managed entries must be updated in the file as well, or a restart can recreate the old configuration.

## 3. Configure gateway controls and access

Keep Parallel’s defaults by omitting search-setting headers and URL parameters. When the user explicitly requests a particular search mode, source policy, or response budget, read [gateway search controls](./references/gateway-controls.md). Apply these as upstream connection settings. Keep the chosen credential and search policy under gateway administration; do not enable caller-supplied overrides of these headers unless explicitly intended.

Confirm Bifrost discovers both tools and grants the intended downstream client or virtual key access to them. Connect the agent to the deployment's Bifrost MCP gateway with its configured downstream authentication. Use the actual discovered tool names, which may be prefixed. Installing this skill does not itself register or expose the MCP tools.

## 4. Verify through Bifrost

1. Confirm the upstream connection is healthy and authenticated, with `web_search` and `web_fetch` discovered.
2. Confirm the intended downstream agent can discover both tools through Bifrost.
3. Run a small search for official Python asyncio documentation, then fetch a returned documentation URL. Use the tools' current schemas and descriptions. Confirm successful results and inspect per-URL errors.
4. Inspect Bifrost's tool-call records to confirm the intended connection was used. Verify account attribution and any configured mode or source policy in available upstream request metadata or account logs; result quality alone does not prove the mode used.
5. Report exactly what was verified and what remains untested. A direct request to Parallel does not prove Bifrost routing, authentication, or downstream permissions.

On a 401/403, check the Parallel credential, account access, and upstream auth configuration. On a handshake 400, check the configured search overrides. For missing tools, inspect connection health and gateway filtering. Keep existing access controls while diagnosing failures.

## Optional: distribute this setup skill through Bifrost

In **Skills Repository → New Skill**, copy this file's name and description into Details, paste only the Markdown body into the SKILL.md editor, and attach `references/gateway-controls.md`. For an existing skill, create a new version. Publish an initial version such as `1.0.0`, then use **Register as Marketplace** and the dashboard's installation commands; the plugin name is `bifrost-parallel-mcp-setup`.

Bifrost serves newly created skills immediately and documents marketplace/download routes as public. Keep deployment credentials and private configuration out of published files. Skill publication is separate from MCP connection setup.

## Sources

- [Parallel Search MCP](https://docs.parallel.ai/integrations/mcp/search-mcp)
- [Bifrost MCP connections](https://docs.getbifrost.ai/mcp/connecting-to-servers)
- [Bifrost header authentication](https://docs.getbifrost.ai/mcp/auth/headers)
- [Bifrost Skills Repository](https://docs.getbifrost.ai/features/skills-repository)
