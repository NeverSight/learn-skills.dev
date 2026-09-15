---
name: openviking-context-database
description: Expert skill for using OpenViking, the open-source context database for AI Agents that manages memory, resources, and skills via a filesystem paradigm.
triggers:
  - set up OpenViking for my AI agent
  - how do I use OpenViking context database
  - configure OpenViking with my LLM provider
  - add memory to my AI agent with OpenViking
  - OpenViking filesystem context management
  - integrate OpenViking RAG into my project
  - OpenViking agent memory and skills setup
  - how to query OpenViking context database
---

# OpenViking Context Database

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

OpenViking is an open-source **context database** for AI Agents that replaces fragmented vector stores with a unified **filesystem paradigm**. It manages agent memory, resources, and skills in a tiered L0/L1/L2 structure, enabling hierarchical context delivery, observable retrieval trajectories, and self-evolving session memory.

---

## Installation

### Python Package

```bash
pip install openviking --upgrade --force-reinstall
```

### Optional Rust CLI

```bash
# Install via script
curl -fsSL https://raw.githubusercontent.com/volcengine/OpenViking/main/crates/ov_cli/install.sh | bash

# Or build from source (requires Rust toolchain)
cargo install --git https://github.com/volcengine/OpenViking ov_cli
```

### Prerequisites

- Python 3.10+
- Go 1.22+ (for AGFS components)
- GCC 9+ or Clang 11+ (for core extensions)

---

## Configuration

Create `~/.openviking/ov.conf`:

```json
{
  "storage": {
    "workspace": "/home/user/openviking_workspace"
  },
  "log": {
    "level": "INFO",
    "output": "stdout"
  },
  "embedding": {
    "dense": {
      "api_base": "https://api.openai.com/v1",
      "api_key": "$OPENAI_API_KEY",
      "provider": "openai",
      "dimension": 1536,
      "model": "text-embedding-3-large"
    },
    "max_concurrent": 10
  },
  "vlm": {
    "api_base": "https://api.openai.com/v1",
    "api_key": "$OPENAI_API_KEY",
    "provider": "openai",
    "model": "gpt-4o",
    "max_concurrent": 100
  }
}
```

> **Note:** OpenViking reads `api_key` values as strings; use environment variable injection at startup rather than literal secrets.

### Provider Options

| Role | Provider Value | Example Model |
|------|---------------|---------------|
| VLM | `openai` | `gpt-4o` |
| VLM | `volcengine` | `doubao-seed-2-0-pro-260215` |
| VLM | `litellm` | `claude-3-5-sonnet-20240620`, `ollama/llama3.1` |
| Embedding | `openai` | `text-embedding-3-large` |
| Embedding | `volcengine` | `doubao-embedding-vision-250615` |
| Embedding | `jina` | `jina-embeddings-v3` |

### LiteLLM VLM Examples

```json
{
  "vlm": {
    "provider": "litellm",
    "model": "claude-3-5-sonnet-20240620",
    "api_key": "$ANTHROPIC_API_KEY"
  }
}
```

```json
{
  "vlm": {
    "provider": "litellm",
    "model": "ollama/llama3.1",
    "api_base": "http://localhost:11434"
  }
}
```

```json
{
  "vlm": {
    "provider": "litellm",
    "model": "deepseek-chat",
    "api_key": "$DEEPSEEK_API_KEY"
  }
}
```

---

## Core Concepts

### Filesystem Paradigm

OpenViking organizes agent context like a filesystem:

```
workspace/
├── memories/          # Long-term agent memories (L0 always loaded)
│   ├── user_prefs/
│   └── task_history/
├── resources/         # External knowledge, documents (L1 on demand)
│   ├── codebase/
│   └── docs/
└── skills/            # Reusable agent capabilities (L2 retrieved)
    ├── coding/
    └── analysis/
```

### Tiered Context Loading (L0/L1/L2)

- **L0**: Always loaded — core identity, persistent preferences
- **L1**: Loaded on demand — relevant resources fetched per task
- **L2**: Semantically retrieved — skills pulled by similarity search

This tiered approach minimizes token consumption while maximizing context relevance.

---

## Python API Usage

### Basic Setup

```python
import os
from openviking import OpenViking

# Initialize with config file
ov = OpenViking(config_path="~/.openviking/ov.conf")

# Or initialize programmatically
ov = OpenViking(
    workspace="/home/user/openviking_workspace",
    vlm_provider="openai",
    vlm_model="gpt-4o",
    vlm_api_key=os.environ["OPENAI_API_KEY"],
    embedding_provider="openai",
    embedding_model="text-embedding-3-large",
    embedding_api_key=os.environ["OPENAI_API_KEY"],
    embedding_dimension=1536,
)
```

### Managing a Context Namespace (Agent Brain)

```python
# Create or open a namespace (like a filesystem root for one agent)
brain = ov.namespace("my_agent")

# Add a memory file
brain.write("memories/user_prefs.md", """
# User Preferences
- Language: Python
- Code style: PEP8
- Preferred framework: FastAPI
""")

# Add a resource document
brain.write("resources/api_docs/stripe.md", open("stripe_docs.md").read())

# Add a skill
brain.write("skills/coding/write_tests.md", """
# Skill: Write Unit Tests
When asked to write tests, use pytest with fixtures.
Always mock external API calls. Aim for 80%+ coverage.
""")
```

### Querying Context

```python
# Semantic search across the namespace
results = brain.search("how does the user prefer code to be formatted?")
for result in results:
    print(result.path, result.score, result.content[:200])

# Directory-scoped retrieval (recursive)
skill_results = brain.search(
    query="write unit tests for a FastAPI endpoint",
    directory="skills/",
    top_k=3,
)

# Direct path read (L0 always available)
prefs = brain.read("memories/user_prefs.md")
print(prefs.content)
```

### Session Memory & Auto-Compression

```python
# Start a session — OpenViking tracks turns and auto-compresses
session = brain.session("task_build_api")

# Add conversation turns
session.add_turn(role="user", content="Build me a REST API for todo items")
session.add_turn(role="assistant", content="I'll create a FastAPI app with CRUD operations...")

# After many turns, trigger compression to extract long-term memory
summary = session.compress()
# Compressed insights are automatically written to memories/

# End session — persists extracted memories
session.close()
```

### Retrieval Trajectory (Observable RAG)

```python
# Enable trajectory tracking to observe retrieval decisions
with brain.observe() as tracker:
    results = brain.search("authentication best practices")
    
trajectory = tracker.trajectory()
for step in trajectory.steps:
    print(f"[{step.level}] {step.path} → score={step.score:.3f}")
    # Output:
    # [L0] memories/user_prefs.md → score=0.82
    # [L1] resources/security/auth.md → score=0.91
    # [L2] skills/coding/jwt_auth.md → score=0.88
```

---

## Common Patterns

### Pattern 1: Agent with Persistent Memory

```python
import os
from openviking import OpenViking

ov = OpenViking(config_path="~/.openviking/ov.conf")
brain = ov.namespace("coding_agent")

def agent_respond(user_message: str, conversation_history: list) -> str:
    # Retrieve relevant context
    context_results = brain.search(user_message, top_k=5)
    context_text = "\n\n".join(r.content for r in context_results)
    
    # Build prompt with retrieved context
    system_prompt = f"""You are a coding assistant.

## Relevant Context
{context_text}
"""
    # ... call your LLM here with system_prompt + conversation_history
    response = call_llm(system_prompt, conversation_history, user_message)
    
    # Store interaction for future memory
    brain.session("current").add_turn("user", user_message)
    brain.session("current").add_turn("assistant", response)
    
    return response
```

### Pattern 2: Hierarchical Skill Loading

```python
# Register skills from a directory structure
import pathlib

skills_dir = pathlib.Path("./agent_skills")
for skill_file in skills_dir.rglob("*.md"):
    relative = skill_file.relative_to(skills_dir)
    brain.write(f"skills/{relative}", skill_file.read_text())

# At runtime, retrieve only relevant skills
def get_relevant_skills(task: str) -> list[str]:
    results = brain.search(task, directory="skills/", top_k=3)
    return [r.content for r in results]

task = "Refactor this class to use dependency injection"
skills = get_relevant_skills(task)
# Returns only DI-related skills, not all registered skills
```

### Pattern 3: RAG over Codebase

```python
import subprocess
import pathlib

brain = ov.namespace("codebase_agent")

# Index a codebase
def index_codebase(repo_path: str):
    for f in pathlib.Path(repo_path).rglob("*.py"):
        content = f.read_text(errors="ignore")
        # Store with relative path as key
        rel = f.relative_to(repo_path)
        brain.write(f"resources/codebase/{rel}", content)

index_codebase("/home/user/myproject")

# Query with directory scoping
def find_relevant_code(query: str) -> list:
    return brain.search(
        query=query,
        directory="resources/codebase/",
        top_k=5,
    )

hits = find_relevant_code("database connection pooling")
for h in hits:
    print(h.path, "\n", h.content[:300])
```

### Pattern 4: Multi-Agent Shared Context

```python
# Agent 1 writes discoveries
agent1_brain = ov.namespace("researcher_agent")
agent1_brain.write("memories/findings/api_rate_limits.md", """
# API Rate Limits Discovered
- Stripe: 100 req/s in live mode
- SendGrid: 600 req/min
""")

# Agent 2 reads shared workspace findings
agent2_brain = ov.namespace("coder_agent")
# Cross-namespace read (if permitted)
shared = ov.namespace("shared_knowledge")
rate_limits = shared.read("memories/findings/api_rate_limits.md")
```

---

## CLI Commands (ov_cli)

```bash
# Check version
ov --version

# List namespaces
ov namespace list

# Create a namespace
ov namespace create my_agent

# Write context file
ov write my_agent/memories/prefs.md --file ./prefs.md

# Read a file
ov read my_agent/memories/prefs.md

# Search context
ov search my_agent "how to handle authentication" --top-k 5

# Show retrieval trajectory for a query
ov search my_agent "database migrations" --trace

# Compress a session
ov session compress my_agent/task_build_api

# List files in namespace
ov ls my_agent/skills/

# Delete a context file
ov rm my_agent/resources/outdated_docs.md

# Export namespace to local directory
ov export my_agent ./exported_brain/

# Import from local directory
ov import ./exported_brain/ my_agent_restored
```

---

## Troubleshooting

### Config Not Found

```bash
# Verify config location
ls -la ~/.openviking/ov.conf

# OpenViking also checks OV_CONFIG env var
export OV_CONFIG=/path/to/custom/ov.conf
```

### Embedding Dimension Mismatch

If you switch embedding models, the stored vector dimensions will conflict:

```python
# Check current dimension setting vs stored index
# Solution: re-index after model change
brain.reindex(force=True)
```

### Workspace Permission Errors

```bash
# Ensure workspace directory is writable
chmod -R 755 /home/user/openviking_workspace

# Check disk space (embedding indexes can be large)
df -h /home/user/openviking_workspace
```

### LiteLLM Provider Not Detected

```python
# Use explicit prefix for ambiguous models
{
  "vlm": {
    "provider": "litellm",
    "model": "openrouter/anthropic/claude-3-5-sonnet",  # full prefix required
    "api_key": "$OPENROUTER_API_KEY",
    "api_base": "https://openrouter.ai/api/v1"
  }
}
```

### High Token Usage

Enable tiered loading to reduce L1/L2 fetches:

```python
# Scope searches tightly to avoid over-fetching
results = brain.search(
    query=user_message,
    directory="skills/relevant_domain/",  # narrow scope
    top_k=2,                               # fewer results
    min_score=0.75,                        # quality threshold
)
```

### Slow Indexing on Large Codebases

```python
# Increase concurrency in config
{
  "embedding": {
    "max_concurrent": 20  # increase from default 10
  },
  "vlm": {
    "max_concurrent": 50
  }
}

# Or batch-write with async
import asyncio

async def index_async(files):
    tasks = [brain.awrite(f"resources/{p}", c) for p, c in files]
    await asyncio.gather(*tasks)
```

---

## Environment Variables Reference

| Variable | Purpose |
|----------|---------|
| `OV_CONFIG` | Path to `ov.conf` override |
| `OPENAI_API_KEY` | OpenAI API key for VLM/embedding |
| `ANTHROPIC_API_KEY` | Anthropic Claude via LiteLLM |
| `DEEPSEEK_API_KEY` | DeepSeek via LiteLLM |
| `GEMINI_API_KEY` | Google Gemini via LiteLLM |
| `OV_LOG_LEVEL` | Override log level (`DEBUG`, `INFO`, `WARN`) |
| `OV_WORKSPACE` | Override workspace path |

---

## Resources

- **Website**: https://openviking.ai
- **Docs**: https://www.openviking.ai/docs
- **GitHub**: https://github.com/volcengine/OpenViking
- **Issues**: https://github.com/volcengine/OpenViking/issues
- **Discord**: https://discord.com/invite/eHvx8E9XF3
- **LiteLLM Providers**: https://docs.litellm.ai/docs/providers
