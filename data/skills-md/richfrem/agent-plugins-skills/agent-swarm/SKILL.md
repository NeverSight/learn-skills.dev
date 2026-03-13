---
name: agent-swarm
aliases: ["Parallel Agent"]
description: "(Industry standard: Parallel Agent) Primary Use Case: Work that can be partitioned into independent sub-tasks running concurrently across multiple agents. Parallel multi-agent execution pattern. Use when: work can be partitioned into independent tasks that N agents can execute simultaneously across worktrees. Includes routing (sequential vs parallel), merge verification, and correction loops."
allowed-tools: Bash, Read, Write
dependencies: ["pip:shlex", "pip:yaml", "plugin:context-bundler"]
---
# Agent Swarm

Parallel or pipelined execution across multiple agents and worktrees. The orchestrator partitions work, dispatches to agents, and verifies/merges the results.

## When to Use

- Large features that can be split into independent work packages
- Bulk operations (tests, docs, migrations, RLM distillation) that benefit from parallelism
- Multi-concern work where specialists handle different aspects simultaneously

## Process Flow

1. **Plan & Partition** -- Break work into independent tasks. Define boundaries clearly.
2. **Route** -- Decide execution mode:
   - **Sequential Pipeline** -- Tasks depend on each other (A -> B -> C)
   - **Parallel Swarm** -- Tasks are independent (A | B | C)
3. **Dispatch** -- Create a worktree per task. Assign each to an agent:
   - CLI agent (Claude, Gemini, Copilot)
   - Deterministic script
   - Human
4. **Execute** -- Each agent works in isolation. No cross-worktree communication.
5. **Verify & Merge** -- Orchestrator checks each worktree's output against acceptance criteria.
   - **Pass** -> Merge into main branch
   - **Fail** -> Generate correction packet, re-dispatch
6. **Seal** -- Bundle all merged artifacts
7. **Retrospective** -- Did the partition strategy work? Was parallelism effective?

## Worker Selection

Each worktree can be assigned to a different worker type based on task complexity:

| Worker | Cost | Best For |
|--------|------|----------|
| **High-reasoning CLI** (Opus, Ultra, GPT-5.3) | High | Complex logic, architecture |
| **Fast CLI** (Haiku, Flash 2.0) | Low | Tests, docs, routine tasks |
| **Free Tier: Copilot gpt-5-mini** | **$0** | Bulk summarization, zero-cost batch jobs |
| **Free Tier: Gemini gemini-3-pro-preview** | **$0** | Large context batch jobs |
| **Deterministic Script** | None | Formatting, linting, data transforms |
| **Human** | N/A | Judgment calls, creative decisions |

> **Zero-Cost Batch Strategy**: For bulk summarization or distillation jobs, use `--engine copilot` (gpt-5-mini) or `--engine gemini` (gemini-3-pro-preview). Both are free-tier models available via their respective CLIs. Gemini Flash 2.0 is also very cheap if more capacity is needed. Use `--workers 2` for Copilot (rate-limit safe) and `--workers 5` for Gemini.

## Implementation: swarm_run.py

The **swarm_run.py** script is the universal engine for executing this pattern. It is driven by **Job Files** (.md with YAML frontmatter).

### Key Features

- **Resume Support** -- Automatically saves state to `.swarm_state_<job>.json`. Use `--resume` to skip already processed items.
- **Intelligent Retry** -- Exponential backoff for rate limits.
- **Verification Skip** -- Use `check_cmd` in the job file to short-circuit work if a file is already processed (e.g. exists in cache).
- **Dry Run** -- Test your file discovery and template substitution without cost.
- **Engine Flag** -- `--engine [claude|gemini|copilot]` switches CLI backends at runtime.

### Usage

```bash
# Zero-cost Copilot batch (2 workers recommended to avoid rate limits)
source ~/.zshrc   # NOTE: use source ~/.zshrc, NOT 'export COPILOT_GITHUB_TOKEN=$(gh auth token)'
                  # gh auth token generates a PAT without Copilot scope -> auth failures
python3 ./scripts/swarm_run.py \
    --engine copilot \
    --job ../../resources/jobs/my_job.job.md \
    --files-from checklist.md \
    --resume --workers 2

# Gemini (free, higher parallelism)
python3 ./scripts/swarm_run.py \
    --engine gemini \
    --job ../../resources/jobs/my_job.job.md \
    --files-from checklist.md \
    --resume --workers 5

# Claude (paid, highest quality)
python3 ./scripts/swarm_run.py \
    --job ../../resources/jobs/my_job.job.md \
    [--dir some/dir] [--resume] [--dry-run]
```

### Job File Schema

```yaml
---
model: haiku        # haiku -> auto-upgraded to gpt-5-mini (copilot) or gemini-3-pro-preview (gemini)
workers: 2          # keep to 2 for Copilot, up to 5-10 for Gemini/Claude
timeout: 120        # seconds per worker
ext: [".md"]        # filters for --dir
# Shell template. {file} is shell-quoted automatically (handles apostrophes safely)
post_cmd: "python3 ./scripts/my_post_cmd.py --file {file} --summary {output}"
# Optional command to check if work is already done (exit 0 => skip)
check_cmd: "python3 ./scripts/check_cache.py --file {file}"
vars:
  profile: project
---
Prompt for the agent goes here.

IMPORTANT for Copilot engine: The copilot CLI ignores stdin when -p is used.
Instead, the instruction is prepended to the file content automatically by swarm_run.py.
Do NOT use tool calls or filesystem access - rely only on the content provided via stdin.
```

## Known Engine Quirks

### Copilot CLI
- **No `-p` flag** -- Copilot ignores stdin when `-p` is present. `swarm_run.py` automatically prepends the prompt to the file content instead.
- **Auth token scope** -- Use `source ~/.zshrc` to load your token. `gh auth token` returns a PAT without Copilot permissions, causing auth failures under concurrency.
- **Rate limits** -- Use `--workers 2` maximum. Higher concurrency trips GitHub's anti-abuse systems and surfaces as authentication errors.
- **Concurrent writes** -- If using a shared JSON post-cmd output (e.g. cache), ensure the writer script uses `fcntl.flock` for atomic writes. See `inject_summary.py`.

### Gemini CLI
- Accepts `-p "prompt"` flag normally
- Supports higher concurrency (5-10 workers)
- Model auto-upgrade: `haiku` -> `gemini-3-pro-preview`

### Checkpoint Reconciliation
If a batch run is interrupted partway through and the output store (e.g. cache JSON) is partially corrupted, reconcile the checkpoint before resuming:

```python
# Remove phantom "done" entries that aren't actually in the output store
completed = [f for f in st['completed'] if f in actual_output_keys]
st['failed'] = {}
```
Then rerun with `--resume`.

## Constraints

- Each worker execution must be independent
- Post-commands must be idempotent if using resume
- Orchestrator owns the overall job state
- `{file}` in post_cmd is shell-quoted automatically -- filenames with apostrophes are safe
- **Asynchronous Benchmark Metric Capture**: Orchestrators MUST capture and log `total_tokens` and `duration_ms` from worker agents to a centralized `timing.json` log immediately as subtasks complete, rather than waiting for the entire swarm batch to finish.

## Diagram

See: [plugins/agent-loops/resources/diagrams/agent_swarm.mmd](plugins/agent-loops/resources/diagrams/agent_swarm.mmd)
