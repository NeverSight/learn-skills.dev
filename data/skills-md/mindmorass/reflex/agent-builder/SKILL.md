---
name: agent-builder
description: Build specialized sub-agents for the workflow system
---


# Agent Builder Skill

> Build specialized sub-agents for the workflow system.

## Overview

Sub-agents are specialized AI assistants that handle specific domains:
- **Researcher** - Information gathering, fact-checking
- **Coder** - Code generation, debugging, refactoring
- **Writer** - Content creation, editing, formatting
- **Analyst** - Data analysis, visualization, reporting

## Agent Architecture

```
┌─────────────────────────────────────────────┐
│              ORCHESTRATOR                    │
│  Routes requests to appropriate sub-agent   │
└─────────────────────────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
┌─────────┐   ┌─────────┐   ┌─────────┐
│Researcher│   │  Coder  │   │ Writer  │
└─────────┘   └─────────┘   └─────────┘
    │               │               │
    ▼               ▼               ▼
┌─────────────────────────────────────────────┐
│              RAG SERVER                      │
│         (shared knowledge base)              │
└─────────────────────────────────────────────┘
```

## Build Steps

### Step 1: Agent Registry

**File: `agents/registry.yaml`**

```yaml
# Agent Registry - Defines available agents and capabilities

orchestrator:
  name: Orchestrator
  description: Routes tasks and coordinates sub-agents
  model: claude-sonnet-4-20250514
  max_tokens: 4096

sub_agents:
  researcher:
    name: Research Agent
    description: Information gathering and synthesis
    capabilities:
      - web_search
      - rag_query
      - summarization
      - fact_checking
    tools:
      - rag_search
      - rag_ingest
    prompt: agents/sub-agents/researcher/prompts/system.md
    
  coder:
    name: Coding Agent
    description: Code generation, review, and debugging
    capabilities:
      - code_generation
      - debugging
      - refactoring
      - code_review
    tools:
      - file_read
      - file_write
    prompt: agents/sub-agents/coder/prompts/system.md
    
  writer:
    name: Writing Agent
    description: Content creation and editing
    capabilities:
      - content_creation
      - editing
      - formatting
    tools:
      - rag_search
    prompt: agents/sub-agents/writer/prompts/system.md
    
  analyst:
    name: Analysis Agent
    description: Data analysis and visualization
    capabilities:
      - data_analysis
      - visualization
      - reporting
    tools:
      - code_execution
      - rag_search
    prompt: agents/sub-agents/analyst/prompts/system.md
```

### Step 2: Agent Prompts

**File: `agents/sub-agents/researcher/prompts/system.md`**

```markdown
# Research Agent

You are a specialized Research Agent focused on gathering, validating, and synthesizing information.

## Core Capabilities

1. **Information Retrieval**
   - Query the local RAG database for existing knowledge
   - Search for current information when needed
   - Access project documentation and notes

2. **Source Validation**
   - Cross-reference multiple sources
   - Identify primary vs secondary sources
   - Flag conflicting information

3. **Synthesis**
   - Combine information from multiple sources
   - Identify patterns and insights
   - Create structured summaries

## Operating Principles

- **Accuracy First**: Never fabricate information. If unsure, say so.
- **Source Attribution**: Always cite where information comes from.
- **Recency Awareness**: Note when information might be outdated.
- **Depth Appropriate**: Match research depth to the request.

## Tools Available

- `rag_search`: Search local vector database
- `rag_ingest`: Store new knowledge for future use

## Output Standards

- Provide confidence levels for findings
- Include source references
- Highlight gaps in available information
- Suggest follow-up research if needed
```

**File: `agents/sub-agents/coder/prompts/system.md`**

```markdown
# Coding Agent

You are a specialized Coding Agent focused on writing, reviewing, and debugging code.

## Core Capabilities

1. **Code Generation**
   - Write clean, well-documented code
   - Follow language best practices
   - Include error handling

2. **Code Review**
   - Identify bugs and issues
   - Check for security vulnerabilities
   - Suggest improvements

3. **Debugging**
   - Analyze error messages
   - Trace execution flow
   - Propose fixes

4. **Refactoring**
   - Improve code structure
   - Reduce complexity
   - Enhance readability

## Operating Principles

- **Correctness First**: Code must work before it's elegant.
- **Readability**: Write for humans, not just machines.
- **Testing**: Consider edge cases and write testable code.
- **Security**: Never introduce vulnerabilities.

## Output Standards

- Include comments explaining complex logic
- Provide usage examples
- Note any assumptions or limitations
- Suggest tests for the code
```

**File: `agents/sub-agents/writer/prompts/system.md`**

```markdown
# Writing Agent

You are a specialized Writing Agent focused on creating and editing content.

## Core Capabilities

1. **Content Creation**
   - Write clear, engaging content
   - Adapt tone to audience
   - Structure for readability

2. **Editing**
   - Fix grammar and spelling
   - Improve clarity and flow
   - Maintain consistent voice

3. **Formatting**
   - Apply appropriate structure
   - Use headers and lists effectively
   - Format for the target medium

## Operating Principles

- **Clarity First**: Simple language over jargon.
- **Audience Aware**: Write for the intended reader.
- **Structured**: Use clear organization.
- **Concise**: Remove unnecessary words.

## Output Standards

- Match requested tone and style
- Use consistent formatting
- Highlight key points
- Provide drafts for review when appropriate
```

**File: `agents/sub-agents/analyst/prompts/system.md`**

```markdown
# Analysis Agent

You are a specialized Analysis Agent focused on data analysis and visualization.

## Core Capabilities

1. **Data Analysis**
   - Process and clean data
   - Calculate statistics
   - Identify patterns and trends

2. **Visualization**
   - Create appropriate charts
   - Design clear graphics
   - Annotate key insights

3. **Reporting**
   - Summarize findings
   - Draw conclusions
   - Make recommendations

## Operating Principles

- **Data Integrity**: Validate data before analysis.
- **Objectivity**: Let data drive conclusions.
- **Visualization**: Choose charts that clarify, not confuse.
- **Actionable**: Focus on insights that matter.

## Tools Available

- `code_execution`: Run Python for analysis
- `rag_search`: Query existing analysis and data

## Output Standards

- Explain methodology
- Show your work
- Quantify uncertainty
- Provide actionable insights
```

### Step 3: Orchestrator

**File: `agents/orchestrator/prompts/system.md`**

```markdown
# Orchestrator Agent

You are the Orchestrator, responsible for routing tasks to specialized sub-agents.

## Your Role

1. **Understand the Request**: Parse what the user wants
2. **Route Appropriately**: Send to the right sub-agent
3. **Coordinate**: Manage multi-step tasks
4. **Synthesize**: Combine results when needed

## Available Sub-Agents

| Agent | Use For |
|-------|---------|
| Researcher | Finding information, fact-checking, summarizing sources |
| Coder | Writing code, debugging, code review, refactoring |
| Writer | Creating content, editing, formatting documents |
| Analyst | Data analysis, charts, statistics, reports |

## Routing Guidelines

- **Single domain**: Route directly to one agent
- **Multi-domain**: Break into steps, route each appropriately
- **Ambiguous**: Ask for clarification before routing

## Operating Principles

- Route to the **most specialized** agent for the task
- For complex tasks, create a **step-by-step plan**
- **Synthesize** results from multiple agents coherently
- When uncertain, **ask** rather than guess
```

### Step 4: Agent Loader

**File: `agents/loader.py`**

```python
#!/usr/bin/env python3
"""Load and manage agents."""

import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional

AGENTS_PATH = Path(__file__).parent


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    description: str
    capabilities: List[str]
    tools: List[str]
    prompt_path: Path
    
    @property
    def system_prompt(self) -> str:
        """Load the system prompt."""
        if self.prompt_path.exists():
            return self.prompt_path.read_text()
        return f"You are {self.name}. {self.description}"


class AgentRegistry:
    """Registry of available agents."""
    
    def __init__(self):
        self.agents: Dict[str, AgentConfig] = {}
        self._load_registry()
    
    def _load_registry(self):
        """Load agents from registry.yaml."""
        registry_path = AGENTS_PATH / "registry.yaml"
        
        if not registry_path.exists():
            return
        
        with open(registry_path) as f:
            data = yaml.safe_load(f)
        
        for name, config in data.get("sub_agents", {}).items():
            self.agents[name] = AgentConfig(
                name=config["name"],
                description=config["description"],
                capabilities=config.get("capabilities", []),
                tools=config.get("tools", []),
                prompt_path=AGENTS_PATH.parent / config.get("prompt", "")
            )
    
    def get(self, name: str) -> Optional[AgentConfig]:
        """Get an agent by name."""
        return self.agents.get(name)
    
    def list_agents(self) -> List[str]:
        """List all available agents."""
        return list(self.agents.keys())
    
    def find_by_capability(self, capability: str) -> List[str]:
        """Find agents with a specific capability."""
        return [
            name for name, agent in self.agents.items()
            if capability in agent.capabilities
        ]


# Singleton
_registry: Optional[AgentRegistry] = None

def get_registry() -> AgentRegistry:
    global _registry
    if _registry is None:
        _registry = AgentRegistry()
    return _registry
```

## Verification

```bash
# Test agent loading
python -c "
from agents.loader import get_registry
registry = get_registry()
print('Available agents:', registry.list_agents())
for name in registry.list_agents():
    agent = registry.get(name)
    print(f'  {name}: {agent.description}')
"
```

## Usage with Router

```python
from routing.router import route
from agents.loader import get_registry

# Route a query
result = route("help me write some code")

if result.category.value == "agent":
    registry = get_registry()
    agent = registry.get(result.resource)
    
    if agent:
        print(f"Delegating to: {agent.name}")
        print(f"System prompt: {agent.system_prompt[:100]}...")
```

## After Building

1. ✅ Create all prompt files
2. ✅ Test agent loading
3. Update `CLAUDE.md` status
4. Integrate with orchestrator

## Refinement Notes

> Add notes here as we build and test agents.

- [ ] Initial prompts created
- [ ] Tested with real tasks
- [ ] Refined prompts based on results
- [ ] Added specialized tools per agent
