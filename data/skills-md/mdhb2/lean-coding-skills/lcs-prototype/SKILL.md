---
name: lcs-prototype
description: "Use this skill to build throwaway code answering a specific design question. Trigger on 'prototype', 'proof of concept', 'does this work', 'throwaway', 'quick test', 'validate approach'. Do NOT trigger for: production code (use lcs-task-executor), research (use lcs-research), or architecture review (use lcs-codebase-doc)."
adapters: [claudecode, opencode]
compatibility: [claudecode, opencode]
---

# LCS Prototype Skill

Shared Coding Contract: Refer to `../lcs-shared/contract.md` for folder conventions, Handoff format, and token optimization.

**Purpose:** Build throwaway code to answer a specific design question.

**Chain of Truth Level:** Strict

## OKF Frontmatter & Writing Safety

When creating artifacts, include YAML frontmatter following the schema in `../lcs-shared/contract.md`. Follow Artifact Writing Safety rules: generate content first, write one file, verify, stop on failure.

### Trigger

Activate when user wants to: validate an approach, build a proof of concept, test a design question, or create throwaway code.

### Behavior Checklist

1. **Pick the branch:**
   - "Does the logic/state model feel right?" → **LOGIC branch:** Single HTML file with state panel and free-play buttons.
   - "What will it look like?" → **UI branch:** Multiple variations switchable via URL params.

2. **Rules:**
   - Throwaway by day one. Trivial to run. No persistence by default.
   - Skip polish (no tests, no abstractions).
   - Surface state after every action.

3. Create prototype in `.lcs/work-items/{ts}-{slug}/prototype/`.

4. **Capture the decision:** Once validated, fold the decision into real code/spec. Archive the prototype code as a throwaway git branch. Leave a context pointer in the PRD/SRS.

5. End with Handoff to `lcs-toprd` or `lcs-tosrs`.

### Output

- `.lcs/work-items/{ts}-{slug}/prototype/` — isolated throwaway prototype

## Chain of Truth Report

### Level
Strict

### Sources Checked
- `.lcs/state.md`
- <PRD/explore sections being validated>

### Assumptions
- <label each [verified] or [unverified]>

### Actions Taken
- <Prototype built, branch picked (LOGIC/UI), validation run>

### Verification
- <Prototype ran successfully; decision captured and folded back>

### Report
<Explicit pass/fail on the design question being validated>

## Handoff

Next recommended skill: lcs-toprd or lcs-tosrs
Next file to read: .lcs/work-items/{ts}-{slug}/prototype/
Current phase: prototype
Current confidence: <low/medium/high>
Blocking questions: <list or None>
Risks to carry forward: <summary>
Source of Truth Bundle: .lcs/state.md, prototype/ output
Must Preserve IDs: <SRC/FR/AC IDs touched by the prototype>
Unresolved IDs: <list or None>
Suggested next command: Fold prototype decision ke PRD/SRS

## Chain of Truth Level

Level: Strict

This skill follows the LCS Chain of Truth protocol at the declared level.
