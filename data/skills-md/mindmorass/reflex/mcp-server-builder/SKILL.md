---
name: mcp-server-builder
description: Build Model Context Protocol servers for Claude Code integration
---


# MCP Server Builder Skill

> Build new MCP servers following established patterns for consistency and reliability.

## Overview

This skill provides a template and guidelines for building new MCP servers that integrate with the agentic workspace. All servers follow the same patterns for:
- Configuration via environment variables
- Error handling and logging
- Tool registration
- Testing
- Documentation

## Prerequisites

```bash
pip install mcp>=1.0.0
```

## Server Template

### Step 1: Create Directory Structure

```bash
mcp/servers/{server-name}/
├── server.py           # Main server implementation
├── requirements.txt    # Python dependencies
├── test_{name}.py      # Test suite
├── README.md           # Server documentation
└── config.example.env  # Example configuration
```

### Step 2: Server Implementation Template

**File: `mcp/servers/{server-name}/server.py`**

```python
#!/usr/bin/env python3
"""
{Server Name} MCP Server - {Brief description}.
"""

import asyncio
import json
import logging
import os
from typing import Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server

# =============================================================================
# Configuration
# =============================================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
# Add server-specific config here
# EXAMPLE_API_KEY = os.getenv("EXAMPLE_API_KEY")
# EXAMPLE_TIMEOUT = int(os.getenv("EXAMPLE_TIMEOUT", "30"))

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# =============================================================================
# Server Implementation
# =============================================================================

class {ServerName}Server:
    """
    {Description of what this server does}.

    Tools provided:
    - tool_one: Description
    - tool_two: Description
    """

    def __init__(self):
        self.server = Server("{server-name}")
        self._validate_config()
        self._setup_tools()
        logger.info("{ServerName} server initialized")

    def _validate_config(self):
        """Validate required configuration."""
        # Example validation:
        # if not EXAMPLE_API_KEY:
        #     raise ValueError("EXAMPLE_API_KEY environment variable required")
        pass

    def _setup_tools(self):
        """Register MCP tools."""

        @self.server.tool()
        async def example_tool(
            param1: str,
            param2: Optional[int] = 10
        ) -> str:
            """
            Brief description of what this tool does.

            Args:
                param1: Description of param1
                param2: Description of param2 (default: 10)

            Returns:
                JSON string with result
            """
            try:
                logger.debug(f"example_tool called: param1={param1}, param2={param2}")

                # Implementation here
                result = {
                    "status": "success",
                    "param1": param1,
                    "param2": param2
                }

                return json.dumps(result)

            except Exception as e:
                logger.error(f"example_tool failed: {e}")
                return json.dumps({
                    "status": "error",
                    "error": str(e)
                })

        @self.server.tool()
        async def another_tool(query: str) -> str:
            """
            Another tool description.

            Args:
                query: The query to process
            """
            try:
                # Implementation
                return json.dumps({"result": query})
            except Exception as e:
                logger.error(f"another_tool failed: {e}")
                return json.dumps({"status": "error", "error": str(e)})

    async def run(self):
        """Run the MCP server."""
        logger.info("Starting {server-name} server...")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream)


# =============================================================================
# Entry Point
# =============================================================================

def main():
    server = {ServerName}Server()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
```

### Step 3: Requirements Template

**File: `mcp/servers/{server-name}/requirements.txt`**

```
mcp>=1.0.0
# Add server-specific dependencies below
# requests>=2.28.0
# aiohttp>=3.8.0
```

### Step 4: Test Template

**File: `mcp/servers/{server-name}/test_{name}.py`**

```python
#!/usr/bin/env python3
"""Tests for {server-name} MCP server."""

import json
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(__file__))

from server import {ServerName}Server


class Test{ServerName}Server:
    """Test suite for {ServerName}Server."""

    @pytest.fixture
    def server(self):
        """Create server instance for testing."""
        return {ServerName}Server()

    def test_server_initialization(self, server):
        """Test server initializes correctly."""
        assert server.server is not None
        assert server.server.name == "{server-name}"

    def test_config_validation(self):
        """Test configuration validation."""
        # Test with missing required config
        # with pytest.raises(ValueError):
        #     os.environ.pop("REQUIRED_VAR", None)
        #     {ServerName}Server()
        pass

    @pytest.mark.asyncio
    async def test_example_tool(self, server):
        """Test example_tool function."""
        # Get the tool function
        tools = server.server._tools
        example_tool = tools.get("example_tool")

        # Call it
        result = await example_tool("test_value", 20)
        data = json.loads(result)

        assert data["status"] == "success"
        assert data["param1"] == "test_value"
        assert data["param2"] == 20

    @pytest.mark.asyncio
    async def test_example_tool_defaults(self, server):
        """Test example_tool with default values."""
        tools = server.server._tools
        example_tool = tools.get("example_tool")

        result = await example_tool("test")
        data = json.loads(result)

        assert data["param2"] == 10  # default value

    @pytest.mark.asyncio
    async def test_error_handling(self, server):
        """Test error handling returns proper format."""
        # Trigger an error condition and verify response format
        pass


def test_imports():
    """Test all imports work."""
    from server import {ServerName}Server, main
    print("✅ Imports working")


def test_quick():
    """Quick smoke test."""
    server = {ServerName}Server()
    assert server is not None
    print("✅ Quick test passed")


if __name__ == "__main__":
    test_imports()
    test_quick()
    print("
✅ All basic tests passed!")
    print("Run 'pytest test_{name}.py -v' for full test suite")
```

### Step 5: README Template

**File: `mcp/servers/{server-name}/README.md`**

```markdown
# {Server Name} MCP Server

{Brief description of what this server does and why it exists.}

## Tools

| Tool | Description |
|------|-------------|
| `example_tool` | Does X with Y |
| `another_tool` | Does A with B |

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `EXAMPLE_API_KEY` | Yes | - | API key for service |

## Installation

```bash
cd mcp/servers/{server-name}
pip install -r requirements.txt
```

## Usage

### As MCP Server

Add to `.claude.json`:

```json
{
  "mcpServers": {
    "{server-name}": {
      "command": "python",
      "args": ["mcp/servers/{server-name}/server.py"],
      "env": {
        "EXAMPLE_API_KEY": "${EXAMPLE_API_KEY}"
      }
    }
  }
}
```

### Tool Examples

```python
# Example usage of example_tool
result = await example_tool(
    param1="value",
    param2=42
)

# Example usage of another_tool
result = await another_tool(query="search term")
```

## Testing

```bash
# Quick test
python test_{name}.py

# Full test suite
pytest test_{name}.py -v
```

## Development

{Any development notes, contribution guidelines, or known limitations.}
```

### Step 6: Example Config

**File: `mcp/servers/{server-name}/config.example.env`**

```bash
# {Server Name} Configuration
# Copy to .env and fill in values

# Logging
LOG_LEVEL=INFO

# Required
# EXAMPLE_API_KEY=your-api-key-here

# Optional
# EXAMPLE_TIMEOUT=30
```

## Patterns to Follow

### Error Handling

Always return JSON with consistent structure:

```python
# Success
{"status": "success", "data": {...}}

# Error
{"status": "error", "error": "Human-readable message"}
```

### Logging

Use structured logging:

```python
logger.debug(f"Tool called: {params}")      # Detailed debugging
logger.info(f"Operation completed: {id}")    # Normal operations
logger.warning(f"Retrying after: {error}")   # Recoverable issues
logger.error(f"Operation failed: {error}")   # Failures
```

### Configuration

- All config via environment variables
- Provide sensible defaults where possible
- Validate required config in `_validate_config()`
- Document all variables in README

### Tool Design

- One responsibility per tool
- Clear, descriptive names
- Comprehensive docstrings
- Type hints on all parameters
- Optional parameters have defaults

## MCP Config Integration

After building, add to `.claude.json`:

```json
{
  "mcpServers": {
    "{server-name}": {
      "command": "python",
      "args": ["mcp/servers/{server-name}/server.py"],
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## Verification Checklist

- [ ] Server starts without errors
- [ ] All tools registered correctly
- [ ] Tests pass
- [ ] README documents all tools
- [ ] Config example provided
- [ ] Added to .claude.json
- [ ] Error handling returns proper JSON

## Common Integrations

### HTTP API Client

```python
import aiohttp

class APIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def get(self, endpoint: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/{endpoint}",
                headers=self.headers
            ) as resp:
                return await resp.json()
```

### Database Connection

```python
import asyncpg

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.dsn)

    async def query(self, sql: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(sql, *args)
```

### Caching

```python
from functools import lru_cache
from datetime import datetime, timedelta

class TTLCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl = timedelta(seconds=ttl_seconds)
        self.cache = {}

    def get(self, key: str):
        if key in self.cache:
            value, expires = self.cache[key]
            if datetime.now() < expires:
                return value
            del self.cache[key]
        return None

    def set(self, key: str, value):
        self.cache[key] = (value, datetime.now() + self.ttl)
```

## Refinement Notes

> Add notes here as you build servers and discover improvements.

- [ ] Template validated with real server
- [ ] Async patterns confirmed working
- [ ] Error handling comprehensive
- [ ] Testing patterns sufficient
