---
name: figma-design-review
description: AI-powered design review for Figma components with weighted dual-scoring system. Evaluates Style Guide Implementation (70%) and LLM Metadata Accessibility (30%). For export, hands off to atomic-design skill.
---

# Figma Design Review Skill

Review and score Figma component designs using weighted dual-scoring.

## Two-Skill Architecture

```
figma-design-review (PHASE 1) -> atomic-design (PHASE 2 - Export)
  Score components (70/30)        Classify level (A/M/O)
  Identify issues                 Generate files
  Recommend fixes                 Extract tokens
  Determine export readiness
```

Score >= 70? -> Hand off to atomic-design

## Scoring Philosophy

| Dimension | Weight | Focus |
|-----------|--------|-------|
| Style Guide Implementation | 70% | Code quality, consistency, accessibility |
| LLM Metadata Accessibility | 30% | Documentation for AI code generation |

## When to Use

| Trigger | Action |
|---------|--------|
| Designer selects component | Full design review |
| "Review this component" | Scored report |
| "What's missing?" | Gap analysis |
| "Is this ready for export?" | Export readiness check |
| Score < 80 | Improvement roadmap |

---

## Dimension 1: Style Guide Implementation (70%)

### Variant Structure (25 pts)
| Criterion | Points |
|-----------|--------|
| Complete variant matrix | 10 |
| Consistent naming (Size=X, State=Y) | 5 |
| TypeScript interface defined | 5 |
| Logical organization | 5 |

### Token System (25 pts)
| Criterion | Points |
|-----------|--------|
| CSS Variables for colors | 10 |
| CSS Variables for typography | 5 |
| CSS Variables for spacing | 5 |
| Semantic token naming | 5 |

### Visual Consistency (20 pts)
| Criterion | Points |
|-----------|--------|
| Consistent font-weight | 5 |
| Consistent border-radius | 5 |
| Consistent padding/spacing | 5 |
| No layout artifacts | 5 |

### Accessibility States (20 pts)
| Criterion | Points |
|-----------|--------|
| Focus state present | 8 |
| Disabled state | 6 |
| Hover state | 4 |
| Touch target >= 44px | 2 |

### Code Quality (10 pts)
| Criterion | Points |
|-----------|--------|
| No duplication | 5 |
| Clean conditionals | 3 |
| Proper defaults | 2 |

---

## Dimension 2: LLM Metadata Accessibility (30%)

### Component Description (20 pts)
| Criterion | Points |
|-----------|--------|
| Primary description | 10 |
| Use case specified | 5 |
| Business context | 5 |

### Searchability (15 pts)
| Criterion | Points |
|-----------|--------|
| Tags present | 8 |
| Tags comprehensive | 7 |

### Development Metadata (25 pts)
| Criterion | Points |
|-----------|--------|
| testId | 5 |
| ariaLabel | 5 |
| analytics | 5 |
| category | 5 |
| level | 5 |

### Usage Guidelines (20 pts)
| Criterion | Points |
|-----------|--------|
| Do's list | 7 |
| Don'ts list | 7 |
| Notes | 6 |

### Technical Specs (20 pts)
| Criterion | Points |
|-----------|--------|
| Design tokens documented | 8 |
| Specs (minWidth, etc.) | 6 |
| A11y requirements | 6 |

---

## Score Interpretation

| Score | Grade | Export Status |
|-------|-------|---------------|
| 90-100 | Excellent | Ready |
| 80-89 | Good | Ready with notes |
| 70-79 | Acceptable | Fix critical first |
| 60-69 | Needs Work | Not ready |
| < 60 | Poor | Major rework |

---

## Report Output Format

```markdown
## Component Evaluation: [Name]

### Style Guide Implementation: **[XX]/100**

**Strengths:**
- [Positive finding]

**Weaknesses:**
- [Issue] -> **Fix:** [Solution]

### LLM Metadata: **[XX]/100**

**Includes:**
- [Present metadata]

**Missing:**
- [Missing metadata]

## Final Weighted Score

| Criterion | Score | Weight | Contribution |
|-----------|-------|--------|--------------|
| Implementation | XX | 70% | XX.X |
| LLM Accessibility | XX | 30% | XX.X |
| **Total** | | | **XX.X/100** |

### Recommendations:
1. [Recommendation] - [explanation]
```

---

## Review Framework

### Step 1: Extract Data
- Name/structure from Figma
- Code from get_design_context
- Screenshot from get_screenshot
- Metadata from description

### Step 2: Evaluate Implementation (70%)
- Variant count: expected vs actual
- Token usage check
- Visual consistency
- Accessibility states
- Code quality

### Step 3: Evaluate LLM Accessibility (30%)
- Description present?
- Tags comprehensive?
- Dev metadata complete?
- Usage guidelines?
- Technical specs?

### Step 4: Calculate
```
implementation_score = variant + token + visual + a11y + code
llm_score = desc + search + dev + usage + specs
weighted = (implementation * 0.7) + (llm * 0.3)
```

### Step 5: Generate Report
- Strengths (max 6)
- Weaknesses (max 5, each with fix)
- Recommendations by priority
- Export readiness

---

## Key Rules

- Every weakness MUST include a fix
- Every issue MUST name specific field
- Strengths capped at 6
- Weaknesses capped at 5
- Recommendations ordered by priority
- English only

## References

| File | Purpose |
|------|---------|
| references/audit-summary-format.md | Output format |
| references/scoring-rubric.md | Scoring criteria |
| references/common-issues.md | Frequent problems |
| ../atomic-design/SKILL.md | Export skill |
