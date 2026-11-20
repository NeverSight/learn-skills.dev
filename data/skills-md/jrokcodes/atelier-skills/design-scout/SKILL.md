---
name: design-scout
description: Live research skill that discovers current UI trends, new components, and design patterns before each build. Searches Magic UI, shadcn, Tremor, Dribbble, and GitHub for the latest premium techniques. Run this BEFORE building to stay current.
allowed-tools: WebSearch, WebFetch, Read, Write
---

# Design Scout

## TL;DR (3 rules)
1. **Run before every new build** — UI trends move fast. What was premium 3 months ago is template-tier now.
2. **Output 3-5 specific, actionable findings** — not a listicle. Each finding must include: what it is, why it's relevant, and how to implement it.
3. **Check component libraries for new releases** — Magic UI, shadcn, Tremor all ship new components monthly.

## When To Use
- Starting any new frontend project
- Client says "make it look modern" or "cutting edge"
- It's been 30+ days since the last frontend build
- You need to differentiate from what you've already built

---

## Scout Protocol

### Step 1: Check Component Library Updates (~3 min)

Search for recent additions to the three core libraries:

```
WebSearch: "magic ui new components 2026" OR "magicui.design changelog"
WebSearch: "shadcn ui new components 2026" OR "ui.shadcn.com changelog" 
WebSearch: "tremor react new components" OR "tremor.so changelog"
```

For each library, note:
- Any new components released in the last 60 days
- Components relevant to the current project type (dashboard, landing page, etc.)
- Breaking changes that affect existing patterns

### Step 2: Industry-Specific Trends (~3 min)

Search for current design patterns in the client's industry:

```
WebSearch: "best [industry] dashboard design [current year]"
WebSearch: "[industry] UI design trends [current month] [current year]"
WebSearch: "dribbble [industry] dashboard" OR "behance [industry] UI"
```

Industries to search for:
- **Finance/Commission**: "financial dashboard", "commission tracking UI", "payment dashboard"
- **Healthcare**: "patient portal design", "EHR dashboard", "health tech UI"
- **SaaS**: "SaaS dashboard design", "admin panel UI", "analytics dashboard"
- **E-commerce**: "shopify dashboard", "order management UI"

### Step 3: Premium Technique Discovery (~3 min)

Search for the latest "premium" techniques that distinguish high-quality from template-tier:

```
WebSearch: "premium dashboard UI techniques [current year]"
WebSearch: "dark mode dashboard design tips"
WebSearch: "micro-interactions dashboard [current year]"
WebSearch: "github dashboard react tailwind stars:>500 pushed:>[last 6 months]"
```

Look specifically for:
- New animation patterns (scroll-driven, view transitions API, etc.)
- New typography trends (variable fonts, kinetic type)
- New color approaches (oklch, P3 gamut, adaptive palettes)
- New component patterns (bento grids, command palettes, AI-generated layouts)

### Step 4: Open Source Dashboard Audit (~2 min)

Check the top open-source dashboards for new patterns:

```
WebSearch: "github shadcn dashboard 2026 stars"
WebSearch: "github admin dashboard react stars:>1000"
```

Key repos to track:
- `satnaing/shadcn-admin` (11.7k stars) — most polished free shadcn dashboard
- `twentyhq/twenty` (43.8k stars) — Linear-inspired CRM
- `tremorlabs/tremor` — dashboard-native components

---

## Output Format

Write findings to the project folder as `DESIGN-SCOUT-REPORT.md`:

```markdown
# Design Scout Report — [Project Name]
**Date:** [current date]
**Industry:** [client industry]
**Project type:** [dashboard / landing page / etc.]

## Finding 1: [Specific technique or component]
**What:** [Description]
**Why it matters:** [How it applies to this project]
**How to implement:** [Specific code or library reference]
**Source:** [URL]

## Finding 2: ...

## Finding 3: ...

## Library Updates
- Magic UI: [new components since last check]
- shadcn/ui: [new components]
- Tremor: [new components]

## Recommended Stack for This Build
Based on findings, use: [specific recommendations]
```

---

## Integration with Creative Director

The design-scout skill runs as Phase 0 of the creative-director's workflow:

```
1. design-scout (research what's current)
2. reference-analysis (analyze client references)
3. design-advisor (create DESIGN-BRIEF.md)
4. frontend-master (build with anti-slop enforcement)
5. premium-layer (apply the premium techniques)
6. screenshot-loop (QA verification)
```

This ensures every build starts with current knowledge, not stale patterns from 3 months ago.
