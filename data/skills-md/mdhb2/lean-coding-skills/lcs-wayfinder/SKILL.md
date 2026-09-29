---
name: lcs-wayfinder
description: "Use this skill to plan huge chunks of work with a shared map and decision tickets. Trigger on 'wayfinder', 'map the codebase', 'plan this refactor', 'decision tickets', 'blocked on'. Do NOT trigger for: architecture documentation (use lcs-codebase-doc), onboarding (use lcs-onboarding), or simple tasks (use lcs-task-slicer)."
adapters: [claudecode, opencode]
compatibility: [claudecode, opencode]
---

# LCS Wayfinder Skill

Shared Coding Contract: Refer to `../lcs-shared/contract.md` for folder conventions, Handoff format, and token optimization.

**Purpose:** Plan huge chunks of work with a shared map and decision tickets resolved one at a time.

**Chain of Truth Level:** Strict

## OKF Frontmatter & Writing Safety

When creating artifacts, include YAML frontmatter following the schema in `../lcs-shared/contract.md`. Follow Artifact Writing Safety rules: generate content first, write one file, verify, stop on failure.

### Trigger

Activate when user wants to: map out a large refactor, plan multi-session work, create decision tickets, or navigate blocked work.

### Behavior Checklist

1. **Name the destination:** Run a grilling session to pin down the spec/change. What does "done" look like?

2. **Map the frontier:** Breadth-first fan-out across the codebase space. Surface open decisions — don't solve them yet, just name them.

3. **Create the map:** Write `.lcs/work-items/{ts}-{slug}/wayfinder-map.md`.

4. **Create decision tickets:** Write child files in `.lcs/work-items/{ts}-{slug}/wayfinder-tickets/`. Use YAML frontmatter with `blocked_by` to render dependencies. Every ticket frontmatter MUST follow the OKF status lifecycle (`draft|reviewed|active|archived`, see `../lcs-shared/contract.md` §3):
   - `status: active` — ticket is open / being resolved
   - `status: archived` — ticket is resolved / closed
   Use `artifact_type: wayfinder` and keep `open`/`resolved` vocabulary in the body text only, never in frontmatter.

5. **Resolve incrementally:** Do NOT resolve more than one ticket per session. Record the resolution, set the ticket `status: archived`, update the map.

6. **Handoff:** When the map clears (no open decisions), hand off to `lcs-toprd` to collapse decisions into a buildable plan.

### Output

- `.lcs/work-items/{ts}-{slug}/wayfinder-map.md` — navigation map
- `.lcs/work-items/{ts}-{slug}/wayfinder-tickets/DEC-###.md` — decision tickets

## Chain of Truth Report

### Level
Strict

### Sources Checked
- `.lcs/state.md`
- <Codebase areas mapped>

### Assumptions
- <label each [verified] or [unverified]>

### Actions Taken
- <Map created, decision tickets written, resolutions recorded>

### Verification
- <Map and tickets exist at declared paths>

### Report
<Explicit status of open vs resolved decisions — frontmatter uses OKF lifecycle: open=active, resolved=archived>

## Handoff

Next recommended skill: lcs-toprd
Next file to read: .lcs/work-items/{ts}-{slug}/wayfinder-map.md
Current phase: wayfinder
Current confidence: <low/medium/high>
Blocking questions: <open decision tickets — i.e. DEC-### with frontmatter status: active>
Risks to carry forward: <unresolved decisions>
Source of Truth Bundle: .lcs/state.md, wayfinder-map.md, wayfinder-tickets/
Must Preserve IDs: DEC-###, SRC-### if referenced
Unresolved IDs: <DEC-### tickets with status: active (open)>
Suggested next command: Collapse decisions ke PRD via lcs-toprd

### Note

Wayfinder plans and navigates work during active development. It is not a one-time architecture mapping tool — use `lcs-codebase-doc` for onboarding/learning-oriented codebase mapping.

## Chain of Truth Level

Level: Strict

This skill follows the LCS Chain of Truth protocol at the declared level.
