---
name: paper-revision
description: Revise papers based on reviewer feedback. Map reviewer concerns to specific sections, apply targeted edits, run additional experiments if needed, and verify improvements. Use after receiving peer review with revision requests.
argument-hint: [reviews-or-draft]
---

# Paper Revision

Systematically revise papers based on reviewer feedback.

## Input

- `$0` — Reviewer comments/feedback
- `$1` — Current paper draft (main.tex or paper directory)

## References

- Revision workflow and prompts: `~/.claude/skills/paper-revision/references/revision-prompts.md`

## Workflow

### Step 1: Parse and Prioritize Concerns
For each reviewer comment:
1. Extract the specific concern
2. Classify: major revision, minor revision, question, suggestion
3. Map to affected paper section(s)
4. Prioritize: address major concerns first

### Step 2: Plan Revisions
Create a revision plan:
```
Concern → Affected Section → Required Action → New Content/Experiment
```

Categories of actions:
- **Clarification**: Rewrite text for clarity
- **Additional experiment**: Run new experiment, add results
- **New analysis**: Add ablation, statistical test, or comparison
- **Structural change**: Move, merge, or split sections
- **Citation**: Add missing references

### Step 3: Execute Revisions
For each planned revision:
1. Read the current section
2. Apply targeted edits (preserve surrounding structure)
3. If new experiments needed: use experiment-code skill
4. If new figures/tables needed: use figure-generation / table-generation skills
5. Mark changes (use `\textcolor{blue}{...}` for revised text)

### Step 4: Verify Improvements
- Re-run self-review skill to check if scores improved
- Verify all reviewer concerns are addressed
- Check that revisions don't introduce new issues
- Ensure page count still fits venue requirements

### Step 5: Write Revision Summary
Generate a diff summary:
- List all changes made with section references
- Note any new experiments, figures, or tables added
- Cross-reference each change to the reviewer concern it addresses

## Rules

- Address EVERY reviewer concern — do not skip any
- Preserve paper structure unless structural change is explicitly needed
- New results must come from actual experiments, not hallucinated
- Mark all revised text clearly for the reviewers
- Keep a copy of the previous version before revising
- Compare new scores vs previous scores after revision

## Related Skills
- Upstream: [self-review](../self-review/)
- Downstream: [paper-compilation](../paper-compilation/)
- See also: [rebuttal-writing](../rebuttal-writing/), [paper-writing-section](../paper-writing-section/)
