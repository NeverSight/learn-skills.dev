---
name: recursive-training
description: 'Use after completed recursive-mode runs accumulate to extract durable experiential memory into `/.recursive/memory/`, then load it for later runs through the canonical loader.'
---

# recursive-training

## Purpose

Use this skill after a repository has accumulated completed recursive-mode runs and you want to turn repeated successes or failures into durable, repo-local guidance.

The canonical workflow still lives in `/.recursive/RECURSIVE.md`. This skill owns only the training, loading, and memory-discipline layer that sits around completed runs.

## When to use it

Use `recursive-training` to:

- extract cross-run learnings from completed recursive-mode runs
- keep those learnings in `/.recursive/memory/` instead of ad hoc mirrors
- refresh memory after Phase 8 locks
- load only the most relevant prior learnings before a new run starts
- provide startup guidance without mutating the memory plane

## Hard rules

1. Repository-local only. Training data and extracted memory stay inside the current repo.
2. No parameter updates. Learning happens through files in `/.recursive/memory/`, not model mutation.
3. `/.recursive/memory/` is the only canonical store. Pointer files are bootstrap-managed and non-authoritative.
4. All markdown under `/.recursive/run/<run-id>/` is eligible training input, not just `00-08`.
5. Group runs by subsystem only. The extractor assigns task types per learning item.
6. Use contrastive extraction when both winners and losers exist; fall back to winner-only extraction for high-quality repos.
7. Every extracted item must remain evidence-grounded in completed runs.
8. Training scripts do not own `AGENTS.md`; bootstrap owns bridge-file updates.

## Training model

`recursive-training` combines two ideas:

- **ReasoningBank-style memory items** for structured, reusable extracted guidance
- **Training-free GRPO-style comparison** for contrastive winner/loser extraction when variance exists

At a high level:

1. Parse all markdown artifacts from completed runs.
2. Infer the dominant subsystem from changed paths and evidence across those artifacts.
3. Classify each subsystem group as contrastive, winner-only, or insufficient.
4. Ask the extractor for structured learning items.
5. Write those items into:
   - `/.recursive/memory/domains/<subsystem>.md`
   - `/.recursive/memory/training/<task-type>.md`
6. Refresh the memory registry/startup guidance without treating pointer files as authoritative memory.

For the full schema, grouping logic, evidence signals, and extraction contracts, see:

- `references/memory-architecture.md`
- `references/phase8-and-loading.md`

## Phase 8 and loading boundary

Phase 8 records the **current run's** observations in `08-memory-impact.md`.

Training then turns **many completed runs** into cross-run memory.

That means:

- `08-memory-impact.md` is run-local capture
- `recursive-training-phase8-trigger.py` is the handoff after Phase 8 locks
- `recursive-training-grpo.py` builds prompts and writes memory after extraction
- `recursive-training-extract.py` evaluates prompts (required companion; not optional)
- `recursive-training-loader.py` is the canonical retrieval path before later runs
- `recursive-training-sync.py` prints startup guidance without mutating the memory plane

Extractor wiring (first match wins):

1. `--response-file` / sibling `<prompt>.response.json` for agent-operated offline evaluation
2. `RECURSIVE_TRAINING_EXTRACTOR_CMD` with `{prompt_file}` / `{repo_root}` placeholders
3. otherwise exit `2` (unavailable) — GRPO/trigger must fail, not claim success

Detailed Phase 8 handoff and loader behavior lives in `references/phase8-and-loading.md`.

## Commands

Full training:

```bash
python .recursive/scripts/recursive-training-grpo.py --repo-root .
```

Incremental training after a specific run:

```bash
python .recursive/scripts/recursive-training-grpo.py --repo-root . --incremental --run-id <run-id>
```

Post-Phase 8 trigger:

```bash
python .recursive/scripts/recursive-training-phase8-trigger.py --repo-root . --run-id <run-id>
python .recursive/scripts/recursive-training-phase8-trigger.py --repo-root . --run-id <run-id> --auto
```

Read-only startup guidance:

```bash
python .recursive/scripts/recursive-training-sync.py --repo-root .
```

Canonical memory loading before a new run:

```bash
python .recursive/scripts/recursive-training-loader.py \
  --repo-root . \
  --query "<task description>" \
  --files "<comma-separated paths>"
```

Optional MCP convenience layer:

```bash
python .recursive/scripts/recursive-training-mcp.py --repo-root .
```

## Trigger patterns

Recognize these as training requests:

- `train`
- `training`
- `extract memories`
- `learn from runs`
- `train from the latest run`
- `incremental training`
- `sync memories`
- `/recursive-training`

Default behavior:

- fewer than 2 completed runs: explain why extraction is skipped
- no explicit scope: default to full training
- explicit run or "incremental": use incremental mode
- "sync" or "what should I read": use `recursive-training-sync.py`

## Operator checklist

1. Confirm the repo already has recursive-mode scaffolding.
2. Confirm completed runs exist under `/.recursive/run/`.
3. Run the trigger or grpo script with the intended scope.
4. Verify updated items land under `/.recursive/memory/domains/` and `/.recursive/memory/training/`.
5. Before the next run, read `/.recursive/memory/MEMORY.md` and call the loader with task context.
6. Treat loader output as advisory context; the canonical records stay in the memory plane.

## Script surface

- `.recursive/scripts/recursive-training-grpo.py`
- `.recursive/scripts/recursive-training-grpo.ps1`
- `.recursive/scripts/recursive-training-extract.py`
- `.recursive/scripts/recursive-training-extract.ps1`
- `.recursive/scripts/recursive-training-phase8-trigger.py`
- `.recursive/scripts/recursive-training-phase8-trigger.ps1`
- `.recursive/scripts/recursive-training-sync.py`
- `.recursive/scripts/recursive-training-sync.ps1`
- `.recursive/scripts/recursive-training-loader.py`
- `.recursive/scripts/recursive-training-loader.ps1`
- `.recursive/scripts/recursive-training-mcp.py`
- `.recursive/scripts/recursive-training-mcp.ps1`

## Detailed references

- `references/memory-architecture.md` — schema, evidence signals, grouping, extraction modes, and output contract
- `references/phase8-and-loading.md` — Phase 8 handoff, trigger behavior, loader timing, and integration patterns

## Coverage Gate

- [x] Canonical memory-store boundary documented
- [x] Contrastive and winner-only extraction modes documented
- [x] Subsystem-only grouping documented
- [x] All-markdown run-folder input scope documented
- [x] Phase 8 handoff and loader boundary documented
- [x] Canonical command surface documented
- [x] Reference docs linked for detailed extraction and loading behavior
- [x] Script-only transport boundary preserved

Coverage: PASS

## Approval Gate

- [x] Skill defers to `/.recursive/RECURSIVE.md` for overall workflow rules
- [x] Repository-local scope preserved
- [x] No parameter-updating behavior introduced
- [x] `/.recursive/memory/` remains the only canonical store
- [x] Phase 8 capture vs training extraction boundary is explicit
- [x] Loader remains the canonical retrieval path
- [x] Pointer files remain bootstrap-managed, not sync-authored mirrors

Approval: PASS
