---
name: audit-typography
description: Review typography consistency and usability. Use to ensure readable, consistent text styling.
---

# Audit Typography

Review typography consistency and usability.

## When to Use
- After adding new text elements
- Checking readability
- Ensuring token adherence

## Approach

### Step 1: Project Invariants (Required)
**Before auditing**, check `docs/knowledge-base/` for project-specific constraints:
- `SPEC-CSS.md` — typography token mandates
- `RULES-UI.md` — typography rules (e.g., weight limits, font prohibitions)
- Flag any violation of documented invariants as **Critical** priority.

### Step 2: Focus Areas
- **Font Sizes**: Consistent use of `var(--font-size-*)` tokens
- **Font Weights**: Appropriate use of `var(--font-weight-*)` tokens
- **Line Height**: Readable line heights
- **Hierarchy**: Clear visual hierarchy (H1 > H2 > H3 > body)
- **Number Sets**: Lining figures for UI, oldstyle for body (if applicable)

### Checklist
- [ ] All font sizes use tokens
- [ ] Font weights follow hierarchy guidelines
- [ ] Line heights appropriate for content type
- [ ] Headings have clear visual distinction
- [ ] No hardcoded font values

### Output
Findings report with specific file:line citations.
