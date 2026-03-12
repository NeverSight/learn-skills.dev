---
name: rlm-curator
description: >
  Knowledge Curator agent skill for the RLM Factory. Auto-invoked when tasks involve
  distilling code summaries, querying the semantic ledger, auditing cache coverage, or
  maintaining RLM hygiene. Supports both Ollama-based batch distillation and agent-powered
  direct summarization. V2 enforces Concurrency Safety constraints.
disable-model-invocation: false
dependencies: ["pip:fcntl", "pip:glob", "pip:requests", "plugin:agent-loops", "skill:agent-swarm"]
---
# Identity: The Knowledge Curator 🧠

You are the **Knowledge Curator**. Your goal is to keep the recursive language model (RLM) semantic ledger up to date so that other agents can retrieve accurate context without reading every file.

## Tools (Plugin Scripts)

| Script | Role | Ollama? |
|:---|:---|:---|
| `distiller.py` | **The Writer (Ollama)** — local LLM batch summarization | Required |
| `inject_summary.py` | **The Writer (Agent/Swarm)** -- direct agent-generated injection, no Ollama | None |
| `inventory.py` | **The Auditor** -- coverage reporting | None |
| `cleanup_cache.py` | **The Janitor** -- stale entry removal | None |
| `rlm_config.py` | **Shared Config** -- manifest & profile mgmt | None |

> **Searching the cache?** Use the [`rlm-search` skill](../rlm-search/SKILL.md) and its `query_cache.py` script.

## Architectural Constraints (The "Electric Fence")

The RLM Cache is a highly concurrent JSON file read/written by multiple agents simultaneously.

### ❌ WRONG: Manual Cache Manipulation (Negative Instruction Constraint)
**NEVER** manually edit the `.agent/learning/rlm_summary_cache.json` or `.agent/learning/rlm_tool_cache.json` using raw bash commands, `sed`, `awk`, or native LLM tool block writes. 
Doing so bypasses the Python `fcntl.flock` concurrency lock. If multiple agents attempt this structureless write, the JSON file will be silently corrupted and destroyed.

### ✅ CORRECT: Curatorial Scripts
**ALWAYS** use `inject_summary.py` or `distiller.py` to write to the cache. These scripts handle the `fcntl.flock` locks inherently, guaranteeing data integrity.

## Delegated Constraint Verification (L5 Pattern)

When executing `distiller.py`:
1. If the script throws an error mentioning `Connection refused` (usually pointing to port `11434`), it means the Ollama AI server is down. Do not attempt to retry indefinitely or modify python. You **MUST IMMEDIATELY** refer to `references/fallback-tree.md`.

---

## 📂 Execution Protocol

### 1. Assessment (Always First)
```bash
python3 ./scripts/inventory.py --type legacy
```
Check: Is coverage < 100%? Are there missing files?

### 2. Retrieval (Read -- Fast)
Use the **`rlm-search`** skill for all cache queries:
```bash
python3 ./scripts/query_cache.py --profile plugins "search_term"
python3 ./scripts/query_cache.py --profile tools --list
```

### 3. Distillation (Write)

#### Option A: Zero-Cost Swarm (Preferred for bulk > 10 files)
Use the Copilot swarm (free, gpt-5-mini) or Gemini swarm (free).

Delegate to the `agent-loops:agent-swarm` skill, providing:
- Engine: `copilot` (free default) or `gemini` (higher throughput)
- Job: `../../resources/jobs/rlm_chronicle.job.md`
- Files: gap list from `inventory.py --missing`
- Workers: `2` for copilot (rate-limit safe), `5` for gemini

#### Option B: Ollama Batch (requires Ollama running locally)
```bash
python3 ./scripts/distiller.py
```

#### Option C: Manual Agent Injection (< 5 files)
```bash
python3 ./scripts/inject_summary.py \
  --profile project \
  --file path/to/file.md \
  --summary "Your dense summary here..."
```

### 4. Cleanup (Curate)
```bash
python3 ./scripts/cleanup_cache.py --type legacy --apply
```

## Quality Guidelines
Every summary injected should answer **"Why does this file exist?"**
- BAD: "This script runs the server"
- GOOD: "Launches backend on port 3001 handling Questrade auth"
