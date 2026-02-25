---
name: seo-optimizer
description: 'SEO architecture and content strategy for search visibility. Covers entity-first optimization, structured data, E-E-A-T signals, AI Overviews optimization, and content auditing. Use when optimizing search rankings, implementing JSON-LD schema, improving E-E-A-T signals, auditing site performance, planning topical authority, or structuring content for AI Overviews and featured snippets.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# SEO Optimizer

## Overview

Optimizes digital visibility through entity-based SEO, structured data, and content architecture. Focuses on AI Overviews optimization, E-E-A-T authority signals, and semantic topic clustering rather than keyword-centric approaches.

**When to use:** Search ranking optimization, structured data implementation, content audits, topical authority planning, featured snippet targeting, Core Web Vitals improvement.

**When NOT to use:** Paid advertising campaigns, social media strategy, email marketing, brand identity design.

## Quick Reference

| Pattern           | Approach                                | Key Points                                                     |
| ----------------- | --------------------------------------- | -------------------------------------------------------------- |
| AI Overviews      | Question-based H2s with direct answers  | 1-2 sentence answer before expanding; scannable lists          |
| E-E-A-T signals   | Experience-led content with author bios | First-hand evidence, SME review labels, credentials            |
| Structured data   | JSON-LD schema for entities             | Organization, Article, FAQ, Breadcrumb schemas                 |
| Topic clusters    | Pillar page + cluster architecture      | Internal links flow between pillar and clusters                |
| Semantic SEO      | Intent mapping + related terms          | Map pages to Informational/Commercial/Transactional intent     |
| Content audit     | 30-point scoring methodology            | Title, meta, keywords, structure, snippets, linking, technical |
| Featured snippets | Format-matched content blocks           | 40-60 word definitions, numbered steps, comparison tables      |
| Schema markup     | Explicit entity definitions             | Define Who/What/Where in first paragraph + Schema.org          |
| Content freshness | Periodic refresh protocol               | Update critical articles every 6 months with current data      |
| Core Web Vitals   | Performance-first design                | LCP, CLS, INP monitoring and continuous improvement            |

## Common Mistakes

| Mistake                                                             | Correct Pattern                                                               |
| ------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Keyword stuffing to boost rankings                                  | Use semantic SEO with semantically related terms and natural language         |
| Publishing generic AI-generated content without expert review       | Lead with first-hand experience and E-E-A-T signals                           |
| Ignoring Core Web Vitals (LCP, CLS, INP) impact on rankings         | Implement performance-first design and monitor vitals continuously            |
| Using hidden or incomplete JSON-LD schema markup                    | Define explicit, complete structured data that maps entities clearly          |
| Building thin affiliate pages without topical depth                 | Create pillar pages with full cluster coverage                                |
| Writing definitions longer than 60 words for snippet targeting      | Keep definition paragraphs to 40-60 words for featured snippet eligibility    |
| Using non-descriptive anchor text like "click here" or "read more"  | Use keyword-rich descriptive anchor text that describes the destination       |
| Missing primary keyword from title, description, or first 100 words | Place primary keyword in title, meta description, first paragraph, and one H2 |

## Delegation

- **Audit a site for technical SEO issues, missing schema, and Core Web Vitals problems**: Use `Explore` agent to crawl pages and identify structured data gaps
- **Implement JSON-LD schema markup and meta tags across page templates**: Use `Task` agent to add Organization, Article, FAQ, and Breadcrumb schemas
- **Plan a topical authority strategy with pillar pages and content clusters**: Use `Plan` agent to map keyword intent, cluster hierarchy, and internal linking architecture

## References

- [AI Overviews optimization and search visibility](references/ai-overviews.md)
- [E-E-A-T standards and authority building](references/eeat-standards.md)
- [Semantic entity SEO and topic clusters](references/semantic-entity-seo.md)
- [Schema markup patterns with JSON-LD](references/schema-markup.md)
- [Content audit methodology and scoring](references/content-audit.md)
