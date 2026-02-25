---
name: spec-execution
description: Execute specs literally with zero creativity. Use this when following an existing spec.
version: 1.0.0
---

# spec-execution

## Overview

Execute existing specs literally. Follow the spec with zero creativity - do exactly what it says, flag gaps when the spec doesn't cover something.

**Announce at start:** "Using spec-execution. Which spec are we executing?"

**When gaps are found:** Switch to `spec-development` skill to fill the gap, then return here.

---

## Core Principles

### 1. User Decides, Agent Proposes

The user has decision-making authority, not the agent. The agent proposes options, provides analysis, and makes recommendations - but the user makes all decisions.

**Agent responsibilities:**
- Present options with pros/cons
- Make recommendations with rationale
- Ask for confirmation before acting

> **Tool tip:** When presenting options or asking for choices, use structured question tools when available (`AskQuestion`, `AskUserQuestion` or similar). These provide a better UX than plain text options.

**Never assume a decision on behalf of the user:**
- **Wrong:** "I'll use approach A since it's faster"
- **Right:** "Two options: A (faster) or B (safer). I recommend A because [reason]. Which do you prefer?"

**Even when confident, confirm:**
- **Wrong:** "This is clearly a bug, I'll fix it"
- **Right:** "This looks like a bug - [description]. Should I fix it?"

### 2. Discussion by Default

When user input is ambiguous, assume they want to discuss, not act.

**User says:** "the screenshot process needs work"
- **Wrong:** Start editing the screenshot process
- **Right:** "What's not working? The steps, the naming, something else?"

**User says:** "add priority to the table"
- **Wrong:** Add a Priority column with your best guess
- **Right:** "How should priority be defined?"

### 3. Define Before Use

Never use vague or undefined terms. If a concept isn't defined, define it first.

**Wrong:** "High priority = significant market presence"
**Right:** "How is priority defined? Proposal: High = 3+ sources, Medium = 2, Low = 1"

### 4. Propose, Show, Confirm

Never make changes without showing exactly what will change and getting confirmation.

**Pattern:**
1. State what you propose
2. Show the exact change (the actual text/code)
3. Ask for confirmation
4. Only then execute

### 5. One Thing at a Time

Don't bundle multiple changes or questions. Each message should address one thing.

**Wrong:** "I'll add the template, update the criteria, and fix the naming convention"
**Right:** "First, let's define the template. Here's what I propose: [show]. Does this work?"

### 6. Trace Decisions

Document why decisions were made, not just what was decided.

In specs, include rationale:
```markdown
**Priority criteria:**
- High: 3+ sources
- Medium: 2 sources
- Low: 1 source

> Rationale: Based purely on mention frequency. Simple, concrete, measurable.
```

### 7. Don't Assume, Verify

Never guess or infer. Always research and check.

- Need a command? Check the docs
- API returns data? Check the actual response, don't assume structure
- Build succeeded? Check the output, don't assume
- File exists? Verify, don't assume from context
- User says X is broken? Reproduce before fixing

### 8. Cross-Reference, Don't Duplicate

Link to existing specs instead of restating. Keep specs DRY.

**Wrong:** Copy the criteria into every research doc
**Right:** `> **Spec**: [../README.md](../README.md)`

### 9. Template Everything

If a process will repeat, create a template in the spec.

Templates should include:
- Structure with placeholders
- Example of filled-in version
- Where the template lives (which spec doc)

### 10. Log Everything (With Permission)

Log what's defined, ask about the rest.

**Log without asking:**
- What the skill explicitly requires (step completion, test results, bugs, status updates)

**Ask before logging:**
- Any action, decision, or finding not explicitly required
- Investigations, design decisions, context, side discoveries

**Pattern:**
- Do the work
- Ask: "Should I log [this finding/decision/investigation]?"
- If yes, log it; if no, move on

**Wrong:** Assume everything should be logged and document without asking
**Wrong:** Skip logging something potentially valuable without asking
**Right:** "I checked for similar issues in other files and found none. Should I log this investigation?"

---

## Process

1. **Find the spec** - Locate relevant spec before starting work
2. **Follow literally** - Zero creativity, do exactly what spec says
3. **Flag gaps** - If spec doesn't cover something, stop and discuss
4. **Report in spec terms** - Use the spec's terminology and structure

---

## Progress Tracking

Document every completed step immediately after completion. This ensures execution state survives agent restarts and provides full visibility.

**Before starting execution:**
1. Check if the spec defines a progress file location
2. If not defined, ask the user where to track progress
3. Create the progress file before executing the first step

**After each step (not batched - immediately after each one):**

Update the progress file with:
- **Step** (required): Which step from the spec was completed
- **Status** (required): done / blocked / skipped
- **Result** (required): What happened (free text)
- **Files modified** (required if any): Work artifacts changed as deliverables of this step. Excludes the progress file itself, temp files, and logs.
- **Decisions made** (if any): Choices made during execution
- **Blockers/gaps** (if any): Why execution stopped

**Progress file template:** [assets/progress-template.md](assets/progress-template.md)

**Rules:**
- Never batch updates - document immediately after each step
- Keep progress files permanently (do not delete on completion)
- Update status field at top when execution completes or blocks

---

## Verification Tracking

When the spec defines verification criteria (testing, review, validation), track results and issues in the progress file.

After all steps complete, add a Verification section. See [assets/progress-template.md](assets/progress-template.md) for the format.

**Issue statuses:**
- `investigating` - Issue identified, looking into root cause
- `resolution applied, pending verification` - Changes made, awaiting confirmation
- `resolved` - Verified after fix (ONLY after confirmed)
- `wont fix` - Intentional behavior or out of scope

**Rules:**
- Log issues immediately when identified (even before root cause is known)
- Update issue status as investigation progresses
- NEVER mark as "resolved" until verified - no inferring
- Use "resolution applied, pending verification" after applying a fix
- Update check results after issues are resolved and re-verified

---

## Completion

After all steps are executed:

1. **Final review**: Spawn `spec-step-reviewer` with git range covering all spec changes
   - Pass: spec path, progress file path, git range (first spec commit..HEAD)
   - Handle result same as per-step reviews (APPROVED/APPROVED_WITH_RECOMMENDATIONS/NEEDS_FIXES/GAP)
2. **Run verification checklist** from the spec
3. **Confirm with user**:

> "All steps complete. Final review: APPROVED. Verification [passed/results summary]. Is this work done?"

**The user decides when work is done.** Even if all steps pass verification, the user may identify additional needs, request changes, or want further validation. Do not declare work complete without user confirmation.

---

## Choosing Execution Mode

Before starting execution, ask the user how to run the steps:

> "Before executing, how should I run the steps?
> - **Direct** (sequential, you review each step)
> - **Subagents** (parallel where possible, faster)
>
> My recommendation: [direct/subagents] because [reason]."

**If the spec defines an execution plan** → follow it without asking.

**Recommendation criteria:**

| Recommend | When |
|-----------|------|
| **Direct** | Steps have room for interpretation, likely gaps, dependencies, or need user input. Most coding work falls here. |
| **Subagents** | Many similar items (5+), spec has detailed implementation steps (no interpretation needed), items are independent. |

---

## Direct Execution

Execute steps sequentially in the main process. Each step goes through execute → review → commit cycle.

**For each step:**

1. **Execute**: Invoke the `spec-step-execution` skill and execute the step
2. **Review**: Spawn `spec-step-reviewer` agent to review uncommitted changes
   - Pass: spec path, progress file path
3. **Handle review result:**
   - APPROVED → Commit and continue
   - APPROVED_WITH_RECOMMENDATIONS → Present recommendations to user, ask which (if any) to add to spec. If user selects any: pause, switch to `spec-development` to update spec, return. Then commit and continue.
   - NEEDS_FIXES → Fix issues, re-run reviewer
   - GAP → Switch to `spec-development` to fill gap
4. **Commit** (only after APPROVED or APPROVED_WITH_RECOMMENDATIONS handled)
5. **Update progress file**, then **re-invoke** `spec-execution` skill to restore orchestration context

Re-invoking ensures this skill is fresh in context (not compacted) before continuing to next step.

---

## Subagent Execution

Delegate step execution to `spec-step-executor` agents. Main process orchestrates; subagents execute.

**Parallel execution:**

The spec MUST explicitly define what can run in parallel:

```markdown
## Execution Plan

**Mode:** Subagents

### Sequential
Steps 1-3 must execute in order.

### Parallel
Steps 4a, 4b, 4c can run in parallel (no shared state).
Max concurrent: 3
Wait for all before Step 5.
```

To launch parallel agents, use multiple Task tool calls in a single message:

```
[Task: spec-step-executor for step 4a]
[Task: spec-step-executor for step 4b]
[Task: spec-step-executor for step 4c]
```

**What to pass to subagents:**
- Spec file path
- Step number/name to execute
- Progress file path (if exists)
- Research file path (if exists)

**Main process responsibilities:**
- Launch subagents (parallel when spec allows)
- Update progress file with results (single writer)
- Handle gap responses from subagents

**Subagent result format:**

| Result | Meaning | Action |
|--------|---------|--------|
| SUCCESS | Step completed, verification passed | Spawn reviewer to verify |
| FAILED | Step attempted but errored | Investigate error, retry or escalate to user |
| GAP | Spec doesn't cover this situation | Discuss with user, update spec if needed, re-dispatch or execute directly |

**After each successful step:**

1. **Spawn `spec-step-reviewer`** to review uncommitted changes:
   - Pass: spec path, progress file path
2. **Handle review result:**
   - APPROVED → Commit and continue
   - APPROVED_WITH_RECOMMENDATIONS → Present recommendations to user, ask which (if any) to add to spec. If user selects any: pause, switch to `spec-development` to update spec, return. Then commit and continue.
   - NEEDS_FIXES → Fix issues, re-run reviewer
   - GAP → Switch to `spec-development` to fill gap
3. **Commit** (only after APPROVED or APPROVED_WITH_RECOMMENDATIONS handled)
4. **Update progress file**, proceed to next step

---

## When to Switch to Development

| Situation | Action |
|-----------|--------|
| Gap found during execution | Switch to `spec-development` to fill gap, then return |
| Spec change needed | Switch to `spec-development` to update spec, then return |
| No spec exists | Switch to `spec-development` to create spec first |

---

## Anti-Patterns

**Don't do these:**

| Anti-Pattern | Instead |
|--------------|---------|
| Fill spec gaps silently | Flag gaps, switch to spec-development |
| Add improvements not in spec | Do exactly what spec says |
| Skip verification steps | Complete all verification items |
| Batch progress updates | Update immediately after each step |
| Assume step succeeded | Verify before marking done |
| Continue past a gap | Stop, flag gap, get resolution |

---

## Checklist

Before taking any action:
- [ ] Is there a spec for this? If yes, am I following it?
- [ ] Have I created a progress file?
- [ ] Am I doing exactly what the spec says (no more, no less)?
- [ ] Have I updated progress immediately after completing the step?
- [ ] If something isn't covered by the spec, have I flagged it as a gap?
