---
name: bio-logic
description: Evaluate scientific rigor, methods, biases, and evidence quality for claims, papers, and study designs.
---

# Bio-Logic: Scientific Reasoning Evaluation

Use structured frameworks to evaluate scientific claims, methodology, and evidence strength.

## Instructions

1. Identify the task (claim assessment, paper critique, study design review).
2. Apply the relevant checklist below.
3. Structure output using the provided format.

### Critique Checklist

Use relevant sections based on the review scope. Skip items not applicable to the study type.

```
## Methodology
- [ ] Design matches research question (causal claim → RCT needed)
- [ ] Sample size justified (power analysis reported)
- [ ] Randomization/blinding implemented where feasible
- [ ] Confounders identified and controlled
- [ ] Measurements validated and reliable

## Statistics
- [ ] Tests appropriate for data type
- [ ] Assumptions checked
- [ ] Multiple comparisons corrected
- [ ] Effect sizes + CIs reported (not just p-values)
- [ ] Missing data handled appropriately

## Interpretation
- [ ] Conclusions match evidence strength
- [ ] Limitations acknowledged
- [ ] Causal claims only from experimental designs
- [ ] No cherry-picking or overgeneralization

## Red Flags
- [ ] P-values clustered just below .05
- [ ] Outcomes differ from registration
- [ ] Correlation presented as causation
- [ ] Subgroups analyzed without preregistration
```

### Claim Assessment

1. Identify claim type (causal, associational, descriptive).
2. Match evidence to claim type.
3. Check logical connection between data and conclusion.
4. Ensure confidence matches evidence strength.

**Claim strength ladder**:
| Language | Requires |
|----------|----------|
| "Proves" / "Demonstrates" | Strong experimental evidence |
| "Suggests" / "Indicates" | Observational with controlled confounds |
| "Associated with" | Observational, no causal claim |
| "May" / "Might" | Preliminary or hypothesis-generating |

### Output Format

```markdown
## Summary
[1-2 sentences: What was studied and main finding]

## Strengths
- [Specific methodological strengths]

## Concerns
### Critical (threaten main conclusions)
- [Issue + why it matters]

### Important (affect interpretation)
- [Issue + why it matters]

### Minor (worth noting)
- [Issue]

## Evidence Rating
[GRADE level: High/Moderate/Low/Very Low with justification]

## Bottom Line
[What can/cannot be concluded from this evidence]
```

## Quick Reference

| Task | Action |
|------|--------|
| Review a paper | Use the Critique Checklist below |
| Evaluate a claim | Use Claim Assessment steps |
| Assess evidence strength | See `references/evidence.md` |
| Identify biases | See `references/biases.md` |
| Statistical errors | See `references/stats.md` |
| Logical fallacies | See `references/fallacies.md` |
| Study design review | See `references/design.md` |

## Input Requirements

- Manuscript or study summary
- Claim statements to evaluate
- Methods and results (as available)

## Output

- Structured critique with strengths, concerns, and evidence rating
- Clear recommendation on claim strength and limitations

## Quality Gates

- [ ] Claim type matches evidence type
- [ ] Key methodological risks are identified
- [ ] Evidence rating is justified with concrete issues

## Examples

### Example 1: Quick Paper Critique

**Input**: "Review this RCT on vitamin D and depression"

**Output**:
```
## Summary
RCT of 200 adults testing vitamin D supplementation for depression over 12 weeks.

## Strengths
- Randomized, double-blind, placebo-controlled
- Validated depression scale (PHQ-9)
- Adequate power analysis

## Concerns
### Critical
- 35% dropout, differential by group (attrition bias)
- ITT analysis not performed

### Important
- Single-site limits generalizability

## Evidence Rating
Moderate (downgraded from high due to attrition bias)

## Bottom Line
Suggestive but not conclusive due to differential attrition.
```

### Example 2: Claim Assessment

**Input**: "This study proves that coffee prevents Alzheimer's"

**Assessment**: If based on observational data, this is a correlation→causation error. Appropriate language: "Coffee consumption is associated with lower Alzheimer's risk."

## Troubleshooting

**Issue**: Insufficient methods details
**Solution**: Request missing design/statistics information before rating evidence.

**Issue**: Conflicting results across studies
**Solution**: Report uncertainty and suggest stronger study designs for resolution.
