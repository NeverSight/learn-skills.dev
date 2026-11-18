---
name: anti-pattern-audit
description: Monthly self-deception audit — 25 anti-patterns from CEO Bible Section M
user-invocable: true
---

# Anti-Pattern Audit

Monthly self-deception check. Based on CEO Bible Section M.

## Process

1. Read daily logs and weekly reviews for the past month
2. Read MEMORY.md — current state
3. Check each block of anti-patterns
4. Score: 0 (not observed), 1 (mild risk), 2 (active problem)
5. Total score > 8 = serious conversation needed

## Block 1: General Founder-CEO Mistakes

1. **Too many wedges at once** — is there diluted signal?
2. **Confusing early revenue with repeatability** — a few sales != PMF
3. **Letting early customers dictate roadmap** — building a services company?
4. **Scaling GTM before retention/onboarding stable** — water into leaky bucket?
5. **Treating fundraising as validation** — investor interest != customer truth

## Block 2: Ex-Engineer Founder Mistakes

6. **Hiding in product** — what % of time does the founder spend in code vs with customers?
7. **"Product should speak for itself"** — markets don't decode architecture
8. **Leading with features, not pain** — buyers buy changed outcomes
9. **Building platform before earning wedge** — breadth is tax on learning
10. **Delegating sales/positioning too early** — losing best signal stream

## Block 3: Metric Interpretation Mistakes

11. **Aggregate dashboards vs cohort/segment cuts**
12. **Calling pilots "ARR"**
13. **Signed contracts = retention proof when engagement dead**
14. **Optimizing traffic before activation/TTFV**
15. **Counting shipped experiments vs changed beliefs**

## Block 4: Growth Mistakes Before PMF

16. **Many channels before one message lands**
17. **Paid acquisition to compensate poor positioning**
18. **Outbound with no proof, no content, no trust**
19. **B2C DAU as success when B2B conversion weak**
20. **Hiring marketer to find PMF**

## Block 5: AI-Era Specific Mistakes

21. **Demo excitement != durable value**
22. **Selling "AI" instead of measurable business result**
23. **Ignoring trust/evals/data handling until procurement**
24. **Pricing ignoring compute/HITL costs** -> negative-margin growth
25. **AI summaries replacing direct founder contact** -> synthetic certainty

## Output Format

```
Anti-Pattern Audit — [Month YYYY]

Score: X/50

Critical (score 2):
- #N: [description] — [evidence from this month]

Watch (score 1):
- #N: [description] — [early signs]

Clean:
- [list of areas with no issues]

Recommendation:
[Top 3 actions to address critical patterns]
```

Follow output preferences from USER.md (language, format, platform constraints).

## Rules

- Be honest. If the founder is hiding in code — say it directly.
- Use concrete data: "this week 2 conversations out of 8-12 target"
- Don't sugar-coat or soften
- Log the result to `memory/YYYY-MM-DD.md`
