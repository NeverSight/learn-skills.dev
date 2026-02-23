---
name: memory-mcp
description: Use and troubleshoot the Memory MCP server for episodic memory retrieval and pattern analysis. Use when working with MCP server tools, validating the MCP implementation, or debugging MCP server issues.
---

# Memory MCP Server

Interacts with and troubleshoot the Memory Model Context Protocol (MCP) server for the self-learning memory system.

## Quick Reference

- **[Tools](tools.md)** - Complete MCP tools reference (query_memory, analyze_patterns, etc.)
- **[Configuration](configuration.md)** - .mcp.json structure and environment variables
- **[Validation](validation.md)** - MCP Inspector validation workflow
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
- **[Best Practices](best-practices.md)** - Tool usage, configuration, and testing guidelines
- **[Token Optimization](token-optimization.md)** - Reduce token usage by 80-85%

## When to Use

- Starting or configuring the memory-mcp server
- Using MCP tools for memory retrieval and pattern analysis
- Validating the MCP server implementation
- Debugging MCP server issues
- Testing MCP tools using the MCP inspector
- Understanding MCP configuration and environment variables

## MCP Server Overview

The memory-mcp server exposes episodic memory functionality through the Model Context Protocol:
- Query past experiences and learned patterns
- Analyze successful strategies from historical episodes
- Execute code in a secure sandbox environment
- Perform advanced statistical and predictive analysis
- Monitor server health and metrics

**Location**: `./target/release/memory-mcp-server`
**Configuration**: `.mcp.json`
**Transport**: stdio (Standard Input/Output)

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `query_memory` | Query episodic memory for relevant past experiences |
| `analyze_patterns` | Analyze patterns from past episodes |
| `advanced_pattern_analysis` | Statistical analysis, predictive modeling |
| `execute_agent_code` | Execute TypeScript/JavaScript in sandbox |
| `health_check` | Check server health status |
| `get_metrics` | Get comprehensive monitoring metrics |

See **[tools.md](tools.md)** for detailed tool documentation and **[best-practices.md](best-practices.md)** for usage guidelines.

## Starting the Server

```bash
# Build
cargo build --release --bin memory-mcp-server

# Run directly
export TURSO_DATABASE_URL="file:./data/memory.db"
./target/release/memory-mcp-server

# Run via MCP Inspector for testing
npx -y @modelcontextprotocol/inspector ./target/release/memory-mcp-server
```

See **[configuration.md](configuration.md)** for full environment setup and **[validation.md](validation.md)** for MCP Inspector workflow.
