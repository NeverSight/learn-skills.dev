---
name: ship
description: Team-orchestrated implement → verify → fix → archive cycle
user-invocable: true
argument-hint: "[change-name]"
---

Ship a change through team-orchestrated implementation, dual verification, leader-driven fixing, and archival.

**Input**: Optionally specify a change name (e.g., `/opsx:ship my-feature`). If omitted, prompt for selection.

**Team Structure**

| Role | Agent Type | Phase | Responsibility |
|------|-----------|-------|----------------|
| Leader | Main agent (you) | All | Orchestration, OpenSpec verify, direct fix, archive |
| implementer | general-purpose | 1 | Task implementation (apply methodology) |
| reviewer | general-purpose | 2, 3 | Codex code review (spawned on-demand at Phase 2) |

**Steps**

1. **Select the change**

   If name provided, use it. Otherwise run `openspec list --json` and use **AskUserQuestion** to let the user select.

   **IMPORTANT**: Do NOT guess or auto-select. Always let the user choose if not provided.

2. **Verify prerequisites**

   ```bash
   openspec status --change "<name>" --json
   ```

   Confirm the tasks artifact exists. If tasks don't exist, suggest running `/opsx:continue` first and stop.

   **Codex availability check:**

   ```bash
   which codex
   ```

   If `codex` is not installed, use **AskUserQuestion** to present options:
   1. "Install Codex, then re-run `/opsx:ship`" — stop workflow
   2. "Proceed without Codex (OpenSpec verify only, skip code review)" — continue with `CODEX_AVAILABLE=false`
   3. "Abort" — stop workflow

   Store the result as `CODEX_AVAILABLE` (true/false) for use in later phases.

3. **Create team and spawn implementer**

   **TeamCreate**:
   - `team_name`: `ship-<change-name>`
   - `description`: `Ship change: <change-name>`

   Spawn **only the implementer** using the **Task** tool (reviewer is spawned later in Phase 2):

   **implementer** teammate:
   - `subagent_type`: `general-purpose`
   - `team_name`: `ship-<change-name>`
   - `name`: `implementer`
   - `mode`: `bypassPermissions`
   - `run_in_background`: `true`
   - `prompt`:
     ```
     You are the **implementer** in team "ship-CHANGENAME".

     Your job: implement all tasks from OpenSpec change "CHANGENAME".

     ## How to implement

     Read planning artifacts for context:
     - openspec/changes/CHANGENAME/proposal.md — intent and scope
     - openspec/changes/CHANGENAME/design.md — technical approach
     - openspec/changes/CHANGENAME/specs/ — requirements
     - openspec/changes/CHANGENAME/tasks.md — implementation checklist

     Read project patterns from CLAUDE.md.

     For each unchecked task (`- [ ]`) in tasks.md:
     1. Understand the task from context
     2. Make the code changes required
     3. Keep changes minimal and focused
     4. Mark task complete: `- [ ]` → `- [x]`
     5. Send progress to leader via SendMessage: "Task N/M complete: <description>"

     After all tasks complete:
     - Send final summary to leader via SendMessage listing all completed tasks

     ## Workflow

     1. Check TaskList for assigned tasks
     2. When you have an implement task, run the implementation
     3. Send progress updates to leader via SendMessage
     4. Mark TaskList task completed via TaskUpdate
     5. Check TaskList for next work

     IMPORTANT: Follow project patterns from CLAUDE.md.
     IMPORTANT: Always communicate progress to the leader via SendMessage.
     IMPORTANT: If a task is unclear or blocked, report to leader instead of guessing.
     ```

   Replace `CHANGENAME` in the prompt with the actual change name before spawning.

4. **Phase 1: Implement**

   - **TaskCreate**: subject "Implement all tasks for <change-name>"
   - **TaskUpdate**: assign owner to `implementer`
   - **SendMessage** to `implementer`: "Implement all tasks for change <change-name>. Read artifacts, implement each task, mark checkboxes, and send me progress updates."

   Wait for implementer to complete. The implementer will send progress messages and a final summary.

   **Error handling**: If implementer fails or crashes:
   - Read `openspec/changes/<name>/tasks.md` to assess partial progress
   - Report to user: "Implementer failed. N/M tasks completed. Remaining: [list]"
   - Use **AskUserQuestion**: "Continue with leader implementing remaining tasks?" / "Abort and retry later"
   - If user chooses to continue, leader implements remaining tasks directly

   After implementer reports completion:
   - Read tasks.md to verify all checkboxes are checked
   - If incomplete tasks remain, send implementer back to finish them
   - Report progress to user: "Phase 1 complete: N/N tasks implemented"

   **Shutdown implementer immediately after Phase 1:**
   - **SendMessage** type `shutdown_request` to `implementer`
   - Do not wait — proceed to Phase 2 while shutdown processes

5. **Phase 2: Dual Verify**

   **a. Spawn and start reviewer (background, if CODEX_AVAILABLE)**

   Only if `CODEX_AVAILABLE=true`:

   Spawn **reviewer** teammate using the **Task** tool:
   - `subagent_type`: `general-purpose`
   - `team_name`: `ship-<change-name>`
   - `name`: `reviewer`
   - `mode`: `bypassPermissions`
   - `run_in_background`: `true`
   - `prompt`:
     ```
     You are the **reviewer** in team "ship-CHANGENAME".

     Your job: run Codex code review against the implementation for change "CHANGENAME".

     ## How to review

     When you receive a review task:

     1. Read the review prompt template: .codex/prompts/code-review.md
     2. Identify files changed for this change by reading:
        - openspec/changes/CHANGENAME/tasks.md (completed tasks reference files)
        - openspec/changes/CHANGENAME/design.md (affected files listed)
     3. Run Codex review:

        ```bash
        codex exec \
          --dangerously-bypass-approvals-and-sandbox \
          -m gpt-5.3-codex \
          "Review the code changes for OpenSpec change CHANGENAME. Follow the review methodology in .codex/prompts/code-review.md. Read the change artifacts at openspec/changes/CHANGENAME/ for context. Write the full review report."
        ```

     4. Parse the Codex output and write structured review to:
        openspec/changes/CHANGENAME/review-report.md

     5. Send summary to leader via SendMessage:
        Include CRITICAL/WARNING/SUGGESTION counts and overall assessment.

     6. Mark task completed via TaskUpdate
     7. Check TaskList for next work

     ## Output Format

     Write review to: openspec/changes/CHANGENAME/review-report.md

     ```
     # Code Review: CHANGENAME

     ## Summary
     | Dimension       | Finding Count | Max Severity |
     |-----------------|---------------|--------------|
     | Security        | N             | ...          |
     | Performance     | N             | ...          |
     | Correctness     | N             | ...          |
     | Maintainability | N             | ...          |

     ## CRITICAL
     - [finding] — `file.ts:line` — Recommendation: ...

     ## WARNING
     - [finding] — `file.ts:line` — Recommendation: ...

     ## SUGGESTION
     - [finding] — `file.ts:line` — Recommendation: ...

     ## Assessment
     [Summary of overall code quality and readiness]
     ```

     IMPORTANT: Only review, do NOT modify code.
     IMPORTANT: Always communicate results to the leader via SendMessage.
     ```

   Replace `CHANGENAME` in the prompt with the actual change name before spawning.

   Then:
   - **TaskCreate**: subject "Code review for <change-name>"
   - **TaskUpdate**: assign owner to `reviewer`
   - **SendMessage** to `reviewer`: "Run Codex code review for change <change-name>. Write review-report.md and send me the summary."

   **b. Leader runs OpenSpec verify (foreground)**

   Follow the verification methodology from `.claude/commands/opsx/verify.md` (steps 2-8):
   - Read all change artifacts
   - Verify Completeness (task + spec coverage)
   - Verify Correctness (requirement implementation, scenario coverage)
   - Verify Coherence (design adherence, pattern consistency)
   - Write report to `openspec/changes/<name>/verify-report.md`

   **c. Collect and merge results into combined-report.md**

   **If CODEX_AVAILABLE and reviewer completed successfully:**
   - Read both verify-report.md and review-report.md
   - Merge into `openspec/changes/<name>/combined-report.md`:
     - Deduplicate issues appearing in both reports
     - Combine all unique CRITICAL/WARNING/SUGGESTION issues

   **If reviewer failed or CODEX_AVAILABLE=false:**
   - Copy verify-report.md content to `openspec/changes/<name>/combined-report.md`
   - If reviewer failed, report to user: "Codex review failed. Proceeding with OpenSpec verify results only."

   Report to user: "Dual verify complete. CRITICAL: N | WARNING: N | SUGGESTION: N"

   **If 0 CRITICAL + 0 WARNING + 0 SUGGESTION** → skip to **step 8** (archive)
   **If issues found** → proceed to **step 6** (fix loop)

6. **Phase 3: Fix Loop** (max 3 iterations)

   For iteration N = 1, 2, 3:

   **a. Leader directly fixes issues**
   - Read `openspec/changes/<name>/combined-report.md` (always use combined-report as single source of truth)
   - Read change artifacts for context (`design.md`, `specs/`, `tasks.md`)
   - For each CRITICAL, WARNING, and SUGGESTION issue:
     1. Read the referenced source file at the specified `file:line`
     2. Understand the issue in context of change requirements
     3. Apply the minimal, scoped fix
   - Keep changes strictly scoped to reported issues — no refactoring or improvements beyond the fix
   - If a design decision in `design.md` conflicts with code, update the **code** to match design
   - Write fix summary to `openspec/changes/<name>/fix-summary.md`:
     ```
     # Fix Summary: <change-name> (Round N)

     ## Fixes Applied
     ### CRITICAL
     - [issue] → Fixed in `file.ts:line` — [what changed]
     ### WARNING
     - [issue] → Fixed in `file.ts:line` — [what changed]
     ### SUGGESTION
     - [issue] → Fixed in `file.ts:line` — [what changed]

     ## Could Not Fix
     - [issue] — Reason: [explanation]
     ```

   **b. Re-verify and update combined-report.md**

   **Round 1 (leader-only, fast check):**
   - Leader runs OpenSpec verify (steps from verify.md)
   - Update verify-report.md
   - Copy verify-report.md to combined-report.md

   **Round 2+ (smart escalation):**
   - If previous round's combined-report.md still has CRITICAL or WARNING issues AND `CODEX_AVAILABLE=true`:
     - Leader runs OpenSpec verify + Send reviewer to run Codex review again (dual verify)
     - Merge into combined-report.md
   - Otherwise (only SUGGESTION issues remaining, or CODEX_AVAILABLE=false):
     - Leader-only verify
     - Copy verify-report.md to combined-report.md

   **c. Check results**
   - If 0 issues in combined-report.md → go to **step 8** (archive)
   - If N < 3 and issues remain → continue loop (N + 1)
   - If N = 3 and issues remain → go to **step 7**

   Report each round: "Fix Round N complete. CRITICAL: N | WARNING: N | SUGGESTION: N"

7. **Max iterations exceeded**

   Display to user:

   ```
   ## Ship Paused: <change-name>

   3 fix rounds completed, issues remain.

   **Remaining Issues:**
   [paste CRITICAL/WARNING/SUGGESTION from latest combined-report.md]

   **Options:**
   1. Fix manually, then re-run `/opsx:ship`
   2. Archive with warnings: `/opsx:archive <change-name>`
   3. Review full report: openspec/changes/<name>/combined-report.md
   ```

   Proceed to **step 9** (cleanup).

8. **Phase 4: Archive**

   Execute the `/opsx:archive` logic (follow `.claude/commands/opsx/archive.md`):
   - Check artifact completion status
   - Assess delta spec sync state (prompt user for sync choice)
   - Move change to archive directory
   - Display ship completion summary:

   ```
   ## Ship Complete: <change-name>

   **Verification:** All checks passed
   **Fix Rounds:** N/3 used
   **Archived to:** openspec/changes/archive/YYYY-MM-DD-<name>/
   **Specs:** ✓ Synced / No delta specs / Sync skipped
   ```

9. **Phase 5: Cleanup**

   - If `reviewer` is still running: **SendMessage** type `shutdown_request` to `reviewer`
   - Wait for shutdown confirmation (timeout: if no response after 30 seconds, proceed)
   - If shutdown_request fails or times out: log warning and proceed
   - **TeamDelete** to clean up team resources

   **IMPORTANT**: Always run cleanup, even if ship was paused or failed.

**Progress Reporting**

Report progress to user at each phase:

```
## Shipping: <change-name>

✓ Team created: ship-<change-name>
✓ Implementer spawned

── Phase 1: Implement ──
⏳ Implementing tasks...
✓ Task 1/N: <description>
✓ Task 2/N: <description>
✓ All tasks implemented
✓ Implementer shutdown

── Phase 2: Dual Verify ──
⏳ Spawning reviewer...
⏳ OpenSpec verify + Codex review in progress...
CRITICAL: 1 | WARNING: 2 | SUGGESTION: 1

── Phase 3: Fix Loop ──
⏳ Fix Round 1/3...
✓ Fix applied
⏳ Re-verifying...
✓ All checks passed!

── Phase 4: Archive ──
✓ Specs synced
✓ Archived to openspec/changes/archive/YYYY-MM-DD-<name>/

── Phase 5: Cleanup ──
✓ Team shutdown complete

Ship complete!
```

**Guardrails**

- Always prompt for change selection if not provided
- Max 3 fix iterations — hard limit to prevent infinite loops
- Implementer implements, reviewer reviews, leader orchestrates — separation of concerns
- Leader does OpenSpec verify and fixes issues directly (not delegated to teammates)
- Implementer is shut down after Phase 1 to free resources
- Reviewer is spawned on-demand at Phase 2 (not at team creation)
- Codex availability is checked upfront; workflow adapts if unavailable
- Agent failures trigger user-facing options instead of silent failure
- combined-report.md is the single source of truth for fix loop (never reference verify-report.md or review-report.md directly in fix loop)
- Always run cleanup (step 9), even on failure or pause
- All working files preserved in change directory (verify-report.md, review-report.md, combined-report.md, fix-summary.md)
- The reviewer follows `.codex/prompts/code-review.md` for review methodology
- The leader reads `.codex/prompts/verify-fix-loop.md` for fix constraints reference
- The implementer follows apply methodology from `.claude/commands/opsx/apply.md`
