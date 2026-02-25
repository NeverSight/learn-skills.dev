---
name: opencode-agent-creator
description: Create specialized OpenCode agents with proper configuration for primary agents and subagents
tags: [opencode, agent, ai, automation]
version: 1.0.0
---

# OpenCode Agent Creator

Use this skill when creating OpenCode agents - specialized AI assistants configured for specific tasks and workflows.

## When to Use

Use this skill when the user wants to:
- Create new OpenCode agents (primary or subagent)
- Configure specialized AI assistants for specific tasks
- Set up agents with custom prompts, models, and tool access
- Define agent permissions and behaviors

## Agent Types

### Primary Agents
Main assistants you interact with directly. Users can cycle through them using **Tab** key or the `switch_agent` keybind.

**Built-in examples:**
- **Build**: Full development with all tools enabled
- **Plan**: Analysis and planning with restricted permissions

### Subagents
Specialized assistants invoked by primary agents or manually via `@mention`. Used for specific tasks.

**Built-in examples:**
- **General**: Multi-step tasks with full tool access (except todo)
- **Explore**: Fast, read-only codebase exploration

## Agent Structure

OpenCode agents can be defined in two ways:

### 1. Markdown Files (Recommended)

Create `.md` files in:
- **Global**: `~/.config/opencode/agents/`
- **Per-project**: `.opencode/agents/`

**Format:**
```markdown
---
description: Brief description of agent purpose
mode: primary|subagent|all
model: provider/model-id (optional)
temperature: 0.0-1.0 (optional)
maxSteps: number (optional)
tools:
  write: true|false
  edit: true|false
  bash: true|false
permission:
  edit: allow|ask|deny
  bash:
    "*": allow|ask|deny
    "specific command": allow|ask|deny
  webfetch: allow|ask|deny
  task:
    "*": allow|ask|deny
    "agent-name": allow|ask|deny
hidden: true|false (optional, for subagents)
disable: true|false (optional)
---

System prompt content here.
Define the agent's purpose, behavior, and guidelines.
```

**Filename becomes agent name**: `code-reviewer.md` → `code-reviewer` agent

### 2. JSON Configuration

Add to `opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "agent-name": {
      "description": "Brief description",
      "mode": "primary",
      "model": "anthropic/claude-sonnet-4-20250514",
      "prompt": "{file:./prompts/agent.txt}",
      "temperature": 0.3,
      "maxSteps": 10,
      "tools": {
        "write": true,
        "edit": true,
        "bash": true
      },
      "permission": {
        "edit": "allow",
        "bash": {
          "*": "ask",
          "git status": "allow"
        }
      }
    }
  }
}
```

## Configuration Options

### Required
- **`description`**: Brief description of agent's purpose and when to use it

### Mode
- **`mode`**: `"primary"`, `"subagent"`, or `"all"` (default: `"all"`)
  - `primary`: User-facing agent, switchable via Tab
  - `subagent`: Invoked by other agents or via @mention
  - `all`: Can be used as both

### Optional
- **`prompt`**: Custom system prompt (inline or `{file:path}`)
- **`model`**: Override default model (format: `provider/model-id`)
- **`temperature`**: Control randomness (0.0-1.0)
  - `0.0-0.2`: Focused/deterministic (code analysis)
  - `0.3-0.5`: Balanced (general development)
  - `0.6-1.0`: Creative (brainstorming)
- **`maxSteps`**: Maximum agentic iterations before text-only response
- **`disable`**: Set `true` to disable agent
- **`hidden`**: Hide subagent from @mention autocomplete (subagents only)

### Tools
Control which tools are available:

```yaml
tools:
  write: true
  edit: false
  bash: false
  mymcp_*: false  # Wildcard to disable MCP server tools
```

### Permissions
Control what actions require approval:

```yaml
permission:
  edit: ask          # ask, allow, or deny
  bash:
    "*": ask         # Default for all commands
    "git status": allow
    "git log*": allow
    "git push": ask
  webfetch: deny
  task:              # Which subagents can be invoked
    "*": deny
    "code-*": allow  # Allow code-prefixed subagents
    "reviewer": ask
```

Values: `"allow"` (no approval), `"ask"` (prompt user), `"deny"` (disable)

### Provider-Specific Options
Any additional options pass through to the provider:

```yaml
reasoningEffort: high      # OpenAI reasoning models
textVerbosity: low         # OpenAI reasoning models
```

## Examples

### Documentation Writer

```markdown
---
description: Writes and maintains project documentation
mode: subagent
tools:
  bash: false
---

You are a technical writer. Create clear, comprehensive documentation.

Focus on:
- Clear explanations
- Proper structure
- Code examples
- User-friendly language
```

### Security Auditor

```markdown
---
description: Performs security audits and identifies vulnerabilities
mode: subagent
tools:
  write: false
  edit: false
permission:
  bash:
    "*": deny
---

You are a security expert. Focus on identifying potential security issues.

Look for:
- Input validation vulnerabilities
- Authentication and authorization flaws
- Data exposure risks
- Dependency vulnerabilities
- Configuration security issues
```

### Code Reviewer

```markdown
---
description: Reviews code for best practices and potential issues
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
tools:
  write: false
  edit: false
permission:
  bash:
    "*": ask
    "git diff": allow
    "git log*": allow
---

You are a code reviewer. Focus on security, performance, and maintainability.

Review checklist:
1. Code quality and best practices
2. Potential bugs and edge cases
3. Performance implications
4. Security considerations

Provide constructive feedback without making direct changes.
```

### Debug Agent

```markdown
---
description: Focused debugging with investigation tools
mode: primary
temperature: 0.2
tools:
  write: false
permission:
  bash:
    "*": allow
  edit: ask
---

You are a debugging specialist. Systematically investigate issues.

Approach:
1. Reproduce the issue
2. Gather relevant logs and context
3. Identify root cause
4. Suggest minimal fix
5. Recommend preventive measures
```

### Deep Thinker (Reasoning Model)

```markdown
---
description: High-effort reasoning for complex problems
mode: subagent
model: openai/gpt-5
temperature: 0.1
reasoningEffort: high
textVerbosity: low
maxSteps: 20
---

You solve complex problems with deep reasoning.

For each problem:
1. Break down into components
2. Analyze dependencies
3. Consider edge cases
4. Propose robust solutions
5. Validate approach
```

## Best Practices

1. **Clear descriptions**: Help users and agents understand when to invoke
2. **Appropriate mode**: Choose `primary` for main work, `subagent` for specialized tasks
3. **Tool restrictions**: Only enable tools the agent needs
4. **Permission granularity**: Use `ask` for risky operations, `allow` for safe ones
5. **Temperature tuning**: Lower for analytical tasks, higher for creative ones
6. **Prompt clarity**: Be specific about agent's role and constraints
7. **File location**:
   - Global: General-purpose agents across projects
   - Project: Project-specific workflows and conventions

## Implementation Steps

When creating an agent:

1. **Determine scope**:
   - Primary agent for main workflows
   - Subagent for specialized tasks

2. **Choose location**:
   - Global (`~/.config/opencode/agents/`) for reusable agents
   - Project (`.opencode/agents/`) for project-specific agents

3. **Define configuration**:
   - Required: `description`, `mode`
   - Optional: `model`, `temperature`, `maxSteps`, `tools`, `permission`

4. **Write system prompt**:
   - Clear role definition
   - Specific guidelines and constraints
   - Expected behaviors

5. **Test the agent**:
   - For primary: Switch to it with Tab
   - For subagent: Invoke with `@agent-name` or let primary agents use it

6. **Refine**:
   - Adjust temperature based on output quality
   - Fine-tune permissions based on usage
   - Update prompt for better results

## Usage

### Primary Agents
- Press **Tab** to cycle through primary agents
- Or use configured `switch_agent` keybind

### Subagents
- **Automatic**: Primary agents invoke based on descriptions
- **Manual**: `@agent-name message` to invoke directly
- **Navigation**: `<Leader>+Right/Left` to switch between parent/child sessions

## Interactive Creation

Use the built-in command:
```bash
opencode agent create
```

This will:
1. Ask for agent location (global/project)
2. Request description
3. Generate system prompt and identifier
4. Let you select tools
5. Create markdown file with configuration

## Notes

- Markdown filename determines agent name
- Custom agents can work alongside built-in agents
- Agent changes require OpenCode restart
- Model format: `provider/model-id` (e.g., `anthropic/claude-sonnet-4-20250514`)
- Hidden subagents (`hidden: true`) don't appear in autocomplete but can still be invoked programmatically
- Task permissions control which subagents an agent can invoke
