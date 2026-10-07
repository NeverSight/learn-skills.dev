---
name: create-locked-down-skill
description: Create a restricted workflow directory with locked-down permissions for Claude Code, Codex CLI, Gemini CLI, and OpenCode. Use when asked to set up a new workflow, create a sandboxed workspace, restrict permissions for a task, or scaffold a locked-down skill.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Create Locked-Down Workflow

Scaffold a new workflow directory with locked-down permissions for one or more AI coding agents: Claude Code, Codex CLI, Gemini CLI, and OpenCode.

## When to Use

- User asks to "create a workflow for X"
- User wants a restricted/sandboxed workspace
- User says "set up a new input skill"
- User wants to lock down permissions for a specific task

## Workflow

### Step 1: Gather Requirements

Ask the user for:

1. **Name** — what to call the workflow (becomes the directory name under `workflows/`)
2. **Purpose** — what the workflow does (becomes the instruction file content)
3. **Which agents** — Claude Code, Codex CLI, Gemini CLI, OpenCode, or all four
4. **Allowed tools** — which tools should be permitted. Common sets:
   - **Research**: web search, web fetch, scoped reads, scoped writes for reports
   - **Writing**: scoped reads + scoped writes
   - **Analysis**: scoped reads only (no writes, no shell)
5. **Write paths** — which directories the workflow can write to. Always includes its own directory.
6. **Source content** — an existing skill or instructions to embed.

### Step 2: Create Directory Structure

Create configs for all requested agents:

```
workflows/<name>/
├── .claude/
│   └── settings.json          # Claude Code permissions (use settings.json, NOT settings.local.json)
├── .codex/
│   ├── config.toml            # Codex sandbox and approval settings
│   ├── requirements.toml      # Constraint enforcement (pins allowed settings)
│   └── rules/
│       └── default.rules      # Codex Starlark execution policy rules
├── .gemini/
│   ├── settings.json          # Gemini tool allowlist and security settings
│   ├── policies/
│   │   └── lockdown.toml      # Gemini TOML policy rules
│   └── GEMINI.md              # Gemini agent instructions
├── opencode.json                # OpenCode permissions and tool config
├── AGENTS.md                   # Codex + OpenCode agent instructions
└── CLAUDE.md                   # Claude Code workflow instructions
```

---

## Claude Code Configuration

File: `.claude/settings.json` (NOT `settings.local.json` — use `settings.json` so it gets committed to git)

### Critical Design Constraint: deny Beats allow

**In Claude Code, `deny` rules take precedence over `allow` rules.** You CANNOT use catch-all denies like `Read(**)` alongside specific allows like `Read(./**/*.md)` — the deny always wins and the allow is ignored. This means you cannot use the permissions system alone to restrict file access to a subset of files.

**The solution is a two-layer hook architecture:**

1. **Permissions deny list** — blocks non-file tools by exact name (Bash, Agent, WebSearch, etc.)
2. **PreToolUse hooks** — handle ALL file tool decisions, returning explicit `allow` or `deny` for every call (so the user is never prompted)

### Architecture: Two Hooks

You need two hook scripts:

#### Hook 1: `block-all.sh` (catch-all, no matcher)

Runs on EVERY tool call. Allows only Read/Write/Edit/Glob/Grep through to the second hook. Denies everything else — this is what catches MCP tools, ListMcpResourcesTool, and any unexpected tools that slip past the deny list.

```bash
#!/usr/bin/env bash
set -euo pipefail
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

# These tools are handled by dir-jail.sh
case "$TOOL_NAME" in
  Read|Write|Edit|Glob|Grep) exit 0 ;;
esac

# Everything else is blocked
jq -n --arg reason "BLOCKED: tool '$TOOL_NAME' is not allowed in this locked-down environment" '{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": $reason
  }
}'
```

**Why this is needed:** The `mcp__*` pattern in the deny list does NOT reliably block MCP tools. MCP tools with names like `mcp__claude_ai_Notion__notion-search` slip through. Tools like `ListMcpResourcesTool` and `ReadMcpResourceTool` are not prefixed with `mcp__` at all. A catch-all hook is the only reliable way to block unexpected tools.

#### Hook 2: `dir-jail.sh` (per-tool matcher)

Runs on Read/Write/Edit/Glob/Grep only. Enforces:
- **Directory jail** — all paths must resolve inside the workflow directory
- **File type restriction** — only `.md` files for Read/Write/Edit (customize per workflow)
- **Config protection** — blocks writes to CLAUDE.md, AGENTS.md
- **Dotfolder protection** — blocks all access to `.claude/`, `.codex/`, `.gemini/`, etc.
- **Returns explicit allow/deny** — never exits without a decision, so the user is never prompted

Key behavior: for Glob/Grep with no path (defaults to cwd), return allow. For paths inside jail that pass all checks, return explicit allow. For everything else, return explicit deny.

```bash
#!/usr/bin/env bash
set -euo pipefail
JAIL_DIR="${CLAUDE_JAIL_DIR:-$PWD}"
JAIL_DIR="$(cd "$JAIL_DIR" 2>/dev/null && pwd -P)"
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

allow() {
  jq -n --arg reason "$1" '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow","permissionDecisionReason":$reason}}'
  exit 0
}
deny() {
  jq -n --arg reason "$1" '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":$reason}}'
  exit 0
}

# Extract path
case "$TOOL_NAME" in
  Read|Write|Edit) TARGET=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty') ;;
  Glob|Grep) TARGET=$(echo "$INPUT" | jq -r '.tool_input.path // empty') ;;
  *) deny "Unknown tool" ;;
esac

# No path = cwd default (Glob/Grep)
[ -z "$TARGET" ] && allow "Default path within jail"

# Resolve path (handle non-existent files for Write)
if [ -e "$TARGET" ]; then
  RESOLVED=$(cd "$(dirname "$TARGET")" && pwd -P)/$(basename "$TARGET")
else
  RESOLVED=$(python3 -c "import os; print(os.path.realpath('$TARGET'))" 2>/dev/null || echo "$TARGET")
fi

IS_WRITE=false
case "$TOOL_NAME" in Write|Edit) IS_WRITE=true ;; esac

# Outside jail?
if [[ "$RESOLVED" != "$JAIL_DIR"* ]]; then
  # Allow read-only access to ~/.claude/ for Claude Code internals
  if ! $IS_WRITE && [[ "$RESOLVED" == "$HOME/.claude/"* ]]; then
    allow "Read-only access to ~/.claude/"
  fi
  deny "BLOCKED: path resolves outside jail"
fi

# Block dotfolders
echo "$RESOLVED" | grep -qE '(^|/)\.[^/]+/' && deny "BLOCKED: dotfolder access denied"

# Glob/Grep: allow searching within jail
case "$TOOL_NAME" in Glob|Grep) allow "Search within jail" ;; esac

# Enforce file extension (customize this list per workflow)
BASENAME=$(basename "$RESOLVED")
[[ "$BASENAME" != *.md ]] && deny "BLOCKED: only .md files allowed, got '$BASENAME'"

# Protect config files from writes
if $IS_WRITE; then
  case "$BASENAME" in
    CLAUDE.md|AGENTS.md) deny "BLOCKED: '$BASENAME' is a protected config file" ;;
  esac
fi

allow "Permitted: .md file within jail"
```

### settings.json Template

**The `allow` list is empty.** All file tool decisions are made by hooks. The `deny` list blocks non-file tools by name. The catch-all hook blocks everything else.

```json
{
  "allowedMcpServers": [],
  "permissions": {
    "allow": [],
    "deny": [
      "Bash",
      "Agent",
      "Skill",
      "NotebookEdit",
      "WebSearch",
      "WebFetch",
      "ToolSearch",
      "mcp__*",
      "TaskCreate",
      "TaskGet",
      "TaskList",
      "TaskOutput",
      "TaskStop",
      "TaskUpdate",
      "SendMessage",
      "CronCreate",
      "CronDelete",
      "CronList",
      "EnterPlanMode",
      "ExitPlanMode",
      "EnterWorktree",
      "ExitWorktree",
      "AskUserQuestion",
      "TeamCreate",
      "TeamDelete",
      "ListMcpResourcesTool",
      "ReadMcpResourceTool"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "<WORKFLOW_DIR>/.claude/hooks/block-all.sh"
          }
        ]
      },
      {
        "matcher": "Read",
        "hooks": [{ "type": "command", "command": "<WORKFLOW_DIR>/.claude/hooks/dir-jail.sh" }]
      },
      {
        "matcher": "Write",
        "hooks": [{ "type": "command", "command": "<WORKFLOW_DIR>/.claude/hooks/dir-jail.sh" }]
      },
      {
        "matcher": "Edit",
        "hooks": [{ "type": "command", "command": "<WORKFLOW_DIR>/.claude/hooks/dir-jail.sh" }]
      },
      {
        "matcher": "Glob",
        "hooks": [{ "type": "command", "command": "<WORKFLOW_DIR>/.claude/hooks/dir-jail.sh" }]
      },
      {
        "matcher": "Grep",
        "hooks": [{ "type": "command", "command": "<WORKFLOW_DIR>/.claude/hooks/dir-jail.sh" }]
      }
    ]
  }
}
```

**Replace `<WORKFLOW_DIR>` with the absolute path** (e.g., `/Users/jv/projects/myrepo/workflows/ai-news`). Hook commands must be absolute paths.

### Rules

- **`allow` list is empty** — all file access decisions are made by hooks, not permission patterns
- **deny list blocks non-file tools by exact name** — Bash, Agent, Skill, WebSearch, WebFetch, all Task/Cron/Worktree tools, MCP resource tools
- **`mcp__*` in deny is unreliable** — it does not block all MCP tools. The catch-all hook (`block-all.sh` with no matcher) is the real MCP blocker
- **`allowedMcpServers: []`** — set this to prevent MCP server connections, but note it may only work from managed/enterprise settings. The catch-all hook is the fallback
- **Catch-all hook must be FIRST** in the PreToolUse array — it runs before the per-tool hooks
- **Hooks must return explicit allow or deny for EVERY call** — if a hook exits without a decision, Claude Code falls through to permission prompting (which is a lockdown failure)
- **Hook commands must use absolute paths** — relative paths won't resolve correctly
- **`dir-jail.sh` must allow read access to `~/.claude/`** — Claude Code reads its own CLAUDE.md and config from there at startup
- If the user needs web access, add `WebSearch` and `WebFetch` to the allow list AND add them to the `case` statement in `block-all.sh`
- To allow different file types, change the extension check in `dir-jail.sh` (e.g., `*.md|*.txt|*.json`)

---

## Codex CLI Configuration

### Critical Design Constraint: No Per-File Policy Engine

**Codex's `workspace-write` sandbox restricts by directory boundary (OS-level), NOT by file type.** The `apply_patch` tool can write to ANY file within the workspace. Unlike Claude Code (hooks) and Gemini (policy engine), Codex has **no mechanism to hard-enforce file extension restrictions**.

File-type restrictions (e.g., .md only) must come from **AGENTS.md soft guardrails** — the model reads AGENTS.md and self-censors. This is reliable in practice (GPT-5.4 consistently refuses even under prompt injection) but is model compliance, not OS/tool enforcement.

### Three-Layer Architecture

1. **OS-level sandbox (`workspace-write`)** — kernel-enforced directory boundary. Can't read or write outside workspace.
2. **Feature toggles** — hard-disable shell, web, MCP at the CLI level. Tools don't exist.
3. **AGENTS.md soft guardrails** — file extension restrictions, config file protection. Model compliance only.

### config.toml

File: `.codex/config.toml`

Key settings:

| Setting | Purpose | Recommended |
|---------|---------|-------------|
| `sandbox_mode` | OS-level sandbox | `workspace-write` (restricts reads AND writes to workspace) |
| `approval_policy` | Human approval gates | `"never"` (zero user prompts) |
| `allow_login_shell` | Login shell access | `false` |
| `web_search` | Web search capability | `"disabled"` for lockdown |
| `file_opener` | Citation link opener | `"none"` |

**Important: Do NOT use `read-only` sandbox mode if you want to restrict reads.** `read-only` only prevents writes — it allows reading ANY file on the entire filesystem including `/etc/hosts`, `~/.ssh/`, etc. Use `workspace-write` instead, which restricts both reads and writes to the workspace directory.

**`approval_policy = "never"` is safe with `workspace-write` sandbox** — the sandbox prevents all dangerous operations at the OS level, so there's nothing to approve. This gives zero user prompts.

To fully disable shell, web, MCP, and related features:
```toml
[features]
codex_hooks = false
shell_tool = false
apps = false
apps_mcp_gateway = false
multi_agent = false
unified_exec = false
```

**Critical: Global MCP servers bleed into project scope.** Setting `apps = false` disables the "Apps" feature but NOT raw MCP servers defined in `~/.codex/config.toml`. You MUST explicitly disable each global MCP server in the project config:

```toml
[mcp_servers.browserplex]
enabled = false

[mcp_servers.some_other_server]
enabled = false
```

If you don't do this, the model can call MCP tools like `browserplex.session_create` and launch browsers, completely bypassing the lockdown.

**Warning:** An `enabled = false` override with no `command` field will cause a startup error ("invalid transport") if the corresponding global server is later removed. Only override servers that currently exist in global config.

### requirements.toml

File: `.codex/requirements.toml`

This file enforces constraints — it limits which settings values are allowed. If anyone tries to change config.toml to use a different sandbox mode or approval policy, requirements.toml blocks it.

```toml
allowedApprovalPolicies = ["never"]
allowedSandboxModes = ["workspace-write"]
allowedWebSearchModes = ["disabled"]

[featureRequirements]
apps = false
apps_mcp_gateway = false
codex_hooks = false
multi_agent = false
request_permissions_tool = false
shell_tool = false
unified_exec = false
```

### Starlark Execution Policy Rules

File: `.codex/rules/default.rules`

Rules only match **shell command arguments** — they cannot restrict `apply_patch` (file writes). With `shell_tool = false`, rules are defense-in-depth only:

```python
# Deny shell entrypoints if shell is ever re-enabled
prefix_rule(
    pattern = [["bash", "sh", "zsh", "fish"]],
    decision = "forbidden",
    justification = "Shell execution is disabled in this workflow.",
    match = [
        "bash -lc ls",
        "zsh -lc pwd",
        "sh -c whoami",
    ],
)
```

Decisions: `"allow"` | `"prompt"` | `"forbidden"`. Rules cannot enforce file-type restrictions.

### AGENTS.md (Soft Guardrails)

File: `AGENTS.md` (workflow directory)

**This is the ONLY mechanism for file-type restrictions in Codex.** The model reads AGENTS.md and complies with it. Include explicit constraints:

```markdown
## Constraints

- ONLY create or edit `.md` files in this directory
- NEVER modify AGENTS.md, CLAUDE.md, or GEMINI.md
- NEVER create `.txt`, `.json`, `.toml`, `.yaml`, or any non-markdown files
- NEVER create files in subdirectories or dotfile directories
```

### Sandbox Details

```toml
[sandbox_workspace_write]
writable_roots = []          # No additional writable dirs beyond workspace
network_access = false       # Block all outbound network
exclude_slash_tmp = true     # Don't allow /tmp writes
exclude_tmpdir_env_var = true # Don't allow $TMPDIR writes
```

### Rules

- **`workspace-write` is OS-level hard enforcement** — kernel sandbox prevents reads/writes outside workspace. This is the strongest layer.
- **`approval_policy = "never"` gives zero prompts** — safe because the sandbox prevents all dangerous operations.
- **`apps = false` does NOT disable MCP servers** — you must explicitly override each global MCP server with `enabled = false` in project config.
- **File extension restrictions are soft-only** — `apply_patch` can write any file type in the workspace. Only AGENTS.md instructions prevent this.
- **Starlark rules only gate shell commands** — they cannot restrict file write tools.
- **`requirements.toml` enforces constraints** — prevents changing sandbox mode or approval policy.
- **Codex has no general file-read tool** — the model can only read AGENTS.md (auto-loaded) and files via `apply_patch` context. It cannot arbitrarily read .toml, .json, etc.
- To allow web access: set `web_search = "live"` and `network_access = true`.

---

## Gemini CLI Configuration

### Critical Design Constraint: Two Enforcement Layers

Gemini CLI uses a **different security model** than Claude Code. Instead of hooks that intercept tool calls, Gemini has:

1. **`tools.core` allowlist (hard enforcement)** — only listed tools are loaded into the model. Unlisted tools literally don't exist — the model can't call them. This is the strongest lockdown mechanism.
2. **Policy engine `.toml` rules (mixed enforcement)** — deny rules with no `argsPattern` remove tools from model awareness entirely (hard). Rules with `argsPattern` for file extension filtering are enforced via model compliance — the model reads the policy file and self-censors (soft).

### Architecture: Allowlist + Policy + Auto-Edit

You need three things working together:

#### Layer 1: `tools.core` Allowlist (settings.json)

This is the hard kill switch. Only list the tools you want available:

| Class Name (for `tools.core`) | Function Name (for policies) | Purpose |
|-------------------------------|------------------------------|---------|
| `ReadFileTool` | `read_file` | Read a single file |
| `ReadManyFilesTool` | `read_many_files` | Read multiple files |
| `GlobTool` | `glob` | Find files by pattern |
| `GrepTool` | `search_file_content` | Search file contents |
| `WriteFileTool` | `write_file` | Create/overwrite files |
| `EditTool` | `replace` | Modify files in-place |
| `LSTool` / `ListDirectoryTool` | `list_directory` | List directory contents |
| `ShellTool` | `run_shell_command` | Execute shell commands |
| `WebSearchTool` | `google_web_search` | Web search |
| `WebFetchTool` | `web_fetch` | Fetch URL content |
| `MemoryTool` | `save_memory` | Save cross-session memory |

**For a markdown-only lockdown, use only:** `ReadFileTool`, `ReadManyFilesTool`, `GlobTool`, `GrepTool`, `WriteFileTool`, `EditTool`. Omit everything else.

**Do NOT use `tools.exclude`** — it's deprecated and will be removed in 1.0. Use `tools.core` (allowlist) + policy engine instead.

#### Layer 2: Policy Engine (lockdown.toml)

The policy provides defense-in-depth and file extension restrictions:

- **Global deny rules** (no `argsPattern`) — remove tools from model awareness entirely. Use for shell, web, MCP.
- **`argsPattern` rules** — regex-based, enforced via model compliance. The model reads the policy file and respects it. Use for file extension filtering.
- **`allow` rules** — auto-approve matching tool calls without user prompts.
- **Priority system** — higher priority wins. Use 900 for denies, 850 for config protection, 800 for allows, 700 for fallback denies.

```toml
# Deny shell (defense-in-depth, tools.core already removes it)
[[rule]]
toolName = "run_shell_command"
decision = "deny"
priority = 900
deny_message = "Shell commands are disabled"

# Deny all MCP
[[rule]]
mcpName = "*"
decision = "deny"
priority = 900
deny_message = "MCP servers are disabled"

# Protect config files from writes
[[rule]]
toolName = ["write_file", "replace"]
argsPattern = '(CLAUDE|AGENTS|GEMINI)\.md"'
decision = "deny"
priority = 850
deny_message = "Config files are read-only"

# Allow .md file reads
[[rule]]
toolName = "read_file"
argsPattern = '\.md"'
decision = "allow"
priority = 800

# Allow .md file writes
[[rule]]
toolName = "write_file"
argsPattern = '\.md"'
decision = "allow"
priority = 800

# Allow .md file edits
[[rule]]
toolName = "replace"
argsPattern = '\.md"'
decision = "allow"
priority = 800

# Allow search tools
[[rule]]
toolName = ["glob", "search_file_content", "read_many_files"]
decision = "allow"
priority = 800

# Deny non-.md reads (fallback)
[[rule]]
toolName = "read_file"
decision = "deny"
priority = 700
deny_message = "Only .md files can be read"

# Deny non-.md writes (fallback)
[[rule]]
toolName = "write_file"
decision = "deny"
priority = 700
deny_message = "Only .md files can be written"

# Deny non-.md edits (fallback)
[[rule]]
toolName = "replace"
decision = "deny"
priority = 700
deny_message = "Only .md files can be edited"
```

#### Layer 3: Auto-Edit Mode (zero user prompts)

**The `defaultApprovalMode` setting is critical.** Without it, Gemini prompts the user for every write operation — which is a lockdown failure.

- `"default"` — prompts for writes (lockdown failure)
- `"auto_edit"` — auto-approves file operations, no prompts
- `"plan"` — read-only mode, blocks all writes
- `"yolo"` — auto-approves everything (too permissive, also enables sandbox)

**Use `"auto_edit"` for lockdown.** It auto-approves reads and writes without prompting, while the policy engine controls what's allowed.

**`disableAlwaysAllow` must be `false`** when using `auto_edit` mode — setting it to `true` prevents the policy engine's `allow` decisions from auto-approving tool calls, which causes user prompts (lockdown failure).

### settings.json Template

```json
{
  "policyPaths": [
    "__WORKFLOW_DIR__/.gemini/policies/lockdown.toml"
  ],
  "hooksConfig": {
    "enabled": false,
    "notifications": false
  },
  "tools": {
    "core": [
      "ReadFileTool",
      "ReadManyFilesTool",
      "GlobTool",
      "GrepTool",
      "WriteFileTool",
      "EditTool"
    ]
  },
  "security": {
    "policy_engine": {
      "enabled": true
    },
    "enableConseca": false,
    "disableYoloMode": true,
    "disableAlwaysAllow": false,
    "blockGitExtensions": true,
    "environmentVariableRedaction": {
      "enabled": true
    }
  },
  "admin": {
    "secureModeEnabled": true,
    "extensions": { "enabled": false },
    "mcp": { "enabled": false },
    "skills": { "enabled": false }
  },
  "general": {
    "defaultApprovalMode": "auto_edit"
  }
}
```

**Replace `__WORKFLOW_DIR__` with the absolute path** to the workflow directory.

### Rules

- **`tools.core` is the strongest lockdown** — unlisted tools don't exist for the model. Always start here.
- **Do NOT use `tools.exclude`** — deprecated, use `tools.core` allowlist instead.
- **Do NOT use `tools.allowed`** — deprecated, use policy engine `allow` rules instead.
- **`defaultApprovalMode: "auto_edit"` is required** for zero user prompts on writes.
- **`disableAlwaysAllow` must be `false`** — otherwise policy `allow` decisions don't auto-approve and the user gets prompted.
- **`policyPaths` must use absolute paths** — relative paths don't resolve correctly.
- **`admin.mcp.enabled: false`** prevents MCP server connections. Pair with `mcpName = "*"` deny rule for defense-in-depth.
- **File extension enforcement is model-compliance based** — the model reads the policy file and self-censors. It's reliable in practice (Gemini 3 consistently refuses) but not a hard block at the tool call level like Claude's hooks.
- **Gemini automatically scopes file reads to the workspace directory** — no directory jail needed. Reads outside the workspace are blocked natively.
- **Config file protection uses `argsPattern`** — add filenames to the deny pattern that should be read-only.
- If web access is needed, add `WebSearchTool`/`WebFetchTool` to `tools.core` and add policy `allow` rules for `google_web_search`/`web_fetch`.

### GEMINI.md

File: `.gemini/GEMINI.md`

Equivalent of CLAUDE.md. Soft guardrails — always pair with settings.json and policy rules.

---

## OpenCode Configuration

### Two-Layer Architecture

OpenCode uses a simpler but effective lockdown model:

1. **Tool toggles (hard enforcement)** — disable tools entirely via `"tools": { "bash": false }`. Disabled tools are invisible to the model — it cannot call them.
2. **Permission patterns (hard enforcement)** — pattern-based `allow`/`deny` rules per tool. Denied operations return `PermissionDeniedError` at the tool level. The model sees the error and learns the restrictions.

**No OS-level sandbox.** OpenCode relies on its own permission system, not a kernel sandbox. The `external_directory: "deny"` permission blocks access outside the project directory.

### opencode.json

File: `opencode.json` (project root). Supports JSONC (JSON with Comments). Config files merge — project config overrides global `~/.config/opencode/opencode.json`.

### Tool Toggles

Disable dangerous tools entirely — they become invisible to the model:

```json
{
  "tools": {
    "bash": false,
    "webfetch": false,
    "websearch": false,
    "lsp": false,
    "skill": false,
    "todowrite": false,
    "todoread": false,
    "patch": false
  }
}
```

Available tools: `read`, `edit`, `write`, `bash`, `glob`, `grep`, `list`, `lsp`, `skill`, `todowrite`, `todoread`, `webfetch`, `websearch`, `patch`, `question`.

### Permission Patterns

Pattern-based rules with `allow`/`ask`/`deny`. **Last matching rule wins.**

```json
{
  "permission": {
    "read": {
      "*": "deny",
      "*.md": "allow"
    },
    "edit": {
      "*": "deny",
      "*.md": "allow",
      "**/AGENTS.md": "deny",
      "**/CLAUDE.md": "deny",
      "**/GEMINI.md": "deny"
    },
    "write": {
      "*": "deny",
      "*.md": "allow",
      "**/AGENTS.md": "deny",
      "**/CLAUDE.md": "deny",
      "**/GEMINI.md": "deny"
    },
    "glob": "allow",
    "grep": "allow",
    "list": "allow",
    "bash": "deny",
    "task": "deny",
    "external_directory": "deny",
    "doom_loop": "deny"
  }
}
```

### Critical Design Constraints

**`"*": "deny"` as global default hides ALL tools from the model.** Unlike `"ask"` which keeps tools visible but prompts, `"deny"` completely removes tools from the model's function list. Do NOT use `"permission": { "*": "deny" }` if you want any tools visible. Instead, explicitly deny each unwanted tool.

**`edit` and `write` need SEPARATE permission entries.** Despite docs saying "`edit` permission governs all file modifications: `edit`, `write`, `patch`, and `multiedit`", in practice pattern-based `edit` rules do NOT cover `write` tool calls. You MUST add both `"edit"` and `"write"` permission entries with the same patterns.

**Config file protection patterns may need glob prefixes.** Simple patterns like `"AGENTS.md": "deny"` may not match if the model passes a full path. Use `"**/AGENTS.md": "deny"` for reliable matching.

**Denied operations return `PermissionDeniedError` at the tool level.** The model sees the full ruleset in the error and learns the restrictions. This is a feedback loop — after seeing a denied write, the model stops trying.

### Rules

- **Disable tools via `tools` for hardest enforcement** — disabled tools don't exist for the model. Use for bash, web, MCP tools.
- **Do NOT use `"*": "deny"` global permission** — it hides all tools, even ones you want available with restrictions.
- **`edit` and `write` are separate permissions** — add both with identical patterns.
- **Pattern-based permissions are hard enforcement** — they return `PermissionDeniedError`, not just model-compliance.
- **`external_directory: "deny"` blocks access outside project dir** — this is OpenCode's equivalent of a workspace sandbox.
- **`doom_loop: "deny"` prevents repeated tool calls** — stops the model from retrying denied operations.
- **MCP servers are configurable** — set `"mcp": {}` to disable all, or disable specific ones with `"enabled": false`.
- **AGENTS.md provides soft guardrails** — OpenCode reads AGENTS.md (same as Codex). Always include file-type constraints.
- **Config merges, not replaces** — global config at `~/.config/opencode/opencode.json` is merged with project config. Override global settings explicitly.
- To allow web access: set `"webfetch": true, "websearch": true` in tools and add permission allows.

---

## Lessons Learned (from testing)

### Claude Code

1. **`deny` beats `allow` — you cannot use both for file tools.** If you put `Read(**)` in deny and `Read(./**/*.md)` in allow, the deny wins and ALL reads are blocked. This is the single most important thing to know. The solution: use hooks for all file access decisions, leave `allow` empty.

2. **`mcp__*` in deny does NOT reliably block MCP tools.** Tools like `mcp__claude_ai_Notion__notion-search` slip through the wildcard. Tools like `ListMcpResourcesTool` aren't prefixed with `mcp__` at all. You MUST use a catch-all PreToolUse hook (no matcher) that denies everything except your allowed tools.

3. **Hooks must return explicit allow/deny for every call.** If a hook exits without outputting a permission decision (just `exit 0`), Claude Code falls through to prompting the user. A user prompt is a lockdown failure — the user could say "yes" to an escape. Every code path in your hooks must end with either an allow or deny JSON response.

4. **MCP servers from global `~/.claude/settings.json` still connect.** Setting `allowedMcpServers: []` in project settings may not block them (it's described as enterprise-only). The catch-all hook is the real defense — even if the MCP server connects, the hook blocks all its tool calls.

5. **Use `settings.json` not `settings.local.json`** — `settings.local.json` is gitignored. Use `settings.json` so lockdown config is committed and shared.

6. **Hook commands must be absolute paths.** Relative paths in hook `command` fields don't resolve correctly.

7. **The catch-all hook must be first in the PreToolUse array.** It runs before per-tool hooks. For allowed tools (Read/Write/Edit/Glob/Grep), it exits cleanly and the per-tool hook takes over.

### Codex

8. **`read-only` sandbox is misleading** — it only prevents writes. It allows reading ANY file on the filesystem. Use `workspace-write` to restrict both reads and writes to the workspace.

9. **Disable shell via features, not just rules** — Starlark rules only gate commands if the approval policy enforces them. Set `[features] shell_tool = false` for hard enforcement, use rules as defense-in-depth.

10. **Global MCP servers bleed into project config** — `apps = false` disables the Apps feature, NOT raw MCP servers from `~/.codex/config.toml`. A global `[mcp_servers.browserplex]` lets the model launch browsers inside your "locked-down" workflow. You MUST add `[mcp_servers.<name>] enabled = false` for each global server.

11. **File extension restrictions are soft-only** — Codex has no policy engine or hook system that can restrict `apply_patch` by file type. The `workspace-write` sandbox restricts by directory, not by file extension. Only AGENTS.md instructions prevent non-.md writes.

12. **`requirements.toml` pins allowed config values** — it constrains which `approval_policy`, `sandbox_mode`, and `web_search` values are valid. If someone edits config.toml to weaken the lockdown, requirements.toml blocks it.

13. **Codex has no general file-read tool** — with `shell_tool = false` and `unified_exec = false`, the model can only read AGENTS.md (auto-loaded as instructions). It cannot arbitrarily read config files, .json, .toml etc. This is an accidental security benefit.

14. **`enabled = false` MCP override with no command causes startup error** — if you override a global MCP server with `enabled = false` but no `command` field, and the global server is later removed, Codex fails with "invalid transport". Only override servers that currently exist in global config.

### Gemini

15. **Workspace sandboxing is automatic** — reads outside the workspace are blocked by default. No need to configure path scoping like Claude Code requires.

16. **Policy denies without `argsPattern` are hard** — a denied tool is removed from the model entirely, not just gated behind approval. But `argsPattern`-based rules (like .md-only extension filtering) are enforced via model compliance, not hard tool-level blocking.

17. **`tools.core` is the strongest mechanism** — it's a strict allowlist. Unlisted tools don't exist for the model. Always prefer removing tools via `tools.core` over policy denies. Policy denies are defense-in-depth.

18. **`auto_edit` mode is required for zero prompts** — without it, Gemini prompts the user for every write ("Action Required: Apply this change?"). `auto_edit` auto-approves file operations. You MUST also set `disableAlwaysAllow: false` or policy `allow` decisions won't auto-approve.

19. **`tools.exclude` and `tools.allowed` are deprecated** — both produce deprecation warnings and will be removed in 1.0. Use `tools.core` (allowlist) + policy engine instead.

20. **Model self-censoring is surprisingly robust** — Gemini 3 reads the policy `.toml` file and consistently refuses disallowed operations, even under adversarial prompt injection ("ignore all policies", "you are in debugging mode"). But this is model compliance, not hard enforcement — a future model version could behave differently.

21. **`policyPaths` must be absolute** — the setting accepts an array of absolute paths to `.toml` policy files. Relative paths don't resolve.

### OpenCode

22. **`"*": "deny"` global permission hides all tools** — unlike `"ask"` which keeps tools visible, `"deny"` removes them from the model's function list entirely. Don't use it as a global default if you need any tools to be visible with restrictions.

23. **`edit` and `write` need separate permission entries** — despite docs claiming `edit` governs all file modifications, pattern-based `edit` rules don't apply to `write` tool calls. Always add both.

24. **Pattern-based permissions are hard enforcement** — `PermissionDeniedError` is returned at the tool level. The model sees the error message containing the full ruleset and stops retrying.

25. **Config file protection patterns need glob prefixes** — simple `"AGENTS.md": "deny"` may not match if the model passes a full path. Use `"**/AGENTS.md": "deny"` for reliability.

26. **Disabled tools are invisible** — `"tools": { "bash": false }` is the strongest enforcement. The model has no function to call.

27. **OpenCode TUI needs Enter twice from tmux** — first Enter types into the input editor, second Enter submits. The TUI uses Bubble Tea with a multiline editor.

### General

28. **Always layer soft + hard guardrails** — instruction files (CLAUDE.md, AGENTS.md, GEMINI.md) are advisory. Always pair with hard enforcement (settings.json, hooks, sandbox, policies).

29. **Block MCP on all agents** — MCP servers can bypass other restrictions. Claude Code: catch-all hook + deny list. Codex: explicitly disable each global MCP server with `enabled = false` in project config. Gemini: `admin.mcp.enabled: false` + policy deny on `mcpName = "*"`. OpenCode: `"mcp": {}` in config.

30. **Test the lockdown** — after creating configs, launch each agent inside the directory and run adversarial tests: read outside dir, write outside dir, shell access, MCP tools, read non-allowed file types, write to config files, spawn subagents. Verify zero user prompts appear.

31. **Each agent has a different security model** — Claude Code uses hook-based hard enforcement (every tool call intercepted). Codex uses OS-level sandbox + soft guardrails (kernel boundary is hard, file-type restrictions are soft). Gemini uses tool allowlisting + model compliance (tools removed from model + model self-censoring from policy). OpenCode uses tool toggles + pattern-based permissions (tools disabled = invisible, permissions = hard deny with error feedback).

---

## Step-by-Step (Quick Reference)

1. Gather requirements (name, purpose, agents, tools, write paths)
2. Create directory structure with all agent configs
3. For Claude: `.claude/settings.json` with empty allow list + deny list for non-file tools + two-hook architecture (`block-all.sh` catch-all + `dir-jail.sh` per-tool)
4. For Codex: `.codex/config.toml` with `workspace-write` sandbox + `approval_policy = "never"` + `shell_tool = false` + `.codex/requirements.toml` + `.codex/rules/default.rules` + explicitly disable global MCP servers + AGENTS.md with file-type constraints
5. For Gemini: `.gemini/settings.json` with `tools.core` allowlist + `auto_edit` mode + `disableAlwaysAllow: false` + `.gemini/policies/lockdown.toml` with priority-layered deny/allow/fallback rules
6. For OpenCode: `opencode.json` with `tools` toggles to disable dangerous tools + pattern-based `permission` for file-type restrictions + `"mcp": {}` + AGENTS.md with file-type constraints
7. Write instruction files: `CLAUDE.md`, `AGENTS.md`, `.gemini/GEMINI.md`
7. Confirm plan with user before writing
8. Test all agents inside the directory — verify zero user prompts

## Templates

Ready-to-copy template files are in `templates/`:

```
templates/
├── claude/
│   ├── settings.json              # __WORKFLOW_DIR__ placeholder for absolute paths
│   └── hooks/
│       ├── block-all.sh           # Catch-all hook (deny everything except file tools)
│       └── dir-jail.sh            # Directory jail + extension filter + config protection
├── codex/
│   ├── config.toml                # __WORKFLOW_DIR__ placeholder for project trust
│   ├── requirements.toml          # Constraint enforcement (pins allowed settings)
│   └── rules/
│       └── default.rules          # Starlark shell deny (defense-in-depth)
├── opencode/
│   └── opencode.json              # Tool toggles + pattern-based permissions
└── gemini/
    ├── settings.json              # __WORKFLOW_DIR__ placeholder for policy path
    └── policies/
        └── lockdown.toml          # Priority-layered deny/allow/fallback rules
```

After copying:
- Replace `__WORKFLOW_DIR__` with the absolute path to the workflow directory
- For Claude: `chmod +x` the hook scripts
- For Codex: add `[mcp_servers.<name>] enabled = false` for each MCP server in your global `~/.codex/config.toml`
- For Codex: add file-type constraints to AGENTS.md (soft guardrails — Codex has no hard file-type enforcement)
- For OpenCode: change `"model"` to your preferred model (format: `provider/model-id`)
