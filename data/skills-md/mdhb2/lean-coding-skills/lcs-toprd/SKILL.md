---
name: lcs-toprd
description: 'Use this skill whenever the user asks to produce a lean, implementation-focused PRD from exploration, debug notes, or direct requirements. Trigger on requests to "create PRD", "write PRD", "plan feature", or when user asks for acceptance criteria, test strategy, or technical approach. Prefer concise, developer-ready PRDs that include Affected Areas / Files to limit code reads.'
adapters: [claudecode, opencode]
compatibility: [claudecode, opencode]
---

LCS ToPRD Skill

Shared Coding Contract
- Refer to Shared Coding Workflow Contract in `../lcs-shared/contract.md` for folder conventions, Handoff format, and token optimization.

Purpose
- Create or update prd.md. Keep practical for coding. Include security, performance, acceptance criteria, test strategy. Do NOT interview the user - just synthesize what you already know.

Trigger
- Activate when user requests to "create PRD", "write PRD", "plan feature", or when user asks for acceptance criteria, test strategy, or technical approach.

## OKF Frontmatter & Writing Safety

- When creating `prd.md`, include YAML frontmatter following the schema in `../lcs-shared/contract.md`.
- Follow the Artifact Writing Safety rules in contract.md — generate content first, write one file, verify, stop on failure.


### Trigger

Activate when user requests related to this skill's purpose. See description field in YAML frontmatter for trigger phrases.

Behavior checklist
- Read state.md first when continuing work. Otherwise, locate explore.md or debug.md. **If prd-enhanced.md exists in the work-item directory, read it first** — it contains reviewer-hardened sections. Do not overwrite sections in prd-enhanced.md without explicit user confirmation.
- If `intent.md` exists in the work-item directory, read it. It is the primary source for the problem, intended outcome, constraints, and out-of-scope boundaries. `explore.md` remains the supporting source for findings, evidence, alternatives, assumptions, decisions, and context. Do not blindly restate the user's initial raw request as the problem when `intent.md` establishes a more accurate one. If `intent.md` is absent (historical work item), proceed from `explore.md`/`debug.md` alone.
- Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the PRD, and respect any ADRs in the area you're touching.
- Sketch out the major modules you will need to build or modify to complete the implementation. Actively look for opportunities to extract deep modules that can be tested in isolation. A deep module encapsulates a lot of functionality in a simple, testable interface which rarely changes.
- Ensure PRD uses Affected Areas / Files to limit later code reads.
- Extract every user instruction, explicit constraint, and requirement bullet from explore.md, intent.md, debug.md, and direct user input into SRC-### rows in the Source Requirement Ledger. Do not collapse P0 requirements into summaries.
- If `explore.md` already contains `SRC-###` IDs in its Decision Ledger,
  preserve those IDs exactly in the PRD Source Requirement Ledger.
  Never renumber, replace, or reassign existing `SRC-###` IDs.
  Assign new `SRC-###` IDs only to requirements that are not already represented.
- If `research/` or `wayfinder-map.md` exists in the work-item directory, read them and fold validated findings/decisions into the PRD (Source Context + Source Requirement Ledger).
- If `intent.md` exists, check the drafted PRD against its Problem, Proposed Outcome, Constraints, and Out of Scope. If the PRD introduces behavior that materially conflicts with `intent.md` (e.g. building something explicitly listed in Out of Scope), surface this conflict to the user instead of silently proceeding.
- Write prd.md under .lcs/work-items/{timestamp}-{slug-work-item}/prd.md. Do not create versioned copies.
- Provide clear Acceptance Criteria and Test Strategy (unit/integration/e2e where applicable).
- Add ## Source Requirement Ledger section with SRC-### IDs, P0/P1/P2 priorities, origin, and description.
- Add Review Notes with last reviewed/summary/changes applied.
- End with Handoff recommending lcs-prd-reviewer, including Source of Truth Bundle, Must Preserve IDs, and Unresolved IDs.

## State Synchronization

After successful `prd.md` creation, update `.lcs/state.md`:
- `current_phase: prd`
- `work_items[state.current_work].phase = prd`
- `work_items[state.current_work].updated_at = <current-ISO-timestamp>`
- `timestamp: <current-ISO-timestamp>`
- `last_session_note: Created prd.md for <work-name>`

Prompt templates
- Starter: "Create PRD for <work-name> based on explore.md"
- Minimal PRD ask: "Include objective, scope, requirements, acceptance criteria, test strategy"

PRD Template Structure
Use this template when writing prd.md. Keep concise and implementation-focused.

# PRD: <work-name>

## Problem Statement & Objective
- Problem Statement: <what is the problem from user perspective — align with intent.md Problem if present>
- Objective: <what is the goal, how to solve it>

## Background & Solution
- Background: <why we are doing this, context>
- Solution: <the proposed solution from user perspective>

## Source Context
<links to explore.md, intent.md, debug.md, or other sources>

## Scope & User Stories
<what is included in this scope>

### User Stories
Provide a detailed, numbered list of user stories in this format:
1. As an <actor>, I want a <feature>, so that <benefit>
2. As an <actor>, I want a <feature>, so that <benefit>

## Source Requirement Ledger

Every original user-provided instruction, explicit constraint, and requirement bullet must be represented here. Preserve exact user intent; do not collapse P0 requirements into summaries.

| SRC ID | Priority | Origin | Description |
|---|---|---|---|
| SRC-001 | P0 | user instruction | <exact instruction or faithful atomic paraphrase> |
| SRC-002 | P1 | user instruction | <exact instruction or faithful atomic paraphrase> |

## Non-Goals / Out of Scope
<what is excluded / out of scope — must not silently drop items listed in intent.md Out of Scope>

## Requirements
<functional requirements checklist>

## Technical Approach & Implementation Decisions
- Deep Modules Design: <major modules to build/modify, interfaces to introduce, how they isolate logic>
- Technical decisions: <architecture, libraries, database changes, APIs, specific interactions, schema changes>

*Note: Do NOT include specific file paths or code snippets in this section to prevent them from becoming outdated quickly. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it here and note briefly that it came from a prototype. Trim to decision-rich parts only.*

## Affected Areas / Files
<files and modules that need edits. CRITICAL for LCS token-optimization flow!>

## Security Considerations
<vulnerabilities, authentication, authz>

## Performance Considerations
<latency, database query limits, caching>

## Potential Bugs / Edge Cases
<what could go wrong, validations>

## Acceptance Criteria
- AC-001: <detail>
- AC-002: <detail>

## Test Strategy & Testing Decisions
- Testing decisions: <what makes a good test (only test external behavior, not implementation details), modules to test, prior art in the codebase>
- Unit: <spec>
- Integration: <spec>
- E2E: <spec>

## Review Notes
- Last Reviewed: <date>
- Summary: <summary of revisions>
- Changes Applied: <list of changes>

## Chain of Truth Report
### Level
Standard

### Sources Checked
- `.lcs/state.md`
- `<explore.md or debug.md path>`
- <additional files read>

### Assumptions
- <label each [verified] or [unverified]>

### Plan
1. <Step one>
2. <Step two>

### Actions Taken
<Per-step record of what was done>

### Verification
<Command output or manual review result>

### Report
<Structured summary with confidence rating>



## Testing Seams

Seams at which we will test this feature. Existing seams preferred. The fewer seams across the codebase, the better.

- **Primary seam:** [Highest level public interface]

- **Secondary seams:** [Integration points if needed]

- **New seams needed:** [Propose at highest point possible]
## Handoff
Next recommended skill: lcs-prd-reviewer
Next file to read: .lcs/work-items/{timestamp}-{slug-work-item}/prd.md
Current phase: prd
Current confidence: <low/medium/high>
Blocking questions: <list or None>
Risks to carry forward: <summary>
Source of Truth Bundle: .lcs/state.md, explore.md if present, intent.md if present, debug.md if present, research/ if present, prototype.md if present, wayfinder-map.md if present, prd.md
Must Preserve IDs: SRC-001, SRC-002, ...
Unresolved IDs: <list or None>
Suggested next command: Review and fix prd.md

## Chain of Truth Level

Level: Standard

This skill follows the LCS Chain of Truth protocol at the declared level.
