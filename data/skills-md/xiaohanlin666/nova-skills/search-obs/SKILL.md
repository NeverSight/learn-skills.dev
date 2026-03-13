---
name: search-obs
description: Search and retrieve OBS (defect/observation) details in HP Nova. Supports querying OBS directly by OBS number, listing all OBS under a specific task code, or first finding tasks by title/owner/status and then retrieving their OBS. Use this skill whenever the user wants to find, view, or analyze OBS records in Nova.
version: 0.0.1
author: Matt Xiao
---

# Search OBS Skill

Search and retrieve OBS (defect/observation) records in the HP Nova test management platform using the `nova_get_obs`, `nova_get_task_obs`, `nova_search_task`, and `nova_search_user` MCP tools.

## When to Use

Invoke this skill when the user says something like:

- "Get OBS details for OBS number 2464344"
- "What is the short description of OBS 2451603?"
- "Show me all OBS under task TASK0000044928"
- "List OBS for task ICQ-TASK0000044928"
- "Find tasks with title 'nova test' and show their OBS"
- "Show blocking OBS for task owned by bjorn_deng"
- "List new OBS under task TASK0000041124"
- "查询 OBS 2467069 的详情"
- "帮我查 ICQ-TASK0000044928 有哪些 OBS"

---

## Three Query Modes

### Mode 1 — Query OBS by OBS Number

**When**: User provides a specific OBS ID (numeric integer).

**Tool**: `nova_get_obs`

**Steps**:
1. Extract the numeric `obs_id` from user input.
2. Call `nova_get_obs` with the `obs_id`.
3. Display full OBS detail (see OBS Detail Output Format below).

---

### Mode 2 — List OBS under a Known Task Code

**When**: User provides a task code directly (e.g., `TASK0000044928`, `ICQ-TASK0000044928`).

**Tool**: `nova_get_task_obs`

**Steps**:
1. Extract `task_code` from user input. Use exactly as provided (including any prefix like `ICQ-`).
2. Apply optional filters if specified:
   - `isNew`: `-1` = all (default), `1` = new OBS only, `0` = existing/recurring OBS only
   - `isBlock`: `-1` = all (default), `1` = blocking OBS only, `0` = non-blocking only
3. Call `nova_get_task_obs` with the task code and filters.
4. Display task summary and OBS list (see Task OBS Output Format below).

---

### Mode 3 — Find Task First, Then List its OBS

**When**: User does not provide a task code but provides task search criteria (title, owner, status, etc.).

**Tools**: `nova_search_user` (if owner specified) → `nova_search_task` → `nova_get_task_obs`

**Steps**:
1. **Resolve owner** (if provided): Call `nova_search_user` to get `userId`.
   - Pick the exact username match; if ambiguous, list candidates and ask the user.
2. **Search tasks**: Call `nova_search_task` with extracted parameters.
   - If multiple tasks are returned, show a task list and ask the user to select one (or confirm to query OBS for all).
   - If only one task matches, proceed directly.
3. **Get OBS**: Call `nova_get_task_obs` for the selected task(s).
4. Display results.

---

## Supported Filters for Task OBS Query

| Filter | Description | Values |
|--------|-------------|--------|
| `isNew` | Filter by new vs. recurring OBS | `-1` = all (default), `1` = new only, `0` = existing/recurring only |
| `isBlock` | Filter by blocking OBS | `-1` = all (default), `1` = blocking only, `0` = non-blocking only |

---

## Task Search Parameters (for Mode 3)

| Parameter | Description | Example Values |
|-----------|-------------|----------------|
| `tasktitle` | Fuzzy match on task title | `nova test`, `regression` |
| `taskcode` | Exact match on task code | `TASK0000041124` |
| `statuss` | Filter by status (array of int) | `[1]` = Testing, `[4]` = Complete |
| `owner` | Filter by owner userId (integer) | resolve via `nova_search_user` |
| `plancodes` | Filter by plan code | `PLN300000009` |
| `startdate` / `enddate` | Date range filter | `2026-01-01` |

### Task Status Codes

| Code | Status |
|------|--------|
| `0` | Draft |
| `1` | Testing |
| `2` | Cancelled |
| `3` | Paused |
| `4` | Complete |
| `5` | Reviewing |
| `6` | Returned |

---

## Output Formats

### OBS Detail Output Format (Mode 1)

**OBS #`{obs_id}` Details:**

| Field | Value |
|-------|-------|
| **OBS ID** | 2464344 |
| **Status** | Open |
| **State** | Under Investigation |
| **Severity** | (if available) |
| **Component** | Embedded Controller 2026 for Nuvolari |
| **Owner** | Weng, Jackey |
| **Originator** | Lan, Yan |
| **Primary Product** | Nuvolari |
| **Date Opened** | 2026-02-10 (27 days open) |
| **Short Description** | [Func-PT][NB][ME][IEC][Nuvolari][PV][PTL][Y91_00.03.00][Flash BIOS]: Can't disable ME when pressing combination key... |

---

### Task OBS Output Format (Mode 2 & 3)

**Task**: `{taskCode}` — {taskTitle}
**Status**: {status} | **Test Lead**: {testLead} | **Date**: {startTime} ~ {endTime}

Found **N** OBS record(s):

| # | OBS ID | Case Title | Status | State | Component | Owner | Platform/Phase | Days Open |
|---|--------|-----------|--------|-------|-----------|-------|----------------|-----------|
| 1 | 2464344 | [SPI] SPI_006 - Flash Descriptor Security Override Test | Open | Under Investigation | Embedded Controller 2026 for Nuvolari | Weng, Jackey | Nuvolari / PV | 27 |

**Short Descriptions:**

1. **OBS 2464344** — `[Func-PT][NB][ME][IEC][Nuvolari][PV][PTL]: Can't disable ME when pressing combination key...`
2. **OBS 2467069** — `[Func-PT][NB][ME][IEC][Merino][PV][PTL][AMT_020]: It will fail at step 165...`

> Total N OBS record(s). Unique OBS count (deduplicated by obs_id): M.

---

## Behavior Notes

- The same `obs_id` may appear multiple times in task OBS results if it is linked to multiple test cases — this is expected. When summarizing, note the total count and the deduplicated unique OBS count.
- Always display **short descriptions** prominently, as users typically want to understand the nature of each defect quickly.
- If `nova_get_task_obs` returns 0 OBS, inform the user and note how many cases were skipped (cases with no OBS).
- When operating in Mode 3 with multiple matching tasks, default to showing the task list first rather than bulk-querying OBS for all tasks simultaneously, unless the user explicitly requests all.
- `owner` passed to `nova_search_task` must be an **integer** userId — always resolve via `nova_search_user` first when an owner name or email is provided.
- Date formats should be `YYYY-MM-DD`.

