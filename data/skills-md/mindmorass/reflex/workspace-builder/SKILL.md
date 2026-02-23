---
name: workspace-builder
description: Set up and configure development workspaces
---


# Workspace Builder Skill

> Master specification for building the agentic workflow system.
> This skill is **reference documentation** - use component-specific skills for building.

## Overview

This workspace provides a reusable, multi-project automation system with:
- Semantic routing for intelligent resource selection
- RAG (vector search) with project isolation
- Modular agents, skills, and commands
- Template-based architecture for cloning to new projects

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER QUERY                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SEMANTIC ROUTER                               │
│  Tier 1: Category (command | agent | skill | workflow)          │
│  Tier 2: Specific resource (e.g., "researcher" agent)           │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌─────────┐     ┌─────────┐     ┌─────────┐
        │Commands │     │ Agents  │     │Workflows│
        └─────────┘     └─────────┘     └─────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   RAG Server    │
                    │    (Qdrant)     │
                    └─────────────────┘
```

## Component Build Order

Build in this sequence for incremental testing:

### Phase 1: Foundation
1. **Directory structure** ✅
2. **CLAUDE.md** ✅
3. **Config files** (base.yaml, .env.template)
4. **Setup scripts** (setup.sh, init-project.sh)

### Phase 2: Core Services
5. **RAG Server** → See `skills/rag-builder/SKILL.md`
6. **Router** → See `skills/router-builder/SKILL.md`

### Phase 3: Interface Layer
7. **Slash Commands** (research, code-review, daily-standup)
8. **MCP Config** (wire up servers)

### Phase 4: Agents
9. **Sub-agents** → See `skills/agent-builder/SKILL.md`
10. **Orchestrator** (ties everything together)

### Phase 5: Automation
11. **Workflows** (YAML definitions + executor)
12. **Service management** (start/stop scripts)

## Key Technical Decisions

### Vector Database: Qdrant
```python
# Why Qdrant:
# - High performance vector search
# - Production-ready with persistence
# - REST and gRPC APIs
# - Excellent filtering capabilities

from qdrant_client import QdrantClient
client = QdrantClient(url="http://localhost:6333")
# Collections managed via MCP server with COLLECTION_NAME env var
```

### Embeddings: all-MiniLM-L6-v2
```python
# Shared across RAG and Router
# - Fast (384 dimensions)
# - Good quality
# - Runs locally

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
```

### Routing: Semantic Router
```python
# Why Semantic Router:
# - ~10ms decisions (not LLM calls)
# - Scales to 1000s of resources
# - Same embeddings as RAG

from semantic_router import Route, RouteLayer
```

## Configuration Strategy

### Layered Config
```
config/base.yaml      # Defaults (version controlled)
config/local.yaml     # Overrides (git-ignored)
.env                  # Secrets (git-ignored)
```

### Multi-Project Pattern
```bash
# Clone template
git clone <repo> project-alpha
cd project-alpha

# Initialize project
./scripts/init-project.sh project-alpha

# Creates:
# - .env.project-alpha (credentials)
# - config/profiles/project-alpha.yaml
# - Isolated RAG collections
```

## File Templates

### Slash Command Template
```markdown

# Command Name

You are executing the **command-name** command.

## Instructions

1. First step
2. Second step
3. Output format

## Output

Describe expected output format.
```

### Agent Prompt Template
```markdown
# Agent Name

You are a specialized **Agent Name** focused on [domain].

## Core Capabilities

1. Capability one
2. Capability two

## Tools Available

- `tool_name`: Description

## Operating Principles

- Principle one
- Principle two

## Output Standards

- Standard one
- Standard two
```

### Route Definition Template
```yaml
routes:
  - name: resource-name
    utterances:
      - "example phrase one"
      - "example phrase two"
      - "variation three"
      - "variation four"
      - "at least 5-10 examples"
    metadata:
      file: "path/to/resource"
      description: "What this resource does"
```

## Testing Strategy

### Incremental Testing
```bash
# Test RAG server
python -c "from rag.server import RAGServer; print('RAG OK')"

# Test router
python -c "from routing.router import route; print(route('test query'))"

# Test full flow
python -c "
from routing.router import route
result = route('research quantum computing')
print(f'Routed to: {result.category}/{result.resource_name}')
"
```

### Integration Test
```bash
# Start all services
./scripts/start-services.sh

# Test via MCP
# (use Claude Code to interact)
```

## Refinement Process

As we build, update docs when:
1. Implementation differs from spec
2. Better patterns emerge
3. Edge cases are discovered

```bash
# After implementing a component:
# 1. Test it works
# 2. Update relevant SKILL.md with actual code
# 3. Update CLAUDE.md status
# 4. Commit with descriptive message
```

## Dependencies

```
# requirements.txt
pyyaml>=6.0
python-dotenv>=1.0.0
mcp>=1.0.0
qdrant-client>=1.7.0
sentence-transformers>=2.2.0
semantic-router>=0.1.0
aiofiles>=23.0.0
httpx>=0.25.0
```

## Next Action

To start building, use one of the component skills:
- `view skills/rag-builder/SKILL.md` - Build RAG server first
- `view skills/router-builder/SKILL.md` - Build semantic router
- `view skills/agent-builder/SKILL.md` - Build sub-agents
