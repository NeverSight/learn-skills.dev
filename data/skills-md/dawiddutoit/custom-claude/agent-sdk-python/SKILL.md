---
name: agent-sdk-python
description: |
  Implements production-ready AI agents using the official Python SDK for autonomous workflows.
  Use when implementing agent workflows, SDK integration, one-shot queries, interactive
  conversations, custom MCP tools, permission control, CLAUDE.md context loading, error
  handling, hooks, or agent delegation. Works with .py files and agent architectures.
  Trigger terms: "Agent SDK", "query()", "ClaudeSDKClient", "@tool decorator",
  "setting_sources", "agent permissions", "SDK hooks".
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Bash
  - Grep
  - Glob
---

# Agent SDK Integration

## Purpose

Build production-ready AI agents using the **Agent SDK** for Python. This skill provides hands-on workflows for implementing agent features including simple queries, interactive conversations, custom MCP tools, permission control, context loading, and error handling.

## Quick Start

**Simple one-shot query:**
```python
from claude_agent_sdk import query

async for message in query(prompt="What is the capital of France?"):
    print(message)
```

**Interactive conversation:**
```python
from claude_agent_sdk import ClaudeSDKClient

async with ClaudeSDKClient() as client:
    await client.query("Hello!")
    async for msg in client.receive_response():
        print(msg)
```

## When to Use This Skill

**Explicit Triggers:**
- "build agent with SDK"
- "use query() function"
- "create ClaudeSDKClient"
- "implement agent workflows"
- "add custom MCP tools"
- "configure agent permissions"
- "load CLAUDE.md context"
- "implement agent hooks"

**Implicit Triggers:**
- Implementing autonomous agent behavior
- Creating interactive chat agents
- Building batch processing workflows
- Adding custom tools to agents
- Managing agent permissions
- Integrating project context into agents

**Debugging Scenarios:**
- Agent not connecting to CLI
- Tools not available to agent
- Permission denied errors
- Context not loading correctly
- Hooks not executing

## Instructions

### Step 1: Choose the Right API Mode

**Use `query()` for:**
- Simple one-shot questions
- Batch processing of independent tasks
- Stateless operations
- When all inputs are known upfront
- CI/CD automation scripts

**Use `ClaudeSDKClient` for:**
- Interactive conversations with follow-ups
- Chat applications or REPL interfaces
- When you need to send messages based on responses
- Long-running sessions with state management
- Interrupt capabilities

### Step 2: Build Simple Agent (query() Function)

**Basic implementation:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Analyze this code for security issues",
    options=ClaudeAgentOptions(
        system_prompt="You are a security expert",
        cwd="/path/to/project",
        permission_mode="default"
    )
):
    if hasattr(message, 'content'):
        print(message.content)
```

**Key configuration options:**
- `system_prompt`: Define agent expertise
- `cwd`: Set working directory
- `permission_mode`: Control tool execution ("default", "acceptEdits", "bypassPermissions")
- `model`: Choose model ("claude-sonnet-4", "claude-opus-4")

### Step 3: Build Interactive Agent (ClaudeSDKClient)

**Full conversation example:**
```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

async with ClaudeSDKClient(
    options=ClaudeAgentOptions(
        system_prompt="You are a helpful coding assistant",
        permission_mode="acceptEdits"
    )
) as client:
    # Send initial message
    await client.query("Help me write a Python web server")

    # Process response
    async for msg in client.receive_response():
        print(msg)

    # Follow-up question
    await client.query("Can you add error handling?")
    async for msg in client.receive_response():
        print(msg)
```

See [references/implementation-guide.md](./references/implementation-guide.md) for detailed patterns.

### Step 4: Create Custom MCP Tools

**Define tools with @tool decorator:**
```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("greet", "Greet a user by name", {"name": str})
async def greet(args):
    return {
        "content": [{"type": "text", "text": f"Hello, {args['name']}!"}]
    }

# Create MCP server
calculator = create_sdk_mcp_server(
    name="calculator",
    version="1.0.0",
    tools=[greet]
)

# Use with agent
options = ClaudeAgentOptions(
    mcp_servers={"calc": calculator},
    allowed_tools=["greet"]
)
```

See [references/implementation-guide.md](./references/implementation-guide.md) for error handling and advanced patterns.

### Step 5: Configure Permissions and Tool Access

**Fine-grained tool restrictions:**
```python
options = ClaudeAgentOptions(
    # Allow only specific tools
    allowed_tools=["Read", "Grep", "search_code"],

    # Block dangerous tools
    disallowed_tools=["Bash", "Write"],

    # Permission mode
    permission_mode="default"
)
```

**Dynamic permission callback:**
```python
from claude_agent_sdk import PermissionResultAllow, PermissionResultDeny

async def can_use_tool(tool_name, tool_input, context):
    if tool_name in ["Read", "Grep", "Glob"]:
        return PermissionResultAllow()

    if tool_name == "Bash" and "rm" in str(tool_input):
        return PermissionResultDeny(
            message="Destructive bash commands are not allowed",
            interrupt=True
        )

    return PermissionResultAllow()

options = ClaudeAgentOptions(can_use_tool=can_use_tool)
```

See [references/implementation-guide.md](./references/implementation-guide.md) for complete examples.

### Step 6: Load CLAUDE.md Context (setting_sources)

**Load project and user instructions:**
```python
options = ClaudeAgentOptions(
    # Load CLAUDE.md files
    setting_sources=["user", "project"],

    # user: ~/.claude/CLAUDE.md (user-level instructions)
    # project: ./CLAUDE.md or ./.claude/CLAUDE.md (project-level)

    cwd="/path/to/project"
)

async for message in query(
    prompt="Review this code following project standards",
    options=options
):
    print(message)
```

**When to use which source:**
- **"user"**: Personal preferences, global workflows
- **"project"**: Team standards, project architecture
- **"local"**: Machine-specific settings
- **Best practice**: Use `["user", "project"]` for most workflows

### Step 7: Implement Error Handling

**Try/catch with specific exceptions:**
```python
from claude_agent_sdk import (
    ClaudeSDKError,
    CLIConnectionError,
    CLINotFoundError,
    ProcessError
)

try:
    async for message in query(prompt="Hello"):
        print(message)

except CLINotFoundError:
    print("Install CLI: npm install -g claude-code")

except CLIConnectionError as e:
    print(f"Connection failed: {e}")

except ProcessError as e:
    print(f"Process error (exit {e.exit_code}): {e.stderr}")
```

See [references/implementation-guide.md](./references/implementation-guide.md) for retry patterns.

### Step 8: Add Hooks for Event-Driven Automation

**PreToolUse hook:**
```python
from claude_agent_sdk import HookMatcher

async def log_tool_use(input_data, tool_use_id, context):
    tool_name = input_data.get("tool", {}).get("name")
    print(f"About to use tool: {tool_name}")
    return {}  # Empty = allow

options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Bash|Write", hooks=[log_tool_use])
        ]
    }
)
```

See [references/implementation-guide.md](./references/implementation-guide.md) for PostToolUse and blocking patterns.

### Step 9: Implement Agent Delegation

**Define custom agents:**
```python
from claude_agent_sdk import AgentDefinition

options = ClaudeAgentOptions(
    agents={
        "python-expert": AgentDefinition(
            description="Python code expert",
            prompt="Expert Python developer",
            tools=["Read", "Write"],
            model="opus"
        )
    }
)

async for message in query(
    prompt="@python-expert Review this code",
    options=options
):
    print(message)
```

See [references/implementation-guide.md](./references/implementation-guide.md) for multi-agent patterns.

## Supporting Files

### References
- **[api-reference.md](./references/api-reference.md)** - Complete API documentation including all classes, functions, and types
- **[implementation-guide.md](./references/implementation-guide.md)** - Detailed patterns for all steps including production examples

### Scripts
- **[verify_sdk.py](./scripts/verify_sdk.py)** - Verify Agent SDK installation and configuration
- **[claude_agent_examples.py](./scripts/claude_agent_examples.py)** - 9 comprehensive examples for claude_agent module
- **[hook_integration_example.py](./scripts/hook_integration_example.py)** - Hook patterns and workflows

## Expected Outcomes

**Successful Agent Implementation:**
```
✅ Agent created with proper configuration
✅ Tools accessible and executing correctly
✅ Permissions enforced as expected
✅ Context loaded from CLAUDE.md files
✅ Error handling captures all exceptions
✅ Hooks executing at correct lifecycle points
```

**Common Issues:**
- **CLI not found**: Install with `npm install -g claude-code`
- **Permission denied**: Check `permission_mode` and `allowed_tools`
- **Tools unavailable**: Verify `mcp_servers` configuration
- **Context not loading**: Check `setting_sources` and `cwd` path

## Requirements

**Python Dependencies:**
```bash
pip install claude-agent-sdk
# or
uv pip install claude-agent-sdk
```

**System Requirements:**
```bash
# Claude CLI
npm install -g claude-code

# Verify installation
claude-code --version
```

**Environment Variables:**
```bash
# API Key (default)
export ANTHROPIC_API_KEY=your_key

# OR Amazon Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1

# OR Google Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

## Integration Points

### With Project Patterns

**ServiceResult Pattern:**
```python
from domain.value_objects import ServiceResult

async def agent_query_service(prompt: str) -> ServiceResult[list]:
    try:
        messages = []
        async for message in query(prompt=prompt):
            messages.append(message)
        return ServiceResult.success(messages)
    except ClaudeSDKError as e:
        return ServiceResult.failure(f"Agent query failed: {e}")
```

**Fail-Fast Imports:**
```python
# ✅ CORRECT - Fail fast
from claude_agent_sdk import query, ClaudeAgentOptions

# ❌ WRONG - Optional dependency
try:
    from claude_agent_sdk import query
except ImportError:
    query = None
```

See [references/implementation-guide.md](./references/implementation-guide.md) for dependency injection patterns.

## Common Patterns

### Code Review Agent
```python
async def code_review_agent(file_path: str):
    async for message in query(
        prompt=f"Review {file_path} for code quality",
        options=ClaudeAgentOptions(
            system_prompt="Senior code reviewer",
            setting_sources=["project"],
            allowed_tools=["Read", "Grep"]
        )
    ):
        yield message
```

### Batch Processing
```python
async def batch_analyze(files: list[str]):
    results = {}
    for file_path in files:
        messages = []
        async for msg in query(
            prompt=f"Analyze {file_path}",
            options=ClaudeAgentOptions(allowed_tools=["Read"])
        ):
            messages.append(msg)
        results[file_path] = messages
    return results
```

See [references/implementation-guide.md](./references/implementation-guide.md) for interactive debugging and production patterns.

## Red Flags to Avoid

- [ ] Using optional imports instead of fail-fast (violates project standards)
- [ ] Not handling CLINotFoundError (users get cryptic errors)
- [ ] Skipping permission configuration (security risk)
- [ ] Not loading project context with setting_sources (ignores team standards)
- [ ] Using bypassPermissions in production (dangerous)
- [ ] Not implementing error handling (unreliable agents)
- [ ] Hardcoding paths instead of using cwd parameter
- [ ] Not testing hooks before deployment
- [ ] Mixing query() and ClaudeSDKClient in same workflow (confusion)
- [ ] Not cleaning up client connections (resource leaks)

## Notes

- **API Mode Choice**: Use `query()` for one-shot, `ClaudeSDKClient` for interactive
- **Permission Modes**: "default" = ask user, "acceptEdits" = auto-accept, "bypassPermissions" = no checks
- **Context Loading**: Always use `["user", "project"]` for team workflows
- **Error Handling**: Always catch CLINotFoundError and CLIConnectionError
- **Hook Matchers**: Use regex patterns or None for all tools
- **Tool Restrictions**: Prefer `allowed_tools` over `disallowed_tools` for security
- **Agent Delegation**: Use @agent-name syntax in prompts
- **Production**: Always implement permission callbacks and logging hooks

## See Also

- **[API Reference](./references/api-reference.md)** - Complete API documentation
- **[Implementation Guide](./references/implementation-guide.md)** - Detailed patterns and examples
- **[Official SDK Documentation](https://docs.anthropic.com/en/docs/claude-code/claude-agent-sdk)** - Anthropic's official docs
