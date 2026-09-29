---
name: lcs-prd-reviewer
description: 'Use this skill whenever the user asks to review, harden, or security-check an existing PRD. Trigger on phrases like "review prd", "audit prd", "harden prd", "security review of prd". This skill aggressively looks for ambiguous acceptance criteria, missing tests, and missing Affected Areas / Files, and writes the hardened/reviewed output to prd-enhanced.md. Do NOT trigger for: creating new PRDs (use lcs-toprd), code review (use lcs-code-review), task execution (use lcs-task-executor), or brainstorming (use lcs-explore). Reviewer hardens existing PRDs, does not create or implement.'
adapters: [claudecode, opencode]
compatibility: [claudecode, opencode]
---

# LCS PRD Reviewer Skill

Shared Coding Contract
- Refer to Shared Coding Workflow Contract in `../lcs-shared/contract.md` for folder conventions, Handoff format, and token optimization.

Purpose
- Review `prd.md`, harden acceptance criteria, test strategy, security, performance, and maintainability.
- Write and save the hardened PRD into `prd-enhanced.md` inside the same work-item directory.

Trigger
- Activate when user requests to "review prd", "audit prd", "harden prd", "security review of prd", or when completing the PRD generation phase.

## OKF Frontmatter & Writing Safety

- When creating `prd-enhanced.md`, include YAML frontmatter following the schema in `../lcs-shared/contract.md`.
- Follow the Artifact Writing Safety rules in contract.md — generate content first, write one file, verify, stop on failure.


### Trigger

Activate when user requests related to this skill's purpose. See description field in YAML frontmatter for trigger phrases.

Behavior checklist
- Read `.lcs/state.md` to identify the active work-item directory: `.lcs/work-items/{timestamp}-{slug-work-item}/`.
- Read `prd.md` inside that active directory.
- If `intent.md` exists in that directory, read it and check `prd.md` for material drift against its Problem, Proposed Outcome, Constraints, and Out of Scope. Flag any conflict under a `## Intent Alignment` note before hardening further.
- Review it for gaps: ambiguous acceptance criteria, missing tests, security, performance, and missing Affected Areas / Files.
- Create or update `prd-enhanced.md` in the same directory with the fully hardened specifications.
- Keep the original `prd.md` intact, but write all improvements and hardenings directly to `prd-enhanced.md`.
- Add `## Preservation Check`. Prove every `SRC-###` from `prd.md` still exists in `prd-enhanced.md`. If a requirement is removed, list it under `## Intentionally Removed` with reason. If a requirement was silently dropped, restore it before finishing.
- Update `Review Notes` section in `prd-enhanced.md` with:
  - Last Reviewed: {timestamp}
  - Summary: <summary of revisions/gaps found>
  - Changes Applied: <improvements written into prd-enhanced.md>
- End with Handoff section pointing to the next logical step (e.g., `lcs-tosrs` for SRS transformation), including Source of Truth Bundle, Must Preserve IDs, and Unresolved IDs.

## State Synchronization

After successful `prd-enhanced.md` creation, update `.lcs/state.md`:
- `current_phase: prd_review`
- `work_items[state.current_work].phase = prd_review`
- `work_items[state.current_work].updated_at = <current-ISO-timestamp>`
- `timestamp: <current-ISO-timestamp>`
- `last_session_note: Hardened prd.md into prd-enhanced.md for <work-name>`

Prompt templates
- Starter: "Review prd.md dan perbaiki menjadi prd-enhanced.md agar siap di-slice"
- Checklist ask: "Apakah acceptance criteria cukup spesifik?"

prd-enhanced.md Structure
Must be exact structure as prd.md:

# PRD: <work-name>

## Objective
<what is the goal>

## Background
<why we are doing this, context>

## Source Context
<links to explore.md, intent.md, debug.md, or other sources>

## Scope
<what is included>

## Non-Goals
<what is excluded>

## Requirements
<functional requirements checklist>

## Technical Approach
<architecture, libraries, database changes, APIs>

## Affected Areas / Files
<files and modules that need edits>

## Security Considerations
<vulnerabilities, authentication, authz>

## Performance Considerations
<latency, database query limits, caching>

## Potential Bugs / Edge Cases
<what could go wrong, validations>

## Acceptance Criteria
- AC 1: <detail>
- AC 2: <detail>

## Intent Alignment
<if intent.md is present: confirm Problem, Proposed Outcome, Constraints, and Out of Scope remain respected. Flag any material drift here rather than silently accepting it.>

## Preservation Check

| SRC ID | Status | Notes |
|---|---|---|
| SRC-001 | preserved | <where/how it appears in enhanced PRD> |
| SRC-002 | enhanced | <what changed while preserving intent> |

## Intentionally Removed

Only list requirements removed after explicit scope decision or contradiction resolution.

| SRC ID | Reason |
|---|---|
| <SRC-### or None> | <reason> |

## Test Strategy
- Unit: <spec>
- Integration: <spec>
- E2E: <spec>

## Review Notes
- Last Reviewed: <date>
- Summary: <summary of revisions>
- Changes Applied: <list of changes>

## Chain of Truth Report
### Level
Strict

### Sources Checked
- `.lcs/state.md`
- `.lcs/work-items/{timestamp}-{slug-work-item}/prd.md` lines {range}
- <additional references>

### Assumptions
- <label each [verified] or [unverified]>

### Plan
<Enumerated steps>

### Actions Taken
<Per-step record>

### Verification
<Automated checks attempted; document every failure>

### Report
<Explicit pass/fail per acceptance criterion>

## Handoff
Next recommended skill: lcs-tosrs
Next file to read: .lcs/work-items/{timestamp}-{slug-work-item}/prd-enhanced.md
Current phase: prd_review
Current confidence: high
Blocking questions: None
Risks to carry forward: <risks>
Source of Truth Bundle: .lcs/state.md, prd.md, prd-enhanced.md, intent.md if present
Must Preserve IDs: SRC-001, SRC-002, ...
Unresolved IDs: <list or None>
Suggested next command: Transform prd-enhanced.md menjadi SRS deterministik (lcs-tosrs)

## Chain of Truth Level

Level: Strict

This skill follows the LCS Chain of Truth protocol at the declared level.
