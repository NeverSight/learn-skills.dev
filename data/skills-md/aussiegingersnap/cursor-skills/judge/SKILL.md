---
name: judge
description: Quality review skill for verifying complex changes against criteria. Use for multi-file changes, new features, or before important commits. Skip for trivial fixes and quick iterations.
skill_type: atomic
---

# Judge

Quality review and evaluation skill that verifies completed work against defined criteria. Part of the two-tier multi-agent architecture where Judge evaluates worker output.

## Contract

**Inputs:**
- Completed work output (files, changes, artifacts)
- Original acceptance criteria or success criteria
- Context about what was attempted

**Outputs:**
- Pass/fail determination
- List of issues found (if any)
- Recommendations for fixes (if failing)

**Success Criteria:**
- [ ] All acceptance criteria evaluated
- [ ] Clear pass/fail determination provided
- [ ] Actionable feedback given for any failures

## When to Use

Invoke the judge skill:

1. **After atomic skill completion** - Before marking work as done
2. **Before committing** - Final quality gate
3. **After build/test phases** - Verify implementation meets spec
4. **When reviewing generated code** - Catch issues before integration

## When NOT to Use

Skip the judge skill for:

- **Trivial changes** - Single-line fixes, typo corrections
- **Mid-workflow** - Don't interrupt atomic skills; judge at phase boundaries
- **Exploratory work** - When user is iterating quickly and explicitly skipping review
- **User-requested skip** - When user says "just do it" or "skip review"

## Review Process

### Step 1: Gather Context

Collect the materials needed for review:

1. **The output** - What was produced (files, code, documents)
2. **The criteria** - What was supposed to be achieved (acceptance criteria, spec)
3. **The scope** - What was in/out of scope for this work

### Step 2: Evaluate Against Criteria

For each acceptance criterion:

1. Check if the criterion is met
2. Note any partial completion
3. Document evidence (file paths, line numbers, test results)

Use this evaluation format:

```markdown
## Review: [Work Description]

### Criteria Evaluation

| Criterion | Status | Evidence |
|-----------|--------|----------|
| [Criterion 1] | PASS/FAIL/PARTIAL | [Evidence] |
| [Criterion 2] | PASS/FAIL/PARTIAL | [Evidence] |

### Issues Found

1. [Issue description]
   - **Severity**: Critical/Major/Minor
   - **Location**: [File/line]
   - **Fix**: [Recommended action]

### Verdict

**PASS** / **FAIL** / **PASS WITH NOTES**

[Summary of decision]
```

### Step 3: Apply Review Dimensions

Evaluate across these dimensions based on work type:

#### For Code Changes

| Dimension | Check |
|-----------|-------|
| **Correctness** | Does it do what was specified? |
| **Completeness** | Are all criteria addressed? |
| **Quality** | No obvious bugs, edge cases handled? |
| **Style** | Follows project conventions? |
| **Scope** | No scope creep beyond criteria? |

#### For Document Generation

| Dimension | Check |
|-----------|-------|
| **Accuracy** | Information is correct? |
| **Completeness** | All required sections present? |
| **Format** | Follows expected structure? |
| **Clarity** | Understandable to target audience? |

#### For Infrastructure Changes

| Dimension | Check |
|-----------|-------|
| **Functionality** | Works as expected? |
| **Security** | No exposed secrets, proper permissions? |
| **Idempotency** | Can be run again safely? |
| **Documentation** | Changes documented? |

## Severity Levels

| Level | Definition | Action |
|-------|------------|--------|
| **Critical** | Blocks functionality, security issue, data loss risk | Must fix before proceeding |
| **Major** | Significant deviation from spec, poor UX | Should fix before commit |
| **Minor** | Style issues, minor improvements | Can note for future |

## Verdicts

### PASS

All criteria met, no critical/major issues. Work can proceed.

### FAIL

Critical issues found OR acceptance criteria not met. Work must be revised.

Provide:
- Specific issues with locations
- Recommended fixes
- Which criteria failed

### PASS WITH NOTES

All criteria met, but minor issues noted. Work can proceed with awareness of noted items.

## Integration with Orchestrators

When used in orchestrated workflows:

1. **Orchestrator invokes atomic skill** - Work is produced
2. **Orchestrator invokes judge** - Work is evaluated
3. **If PASS** - Proceed to next phase
4. **If FAIL** - Return to previous skill with feedback

This creates the planner/worker/judge pattern that scales.

## Quick Review Checklist

For rapid reviews, use this checklist:

```markdown
## Quick Review

- [ ] All acceptance criteria addressed
- [ ] No obvious bugs or errors
- [ ] Follows project conventions
- [ ] No scope creep
- [ ] Ready to commit/proceed

**Verdict**: PASS / FAIL
```

## References

See `references/review-criteria.md` for detailed review criteria by skill type.
