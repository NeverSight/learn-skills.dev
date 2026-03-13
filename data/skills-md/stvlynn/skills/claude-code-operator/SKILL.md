---
name: claude-code-operator
description: "Operate and control Claude Code CLI from within Clawdbot. Allows spawning Claude Code processes, executing commands in Claude Code, managing sessions, and deploying projects using Claude Code's capabilities."
---

# Claude Code Operator

This skill enables controlling Claude Code CLI programmatically from Clawdbot.

## Overview

Claude Code is Anthropic's agentic coding tool that operates in the terminal. This skill provides workflows for:

1. **Spawning Claude Code processes** - Start Claude Code with specific configurations
2. **Executing commands** - Send natural language commands to Claude Code
3. **Managing sessions** - Resume, continue, or start new sessions
4. **Deploying projects** - Use Claude Code's MCP tools for deployment

## Prerequisites

- Claude Code must be installed: `npm install -g @anthropic-ai/claude-code`
- For Zhipu/Chinese users: Configure with GLM API key
- MCP servers configured in `~/.claude/mcp-settings.json`

## Configuration

### Zhipu (智谱) Configuration

Set environment variables before running Claude Code:

```bash
export ANTHROPIC_AUTH_TOKEN="your-zhipu-api-key"
export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic"
export API_TIMEOUT_MS="3000000"
```

Or configure in `~/.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-api-key",
    "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
    "API_TIMEOUT_MS": "3000000"
  }
}
```

### MCP Server Configuration

Add to `~/.claude/mcp-settings.json`:

```json
{
  "mcpServers": {
    "edgeone-pages-mcp-server": {
      "url": "https://mcp-on-edge.edgeone.app/mcp-server"
    }
  }
}
```

## CLI Commands

### Basic Commands

| Command | Description |
|---------|-------------|
| `claude` | Start Claude Code in current directory |
| `claude --version` | Check installed version |
| `claude --continue` | Resume last session |
| `claude --resume <name>` | Resume specific session |
| `claude -p` / `claude --print` | Print mode (non-interactive) |
| `claude --debug` | Debug mode with detailed logs |

### Internal Commands (within Claude Code)

| Command | Description |
|---------|-------------|
| `/mcp` | List available MCP servers and tools |
| `/help` | Show available commands |
| `/context` | Show context window usage |
| `/status` | Check current model and configuration |
| `/login` | Re-authenticate |
| `/plugin` | Manage plugins |

## Workflows

### Workflow 1: Deploy HTML to EdgeOne Pages

**Method 1: Using MCP directly (recommended)**

```bash
# Call deploy-html tool directly
curl -X POST https://mcp-on-edge.edgeone.app/mcp-server \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "deploy-html",
      "arguments": {
        "value": "HTML content here"
      }
    },
    "id": 1
  }'
```

**Method 2: Using Claude Code in print mode**

```bash
# Export environment variables first
export ANTHROPIC_AUTH_TOKEN="your-api-key"
export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic"

# Deploy using Claude Code
cd /path/to/project
echo "Deploy index.html to EdgeOne Pages" | claude -p
```

**Method 3: Interactive mode**

```bash
claude
# Then type: Deploy index.html to EdgeOne Pages
```

### Workflow 2: Execute Code Generation Task

```bash
# Start Claude Code with specific task
cd /path/to/project
claude -p << 'EOF'
Generate a React component for a todo list with the following features:
1. Add new todos
2. Mark todos as complete
3. Delete todos
4. Filter by status
EOF
```

### Workflow 3: Check MCP Tools Available

```bash
# List all MCP tools
curl -s -X POST https://mcp-on-edge.edgeone.app/mcp-server \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }' | jq '.result.tools'
```

## Environment Setup Script

Create a setup script for Zhipu users:

```bash
#!/bin/bash
# setup_claude_code_env.sh

echo "🚀 Setting up Claude Code environment..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+ first."
    exit 1
fi

# Check Node version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version must be 18+. Current: $(node --version)"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Install Claude Code if not present
if ! command -v claude &> /dev/null; then
    echo "📦 Installing Claude Code..."
    npm install -g @anthropic-ai/claude-code
else
    echo "✅ Claude Code already installed: $(claude --version)"
fi

# Create config directory
mkdir -p ~/.claude

# Configure for Zhipu
echo "🔑 Configuring for Zhipu..."
cat > ~/.claude/settings.json << 'CONFIGEOF'
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "YOUR_ZHIPU_API_KEY_HERE",
    "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": 1
  }
}
CONFIGEOF

echo ""
echo "✅ Configuration template created at ~/.claude/settings.json"
echo "⚠️  Please edit the file and replace YOUR_ZHIPU_API_KEY_HERE with your actual API key"
echo ""
echo "🎉 Setup complete! Run 'claude' to start using Claude Code."
```

## Troubleshooting

### Issue 1: "Invalid bearer token" or "Invalid API key"

**Cause**: API key not properly configured

**Solution**:
```bash
# Check if env vars are set
env | grep ANTHROPIC

# Or check config file
cat ~/.claude/settings.json

# Re-run setup script
bash setup_claude_code_env.sh
```

### Issue 2: MCP tools not found

**Cause**: MCP server not configured

**Solution**:
```bash
# Check MCP config
cat ~/.claude/mcp-settings.json

# Restart Claude Code after config changes
claude
```

### Issue 3: Claude Code hangs or timeouts

**Cause**: Network issues or API rate limits

**Solution**:
```bash
# Increase timeout
export API_TIMEOUT_MS="3000000"

# Or run in debug mode to see detailed logs
claude --debug
```

## Common Use Cases

### Use Case 1: Quick HTML Deployment

```bash
# Create HTML file
cat > demo.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>Demo</title></head>
<body><h1>Hello from Claude Code!</h1></body>
</html>
EOF

# Deploy using curl (fastest)
curl -X POST https://mcp-on-edge.edgeone.app/mcp-server \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "deploy-html",
      "arguments": {
        "value": "'"$(cat demo.html | sed 's/"/\\"/g')"'"
      }
    }
  }'
```

### Use Case 2: Batch Operations

```bash
# Process multiple files
for file in *.html; do
    echo "Processing $file..."
    # Send to Claude Code for processing
    cat "$file" | claude -p << 'EOF'
    Optimize this HTML for performance and accessibility
    EOF
done
```

### Use Case 3: CI/CD Integration

```bash
# In a CI/CD pipeline
claude -p << 'EOF'
Review the recent changes in this repository and:
1. Check for any security issues
2. Suggest performance improvements
3. Generate a summary of changes
EOF
```

## References

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Zhipu Claude Code Docs](https://docs.bigmodel.cn/cn/coding-plan/tool/claude)
- [EdgeOne MCP Documentation](https://pages.edgeone.ai/zh/document/pages-mcp)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)

## Notes

- Claude Code requires interactive authentication on first run
- For automated/scripted usage, prefer direct MCP API calls over Claude Code CLI
- Environment variables take precedence over config file settings
- Use `--debug` flag for troubleshooting connection issues
