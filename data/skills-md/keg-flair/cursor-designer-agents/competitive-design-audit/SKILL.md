---
name: competitive-design-audit
description: Runs structured competitive and heuristic design audits (patterns, trade-offs, opportunities, recommendations). Use when the user asks to compare competitors, do a teardown, benchmark against best-in-class, or audit a feature/flow against references.
---

# Competitive Design Audit

## Defaults

- **Decision-oriented**: tie findings back to the design decision the audit is meant to inform.
- **Comparative, not encyclopedic**: focus on patterns, trade-offs, and implications.
- **Evidence-first**: clearly separate what’s provided vs inferred; cite sources if given.
- **Actionable output**: end with concrete recommendations and what to capture next.

## Constraints

- **Do not invent** competitor behavior as fact. If screenshots/links aren’t provided, frame as **hypotheses to verify** and suggest what to look for.
- **Ask at most 2 clarifying questions**. If unanswered, proceed with assumptions.
- Always include **one best-in-class reference** outside the direct category for contrast (unless user forbids).

## Clarifying questions (ask max 2)

1. What **feature/flow/pattern** are we auditing, and what **decision** will this inform?
2. Which **products** should be included? (If none, propose 3–5 and proceed.)

## Inputs to request (only if missing)

- Audit scope + decision to inform
- Comparator list (or permission to propose)
- Any screenshots/links/notes gathered so far (optional)
- Target audience (design-only vs cross-functional)

## Output template

```markdown
## Competitive design audit: [Feature / Flow / Pattern]

### Assumptions / constraints
- …

### Decision this informs
- …

### TL;DR
- 2–3 sentences: the dominant market pattern + the key opportunity/trade-off.

### Products audited
| Product | Tier | Why included | Evidence |
| --- | --- | --- | --- |
| … | Direct competitor | … | link / screenshot / “not provided” |
| … | Best-in-class reference | … | … |

### Comparison by aspect

#### Aspect 1: [e.g., entry point / discoverability]
- **Pattern observed**:
- **How products implement it**:
  - Product A:
  - Product B:
- **Trade-offs**:
- **Implication for us**:

#### Aspect 2: [e.g., safeguards / confirmation]
…

#### Aspect 3: [e.g., feedback / error handling]
…

### Pattern analysis
- **What the market converges on (and why)**:
- **Where products diverge (and what it implies)**:
- **Who does it best (and why it works)**:

### Opportunities for differentiation (2–4)

- **Opportunity**:
  - **User value**:
  - **Why competitors don’t do it**: (constraint / risk / inertia)
  - **Risks / trade-offs**:
  - **How to validate**:

### Recommendations

- **Do**:
- **Consider**:
- **Avoid**:

### What to capture next (if evidence missing)

- Screenshots/flows to collect for each product
- Specific questions to answer (e.g., “Where is undo offered?”)
```

## Category/domain lenses (use only when relevant)

If the user signals enterprise/compliance-heavy contexts, include lenses like:

- **Role-based UX** (admin vs manager vs end user)
- **Compliance constraints** (audit trails, required fields, approvals)
- **Mobile parity** and where it matters

