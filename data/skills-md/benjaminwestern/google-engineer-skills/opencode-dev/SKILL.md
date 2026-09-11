---
name: opencode-dev
version: "1.0.0"
description: Create and manage OpenCode agents, tools, MCP servers, prompts, and workflows. Use when setting up custom agents, configuring tools, creating agent workflows with subagents, or managing opencode.json configurations.
metadata:
  source_url: https://opencode.ai
  docs_url: https://opencode.ai/docs
---

# OpenCode Development

Create and manage OpenCode agents, tools, MCP servers, and workflows.

## Quick Start

```bash
# Create a new agent
Create a documentation agent that reviews code and writes docs

# Create a custom tool
Create a tool called "deploy" that runs deployment scripts

# Add an MCP server
Add the PostgreSQL MCP server

# Create agent workflow
Create a workflow where a planner agent delegates to a coder agent
```

## Finding Configuration Location

### Search Order

1. **Project-specific**: Look for `.opencode/` folder in current directory
2. **Parent directories**: Search up the tree for `.opencode/` folder
3. **Global config**: Default to `~/.config/opencode/opencode.json`

```bash
# Find closest .opencode folder
find . -maxdepth 3 -type d -name ".opencode" 2>/dev/null | head -1

# Or search upward
pwd | tr '/' '\n' | tac | while read -r dir; do
  test -d "$dir/.opencode" && echo "$dir/.opencode" && break
done
```

### Determine Target Path

```javascript
// Logic to determine where to save configurations
function getTargetPath() {
  // 1. Check for .opencode in current and parent directories
  let currentDir = process.cwd();
  while (currentDir !== '/') {
    const opencodePath = path.join(currentDir, '.opencode');
    if (fs.existsSync(opencodePath)) {
      return opencodePath;
    }
    currentDir = path.dirname(currentDir);
  }
  
  // 2. Default to global config
  return path.join(os.homedir(), '.config/opencode');
}
```

## Creating Agents

### Method 1: Markdown Agent File

**Best for**: Simple agents with prompts and basic configuration

**Location**: `.opencode/agents/<agent-name>.md` or `~/.config/opencode/agents/<agent-name>.md`

```markdown
---
description: What this agent does
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.3
tools:
  write: false
  edit: false
  bash: true
permissions:
  edit: deny
  bash:
    "*": ask
    "git *": allow
---

You are a specialized agent. Your purpose is to...

Focus on:
- Task 1
- Task 2
- Task 3
```

### Method 2: JSON Configuration

**Best for**: Complex agents with detailed tool/permission configurations

**Location**: `.opencode/opencode.json` or `~/.config/opencode/opencode.json`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "my-agent": {
      "description": "What this agent does",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "temperature": 0.3,
      "prompt": "You are a specialized agent...",
      "tools": {
        "write": false,
        "edit": false,
        "bash": true
      },
      "permissions": {
        "edit": "deny",
        "bash": {
          "*": "ask",
          "git *": "allow"
        }
      }
    }
  }
}
```

### Agent Options Reference

| Option | Type | Description |
|--------|------|-------------|
| `description` | string | **Required.** What the agent does |
| `mode` | string | `primary`, `subagent`, or `all` |
| `model` | string | Model ID (e.g., `anthropic/claude-sonnet-4-20250514`) |
| `temperature` | number | 0.0-1.0, creativity control |
| `top_p` | number | 0.0-1.0, response diversity |
| `steps` | number | Max agentic iterations |
| `prompt` | string | System prompt or `{file:./path.txt}` |
| `tools` | object | Tool enable/disable map |
| `permissions` | object | Permission configuration |
| `hidden` | boolean | Hide from @ autocomplete |
| `color` | string | UI color (hex or theme name) |
| `disable` | boolean | Disable the agent |

### Agent Modes

- **primary**: Main agents you interact with directly (switch with Tab key)
- **subagent**: Invoked via @mention or by other agents via Task tool
- **all**: Can be used as both primary and subagent

## Creating Custom Tools

### Simple Tool Definition

**Location**: `.opencode/opencode.json` or `~/.config/opencode/opencode.json`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "customTools": [
    {
      "name": "deploy",
      "description": "Deploy the application to production",
      "command": "./scripts/deploy.sh {{environment}}",
      "parameters": {
        "environment": {
          "type": "string",
          "description": "Deployment environment",
          "enum": ["staging", "production"]
        }
      }
    }
  ]
}
```

### Advanced Tool with Validation

```json
{
  "customTools": [
    {
      "name": "database-query",
      "description": "Run a database query",
      "command": "psql -d {{database}} -c \"{{query}}\"",
      "parameters": {
        "database": {
          "type": "string",
          "description": "Database name"
        },
        "query": {
          "type": "string",
          "description": "SQL query to execute"
        }
      },
      "validation": {
        "database": {
          "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*$",
          "message": "Invalid database name"
        }
      }
    }
  ]
}
```

### Tool Parameters

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | **Required.** Tool name |
| `description` | string | **Required.** What the tool does |
| `command` | string | **Required.** Shell command to execute |
| `parameters` | object | Parameter definitions |
| `validation` | object | Parameter validation rules |

### Parameter Types

```json
{
  "parameters": {
    "stringParam": {
      "type": "string",
      "description": "A string parameter",
      "default": "default value"
    },
    "numberParam": {
      "type": "number",
      "description": "A numeric parameter",
      "minimum": 0,
      "maximum": 100
    },
    "booleanParam": {
      "type": "boolean",
      "description": "A boolean flag"
    },
    "enumParam": {
      "type": "string",
      "description": "A choice parameter",
      "enum": ["option1", "option2", "option3"]
    }
  }
}
```

## Configuring MCP Servers

### Basic MCP Server

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
    }
  }
}
```

### MCP Server with Environment Variables

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "{{env.GITHUB_TOKEN}}"
      }
    }
  }
}
```

### MCP Server with Permissions

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    }
  },
  "permissions": {
    "postgres_*": "ask"
  }
}
```

## Managing Prompts

### External Prompt Files

Create prompt files in `.opencode/prompts/`:

```bash
# Create prompts directory
mkdir -p .opencode/prompts

# Create a prompt file
cat > .opencode/prompts/code-reviewer.txt << 'EOF'
You are an expert code reviewer. Focus on:
- Security vulnerabilities
- Performance issues
- Code maintainability
- Best practices

Provide specific, actionable feedback.
EOF
```

Reference in agent config:

```json
{
  "agent": {
    "reviewer": {
      "description": "Code reviewer agent",
      "mode": "subagent",
      "prompt": "{file:./prompts/code-reviewer.txt}"
    }
  }
}
```

### Inline Prompts

```json
{
  "agent": {
    "reviewer": {
      "description": "Code reviewer agent",
      "mode": "subagent",
      "prompt": "You are a code reviewer. Focus on security, performance, and maintainability."
    }
  }
}
```

## Creating Agent Workflows

### Subagent Delegation Pattern

**Orchestrator Agent** (primary):

```json
{
  "agent": {
    "orchestrator": {
      "description": "Orchestrates complex tasks by delegating to subagents",
      "mode": "primary",
      "prompt": "You are a task orchestrator. For complex tasks:\n1. Break down into subtasks\n2. Use the Task tool to delegate to appropriate subagents\n3. Synthesize results\n\nAvailable subagents:\n- @planner: Creates implementation plans\n- @coder: Writes and edits code\n- @reviewer: Reviews code quality",
      "permissions": {
        "task": {
          "*": "allow"
        }
      }
    }
  }
}
```

**Planner Subagent**:

```markdown
---
description: Creates detailed implementation plans
mode: subagent
tools:
  write: false
  edit: false
---

You are a technical planner. Create detailed, actionable plans.

Structure your plans:
1. Overview
2. Files to modify/create
3. Step-by-step implementation
4. Testing strategy
5. Potential risks
```

**Coder Subagent**:

```json
{
  "agent": {
    "coder": {
      "description": "Writes and edits code based on plans",
      "mode": "subagent",
      "tools": {
        "write": true,
        "edit": true,
        "read": true
      }
    }
  }
}
```

### Workflow Definition File

Create complex workflows in `.opencode/workflows/`:

```yaml
# .opencode/workflows/feature-development.yaml
name: Feature Development

trigger: primary agent delegates feature requests

steps:
  1_plan:
    agent: planner
    prompt: "Analyze requirements and create implementation plan for: {{task}}"
    output: plan

  2_implement:
    agent: coder
    prompt: "Implement based on plan:\n{{plan}}"
    tools: [write, edit, read]

  3_review:
    agent: reviewer
    prompt: "Review the implementation for quality and issues"
    tools: [read]
    optional: true

  4_finalize:
    agent: orchestrator
    prompt: "Summarize changes and suggest next steps"
```

## Configuration Structure

### Complete opencode.json Example

```json
{
  "$schema": "https://opencode.ai/config.json",
  
  "agent": {
    "build": {
      "mode": "primary",
      "model": "anthropic/claude-sonnet-4-20250514"
    },
    "plan": {
      "mode": "primary",
      "permissions": {
        "edit": "ask",
        "bash": "ask"
      }
    },
    "docs-writer": {
      "description": "Writes technical documentation",
      "mode": "subagent",
      "prompt": "{file:./prompts/docs-writer.txt}",
      "tools": {
        "bash": false
      }
    },
    "security-auditor": {
      "description": "Performs security audits",
      "mode": "subagent",
      "tools": {
        "write": false,
        "edit": false
      }
    }
  },
  
  "customTools": [
    {
      "name": "deploy",
      "description": "Deploy to environment",
      "command": "./scripts/deploy.sh {{env}}",
      "parameters": {
        "env": {
          "type": "string",
          "enum": ["staging", "production"]
        }
      }
    }
  ],
  
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    }
  },
  
  "permissions": {
    "bash": "ask",
    "edit": "allow",
    "postgres_*": "ask"
  }
}
```

### Directory Structure

```
.opencode/
├── opencode.json          # Main configuration
├── agents/                # Markdown agent definitions
│   ├── docs-writer.md
│   ├── security-auditor.md
│   └── code-reviewer.md
├── prompts/               # External prompt files
│   ├── docs-writer.txt
│   ├── security-prompt.txt
│   └── code-reviewer.txt
├── workflows/             # Workflow definitions
│   └── feature-development.yaml
└── tools/                 # Custom tool scripts
    ├── deploy.sh
    └── test-runner.sh
```

## Examples

### Example 1: Create a Documentation Agent

```bash
# 1. Find or create .opencode directory
mkdir -p .opencode/agents .opencode/prompts

# 2. Create the prompt file
cat > .opencode/prompts/docs-writer.txt << 'EOF'
You are a technical documentation writer. Create clear, comprehensive documentation.

Guidelines:
- Use clear, concise language
- Include code examples
- Structure with headers and lists
- Explain "why" not just "how"
EOF

# 3. Create the agent
cat > .opencode/agents/docs-writer.md << 'EOF'
---
description: Writes and maintains technical documentation
mode: subagent
temperature: 0.3
tools:
  bash: false
---

You are a technical writer. Create documentation that is:
- Clear and concise
- Well-structured
- Includes examples
- Accessible to the target audience
EOF
```

### Example 2: Create a Code Review Agent

```json
{
  "agent": {
    "code-reviewer": {
      "description": "Reviews code for quality and best practices",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "temperature": 0.1,
      "prompt": "You are an expert code reviewer. Focus on:\n- Security vulnerabilities\n- Performance issues\n- Maintainability\n- Best practices\n\nProvide specific, actionable feedback.",
      "tools": {
        "write": false,
        "edit": false,
        "read": true,
        "grep": true
      },
      "permissions": {
        "edit": "deny"
      }
    }
  }
}
```

### Example 3: Create a Deployment Tool

```json
{
  "customTools": [
    {
      "name": "deploy-app",
      "description": "Deploy application to specified environment",
      "command": "bash scripts/deploy.sh --env {{environment}} --version {{version}}",
      "parameters": {
        "environment": {
          "type": "string",
          "description": "Target deployment environment",
          "enum": ["development", "staging", "production"],
          "default": "staging"
        },
        "version": {
          "type": "string",
          "description": "Version to deploy (git tag or branch)",
          "default": "main"
        }
      }
    }
  ]
}
```

### Example 4: Create Agent Workflow

**Orchestrator** (primary agent):

```json
{
  "agent": {
    "feature-orchestrator": {
      "description": "Orchestrates feature development workflow",
      "mode": "primary",
      "prompt": "You coordinate feature development:\n1. Use @planner to create implementation plan\n2. Use @implementer to write code\n3. Use @tester to verify\n4. Summarize results\n\nDelegate tasks using Task tool.",
      "permissions": {
        "task": {
          "planner": "allow",
          "implementer": "allow",
          "tester": "allow"
        }
      }
    }
  }
}
```

**Subagents**:

```markdown
---
description: Creates implementation plans
mode: subagent
tools:
  write: false
  edit: false
---

Create detailed implementation plans with file structure, steps, and considerations.
```

```markdown
---
description: Implements code based on plans
mode: subagent
tools:
  write: true
  edit: true
  read: true
---

Implement features according to the provided plan. Follow best practices.
```

### Example 5: Add MCP Server

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "./data.db"]
    }
  },
  "permissions": {
    "sqlite_*": "ask"
  }
}
```

## Helper Scripts

### Script: opencode-init.sh

Initialize OpenCode configuration in current project:

```bash
#!/bin/bash
# opencode-init.sh - Initialize OpenCode configuration

OPENCODE_DIR=".opencode"

# Create directory structure
mkdir -p "$OPENCODE_DIR"/{agents,prompts,workflows,tools}

# Create base opencode.json
cat > "$OPENCODE_DIR/opencode.json" << 'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {},
  "customTools": [],
  "mcpServers": {},
  "permissions": {}
}
EOF

echo "OpenCode configuration initialized in $OPENCODE_DIR/"
```

### Script: create-agent.sh

Create a new agent:

```bash
#!/bin/bash
# create-agent.sh - Create a new OpenCode agent

AGENT_NAME="$1"
AGENT_MODE="${2:-subagent}"

if [ -z "$AGENT_NAME" ]; then
  echo "Usage: create-agent.sh <agent-name> [mode]"
  exit 1
fi

# Find .opencode directory
OPENCODE_DIR=""
CURRENT_DIR="$(pwd)"
while [ "$CURRENT_DIR" != "/" ]; do
  if [ -d "$CURRENT_DIR/.opencode" ]; then
    OPENCODE_DIR="$CURRENT_DIR/.opencode"
    break
  fi
  CURRENT_DIR="$(dirname "$CURRENT_DIR")"
done

# Default to global if not found
if [ -z "$OPENCODE_DIR" ]; then
  OPENCODE_DIR="$HOME/.config/opencode"
  mkdir -p "$OPENCODE_DIR/agents"
fi

cat > "$OPENCODE_DIR/agents/$AGENT_NAME.md" << EOF
---
description: $AGENT_NAME agent
mode: $AGENT_MODE
---

You are a $AGENT_NAME agent. Your purpose is to...
EOF

echo "Created agent: $OPENCODE_DIR/agents/$AGENT_NAME.md"
```

## Best Practices

### Agent Design

1. **Clear descriptions**: Make agent purpose obvious from description
2. **Appropriate restrictions**: Limit tools based on agent role
3. **Specific prompts**: Give clear instructions and guidelines
4. **Temperature tuning**: Use low temps (0.1-0.3) for analysis, higher (0.5-0.7) for creative tasks

### Tool Design

1. **Validate inputs**: Use parameter validation
2. **Clear descriptions**: Help LLM understand when to use the tool
3. **Safe defaults**: Set sensible defaults for optional parameters
4. **Idempotent**: Tools should be safe to run multiple times

### MCP Server Security

1. **Use permissions**: Set `ask` for destructive operations
2. **Limit scope**: Configure servers with minimal required access
3. **Env variables**: Store secrets in environment variables, not config

### Workflow Organization

1. **Single responsibility**: Each agent should have a focused purpose
2. **Clear handoffs**: Define what each subagent returns
3. **Error handling**: Plan for subagent failures
4. **Progress tracking**: Use todo lists for complex workflows

## Troubleshooting

### Agent not appearing

- Check agent file has correct YAML frontmatter
- Verify JSON syntax in opencode.json
- Restart OpenCode to reload config

### Tools not available

- Check permissions configuration
- Verify tool is enabled (not set to `false`)
- Check for conflicting permission rules

### MCP server errors

- Verify MCP server is installed (`npm list -g` or `pip list`)
- Check server command is in PATH
- Review server logs for errors

### Permission denied

- Check global permissions first
- Verify agent-specific permissions aren't more restrictive
- Use glob patterns carefully (order matters)

## References

- [Agents Documentation](https://opencode.ai/docs/agents/)
- [Tools Documentation](https://opencode.ai/docs/tools/)
- [Permissions Documentation](https://opencode.ai/docs/permissions/)
- [MCP Servers](https://opencode.ai/docs/mcp-servers/)
- [Custom Tools](https://opencode.ai/docs/custom-tools/)
