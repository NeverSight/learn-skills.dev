---
name: code-no-test
description: '[Implementation] ⚡⚡ Start coding an existing plan (no testing)'
argument-hint: [plan]
---

**MUST READ** `CLAUDE.md` then **THINK HARDER** to start working on the following plan follow the Orchestration Protocol, Core Responsibilities, Subagents Team and Development Rules:
<plan>$ARGUMENTS</plan>

## ⚠️ Anti-Hallucination Reminder

**Before modifying ANY code:** Verify assumptions with actual code evidence. Search for usages, read implementations, trace dependencies. If confidence < 90% on any change, investigate first or ask user. See `.claude/skills/shared/anti-hallucination-protocol.md` for full protocol.

## Summary

**Goal:** Execute an implementation plan without testing phase -- code review and user approval still required.

| Step | Action                     | Key Notes                                        |
| ---- | -------------------------- | ------------------------------------------------ |
| 0    | Plan detection             | Auto-select latest plan or use argument          |
| 1    | Analysis & task extraction | Parse phase file, create TodoWrite tasks         |
| 2    | Implementation             | Code step-by-step, compile to verify             |
| 3    | Code review                | 0 critical issues required -- blocking gate      |
| 4    | User approval              | Blocking gate -- must wait for explicit approval |
| 5    | Finalize                   | Status update, docs, auto-commit                 |

**Key Principles:**

- No testing step -- use when tests are impractical or will be added separately
- Code review still mandatory with code-reviewer subagent
- Must read backend and frontend code patterns before implementation

**⚠️ MUST READ before implementation:**

- `.ai/docs/backend-code-patterns.md` — Backend code patterns
- `.ai/docs/frontend-code-patterns.md` — Frontend code patterns

---

## Role Responsibilities

- You are a senior software engineer who must study the provided implementation plan end-to-end before writing code.
- Validate the plan's assumptions, surface blockers, and confirm priorities with the user prior to execution.
- Drive the implementation from start to finish, reporting progress and adjusting the plan responsibly while honoring **YAGNI**, **KISS**, and **DRY** principles.

**IMPORTANT:** Remind these rules with subagents communication:

- Sacrifice grammar for the sake of concision when writing reports.
- In reports, list any unresolved questions at the end, if any.
- Ensure token efficiency while maintaining high quality.

---

## Step 0: Plan Detection & Phase Selection

**If `$ARGUMENTS` is empty:**

1. Find latest `plan.md` in `./plans` | `ls -t ./plans/**/plan.md 2>/dev/null | head -1`
2. Parse plan for phases and status, auto-select next incomplete (prefer IN_PROGRESS or earliest Planned)

**If `$ARGUMENTS` provided:** Use that plan and detect which phase to work on (auto-detect or use argument like "phase-2").

**Output:** `✓ Step 0: [Plan Name] - [Phase Name]`

**Subagent Pattern (use throughout):**

```
Task(subagent_type="[type]", prompt="[task description]", description="[brief]")
```

---

## Workflow Sequence

**Rules:** Follow steps 1-6 in order. Each step requires output marker starting with "✓ Step N:". Mark each complete in TodoWrite before proceeding. Do not skip steps.

---

## Step 1: Analysis & Task Extraction

Read plan file completely. Map dependencies between tasks. List ambiguities or blockers. Identify required skills/tools and activate from catalog. Parse phase file and extract actionable tasks.

**TodoWrite Initialization & Task Extraction:**

- Initialize TodoWrite with `Step 0: [Plan Name] - [Phase Name]` and all command steps (Step 1 through Step 6)
- Read phase file (e.g., phase-01-preparation.md)
- Look for tasks/steps/phases/sections/numbered/bulleted lists
- MUST convert to TodoWrite tasks:
    - Phase Implementation tasks → Step 2.X (Step 2.1, Step 2.2, etc.)
    - Phase Code Review tasks → Step 3.X (Step 3.1, Step 3.2, etc.)
- Ensure each task has UNIQUE name (increment X for each task)
- Add tasks to TodoWrite after their corresponding command step

**Output:** `✓ Step 1: Found [N] tasks across [M] phases - Ambiguities: [list or "none"]`

Mark Step 1 complete in TodoWrite, mark Step 2 in_progress.

---

## Step 2: Implementation

Implement selected plan phase step-by-step following extracted tasks (Step 2.1, Step 2.2, etc.). Mark tasks complete as done. For UI work, call `ui-ux-designer` subagent: "Implement [feature] UI per ./docs/design-guidelines.md". Use `ai-multimodal` skill for image assets, `imagemagick` for editing. Run type checking and compile to verify no syntax errors.

**Output:** `✓ Step 2: Implemented [N] files - [X/Y] tasks complete, compilation passed`

Mark Step 2 complete in TodoWrite, mark Step 3 in_progress.

---

## Step 3: Code Review

Call `code-reviewer` subagent: "Review changes for plan phase [phase-name]. Check security, performance, architecture, YAGNI/KISS/DRY". If critical issues found: STOP, fix all, re-run `tester` to verify, re-run `code-reviewer`. Repeat until no critical issues.

**Critical issues:** Security vulnerabilities (XSS, SQL injection, OWASP), performance bottlenecks, architectural violations, principle violations.

**Output:** `✓ Step 3: Code reviewed - [0] critical issues`

**Validation:** If critical issues > 0, Step 3 INCOMPLETE - do not proceed.

Mark Step 3 complete in TodoWrite, mark Step 4 in_progress.

---

## Step 4: User Approval ⏸ BLOCKING GATE

Present summary (3-5 bullets): what implemented, code review outcome.

**Ask user explicitly:** "Phase implementation complete. Code reviewed. Approve changes?"

**Stop and wait** - do not output Step 5 content until user responds.

**Output (while waiting):** `⏸ Step 4: WAITING for user approval`

**Output (after approval):** `✓ Step 4: User approved - Ready to complete`

Mark Step 4 complete in TodoWrite, mark Step 5 in_progress.

---

## Step 5: Finalize

**Prerequisites:** User approved in Step 4 (verified above).

1. **STATUS UPDATE - BOTH MANDATORY - PARALLEL EXECUTION:**

- **Call** `project-manager` sub-agent: "Update plan status in [plan-path]. Mark plan phase [phase-name] as DONE with timestamp. Update roadmap."
- **Call** `docs-manager` sub-agent: "Update docs for plan phase [phase-name]. Changed files: [list]."

2. **ONBOARDING CHECK:** Detect onboarding requirements (API keys, env vars, config) + generate summary report with next steps.

3. **AUTO-COMMIT (after steps 1 and 2 completes):**

- Run only if: Steps 1 and 2 successful + User approved + Tests passed
- Auto-stage and commit with message [phase - plan]. Do NOT push unless user explicitly requests

**Validation:** Steps 1 and 2 must complete successfully. Step 3 (auto-commit) runs only if conditions met.

Mark Step 5 complete in TodoWrite.

**Phase workflow finished. Ready for next plan phase.**

---

## Critical Enforcement Rules

**Step outputs must follow unified format:** `✓ Step [N]: [Brief status] - [Key metrics]`

**Examples:**

- Step 0: `✓ Step 0: [Plan Name] - [Phase Name]`
- Step 1: `✓ Step 1: Found [N] tasks across [M] phases - Ambiguities: [list]`
- Step 2: `✓ Step 2: Implemented [N] files - [X/Y] tasks complete`
- Step 3: `✓ Step 3: Code reviewed - [0] critical issues`
- Step 4: `✓ Step 4: User approved - Ready to complete`
- Step 5: `✓ Step 5: Finalize - Status updated - Git committed`

**If any "✓ Step N:" output missing, that step is INCOMPLETE.**

**TodoWrite tracking required:** Initialize at Step 0, mark each step complete before next.

**Mandatory subagent calls:**

- Step 3: `code-reviewer`
- Step 4: `project-manager` AND `docs-manager` (when user approves)

**Blocking gates:**

- Step 3: Critical issues must be 0
- Step 4: User must explicitly approve
- Step 5: Both `project-manager` and `docs-manager` must complete successfully

**REMEMBER:**

- Do not skip steps. Do not proceed if validation fails. Do not assume approval without user response.
- One plan phase per command run. Command focuses on single plan phase only.
- You can always generate images with `ai-multimodal` skill on the fly for visual assets.
- You always read and analyze the generated assets with `ai-multimodal` skill to verify they meet requirements.
- For image editing (removing background, adjusting, cropping), use `media-processing` skill or similar tools as needed.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
