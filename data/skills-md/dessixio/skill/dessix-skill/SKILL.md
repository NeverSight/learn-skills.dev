---
name: dessix-skill
description: Access a local Dessix desktop workspace by calling the Electron MCP bridge directly from Node.js (socket/pipe), without using MCP stdio JSON-RPC. Use when an agent needs to read or invoke Dessix tools programmatically, build local automations, or fetch Action/Scene prompt content from Dessix blocks.
metadata:
  {"openclaw": {"requires": {"env": ["DESSIX_MCP_BRIDGE_ENDPOINT"], "bins": ["node"]}, "primaryEnv": "DESSIX_MCP_BRIDGE_ENDPOINT", "os": ["darwin", "linux", "win32"], "homepage": "https://github.com/DessixIO/skill"}}
---

# Dessix Skill

Call the local Dessix bridge directly through a line-delimited JSON socket protocol.

Use `scripts/dessix-bridge.mjs` for all requests instead of re-implementing socket logic.

## Workflow

1. (Optional) Locate bundled MCP script path dynamically:

```bash
node scripts/dessix-bridge.mjs locate-mcp-script
```

2. Verify the bridge is reachable:

```bash
node scripts/dessix-bridge.mjs health
```

3. List workspaces:

```bash
node scripts/dessix-bridge.mjs invoke \
  --tool dessix_list_workspaces \
  --args '{}'
```

4. Call target tool with JSON args:

```bash
node scripts/dessix-bridge.mjs invoke \
  --tool dessix_search_blocks \
  --args '{"query":"MCP","limit":10}'
```

5. Read a Skill prompt from an Action/Scene block:

```bash
node scripts/dessix-bridge.mjs invoke \
  --tool dessix_get_skill \
  --args '{"block_id":"<BLOCK_ID>"}'
```

## Notes

- Start Dessix desktop app first. The bridge is served by the Electron app process.
- To discover bundled MCP script path at runtime, use `node scripts/dessix-bridge.mjs locate-mcp-script`.
  - Override auto-detection with `DESSIX_MCP_SCRIPT_PATH` (or `--mcpScriptPath <path>`).
  - Current built-in candidates include:
    - macOS: `/Applications/Dessix.app/Contents/Resources/electron/compiled/dessix-mcp.js`
    - Windows: `%LOCALAPPDATA%\\Programs\\Dessix\\resources\\electron\\compiled\\dessix-mcp.js`
- If `DESSIX_MCP_BRIDGE_ENDPOINT` is unset, this bridge client uses platform endpoint defaults:
  - macOS/Linux: `~/.dessix/mcp/dessix-mcp-bridge.sock`
  - Windows: `\\\\.\\pipe\\dessix-mcp-bridge`
- Use compact JSON for `--args`. Invalid JSON fails fast.
- Read `references/dessix-tools.md` for tool names and argument templates.

## Multi-Step Workflows

Combine tools to achieve higher-level goals. Validate outputs before any write.

### Skill Discovery

Build a skill map for the current workspace (read-only):

```bash
node scripts/dessix-bridge.mjs invoke --tool dessix_get_current_workspace --args '{}'
node scripts/dessix-bridge.mjs invoke --tool dessix_search_blocks --args '{"types":["Action","Scene"],"limit":100}'
# for each block_id in results:
node scripts/dessix-bridge.mjs invoke --tool dessix_get_skill --args '{"block_id":"<BLOCK_ID>"}'
```

### Topic to Skill Draft

Turn a discussion thread into a reusable Action/Scene block:

```bash
node scripts/dessix-bridge.mjs invoke --tool dessix_get_topic_context --args '{"topic_id":"<THREAD_BLOCK_ID>"}'
node scripts/dessix-bridge.mjs invoke --tool dessix_search_blocks --args '{"semantic":"related skills and constraints","limit":20}'
# draft title+content from combined context, then:
node scripts/dessix-bridge.mjs invoke --tool dessix_create_block --args '{"patch":{"type":"Action","title":"<TITLE>","content":"<CONTENT>"}}'
```

### Skill Maintenance

Find and refresh stale skill blocks:

```bash
node scripts/dessix-bridge.mjs invoke --tool dessix_search_blocks --args '{"query":"skill","types":["Action","Scene"],"limit":50}'
node scripts/dessix-bridge.mjs invoke --tool dessix_read_block --args '{"block_id":"<BLOCK_ID>"}'
# compare current state, then patch:
node scripts/dessix-bridge.mjs invoke --tool dessix_update_block --args '{"block_id":"<BLOCK_ID>","patch":{"title":"<UPDATED>","content":"<UPDATED>"}}'
```

### Safety

- Run read-only workflows first; escalate to writes only after validating `block_id` and result counts.
- Compact JSON only for `--args`.
