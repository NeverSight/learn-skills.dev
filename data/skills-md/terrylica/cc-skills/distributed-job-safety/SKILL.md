---
name: distributed-job-safety
description: Concurrency safety patterns for distributed pueue + mise + systemd-run job pipelines. TRIGGERS - queue pueue jobs, deploy to remote host, concurrent job collisions, checkpoint races, resource guards, cgroup memory limits, systemd-run, autoscale, batch processing safety, job parameter isolation.
allowed-tools: Read, Bash, Write
---

# Distributed Job Safety

Patterns and anti-patterns for concurrent job management with pueue + mise + systemd-run, learned from production failures in distributed data pipeline orchestration.

**Scope**: Universal principles for any pueue + mise workflow with concurrent parameterized jobs. Examples use illustrative names but the principles apply to any domain.

**Prerequisite skills**: `devops-tools:pueue-job-orchestration`, `itp:mise-tasks`, `itp:mise-configuration`

---

## The Nine Invariants

Non-negotiable rules for concurrent job safety. Violating any one causes silent data corruption or job failure.

Full formal specifications: [references/concurrency-invariants.md](./references/concurrency-invariants.md)

### 1. Filename Uniqueness by ALL Job Parameters

Every file path shared between concurrent jobs MUST include ALL parameters that differentiate those jobs.

```
WRONG:  {symbol}_{start}_{end}.json                    # Two thresholds collide
RIGHT:  {symbol}_{threshold}_{start}_{end}.json         # Each job gets its own file
```

**Test**: If two pueue jobs can run simultaneously with different parameter values, those values MUST appear in every shared filename, temp directory, and lock file.

### 2. Verify Before Mutate (No Blind Queueing)

Before queueing jobs, check what is already running. Before deleting state, check who owns it.

```bash
# WRONG: Blind queue
for item in "${ITEMS[@]}"; do
    pueue add --group mygroup -- run_job "$item" "$param"
done

# RIGHT: Check first
running=$(pueue status --json | jq '[.tasks[] | select(.status | keys[0] == "Running") | .label] | join(",")')
if echo "$running" | grep -q "${item}@${param}"; then
    echo "SKIP: ${item}@${param} already running"
    continue
fi
```

### 3. Idempotent File Operations (missing_ok=True)

All file deletion in concurrent contexts MUST tolerate the file already being gone.

```python
# WRONG: TOCTOU race
if path.exists():
    path.unlink()        # Crashes if another job deleted between check and unlink

# RIGHT: Idempotent
path.unlink(missing_ok=True)
```

### 4. Atomic Writes for Shared State

Checkpoint files must never be partially written. Use the tempfile-fsync-rename pattern.

```python
fd, temp_path = tempfile.mkstemp(dir=path.parent, prefix=".ckpt_", suffix=".tmp")
with os.fdopen(fd, "w") as f:
    f.write(json.dumps(data))
    f.flush()
    os.fsync(f.fileno())
os.replace(temp_path, path)  # POSIX atomic rename
```

**Bash equivalent** (for NDJSON telemetry appends):

```bash
# Atomic multi-line append via flock + temp file
TMPOUT=$(mktemp)
# ... write lines to $TMPOUT ...
flock "${LOG_FILE}.lock" bash -c "cat '${TMPOUT}' >> '${LOG_FILE}'"
rm -f "$TMPOUT"
```

### 5. Config File Is SSoT

The `.mise.toml` `[env]` section is the single source of truth for environment defaults. Per-job `env` overrides bypass the SSoT and allow arbitrary values with no review gate.

```bash
# WRONG: Per-job override bypasses mise SSoT
pueue add -- env MY_APP_MIN_THRESHOLD=50 uv run python script.py

# RIGHT: Set the correct value in .mise.toml, no per-job override needed
pueue add -- uv run python script.py
```

**Controlled exception**: `pueue env set <id> KEY VALUE` is acceptable for one-off overrides on stashed/queued tasks (e.g., hyperparameter sweeps). The key distinction: mise `[env]` is SSoT for **defaults** that apply to all runs; `pueue env set` is for **one-time parameterization** of a specific task without modifying the config file. See `devops-tools:pueue-job-orchestration` Per-Task Environment Override section.

### 6. Maximize Parallelism Within Safe Margins

Always probe host resources and scale parallelism to use available capacity. Conservative defaults waste hours of idle compute.

```bash
# Probe host resources
ssh host 'nproc && free -h && uptime'

# Sizing formula (leave 20% margin for OS + DB + overhead)
# max_jobs = min(
#     (available_memory_gb * 0.8) / per_job_memory_gb,
#     (total_cores * 0.8) / per_job_cpu_cores
# )
```

**For ClickHouse workloads**: The bottleneck is often ClickHouse's `concurrent_threads_soft_limit` (default: 2 x nproc), not pueue's parallelism. Each query requests `max_threads` threads (default: nproc). Right-size `--max_threads` per query to match the effective thread count (soft_limit / pueue_slots), then increase pueue slots. Pueue parallelism can be adjusted live without restarting running jobs.

**Post-bump monitoring** (mandatory for 5 minutes after any parallelism change):

- `uptime` -- load average should stay below 0.9 x nproc
- `vmstat 1 5` -- si/so columns must remain 0 (no active swapping)
- ClickHouse errors: `SELECT count() FROM system.query_log WHERE event_time > now() - INTERVAL 5 MINUTE AND type = 'ExceptionWhileProcessing'` -- must be 0

**Cross-reference**: See `devops-tools:pueue-job-orchestration` ClickHouse Parallelism Tuning section for the full decision matrix.

### 7. Per-Job Memory Caps via systemd-run

On Linux with cgroups v2, wrap each job with `systemd-run` to enforce hard memory limits.

```bash
systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 \
    uv run python scripts/process.py --symbol BTCUSDT --threshold 250
```

**Critical**: `MemorySwapMax=0` is mandatory. Without it, the process escapes into swap and the memory limit is effectively meaningless.

### 8. Monitor by Stable Identifiers, Not Ephemeral IDs (INV-8)

Pueue job IDs are ephemeral -- they shift when jobs are removed, re-queued, or split. Use group names and label patterns for monitoring.

```bash
# WRONG: Hardcoded job IDs
if pueue status --json | jq -e ".tasks.\"14\"" >/dev/null; then ...

# RIGHT: Query by group/label
pueue status --json | jq -r '.tasks | to_entries[] | select(.value.group == "mygroup") | .value.id'
```

Full specification: [references/concurrency-invariants.md](./references/concurrency-invariants.md#inv-8)

### 9. Derived Artifact Filenames Must Include ALL Category Dimensions (INV-9)

When concurrent or sequential pipeline phases produce derived artifacts (Parquet chunks, JSONL summaries, temp files) that share a directory, **every filename must include ALL discriminating dimensions** -- not just the job-level parameters (INV-1), but also pipeline-level categories like direction, strategy, or generation.

```
WRONG:  _chunk_{formation}_{symbol}_{threshold}.parquet     # No direction -- LONG glob eats SHORT files
RIGHT:  _chunk_{direction}_{formation}_{symbol}_{threshold}.parquet  # Direction-scoped
```

**Glob scope rule**: Cleanup and merge globs must match the filename pattern exactly:

```python
# WRONG: Unscoped glob -- consumes artifacts from other categories
chunk_files = folds_dir.glob("_chunk_*.parquet")

# RIGHT: Category-scoped glob -- only touches this category's artifacts
chunk_files = folds_dir.glob(f"_chunk_{direction}_*.parquet")
```

**Post-merge validation**: After merging artifacts, assert expected values in category columns:

```python
merged_df = pl.concat([pl.read_parquet(p) for p in chunk_files])
assert set(merged_df["strategy"].unique()) == {"standard"}, "Direction contamination!"
```

**Relationship to INV-1**: INV-1 ensures checkpoint file uniqueness by job parameters (runtime isolation). INV-9 extends this to derived artifacts that persist across pipeline phases (artifact isolation). Both prevent the same class of bug -- silent cross-contamination from filename collisions.

Full specification: [references/concurrency-invariants.md](./references/concurrency-invariants.md#inv-9)

---

## Anti-Patterns (Learned from Production)

17 anti-patterns documented from production failures. Full details with code examples: [references/anti-patterns.md](./references/anti-patterns.md)

| AP    | Name                                   | Key Symptom                                    | Related Invariant |
| ----- | -------------------------------------- | ---------------------------------------------- | ----------------- |
| AP-1  | Redeploying without checking running   | Checkpoint collisions after kill+requeue       | INV-2             |
| AP-2  | Checkpoint filename missing parameters | `FileNotFoundError` on checkpoint delete       | INV-1             |
| AP-3  | Trusting `pueue restart` logs          | Old error appears after restart                | --                |
| AP-4  | Assuming PyPI propagation is instant   | "no version found" after publish               | --                |
| AP-5  | Editable source vs. installed wheel    | `uv run` uses old code after pip upgrade       | --                |
| AP-6  | Sequential phase assumption            | Phase contention from simultaneous queueing    | --                |
| AP-7  | Manual post-processing steps           | "run optimize after they finish" never happens | --                |
| AP-8  | Hardcoded job IDs in monitors          | Monitor crashes after job re-queue             | INV-8             |
| AP-9  | Sequential when epochs enable parallel | 1,700 hours single-threaded on 25+ cores       | INV-6             |
| AP-10 | State file bloat                       | Silent 60x slowdown in job submission          | --                |
| AP-11 | Wrong working directory in remote jobs | `[Errno 2] No such file or directory`          | --                |
| AP-12 | Per-file SSH for bulk submission       | 300K jobs takes days (SSH overhead)            | --                |
| AP-13 | SIGPIPE under `set -euo pipefail`      | Exit code 141 on harmless pipe ops             | --                |
| AP-14 | False data loss from variable NDJSON   | `wc -l` shows 3-6% fewer lines                 | --                |
| AP-15 | Cursor file deletion on completion     | Full re-run instead of incremental resume      | --                |
| AP-16 | mise `[env]` for pueue/cron secrets    | Empty env vars in daemon jobs                  | INV-5             |
| AP-17 | Unscoped glob across pipeline phases   | Phase A consumes Phase B's artifacts           | INV-9             |

---

## The Mise + Pueue + systemd-run Stack

Full architecture diagram and responsibility boundaries: [references/stack-architecture.md](./references/stack-architecture.md)

| Layer           | Responsibility                                             |
| --------------- | ---------------------------------------------------------- |
| **mise**        | Environment variables, tool versions, task discovery       |
| **pueue**       | Daemon persistence, parallelism limits, restart, `--after` |
| **systemd-run** | Per-job cgroup memory caps (Linux only, no-op on macOS)    |
| **autoscaler**  | Dynamic parallelism tuning based on host resources         |
| **Python/app**  | Domain logic, checkpoint management, data integrity        |

---

## Remote Deployment Protocol

When deploying a fix to a running host:

```
1. AUDIT:   ssh host 'pueue status --json' -> count running/queued/failed
2. DECIDE:  Wait for running jobs? Kill? Let them finish with old code?
3. PULL:    ssh host 'cd ~/project && git fetch origin main && git reset --hard origin/main'
4. VERIFY:  ssh host 'cd ~/project && python -c "import pkg; print(pkg.__version__)"'
5. UPGRADE: ssh host 'cd ~/project && uv pip install --python .venv/bin/python --refresh pkg==X.Y.Z'
6. RESTART: ssh host 'pueue restart <failed_id>' OR add fresh jobs
7. MONITOR: ssh host 'pueue status --group mygroup'
```

**Critical**: Step 1 (AUDIT) is mandatory. Skipping it is the root cause of cascade failures.

See: [references/deployment-checklist.md](./references/deployment-checklist.md) for full protocol.

---

## Concurrency Safety Decision Tree

```
Adding a new parameter to a resumable job function?
|-- Is it job-differentiating (two jobs can have different values)?
|   |-- YES -> Add to checkpoint filename
|   |          Add to pueue job label
|   |          Add to remote checkpoint key
|   |-- NO  -> Skip (e.g., verbose, notify are per-run, not per-job)
|
|-- Does the function delete files?
|   |-- YES -> Use missing_ok=True
|   |          Use atomic write for creates
|   |-- NO  -> Standard operation
|
|-- Does the function write to shared storage?
    |-- YES -> Force deduplication after write
    |          Use UPSERT semantics where possible
    |-- NO  -> Standard operation
```

---

## Autoscaler

Dynamic parallelism tuning for pueue groups based on host CPU and memory. Full details: [references/autoscaler.md](./references/autoscaler.md)

```
CPU < 40% AND MEM < 60%  ->  SCALE UP (+1 per group)
CPU > 80% OR  MEM > 80%  ->  SCALE DOWN (-1 per group)
Otherwise                 ->  HOLD
```

**Key principle**: Ramp up incrementally (not to max). Job memory grows over time -- jumping to max parallelism risks OOM when all jobs peak simultaneously.

---

## Project-Specific Extensions

This skill provides **universal patterns** that apply to any distributed job pipeline. Projects should create a **local extension skill** (e.g., `myproject-job-safety`) in their `.claude/skills/` directory that provides:

| Local Extension Provides        | Example                                           |
| ------------------------------- | ------------------------------------------------- |
| Concrete function names         | `run_resumable_job()` -> `myapp_populate_cache()` |
| Application-specific env vars   | `MY_APP_MIN_THRESHOLD`, `MY_APP_CH_HOSTS`         |
| Memory profiles per job type    | "250 dbps peaks at 5 GB, use MemoryMax=8G"        |
| Database-specific audit queries | `SELECT ... FROM mydb.mytable ... countIf(x < 0)` |
| Issue provenance tracking       | "Checkpoint race: GH-84"                          |
| Host-specific configuration     | "bigblack: 32 cores, 61 GB, groups p1/p2/p3/p4"   |

**Two-layer invocation pattern**: When this skill is triggered, also check for and invoke any local `*-job-safety` skill in the project's `.claude/skills/` directory for project-specific configuration.

```
devops-tools:distributed-job-safety    (universal patterns - this skill)
  + .claude/skills/myproject-job-safety  (project-specific config)
  = Complete operational knowledge
```

---

## SOTA Alternative: Temporal for Durable Workflows

For structured, repeatable job pipelines, [Temporal](https://temporal.io/) provides built-in enforcement of many invariants in this skill:

| This Skill's Invariant              | Temporal Equivalent                                |
| ----------------------------------- | -------------------------------------------------- |
| INV-2 (Verify before mutate)        | Workflow ID uniqueness — duplicate starts rejected |
| INV-3 (Idempotent operations)       | Activity retry with `non_retryable_error_types`    |
| INV-6 (Maximize parallelism safely) | `max_concurrent_activities` per worker             |
| INV-8 (Stable identifiers)          | Workflow IDs are user-defined and permanent        |

**When to consider Temporal**: When your pipeline has well-defined activities (not ad-hoc shell commands), needs dedup/idempotency guarantees, or when the overhead of pueue guardrails (autoscaler agents, manual retry classification) exceeds the overhead of running a Temporal server.

**Install**: `pip install temporalio` (Python SDK), `brew install temporal` (CLI + dev server).

**Lesson from 2026-03-04 incident**: 5 autonomous Claude Code agents monitoring 60 pueue jobs created ~12,800 runaway tasks because pueue's `restart` creates new tasks (not in-place), agents had no mutation budgets, and persistent failures were blindly retried. Temporal prevents all three failure modes natively.

---

## References

- [Anti-Patterns](./references/anti-patterns.md) -- 17 production failure patterns (AP-1 through AP-17)
- [Concurrency Invariants](./references/concurrency-invariants.md) -- Formal invariant specifications (INV-1 through INV-9)
- [Deployment Checklist](./references/deployment-checklist.md) -- Step-by-step remote deployment protocol
- [Environment Gotchas](./references/environment-gotchas.md) -- Host-specific pitfalls (G-1 through G-17)
- [Stack Architecture](./references/stack-architecture.md) -- Mise + Pueue + systemd-run layer diagram
- [Autoscaler](./references/autoscaler.md) -- Dynamic parallelism tuning patterns
- **Cross-reference**: `devops-tools:pueue-job-orchestration` -- Pueue basics, dependency chaining, installation
- **SOTA Alternative**: [Temporal](https://temporal.io/) -- Durable workflow orchestration with built-in dedup and retry
