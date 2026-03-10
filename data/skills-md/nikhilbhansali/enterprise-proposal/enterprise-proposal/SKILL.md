---
name: enterprise-proposal
description: Create comprehensive, BCG/McKinsey-style enterprise proposals with professional formatting, data-driven insights, and conversion-focused structure. Use when creating client proposals, service agreements, project pitches, rate cards, or business development documents. The skill guides information gathering (testimonials, experience, statistics, timelines, costs, add-ons, team profiles) and outputs professionally structured proposals using tables, tiered pricing, ROI projections, and executive-ready formatting. Triggers include requests for "proposal", "pitch deck", "service agreement", "rate card", "client quote", "business proposal", "create a proposal", or "draft a proposal for [client]".
license: MIT
metadata:
  author: nikhilbhansali
  version: "1.0.0"
  argument-hint: <client-name-or-context>
---

# Enterprise Proposal Builder

Create BCG/McKinsey-quality proposals with professional structure, data tables, and conversion-focused content.

## When to Apply

Use this skill when:
- Creating client proposals or service agreements
- Building pitch decks or rate cards
- Drafting business development documents
- Responding to RFPs or project inquiries
- Creating pricing packages or investment summaries

## Before You Start: Context Required

**Important:** Before generating the proposal, gather comprehensive context. The more context provided upfront, the better the proposal.

### Essential Context Checklist

| Category | Details Needed |
|----------|----------------|
| **Client Info** | Company name, industry, size, decision maker(s), existing relationship |
| **Problem/Opportunity** | What challenge are we solving? Why now? |
| **Services** | What are we proposing? Scope and deliverables |
| **Budget/Pricing** | Target budget, preferred tier, currency |
| **Timeline** | Start date, milestones, duration, urgency |
| **Credibility** | Relevant case studies, team to highlight, specific experience |
| **Competition** | Who else are they considering? Key differentiators needed |
| **Add-Ons** | Optional services to include? |
| **Terms** | Special conditions, payment terms, guarantees |
| **Testimonials** | Any client-specific testimonials or references? |
| **Statistics** | Any specific metrics, benchmarks, or data to include? |

**Tip:** Paste discovery call notes, email threads, or any background documents for maximum context.

## Proposal Creation Workflow

### Step 1: Information Gathering

Review provided context first. Use AskUserQuestion only for critical missing details.

**Batch 1: Client & Opportunity**
| Information | Purpose |
|-------------|---------|
| Client name and industry | Personalization and positioning |
| Decision maker name(s) and title(s) | Proposal addressing |
| Core problem/challenge | Frame the narrative |
| Services being proposed | Scope definition |
| Budget range or tier preference | Right-size the offer |

**Batch 2: Credibility Elements**
| Information | Purpose |
|-------------|---------|
| Relevant case studies | Social proof |
| Team members to highlight | Build trust |
| Experience metrics (years, projects, clients) | Establish authority |
| Existing client relationship | Warm vs cold context |

**Batch 3: Engagement Specifics**
| Information | Purpose |
|-------------|---------|
| Timeline and milestones | Set expectations |
| Pricing structure | Commercial terms |
| Add-on services | Upsell opportunities |
| Special terms/conditions | Flexibility |

### Step 2: Research (When Applicable)

Before writing, gather relevant data:

| Data Type | Source | When to Use |
|-----------|--------|-------------|
| Market data | Web search, industry reports | Market sizing, benchmarks |
| Competitor info | Web search, analysis tools | Positioning |
| Industry benchmarks | Research, case studies | ROI projections |
| Similar proposals | Internal templates | Pricing reference |

### Step 3: Generate Proposal

Follow the structure template below. Apply professional formatting guidelines.

## Key Principles

### 1. Data Integrity (Critical)
- **NEVER fabricate statistics** - use real data or mark as "estimated"
- Use verified case studies only
- When data unavailable, state "industry benchmark" or "estimated range"

### 2. Professional Formatting
- Use **tables** for pricing, comparisons, timelines, deliverables
- Use **headers and sections** for clear navigation
- Include **table of contents** for proposals >10 pages
- **Bold** key numbers, metrics, and recommendations

### 3. Conversion Focus
- Lead with client's problem, not services
- Quantify ROI wherever possible
- Include clear next steps and CTAs
- Make signing feel like the obvious choice

### 4. Narrative Structure
- Tell a story: Current State → Problem → Solution → Outcome
- Use the "Why Now" urgency framework
- Address objections proactively
- End with clear, time-bound call to action

## Proposal Structure Template

### Standard Sections

```
1. Cover Section
   - Client name, service type, date, version

2. Table of Contents (for proposals >10 pages)

3. Executive Summary
   - The opportunity (1-2 sentences)
   - The recommendation (high level)
   - Investment overview table
   - Break-even analysis

4. Current Situation Analysis
   - Metrics table (current vs benchmark vs gap)
   - Critical issues identified
   - What's working (do more of this)

5. Market Opportunity
   - Market size and trends table
   - Competitive position analysis
   - Target audience profiles

6. Recommended Strategy
   - Multi-pillar approach (e.g., 3 pillars)
   - Content/activity mix table
   - Implementation priorities

7. Service Breakdown & Deliverables
   - Monthly deliverables by tier
   - Sample calendar/schedule

8. Investment Options
   - Tiered packages (Starter, Growth, Premium)
   - ROI calculations per tier
   - Recommended option with rationale

9. Timeline & Implementation
   - 90-day launch plan with phases
   - Expected results timeline

10. Why [Your Company]
    - Track record table
    - Differentiators
    - Guarantees

11. Next Steps
    - Action items list
    - Requirements from client
    - Timeline to launch table

12. Contact & Terms
    - Contact information
    - Terms and conditions
    - Validity period
```

## Pricing Table Formats

### Tiered Service Packages

```markdown
| Feature | Starter | Growth ⭐ | Premium |
|---------|---------|----------|---------|
| **Monthly Investment** | $X | $X | $X |
| Deliverable 1 | X/month | X/month | X/month |
| Deliverable 2 | Basic | Advanced | Full |
| Support Level | Email | Dedicated | Premium |
| **Best For** | Testing | Scaling | Enterprise |
```

### Add-On Services

```markdown
| Service | Price | Best For |
|---------|-------|----------|
| Service name | $X/unit | Use case |
| Rush delivery | +X% | Time-sensitive |
| Additional scope | $X/item | Expansion |
```

### ROI Calculation

```markdown
| Metric | Current | Target (6 Mo) | Value Created |
|--------|---------|---------------|---------------|
| Monthly leads | X | Y | +Z% increase |
| Cost per lead | $X | $Y | -Z% reduction |
| Close rate | X% | Y% | +Z% improvement |
| **Revenue impact** | - | **$X/month** | **$Y/year** |
```

### Investment Summary

```markdown
| Component | Investment | Notes |
|-----------|------------|-------|
| One-time setup | $X | Foundation work |
| Monthly retainer | $X/month | Ongoing services |
| Ad spend (if applicable) | $X-Y/month | Paid to platforms |
| **Total (Month 1)** | **$X** | Setup + first month |
| **Ongoing monthly** | **$X** | After setup |
```

## Proposal Length Guidelines

| Type | Pages | Sections | Use Case |
|------|-------|----------|----------|
| Quick Quote | 2-4 | Summary, Pricing, Terms | Small projects |
| Standard | 8-15 | Full structure | Most proposals |
| Enterprise | 15-30 | Full + Appendices | Large deals, RFPs |
| Comprehensive | 30+ | Full + Detailed appendices | Complex projects |

## Formatting Guidelines

### Typography & Emphasis
- **Bold** for package names, key metrics, recommendations
- *Italics* for purpose statements, notes, caveats
- Title Case for main headers
- ALL CAPS only for acronyms (ROI, SEO)

### Tables
- Include recommendation marker (⭐) for preferred option
- Bold totals and key rows
- Use checkmarks (✓) and dashes (-) for feature inclusion

### Visual Hierarchy
- `##` for main sections
- `###` for subsections
- Horizontal rules (`---`) between major sections
- Numbered lists for sequential steps
- Bulleted lists for non-sequential items

### Status Indicators
- ✅ Complete/Included
- ⚠️ Needs attention
- ❌ Not available
- ⭐ Recommended

## Output Specifications

### File Format
- Output as Markdown (.md)
- Proper headers for hierarchy
- Tables for all data comparisons
- Horizontal rules between major sections

### File Naming
`[ClientName]_[ServiceType]_Proposal_[YYYYMMDD].md`

Examples:
- `Acme_Corp_Marketing_Proposal_20260128.md`
- `TechStart_Consulting_Proposal_20260128.md`

## Credibility Section Template

### Track Record Table

```markdown
| Client | Before | Current | Impact |
|--------|--------|---------|--------|
| [Client 1] | [Metric] | [Metric] | [% change] |
| [Client 2] | [Metric] | [Metric] | [% change] |
```

### Differentiators Format

```markdown
1. **[Differentiator 1]**
   - [Evidence/explanation]

2. **[Differentiator 2]**
   - [Evidence/explanation]
```

### Guarantees Format

```markdown
- **[Guarantee Name]:** "[Specific promise]"
- **[Guarantee Name]:** "[Specific promise]"
```

## Call-to-Action Formatting

### Primary CTA (End of Proposal)

```markdown
---

**Ready to [achieve outcome]?**

**[Schedule Your Call](link)** | **[Email Us](mailto:)**

---

*This proposal is valid for 30 days from the date of issue.*
```

## Quick Reference

| Element | Format |
|---------|--------|
| Currency (US) | $1,000 or $1.2M |
| Currency (EU) | €1,000 or €1.2M |
| Percentages | 25% or +25% / -25% |
| Large numbers | 1K, 1M, or spelled out |
| Recommendations | ⭐ after name |
| Included features | ✓ |
| Not included | - |
| Bold emphasis | **key terms** |
