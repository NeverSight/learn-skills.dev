---
name: web-perf-ux
description: Web application performance and UX optimization through automated analysis. Use when developers need to (1) measure and diagnose performance issues using Lighthouse and Core Web Vitals, (2) identify root causes of LCP, CLS, INP problems, (3) analyze UX pain points like layout shifts or slow interactivity, (4) generate actionable improvement plans with concrete code-level fixes. Triggers on requests like "analyze performance", "why is my page slow", "fix CLS issues", "optimize web vitals", "run Lighthouse", "performance audit", or "improve page speed".
user-invocable: true
argument-hint: [URL]
allowed-tools: WebSearch
---

# Web Performance & UX Optimization

End-to-end workflow: **measure → analyze → explain → plan → execute**

## Preflight Checklist

Before starting, verify:

1. **Playwright MCP** - Browser automation available
   - Test: `browser_navigate` to target URL works
   - If unavailable: User must configure Playwright MCP server

2. **Lighthouse CLI** - Performance measurement
   - Test: `lighthouse --version`
   - Install if missing: `npm install -g lighthouse`

3. **Target URL accessible**
   - Production/staging preferred for reliable metrics
   - Local dev works but label results as "non-prod environment"

## Workflow

### 1. Measure

**Primary: Lighthouse CLI**

Run via `scripts/lighthouse-runner.sh`:
```bash
./lighthouse-runner.sh https://example.com           # Mobile (default)
./lighthouse-runner.sh https://example.com --desktop # Desktop
./lighthouse-runner.sh http://localhost:3000 --no-throttling  # Local dev
```

**Secondary: Real-time Web Vitals via Playwright**

Inject `scripts/collect-vitals.js` for interaction-based metrics:
```javascript
// Navigate and inject
await page.evaluate(collectVitalsScript);
// Interact with page...
// Retrieve metrics
const vitals = await page.evaluate(() => window.__GET_VITALS_SUMMARY__());
```

Use Playwright collection when:
- Testing specific user flows (not just page load)
- Measuring INP on real interactions
- Debugging CLS sources during navigation

### 2. Analyze

Parse Lighthouse JSON for:
- Performance score and individual metric values
- Failed audits with estimated savings
- Diagnostic details (render-blocking resources, unused JS, etc.)

Cross-reference with:
- **CWV thresholds** → See `references/core-web-vitals.md`
- **Known issue patterns** → See `references/common-issues.md`

**Framework-specific analysis:**
- Next.js apps → See `references/nextjs.md`
- React apps → See `references/react.md`

### 3. Explain (Generate Report)

Output markdown report with this structure:

```markdown
# Performance & UX Report

**Target:** [URL]
**Environment:** [Production | Staging | Local Dev*]
**Device:** [Mobile | Desktop]
**Date:** [timestamp]

*Local dev results may not reflect production performance

## Executive Summary

Top 3 issues with expected impact:
1. [Issue] → [Expected improvement]
2. [Issue] → [Expected improvement]
3. [Issue] → [Expected improvement]

## Scorecard

| Metric | Value | Rating | Target |
|--------|-------|--------|--------|
| Performance | X/100 | 🟡 | ≥90 |
| LCP | Xs | 🔴 | ≤2.5s |
| CLS | X.XX | 🟢 | ≤0.1 |
| INP | Xms | 🟡 | ≤200ms |
| FCP | Xs | | ≤1.8s |
| TTFB | Xms | | ≤800ms |

Rating: 🟢 Good | 🟡 Needs Improvement | 🔴 Poor

## Findings

### Finding 1: [Title]

**Evidence:**
- [Lighthouse audit / metric value / observation]

**Root Cause:**
- [Technical explanation of why this happens]

**Fix Proposal:**
- [Specific code/config change]
- [File(s) likely affected]

**Verification:**
- [How to confirm the fix worked]

### Finding 2: ...

## Quick Wins vs Strategic Fixes

### Quick Wins (< 1 hour, high confidence)
- [ ] [Action item]
- [ ] [Action item]

### Strategic Fixes (requires planning)
- [ ] [Action item with complexity note]

## Re-test Plan

After implementing fixes:
1. Run Lighthouse again with same configuration
2. Compare: [specific metrics to watch]
3. Expected improvements: [quantified targets]
```

### 4. Plan (Create Tasks)

Convert findings to tasks using Plan/Task tools:

**Task structure:**
```
Subject: [Action verb] [specific target]
Description:
  - Rationale: [why this matters, linked to finding]
  - Files/Areas: [likely locations to modify]
  - Acceptance Criteria: [measurable outcome]
  - Re-measure: [how to verify improvement]
```

**Prioritization:**
1. **Impact** (CWV improvement potential)
2. **Confidence** (certainty the fix will help)
3. **Category** labels: `Hydration/SSR`, `Images`, `JS Bundle`, `Fonts`, `CSS`, `Caching`, `Third-Party`

**Example tasks:**
```
High Priority:
1. [Images] Add width/height to hero image
   - Impact: CLS 0.15 → <0.1
   - Files: components/Hero.tsx
   - Verify: CLS audit passes

2. [JS Bundle] Lazy load chart component
   - Impact: TBT -200ms, LCP -0.5s
   - Files: pages/dashboard.tsx
   - Verify: Main bundle <200KB

Medium Priority:
3. [Fonts] Preload critical font
   - Impact: FCP -100ms
   - Files: app/layout.tsx
```

## Environment Notes

### Production/Staging (Recommended)
- Metrics reflect real CDN, caching, compression
- Use throttled Lighthouse (default) for user-representative results

### Local Development
- **Always label** results as "Local Dev Environment"
- Use `--no-throttling` flag
- Useful for: regression testing, debugging specific issues
- Not reliable for: absolute performance numbers, TTFB, caching

## When to Use Each Reference

| Situation | Reference File |
|-----------|----------------|
| Understanding metric thresholds | `core-web-vitals.md` |
| Identifying root cause of issue | `common-issues.md` |
| Next.js-specific optimizations | `nextjs.md` |
| React patterns (any framework) | `react.md` |

## Optional: Implementation Mode

By default, stop at plan + task list. If user requests implementation:

1. Confirm scope of changes
2. For high-confidence fixes, provide specific code patches
3. Still require user approval before applying
4. Re-run measurement after changes to verify
