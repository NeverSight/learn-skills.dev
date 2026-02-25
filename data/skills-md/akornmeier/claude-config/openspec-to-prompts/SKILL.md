---
name: openspec-to-prompts
description: Transform an OpenSpec change phase into UI-ready build prompts through a 3-step pipeline. PRD generation, then UX specification, then build-order prompts. Use when starting implementation of an OpenSpec feature phase, or when the user mentions "openspec-to-prompts", "feature pipeline", or asks to convert a spec phase to implementation prompts. Requires an openspec change-id and phase number as input.
---

# OpenSpec to Prompts Pipeline

Transform an OpenSpec change phase into actionable UI build prompts through a structured 3-step process.

## Overview

This skill orchestrates three sub-skills in sequence:

```
OpenSpec Phase → [prd-lite + prd-clarifier] → [prd-to-ux] → [ux-spec-to-prompts] → Build Prompts
```

**Input:** OpenSpec change-id and phase number
**Output:** Three documents ready for UI generation tools

## When to Use

- Starting implementation of an OpenSpec feature phase
- Converting spec requirements into UI build prompts
- User says "run the feature pipeline" or "openspec-to-prompts"
- User wants to prepare a phase for frontend development

## Required Inputs

Before starting, confirm these inputs with the user:

| Input | Description | Example |
|-------|-------------|---------|
| `change-id` | OpenSpec change directory name | `add-launch-features` |
| `phase` | Section number from tasks.md | `1` (for "1. Pocket Import") |

## Pipeline Execution

### Pre-Flight: Gather Context

Before running the pipeline, read and understand:

1. **Tasks file**: `openspec/changes/{change-id}/tasks.md`
   - Extract the specific phase section (e.g., "## 1. Pocket Import")
   - Note all sub-tasks and requirements

2. **Proposal file**: `openspec/changes/{change-id}/proposal.md`
   - Understand the "Why" and context
   - Note any constraints or dependencies

3. **Spec files**: `openspec/changes/{change-id}/specs/{capability}/spec.md`
   - Read relevant capability specs
   - Extract scenarios and requirements

Create a summary of the phase for use in Step 1.

### Step 1: PRD Generation + Clarification

**Invoke:** `prd-lite` skill, then `prd-clarifier` skill

**Process:**
1. Generate a demo-grade PRD from the phase requirements
2. Run clarification session (recommend "Long" depth = 20 questions)
3. Document all decisions in the clarification session log

**Output file:** `{change-id}/specs/{capability}/{capability}-prd-clarification-session.md`

**Example:** For phase "1. Pocket Import" in change "add-launch-features":
- Output: `add-launch-features/specs/article-import/article-import-prd-clarification-session.md`

### Step 2: UX Specification

**Invoke:** `prd-to-ux` skill

**Process:**
1. Read the clarification session from Step 1
2. Execute all 6 UX passes (NO shortcuts):
   - Pass 1: Mental Model
   - Pass 2: Information Architecture
   - Pass 3: Affordances
   - Pass 4: Cognitive Load
   - Pass 5: State Design
   - Pass 6: Flow Integrity
3. Generate visual specifications

**Output file:** `{prd-clarification-file}-ux-spec.md` (same directory as Step 1 output)

### Step 3: Build-Order Prompts

**Invoke:** `ux-spec-to-prompts` skill

**Process:**
1. Read the UX spec from Step 2
2. Extract atomic buildable units
3. Map dependencies between units
4. Sequence by build order (foundation → components → assembly)
5. Generate self-contained prompts

**Output file:** `{capability}-build-prompts.md` (same directory)

## Output Summary

After completion, report all generated files:

```
Pipeline Complete: {change-id} Phase {phase}

Generated Files:
1. PRD + Clarifications: {path}
2. UX Specification: {path}
3. Build Prompts: {path}

Next Steps:
- Use build prompts with v0, Bolt, or frontend-design skill
- Update tasks.md with any new requirements discovered
- Update spec.md with new scenarios from clarifications
```

## File Naming Convention

All outputs go in the openspec change's specs directory for the relevant capability:

```
openspec/changes/{change-id}/specs/{capability}/
├── spec.md                                          # Original spec (don't modify)
├── {capability}-prd-clarification-session.md        # Step 1 output
├── {capability}-prd-clarification-session-ux-spec.md  # Step 2 output
└── {capability}-build-prompts.md                    # Step 3 output
```

## Determining Capability Name

Map phase numbers to capability names by reading the change's spec structure:

| Phase | tasks.md Section | Likely Capability |
|-------|-----------------|-------------------|
| 1 | "1. Pocket Import" | `article-import` |
| 2 | "2. Browser Extension" | `browser-extension` |
| 3 | "3. Offline Reading" | `offline-reading` |

Check `openspec/changes/{change-id}/specs/` for exact capability directory names.

## Error Handling

| Issue | Resolution |
|-------|------------|
| Phase not found in tasks.md | List available phases, ask user to confirm |
| No specs directory for capability | Create it, or output to change root |
| User wants to skip clarification | Not allowed - clarification prevents implementation bugs |
| User wants fewer than 20 questions | Recommend "Long" but accept "Medium" (10) minimum |

## Important Constraints

1. **No shortcuts** - Each step must complete fully before the next begins
2. **Clarification is mandatory** - The questions prevent costly rework
3. **UX passes are mandatory** - All 6 passes, no skipping to visuals
4. **Self-contained prompts** - Each build prompt must stand alone
5. **Track progress** - Use TodoWrite to show pipeline progress

## Example Invocation

User: "Run openspec-to-prompts for add-launch-features phase 2"

Response:
1. Read tasks.md section "2. Browser Extension"
2. Read proposal.md for context
3. Read specs/browser-extension/spec.md for requirements
4. Invoke prd-lite → generate PRD
5. Invoke prd-clarifier → clarification questions (Long depth)
6. Invoke prd-to-ux → 6-pass UX spec
7. Invoke ux-spec-to-prompts → build prompts
8. Report all generated files
