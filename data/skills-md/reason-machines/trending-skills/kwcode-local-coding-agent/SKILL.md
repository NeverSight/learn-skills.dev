---
name: kwcode-local-coding-agent
description: KWCode (天工开物) — a CLI coding agent optimized for local open-source models (8B-30B), featuring deterministic expert pipelines, BM25+AST code location, runtime debugging, and a self-improving flywheel — all running fully offline.
triggers:
  - set up kwcode for my local model
  - use kwcode to fix a bug in my project
  - run kwcode with deepseek or qwen
  - configure kwcode api endpoint
  - use kwcode multi-task mode
  - install kwcode search enhancement
  - understand kwcode expert pipeline
  - troubleshoot kwcode not finding files
---

# KWCode Local Coding Agent

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

KWCode is a CLI coding agent designed specifically for local open-source models (8B–30B parameters). Unlike cloud-first agents (Claude Code, Cursor), KWCode uses a **deterministic expert pipeline** where the LLM only classifies and generates — all routing, validation, and decision-making is handled by deterministic code. This lets small models succeed where they would otherwise hallucinate or loop.

---

## Installation

```bash
# Standard install
pip install kwcode

# China mirror (faster in mainland)
pip install kwcode -i https://pypi.tuna.tsinghua.edu.cn/simple

# Optional: Cross-Encoder search reranking
pip install "kwcode[rerank]"
```

**Requirements:** Python 3.10+, any OpenAI-compatible API (local or cloud).

---

## Quick Start

```bash
# Launch interactive REPL
kwcode
```

On first launch, KWCode runs a setup wizard to configure your model connection.

---

## Configuration

### Connect to a local inference engine (Ollama example)

```bash
# Inside kwcode REPL or as a slash command:
/api default http://localhost:11434/v1 ollama qwen3:8b
```

### Connect to a cloud API (no local GPU needed)

```bash
/api default https://api.deepseek.com $DEEPSEEK_API_KEY deepseek-coder
/api default https://api.siliconflow.cn/v1 $SILICONFLOW_API_KEY Qwen/Qwen3-8B
```

### Environment variable approach

```bash
export KWCODE_API_BASE=http://localhost:11434/v1
export KWCODE_API_KEY=ollama
export KWCODE_MODEL=qwen3:8b
kwcode
```

### Recommended models by VRAM

| VRAM | Model |
|------|-------|
| 4 GB | `gemma3:4b` |
| 8 GB | `qwen3:8b` |
| 16 GB | `qwen3:14b` |
| 24 GB+ | `qwen3:30b-a3b` |

---

## Key Commands

All commands are entered inside the `kwcode` REPL (`>`  prompt).

### Core task commands

```
> <natural language task description>
```
```
> 修复登录验证失败的问题
> write a FastAPI login endpoint with JWT auth
> refactor calculate_price into smaller functions
```

### Planning & safety

```
> /plan <task description>
```
Shows execution steps and risk level (High / Medium / Low) before touching any file. Requires confirmation.

```
> /checkpoint
```
Manually snapshot current project state. KWCode also auto-snapshots before each task.

```
> /rollback
```
Restore to the last checkpoint if a task goes wrong.

### Multi-task orchestration (DAG)

```
> /multi task1 ; task2 ; task3          # all parallel
> /multi task1 -> task2 -> task3        # serial chain
> /multi                                # interactive builder
```

Interactive multi-task example:

```
> /multi
  + add docstring to function `add`       (parallel)
  + add docstring to function `sub`       (parallel)
  + >write tests for the modified code    (serial, depends on above two)
```

### Search enhancement

```bash
# Install SearXNG (requires Docker Desktop running)
kwcode setup-search
```

```
> /search <query>       # explicit search inside REPL
```

Without Docker, KWCode falls back to DuckDuckGo automatically.

### Statistics & flywheel

```bash
kwcode stats            # CLI command (outside REPL)
```

Shows tasks completed, estimated time saved, and flywheel expert promotions.

### API management

```
> /api list                              # show configured endpoints
> /api default <base_url> <key> [model] # set default endpoint
> /api add <name> <base_url> <key>      # add named endpoint
> /api use <name>                        # switch active endpoint
```

---

## Project Configuration Files

KWCode looks for these files in your project root and injects them as context:

| File | Purpose |
|------|---------|
| `KWCODE.md` | Project-level rules, conventions, coding standards. Injected per task type. |
| `PROJECT.md` | Auto-maintained project summary (Layer 1 memory). |
| `EXPERT.md` | Domain expert knowledge accumulated by the flywheel (Layer 2). |
| `PATTERN.md` | Recurring code patterns learned from your project (Layer 3). |
| `REFLECTION.md` | Structured log of past failures and lessons (auto-updated). |

### Example `KWCODE.md`

```markdown
# Project Rules

## bugfix
- Always run `pytest tests/` after any fix
- Never modify migration files directly

## codegen
- Use `async def` for all new route handlers
- Import order: stdlib → third-party → local

## general
- Line length: 88 (black default)
- All new functions must have type hints
```

---

## How the Expert Pipeline Works

Every user input flows through five deterministic stages:

```
Input
  └─► Gate       — classifies task, routes to skill, matches domain knowledge
        └─► Locator    — BM25 keyword recall + AST call-graph expansion (no LLM)
              └─► Generator  — generates only the changed diff, injects SKILL.md
                    └─► Verifier   — syntax check + pytest (deterministic)
                          └─► Debugger   — sys.settrace captures live variable values
                                └─► Reviewer   — LLM checks intent vs actual change
```

**The LLM is only called at Generator and Reviewer stages.** Everything else is deterministic Python.

---

## Code Examples

### Trigger a bugfix task

```python
# KWCode detects "bug", "fix", "error", "失败" → routes to BugFix expert
# Inside REPL:
# > fix the KeyError in user_service.py when email is missing
```

KWCode will:
1. BM25-locate `user_service.py` + trace call graph for hidden dependencies
2. Generate a minimal patch (only changed lines)
3. Run `pytest` automatically
4. If failing: inject runtime variable values via `sys.settrace` and retry

### Trigger a test generation task

```
> generate pytest tests for the PaymentProcessor class
```

KWCode injects the `TestGen` SKILL.md, locates `PaymentProcessor` via AST, generates tests, and verifies they pass.

### Use the Python API (programmatic access)

```python
from kwcode import KWCodeAgent

agent = KWCodeAgent(
    api_base="http://localhost:11434/v1",
    api_key="ollama",
    model="qwen3:8b",
    project_dir="/path/to/your/project",
)

result = agent.run("fix the login validation bug")
print(result.status)        # "success" | "failed" | "rolled_back"
print(result.files_changed) # list of modified file paths
print(result.patch)         # unified diff string
```

### Multi-task via Python API

```python
from kwcode import KWCodeAgent, TaskGraph

agent = KWCodeAgent(model="qwen3:14b", project_dir=".")

graph = TaskGraph()
t1 = graph.add("add type hints to utils.py")
t2 = graph.add("add type hints to models.py")
t3 = graph.add("write tests for typed functions", depends_on=[t1, t2])

results = agent.run_graph(graph)
for task_id, result in results.items():
    print(f"{task_id}: {result.status}")
```

---

## Three-Stage Retry Logic

When `Verifier` fails, KWCode does **not** repeat the same attempt:

| Attempt | Strategy |
|---------|----------|
| 1st | Normal task description sent to Generator |
| 2nd | Error message + `sys.settrace` runtime variable dump injected; LLM reflects on why attempt 1 failed |
| 3rd | Minimal-change constraint enforced; Debug Subagent provides full `pytest --tb=long` trace |

After 3 failures, task is marked failed and rolled back to checkpoint.

---

## Troubleshooting

### Model returns garbled output or loops

```
/api default <your_base_url> <key> <model>   # re-confirm model name matches server
```

Check that your local inference engine is running:
```bash
curl http://localhost:11434/v1/models        # Ollama
curl http://localhost:8080/v1/models         # llama.cpp / LM Studio
```

### KWCode can't find the right file

BM25 needs indexed content. If your project is new:
```
> /index                    # force re-index project files
```

If the file uses an unusual extension, add it to `KWCODE.md`:
```markdown
## index
- include: ["*.pyx", "*.pxd", "*.proto"]
```

### pytest not found / tests not running

```
> /config verifier.test_cmd "python -m pytest tests/ -x"
```

Or set in `KWCODE.md`:
```markdown
## verifier
- test_cmd: python -m pytest tests/ -x --tb=short
```

### Search not working (DuckDuckGo blocked)

```bash
# Install local SearXNG (requires Docker)
kwcode setup-search

# Verify it's running
curl http://localhost:8080/search?q=test&format=json
```

### Context window overflow with large projects

KWCode auto-compresses context when it approaches the limit, but you can tune aggressiveness:

```
> /config context.compression_ratio 0.6    # keep 60% of mid-conversation history
> /config locator.max_files 3              # limit files sent to Generator
```

### Flywheel expert not promoting

Promotion requires: ≥5 successes of the same task type → backtest pass rate ≥ baseline → 10-run A/B test with >10% improvement. Check flywheel status:

```
kwcode stats --flywheel
```

---

## Skill Domains (SKILL.md Library)

KWCode ships with 15 built-in domain skills injected at Generator stage:

| Skill | Triggers |
|-------|---------|
| `BugFix` | fix, bug, error, crash, 修复 |
| `FastAPI` | fastapi, route, endpoint, async |
| `TestGen` | test, pytest, unittest, 测试 |
| `API` | api, rest, http, request |
| `DeepSeekAPI` | deepseek, r1, v3 |
| `Docstring` | docstring, document, 注释 |
| `MyBatis` | mybatis, mapper, xml, sql |
| `Office` | excel, word, ppt, spreadsheet |
| `Refactor` | refactor, clean, extract, 重构 |
| `SpringBoot` | spring, springboot, java |
| `SQLOpt` | sql, query, optimize, index |
| `TypeHint` | type hint, annotation, mypy |
| `UniApp` | uniapp, vue, miniprogram |

Custom skills can be added by placing a `SKILL_<name>.md` file in your project root or `~/.kwcode/skills/`.

---

## Data & Privacy

- **All processing is local.** No code, file contents, or task descriptions leave your machine.
- Model inference: your local engine or your chosen cloud API endpoint only.
- Search: SearXNG self-hosted (recommended) or DuckDuckGo (queries only, no code).
- Statistics: stored in `~/.kwcode/stats.db` (SQLite, local only).
- Reflection/memory files: written to your project directory, fully under your control.
