---
name: page-structure
description: Generates section list for a page. Deterministic mapping. Does not write content.
---

# Page Structure Skill

## Purpose

Outputs ordered section list for a page type. Structure only.

## Input

```yaml
page_type: landing | service | service-area | article | calculator | thank-you
goal: lead | inform | compare | convert
industry: removals | cleaning | trades | legal | healthcare
```

## Output

```yaml
sections: [hero, trust-strip, benefits, ...]
primary_conversion_section: final-cta
cta_sections: [hero, benefits, final-cta]
seo_roles: { hero: primary_keyword, faq: long_tail }
structure_verdict: PASS | WARN | FAIL
```

## Invalid Combinations (STOP)

| page_type | goal | Result |
|-----------|------|--------|
| thank-you | lead | ❌ STOP |
| calculator | inform | ❌ STOP |
| article | convert | ❌ STOP |

**Invalid combination → no output, STOP.**

## Primary Conversion Section

**One section is THE conversion point.** All other CTAs support this.

| Page Type | Primary Conversion |
|-----------|-------------------|
| landing | final-cta |
| service | final-cta |
| service-area | final-cta |
| article | service-cta |
| calculator | calculator-widget |
| thank-you | upsell |

## SEO Responsibility Mapping

| Section | SEO Role |
|---------|----------|
| hero | primary_keyword in H1 |
| benefits | secondary_keywords |
| faq | long_tail_questions |
| service-intro | semantic_support |
| area-intro | location_keyword |

**Cross-reference:** `heading-tree` skill uses this.

## CTA Limits

| Rule | Value |
|------|-------|
| Max total CTAs | 4 |
| Min distance | 2 sections apart |

**Over 4 CTAs = WARN.** Adjacent CTAs = WARN.

## Section Dependencies

| Section | Requires |
|---------|----------|
| pricing | benefits |
| how-it-works | solution OR service-intro |
| local-reviews | area-intro |
| related-posts | body |

**Missing dependency → WARN.**

## Conditional Sections

| Section | Condition |
|---------|-----------|
| calculator | industry == removals |
| pricing-table | industry == cleaning |
| gallery | industry == trades |
| credentials-detail | industry == legal |
| compliance-badges | industry == healthcare |

## Section Maps (Summary)

| Page Type | Sections | Viewports |
|-----------|----------|-----------|
| landing | 11-12 | 8-10 |
| service | 11 | 6-8 |
| service-area | 9 | 5-6 |
| article | 8 | varies |
| calculator | 5 | 2-3 |
| thank-you | 5 | 1-2 |

**Full section lists → [references/section-maps.md](references/section-maps.md)**

## Structure Verdict

```yaml
structure_verdict: PASS | WARN | FAIL
issues: []
```

| Condition | Verdict |
|-----------|---------|
| Invalid page_type + goal | FAIL |
| Missing required section | FAIL |
| Missing dependency | WARN |
| CTA over limit | WARN |
| All rules pass | PASS |

## FAIL States

| Condition |
|-----------|
| Invalid page_type + goal combination |
| Missing hero section |
| Missing footer section |
| No CTA on lead goal page |

## WARN States

| Condition |
|-----------|
| >4 CTA sections |
| Adjacent CTA sections |
| Missing section dependency |

## Non-goals

- Does NOT write content
- Does NOT generate components
- Does NOT handle copy
- Does NOT validate content quality

## References

- [section-maps.md](references/section-maps.md) — Full section lists

## Definition of Done

- [ ] page_type + goal valid combination
- [ ] All required sections present
- [ ] Dependencies satisfied
- [ ] CTA count ≤4
- [ ] primary_conversion_section defined
- [ ] seo_roles mapped
- [ ] structure_verdict = PASS
