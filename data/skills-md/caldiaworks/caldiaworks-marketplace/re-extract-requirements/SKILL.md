---
name: re-extract-requirements
version: 0.1.0
description: "Extract EARS requirements from source code and logic diagrams with Doer/Critic verification. Reads targets from manifest.json (Phase 2 output). Produces traceable requirements per component. Language-agnostic with optional language references. Use when: extract requirements, reverse engineer requirements, EARS extraction, re-extract-requirements."
args:
  analysis: required  # Analysis name. Reads targets from docs/reverse/{analysis}/manifest.json
  component: optional  # Specific component to process. If omitted, processes all remaining from manifest
allowed-tools: Read, Grep, Glob, Bash, Write, mcp__serena__find_symbol, mcp__serena__search_for_pattern, mcp__serena__find_referencing_symbols
context: fork
agent: general-purpose
---

# Requirements Extraction — Reverse Engineering Phase 3

Extract system requirements from source code and logic diagrams using EARS notation. This skill reads targets from `manifest.json` (populated by Phase 2) and implements internal Doer/Critic verification within a single execution.

## Three Principles

### 1. Code is Truth
- Requirements reflect ACTUAL code behavior, not intended behavior
- Bugs are documented as requirements with note: `[Suspected Bug]`
- Separate As-Is requirements from Question List

### 2. Traceability to Line
- Every requirement MUST cite `file:line` reference
- Requirements without evidence are rejected as hallucination

### 3. Behavior over Intent
- Requirements describe observable behavior: input → output, side effects
- Use concrete values from code (e.g., "retry 3 times", not "retry several times")

## EARS Notation Types

| Type | Pattern | When to Use |
|:-----|:--------|:------------|
| Ubiquitous | System SHALL [action] | Unconditional, always-active behavior |
| Event-driven | WHEN [trigger], system SHALL [action] | Triggered by external input or event |
| Unwanted | IF [condition], system SHALL [action] | Error handling, validation failures |
| State-driven | WHILE [state], system SHALL [action] | Background services, stateful behavior |
| Optional | WHERE [config/feature], system MAY [action] | Configurable or optional behavior |

## Execution

### Step 1: Load Manifest and Determine Targets

Read `docs/reverse/{analysis}/manifest.json`.

Verify:
- `phase2.status` is `"verified"` — if not, report error and stop
- `phase2.targets_for_phase3` contains entries

Determine targets:
- If `component` argument is provided, process only that component
- If omitted, process all entries in `phase3.remaining` (or all targets_for_phase3 if phase3 hasn't started)

Set `phase3.status` to `"in_progress"`.

Load language reference if available.

### Step 2: Doer — Extract Requirements

For each target component:

1. Read the source code file
2. Read the logic diagram from Phase 2 (if available)
3. Systematically scan for each EARS type:

**Ubiquitous** — Scan for unconditional actions:
- No surrounding if/switch/while
- Direct method calls in main flow
- Always-executed logging, persistence

**Event-driven** — Scan for event triggers:
- Request/command handling methods
- Event subscribers, message handlers
- Callback invocations

**Unwanted** — Scan for error conditions:
- Null checks, validation, type guards
- Exception handling (try/catch)
- Error response returns

**State-driven** — Scan for stateful behavior:
- Background service loops
- While conditions with state checks
- Timer-based processing

**Optional** — Scan for configurable behavior:
- Configuration/environment checks
- Feature flags
- Optional logging or processing

For each requirement, record:
- EARS type and requirement statement
- Source reference (`file:line`)
- Evidence (code snippet)
- Concrete values (thresholds, timeouts, error messages)

### Step 3: Critic — Verify Each Requirement

For EVERY extracted requirement:

1. Re-read the source file at the cited line
2. Verify:
   - Line number exists in source file
   - Code at that line matches the requirement description
   - Condition boundaries are correct (>= vs >, == vs !=)
   - Concrete values match exactly
   - No assumed behavior that doesn't exist in code

3. Classify:
   - ✅ **APPROVED**: Verified against source
   - ⚠️ **CORRECTED**: Line number or detail corrected
   - ❌ **REJECTED**: Hallucination — not present in code

Remove rejected requirements. Correct inaccurate ones. Log all decisions.

### Step 4: Generate Output

Write to `docs/reverse/{analysis}/03-requirements-{component}.md`:

```markdown
# EARS Requirements: {component}

**Analysis Date**: {YYYY-MM-DD}
**Source File**: [{file}]({file})
**Requirements Extracted**: {count}
**Verification**: All requirements verified against source

## Requirements Table

| REQ-ID | EARS Type | Requirement | Source | Concrete Values | Notes |
|:-------|:----------|:------------|:-------|:----------------|:------|
| REQ-U001 | Ubiquitous | {statement} | [{file}:{line}]({file}:{line}) | {values} | {notes} |
| REQ-E001 | Event-driven | WHEN {trigger}, system SHALL {action}. | [{file}:{line}]({file}:{line}) | {values} | {notes} |
| REQ-W001 | Unwanted | IF {condition}, system SHALL {action}. | [{file}:{line}]({file}:{line}) | {values} | {notes} |

## Detailed Requirements

### Ubiquitous Requirements

#### REQ-U001: {title}
**Statement**: {EARS statement}

**Source**: [{file}:{line}]({file}:{line})

**Evidence**:
```{language}
// Line {N}
{code snippet}
```

**Concrete Values**: {list of specific values}

**Verification**: ✅ Approved — {brief justification}

---

{repeat for all requirements}

## Verification Log

| REQ-ID | Verdict | Issue | Corrective Action | Evidence |
|:-------|:--------|:------|:-------------------|:---------|
| REQ-U001 | ✅ Approved | — | — | Line {N} verified |
| REQ-E003 | ❌ Rejected | Hallucination | Removed | No validation at L50 |

## Concrete Values Summary

### Thresholds and Constants
| Value Type | Value | Source | Context |
|:-----------|:------|:-------|:--------|

### Error Messages
| Error Type | Message | Source | Trigger |
|:-----------|:--------|:-------|:--------|

### Configuration Keys
| Key | Type | Default | Source | Effect |
|:----|:-----|:--------|:-------|:-------|

## Question List

### Suspected Bugs
- [ ] **{description}** — [{file}:{line}]({file}:{line})

### Unclear Logic
- [ ] **{description}** — [{file}:{line}]({file}:{line})
```

### Step 5: Update Manifest

After each component:
- Add to `phase3.completed`: `{"component": "{name}", "output": "03-requirements-{name}.md", "verification": null}`
- Remove from `phase3.remaining`

After all components:
- Set `phase3.status` to `"completed"`
- Update `updated` timestamp

## Validation Before Completion

- [ ] Every requirement has an EARS type classification
- [ ] Every requirement has a `file:line` source reference
- [ ] All requirements verified by Critic step (re-read source)
- [ ] Verification log documents all approval/rejection decisions
- [ ] Concrete values extracted from code (not guessed)
- [ ] Suspected bugs noted in Question List, not removed from requirements
- [ ] No ambiguous words (appropriate, handle, properly, etc.)

## Prohibited Actions

- Do NOT output requirements as chat response only — MUST create markdown file
- Do NOT add requirements for behavior not present in code
- Do NOT use vague terms ("appropriate", "reasonable", "several")
- Do NOT skip the Critic verification step
- Do NOT publish requirements without line numbers
- Do NOT modify source code files
