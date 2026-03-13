---
name: codex-code-reviewer
description: Systematic code review workflow using zen mcp's codex tool. Use this skill when the user explicitly requests "use codex to check the code", "check if the recently generated code has any issues", or "check the code after each generation". The skill performs iterative review cycles - checking code quality, presenting issues to the user for approval, applying fixes, and re-checking until no issues remain or maximum iterations (5) are reached.
---

# Codex Code Reviewer

## Overview

This skill provides a systematic, iterative code review workflow powered by zen mcp's codex tool. It automatically checks recently modified code files against project standards (CLAUDE.md requirements), presents identified issues to users for approval, applies fixes, and re-validates until code quality standards are met or the maximum iteration limit is reached.

**Operation Modes:**
- **Interactive Mode (Default)**: Present issues to user, wait for approval before applying fixes
- **Full Automation Mode**: Automatically select and apply all suggested fixes without user approval (activated when user initially requests "full automation" or "complete automation")

## When to Use This Skill

Trigger this skill when the user says:
- "Use codex to check the code"
- "Please help me check if the recently generated code has any issues"
- "Check the code after each generation"
- Similar requests for code quality validation using codex

## Workflow: Iterative Code Review Cycle

### Prerequisites

Before starting the review cycle:

1. ** Read Operation Mode from Context (automation_mode - READ FROM SSOT):**
   - automation_mode definition and constraints: See CLAUDE.md「📚 共享概念速查」
   - **This skill's role**: Skill Layer (read-only), read from context `[AUTOMATION_MODE: true/false]`, true → auto-fix / false → ask user

1a. **Read Coverage Target from Context (coverage_target - READ FROM SSOT):**
   - coverage_target definition and constraints: See CLAUDE.md「📚 共享概念速查」
   - **This skill's role**: Skill Layer (read-only), read from context `[COVERAGE_TARGET: X%]`, validate coverage (≥ target pass, < 70% reject)

2. **Identify Files to Review:**
   - Use `git status` or similar to identify recently modified files
   - **Interactive Mode (automation_mode = false)**: Confirm with user which files should be reviewed
   - **Automated Mode (automation_mode = true)**: Auto-select all recently modified files, log decision to auto_log.md

3. Initialize iteration counter: `current_iteration = 1`
4. Set maximum iterations: `max_iterations = 5`
5. Initialize review tool tracker: `first_review_done = false`
6. **Detect Review Context:**
   - Check if this is **final quality validation** (project completion/final verification)
   - If YES: Enable **Final Validation Mode** (requires minimum 2 passes: codereview + clink)
   - If NO: Use **Standard Review Mode**

### Review Cycle Loop

Execute the following loop until termination conditions are met:

#### Step 1: Select and Invoke Appropriate Review Tool

**Tool Selection Logic:**

```python
if current_iteration == 1 and not first_review_done:
    # First review: Use mcp__zen__codereview
    review_tool = "mcp__zen__codereview"
    first_review_done = True
else:
    # Second and subsequent reviews: Use mcp__zen__clink with codex CLI
    review_tool = "mcp__zen__clink"
```

**A) First Review: Call `mcp__zen__codereview`**

```
Tool: mcp__zen__codereview
Parameters:
- step: Detailed review request (e.g., "Review the following files for code quality, security, performance, and adherence to project standards...")
- step_number: current_iteration
- total_steps: Estimate based on findings (start with 2-3)
- next_step_required: true (initially)
- findings: Document all discovered issues
- relevant_files: [list of recently modified file paths - MUST be absolute full paths]
- review_type: "full" (covers quality, security, performance, architecture)
- model: "codex" (or user-specified model)
- review_validation_type: "external" (for expert validation)
- confidence: Start with "exploring", increase as understanding grows
```

**Important**: Use absolute full paths; follow zen mcp's codereview workflow (2-3 steps); reference `references/quality_standards/README.md` (on-demand loading)

**B) Second and Subsequent Reviews: Call `mcp__zen__clink` with codex CLI**

```
Tool: mcp__zen__clink
Parameters:
- prompt: "Review files for: 1) Code quality 2) Security 3) Performance 4) Architecture 5) Documentation. Categorize by severity (critical/high/medium/low), provide file:line locations and fix recommendations."
- cli_name: "codex"
- role: "code_reviewer"
- files: [absolute full paths]
- continuation_id: [optional, for context continuity]
```

**Important**: Use absolute full paths for `files`; use `continuation_id` for context continuity; supported params: prompt, cli_name, role, files, images, continuation_id

#### Step 2: Present Findings and Decision Making

After codex returns the review results:

1. **Summarize Issues Clearly:**
   - Group by severity (critical/high/medium/low)
   - Provide specific file locations and line numbers
   - Explain the impact of each issue

2. **Decision Making Based on automation_mode (READ FROM CONTEXT):**

   - automation_mode behavior and decision logic: See CLAUDE.md「📚 共享概念速查」and「G11 Automated Repair Skills」
   - `[AUTOMATION_MODE: false]` → Interactive: Ask user approval
   - `[AUTOMATION_MODE: true]` → Automated: Auto-fix Critical/High, conditional Medium, auto-fix Low style issues
   - Output `[Automated Decision Record]` fragments for auto_log.md (collected by router, generated by simple-gemini)

#### Step 3: Apply Fixes

**Interactive Mode**: If user approves
**Automation Mode**: Proceed directly based on auto-decision logic

1. Apply fixes to the identified issues
2. Use appropriate tools (Edit, Write, etc.) to modify code
3. Follow project coding standards from CLAUDE.md
4. Document changes made

**Automation Mode Transparency:**
- auto_log mechanism and format: See CLAUDE.md「📚 共享概念速查 → auto_log」and `skills/shared/auto_log_template.md`
- Example output:
  ```
  [Automated Fix Record]
   Fixed: 3 critical, 2 medium, 1 low | Skipped: 1 medium (business logic)
   1. SQL injection (critical) → Fixed | 2. N+1 query (medium) → Fixed
   3. Variable naming (low) → Fixed | 4. Logic optimization (medium) → Skipped
  ```

#### Step 4: Increment and Validate

```
current_iteration = current_iteration + 1
```

Check termination conditions:

**Standard Review Mode:**
- **Success**: Review tool reports no issues → Exit loop, report success
- **Max iterations reached**: current_iteration > max_iterations → Exit loop, report remaining issues
- **User cancellation**: User declined fixes → Exit loop
- **Continue**: Issues remain and iterations < max_iterations → Go to Step 1

**Final Validation Mode (Project Completion/Final Verification):**
- **Minimum Pass Requirement**: MUST complete at least 2 passes
  - Pass 1: mcp__zen__codereview (first_review_done = true)
  - Pass 2: mcp__zen__clink with codex CLI
- **Early Exit Prevention**:
  - If current_iteration < 2 → MUST continue to Step 1 (even if no issues found)
  - If current_iteration >= 2 AND no issues found in both passes → Exit loop, report success
- **Max iterations reached**: current_iteration > max_iterations → Exit loop, report remaining issues
- **User cancellation**: User declined fixes → Exit loop
- **Continue**: Issues remain OR minimum passes not met → Go to Step 1

### Termination and Reporting

When the cycle terminates, provide a final report:

```
Code Review Completion Report:

Review rounds: X / 5
Reviewed files: [list files]

Tools used:
- Round 1: mcp__zen__codereview (codex workflow validation)
- Round 2: mcp__zen__clink (codex CLI direct analysis)
- Round 3+: mcp__zen__clink (continued)

Final status:
- All issues fixed / Max reviews reached / User cancelled
- [Final Validation Mode] Completed minimum 2 passes / Did not meet minimum 2 pass requirement

Fix summary:
- Fixed issues: X
- Remaining issues: Y (if any)

Recommendations: [next steps]
```

## Code Quality Standards

This skill enforces standards defined in:
- **CLAUDE.md**: Global rules (G1-G11), phase-specific requirements (P1-P4), model development workflow
- **Project-specific**: PROJECTWIKI.md architecture decisions and conventions

Key quality dimensions checked:
1. **Code Quality**: Readability, maintainability, complexity
2. **Security**: Vulnerabilities, sensitive data handling
3. **Performance**: Efficiency, resource usage
4. **Architecture**: Adherence to documented design decisions
5. **Documentation**: Code comments, PROJECTWIKI.md alignment

**Test Coverage Standards (G9 Compliance):**
- coverage_target usage and thresholds: See CLAUDE.md「📚 共享概念速查」

See `references/quality_standards/README.md` for on-demand quality standards (load specific files as needed).

## Best Practices

### For Effective Reviews

1. **Scope Control**: Review recently modified files only (use git diff/status)
2. **Context Preservation**: Maintain continuation_id across review cycles for context continuity
3. **Incremental Fixes**: Address high-severity issues first, then iterate for lower-priority ones
4. **User Communication**: Always explain WHY an issue matters and HOW the fix improves code

### Error Handling

- **Tool Errors**: If `mcp__zen__codereview` fails, report to user and offer manual review
- **Ambiguous Issues**: When codex findings are unclear, seek user clarification before fixing
- **Conflicting Standards**: If global and project-specific CLAUDE.md conflict, prioritize global CLAUDE.md

## Resources

### references/quality_standards/README.md

Quality standards index and on-demand loading guide. Load this reference when:
- Need overview of available quality standards
- Detailed quality criteria are needed

Then load specific standard files as needed:
- `global_rules.md` - G1-G8 全局规则
- `core_principles.md` - 核心开发原则
- `p3_constraints_and_quality.md` - P3执行约束
- `commit_and_quality_gates.md` - Conventional Commits规范
- `error_handling_and_usage.md` - P4错误处理

Use grep patterns to search: `G1|G2|core principles|ethics|reproducible`

## Example Usage

### Example 1: Interactive Mode (Default)

**User**: "Use codex to check the code"

**Workflow**:
1. Identify files: src/features.py, src/model_training.py
2. Read context: `[AUTOMATION_MODE: false]` → Interactive mode
3. Round 1 (`mcp__zen__codereview`): Found 3 issues (1 critical, 1 medium, 1 low)
4. Ask user approval → User: "Yes"
5. Apply fixes
6. Round 2 (`mcp__zen__clink`): No new issues
7. **Result**: All issues fixed in 2/5 rounds

---

### Example 2: Full Automation Mode ⭐

**User Initial Request**: "Full automation, help me develop login functionality, automatically check quality after code completion"

**Main Router**: Detects "full automation" → Sets automation_mode = true

**After code generation, Main Claude invokes codex-code-reviewer with automation_mode = true:**

**Assistant**:
```
Alright, I will use codex to systematically review the just-generated code.

First, let me identify recently modified files...
[Running git status]

Found the following modified files:
- src/auth/login.py
- src/auth/session.py
- tests/test_login.py

Reading context: [AUTOMATION_MODE: true]
Mode: Full automation review (automatically select and apply fixes)

Starting round 1 review...
[Calling mcp__zen__codereview]

Review results:
Found 5 issues:
[Critical] src/auth/login.py:45 - SQL injection risk (critical)
[Critical] src/auth/session.py:23 - Plaintext password storage (critical)
[Medium] src/auth/login.py:78 - Missing exception handling (medium)
[Medium] src/auth/session.py:56 - Performance issue: N+1 query (medium)
[Low] tests/test_login.py:12 - Non-standard test naming (low)

[Full Automation Mode] Auto-decision + fixes applied:

[Automated Fix Record] Fixed: 2 critical, 2 medium, 1 low
1. SQL injection (critical) → Fixed with parameterized queries
2. Plaintext password (critical) → Fixed with bcrypt encryption
3. Exception handling (medium) → Fixed with try-except blocks
4. N+1 query (medium) → Fixed with select_related optimization
5. Test naming (low) → Fixed by renaming to standard convention

Fixes completed. Starting round 2 review...
[Calling mcp__zen__clink with codex CLI]

Review results: No new issues found

Code review complete!
Review rounds: 2 / 5
Tools used:
- Round 1: mcp__zen__codereview
- Round 2: mcp__zen__clink (codex CLI)
Full automation mode: Auto-fixed 5 issues, skipped 0 issues
All issues successfully fixed without user intervention.
```

**Key Differences:** No user approval, auto-decision by severity/safety, transparent logging with rationale, same quality standards

---

### Example 3: Final Validation Mode (Project Completion/Final Quality Verification) ⭐⭐

**User**: "Project is complete, please perform final quality verification"

**Workflow**:
1. Detect: Project completion/final verification → Enable Final Validation Mode (min 2 rounds)
2. Identify files: 5 core files (src + tests)
3. Round 1 (`mcp__zen__codereview`): Found 2 issues (1 medium, 1 low)
4. Ask user approval → User: "Yes" → Apply fixes
5. Round 2 (`mcp__zen__clink` with codex CLI): No new issues
6. **Result**: All issues fixed, minimum 2-round requirement met, quality verification passed

**Key Features:** Mandatory 2+ passes (codereview + clink), early exit prevention, comprehensive validation before release

---

## Notes

- Dual-tool approach: Iteration 1 uses `mcp__zen__codereview`, iteration 2+ uses `mcp__zen__clink` with codex CLI
- Max 5 iterations, CLAUDE.md workflow compatible (P3/P4), three modes: Interactive (default) / Full Automation / Final Validation (2+ passes)
- **automation_mode & auto_log (READ FROM SSOT)**:
  - Definitions and constraints: See CLAUDE.md「📚 共享概念速查」
  - This skill: Skill Layer (read-only), outputs `[Automated Decision Record]` fragments when automation_mode=true
- Final validation mode activated when user mentions "project completion" / "final verification" / "final quality validation"
