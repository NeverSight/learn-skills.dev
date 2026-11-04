---
name: zenf-mcp
description: "Audit, connect, and configure the zenfd MCP server integration for Antigravity, Claude Code, Cursor, and other AI agents."
---

# zenf-mcp — Model Context Protocol Integration & Orchestration Engine

## Operating Invariants

1. **Short-Circuit on Connected State**:
   - When the `zenfd` MCP server is verified as already configured and valid (the configuration file exists and the `zenfd` entry points to a valid, existing binary):
     - **Emit a concise status report** confirming the connected state.
     - **Halt the turn immediately**. Strictly forbid any additional file modifications, command executions, or redundant actions.
2. **Zero-Touch Without Affirmative Human Review & Confirmation**:
   - If the `zenfd` MCP server is not yet connected or has an invalid/missing configuration:
     - **Strictly forbid running setup commands or overwriting user configuration files automatically**.
     - Display the exact CLI command (e.g. `apps/daemon/bin/zenfd mcp setup --client agy`), target configuration file path, and proposed JSON preview for Human Review & Confirmation.
     - Begin execution only AFTER receiving explicit, affirmative user confirmation.
3. **SSOT Alignment**:
   - The MCP server connects directly to the SQLite WAL database (`~/.zenforge/state.db`) via stdio transport as the durable Single Source of Truth (SSOT).

---

## Domain Rubric

### 1. Client Configuration Matrix

| AI Client | Identifier (`--client`) | Canonical Config Path | Transport Protocol |
| :--- | :--- | :--- | :--- |
| **Antigravity CLI / IDE** | `agy` (default) | `~/.gemini/config/mcp_config.json` | Stdio JSON-RPC 2.0 |
| **Claude Code** | `claude` | `~/.claude.json` / `.mcp.json` | Stdio JSON-RPC 2.0 |
| **Cursor** | `cursor` | `~/.cursor/mcp.json` | Stdio JSON-RPC 2.0 |

---

## Execution Protocol

### Step 1: Audit & Check Connection Status

Execute the status check for the target client (default: `agy`):
```bash
apps/daemon/bin/zenfd mcp check --client agy --json
```

- **CASE A: CONNECTED & VALID (`configured: true` AND `binary_exists: true`)**:
  - Output a concise single-block report:
    > ✅ **zenfd MCP server is successfully connected to Antigravity CLI/IDE** (`<config_path>`). All 20 MCP tools are active; no further configuration required.
  - **Halt the turn immediately**. Do not call additional tools.

- **CASE B: NOT CONFIGURED OR BROKEN (`configured: false` OR `binary_exists: false`)**:
  - Transition to Step 2 (Review & Confirmation Gate).

---

### Step 2: Review & Confirmation Gate (Wait for Approval)

Present the configuration plan clearly to the user:
1. **Current Status**: (e.g. File `~/.gemini/config/mcp_config.json` is empty 0 bytes or lacks `zenfd` entry).
2. **Proposed Command**:
   ```bash
   apps/daemon/bin/zenfd mcp setup --client agy
   ```
3. **Target Config Path**:
   `~/.gemini/config/mcp_config.json`
4. **Configuration JSON Preview**:
   ```json
   {
     "mcpServers": {
       "zenfd": {
         "command": "/absolute/path/to/apps/daemon/bin/zenfd",
         "args": [
           "mcp",
           "--db",
           "/home/rirong/.zenforge/state.db"
         ]
       }
     }
   }
   ```
5. Prompt the user for confirmation: *"Do you confirm running this command to configure the zenfd MCP server?"* and **HALT TURN IMMEDIATELY TO AWAIT USER RESPONSE**.

---

### Step 3: Execution After Confirmation

Upon receiving affirmative human confirmation:
1. Run the setup command:
   ```bash
   apps/daemon/bin/zenfd mcp setup --client agy
   ```
2. Verify with the audit check:
   ```bash
   apps/daemon/bin/zenfd mcp check --client agy
   ```
3. Report success and remind the user to restart their AI client session (e.g. `agy`) to discover the 20 `zenfd` MCP tools.
