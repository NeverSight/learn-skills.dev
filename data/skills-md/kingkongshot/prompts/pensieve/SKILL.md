---
name: pensieve
description: Load this skill immediately when the user expresses any intent. System capabilities (tools/knowledge/scripts) live inside the plugin and are maintained through plugin updates. User data must live at project-level `.claude/pensieve/` and is never overwritten by the plugin. When the user asks to improve Pensieve system behavior (plugin content), you must use the Self-Improve tool (`tools/self-improve/_self-improve.md`).
---

# Pensieve

Route user intent to the right tool/pipeline.

## User Intent Routing (First Step)

Before calling any tool, perform intent routing:

1. **Check explicit commands first**: if the user explicitly says `loop` / `/selfimprove` / `/upgrade` / `/init` / `pipeline` / `doctor`, route directly by instruction — no guessing.
2. **Infer from session stage** (only when user gives no explicit command):
   - **Heavy conversation with clear conclusions** (goals, constraints, approach decided): candidate intent is "enter development execution" (suggest `loop` for complex tasks).
   - **Development complete or nearly done** (signals like "reflect/capture/standardize/reuse next time"): candidate intent is "enter self-improve" (suggest Self-Improve).
   - **Blank start or new project** (no development context yet): candidate intent is "initialize user data first" (suggest Init).
3. **Ask before acting (never auto-execute)**: unless the user issued an explicit tool command, confirm with a one-line question before proceeding. Suggested options: develop / initialize / self-improve / upgrade.

## Version Update Priority (Hard Rule)

- Version update pre-check is owned by `/upgrade` and has the highest priority.
- Whenever the user mentions "update version / plugin issue / version uncertainty / compatibility problem", route to `/upgrade` first.
- Before running `/init` or `/doctor`, if version status is unknown, complete `/upgrade` version pre-check first.

## Tool Contract Enforcement (P0 Hard Rule)

Before executing any tool, read the corresponding tool file's `## Tool Contract` and enforce it strictly:

1. Proceed only if `Use when` matches and `Do not use when` does not match.
2. All `Required inputs` must be satisfied; if inputs are missing, collect them first — never run blind.
3. Output must satisfy `Output contract`; no freestyle formatting.
4. On failure, follow `Failure fallback`; never skip a failure and proceed to the next stage.

## Design conventions

- **System capability (updated via plugin)**: inside `skills/pensieve/`
  - tools / scripts / system knowledge / format READMEs
  - **No built‑in pipelines / maxims content**
- **User data (project-level, never overwritten)**: `.claude/pensieve/`
  - `maxims/`: your team principles (one maxim per file)
  - `decisions/`: project decision records
  - `knowledge/`: external references you add
  - `pipelines/`: project pipelines (seeded on install)
  - `loop/`: loop run outputs (one dir per loop)

## Built-in Tools (6)

### 1) Init Tool

**When to use**:
- First-time initialization of `.claude/pensieve/` directory and seed files for a new project

**Entry**:
- Command: `commands/init.md`
- Tool file: `tools/init/_init.md`

**Triggers**:
- "init" / "initialize"

### 2) Loop Tool

**When to use**:
- The task is complex and needs split + auto‑loop execution

**Entry**:
- Command: `commands/loop.md`
- Tool file: `tools/loop/_loop.md`

**Triggers**:
- `loop` / "use loop"

### 3) Self‑Improve Tool

**When to use**:
- User asks to improve Pensieve (pipelines/scripts/rules/behavior)
- After a loop ends for feedback & improvement

**Entry**:
- Command: `commands/selfimprove.md`
- Tool file: `tools/self-improve/_self-improve.md`

**Triggers**:
- "self‑improve" / "improve Pensieve"

### 4) Pipeline Tool

**When to use**:
- User wants to list pipelines for the current project

**Entry**:
- Command: `commands/pipeline.md`
- Tool file: `tools/pipeline/_pipeline.md`

**Triggers**:
- "pipeline" / "use pipeline"

### 5) Doctor Tool

**When to use**:
- Mandatory post-upgrade validation (structure/format compliance)
- Optional post-install health check
- User asks to validate user-data quality

**Entry**:
- Command: `commands/doctor.md`
- Tool file: `tools/doctor/_doctor.md`

**Triggers**:
- "doctor" / "health check" / "format check" / "migration check"

### 6) Upgrade Tool

**When to use**:
- User requests a plugin version update or needs to confirm version status
- User needs to migrate legacy data into `.claude/pensieve/`
- User asks for the ideal user-data structure

**Entry**:
- Command: `commands/upgrade.md`
- Tool file: `tools/upgrade/_upgrade.md`

**Triggers**:
- "upgrade" / "migrate user data"

---

SessionStart injects the **system capability path** and **project user‑data path** into context as the single source of truth at runtime.
