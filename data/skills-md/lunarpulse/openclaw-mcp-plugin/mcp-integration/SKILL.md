---
name: mcp-integration
description: Use Model Context Protocol servers to access external tools and data sources. Enable AI agents to discover and execute tools from configured MCP servers (legal databases, APIs, database connectors, weather services, etc.).
license: MIT
---

# MCP Integration Usage Guide

## Overview

Use the MCP integration plugin to discover and execute tools provided by external MCP servers. This skill enables you to access legal databases, query APIs, search databases, and integrate with any service that provides an MCP interface.

The plugin provides a unified `mcp` tool with two actions:
- `list` - Discover available tools from all connected servers
- `call` - Execute a specific tool with parameters

---

# Process

## 🔍 Phase 1: Tool Discovery

### 1.1 Check Available Tools

**Always start by listing available tools** to see what MCP servers are connected and what capabilities they provide.

**Action:**
```
{
  tool: "mcp",
  args: {
    action: "list"
  }
}
```

**Response structure:**
```json
[
  {
    "id": "server:toolname",
    "server": "server-name",
    "name": "tool-name", 
    "description": "What this tool does",
    "inputSchema": {
      "type": "object",
      "properties": {...},
      "required": [...]
    }
  }
]
```

### 1.2 Understand Tool Schemas

For each tool, examine:
- **id**: Format is `"server:toolname"` - split on `:` to get server and tool names
- **description**: Understand what the tool does
- **inputSchema**: JSON Schema defining parameters
  - `properties`: Available parameters with types and descriptions
  - `required`: Array of mandatory parameter names

### 1.3 Match Tools to User Requests

Common tool naming patterns:
- `search_*` - Find or search operations (e.g., `search_statute`, `search_users`)
- `get_*` - Retrieve specific data (e.g., `get_statute_full_text`, `get_weather`)
- `query` - Execute queries (e.g., `database:query`)
- `analyze_*` - Analysis operations (e.g., `analyze_law`)
- `resolve_*` - Resolve references (e.g., `resolve_citation`)

---

## 🎯 Phase 2: Tool Execution

### 2.1 Validate Parameters

Before calling a tool:
1. Identify all required parameters from `inputSchema.required`
2. Verify parameter types match schema (string, number, boolean, array, object)
3. Check for constraints (minimum, maximum, enum values, patterns)
4. Ensure you have necessary information from the user

### 2.2 Construct Tool Call

**Action:**
```
{
  tool: "mcp",
  args: {
    action: "call",
    server: "<server-name>",
    tool: "<tool-name>",
    args: {
      // Tool-specific parameters from inputSchema
    }
  }
}
```

**Example - Korean legal search:**
```
{
  tool: "mcp",
  args: {
    action: "call",
    server: "kr-legal",
    tool: "search_statute",
    args: {
      query: "연장근로 수당",
      limit: 5
    }
  }
}
```

### 2.3 Parse Response

Tool responses follow this structure:
```json
{
  "content": [
    {
      "type": "text",
      "text": "JSON string or text result"
    }
  ],
  "isError": false
}
```

For JSON responses:
```javascript
const data = JSON.parse(response.content[0].text);
// Access data.result, data.results, or direct properties
```

---

## 🔄 Phase 3: Multi-Step Workflows

### 3.1 Chain Tool Calls

For complex requests, execute multiple tools in sequence:

**Example - Legal research workflow:**
1. **Search** - `search_statute` to find relevant laws
2. **Retrieve** - `get_statute_full_text` for complete text
3. **Analyze** - `analyze_law` for interpretation
4. **Precedents** - `search_case_law` for related cases

Each step uses output from the previous step to inform the next call.

### 3.2 Maintain Context

Between tool calls:
- Extract relevant information from each response
- Use extracted data as parameters for subsequent calls
- Build up understanding progressively
- Present synthesized results to user

---

## ⚠ Phase 4: Error Handling

### 4.1 Common Errors

**"Tool not found: server:toolname"**
- Cause: Server not connected or tool doesn't exist
- Solution: Run `action: "list"` to verify available tools
- Check spelling of server and tool names

**"Invalid arguments for tool"**
- Cause: Missing required parameter or wrong type
- Solution: Review `inputSchema` from list response
- Ensure all required parameters provided with correct types

**"Server connection failed"**
- Cause: MCP server not running or unreachable
- Solution: Inform user service is temporarily unavailable
- Suggest alternatives if possible

### 4.2 Error Response Format

Errors return:
```json
{
  "content": [{"type": "text", "text": "Error: message"}],
  "isError": true
}
```

**Handle gracefully:**
- Explain what went wrong clearly
- Don't expose technical implementation details
- Suggest next steps or alternatives
- Don't retry excessively

---

# Complete Example

## User Request: "Find Korean laws about overtime pay"

### Step 1: Discover tools
```
{tool: "mcp", args: {action: "list"}}
```

Response shows `kr-legal:search_statute` with:
- Required: `query` (string)
- Optional: `limit` (number), `category` (string)

### Step 2: Execute search
```
{
  tool: "mcp",
  args: {
    action: "call",
    server: "kr-legal",
    tool: "search_statute",
    args: {
      query: "연장근로 수당",
      category: "노동법",
      limit: 5
    }
  }
}
```

### Step 3: Parse and present
```javascript
const data = JSON.parse(response.content[0].text);
// Present data.results to user
```

**User-facing response:**
```
Found 5 Korean statutes about overtime pay:

1. 근로기준법 제56조 (연장·야간 및 휴일 근로)
   - Overtime work requires 50% premium
   
2. 근로기준법 제50조 (근로시간)
   - Standard working hours: 40 hours per week

Would you like me to retrieve the full text of any statute?
```

---

# Quick Reference

## List Tools
```
{tool: "mcp", args: {action: "list"}}
```

## Call Tool
```
{
  tool: "mcp",
  args: {
    action: "call",
    server: "server-name",
    tool: "tool-name",
    args: {param1: "value1"}
  }
}
```

## Essential Patterns

**Tool ID parsing:** `"server:toolname"` → split on `:` for server and tool names

**Parameter validation:** Check `inputSchema.required` and `inputSchema.properties[param].type`

**Response parsing:** `JSON.parse(response.content[0].text)` for JSON responses

**Error detection:** Check `response.isError === true`

---

# Reference Documentation

## Core Documentation

- **Plugin README**: [README.md](README.md) - Installation and configuration
- **Real Example**: [REAL_EXAMPLE_KR_LEGAL.md](docs/REAL_EXAMPLE_KR_LEGAL.md) - Working kr-legal setup
- **API Reference**: [API.md](docs/API.md) - Technical API details
- **Configuration**: [CONFIGURATION.md](docs/CONFIGURATION.md) - Server configuration guide
- **Troubleshooting**: [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Common issues and solutions

## Usage Examples

- **Examples Collection**: [EXAMPLES.md](docs/EXAMPLES.md) - 13 real-world examples including:
  - Legal research workflows
  - Database queries
  - Weather service integration
  - Multi-step complex workflows
  - Error handling patterns

---

**Remember:** Always start with `action: "list"` when uncertain about available tools.
