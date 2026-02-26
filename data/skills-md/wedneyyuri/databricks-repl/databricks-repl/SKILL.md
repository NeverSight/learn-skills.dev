---
name: databricks-repl
description: Execute Python code on a Databricks cluster via a stateful REPL session. Use this skill when the user wants to run Python on Databricks, perform data analysis with Spark, train models on a cluster, query Unity Catalog tables, use sub_llm() for recursive LM calls, or any task requiring a persistent Databricks execution context. Always use a dedicated --project-dir (e.g., examples/my-task/) to isolate session.json and repl_outputs per task. Covers session lifecycle (create, exec, await, cancel, destroy), output file management, and eviction recovery.
argument-hint: '[profile] [cluster-name]'
---

# Databricks RLM REPL

Execute Python on a Databricks cluster through a stateful REPL that follows the Recursive Language Model (RLM) pattern. The root LM (Claude Code) never sees auth tokens, connection boilerplate, raw polling, or large dataframes — it interacts with Databricks through a clean CLI that returns JSON metadata and file paths.

## Design Principles

| Principle | Meaning |
|---|---|
| **Clean root context** | Claude sees only JSON metadata and file paths — never tokens, boilerplate, or raw output |
| **Append-only execution** | Commands are cells in an ordered log — never edited, only appended — enabling lineage tracking and eviction replay |
| **Output via files** | stdout/stderr land as files. Claude reads selectively to control what enters its context |
| **`sub_llm()` for recursion** | On-cluster LLM calls for map/reduce, classification, summarization. No tools — pure text completions |
| **Everything recorded** | `.cmd.py` files + `session.json` steps = full lineage |

## Constraints

- **Classic all-purpose clusters only** — the Command Execution API requires them
- **Max 145 execution contexts per cluster** — destroy unused sessions to free slots
- **Idle contexts evicted permanently** — the wrapper detects eviction and Claude replays steps
- **Use `%pip install`** for packages — `%pip` works in execution contexts; `%%pip` (double percent) does not
- **Sub-LM calls are blocking** — `sub_llm_batch()` provides parallelism within a single command

## When Invoked

Arguments: `$0` = Databricks CLI profile from `~/.databrickscfg`, `$1` = cluster name (or substring).

1. **Resolve the cluster ID** from the cluster name:
   ```bash
   python3 .claude/skills/databricks-repl/find_cluster.py --profile $0 --name "$1"
   ```
   Returns JSON with `cluster_id`, `cluster_name`, `state`. If multiple matches, ask the user to pick. If the cluster is not running, inform the user.

2. **Check for an active session** — look for `session.json` in the project dir. If one exists and is not destroyed, reuse it. If destroyed or missing, create a new one:
   ```bash
   python3 .claude/skills/databricks-repl/dbx_repl.py create \
     --cluster-id <RESOLVED_ID> --session-name <task-name> --profile $0
   ```

3. **Execute the user's code** via `exec`. Keep the session alive for follow-up commands.

4. **Read output selectively** — use `stdout_preview` for small output, read the file for larger output. Present results to the user.

5. **Only destroy** when the user says they're done, or when switching to a different task.

## Quick Start

```bash
# 1. Create a session (injects bootstrap helpers into the REPL)
python .claude/skills/databricks-repl/dbx_repl.py create --cluster-id $CLUSTER_ID --session-name my-task --profile $0

# 2. Execute code (submit + wait, returns JSON metadata)
python .claude/skills/databricks-repl/dbx_repl.py exec \
  --command "df = spark.read.parquet('s3://bucket/data')" \
  --tag "load_data"

# 3. Read output selectively (never dump full stdout)
head -20 repl_outputs/001_load_data.stdout

# 4. Iterate — execute more commands, read results, refine
python .claude/skills/databricks-repl/dbx_repl.py exec \
  --command "print(df.describe().toPandas().to_string())" \
  --tag "explore"

# 5. Destroy when done
python .claude/skills/databricks-repl/dbx_repl.py destroy
```

## Core Workflow

1. **Create** a session — one per task. The wrapper creates an execution context and injects bootstrap helpers.
2. **Exec** commands sequentially — each returns JSON metadata with `stdout_file`, `stderr_file`, and `stdout_preview`. Never see raw output in the response.
3. **Read output files selectively** — use `head`, `grep`, or partial reads. Control what enters your context.
4. **Persist results to Volumes** using standard Python (`shutil.copy2`, `df.write.parquet`, `open().write()`) when you need outputs to survive eviction.
5. **Handle eviction** if it occurs — the wrapper detects it and returns a structured response. Replay steps using idempotent patterns.
6. **Destroy** the session when finished.

## Core Principles

- **You are the root LM.** Reason about the task, decide what code to run, read outputs selectively. The wrapper handles auth tokens, SDK internals, and polling so they stay out of your context — no need to inspect them.
- **Project directory = session scope.** All commands use `--project-dir` (defaults to cwd) to locate `session.json` and `repl_outputs/`. Each project directory is an independent session. Use `--project-dir` when managing multiple tasks from a single location.
- **Append-only execution.** Each `exec` is a new cell in an ordered log. Append corrections rather than editing previous commands — the ordered log enables lineage tracking and eviction replay.
- **Output via files.** The wrapper writes stdout/stderr to disk. Read only what you need.
- **`sub_llm()` for heavy lifting.** When you need to classify rows, summarize partitions, or process text at scale, use `sub_llm()` inside the REPL — it calls a Databricks serving endpoint.
- **Use standard Python for persistence.** Write files to Volumes with `shutil.copy2`, `df.write.parquet()`, `open().write()`, etc. Track paths yourself for eviction recovery.

## CLI Reference

All commands accept these common options:

| Option | Default | Description |
|---|---|---|
| `--project-dir` | `.` (cwd) | Project root directory. `session.json` and `repl_outputs/` live here. |
| `--profile` | SDK default | Databricks CLI profile name from `~/.databrickscfg` |
| `--debug` | — | Print SDK-level debug information to stderr |

### create

```bash
python .claude/skills/databricks-repl/dbx_repl.py create \
  --cluster-id <CLUSTER_ID> \
  --session-name <NAME>
```

| Parameter | Required | Default | Description |
|---|---|---|---|
| `--cluster-id` | Yes | — | Databricks cluster ID (classic all-purpose only) |
| `--session-name` | Yes | — | Human-readable session name (used in manifest) |

### exec

```bash
# Inline code
python .claude/skills/databricks-repl/dbx_repl.py exec \
  --command "df = spark.read.table('catalog.schema.table')" \
  --tag "load_data"

# Code from file (prefix with @)
python .claude/skills/databricks-repl/dbx_repl.py exec \
  --command @step3_train.py \
  --tag "train"
```

| Parameter | Required | Default | Description |
|---|---|---|---|
| `--command` | Yes | — | Python code (inline string or `@filepath`) |
| `--tag` | Yes | — | Descriptive label for this step |
| `--timeout` | No | 600 | Max seconds to wait. If exceeded, returns `Running` status (command keeps running on cluster). |

Side effects per exec:
- Command saved to `{project-dir}/repl_outputs/{step}_{tag}.cmd.py`
- stdout/stderr written to `.stdout` / `.stderr` files
- `session.json` steps array updated with the new step

### cancel

```bash
# Auto-detect active command from session.json (preferred)
python .claude/skills/databricks-repl/dbx_repl.py cancel

# Or specify a command ID explicitly
python .claude/skills/databricks-repl/dbx_repl.py cancel --run-id <COMMAND_ID>
```

| Parameter | Required | Default | Description |
|---|---|---|---|
| `--run-id` | No | auto-detect | Command ID to cancel. If omitted, reads `active_command` from session.json. |

### await

Re-poll a command that is still running after a previous `exec` or `await` timed out.

```bash
# Re-poll with default timeout (600s)
python .claude/skills/databricks-repl/dbx_repl.py await

# Re-poll with custom timeout
python .claude/skills/databricks-repl/dbx_repl.py await --timeout 1200
```

| Parameter | Required | Default | Description |
|---|---|---|---|
| `--timeout` | No | 600 | Max seconds to wait before returning `Running` status again. |

Reads `active_command` from `session.json`. If the command has finished, writes output files and records the step. If still running, returns a `Running` response with a `tip` for next actions.

### destroy

```bash
python .claude/skills/databricks-repl/dbx_repl.py destroy
```

## Response Schemas

**Exec success:**

```json
{
  "cmd_id": "003_train",
  "status": "Finished",
  "stdout_file": "repl_outputs/003_train.stdout",
  "stderr_file": "repl_outputs/003_train.stderr",
  "stdout_bytes": 1247,
  "stderr_bytes": 342,
  "stdout_preview": "Training complete. F1: 0.87...",
  "elapsed_seconds": 47.3
}
```

**Exec error:**

```json
{
  "cmd_id": "003_train",
  "status": "Error",
  "stdout_file": "repl_outputs/003_train.stdout",
  "stderr_file": "repl_outputs/003_train.stderr",
  "stdout_bytes": 0,
  "stderr_bytes": 891,
  "stderr_preview": "Traceback (most recent call last):\n  File...",
  "elapsed_seconds": 2.1
}
```

**Exec interrupted (Ctrl+C):**

```json
{
  "cmd_id": "003_train",
  "status": "Cancelled",
  "stdout_file": "repl_outputs/003_train.stdout",
  "stderr_file": "repl_outputs/003_train.stderr",
  "stdout_bytes": 0,
  "stderr_bytes": 0,
  "elapsed_seconds": 12.4,
  "message": "Command interrupted by user."
}
```

**Exec timeout (command still running):**

```json
{
  "cmd_id": "003_train",
  "status": "Running",
  "command_id": "abc123-def456",
  "elapsed_seconds": 600.0,
  "message": "Command still running after 600s client-side timeout.",
  "tip": {
    "await": "dbx_repl.py await --timeout 600 --project-dir .",
    "cancel": "dbx_repl.py cancel --project-dir ."
  }
}
```

**Cancel success:**

```json
{
  "status": "cancelled",
  "command_id": "abc123-def456"
}
```

**Exec eviction detected:** See [references/eviction-replay.md](references/eviction-replay.md).

**Decision guide after exec:**
- `stdout_bytes` small (< 500) → read the full file
- `stdout_bytes` large → use `stdout_preview` or `head`/`grep` on the file
- `status: "Error"` → read stderr file, fix the code, exec again

## Error Handling

| Error | Cause | Resolution |
|---|---|---|
| `ClusterNotRunning` | Cluster is off or terminating | Start the cluster and retry |
| `ContextEvicted` | Idle context was garbage-collected | See [references/eviction-replay.md](references/eviction-replay.md) |
| `ContextLimitReached` | 145 contexts on this cluster | Destroy unused sessions |
| `Running` | Exec exceeded `--timeout` | Use `await` to re-poll, `cancel` to abort, or increase `--timeout` |
| `NothingToAwait` | No active command to await | Command already finished or was cancelled |
| `AuthError` | Missing or invalid credentials | Check `~/.databrickscfg` profile or env vars |
| `NothingToCancel` | No active command running | Nothing to do — command already finished |
| `NoSession` | No session.json in project directory | Run `create` first |

## Best Practices

- **Tag every command** with a descriptive `--tag` (e.g., `load_data`, `train`, `evaluate`). Tags appear in the manifest and output filenames.
- **One logical step per exec.** Keep commands focused. Avoid multi-paragraph scripts in a single exec — split into steps.
- **Persist expensive results to Volumes.** If it takes more than a few seconds to compute, write it to a Volume with standard Python. This is both a safety net and a replay optimization.
- **Use `sub_llm()` instead of manual iteration.** When processing rows, classifying text, or summarizing — use the on-cluster LM, not your own context.
- **Handle timeouts gracefully.** If an exec returns `status: "Running"`, the command is still executing on the cluster. Use `await` to re-poll with a fresh timeout, or `cancel` to abort. Do not run another `exec` while a command is running — the execution context is single-threaded and the new command will queue behind the old one.
- **Read before you act.** After an exec, read the output file before deciding the next step. Don't chain multiple execs blindly.
- **Execute from file for long code.** Write complex code to a `.py` file first, then use `--command @filename.py`.
- **Use `--project-dir` for multi-task workflows.** Run independent sessions in separate project directories:
  ```bash
  python .claude/skills/databricks-repl/dbx_repl.py exec --project-dir ./examples/categorization --command "..." --tag "classify"
  python .claude/skills/databricks-repl/dbx_repl.py exec --project-dir ./examples/reranking --command "..." --tag "rerank"
  ```

## Reference Files

Read these as needed for detailed documentation:

- **[references/bootstrap-helpers.md](references/bootstrap-helpers.md)** — Read when using `sub_llm()` or `sub_llm_batch()` inside the REPL. Includes signatures and examples.
- **[references/eviction-replay.md](references/eviction-replay.md)** — Read when a command fails due to context eviction. Covers detection, the eviction response format, and idempotent replay strategies.
