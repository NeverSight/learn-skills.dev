---
name: turbo-lifecycle
description: "Pipeline state management for Goldsky Turbo — pause, resume, restart, and delete commands with their rules and safety behavior. Use this skill when the user asks: will deleting my pipeline lose the data already in my postgres/clickhouse table, how do I pause a pipeline while doing database maintenance, how do I restart from block zero to reprocess all historical data, can I update a running streaming pipeline in place or do I have to delete and redeploy, will resuming a paused pipeline pick up from where it left off (checkpoint), how do I re-run a completed job pipeline from the beginning, can I pause or restart a job-mode pipeline. Also covers what happens to checkpoint state on delete, and job auto-deletion 1 hour after termination. For actively diagnosing why a pipeline is broken or erroring, use /turbo-doctor instead."
---

# Turbo Pipeline Lifecycle Reference

CLI commands for managing pipeline lifecycle. Covers streaming and job-mode differences. For interactive pipeline troubleshooting, use `/turbo-doctor` instead.

## Quick Reference

| Action             | Command                                           |
| ------------------ | ------------------------------------------------- |
| List all pipelines | `goldsky turbo list`                              |
| Delete by name     | `goldsky turbo delete <pipeline-name>`            |
| Delete by YAML     | `goldsky turbo delete -f <pipeline.yaml>`         |
| Pause pipeline     | `goldsky turbo pause <pipeline-name>`             |
| Resume pipeline    | `goldsky turbo resume <pipeline-name>`            |
| Restart pipeline   | `goldsky turbo restart <pipeline-name>`           |
| Restart fresh      | `goldsky turbo restart <pipeline-name> --clear-state` |

## Pipeline States

| State     | Description                                  |
| --------- | -------------------------------------------- |
| running   | Pipeline is actively processing data         |
| starting  | Pipeline is initializing                     |
| paused    | Pipeline is paused (replicas set to 0)       |
| stopped   | Pipeline is not running (manually stopped)   |
| error     | Pipeline encountered an error                |
| completed | Job-mode pipeline finished processing range  |

## Streaming vs Job Mode Lifecycle

Streaming and job-mode pipelines behave differently for lifecycle operations:

| Operation     | Streaming Pipeline            | Job-Mode Pipeline (`job: true`)             |
| ------------- | ----------------------------- | ------------------------------------------- |
| **List**      | Shows as `running`/`paused`   | Shows as `running`/`completed`              |
| **Pause**     | ✅ Supported                   | ❌ Not supported                             |
| **Resume**    | ✅ Supported                   | ❌ Not supported                             |
| **Restart**   | ✅ Supported                   | ❌ Not supported — use delete + apply        |
| **Delete**    | ✅ Supported                   | ✅ Supported (auto-cleanup ~1hr after done)  |
| **Apply**     | Updates in place              | Must delete first, then re-apply            |

### Job-Mode Pipeline Lifecycle

Job-mode pipelines (`job: true` in YAML) are one-time batch processes. They:

1. **Start** — process data from `start_at` (or `earliest`) to `end_block` (or chain tip)
2. **Run** — process the bounded data range
3. **Complete** — automatically stop when the range is fully processed
4. **Auto-cleanup** — ~1 hour after completion, the pipeline is automatically removed

**Key rules for job-mode pipelines:**

- **Cannot pause, resume, or restart** — these commands return an error for job pipelines
- **Cannot update in place** — must delete the old job, then apply a new one
- **Redeploying a job** — if you need to re-run:
  ```bash
  goldsky turbo delete my-job-pipeline
  goldsky turbo apply my-job-pipeline.yaml
  ```
- **If the job errors**, it still auto-deletes ~1 hour after termination — same as successful jobs.

## Pause, Resume, and Restart

### Pause a Pipeline

Temporarily stop processing without deleting:

```bash
goldsky turbo pause <pipeline-name>
# or by YAML:
goldsky turbo pause -f <pipeline.yaml>
```

This sets deployment replicas to 0, preserving all state for later resumption.

### Resume a Pipeline

Restore a paused pipeline to its running state:

```bash
goldsky turbo resume <pipeline-name>
# or by YAML:
goldsky turbo resume -f <pipeline.yaml>
```

> You can only resume a **paused** pipeline. Attempting to resume an already running pipeline returns an error.

### Restart a Pipeline

Trigger a pod restart for a running or paused pipeline:

```bash
goldsky turbo restart <pipeline-name>
```

To clear all checkpoints and reprocess from the beginning:

```bash
goldsky turbo restart <pipeline-name> --clear-state
```

> **Restart vs Resume:** Use `resume` to restore a paused pipeline without restarting pods. Use `restart` when you need a fresh pod restart (e.g., after configuration changes or to recover from issues). Restart is **not supported** for Job-mode pipelines — use `delete` + `apply` instead.

---

## Important Notes

### Deletion is Permanent

- All checkpoints are lost
- Pipeline configuration is removed
- Cannot be undone

### Data in Sinks is Preserved

- Data already written to PostgreSQL, ClickHouse, etc. remains
- Only the pipeline itself is deleted
- You may need to manually clean up sink data if desired

### Checkpoints and Restarts

- Deleting a pipeline removes its checkpoints
- If you recreate a pipeline with the same name, it starts fresh
- To preserve checkpoints, use `goldsky turbo apply` to update instead of delete/recreate

### Job-Mode Pipelines Cannot Be Updated In Place

- Job pipelines (`job: true`) **must be deleted before redeploying**
- Attempting `goldsky turbo apply` on an existing job returns an error: `pipeline already exists`
- Jobs auto-cleanup ~1 hour after termination regardless of success or failure
- Always delete the old job first if redeploying: `goldsky turbo delete <name>`, then `goldsky turbo apply <file.yaml>`

### Project Scope

- `goldsky turbo list` shows pipelines in your current project only
- Use `goldsky project list` to see available projects
- Pipelines are isolated per project

## Common Patterns

### Delete and Recreate

If you need to restart a pipeline from scratch:

1. Delete the existing pipeline:

   ```bash
   goldsky turbo delete my-pipeline
   ```

2. Deploy fresh:

   ```bash
   goldsky turbo apply my-pipeline.yaml
   ```

This resets all checkpoints and starts processing from the configured `start_at` position.

### Rename Instead of Delete

To keep checkpoints but change the pipeline name:

1. Update the `name` field in your YAML
2. Apply the new configuration:

   ```bash
   goldsky turbo apply my-pipeline-v2.yaml
   ```

3. Delete the old pipeline:

   ```bash
   goldsky turbo delete my-pipeline
   ```

**Note:** This creates a new pipeline; checkpoints don't transfer between names.

### Clean Up Test Pipelines

For development, use a naming convention like `test-*` or `dev-*`:

```yaml
name: test-usdc-transfers # Easy to identify for cleanup
```

Then clean up all test pipelines when done.

## Troubleshooting

| Issue                        | Action                                                        |
| ---------------------------- | ------------------------------------------------------------- |
| Pipeline not found           | Check spelling; use `goldsky turbo list` to see names         |
| Permission denied            | Verify you have Editor or Admin role in the project           |
| Delete failed                | Check logs for errors; pipeline may be in transition          |
| Wrong project                | Use `goldsky project list` to verify current project          |
| `pipeline already exists`    | Job-mode pipeline — delete first, then re-apply               |
| Cannot pause/resume job      | Job-mode pipelines don't support pause/resume; use delete     |
| Cannot restart job           | Job-mode pipelines don't support restart; delete + re-apply   |

### Error: Pipeline Not Found

```
Error: Pipeline 'wrong-name' not found
```

Fix: Run `goldsky turbo list` to see exact pipeline names. Names are case-sensitive.

### Error: Permission Denied

```
Error: Permission denied
```

Fix: You need Editor or Admin role. Contact a project Owner to upgrade your role.

## Related

- **`/turbo-doctor`** — Interactive diagnostic skill for pipeline issues
- **`/turbo-builder`** — Build and deploy new pipelines
