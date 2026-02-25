---
name: foundry-spec
description: Spec-first development methodology that creates detailed specifications before coding. Creates structured specs with phases, file-level details, and verification steps. Includes automatic AI review, modification application, and validation.
---

# Spec-Driven Development: Specification Skill

## Overview

`Skill(foundry:foundry-spec)` creates detailed JSON specifications before any code is written. It analyzes the codebase, designs a phased implementation approach, produces structured task hierarchies, and runs automatic quality checks including AI review.

**Core capabilities:**
- Analyze codebase structure using Explore agents and LSP
- Design phased implementation approaches
- Create JSON specifications with task hierarchies
- Define verification steps for each phase
- **Automatic AI review** of specifications
- **Apply review feedback** as modifications
- **Validate and auto-fix** specifications

## Integrated Workflow

This skill follows a **plan-first methodology**. A markdown plan is **MANDATORY** before JSON spec creation, with human approval required after AI review.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  1. Analyze    2. Create Plan    3. Plan Review   4. APPROVAL   5. Create Spec   6. Spec Review   7. Validate │
│  ──────────    ─────────────     ────────────     ───────────   ─────────────    ────────────     ──────────  │
│  Explore/LSP → plan-create   →   plan-review  →  HUMAN GATE →  spec-create  →   spec-review  →  validate-fix │
│  (understand)  (MANDATORY)       (AI feedback)   (approve)     (from plan)      (MANDATORY)     (auto-fix)   │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Flow

> `[x?]`=decision · `(GATE)`=user approval · `→`=sequence · `↻`=loop

```
- **Entry** → UnderstandIntent → Analyze[Explore|LSP]
- **Plan** (MANDATORY)
  - `plan action="create"` → create markdown plan
  - Fill in plan content with analysis results
- **Plan Review** → `plan action="review"`
  - [critical/high?] → Revise plan, re-review
  - ↻ Self-iterate until no critical/high issues remain
  - Present final plan + review summary to user
- **(GATE: approve plan)**
  - Present plan summary + AI review findings to user
  - User must explicitly approve via AskUserQuestion
  - [approved] → continue to spec creation
  - [revise] → ↻ back to plan editing
  - [abort] → **Exit** (no spec created)
- **Spec Creation** → `authoring action="spec-create"`
  - `authoring action="phase-add-bulk"` ↻ per phase
  - `authoring action="spec-update-frontmatter"` → mission/metadata
- **Spec Review** (MANDATORY) → `review action="spec"`
  - [critical/high?] → `review action="parse-feedback"` → fix spec → re-review
  - ↻ Self-iterate until no critical/high issues remain
  - Present final spec + review summary to user
  - (GATE: approve remaining modifications) → `spec action="apply-plan"`
- **Validate** → `spec action="validate"` ↻ [errors?] → `spec action="fix"`
- **Exit** → specs/pending/{spec-id}.json
```

## When to Use This Skill

**Use for:**
- New features or significant functionality additions
- Complex refactoring across multiple files
- API integrations or external service connections
- Architecture changes or system redesigns
- Any task requiring precision and reliability

**Do NOT use for:**
- Simple one-file changes or bug fixes
- Trivial modifications or formatting changes
- Exploratory prototyping or spikes
- Finding next task or tracking progress (use `foundry-implement`)

## MCP Tooling

| Router | Key Actions |
|--------|-------------|
| `authoring` | `spec-create`, `spec-update-frontmatter`, `phase-add-bulk`, `phase-move`, `phase-update-metadata`, `assumption-add`, `assumption-list`, `constraint-add`, `constraint-list`, `risk-add`, `risk-list`, `question-add`, `question-list`, `success-criterion-add`, `success-criteria-list` |
| `spec` | `validate`, `fix`, `apply-plan`, `completeness-check`, `duplicate-detection`, `stats`, `analyze-deps` |
| `review` | `spec`, `parse-feedback`, `list-tools` |
| `task` | `add`, `remove`, `move`, `update-metadata` |

**Critical Rule:** NEVER read spec JSON files directly with `Read()` or shell commands.

## Core Workflow

### Step 1: Understand Intent

Before creating any plan:
- **Core objective**: What is the primary goal?
- **Spec mission**: Single-sentence mission for `metadata.mission`
- **Success criteria**: What defines "done"?
- **Constraints**: What limitations or requirements exist?

### Step 2: Analyze Codebase

Use **Explore subagents** for large codebases (prevents context bloat), or `Glob`/`Grep`/`Read` for targeted lookups.

**LSP-Enhanced Analysis** for refactoring:
- `documentSymbol` - Understand file structure
- `findReferences` - Assess impact (count affected files)
- `goToDefinition` - Navigate to implementations

> See `references/codebase-analysis.md` for detailed patterns.

### Step 3: Create Phase Plan (MANDATORY)

**This step is REQUIRED.** All specifications must begin as markdown plans before JSON conversion.

```bash
mcp__plugin_foundry_foundry-mcp__plan action="create" name="Feature Name"
```

The command creates a template at `specs/.plans/feature-name-YYYY-MM-DD.md` (date is auto-appended). Fill in all sections:
- Mission statement (becomes `metadata.mission`)
- Objectives and success criteria
- Assumptions and constraints
- Phase breakdown with tasks
- Risks, dependencies, and open questions

**After completing the plan:**
1. Run AI review (Step 4)
2. Obtain human approval (Step 5)
3. Then proceed to JSON spec creation (Step 6)

> See `references/phase-authoring.md` for templates and bulk macros.
> See `references/phase-plan-template.md` for the plan structure.

### Step 4: Run AI Review on Plan

After completing the markdown plan, run AI review to catch issues before JSON conversion:

```bash
mcp__plugin_foundry_foundry-mcp__plan action="review" plan_path="specs/.plans/feature-name-YYYY-MM-DD.md"
```

**Review output:** Saved to `specs/.plan-reviews/<plan-name-YYYY-MM-DD>-review.md`

> **Important:** Use the actual `plan_path` returned by the create step — do not hardcode the path.

All 6 dimensions are always assessed: Completeness, Architecture, Sequencing, Feasibility, Risk, Clarity.

**Self-iterate before presenting to user:** Address all critical and high issues yourself:
1. Read the review feedback
2. Revise the plan to address critical/high findings
3. Re-run review
4. Repeat until no critical/high issues remain
5. Then present the clean plan + review summary at the human approval gate

> See `references/ai-review.md` for review output format and iteration workflow.

### Step 5: Human Approval Gate (MANDATORY)

**Before creating the JSON spec, obtain explicit user approval.**

Present to user:
1. Plan summary (mission, phases, task count)
2. What you fixed during self-iteration (critical/high issues resolved)
3. Any remaining medium/low findings for awareness
4. Any unresolved questions or risks

**Use `AskUserQuestion` with options:**
- **"Approve & Create JSON Spec"** - Proceed to Step 6
- **"Revise Plan"** - Return to Step 3 for modifications
- **"Abort"** - Exit without creating spec

**CRITICAL:** Do NOT proceed to JSON spec creation without explicit "Approve" response.

### Step 6: Create JSON Specification (From Approved Plan)

```bash
mcp__plugin_foundry_foundry-mcp__authoring action="spec-create" name="feature-name" template="empty" plan_path="specs/.plans/feature-name-YYYY-MM-DD.md" plan_review_path="specs/.plan-reviews/feature-name-YYYY-MM-DD-review.md"
```

> **Important:** Use the actual paths returned by the create and review steps. The date suffix is auto-generated.

Add phases with tasks:
```bash
mcp__plugin_foundry_foundry-mcp__authoring action="phase-add-bulk" spec_id="{spec-id}" phase='{"title": "Implementation", "description": "Core work"}' tasks='[{"type": "task", "title": "Build core logic", "task_category": "implementation", "file_path": "src/core.py", "acceptance_criteria": ["Workflow works"]}]'
```

Update metadata:
```bash
mcp__plugin_foundry_foundry-mcp__authoring action="spec-update-frontmatter" spec_id="{spec-id}" key="mission" value="Single-sentence objective"
```

### Step 6a: Enrich Spec Metadata (From Approved Plan)

After creating the spec, populate structured metadata extracted from the approved plan:

```bash
# Add constraints from plan
mcp__plugin_foundry_foundry-mcp__authoring action="constraint-add" spec_id="{spec-id}" text="Must maintain backward compatibility with v2 API"

# Add risks from plan
mcp__plugin_foundry_foundry-mcp__authoring action="risk-add" spec_id="{spec-id}" description="OAuth provider rate limits" likelihood="medium" impact="high" mitigation="Implement token caching"

# Add open questions from plan
mcp__plugin_foundry_foundry-mcp__authoring action="question-add" spec_id="{spec-id}" text="Which OAuth scopes are required for the admin flow?"

# Add success criteria from plan
mcp__plugin_foundry_foundry-mcp__authoring action="success-criterion-add" spec_id="{spec-id}" text="All protected endpoints return 401 without valid token"

# Add assumptions
mcp__plugin_foundry_foundry-mcp__authoring action="assumption-add" spec_id="{spec-id}" text="Single GCP project for staging and production"
```

> See `references/metadata-management.md` for full action reference and workflow.
> See `references/json-spec.md` and `references/task-hierarchy.md` for structure details.

### Step 7: Spec Review — Spec-vs-Plan Comparison (MANDATORY)

After spec creation, the spec review compares the JSON spec against its source plan:

```bash
mcp__plugin_foundry_foundry-mcp__review action="spec" spec_id="{spec-id}"
```

> **Action name:** Use `action="spec"` (canonical). The alias `"spec-review"` also works but `"spec"` is preferred.

The spec review compares the JSON spec against its source plan to catch translation gaps — evaluating coverage, fidelity, success criteria mapping, and preservation of constraints, risks, and open questions. The response includes a verdict of `aligned`, `deviation`, or `incomplete`.

**Prerequisites for spec review to succeed:**
- The spec must already be saved to disk (completed by `spec-create` + `phase-add-bulk`)
- The spec's `metadata.plan_path` must point to an existing plan file (set during `spec-create`)
- An AI provider must be available (configured in `foundry-mcp.toml` or environment)

**If the review returns `success: false`:**
1. Check `error_code` in the response — common causes:
   - `SPEC_NOT_FOUND`: Verify `spec_id` is correct via `spec action="list"`
   - `AI_NO_PROVIDER`: Check AI provider configuration
   - `AI_PROVIDER_TIMEOUT`: Retry with a higher `ai_timeout` value
2. Do NOT retry with a different action name — `"spec"` and `"spec-review"` are identical

**Self-iterate before presenting to user:** Address all critical and high issues yourself:
1. Parse review findings via `review action="parse-feedback"`
2. Fix the spec to address critical/high findings (using authoring/task MCP tools)
3. Re-run spec review
4. Repeat until no critical/high issues remain
5. Then present the clean spec + review summary to the user

> See `references/plan-review-workflow.md` for detailed review workflow.
> See `references/plan-review-dimensions.md` for review dimensions.
> See `references/plan-review-consensus.md` for interpreting results.

### Step 8: Apply Modifications (If Needed)

If review finds issues, parse and apply feedback:

```bash
# Parse review feedback into modifications
mcp__plugin_foundry_foundry-mcp__review action="parse-feedback" spec_id="{spec-id}" review_path="path/to/review.md"

# Preview changes (always preview first!)
mcp__plugin_foundry_foundry-mcp__spec action="apply-plan" spec_id="{spec-id}" modifications_file="suggestions.json" dry_run=true

# Apply changes (backup created automatically)
mcp__plugin_foundry_foundry-mcp__spec action="apply-plan" spec_id="{spec-id}" modifications_file="suggestions.json"
```

> See `references/modification-workflow.md` for detailed workflow.
> See `references/modification-operations.md` for operation formats.

### Step 9: Validate Specification

Validate and auto-fix the specification:

```bash
# Validate
mcp__plugin_foundry_foundry-mcp__spec action="validate" spec_id="{spec-id}"

# Auto-fix common issues
mcp__plugin_foundry_foundry-mcp__spec action="fix" spec_id="{spec-id}"

# Re-validate until clean
mcp__plugin_foundry_foundry-mcp__spec action="validate" spec_id="{spec-id}"
```

**Exit codes:**
- 0: Valid (no errors)
- 1: Warnings only
- 2: Errors (run fix)
- 3: File error

> See `references/validation-workflow.md` for detailed workflow.
> See `references/validation-fixes.md` for fix patterns.
> See `references/validation-issues.md` for issue types.

## Phase-First Authoring

Use this approach for efficient spec creation:

**Step 1: Create spec from approved plan**
```bash
mcp__plugin_foundry_foundry-mcp__authoring action="spec-create" name="my-feature" template="empty" plan_path="specs/.plans/my-feature-YYYY-MM-DD.md" plan_review_path="specs/.plan-reviews/my-feature-YYYY-MM-DD-review.md"
```
> **Both `plan_path` and `plan_review_path` are required.** Create these first via `plan action="create"` and `plan action="review"`. Use the actual paths returned by those steps.

**Step 2: Add phases with bulk macro**
```bash
mcp__plugin_foundry_foundry-mcp__authoring action="phase-add-bulk" spec_id="{spec-id}" phase='{"title": "Phase 1"}' tasks='[...]'
```

**Step 3: Fine-tune tasks**
Use modification operations to adjust individual tasks.

**Step 4: Update frontmatter**
```bash
mcp__plugin_foundry_foundry-mcp__authoring action="spec-update-frontmatter" spec_id="{spec-id}" key="mission" value="..."
```

## File Path Policy

For `implementation` or `refactoring` tasks, set `metadata.file_path` to a **real repo-relative path**. Do not guess or use placeholders. If unclear, use `task_category: "investigation"` first.

## Valid Values Reference

### Spec Templates

| Template | Use Case | Required Fields |
|----------|----------|-----------------|
| `empty` | All specs (blank with no phases) | Add phases via `phase-add-bulk` |

### Task Categories

| Category | Requires `file_path` |
|----------|---------------------|
| `investigation` | No |
| `implementation` | **Yes** |
| `refactoring` | **Yes** |
| `decision` | No |
| `research` | No |

### Node Types

| Node Type | `type` Value | Key Fields |
|-----------|--------------|------------|
| Task | `"task"` | `task_category`, `file_path` |
| Research | `"research"` | `research_type`, `blocking_mode`, `query` |
| Verification | `"verify"` | `verification_type` |

> See `references/task-hierarchy.md` for research node patterns and blocking modes.

### Verification Types

| Type | Purpose |
|------|---------|
| `run-tests` | Execute test suite |
| `fidelity` | Compare implementation to spec |
| `manual` | Manual testing checklist |

> **Best Practice:** Every phase should end with a fidelity review task (`verification_type: "fidelity"`). This ensures implementation matches the spec before moving to the next phase. The `foundry-review` skill performs this comparison.

### Task Statuses

| Status | Description |
|--------|-------------|
| `pending` | Not yet started |
| `in_progress` | Currently being worked on |
| `completed` | Finished successfully |
| `blocked` | Cannot proceed |

## Size Guidelines

If >6 phases or >50 tasks, recommend splitting into multiple specs.

## Output Artifacts

1. **JSON spec file** at `specs/pending/{spec-id}.json`
2. **Plan review report** at `specs/.plan-reviews/{plan-name-YYYY-MM-DD}-review.md`
3. **Spec review report** at `specs/.spec-reviews/{spec-id}-spec-review.md`
4. **Validation passed** with no errors

## Detailed Reference

**Planning:**
- Investigation strategies → `references/investigation.md`
- Phase authoring → `references/phase-authoring.md`
- Phase plan template → `references/phase-plan-template.md`
- JSON spec structure → `references/json-spec.md`
- Task hierarchy → `references/task-hierarchy.md`
- Metadata management → `references/metadata-management.md`
- Codebase analysis → `references/codebase-analysis.md`

**Review:**
- Review workflow → `references/plan-review-workflow.md`
- Review dimensions → `references/plan-review-dimensions.md`
- Consensus interpretation → `references/plan-review-consensus.md`

**Modification:**
- Modification workflow → `references/modification-workflow.md`
- Operation formats → `references/modification-operations.md`

**Validation:**
- Validation workflow → `references/validation-workflow.md`
- Fix patterns → `references/validation-fixes.md`
- Issue types → `references/validation-issues.md`

**General:**
- AI review → `references/ai-review.md`
- Troubleshooting → `references/troubleshooting.md`
