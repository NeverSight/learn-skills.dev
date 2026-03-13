---
name: capture-work-items
description: Capture requirements, bugs, or issues from free-form input into structured, persistent artifacts. Use when user wants to record a work item quickly without deep validation.
tags: [writing, eng-standards, documentation, workflow]
version: 1.0.0
license: MIT
related_skills: [analyze-requirements, brainstorm-design]
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [capture, quick capture, record bug]
input_schema:
  type: free-form
  description: Raw description of requirement, bug, or issue from user
output_schema:
  type: document-artifact
  description: Structured work item(s) written per path detection
  artifact_type: backlog-item
  path_pattern: docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md (canonical) or docs/backlog/YYYY-MM-DD-{slug}.md (fallback)
  lifecycle: living
---

# Skill: Capture Work Items

## Purpose

Capture requirements, bugs, or issues from free-form input into structured, persistent artifacts. Provide quick structured recording without the deep validation that `analyze-requirements` performs. Align output paths with project documentation structure (e.g. project-documentation-template) and include status tracking for governance.

---

## Core Objective

**Primary Goal**: Transform user-provided requirement, bug, or issue descriptions into structured work items with all required fields and persist them to the project-convention path.

**Success Criteria** (ALL must be met):

1. ✅ **Type identified**: Work item classified as requirement, bug, or issue
2. ✅ **Required fields complete**: All mandatory fields for the type are filled (no inference; ask user when missing)
3. ✅ **Status set**: Initial `status: captured` in front-matter
4. ✅ **Path detected**: Output path chosen per project doc structure (see Path Detection)
5. ✅ **Artifact persisted**: Work item written to the selected path
6. ✅ **User confirmed**: User explicitly confirmed or delegated write

**Acceptance Test**: Can someone or a downstream system read the artifact and understand the full work item and take action without asking clarifying questions?

---

## Scope Boundaries

**This skill handles**:

- Free-form input → Structured work item
- Single or batch capture (batch: confirm per item or batch)
- Output to local Markdown under project-convention path
- Status lifecycle: initial `captured` only (downstream updates `triaged`, `in-progress`, `done`, `blocked`, `cancelled`)

**This skill does NOT handle**:

- Deep requirements clarification or validation → Use `analyze-requirements`
- Design or architecture → Use `brainstorm-design`
- Direct API calls to Zentao/GitHub to create issues (extension point; not required for v1)

**Handoff point**: When artifact is persisted and user confirmed, hand off to `analyze-requirements` if item needs deeper validation, or to process-management/milestones for planning.

---

## Use Cases

- **Quick backlog entry**: User says "record this bug" or "add this requirement" — structure and persist without full analysis.
- **Meeting/email capture**: Extract work items from meeting notes or email and save as structured artifacts.
- **Triage input**: Capture items for later triage and prioritization in milestones or task breakdown.
- **Backlog evidence**: Fill the Backlog gap identified in assess-doc-readiness (e.g. "Backlog: weak — no explicit backlog doc").

---

## Behavior

### Interaction Policy

- **Defaults**: Path from project norms or spec/artifact-contract; type from input
- **Choice options**: One missing-field question at a time; offer choices when applicable
- **Confirm**: Target path when different from default; user confirms before write

### Resolve Project Norms

Before persisting, resolve artifact norms per [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md):

1. Check for `.ai-cortex/artifact-norms.yaml` or `docs/ARTIFACT_NORMS.md`
2. If found, parse path_pattern for `backlog-item` and use project rules
3. If not found, use defaults from [spec/artifact-contract.md](../../spec/artifact-contract.md)

### Path Detection

Choose output path using resolved norms (or contract default):

| Condition | Output path |
| :--- | :--- |
| `docs/process-management/` exists | `docs/process-management/project-board/backlog/YYYY-MM-DD-<slug>.md` |
| Otherwise | `docs/backlog/YYYY-MM-DD-<slug>.md` |

Create subdirectories if they do not exist. Use `YYYY-MM-DD` for today; `<slug>` is kebab-case from title.

### Phase 0: Triage — Identify Type

**Announce at start:** "I'm using the capture-work-items skill to record this work item."

Classify input as:

- **requirement**: New need, feature request, or enhancement
- **bug**: Defect, incorrect behavior, failure to meet specification
- **issue**: Task, improvement, or question (generic work item)

### Phase 1: Extract — Identify Fields

Extract available fields from input. Required fields by type:

| Type | Required fields |
| :--- | :--- |
| requirement | Title, Problem/Need, Acceptance criteria |
| bug | Title, Description, Steps to reproduce, Expected vs Actual, Severity |
| issue | Title, Description, Type (task \| improvement \| question) |

### Phase 2: Prompt — Fill Missing Required Fields

For any missing required field, ask user **one question at a time**. Do not infer or guess.

### Phase 3: Persist — Write Artifact

1. Run Resolve Project Norms, then Path Detection (see above)
2. Confirm target path with user if different from default
3. Write Markdown with YAML front-matter using the appropriate template (see Output Templates)
4. Set `status: captured` in front-matter

### Phase 4: Confirm

Confirm with user that the artifact was written and is complete. Do not commit to version control unless user explicitly requests.

---

## Input & Output

### Input

- Raw description of requirement, bug, or issue from user
- Optional: project context (existing `docs/` structure for path detection)

### Output

Structured work item Markdown file with YAML front-matter. Templates follow.

#### Requirement Template

```markdown
---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: requirement
date: YYYY-MM-DD
status: captured
source: [user|meeting|email]
trace_id: optional
---

# [Title]

## Problem / Need
[Who has what problem; no solution language]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Notes
[Optional]
```

#### Bug Template

```markdown
---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: bug
date: YYYY-MM-DD
status: captured
severity: [critical|major|minor]
---

# [Title]

## Description
[What goes wrong]

## Steps to Reproduce
1. ...
2. ...

## Expected vs Actual
- **Expected**: ...
- **Actual**: ...

## Environment
[Optional]
```

#### Issue Template

```markdown
---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: issue
subtype: [task|improvement|question]
date: YYYY-MM-DD
status: captured
---

# [Title]

## Description
[Content]
```

### Status Lifecycle

The skill sets only `status: captured`. Downstream processes (milestones, promotion-iteration-tasks, run-checkpoint) may update to: `triaged`, `in-progress`, `done`, `blocked`, `cancelled`.

---

## Restrictions

### Hard Boundaries

- **No skipping required fields**: If a required field cannot be inferred, ask the user. Do not leave blanks.
- **No analyze-requirements flow**: Do not run diagnostic states (RA0–RA5). If input is very vague, suggest capture first then hand off to `analyze-requirements`.
- **Confirm path before write**: Avoid overwriting existing files; confirm target path when ambiguous.
- **Path follows project structure**: Use Path Detection rules; do not hard-code a single path.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these** (other skills handle them):

- **Deep requirements validation**: Diagnostic states, problem articulation, scope bounding → Use `analyze-requirements`
- **Design and architecture**: Solutions, alternatives, trade-offs → Use `brainstorm-design`
- **Task breakdown**: Epic/task decomposition, acceptance criteria refinement → Use process-management or implementation planning

**When to stop and hand off**:

- User says "this needs more analysis" → Hand off to `analyze-requirements`
- User says "design this" → Hand off to `brainstorm-design`
- Artifact persisted and confirmed → Hand off complete

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Type identified**: Work item is requirement, bug, or issue
- [ ] **Required fields complete**: All mandatory fields filled (no inference)
- [ ] **Status set**: `status: captured` in front-matter
- [ ] **Path detected**: Output path follows Path Detection rules
- [ ] **Artifact persisted**: File written to selected path
- [ ] **User confirmed**: User confirmed or delegated write

### Process Quality Checks

- [ ] **One question at a time**: Did not overwhelm user with multiple missing-field questions
- [ ] **No solution language in requirements**: Problem/Need describes problem, not implementation
- [ ] **Path creation**: Created `backlog/` subdirectory if needed
- [ ] **Filename convention**: Used YYYY-MM-DD-{slug}.md

### Acceptance Test

**Can someone or a downstream system read the artifact and understand the full work item and take action without asking clarifying questions?**

If NO: Required fields are incomplete. Return to Prompt phase.

If YES: Capture complete. Hand off as needed.

---

## Examples

### Example 1: Bug Capture

**User**: "The login page shows 500 when I use special characters in the password field."

**Agent announces**: "I'm using the capture-work-items skill to record this work item."

**Triage**: Classified as bug.

**Extract**: Title and description present; Steps to reproduce, Expected vs Actual, Severity missing.

**Prompt** (one at a time):

Agent: "What are the exact steps to reproduce this?"

User: "1. Go to /login 2. Enter any username 3. Enter a password with @ or # 4. Click Login"

Agent: "What did you expect vs what actually happened?"

User: "Expected: normal login or validation error. Actual: 500 Internal Server Error."

Agent: "What severity would you assign: critical, major, or minor?"

User: "major."

**Persist**: Path detected — `docs/process-management/` exists. Write to `docs/process-management/project-board/backlog/2026-03-06-login-500-special-chars.md`.

**Confirm**: "Written. Do you want to adjust anything or hand off to triage?"

### Example 2: Requirement Capture — Vague Input

**User**: "We need better error messages."

**Agent announces**: "I'm using the capture-work-items skill to record this work item."

**Triage**: Classified as requirement (could be issue; agent chooses requirement as default for "need").

**Extract**: Title derivable ("Better error messages"); Problem/Need and Acceptance criteria missing.

**Prompt**:

Agent: "Who has this problem and what exactly is wrong with current error messages?"

User: "Our API users get generic 'Something went wrong' with no actionable info."

Agent: "What would 'done' look like — at least one concrete acceptance criterion?"

User: "Error responses should include a code (e.g. ERR_001) and a short human-readable message explaining what went wrong."

**Persist**: Path detected — `docs/process-management/` does not exist. Write to `docs/backlog/2026-03-06-better-error-messages.md`.

**Handoff suggestion**: "This could benefit from deeper validation with analyze-requirements. Proceed with capture only, or hand off for full analysis?"

User: "Capture only for now."

**Confirm**: "Written. Hand off to triage when ready."

### Example 3: Issue Capture — Edge Case (Multiple Items in One Message)

**User**: "Two things: 1) Update the README install section. 2) Add a CONTRIBUTING.md."

**Agent announces**: "I'm using the capture-work-items skill. I see two separate work items. I will capture them one at a time."

**Item 1** — Type: issue (task). Title: "Update README install section". Description: from context. Persist as `2026-03-06-update-readme-install.md`.

**Item 2** — Type: issue (task). Title: "Add CONTRIBUTING.md". Description: from context. Persist as `2026-03-06-add-contributing.md`.

**Confirm**: "Both items captured. Review and adjust if needed."

---

## Appendix: Output contract

This skill produces a **document-artifact** (backlog-item). Each output file MUST conform to:

| Element | Requirement |
| :--- | :--- |
| **Path** | Per Path Detection: `docs/process-management/project-board/backlog/YYYY-MM-DD-<slug>.md` or `docs/backlog/YYYY-MM-DD-<slug>.md` |
| **artifact_type** | `backlog-item` |
| **created_by** | `capture-work-items` |
| **lifecycle** | `living` |
| **type** | `requirement` \| `bug` \| `issue` |
| **status** | `captured` |
| **Required sections** | Per type: requirement (Title, Problem/Need, Acceptance criteria); bug (Title, Description, Steps to reproduce, Expected vs Actual, Severity); issue (Title, Description, subtype) |
