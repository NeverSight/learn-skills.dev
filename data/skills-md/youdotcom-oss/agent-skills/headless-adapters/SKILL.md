---
name: headless-adapters
description: Discover, create, and validate headless adapters for agent integration. Includes scaffolding tools and schema-driven compliance testing.
compatibility: Bun >= 1.2.9
---

# Headless Adapters

## Purpose

Schema-driven adapter for headless CLI agents. **No code required** - just define a JSON schema describing how to interact with the CLI.

| Use Case | Tool |
|----------|------|
| Wrap headless CLI agent | `headless` command |
| Create new schemas | [Schema Creation Guide](references/schema-creation-guide.md) |

## Quick Start

1. **Check if a schema exists** in [schemas/](schemas/)
2. **Run the adapter:**
   ```bash
   ANTHROPIC_API_KEY=... bunx @plaited/agent-eval-harness headless --schema .claude/skills/headless-adapters/schemas/claude-headless.json
   ```

## CLI Commands

### headless

Schema-driven adapter for ANY headless CLI agent.

```bash
bunx @plaited/agent-eval-harness headless --schema <path>
```

**Options:**
| Flag | Description | Required |
|------|-------------|----------|
| `-s, --schema` | Path to adapter schema (JSON) | Yes |

**Schema Format:**

```json
{
  "version": 1,
  "name": "my-agent",
  "command": ["my-agent-cli"],
  "sessionMode": "stream",
  "prompt": { "flag": "-p" },
  "output": { "flag": "--output-format", "value": "stream-json" },
  "autoApprove": ["--allow-all"],
  "outputEvents": [
    {
      "match": { "path": "$.type", "value": "message" },
      "emitAs": "message",
      "extract": { "content": "$.text" }
    }
  ],
  "result": {
    "matchPath": "$.type",
    "matchValue": "result",
    "contentPath": "$.content"
  }
}
```

**Session Modes:**

| Mode | Description | Use When |
|------|-------------|----------|
| `stream` | Keep process alive, multi-turn via stdin | CLI supports session resume |
| `iterative` | New process per turn, accumulate history | CLI is stateless |

## Pre-built Schemas

Tested schemas are available in [schemas/](schemas/):

| Schema | Agent | Mode | Auth Env Var | Status |
|--------|-------|------|--------------|--------|
| `claude-headless.json` | Claude Code | stream | `ANTHROPIC_API_KEY` | Tested |
| `gemini-headless.json` | Gemini CLI | iterative | `GEMINI_API_KEY` | Tested |

**Usage:**
```bash
# Claude Code
ANTHROPIC_API_KEY=... bunx @plaited/agent-eval-harness headless --schema .claude/skills/headless-adapters/schemas/claude-headless.json

# Gemini CLI
GEMINI_API_KEY=... bunx @plaited/agent-eval-harness headless --schema .claude/skills/headless-adapters/schemas/gemini-headless.json
```

## Creating a Schema

1. Explore the CLI's `--help` to identify prompt, output, and auto-approve flags
2. Capture sample JSON output from the CLI
3. Map JSONPath patterns to output events
4. Create schema file based on an existing template
5. Test with `headless` command

See [Schema Creation Guide](references/schema-creation-guide.md) for the complete workflow.

## Troubleshooting

### Common Issues

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| Tool calls not captured | JSONPath not iterating arrays | Use `[*]` wildcard syntax - [see guide](references/troubleshooting-guide.md#tool-calls-not-appearing) |
| "unexpected argument" error | Stdin mode misconfigured | Use `stdin: true` - [see guide](references/troubleshooting-guide.md#stdin-mode-issues) |
| 401 Authentication errors | API key not properly configured | Set the correct API key environment variable (see Pre-built Schemas table) |
| Timeout on prompt | JSONPath not matching | Capture raw CLI output, verify paths - [see guide](references/troubleshooting-guide.md#jsonpath-debugging) |
| Empty responses | Content extraction failing | Check extract paths - [see guide](references/troubleshooting-guide.md#output-event-matching) |

**Complete troubleshooting documentation:** [Troubleshooting Guide](references/troubleshooting-guide.md)

## External Resources

- **AgentSkills Spec**: [agentskills.io](https://agentskills.io)

## Related

- **[agent-eval-harness skill](../agent-eval-harness/SKILL.md)** - Running evaluations against adapters
