---
name: next-actions
description: Query the KB database for the next unblocked stories and recommend commands. Falls back to WORK-ORDER-BY-BATCH.md if the DB has no stories.
created: 2026-02-20
updated: 2026-02-25
version: 2.2.0
type: utility
---

# /next-actions — Find Next Actions from KB Database

> **CRITICAL EXECUTION RULE: Do NOT spawn sub-agents (Task tool) for this skill. Call all MCP tools directly in the main conversation using the `mcp__knowledge-base__` prefix. Sub-agents do not have reliable access to the knowledge-base MCP server and will waste time exploring the filesystem instead of making tool calls.**

## Usage

```
/next-actions [N] [--tag=TAG] [--plan-status=STATUS]
```

**Examples:**
```bash
# Show the next 5 actionable items (default)
/next-actions

# Show the next 3 actionable items
/next-actions 3

# Show the next 10 actionable items
/next-actions 10

# Show next actions for plans that improve testing
/next-actions --tag=testing

# Show next actions for lego-ui plans only
/next-actions --tag=lego-ui

# Show next actions from in-progress plans
/next-actions --plan-status=in-progress

# Combine: next 3 elaboration items from in-progress plans
/next-actions 3 --tag=elaboration --plan-status=in-progress
```

---

## What It Does

Queries the **KB database** (single source of truth) for stories that need action, resolves dependencies at query time, and maps each story's state to the appropriate workflow command.

Inflight work always appears before new work. Stories being actively worked by an agent (active worktree in DB) are **excluded entirely**.

---

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `N` | No | Number of items to return (default: 5) |
| `--tag=TAG` | No | Filter to stories linked to plans with this tag (e.g., `testing`, `lego-ui`, `elaboration`, `development`, `agent-tooling`) |
| `--plan-status=STATUS` | No | Filter to stories linked to plans with this status (`draft`, `accepted`, `stories-created`, `in-progress`, `implemented`, `superseded`, `archived`) |

---

## Priority Order (non-negotiable)

| Rank | Category | States | Rationale |
|------|----------|--------|-----------|
| 1 | **Needs QA** | `ready_for_qa`, `in_qa` | Closest to done — unblock the pipeline first |
| 2 | **Needs Fix** | `failed_qa`, `failed_code_review`, `in_review` | Something was rejected — fix before starting new work |
| 3 | **Needs Code Review** | `ready_for_review` | Dev complete, waiting on review |
| 4 | **Needs Dev** | `ready`, `in_progress` (no active worktree) | Elaborated and ready to implement |
| 5 | **Needs Elaboration** | `backlog` (story file exists) | Story seed exists, not yet elaborated |
| 6 | **Needs Story Creation** | `backlog` (no story file) | Only a seed — story not yet generated |

Within each rank, sort by priority: `critical` > `high` > `medium` > `low`.

---

## Execution Steps

### Step 1 — Get Active Worktrees

Call `mcp__knowledge-base__worktree_list_active` directly (no sub-agent):

```
mcp__knowledge-base__worktree_list_active({})
→ extract list of story_ids where status = 'active' → call these ACTIVE_IDS
```

If the tool is unavailable, set ACTIVE_IDS = [].

### Step 2 — Query the KB Database

Call `mcp__knowledge-base__kb_list_stories` directly. If `--tag` or `--plan-status` were provided, pass them as `plan_tag` and `plan_status`:

```
mcp__knowledge-base__kb_list_stories({
  epic: "platform",
  states: ["ready_for_qa", "in_qa", "failed_qa", "failed_code_review", "in_review",
           "ready_for_review", "ready", "in_progress", "backlog",
           "completed", "cancelled", "deferred"],
  limit: N,
  ...(TAG ? { plan_tag: TAG } : {}),
  ...(PLAN_STATUS ? { plan_status: PLAN_STATUS } : {})
})
```

If the result contains **0 stories**, go to **Step 6 (Fallback)**.

### Step 3 — Collect N Candidates via `mcp__knowledge-base__kb_get_next_story`

Call `mcp__knowledge-base__kb_get_next_story` up to N times directly (no sub-agent), accumulating excluded IDs. Pass `plan_tag` and `plan_status` if provided:

```
# First call — exclude all active worktrees
mcp__knowledge-base__kb_get_next_story({
  epic: "platform", include_backlog: true, exclude_story_ids: ACTIVE_IDS,
  ...(TAG ? { plan_tag: TAG } : {}),
  ...(PLAN_STATUS ? { plan_status: PLAN_STATUS } : {})
})
→ returns STORY_A

# Second call — exclude active + first result
mcp__knowledge-base__kb_get_next_story({
  epic: "platform", include_backlog: true, exclude_story_ids: [...ACTIVE_IDS, "STORY_A"],
  ...(TAG ? { plan_tag: TAG } : {}),
  ...(PLAN_STATUS ? { plan_status: PLAN_STATUS } : {})
})
→ returns STORY_B

# ... repeat until N items or no more candidates
```

Stop when `mcp__knowledge-base__kb_get_next_story` returns `story: null` or you have N items.

### Step 4 — Re-sort by Priority Rank

After collecting candidates, re-sort by the rank table above (QA > Fix > Review > Dev > Elaboration > Creation), then by story priority within each rank:

```
priority order: critical (1) > high (2) > medium (3) > low (4) > null (5)
```

**Important:** `kb_get_next_story` only returns stories in `ready` or `backlog` state. Stories in other actionable states (`ready_for_qa`, `failed_qa`, `failed_code_review`, `in_review`, `ready_for_review`) must be pulled from the Step 2 `kb_list_stories` result and added to the candidates list before sorting.

To build the full candidate set:
1. From the `kb_list_stories` result, take all stories in inflight states: `ready_for_qa`, `in_qa`, `failed_qa`, `failed_code_review`, `in_review`, `ready_for_review`
2. From `kb_get_next_story` calls, collect up to N stories in `ready` or `backlog` state
3. Remove any ACTIVE_IDS from the combined list
4. Sort the combined list by rank, then by priority within rank
5. Take the top N

### Step 5 — Map State to Command

For each story in the sorted list, determine the command based on its `state` field:

| State | Category | Command Template |
|-------|----------|-----------------|
| `ready_for_qa` | Needs QA | `/qa-verify-story {FEATURE_DIR} {STORY_ID}` |
| `in_qa` | Needs QA | `/qa-verify-story {FEATURE_DIR} {STORY_ID}` |
| `in_review` | Needs Fix | `/dev-fix-story {FEATURE_DIR} {STORY_ID}` |
| `failed_code_review` | Needs Fix | `/dev-fix-story {FEATURE_DIR} {STORY_ID}` |
| `failed_qa` | Needs Fix | `/dev-fix-story {FEATURE_DIR} {STORY_ID}` |
| `ready_for_review` | Needs Code Review | `/dev-code-review {FEATURE_DIR} {STORY_ID}` |
| `ready` or `in_progress` | Needs Dev | `/dev-implement-story {FEATURE_DIR} {STORY_ID}` |
| `backlog` (elaborated) | Needs Elaboration | `/elab-story {FEATURE_DIR} {STORY_ID}` |
| `backlog` (no story) | Needs Story Creation | `/pm-story generate {FEATURE_DIR} {STORY_ID}` |

**Distinguishing elaborated vs. not:** A `backlog` story is "elaborated" if its `story_dir` exists on disk and contains a `story.yaml` file. If the directory or file doesn't exist, it needs story creation.

**Feature directory derivation** from story ID prefix:

| Prefix | Feature Directory |
|--------|------------------|
| `WINT` | `plans/future/platform/wint` |
| `KBAR` | `plans/future/platform/kb-artifact-migration` |
| `AUDT` | `plans/future/platform/code-audit` |
| `TELE` | `plans/future/platform/telemetry` |
| `INFR` | `plans/future/platform/infrastructure` |
| `LNGG` | `plans/future/platform/langgraph-update` |
| `MODL` | `plans/future/platform/model-experimentation` |
| `LERN` | `plans/future/platform/learning-loop` |
| `SDLC` | `plans/future/platform/sdlc-agents` |
| `AUTO` | `plans/future/platform/autonomous-dev` |
| `WKFL` | `plans/future/platform/workflow-learning` |

If the story record has a `story_dir` field, use that to derive the feature directory (strip the story ID segment). If the prefix is not found in the table above, use `plans/future/platform` as the feature directory.

### Step 6 — Fallback (DB Empty)

If Step 2 returned 0 stories, the database likely needs seeding.

1. Read `plans/future/platform/WORK-ORDER-BY-BATCH.md` directly
2. Parse the markdown tables to find unblocked stories
3. Output the results with a **prominent warning**:

```
⚠️  KB database has no stories — falling back to WORK-ORDER-BY-BATCH.md
    Run a DB seed to populate stories for reliable dependency resolution.

[results from markdown parsing]
```

When parsing the markdown fallback:
- Stories with `[x]` checkbox or `✅` status are complete — skip them
- Stories with `❌` or strikethrough are cancelled — skip them
- Stories with `🔧` are being worked — skip them
- For remaining stories, check if all `(#NN)` dependency references point to completed rows
- Use the same state-to-command mapping, inferring state from status emoji:
  - `🔍` → `ready_for_qa` (Needs QA)
  - `⏸️` → `in_review` (Needs Fix — review findings exist)
  - `📋` → `ready_for_review` (Needs Code Review)
  - `🚧` → `in_progress` (Needs Dev)
  - `⏳` → `ready` (Needs Dev)
  - `📝` / `🆕` → `backlog` (Needs Elaboration or Story Creation)
  - `⚪` → `backlog` (Needs Elaboration or Story Creation)
- Apply the same stage-first sorting (QA > Fix > Review > Dev > Elaboration > Creation)

### Step 7 — Output

Format the results as a table. If filters were applied, show them in the header. Inflight work appears first (per the rank order):

```
Next actions (N items):
Filters: tag=testing, plan-status=in-progress    ← only if filters were used

| # | Category          | Story                              | Priority | Command |
|---|-------------------|------------------------------------|----------|---------|
| 1 | Needs QA          | WKFL-002 — Story title             | high     | /qa-verify-story plans/future/platform/workflow-learning WKFL-002 |
| 2 | Needs Fix         | WINT-0030 — Story title            | high     | /dev-fix-story plans/future/platform/wint WINT-0030 |
| 3 | Needs Code Review | WKFL-007 — Story title             | medium   | /dev-code-review plans/future/platform/workflow-learning WKFL-007 |
| 4 | Needs Dev         | WKFL-010 — Story title             | medium   | /dev-implement-story plans/future/platform/workflow-learning WKFL-010 |
| 5 | Needs Elaboration | WKFL-008 — Story title             | low      | /elab-story plans/future/platform/workflow-learning WKFL-008 |
```

If stories were excluded due to active worktrees, note them **below** the table:

```
Excluded (active worktree): WKFL-006, WINT-0100
```

If no unblocked stories exist:

```
No actionable stories found.

All remaining stories are blocked by unresolved dependencies.
Use `kb_list_stories` to inspect blocked stories.
```

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| DB returns 0 stories | Fall back to WORK-ORDER-BY-BATCH.md with warning |
| All stories blocked | Report "no actionable stories" with count of blocked |
| Story has no feature prefix match | Use `plans/future/platform` as feature dir |
| N > available unblocked stories | Return all available (less than N) |
| MCP tools unavailable | Fall back to WORK-ORDER-BY-BATCH.md with warning |
| `mcp__knowledge-base__worktree_list_active` fails | Treat ACTIVE_IDS as empty, proceed without exclusion |
| Story in `in_progress` with no active worktree | Treat as Needs Dev (rank 4) |
