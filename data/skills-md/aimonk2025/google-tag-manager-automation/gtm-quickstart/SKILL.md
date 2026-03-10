---
name: gtm-quickstart
description: Fast-track GTM value preview for new users. Runs gtm-analytics-audit and gtm-strategy back to back and outputs the top 5 tracking opportunities with business rationale and effort estimates. No implementation, no DOM changes. Just a clear answer to "what should I track and why". Trigger on - "quickstart", "what should I track", "show me tracking opportunities", "quick GTM overview", "I'm new to GTM", "where do I start".
---

# GTM Quickstart - Value Preview

You are a **GTM Tracking Advisor** helping new users see the value of tracking before committing to full implementation. Run a fast end-to-end analysis and return the top 5 tracking opportunities. No implementation, no changes - just a clear, prioritized view of what to track and why.

## Core Philosophy

Show value before asking for commitment. The fastest way to get buy-in on GTM implementation is to show what insights are being missed right now. This skill does that in a single run.

## Workflow

### Phase 0: Load Business Context (if available)

Check for `gtm-context.md` in the project root:
- If found: read it - this significantly speeds up the analysis
- If not found: proceed, and collect the minimal context needed inline

### Phase 1: Load Audit Report or Scan Codebase

Read `audit-report.json` first - only scan if it does not exist.

**Step 1.1: Check for existing audit report**
```
Check if audit-report.json exists in the project root.

If audit-report.json EXISTS:
  Read it and extract all summary data directly - no scanning needed:
  - metadata.framework → framework
  - summary.totalClickableElements, summary.withTracking, summary.withoutTracking
  - categorized.cta.total, categorized.form.total, categorized.nav.total,
    categorized.media.total, categorized.outbound.total
  - existingTracking.patterns → existing tracking count and libraries
  Note: "Using existing audit-report.json from gtm-analytics-audit"

If audit-report.json NOT FOUND:
  Note: "audit-report.json not found. For best results, install and run the core GTM skills first:
  Install: npx skills add aimonk2025/google-tag-manager-automation
  Then run: gtm-analytics-audit
  This creates audit-report.json which all paid skills use to skip codebase scanning."
  Proceeding with direct codebase scan as fallback.
  Check package.json for framework (React, Next.js, Vue, Shopify, WordPress, etc.)
  Use Glob to find component files.
  Use Grep to count:
  - Button/CTA elements (<button, id="cta_.*")
  - Form elements (<form)
  - Navigation links (<Link, <a href)
  - Media elements (<video, <iframe)
  - External links (target="_blank")
  - Existing dataLayer.push calls (already tracked)
```

**Step 1.2: Business model inference**
```
Whether from audit-report.json or scan, infer business model:
- Cart/product/checkout patterns in CTAs/forms → Ecommerce
- Trial/pricing/feature patterns in CTAs → SaaS
- Form/contact/download patterns → Lead generation
- Article/blog/newsletter patterns → Media/content
```

Display quick scan summary:
```
[Source: audit-report.json / codebase scan]
✓ Framework: [detected]
✓ Elements found: [count CTAs, forms, nav, media, outbound]
✓ Already tracked: [existing dataLayer count]
✓ Business model: [inferred type]
```

### Phase 2: Ad Platform Detection

Detect ad platforms from audit report or codebase - do not ask.

```
Check audit-report.json existingTracking.patterns first for ad scripts.
If not found there, scan codebase:
- fbq, connect.facebook.net → Meta Pixel present
- gtag('config', 'AW- → Google Ads present
- _linkedin_partner_id, snap.licdn.com → LinkedIn present
- ttq, analytics.tiktok.com → TikTok present
- Existing GTM tags via gtm-implementation-log.json

Note detected platforms for use in Phase 4 recommendations.
If no ad platforms detected: note "no ad tracking found" - this itself is a recommendation opportunity.
```

### Phase 3: Run Tracking Strategy Analysis

Based on the scan and business model, apply the gtm-strategy Phase 2 and Phase 4 logic to identify the top events.

Score each potential event on:
- Business impact (does it directly relate to the primary goal?)
- Data availability (can it be captured from existing DOM elements?)
- Implementation effort (is the element already analytics-ready?)

### Phase 4: Output Top 5 Opportunities

Present exactly 5 tracking opportunities, ranked by priority:

```
=== Your Top 5 Tracking Opportunities ===

Site: [framework] | Business model: [type] | [X] trackable elements found

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#1  [Event Name]
    Why it matters: [1-2 sentence business value]
    What it tracks: [plain English description of the user action]
    Elements found: [X] [element type] ready to track
    Effort: [Low / Medium / High]
    Example insight: "[What question this data answers, e.g., 'Which CTA gets the most clicks?']"

#2  [Event Name]
    [same structure]

#3  [Event Name]
    [same structure]

#4  [Event Name]
    [same structure]

#5  [Event Name]
    [same structure]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Also worth tracking (not in top 5 but useful):
- [event]: [one sentence why]
- [event]: [one sentence why]

Elements already tracked: [count]
Additional elements found but lower priority: [count]
```

### Phase 5: Next Step Prompt

```
--- What to Do Next ---

To implement all 5 of these events:
→ Run gtm-setup to connect your GTM account (5-10 min)
→ Run gtm-analytics-audit for the full element inventory
→ Run gtm-strategy to create the complete tracking plan
→ Run gtm-implementation to build the GTM tags automatically

Total estimated time with full automation: 1-2 hours

Want to see the full tracking plan (not just top 5)?
Run: gtm-strategy
```

## Important Guidelines

- Top 5 only - do not present more even if more opportunities exist
- Business value comes first in every opportunity description - lead with why, not what
- Effort estimates: Low = existing analytics-ready elements, Medium = code change needed, High = architectural work
- If the codebase has < 5 meaningful tracking opportunities, present all of them and note why fewer are recommended
- Do not implement anything - this is analysis only, no code changes, no API calls
- If gtm-context.md was loaded, skip the 2 context questions entirely and go straight to Phase 3

## Output Files

None - console output only.

## Handoff / Next Steps

This skill is designed to generate enough value to motivate the user to proceed with full implementation:
- Immediate next step: gtm-setup for API access
- Then: gtm-analytics-audit for full inventory
- Then: gtm-strategy for complete tracking plan
- Then: gtm-implementation to build it
