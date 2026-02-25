---
name: code-review
description: "Review code for quality, security, and pattern compliance, then auto-fix Critical/High issues. Grounds every finding in actual codebase reference files."
argument-hint: "[path-to-phase-file]"
context: fork
agent: general-purpose
model: sonnet
allowed-tools: "Read Grep Glob Write Edit Bash(git diff*) Bash(git log*) Bash(git show*) Task TaskCreate TaskUpdate TaskList TaskGet"
metadata:
  version: 1.2.0
---

<!-- ultrathink: Enable extended thinking for deep code analysis -->

# Code Review

**YOUR ARGUMENTS: `$ARGUMENTS`**

**DO NOT ask the user for arguments. They are provided above. Parse them NOW and proceed with the review.**

The argument is the path to the phase file to review (e.g., `plans/voice-assistant/phase-01-database-schema.md`).

## Recent Git Activity

Recent commits (helps identify which files were modified for this phase):

!`git log --oneline -10 2>/dev/null || echo "(not a git repository)"`

Recently changed files:

!`git diff --name-only HEAD~5 2>/dev/null || echo "(no recent changes)"`

## Why This Review Exists

The user depends on this review to catch issues before they reach production. Self-review misses problems because the implementer has blind spots about their own code.

**What skipping or rushing this review costs the user:**

| Missed Check | Consequence |
|--------------|-------------|
| Step verification | Features incomplete, user discovers gaps in production |
| Security issues (RLS, credentials) | Data leakage between accounts, security incidents |
| Project pattern compliance | Inconsistent codebase, harder to maintain |
| Codebase pattern deviation | Code works differently from every other feature, confusing to maintain |
| Persistent review record | No audit trail, same mistakes repeated across future phases |

This review creates accountability. Specific file:line references and concrete fixes give the user actionable feedback — not vague "looks good" responses that hide problems.

## Codebase-Grounded Review

This review is **grounded in the actual codebase**, not just a static checklist. Before flagging pattern violations, you read a reference implementation to confirm what the correct pattern looks like. This prevents:

- Flagging things that are actually correct in this codebase
- Missing violations because the checklist is stale
- Giving generic advice instead of specific "line X should match how it's done in file Y"

## Output Location

Code/implementation reviews go in the `reviews/code/` subfolder:

- Phase file: `plans/feature-name/phase-01-slug.md`
- Review file: `plans/feature-name/reviews/code/phase-01.md`

Examples:
- `plans/250202-voice-assistant/reviews/code/phase-01.md`
- `plans/250202-voice-assistant/reviews/code/phase-12.md`

Create the `reviews/code/` directory if it doesn't exist.

> **Note:** Planning/template reviews go in `reviews/planning/` instead — see `/review-plan` skill.

## Delegation & Batching

For instructions on spawning multiple code review agents in batches, see [delegation.md](delegation.md).

## Task Tracking

Tasks survive context compacts — skipping this check causes lost progress and repeated work.

Before starting work, run `TaskList` to check if tasks already exist from a previous session or before a compact. If tasks exist:
1. Read existing tasks with `TaskGet` for each task ID
2. Find the first task with status `pending` or `in_progress`
3. Resume from that task — do NOT recreate the task list

If no tasks exist, create them after Step 2 (identifying files to review):

**Example task list:**
```
Task 1: Read phase document and extract requirements
Task 2: Identify files to review
Task 3: Find reference implementations
Task 4: Run completeness check
Task 5: Run code quality & codebase compliance check
Task 6: Write review file using template
Task 7: Auto-fix Critical and High issues
Task 8: Return summary with next steps
```

Mark each task `in_progress` when starting and `completed` when done.

## Workflow

### Step 1: Read the Phase Document

Read the phase file at the path provided in the arguments above. Extract:

- All Implementation Steps (Step 0 through Step N)
- All Verifiable Acceptance Criteria
- All Functional and Technical Requirements

### Step 2: Identify Files to Review

The user should have provided a file list when invoking. If not, ask which files were modified in this phase. You cannot use git commands.

### Step 3: Find Reference Implementations

**Before reviewing code quality, read at least one reference file from the codebase.** This grounds your review in actual patterns, not memory. Without this step, you risk flagging correct code as violations or missing actual deviations.

Classify the files under review and find a reference for each type:

| File Type | How to Find Reference |
|-----------|----------------------|
| Server actions | Glob: `app/home/[account]/**/*server-actions*.ts` — read one |
| Service files | Glob: `app/home/[account]/**/*service*.ts` — read one |
| Zod schemas | Glob: `app/home/[account]/**/*.schema.ts` — read one |
| SQL migrations | Glob: `supabase/migrations/*.sql` — read a recent one |
| React components | Glob: `app/home/[account]/**/_components/*.tsx` — read one |
| Page files | Glob: `app/home/[account]/**/page.tsx` — read one |
| Test files | Glob: `__tests__/**/*.test.ts` — read one |

**Read the reference file.** This is your ground truth for:
- Function signatures (e.g., Server Action auth pattern)
- Import paths and sources
- Naming conventions
- File organization
- Error handling patterns

**Complete this step before Step 5.** Flagging pattern violations without first confirming the correct pattern from a real file leads to false positives that waste the user's time.

### Step 4: Completeness Check

Verify every section in the phase document was implemented. See [checklist.md](checklist.md) for detailed criteria.

### Step 5: Code Quality & Codebase Compliance Check

Review the files against project patterns, security requirements, AND the reference implementations from Step 3. See [checklist.md](checklist.md) for detailed criteria.

For each file under review:
1. Compare its patterns against the reference from Step 3
2. Check against the codebase compliance checklist in [checklist.md](checklist.md)
3. Flag deviations with severity and specific file:line references

**When flagging an issue, cite the reference:** "Line 42 uses `async (data) =>` but reference file `claude-ai-server-actions.ts:65` shows `async (data, user) =>` is required when `auth: true`."

**For React/Next.js Code: Load Performance Guidelines**

If reviewing React components, Next.js pages, or frontend code, invoke:

```
/vercel-react-best-practices
```

This loads 57 performance rules. Check the code against CRITICAL and HIGH priority rules:

**CRITICAL - Eliminating Waterfalls:**
- No sequential awaits for independent operations (use Promise.all)
- Suspense boundaries for streaming content
- Early promise initiation in API routes

**CRITICAL - Bundle Optimization:**
- No barrel file imports (import directly from source)
- Heavy components use next/dynamic
- Third-party scripts deferred after hydration

**HIGH - Server-Side Performance:**
- React.cache() for per-request deduplication
- Minimal data serialization to client components
- Parallel data fetching in server components

**MEDIUM - Re-render Optimization:**
- Derived state computed during render, not useEffect
- Memoization for expensive computations
- useTransition for non-urgent updates

Flag violations in the appropriate priority section of the review.

### Step 6: Read Output Template and Write Review File

**Read the output template BEFORE writing the review.**

Reviews written without reading the template first produce inconsistent formats that the user cannot compare across phases. Read `references/CODE-REVIEW-TEMPLATE.md` and follow the exact format specified.

The template defines the exact sections, table columns, and verdict format. Inventing custom formats, adding extra sections like "Positive Observations" or "Technical Excellence", or using emoji checkmarks breaks the user's ability to track review status consistently across phases.

**Write to:** `{plan-folder}/reviews/code/phase-{NN}.md`

### Step 6b: Validate Review Format

After writing the review file, run the validation script to catch structural issues:

```bash
python $CLAUDE_PROJECT_DIR/.claude/skills/code-review/scripts/validate_review.py {review-file-path}
```

If validation fails, fix the reported issues in the review file before proceeding. The script checks for missing sections, incorrect table formats, and forbidden patterns (like "Positive Observations" sections that aren't in the template).

### Step 7: Auto-Fix Critical and High Issues

**If no Critical/High issues were found, skip to Step 8.**

**Default: FIX IT.** Most review issues are straightforward pattern corrections. Auto-fix is the expected outcome, not the exception. A review that identifies problems but fixes nothing is only half the job.

Fix Critical and High issues directly in the source files:

1. For each Critical/High issue:
   a. Read the source file at the file:line cited in the review
   b. Read the reference file that shows the correct pattern
   c. Apply the fix using Edit (for targeted changes) or Write (for new files)

2. **Examples of fixes to make (never defer these):**
   - Wrong function signatures — fix to match the reference
   - Missing `'use client'` or `'use server'` directives
   - Wrong import paths or import ordering
   - Missing error handling where the reference shows a clear pattern
   - Missing `server-only` imports in server-side files
   - Wrong TypeScript types (e.g., `any` where a proper type exists)
   - Security issues: missing RLS checks, exposed credentials, missing auth
   - Naming/convention violations where the reference shows the correct pattern

3. **The ONLY reasons to defer to the main agent** (use sparingly):
   - The fix would change the feature's business logic or user-facing behavior
   - The fix contradicts the phase's Decision Log or architectural approach
   - You genuinely cannot determine the correct fix even after reading references

4. After fixing, re-read the file to verify the fix is correct and doesn't introduce new issues.

5. Update the review file:
   - Append "(Auto-fixed)" to fixed items in the Issues tables
   - Fill in the "Fixes Applied" section (see template)
   - Update the Verdict to reflect only remaining unfixed issues

### Step 8: Return Summary with Next Steps

After writing the review file, return:

- Review file location
- Verdict (Ready/Not Ready) — based on remaining unfixed issues only
- Count of issues (total, auto-fixed, deferred)
- Reference files used
- **Auto-fixed** (count and brief list of what was fixed)
- **Deferred to main agent** (issues not auto-fixed and why)
- **Next Steps for Medium/Low** — present as improvement opportunities

**Improvement mindset:** When listing Medium/Low issues, frame them as concrete improvements worth doing now — not optional niceties. Phases are rarely revisited after completion, so "fix later" effectively means "never." The user prefers investing in quality now over speed.

**Action directive for main agent:** If there are deferred items or Medium/Low suggestions, end your summary with:

```
ACTION REQUIRED: [N] deferred items and [M] improvement suggestions need main agent attention.
Please review the items above and fix or discuss with the user before proceeding.
```

## Troubleshooting

### Review produces false positives (flagging correct code)

**Cause:** The review skipped Step 3 (reading reference implementations) and flagged code based on assumptions rather than actual codebase patterns.

**Fix:** Always read at least one reference file of each type before flagging issues. If the codebase uses a pattern that differs from generic best practices, the codebase wins.

### Review is superficial ("looks good, no issues found")

**Cause:** The reviewer didn't read individual files at specific line numbers, relying on a surface-level scan instead of deep inspection.

**Fix:** For each file under review, read the full file and compare line-by-line against both the phase requirements and the reference implementation. Check every import path, function signature, and error handling pattern.

### Auto-fix introduces new issues

**Cause:** The fix was applied without re-reading the file to verify correctness, or the fix didn't account for surrounding context.

**Fix:** After every Edit, re-read the modified file to verify the fix is correct. Check that imports still resolve and that the change doesn't break adjacent code.

### Review format is inconsistent across phases

**Cause:** The reviewer didn't read `references/CODE-REVIEW-TEMPLATE.md` before writing (Step 6). Custom formats break the user's ability to track review status.

**Fix:** Always read the template first and follow its exact structure. Do not add custom sections or change the table format.

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

- Write review files within the plan folder
- When auto-fixing, you may also edit source files cited in the review
- Read the phase file FIRST before reviewing code
- **Read at least one reference implementation** before flagging pattern violations
- **Cite references** when flagging codebase pattern issues (e.g., "reference: claude-ai-server-actions.ts:65")
- Be specific with file paths and line numbers
- Critical and High issues block phase completion (unless auto-fixed)
- **Auto-fix**: Default is to fix. Only defer for genuine business logic changes or ADR contradictions
- **Auto-fix**: "Needs verification" is not a valid excuse — use Glob/Grep/Read to verify, then fix

The user configured this review to be thorough because vague feedback ("looks good", "some issues") doesn't help fix problems. Specific file:line references, comparison to known-good reference code, and concrete fixes are what the user needs to take action.
