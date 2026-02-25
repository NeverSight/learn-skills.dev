---
name: review-plan
description: "Review plan.md or a single phase file against templates and codebase compliance. One file per invocation."
argument-hint: "[plan-folder] [phase NN]"
context: fork
agent: general-purpose
model: sonnet
allowed-tools: "Read Grep Glob Write Edit Bash(python*) TaskCreate TaskUpdate TaskList TaskGet"
metadata:
  version: 1.1.0
---

<!-- ultrathink: Enable extended thinking for thorough plan review -->

# Plan Review

**YOUR ARGUMENTS: `$ARGUMENTS`**

Arguments are provided above via `$ARGUMENTS`. Asking the user to re-provide them wastes their time since the data is already available. Parse them and proceed with the review.

Parse the arguments to determine what to review:
- If arguments contain "phase" followed by a number → Review that phase file
- If arguments contain only a folder path → Review plan.md
- The first part is always the plan folder path (e.g., `plans/voice-assistant`)
- A bare number like `11` means `phase 11`

Examples: `plans/voice-assistant` → review plan.md | `plans/voice-assistant phase 11` → review phase-11 | `plans/voice-assistant 11` → review phase-11

**One file per invocation.** Reviewing multiple files causes cognitive overload and superficial results — the user experienced agents ignoring templates when given too many files.

---

## Two-Layer Review

This skill performs two complementary checks:

| Layer | What It Catches | Example |
|-------|----------------|---------|
| **Template Compliance** | Missing sections, incomplete structure | No "Step 0: TDD" section, missing acceptance criteria |
| **Codebase Compliance** | Code blocks that won't compile or violate patterns | Wrong Server Action pattern, missing auth check, bad import paths |

**Why two layers?** Template compliance alone produces "12/12 Ready" verdicts for phases containing compilation-breaking issues. In real reviews, template compliance caught 0 of 26 actual issues. All real problems were codebase compliance — wrong API signatures, missing imports, naming violations, patterns that wouldn't work.

| Issue Type | Template Check | Codebase Check |
|------------|:--------------:|:--------------:|
| Missing section | Caught | N/A |
| Wrong Server Action pattern (missing auth/validation) | Missed | Caught |
| Missing `getSession()` auth check | Missed | Caught |
| Bad import path (wrong alias resolution) | Missed | Caught |
| Schema file in plural `schemas/` not singular `schema/` | Missed | Caught |
| Server action missing account slug resolution | Missed | Caught |
| Exported class instead of factory wrapping private class | Missed | Caught |
| Missing `server-only` import | Missed | Caught |
| Plan says "update documentation" (violates CLAUDE.md) | Missed | Caught |

**Note:** Codebase compliance is skipped for plan.md reviews (only phases contain code blocks).

## Task Tracking

Tasks survive context compacts — skipping this check causes lost progress and repeated work.

Before starting work, run `TaskList` to check if tasks already exist from a previous session or before a compact. If tasks exist:
1. Read existing tasks with `TaskGet` for each task ID
2. Find the first task with status `pending` or `in_progress`
3. Resume from that task — do NOT recreate the task list

If no tasks exist, create them after determining the review type (Step 1):

**Example task list (phase review):**
```
Task 1: Determine review type and read template
Task 2: Read the target phase file
Task 3: Run automated validators
Task 4: Compare against template (section-by-section)
Task 5: Check specific requirements
Task 6: Find reference implementations
Task 7: Codebase compliance check
Task 8: Write review file using template
Task 9: Validate review format
Task 10: Auto-fix Critical/High/Medium issues
Task 11: Return summary with next steps
```

Mark each task `in_progress` when starting and `completed` when done.

## Output Location

Planning reviews go in the `reviews/planning/` subfolder:

**For plan.md review:**
Write to: `{plan-folder}/reviews/planning/plan.md`

**For single phase review:**
Write to: `{plan-folder}/reviews/planning/phase-{NN}.md`

Examples:
- `plans/250202-voice-assistant/reviews/planning/plan.md` (plan.md)
- `plans/250202-voice-assistant/reviews/planning/phase-01.md` (phase 01)
- `plans/250202-voice-assistant/reviews/planning/phase-12.md` (phase 12)

Create the `reviews/planning/` directory if it doesn't exist. You may ONLY write files within the plan folder.

> **Note:** Code/implementation reviews go in `reviews/code/` instead — see `/code-review` skill.

## Workflow

### Step 1: Determine Review Type

Use the arguments parsed at the top of this document:
- No phase specified → Review plan.md
- `phase NN` or bare number specified → Review phase-NN-*.md

### Step 2: Read the Appropriate Template

**For plan.md review:**
Read `../create-plan/references/PLAN-TEMPLATE.md`

**For phase review:**
Read `../create-plan/references/PHASE-TEMPLATE.md`

Extract all required sections from the template.

### Step 3: Read the Target File

**For plan.md review:**
Read `{plan-folder}/plan.md`

**For phase review:**
Find and read `{plan-folder}/phase-{NN}-*.md` (use Glob to find the exact filename)

### Step 4: Compare Against Template

First, run the automated validators to catch structural issues before manual review:

```bash
# Verify required sections exist (for phase files)
echo '{"cwd":"."}' | uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_file_contains.py \
  --directory {plan-folder} --extension .md \
  --contains '## Overview' \
  --contains '## Requirements' \
  --contains '## Implementation Steps' \
  --contains '## Acceptance Criteria'

# Check for skeleton/placeholder content
echo '{"cwd":"."}' | uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_no_placeholders.py \
  --directory {plan-folder} --extension .md

# For phase files: verify TDD ordering
echo '{"cwd":"."}' | uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_tdd_tasks.py \
  --directory {plan-folder} --extension .md
```

Include any validator failures in the review findings as Critical issues.

Then go through the template section-by-section manually:
- Check if each required section exists in the target file
- Note missing sections
- Note incomplete sections (header exists but content missing)

### Step 5: Check Specific Requirements

See [checklist.md](checklist.md) for detailed criteria covering:

- Template structure compliance
- Project framework alignment section (plan.md only)
- Security requirements section (plan.md only)
- Phase constraints — size, dependencies, Step 0 TDD (phase files only)

### Step 6: Identify Phase Type and Find References

**Skip this step for plan.md reviews.**

Classify the phase by its primary deliverable:

| Phase Type | Indicators | Reference Pattern to Search |
|------------|------------|----------------------------|
| **Schema/Database** | Creates tables, migrations, RLS | `supabase/migrations/*.sql` |
| **Service** | Creates `createXxxService()` | `app/home/[account]/**/*service*.ts` |
| **Server Action** | Creates Server Actions with auth + Zod | `app/home/[account]/**/*server-actions*.ts` |
| **Schema (Zod)** | Creates validation schemas | `app/home/[account]/**/*.schema.ts` |
| **UI/Component** | Creates React components, pages | `app/home/[account]/**/_components/*.tsx` |
| **Mixed** | Multiple types | Find reference for each type |

**Find the closest reference implementation:**
1. Use Glob to find 2-3 files matching the phase type pattern
2. Read the most relevant one (prefer files in similar feature areas)
3. This reference is your ground truth for what correct code looks like

Example: For a phase creating server actions, read an existing `*-server-actions.ts` file like `app/home/[account]/feature/_lib/server/server-actions.ts`.

### Step 7: Codebase Compliance Check

**Skip this step for plan.md reviews.**

For each code block in the phase file:

1. **Compare against the reference** from Step 6
2. **Check against the codebase compliance checklist** in [checklist.md](checklist.md)
3. **Flag deviations** with severity (Critical/High/Medium/Low)

**Only flag verifiable deviations.** If you can see the correct pattern in the reference file and the phase code differs, that's a valid finding. Flagging ambiguous or intentional design choices produces noisy reviews that waste the user's time.

**Severity guide:**
- **Critical**: Won't compile or will crash at runtime (wrong function signature, bad imports)
- **High**: Violates security or established patterns (missing auth, wrong RLS, missing permission check)
- **Medium**: Naming/convention violations that cause confusion (wrong file paths, inconsistent naming)
- **Low**: Style issues that don't affect functionality (comment style, ordering)

### Step 8: Read Output Template and Write Review File

Reviews written without reading the template first produce inconsistent formats that the user cannot compare across phases. Read `PLAN-REVIEW-TEMPLATE.md` and follow the exact format specified:
- **Variant A** for plan.md reviews
- **Variant B** for phase reviews

The template defines the exact sections, table columns, and verdict format. Inventing custom formats breaks the user's ability to track review status consistently across phases.

**Write to:**
- Plan.md review: `{plan-folder}/reviews/planning/plan.md`
- Phase review: `{plan-folder}/reviews/planning/phase-{NN}.md`

### Step 8b: Validate Review Format

After writing the review file, run the validation script to catch structural issues:

```bash
python $CLAUDE_PROJECT_DIR/.claude/skills/review-plan/scripts/validate_review.py {review-file-path}
```

The script auto-detects whether this is a plan.md review (Variant A) or phase review (Variant B). If validation fails, fix the reported issues in the review file before proceeding.

### Step 9: Auto-Fix Critical, High, and Medium Issues

**Skip this step for plan.md reviews or if no Critical/High/Medium codebase issues were found.**

**Default: FIX IT.** Most review issues are straightforward pattern corrections. A review that identifies problems but fixes nothing is only half the job — the user depends on auto-fix to save implementation time.

Fix Critical, High, and Medium issues directly in the phase file:

1. For each Critical/High/Medium issue:
   a. Read the reference file cited in the issue (if not already read)
   b. Locate the problem in the phase file
   c. Apply the fix using Edit (for targeted changes) or Write (for larger rewrites)

2. **Examples of fixes to make (never defer these):**
   - Title/phase number mismatches — filename is the source of truth
   - Missing `'use client'` directives in code blocks
   - Wrong import paths or import ordering
   - Wrong file locations (e.g., wrong test directory)
   - Missing code blocks where the review says "should have concrete examples" — write them
   - Wrong function signatures — fix to match the reference
   - Removing documentation update steps — CLAUDE.md prohibits proactive docs
   - Wrong skill references (e.g., `/review-phase` → `/code-review`)
   - Convention violations where the correct pattern is clear from reference
   - "Needs codebase verification" — use your Glob/Grep tools to verify, then fix
   - Medium severity: Pattern deviations where reference shows correct approach
   - Medium severity: Missing code blocks where review says "should have concrete examples"

3. **The ONLY reasons to defer to the main agent** (use sparingly):
   - The fix would change which features the phase delivers (scope change)
   - The fix contradicts an ADR or Decision Log entry
   - You genuinely cannot determine the correct fix even after using Glob/Grep to investigate

4. After fixing, re-read the phase file to verify each fix is correct.

5. Update the review file:
   - Append "(Auto-fixed)" to fixed items in the Issues table
   - Fill in the "Fixes Applied" section (see template)
   - Update the Verdict to reflect only remaining unfixed issues

### Step 10: Return Summary with Next Steps

After writing the review file, return:

- Review file location
- Verdict (Ready/Not Ready) — based on remaining unfixed issues only
- Template score (e.g., "12/12 sections")
- Codebase score (e.g., "3 issues: 1 critical, 2 medium") — phase reviews only
- **Auto-fixed** (count and brief list of what was fixed — includes Critical, High, and Medium)
- **Deferred to main agent** (issues not auto-fixed and why)
- **Next Steps for Low** — present as improvement opportunities (fix unless hallucinated or purely cosmetic)

**Improvement mindset:** When listing Medium/Low issues, frame them as concrete improvements worth doing now — not optional niceties. Phases are rarely revisited after completion, so "fix later" effectively means "never." The user prefers investing in quality now over speed. Suggest specific enhancements that would make the phase better, even if they go slightly beyond strict requirements.

**Action directive for main agent:** If there are deferred items or Medium/Low suggestions, end your summary with:

```
ACTION REQUIRED: [N] deferred items and [M] improvement suggestions need main agent attention.
Please review the items above and fix or discuss with the user before proceeding to implementation.
```

This ensures the main agent acts on the findings rather than just echoing the summary.

## Resuming After Context Compact

If you notice context was compacted or you're unsure of current progress:

1. Run `TaskList` to see all tasks and their status
2. Find the `in_progress` task — that's where you were
3. Run `TaskGet {id}` on that task to read full details
4. Continue from that task — don't restart from the beginning

Tasks persist across compacts. The task list is your source of truth for progress, not your memory.

**Pattern for every work session:**
```
TaskList → find in_progress or first pending → TaskGet → continue work → TaskUpdate (completed) → next task
```

## Constraints

- **ONE file per invocation** — Either plan.md OR one phase file, never both
- NO git commands (you don't have Bash access)
- ONLY write files within the plan folder (review files AND phase file fixes)
- Read the appropriate template before reviewing
- Check EVERY section, not just a sample
- **Codebase compliance**: Read at least one reference file before flagging issues
- **Codebase compliance**: Only flag verifiable deviations (pattern clearly differs from reference)
- **Codebase compliance**: Skipped for plan.md reviews (no code blocks to verify)
- **Auto-fix**: Default is to fix. Only defer for genuine scope changes or ADR contradictions
- **Auto-fix**: Use Glob/Grep to verify before claiming "needs codebase verification" — you have the tools

The user depends on thorough, section-by-section verification AND code block verification. Skimming and saying "looks good" without checking each section causes issues to be discovered during implementation when they're more costly to fix.

## Troubleshooting

### Review Produces "12/12 Ready" But Phase Has Code Issues

**Cause:** Template compliance check passed (all sections exist) but codebase compliance was skipped or superficial.

**Fix:** Ensure Step 6 (Identify Phase Type and Find References) reads an actual codebase file. The reference file is ground truth for what correct code looks like. Without it, code blocks can't be verified.

### Phase File Not Found

**Cause:** Phase number in arguments doesn't match any `phase-{NN}-*.md` file in the plan folder.

**Fix:** Use Glob to list all files in the plan folder: `plans/{folder}/phase-*.md`. Verify the phase number matches the file naming pattern.

### Review File Overwrites Previous Review

**Cause:** Running review twice on the same file without reading the previous review first.

**Fix:** Check if a review file already exists at the output location before writing. If it does, read it first and note what changed since the last review.

## Delegation & Batching

For instructions on spawning multiple review agents in batches, see [delegation.md](delegation.md).
