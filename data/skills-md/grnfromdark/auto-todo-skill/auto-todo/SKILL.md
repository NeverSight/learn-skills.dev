---
name: auto-todo
description: Use when user says "autotodo", "auto-todo", or needs to convert a requirement document (from auto-requirement or any structured markdown) into a todolist.md for auto-dev pipeline consumption. Bridges requirement docs and executable task lists.
---

# Auto-Todo: Requirement → Executable Task List

## Overview

Convert requirement documents into **auto-dev compatible todolist.md** files through intelligent task decomposition. Reads SG→CD→FR hierarchy (or any structured markdown), decomposes FRs into right-sized tasks, organizes by dependency and phase, and outputs a ready-to-execute task list.

### Pipeline Positioning

```
auto-requirement → **auto-todo** → auto-dev
(产品决策层)         (工程任务层)      (代码实现层)
```

**Decision boundary:** Macro architecture belongs to auto-requirement. Code implementation belongs to auto-dev. **auto-todo owns engineering-level decisions** that affect task structure (e.g., "need DB migration task", "split frontend/backend phases").

<HARD-GATE>
Do NOT write todolist.md until the user has reviewed and approved the task breakdown summary. No shortcutting the review gate.
</HARD-GATE>

## Trigger

Keywords: `autotodo:`, `auto-todo:`, `autotodo`, `auto-todo`

Usage patterns:
- `autotodo: project-name` → auto-discover in `docs/requirements/`
- `autotodo: path/to/requirement.md` → use specified file
- `auto-todo` (no args) → scan for latest requirement doc

## Checklist

Execute these phases **in order**. Create a TodoWrite task for each:

1. **Validate input** — find and validate requirement document
2. **Parse requirement document** — extract hierarchy, FRs, ACs, metadata
3. **Detect project context** — tech stack, existing patterns, constraints
4. **Decompose FRs into tasks** — apply merge/split/pass-through rules
5. **Organize tasks** — dependencies, topological sort, phase grouping
6. **Present review summary** — show summary, get user approval
7. **Generate todolist.md** — write file with backup safety

## Phase 1: Validate Input (FR-018)

1. Resolve the requirement document path:
   - If user provides a path → use it directly
   - If user provides a project name → scan `docs/requirements/` for matching `*-requirement.md`
   - If multiple matches → present selection menu via AskUserQuestion
   - If none found → prompt user to provide path or run auto-requirement first

2. Validate the file:
   - **Hard errors** (abort): file not found, empty file, not readable
   - **Soft warnings** (continue + warn): file >100KB (suggest splitting), non-.md extension
   - On success: proceed silently (no "validation passed" noise)

## Phase 2: Parse Requirement Document (FR-001, FR-003)

Detect input format tier and parse accordingly:

| Tier | Detection | Strategy |
|------|-----------|----------|
| **Tier 1: auto-requirement output** | Has `SG-`, `CD-`, `FR-` IDs with hierarchy | Full structured parse — extract all SG/CD/FR/AC nodes, priorities, dependencies |
| **Tier 2: Structured markdown** | Has `##`/`###` headings with lists, but no FR IDs | Heuristic parse — infer hierarchy from headings, assign synthetic IDs, show "parse receipt" for confirmation |
| **Tier 3: Free-form markdown** | Minimal structure | LLM comprehension — extract key requirements, mark all as `[INFERRED]`, require user confirmation |

**Missing information handling (FR-003):**
- Missing priority → default `Should`, tag `[INFERRED: priority=Should]`
- Missing ACs → generate from FR description, tag `[INFERRED]`
- Missing dependencies → assume none, tag `[INFERRED: no deps]`
- Missing FR title → **hard error**, require user fix
- Batch all inferences for review summary (don't ask one-by-one)

**Large document handling (FR-020):**
- <10 FRs → single-pass processing
- 10-30 FRs → phased loading (parse → decompose → output), discard intermediate raw text
- \>30 FRs → dispatch sub-Agents per CD domain, merge results

## Phase 3: Project Context (FR-007, FR-021)

**Security:** Never read `.env`, `credentials.*`, `*secret*`, or other sensitive files. Use only manifest files (package.json, Cargo.toml, etc.) for detection.

Use Glob/Read to detect project context:

1. **Tech stack detection** — scan for `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, etc. Extract language, framework, **test runner and test command**.
2. **Resolve test command** — this is CRITICAL for auto-dev. Detect from project config (e.g., `npm test`, `pytest tests/ -q`, `go test ./...`). If undetectable, ask user. The test command populates the `## 测试命令` section in output.
3. **Show detection receipt** — brief summary for user to confirm/correct. If nothing detected, ask or skip.
4. **Engineering decisions** — based on requirement NFRs + project context:
   - Requirement says "前后端分离" → create Frontend/Backend phase split
   - Database FRs detected → add DB schema/migration task
   - Test framework found → include test commands in tasks
   - Tag decisions: `[DECISION: based on NFR-xxx / project context]`
   - If decision contradicts requirement doc → flag for user confirmation

## Phase 4: Task Decomposition (FR-002)

Apply the **Granularity Classifier** to each FR. See `references/decision-rules.md` for the full decision tree.

| AC Count | Has Depth Artifacts? | Same-CD small FRs? | → Action |
|----------|---------------------|---------------------|----------|
| ≤2 | No | Yes | **MERGE** candidates |
| ≤2 | No | No | **PASS-THROUGH** |
| 3-5 | No | — | **PASS-THROUGH** |
| 3-5 | Yes | — | **SPLIT** by artifact boundary |
| >5 | No | — | **SPLIT** by AC groups |
| >5 | Yes | — | **SPLIT** by concern |

**Rules:**
- Target granularity: 1 task ≈ 1 auto-dev Card (2-8 hours work)
- Every task gets `traces_to: FR-xxx` field
- FR with no ACs: infer complexity from description, tag `[NO AC - INFERRED]`
- Max 1 additional split round (prevent infinite recursion)
- User can select Fine/Standard/Coarse granularity preset

**Complexity scoring (FR-009):**
```
score = AC_count × 1.0 + depth_artifacts × 3.0 + dependency_fan_out × 0.5
S: score < 3  |  M: score 3-7  |  L: score > 7
Boundary ties round up. No ACs → default M. Tag as [AI estimate].
```

## Phase 5: Task Organization (FR-004, FR-005, FR-006)

### 5a. Dependency Mapping (FR-004)

Rewrite FR-level dependencies to task-level. See `references/decision-rules.md` for the full impact matrix.

Core rules:
- Both pass-through → direct inherit
- Source split → earliest subtask inherits upstream deps
- Target split → depend on latest subtask
- Both merged → internal deps eliminated
- **Cycle detection** → abort with error listing the cycle path

### 5b. Topological Sort (FR-005)

- Sort tasks by dependency graph (topological order)
- Same-level ties → sort by priority: Must > Should > Could
- Identify critical path (longest dependency chain)
- Mark parallelizable tasks

### 5c. Phase Grouping (FR-006)

- Assign tasks to phases (3-7 tasks per phase)
- Grouping strategies: by CD domain, by architecture layer, or by dependency cluster
- No task depends on a task in a later phase
- Phase names derived from CD titles or standard names (Foundation, Core, Integration, Validation)
- Too many tasks in a phase → split; too few → merge with adjacent

## Phase 6: Review & Approval (FR-013, FR-014, FR-017)

**Level 1 Summary** (always shown, <15 lines):
```
📋 Task Breakdown Summary
─────────────────────────
Source: [requirement doc name]
Tech Stack: [detected or "not detected"]
Total: [N] tasks across [M] phases | Critical path: [K] tasks
Complexity: S×[a] M×[b] L×[c]

Phase 1: [Name] ([n] tasks)
Phase 2: [Name] ([n] tasks)
...

⚠️ Inferred items: [count] (details on request)
⚠️ Low confidence tasks: [list] (details on request)

[Enter=Accept | "details"=Show Level 2 | "modify"=Edit | "regenerate"=Redo]
```

**User actions:**
- **Enter/Accept** → proceed to file generation
- **"details"** or **"show phase N"** → Level 2: task list per phase
- **"show T-xx"** → Level 3: full task card content
- **"modify"** → natural language modification (merge/split/regroup/add/delete tasks). Auto-revalidate deps after changes. Confirm before applying.
- **"reset"** → revert to original generation
- **"regenerate"** → redo from Phase 4 with different parameters

## Phase 7: Generate & Write (FR-008, FR-010, FR-012, FR-019)

### File Safety (FR-019)

Before writing:
1. Check if `todolist.md` exists at target path
2. If exists → create backup: `todolist.YYYYMMDD-HHMMSS.md`
3. Ask user: overwrite / new versioned file / view diff
4. Write via temp file → rename (atomic write)

### Output Format

Generate `todolist.md` following the template in `references/todolist-template.md`.

**CRITICAL: The output must include these 3 sections that auto-dev depends on:**

1. **`## 设计文档`** — table with spec doc path(s). auto-dev uses this as `{SPEC_PATH}` for Card generation.
2. **`## 测试命令`** — detected test command in a code block. auto-dev uses this as `{TEST_CMD}` in autodev.sh.
3. **`## 约束`** — extracted from requirement NFRs. auto-dev writes these into system_prompt.md.

Key structure:
```markdown
# [Project] — 执行任务清单

> 唯一需求来源：`[requirement doc path]`
> Generated: [timestamp] by auto-todo
> Tech Stack: [detected stack] | Tasks: [N] | Phases: [M]

---

## 设计文档

| 文件 | 路径 | 用途 |
|------|------|------|
| 需求文档 | `[requirement doc path]` | 产品需求与验收标准的唯一来源 |

## 测试命令

​```bash
[detected test command, e.g., pytest tests/ -q]
​```

## 约束

- [Constraint from NFR, e.g., 向后兼容现有 API]
- [Constraint 2]

---

## Phase A：[Phase Name]

### A-1：[Task Title]
- [任务描述]
- 依赖：none
- 来源：FR-xxx, FR-yyy
- 验证：
  - [ ] [验收标准 1]
  - [ ] [验收标准 2]

---

## 可追溯性矩阵

| FR | Task(s) | Status |
|----|---------|--------|
| FR-001 | A-1 | ✅ Covered |
| FR-002 | A-2, A-3 | ✅ Covered |
| FR-003 | — | ⚠️ UNCOVERED |

Coverage: [X]% ([covered]/[total] Must+Should FRs)
```

### Traceability Matrix (FR-010)

Append at end of todolist.md:
- Map every FR → task(s)
- Flag `[UNCOVERED]` for any Must/Should FR without a task
- Display coverage percentage
- **Target: 100% coverage of Must + Should FRs**

### Final Output

After writing, display:
```
✅ todolist.md generated successfully
   Path: [relative path]
   Tasks: [N] across [M] phases
   Coverage: [X]% of Must+Should FRs
   Processing time: [seconds]s

Next step: Run `autodev: [project-name]` to generate the development pipeline.
```
