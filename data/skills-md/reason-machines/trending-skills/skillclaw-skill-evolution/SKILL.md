---
name: skillclaw-skill-evolution
description: Framework for collective skill evolution in multi-user LLM agent ecosystems — automatically distills session experience into reusable SKILL.md files and shares them across agent clusters.
triggers:
  - set up SkillClaw skill evolution
  - evolve agent skills from session data
  - share skills across agents with SkillClaw
  - start skillclaw proxy server
  - configure skillclaw with OSS storage
  - run wildclawbench skill evolution experiment
  - pull push sync agent skills
  - start evolve server for skill distillation
---

# SkillClaw: Collective Skill Evolution for LLM Agents

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

SkillClaw is a framework that makes LLM agents progressively smarter by **evolving reusable skills** from real session data and sharing them across a group of agents. It intercepts OpenAI-compatible API calls via a local proxy, records session artifacts, and runs an evolve server that distills experience into `SKILL.md` files synced via cloud storage (OSS/S3/local).

## Architecture

```
User → OpenClaw Agent → SkillClaw Client Proxy → Upstream LLM API
                              ↓ records sessions
                        Shared Storage (OSS/S3/local)
                              ↑ reads sessions, writes skills
                        Evolve Server (workflow or agent)
```

Three components share the same storage layer and skill format:

1. **Client Proxy** — Local API proxy intercepting `/v1/chat/completions` and `/v1/messages`, syncing skills
2. **Workflow Evolve Server** (`evolve_server`) — Fixed 3-stage pipeline: Summarize → Aggregate → Execute
3. **Agent Evolve Server** (`agent_evolve_server`) — Autonomous OpenClaw agent that reads sessions and writes evolved skills

## Installation

### Client / Local Development

```bash
git clone <repo-url> SkillClaw && cd SkillClaw
bash scripts/install_skillclaw.sh
source .venv/bin/activate
```

### Server Deployment

```bash
bash scripts/install_skillclaw_server.sh
source .venv-server/bin/activate

# Required only for the agent evolve server
npm install -g openclaw
```

## Environment Configuration

Copy and populate credentials — never hardcode secrets:

```bash
# From example_env.sh
export OPENAI_BASE_URL="https://your-api-gateway/v1"
export OPENAI_API_KEY="$OPENAI_API_KEY"

# For OSS storage backend
export EVOLVE_STORAGE_ENDPOINT="$OSS_ENDPOINT"
export EVOLVE_STORAGE_BUCKET="$OSS_BUCKET"
export OSS_ACCESS_KEY_ID="$OSS_ACCESS_KEY_ID"
export OSS_ACCESS_KEY_SECRET="$OSS_ACCESS_KEY_SECRET"
```

Config file lives at `~/.skillclaw/config.yaml`. Inspect and modify:

```bash
skillclaw config show
skillclaw config <key> <value>
```

## CLI Reference

### Client Proxy Setup

```bash
skillclaw setup          # Initialize config and directories
skillclaw start          # Start the local proxy server
skillclaw stop           # Stop the proxy server
skillclaw status         # Show proxy status and config summary
skillclaw config show    # Dump full resolved config
```

### Skill Management

```bash
skillclaw skills pull          # Download shared skills from cloud storage
skillclaw skills push          # Upload local skills to cloud storage
skillclaw skills sync          # Bidirectional sync (pull + push)
skillclaw skills list-remote   # Browse skills available in shared storage
```

### Benchmarking

```bash
skillclaw benchmark --help     # List all benchmark subcommands
```

## Starting the Evolve Servers

### Workflow Evolve Server (Summarize → Aggregate → Execute)

```bash
skillclaw-evolve-server \
  --port 8787 \
  --interval 300 \
  --storage-backend oss \
  --oss-endpoint "$EVOLVE_STORAGE_ENDPOINT" \
  --oss-bucket "$EVOLVE_STORAGE_BUCKET" \
  --group-id my-group
```

### Agent Evolve Server (Autonomous OpenClaw agent)

```bash
skillclaw-agent-evolve-server \
  --port 8787 \
  --interval 300 \
  --no-fresh \
  --storage-backend oss \
  --oss-endpoint "$EVOLVE_STORAGE_ENDPOINT" \
  --oss-bucket "$EVOLVE_STORAGE_BUCKET" \
  --group-id my-group
```

Use `--no-fresh` to continue from existing evolved skills rather than starting from scratch each run.

### Local Filesystem Backend (for development)

```bash
skillclaw-evolve-server \
  --port 8787 \
  --interval 60 \
  --storage-backend local \
  --local-storage-path ./skill_storage \
  --group-id dev-group
```

## Key Configuration Options

| Option | Description | Default |
|---|---|---|
| `--port` | Server port | `8787` |
| `--interval` | Seconds between evolution cycles | `300` |
| `--storage-backend` | `oss`, `s3`, or `local` | `local` |
| `--group-id` | Identifier for your agent cluster | required |
| `--no-fresh` | Resume from existing skills | flag |
| `--oss-endpoint` | OSS endpoint URL | env var |
| `--oss-bucket` | OSS bucket name | env var |

## Skill Format (SKILL.md)

Skills are Markdown files with YAML frontmatter. The evolve server reads session data and writes or updates these files:

```markdown
---
name: my-skill-name
description: What this skill does
version: 1.0.0
tags: [web, scraping]
---

# Skill Name

## When to Use
...

## Instructions
Step-by-step instructions the agent follows.

## Examples
\`\`\`python
# working code example
\`\`\`
```

## WildClawBench Experiment

Run the main iterative evolution experiment:

```bash
python scripts/run_wildclawbench_iterative_evolve_agent.py \
  --group-id wildclawbench-test \
  --storage-backend local \
  --local-storage-path ./wb_storage \
  --num-iterations 3
```

This evaluates skill evolution on real-world agent tasks from [WildClawBench](https://github.com/InternLM/WildClawBench).

## Python API Usage

### Programmatic Skill Sync

```python
from skillclaw.skill_manager import SkillManager
from skillclaw.skill_hub import SkillHub

# Initialize with local backend
manager = SkillManager(storage_backend="local", local_path="./skills")

# Pull skills from shared storage
manager.pull()

# List available skills
skills = manager.list_local()
for skill in skills:
    print(f"{skill.name}: {skill.description}")

# Push a new skill
manager.push("path/to/SKILL.md")
```

### Launching the Proxy Programmatically

```python
from skillclaw.launcher import SkillClawLauncher
from skillclaw.config import SkillClawConfig

config = SkillClawConfig(
    upstream_base_url="https://api.openai.com/v1",
    upstream_api_key="$OPENAI_API_KEY",   # loaded from env at runtime
    proxy_port=8080,
    storage_backend="local",
    local_storage_path="./skillclaw_data",
    group_id="my-agents",
)

launcher = SkillClawLauncher(config)
launcher.start()
# Agents now point to http://localhost:8080/v1
```

### Using the Evolve Server API

```python
import httpx

# Trigger an immediate evolution cycle
response = httpx.post("http://localhost:8787/evolve")
print(response.json())  # {"status": "ok", "skills_evolved": 3}

# Check server status
status = httpx.get("http://localhost:8787/status")
print(status.json())
```

### Evolve Server Config (`.env.example`)

```bash
# evolve_server/.env.example
OPENAI_BASE_URL="https://your-api-gateway/v1"
OPENAI_API_KEY="$OPENAI_API_KEY"

STORAGE_BACKEND=oss
OSS_ENDPOINT="$EVOLVE_STORAGE_ENDPOINT"
OSS_BUCKET="$EVOLVE_STORAGE_BUCKET"
OSS_ACCESS_KEY_ID="$OSS_ACCESS_KEY_ID"
OSS_ACCESS_KEY_SECRET="$OSS_ACCESS_KEY_SECRET"

GROUP_ID=production-cluster
EVOLVE_INTERVAL=300
```

## Supported Frameworks

SkillClaw natively integrates with these OpenClaw-compatible frameworks:

- **CoPaw** — collaborative agent framework
- **IronClaw** — robust task execution
- **PicoClaw** — lightweight agents
- **ZeroClaw** — zero-shot agents
- **NanoClaw** — minimal footprint
- **NemoClaw** — NVIDIA NeMo-based agents

Point any framework's OpenAI-compatible API calls at the SkillClaw proxy to start recording sessions.

## Deployment Pattern: Multi-User Cluster

```
User A → Agent (port 8080) ─┐
User B → Agent (port 8081) ─┼──→ Shared OSS Bucket ←── Evolve Server
User C → Agent (port 8082) ─┘         ↑
                                  Skills sync'd
                                  back to all agents
```

```bash
# Each user's machine runs:
skillclaw start --group-id production-cluster --port 8080

# One central server runs:
skillclaw-evolve-server \
  --storage-backend oss \
  --oss-bucket "$SHARED_BUCKET" \
  --group-id production-cluster \
  --interval 300
```

## Troubleshooting

**Proxy won't start:**
```bash
skillclaw status        # Check if already running
skillclaw stop && skillclaw start   # Restart
skillclaw config show   # Verify OPENAI_BASE_URL is set
```

**Skills not syncing:**
```bash
skillclaw skills list-remote   # Verify storage connection
skillclaw config show          # Check storage backend config
# Confirm env vars are exported: echo $OSS_ACCESS_KEY_ID
```

**Evolve server not processing sessions:**
```bash
# Check server logs for cycle output
# Verify --group-id matches the client proxy group-id
# Try --storage-backend local for debugging
skillclaw-evolve-server --storage-backend local --local-storage-path ./debug_storage --group-id debug
```

**Agent evolve server fails to start:**
```bash
which openclaw          # Must be in PATH
npm install -g openclaw # Install if missing
# Verify OPENAI_BASE_URL and OPENAI_API_KEY are set for the agent's LLM
```

**Port already in use:**
```bash
skillclaw stop
lsof -i :8787 | grep LISTEN   # Find conflicting process
skillclaw-evolve-server --port 8788 ...
```

## Project Structure Reference

```
SkillClaw/
├── skillclaw/               # Client proxy, CLI, config
│   ├── cli.py               # All `skillclaw` CLI commands
│   ├── api_server.py        # Proxy server implementation
│   ├── launcher.py          # Process management
│   ├── skill_manager.py     # Local skill CRUD
│   ├── skill_hub.py         # Cloud sync logic
│   └── experiments/         # Benchmark runners
├── evolve_server/           # Workflow evolve server
│   ├── summarizer.py        # Stage 1: session → summary
│   ├── aggregation.py       # Stage 2: summaries → patterns
│   ├── execution.py         # Stage 3: patterns → SKILL.md
│   └── skill_registry.py    # Skill dedup and versioning
├── agent_evolve_server/     # OpenClaw-based evolve server
│   ├── workspace.py         # Session/skill file workspace
│   ├── openclaw_runner.py   # Agent execution harness
│   └── EVOLVE_AGENTS.md     # Agent prompt and tool config
└── scripts/
    ├── install_skillclaw.sh
    ├── install_skillclaw_server.sh
    └── run_wildclawbench_iterative_evolve_agent.py
```
