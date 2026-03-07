---
name: go
allowed-tools: Read, Write, Edit, Bash(git checkout:*), Bash(git pull:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git branch:*), Bash(prettier --write:*), Bash(open:*), Bash(gh repo:*), Bash(cp:*), Bash(mkdir -p:*), Bash(date:*), Bash(PLUGIN_DIR:*), Bash(uv run:*), Grep, Glob, Task
argument-hint: "Start: [name] [-b] [-r] [-p] | Resume: -c [choice]"
description: "Execute the ADR-driven 4-phase development workflow (preflight, implementation, formatting, release). Use whenever the user says 'itp go', 'start the workflow', 'implement this feature', 'begin the task', or references the ITP workflow. Also use when the user has an approved plan and wants structured execution with ADR tracking. Do NOT use for simple one-off edits, quick fixes, or tasks that do not need ADR tracking or phased execution."
---

<!-- ⛔⛔⛔ MANDATORY: READ THIS ENTIRE FILE BEFORE ANY ACTION ⛔⛔⛔ -->

# ⛔ ITP Workflow — STOP AND READ

**DO NOT ACT ON ASSUMPTIONS. Read this file first.**

This is a structured workflow command. Follow the phases in order.

Your FIRST and ONLY action right now: **Execute the TodoWrite below.**

## ⛔ MANDATORY FIRST ACTION: Plan-Aware Todo Integration

**YOUR FIRST ACTION MUST BE a MERGED TodoWrite that preserves existing todos.**

<!-- ADR: 2025-12-05-itp-todo-insertion-merge -->

DO NOT:

- ❌ Overwrite existing todos from plan files or previous sessions
- ❌ Ignore the plan file at `~/.claude/plans/*.md`
- ❌ Create your own todos without checking for existing ones
- ❌ Jump to coding without completing Step 0
- ❌ Create a branch before TodoWrite

**Follow the full merge strategy (Steps 0.1-0.5) and TodoWrite template**: [Todo Merge Strategy](./references/todo-merge-strategy.md)

**After TodoWrite completes, proceed to Preflight section below.**

---

## Quick Reference

### Skills Invoked

| Skill                      | Phase     | Purpose                         |
| -------------------------- | --------- | ------------------------------- |
| `implement-plan-preflight` | Preflight | ADR + Design Spec creation      |
| `adr-graph-easy-architect` | Preflight | Architecture diagrams           |
| `impl-standards`           | Phase 1   | Error handling, constants       |
| `mise-configuration`       | Phase 1   | Env var centralization patterns |
| `adr-code-traceability`    | Phase 1   | Code-to-ADR references          |
| `code-hardcode-audit`      | Phase 1   | Pre-release validation          |
| `semantic-release`         | Phase 3   | Version tagging + release       |
| `pypi-doppler`             | Phase 3   | PyPI publishing (if applicable) |

### File Locations

| Artifact    | Path                                 | Notes                                |
| ----------- | ------------------------------------ | ------------------------------------ |
| ADR         | `/docs/adr/$ADR_ID.md`               | Permanent                            |
| Design Spec | `/docs/design/$ADR_ID/spec.md`       | Permanent, SSoT after Preflight      |
| Global Plan | `~/.claude/plans/<adj-verb-noun>.md` | **EPHEMERAL** - replaced on new plan |

### Spec YAML Frontmatter

```yaml
---
adr: YYYY-MM-DD-slug # Links to ADR (programmatic)
source: ~/.claude/plans/<adj-verb-noun>.md # Global plan (EPHEMERAL)
implementation-status: in_progress # in_progress | blocked | completed | abandoned
phase: preflight # preflight | phase-1 | phase-2 | phase-3
last-updated: YYYY-MM-DD
---
```

**Note**: The `source` field preserves the global plan filename for traceability, but the file may no longer exist after a new plan is created.

### ADR ID Format

```
ADR_ID="$(date +%Y-%m-%d)-<slug>"
```

Example: `2025-12-01-clickhouse-aws-ohlcv-ingestion`

### Folder Structure

```text
/docs/
  adr/
    YYYY-MM-DD-slug.md          # ADR file
  design/
    YYYY-MM-DD-slug/            # Design folder (1:1 with ADR)
      spec.md                   # Active implementation spec (SSoT)
```

**Naming Rule**: Use exact same `YYYY-MM-DD-slug` for both ADR and Design folder.

---

## CRITICAL: Mandatory Workflow Execution

**THIS WORKFLOW IS NON-NEGOTIABLE. DO NOT SKIP ANY PHASE.**

You MUST execute ALL phases in order, regardless of task complexity:

1. **Step 0**: TodoWrite initialization (FIRST ACTION - NO EXCEPTIONS)
2. **Preflight**: ADR + Design Spec creation
3. **Phase 1**: Implementation per spec.md
4. **Phase 2**: Format & Push
5. **Phase 3**: Release (if on main/master)

**FORBIDDEN BEHAVIORS:**

- ❌ Deciding "this is simple, skip the workflow"
- ❌ Jumping directly to implementation without TodoWrite
- ❌ Skipping ADR/Design Spec for "document fixes" or "small changes"
- ❌ Making autonomous judgments to bypass phases

**If the task seems too simple for this workflow**: Stop and ask the user if they want to proceed without `/itp:go`. Do NOT silently skip phases.

---

## Arguments

Parse `$ARGUMENTS` for:

| Argument     | Short | Description                                                       | Default                         |
| ------------ | ----- | ----------------------------------------------------------------- | ------------------------------- |
| `slug`       | -     | Feature name for ADR ID (e.g., `clickhouse-aws-ohlcv-ingestion`)  | Derive from Global Plan context |
| `--branch`   | `-b`  | Create branch `{type}/{adr-id}` from main/master                  | Work on current branch          |
| `--continue` | `-c`  | Continue in-progress work; optionally provide decision            | Last "Recommended Next Steps"   |
| `--release`  | `-r`  | Enable semantic-release in Phase 3 (required on main for release) | Skip Phase 3 release            |
| `--publish`  | `-p`  | Enable PyPI publishing in Phase 3 (required on main for publish)  | Skip Phase 3 publish            |

**Detailed usage examples, branch types, and slug derivation rules**: [Arguments Reference](./references/arguments-reference.md)

---

## Workflow Preview

**Detect branch and show expected workflow before starting.** See [Workflow Preview](./references/workflow-preview.md) for the branch detection script and condition table.

---

## Step 0: Initialize Todo List (ALREADY DONE)

**If you followed the STOP instruction at the top, this step is complete.**

The TodoWrite template is in the [Todo Merge Strategy](./references/todo-merge-strategy.md). If you haven't executed it yet, **STOP and go back to the top**.

**Mark each todo `in_progress` before starting, `completed` when done.**

### Preflight Gate (MANDATORY)

**You CANNOT proceed to Phase 1 until ALL Preflight todos are marked `completed`.**

Before starting "Phase 1: Execute implementation tasks":

1. Verify all `Preflight:` todos show `completed`
2. Verify ADR file exists at `/docs/adr/$ADR_ID.md`
3. Verify design spec exists at `/docs/design/$ADR_ID/spec.md`

If any Preflight item is not complete, **STOP** and complete it first. Do NOT skip ahead.

---

## Preflight: Artifact Setup

**MANDATORY Skill tool call: `implement-plan-preflight`** -- activate NOW before proceeding.

This skill provides detailed ADR and Design Spec creation instructions (MADR 4.0 frontmatter, perspectives taxonomy, validation).

### Preflight Steps (via skill)

1. **P.0**: **Create feature branch FIRST** (if `-b` flag) -- MUST happen before ANY file operations
2. **P.1**: **MANDATORY Skill tool call: `implement-plan-preflight`** -- activate NOW for ADR/spec instructions
3. **P.2**: Create ADR file -- path in [Quick Reference](#file-locations)
4. **P.2.1**: **ADR Diagram Creation (MANDATORY for ALL ADRs)**

   **ALL ADRs require BOTH diagrams -- NO EXCEPTIONS, regardless of task complexity.**
   - INVOKE: **Skill tool call with `adr-graph-easy-architect`** -- triggers diagram workflow
   - CREATE: **Before/After diagram** -- visualizes state change in Context section
   - CREATE: **Architecture diagram** -- visualizes component relationships in Architecture section
   - VERIFY: Confirm BOTH diagrams embedded in ADR before proceeding

   **BLOCKING GATE**: Do NOT proceed to P.3 until BOTH diagrams are verified in ADR.

5. **P.3**: Create design spec -- path in [Quick Reference](#file-locations)
6. **P.4**: Verify checkpoint

**WHY P.0 FIRST**: Files created before `git checkout -b` stay on main/master. Branch must exist before ADR/spec creation.

### Preflight Checkpoint (MANDATORY)

**STOP. Verify artifacts exist before proceeding to Phase 1.** Full checklist and validator script: [Preflight Checkpoint](./references/preflight-checkpoint.md)

---

## Phase 1: Implementation

### 1.1 Resumption Protocol

**Entry point for both fresh starts and continuations.** Full protocol (continuation detection, branch verification, sync checks): [Phase 1 Protocols](./references/phase1-protocols.md#11-resumption-protocol)

### 1.2 Implement the Spec

Execute each task in `spec.md`:

1. Mark current task as `in_progress` in todo list
2. Implement the change
3. Verify it works
4. Update `spec.md` to reflect completion
5. Mark task as `completed`
6. Move to next task

### 1.3 Engineering Standards

**Skill Execution Order** (invoke sequentially, in this order):

1. **`impl-standards`** -- Apply error handling & constants patterns FIRST
2. **`mise-configuration`** -- Centralize config via mise [env] SECOND
3. **`adr-code-traceability`** -- Add ADR references to code THIRD
4. **`code-hardcode-audit`** -- Final audit LAST (before Phase 2)

**MANDATORY Skill tool call: `impl-standards`** -- activate NOW for detailed standards.

**MANDATORY Skill tool call: `mise-configuration`** -- activate when creating/modifying scripts with configurable values.

**MANDATORY Skill tool call: `adr-code-traceability`** -- activate NOW for ADR references in code.

**MANDATORY Skill tool call: `code-hardcode-audit`** -- activate NOW before release.

### 1.4 Decision Capture

When implementation requires a user decision, follow the decision capture protocol: [Decision Capture](./references/phase1-protocols.md#14-decision-capture)

### 1.5 Status Synchronization Protocol

Spec `implementation-status` drives ADR `status` updates. Full sync table and scripts: [Status Sync Protocol](./references/phase1-protocols.md#15-status-synchronization-protocol)

### Phase 1 Success Criteria

- [ ] Implementation complete per spec.md
- [ ] All artifacts synced (ADR <-> spec <-> todo <-> code)
- [ ] New files include `ADR: {adr-id}` in file header
- [ ] Non-obvious changes have inline `ADR:` comments

---

## Phase 2: Format & Push

Execute Prettier formatting, git push, and browser open. Full scripts: [Phase 2 Scripts](./references/phase2-scripts.md)

### Phase 2 Success Criteria

- [ ] Markdown formatted with Prettier
- [ ] Pushed to GitHub
- [ ] Files viewable in browser

---

## Phase 3: Release & Publish (Requires -r or -p Flag on Main)

**Phase 3 requires EXPLICIT flags. It does NOT run automatically.**

For entry gate logic and branch-specific messaging, see [Phase 3 Gate Logic](./references/phase3-gate-logic.md).

### 3.1 Pre-Release Verification

Before releasing:

- [ ] All Success Criteria items in design spec are checked off
- [ ] Status value in design spec is updated (e.g., `Accepted`, `Implemented`)
- [ ] ADR and spec.md are in sync with final implementation
- [ ] Version fields use `semantic-release` patterns (no dynamic versioning)

### 3.2 Semantic Release (if -r flag)

**Condition**: Only execute if `-r` or `--release` flag was provided.

**MANDATORY Skill tool call: `semantic-release`** -- activate NOW for version tagging and release.

- Follow the [Local Release Workflow](../skills/semantic-release/references/local-release-workflow.md)
- Conventional commits -> tag -> release -> changelog -> push

### 3.3 PyPI Publishing (if -p flag)

**Condition**: Only execute if `-p` or `--publish` flag was provided.

Only if package pre-exists on PyPI:

- **MANDATORY Skill tool call: `pypi-doppler`** -- activate NOW to publish

### 3.4 Earthly Pipeline

Use Earthly as canonical pipeline: non-blocking, observability-first, ensure GitHub Release exists, record stats/errors, Pushover alert, wire into GitHub Actions.

### Phase 3 Success Criteria

- [ ] ADR status updated to `accepted` or `implemented`
- [ ] Release completed via semantic-release
- [ ] If feature branch: PR created, Phase 3 skipped

## Troubleshooting

| Issue                  | Cause                        | Solution                                     |
| ---------------------- | ---------------------------- | -------------------------------------------- |
| TodoWrite not found    | Skipped mandatory first step | Start from top of file, execute TodoWrite    |
| ADR file not created   | Preflight incomplete         | Run Skill(itp:implement-plan-preflight)      |
| Branch mismatch        | Working on wrong branch      | Switch to correct branch with `git checkout` |
| Phase 3 skipped        | Not on main/master           | Merge to main first, then run `/itp:go -r`   |
| semantic-release fails | No GITHUB_TOKEN              | Check token with `echo $GITHUB_TOKEN`        |
| Diagram missing        | graph-easy not invoked       | Run Skill(itp:adr-graph-easy-architect)      |
| Spec validation fails  | Missing frontmatter fields   | Check required fields in Quick Reference     |
