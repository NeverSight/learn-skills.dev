---
name: permission-analyzer
description: Generate Claude Code permissions config from session history. Use when setting up autonomous mode, configuring .claude/settings.json, avoiding --dangerously-skip-permissions, or analyzing what permissions a project needs. Reads session logs to extract Bash commands and MCP tools actually used, then generates appropriate allow/deny rules.
# model: inherit
# allowedTools: []
---

# Permission Analyzer

Generate permissions configuration based on actual tool usage from past sessions.

## Workflow

1. Run the analysis script for the current project:
   ```bash
   ~/.claude/skills/permission-analyzer/scripts/analyze_permissions.py
   ```

2. Review the generated permissions output

3. Offer to merge into existing settings:
   - If `.claude/settings.json` exists, merge the `permissions` section
   - If not, create new file with generated config
   - Preserve existing settings (model, env, etc.)

## Script Output

The script outputs to stderr (summary) and stdout (JSON):

```
Analyzing: /path/to/project
Sessions analyzed: 42

Bash commands found:
  git: 150
  make: 80
  go: 45

MCP tools found:
  mcp__devtools__think

{
  "permissions": {
    "allow": ["Bash(git:*)", "Bash(go:*)", ...],
    "deny": [...],
    "defaultMode": "acceptEdits"
  }
}
```

## Generated Rules

**Allow list** includes:
- Development commands used (git, make, go, npm, cargo, etc.)
- Filesystem commands used (ls, mkdir, find, etc.)
- MCP server wildcards for servers that were used

**Deny list** includes:
- Dangerous gh operations (merge, delete, secrets, auth)
- Sensitive file patterns (.env, secrets/, *.pem, *.key)
- Destructive commands (rm -rf, sudo, chmod 777)

## Merging Settings

When `.claude/settings.json` exists, merge only the `permissions` key while preserving other settings. If user has custom allow/deny rules, ask whether to merge or replace.
