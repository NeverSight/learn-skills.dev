---
name: client-proposal
description: Generate a professional project proposal from a website audit. Analyzes the prospect's current site, identifies issues, and produces a structured proposal with scope, deliverables, tech recommendations, and phased timeline. Use as a sales tool or for scoping client engagements.
---

This skill generates a professional, data-driven project proposal by auditing a prospect's existing website. It combines findings from `content-extraction`, `web-audit`, and `seo-migration` into a persuasive document that demonstrates expertise and defines a clear scope of work.

The user provides: the prospect's website URL, the type of engagement (redesign, migration, optimization, new build), and optionally the target budget range or timeline constraints.

## Proposal Generation Process

### Step 1: Automated Site Analysis

Run a lightweight version of the audit skills to gather data:

#### Quick Performance Scan
```
- Lighthouse scores (performance, a11y, SEO, best practices) on homepage + 3 key pages
- Core Web Vitals (LCP, CLS, INP)
- Page weight and request count
- Mobile responsiveness at 390px
```

#### Content & Structure Scan
```
- Total page count and sitemap
- Tech stack detection (framework, CMS, hosting, analytics)
- Image optimization status (formats, sizes, lazy loading)
- Missing metadata (titles, descriptions, OG tags)
- Broken links count
```

#### SEO Scan
```
- Missing structured data
- Redirect issues
- Canonical URL problems
- robots.txt and sitemap.xml status
- HTTPS status
```

Save raw data to `proposal-data/{prospect-name}/` for reference.

### Step 2: Identify Issues & Opportunities

Categorize findings into:

**Critical Issues** (breaking or losing business):
- Site not mobile-responsive
- Performance scores below 50
- Accessibility violations (legal risk)
- Broken forms or checkout flows
- HTTPS not enabled

**High Impact Improvements** (measurable ROI):
- Performance optimization (faster = better conversion)
- SEO improvements (more organic traffic)
- Mobile UX improvements
- Modern design refresh

**Nice-to-Have Enhancements**:
- Animations and micro-interactions
- Blog or content management
- Multi-language support
- Analytics and tracking improvements

### Step 3: Generate Proposal Document

Output a professional proposal as Markdown (easily convertible to PDF):

```markdown
# Proposal: Website Redesign for {Company Name}

**Prepared by**: {Agency Name}
**Date**: {Date}
**Version**: 1.0

---

## Executive Summary

{2-3 paragraphs summarizing the current state, key issues found, and the
proposed solution. Written for a non-technical decision-maker.}

---

## Current Site Analysis

### Performance
| Metric | Current | Industry Target | Status |
|--------|---------|----------------|--------|
| Performance Score | 43 | ≥ 90 | ❌ |
| LCP | 4.8s | < 2.5s | ❌ |
| CLS | 0.23 | < 0.1 | ❌ |
| Mobile Responsive | Partial | Full | ⚠️ |

### Accessibility
- {X} violations found (WCAG AA)
- Missing alt text on {X} images
- {Specific high-impact issues}

### SEO
- Missing meta descriptions on {X}/{Y} pages
- No structured data (schema.org)
- Sitemap.xml: {status}

### Key Screenshots
{Include annotated screenshots showing specific issues — broken mobile layout,
slow loading, accessibility problems}

---

## Proposed Solution

### Approach
{Describe the technical approach — which stack, why, what changes}

### Scope of Work

#### Phase 1: Foundation ({X} weeks)
- [ ] Content extraction and migration
- [ ] Project scaffolding ({tech stack})
- [ ] Design system setup (typography, colors, components)
- [ ] Responsive layout framework
- [ ] SEO redirect mapping

#### Phase 2: Implementation ({X} weeks)
- [ ] Homepage redesign
- [ ] {Page 2} redesign
- [ ] {Page 3} redesign
- [ ] ...
- [ ] Contact form with email integration
- [ ] Mobile navigation

#### Phase 3: Quality Assurance ({X} weeks)
- [ ] Cross-browser testing (Chrome, Safari, Firefox)
- [ ] Mobile responsiveness testing
- [ ] Accessibility audit (WCAG AA compliance)
- [ ] Performance optimization (target: 90+ Lighthouse)
- [ ] SEO migration validation (all redirects verified)
- [ ] Content parity verification

#### Phase 4: Launch ({X} week)
- [ ] Staging deployment and client review
- [ ] DNS / domain configuration
- [ ] Production deployment
- [ ] Post-launch monitoring (2 weeks)

### Out of Scope
{Explicitly list what is NOT included to prevent scope creep:
- CMS/backend development (unless specified)
- Content writing/copywriting
- Logo or brand identity design
- Ongoing maintenance (separate retainer)
- Third-party integrations beyond {X}}

---

## Tech Stack Recommendation

| Layer | Technology | Why |
|-------|-----------|-----|
| Framework | {e.g., Next.js 16} | {Rationale} |
| Styling | {e.g., Tailwind CSS v4} | {Rationale} |
| Components | {e.g., shadcn/ui} | {Rationale} |
| Hosting | {e.g., Vercel} | {Rationale} |
| Forms | {e.g., Nodemailer} | {Rationale} |

---

## Expected Outcomes

| Metric | Current | Target | Impact |
|--------|---------|--------|--------|
| Performance | 43 | 90+ | Faster load → better conversion |
| Accessibility | 67 | 95+ | WCAG AA compliance, wider reach |
| SEO | 72 | 95+ | Better rankings, more organic traffic |
| Mobile | Partial | Full | {X}% of traffic is mobile |

---

## Timeline

{Gantt-style overview}

| Phase | Weeks | Deliverables |
|-------|-------|-------------|
| Foundation | 1-2 | Content migrated, project scaffolded |
| Implementation | 3-6 | All pages implemented and responsive |
| QA | 7-8 | All audits passing, issues resolved |
| Launch | 9 | Live on production |

---

## Investment

{Optional — include if user provides budget context}

| Item | Description |
|------|------------|
| Website redesign | {Scope summary} |
| SEO migration | Redirect mapping, sitemap, structured data |
| Quality assurance | Cross-browser, a11y, performance |
| Post-launch support | {X} weeks monitoring |

---

## Next Steps

1. Review this proposal
2. Alignment meeting to discuss scope and priorities
3. Kick-off upon agreement
```

### Step 4: Generate Supporting Materials

Alongside the main proposal, generate:

- **proposal-data/{prospect}/audit-summary.md** — Raw audit findings for internal reference
- **proposal-data/{prospect}/screenshots/** — Annotated screenshots of current issues
- **proposal-data/{prospect}/competitor-notes.md** — Optional: quick scan of 1-2 competitors for comparison

## Customization

The proposal adapts based on engagement type:

| Type | Focus areas | Key sections |
|------|------------|-------------|
| **Redesign** | Design, UX, performance | Before/after mockups, design direction |
| **Migration** | Content parity, SEO, redirects | Redirect map, content inventory, SEO plan |
| **Optimization** | Performance, a11y, SEO | Current vs target metrics, ROI estimates |
| **New build** | Tech stack, architecture, features | Feature list, wireframes, tech rationale |

## Agent Team Integration

In the `website-refactor` workflow, the proposal is generated in Phase 1 by the Lead using data from `content-extractor`. It serves as the spec document that the user approves before implementation begins.

## Standalone Usage

- **Sales prospecting**: "Audit prospect.com and generate a proposal showing what we'd fix"
- **Scoping**: "Analyze this site and estimate the work needed for a redesign"
- **Upselling**: "The client hired us for SEO — generate a proposal showing what else needs work"
