---
name: agno
description: Agno AI agent framework - build production-ready agents, multi-agent teams, workflows, MCP integrations, and deploy with AgentOS. Use when building, debugging, or learning about Agno agents.
---

# Agno Skill

Build production-ready AI agents with Agno - a lightweight, model-agnostic framework for agents, teams, workflows, and MCP integration.

## When to Use This Skill

This skill should be triggered when:
- Building AI agents with tools, memory, structured outputs, or knowledge
- Creating multi-agent teams with role-based delegation
- Implementing workflows with sequential, parallel, conditional, or routing steps
- Integrating MCP servers (stdio, SSE, or Streamable HTTP)
- Deploying agents with AgentOS (FastAPI-based runtime)
- Working with the LearningMachine (user profiles, entity memory, session context)
- Debugging agent behavior or optimizing performance

## Architecture Overview

```
Agent          - Single autonomous AI unit (model + tools + instructions)
Team           - Multiple agents coordinated by a leader (route/broadcast/tasks modes)
Workflow       - Pipeline-based execution (Step, Parallel, Condition, Loop, Router)
AgentOS        - FastAPI runtime for deploying agents as production APIs
LearningMachine - Persistent learning across sessions (profiles, memory, knowledge)
```

## Quick Reference

### 1. Basic Agent with Tools

```python
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools

agent = Agent(
    name="Finance Agent",
    model=Gemini(id="gemini-3-flash-preview"),
    tools=[YFinanceTools()],
    add_datetime_to_context=True,
    markdown=True,
)

agent.print_response("Give me a quick brief on NVIDIA", stream=True)
```

### 2. Structured Output with Pydantic

```python
from typing import List, Optional
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from pydantic import BaseModel, Field

class StockAnalysis(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    company_name: str = Field(..., description="Full company name")
    current_price: float = Field(..., description="Current price in USD")
    summary: str = Field(..., description="One-line summary")
    key_drivers: List[str] = Field(..., description="2-3 key growth drivers")
    recommendation: str = Field(..., description="Buy, Hold, or Sell")

agent = Agent(
    model=Gemini(id="gemini-3-flash-preview"),
    tools=[YFinanceTools()],
    output_schema=StockAnalysis,
)

response = agent.run("Analyze NVIDIA")
analysis: StockAnalysis = response.content
print(f"{analysis.company_name}: {analysis.recommendation}")
```

### 3. Agent with Storage (Session Persistence)

```python
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini

agent = Agent(
    model=Gemini(id="gemini-3-flash-preview"),
    db=SqliteDb(db_file="tmp/agents.db"),
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# Same session_id = continuous conversation across runs
agent.print_response("Analyze NVDA", session_id="my-session", stream=True)
agent.print_response("Compare that to Tesla", session_id="my-session", stream=True)
```

### 4. Agent with Memory (User Preferences)

```python
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager
from agno.models.google import Gemini

db = SqliteDb(db_file="tmp/agents.db")

agent = Agent(
    model=Gemini(id="gemini-3-flash-preview"),
    db=db,
    memory_manager=MemoryManager(
        model=Gemini(id="gemini-3-flash-preview"),
        db=db,
    ),
    enable_agentic_memory=True,  # Agent decides when to store/recall
    markdown=True,
)

# Agent remembers user preferences across sessions
agent.print_response(
    "I'm interested in AI stocks. My risk tolerance is moderate.",
    user_id="alice@example.com",
    stream=True,
)
```

### 5. Multi-Agent Team

```python
from agno.agent import Agent
from agno.models.google import Gemini
from agno.team.team import Team
from agno.tools.yfinance import YFinanceTools

bull = Agent(
    name="Bull Analyst",
    role="Make the investment case FOR a stock",
    model=Gemini(id="gemini-3-flash-preview"),
    tools=[YFinanceTools()],
)

bear = Agent(
    name="Bear Analyst",
    role="Make the investment case AGAINST a stock",
    model=Gemini(id="gemini-3-flash-preview"),
    tools=[YFinanceTools()],
)

team = Team(
    name="Investment Research",
    model=Gemini(id="gemini-3-flash-preview"),
    members=[bull, bear],
    instructions=["Get both perspectives, then synthesize a balanced recommendation"],
    show_members_responses=True,
    markdown=True,
)

team.print_response("Should I invest in NVIDIA?", stream=True)
```

### 6. Sequential Workflow

```python
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from agno.workflow import Step, Workflow

data_agent = Agent(name="Data Gatherer", model=Gemini(id="gemini-3-flash-preview"), tools=[YFinanceTools()])
analyst = Agent(name="Analyst", model=Gemini(id="gemini-3-flash-preview"))
writer = Agent(name="Report Writer", model=Gemini(id="gemini-3-flash-preview"), markdown=True)

workflow = Workflow(
    name="Research Pipeline",
    steps=[
        Step(name="Gather Data", agent=data_agent),
        Step(name="Analyze", agent=analyst),
        Step(name="Write Report", agent=writer),
    ],
)

workflow.print_response("Analyze NVIDIA for investment", stream=True)
```

### 7. MCP Server Integration (stdio)

```python
import asyncio
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools

async def run_agent(message: str) -> None:
    async with MCPTools(command="uvx mcp-server-git") as mcp_tools:
        agent = Agent(model=Claude(id="claude-sonnet-4-5-20250929"), tools=[mcp_tools])
        await agent.aprint_response(message, stream=True)

asyncio.run(run_agent("What is the license for this project?"))
```

### 8. MCP Server (Streamable HTTP)

```python
import asyncio
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools

async def run_agent(message: str) -> None:
    async with MCPTools(
        transport="streamable-http",
        url="https://docs.agno.com/mcp",
    ) as mcp_tools:
        agent = Agent(model=Claude(id="claude-sonnet-4-5-20250929"), tools=[mcp_tools], markdown=True)
        await agent.aprint_response(message, stream=True)

asyncio.run(run_agent("What is Agno?"))
```

### 9. Multiple MCP Servers

```python
import asyncio
from os import getenv
from agno.agent import Agent
from agno.tools.mcp import MultiMCPTools

async def run_agent(message: str) -> None:
    mcp_tools = MultiMCPTools(
        commands=["npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt"],
        urls=["http://localhost:8000/mcp"],
        urls_transports=["streamable-http"],
        timeout_seconds=30,
    )
    await mcp_tools.connect()
    agent = Agent(tools=[mcp_tools], markdown=True)
    await agent.aprint_response(message, stream=True)
    await mcp_tools.close()

asyncio.run(run_agent("Find listings in Barcelona"))
```

### 10. LearningMachine (Persistent Learning)

```python
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import LearningMachine, LearningMode, UserProfileConfig
from agno.models.openai import OpenAIResponses

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    learning=LearningMachine(
        user_profile=UserProfileConfig(mode=LearningMode.ALWAYS),
    ),
    markdown=True,
)

agent.print_response("Hi! I'm Alice, call me Ali.", user_id="alice@example.com", stream=True)
# Profile fields (name, preferred_name) captured automatically
```

## Key Patterns

### Pattern: MCP Connection Lifecycle
Always close MCP connections. Use async context managers or try/finally:
```python
# Preferred: context manager
async with MCPTools(command="uvx mcp-server-git") as tools:
    agent = Agent(tools=[tools])
    await agent.aprint_response("query")

# Alternative: manual lifecycle
tools = MCPTools(command="uvx mcp-server-git")
await tools.connect()
try:
    agent = Agent(tools=[tools])
    await agent.aprint_response("query")
finally:
    await tools.close()
```

### Pattern: Production Database (PostgreSQL)
```python
from agno.db.postgres import PostgresDb
db = PostgresDb(db_url="postgresql+psycopg://user:pass@localhost:5432/agno")
agent = Agent(db=db, add_history_to_context=True)
```

### Pattern: Debug Mode
```python
agent = Agent(debug_mode=True)  # Detailed logs of messages, tools, tokens
```

### Pattern: Custom Tools
```python
from agno.tools.decorator import tool

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"Weather in {city}: 72F, sunny"

agent = Agent(tools=[get_weather])
```

## Important Rules

- **Never create agents in loops** - reuse agents for performance
- **Use `output_schema`** for structured responses (not free-form parsing)
- **PostgreSQL for production**, SQLite only for development
- **Both sync and async** - all public methods have async variants (prefix with `a`)
- **Always close MCP connections** - use try/finally or async context managers
- **Enable `debug_mode=True`** when troubleshooting

## Reference Files

Detailed documentation is available in `references/`:

- **agents.md** - Agent parameters, configuration, tools, memory, knowledge, guardrails
- **teams.md** - Team modes (route/broadcast/tasks), member coordination
- **workflows.md** - Step types (Step, Parallel, Condition, Loop, Router)
- **mcp.md** - MCP integration (stdio, SSE, Streamable HTTP), MultiMCPTools
- **tools.md** - Built-in tools list, custom tool creation, tool hooks
- **learning.md** - LearningMachine stores (profile, memory, session, knowledge, entity)
- **models.md** - Supported model providers and configuration

## Resources

- **Documentation**: https://docs.agno.com
- **GitHub**: https://github.com/agno-agi/agno
- **Cookbook Examples**: https://github.com/agno-agi/agno/tree/main/cookbook
- **Install**: `pip install agno`
