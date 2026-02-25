---
name: fix-issue
description: '[Fix & Debug] ⚡⚡ Fix a GitHub issue with systematic debugging'
argument-hint: [issue-number]
---

# Fix GitHub Issue: $ARGUMENTS

Fix a GitHub issue following the systematic debugging workflow based on the `debug` skill.

## Summary

**Goal:** Systematically diagnose and fix a GitHub issue with evidence-based root cause analysis and user approval before implementation.

| Step | Action               | Key Notes                                                           |
| ---- | -------------------- | ------------------------------------------------------------------- |
| 1    | Fetch issue details  | `gh issue view` -- extract title, labels, stack traces              |
| 2    | Understand the issue | Map expected vs actual behavior, reproduction steps                 |
| 3    | Evidence gathering   | Multi-pattern search: imports, string literals, dynamic invocations |
| 4    | Root cause analysis  | Rank causes by probability with file:line evidence                  |
| 5    | Propose fix          | Minimal changes, risk assessment, test plan, rollback plan          |
| 6    | Wait for approval    | Present analysis -- DO NOT code without explicit user approval      |
| 7    | Implement fix        | Code changes, tests, PR creation                                    |

**Key Principles:**

- **Be skeptical. Critical thinking. Everything needs traced proof.** — Never accept code at face value; verify claims against actual behavior, trace data flow end-to-end, and demand evidence (file:line references, grep results, runtime confirmation) for every finding
- Always use external memory at `.ai/workspace/analysis/issue-[number].md`
- If confidence < 90%, request user confirmation before proceeding
- Never make code changes without explicit user approval

**IMPORTANT**: Always use external memory at `.ai/workspace/analysis/issue-[number].md` for structured analysis.

## IMPORTANT: Anti-Hallucination Protocols

Before any operation:

1. "What assumptions am I making about this issue?"
2. "Have I verified this with actual code evidence?"
3. "Could I be wrong about the root cause?"

---

## Phase 1: Fetch Issue Details

1. **Get issue information:**

    ```bash
    gh issue view $ARGUMENTS
    ```

2. **Extract key information:**
    - Issue title and description
    - Labels (bug, feature, enhancement)
    - Related PRs or issues
    - Assignees and reviewers
    - Stack traces or error messages

3. **Create analysis notes** at `.ai/workspace/analysis/issue-[number].md`

---

## Phase 2: Understand the Issue

1. **Analyze the issue:**
    - What is the expected behavior?
    - What is the actual behavior?
    - Are there reproduction steps?
    - Is there a stack trace or error message?

2. **Search codebase for relevant code:**
    - Use grep for error messages and keywords
    - Search patterns: `.*EventHandler.*{Entity}`, `.*Consumer.*{Entity}`, etc.
    - Find related entities/components
    - Map the affected code paths

---

## Phase 3: Evidence Gathering

1. **Multi-pattern search:**
    - Static imports and usages
    - String literals (runtime/config references)
    - Dynamic invocations (reflection, attributes)

2. **Trace dependency chains:**
    - Who calls this code?
    - Who depends on this code?
    - Cross-service message flows

3. **Read actual implementations** (not just interfaces)

4. **Document evidence** with file:line references

---

## Phase 4: Root Cause Analysis

Analyze across dimensions:

1. **Technical**: Code defects, architectural issues
2. **Business Logic**: Rule violations, validation failures
3. **Data**: Corruption, integrity violations, race conditions
4. **Integration**: API contract violations, cross-service failures
5. **Environmental**: Configuration issues, deployment problems

Document:

- Potential root causes ranked by probability
- Evidence with file:line references
- Confidence level (High 90%+, Medium 70-89%, Low <70%)

---

## Phase 5: Propose Fix

1. **Design the fix:**
    - Minimal changes principle
    - Follow platform patterns from documentation
    - Consider edge cases

2. **Risk assessment:**
    - Impact level (Low/Medium/High)
    - Regression risk
    - Affected components

3. **Test plan:**
    - Unit tests to add
    - Manual testing steps
    - Regression considerations

4. **Rollback plan:**
    - How to revert if fix causes issues

---

## Phase 6: Wait for Approval

**CRITICAL:** Present your analysis and proposed fix in this format:

```markdown
## Issue Analysis Complete - Approval Required

### Issue

#[number] - [title]

### Root Cause Summary

[Primary root cause with evidence at file:line]

### Proposed Fix

[Fix description with specific files and changes]

### Risk Assessment

- **Risk Level**: [Low/Medium/High]
- **Regression Risk**: [assessment]

### Confidence Level: [X%]

### Files to Modify:

1. `path/to/file.cs:line` - [change description]

**Awaiting approval to proceed with implementation.**
```

**DO NOT** make any code changes without explicit user approval.

---

## Phase 7: Implement Fix

After approval:

1. Make the code changes following platform patterns
2. Add/update tests
3. Verify fix works
4. Create PR with issue reference using `gh pr create`

---

## Quick Verification Checklist

Before proposing any change:

- [ ] Searched static imports?
- [ ] Searched string literals?
- [ ] Checked dynamic invocations?
- [ ] Read actual implementations?
- [ ] Traced dependencies?
- [ ] Assessed what breaks?
- [ ] Documented evidence?
- [ ] Declared confidence?

**If ANY unchecked → DO MORE INVESTIGATION**
**If confidence < 90% → REQUEST USER CONFIRMATION**

---

Use the `debug` skill for the complete debugging protocol. For autonomous mode, use `debugging --autonomous`.
**⚠️ MUST READ** `.ai/docs/AI-DEBUGGING-PROTOCOL.md` for comprehensive guidelines.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
