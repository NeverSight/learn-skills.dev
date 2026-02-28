---
name: app-store-opportunity-research
description: Full-pipeline App Store opportunity research. Discovers underserved niches, analyzes competitor gaps, produces revenue-validated top-3 opportunity reports, writes MVP PRDs, and builds working prototypes on Rork (https://rork.com/?ref=frederik) — all automated through browser research.
metadata:
  tags: app-store, research, mobile-app, competitor-analysis, market-research, prd, prototype, rork, indie-hacker, startup
---

## When to Use

Use this skill when the user wants to:
- Find profitable app ideas in a category or niche
- Research App Store charts for underserved opportunities
- Analyze competitor apps (ratings, reviews, revenue, gaps)
- Generate a top-3 opportunity report with revenue validation
- Write a detailed MVP Product Requirements Document (PRD)
- Build a working prototype from the PRD on [Rork](https://rork.com/?ref=frederik)

Trigger phrases: "find app opportunities", "app store research", "what app should I build", "research this app category", "find a gap in the app store"

## Prerequisites

- **Chrome browser** with Claude in Chrome extension (for App Store browsing)
- **Rork account** at [rork.com](https://rork.com/?ref=frederik) (for prototype building, optional)
- No API keys required — all research is done through live browser interaction

## Pipeline Overview

```
App Store Charts → Competitor Deep-Dive → Gap Analysis → Top 3 Report → PRD → Rork Prototype
```

The entire pipeline can run end-to-end in a single session (~30-45 min).

---

## Step 1: Define the Category

Ask the user what space they want to explore. Help them narrow down:

- **Too broad:** "Health apps" (thousands of competitors)
- **Good:** "Sleep + anxiety apps for consumers" (specific intersection)
- **Good:** "Habit tracking for fitness beginners" (audience + niche)
- **Good:** "AI-powered journaling apps" (tech angle + category)

**Key questions to ask:**
1. What category or problem space interests you?
2. Consumer or B2B? (Consumer is easier to validate quickly)
3. Any budget constraints? (No-AI = cheaper to build, AI = higher ceiling)
4. Target revenue? ($1K/mo hobby vs $10K/mo business)

---

## Step 2: App Store Charts Research

Browse the App Store charts in the relevant category using Chrome:

1. **Navigate to:** `https://apps.apple.com/us/charts/iphone/{category-slug}/{category-id}`
   - Health & Fitness: `/health-fitness-apps/6013`
   - Lifestyle: `/lifestyle-apps/6012`
   - Productivity: `/productivity-apps/6007`
   - Education: `/education-apps/6017`
   - Medical: `/medical-apps/6020`
   - Entertainment: `/entertainment-apps/6016`

2. **Document the top 25-50 apps** noting:
   - App name and position
   - Rating count (proxy for install base)
   - Star rating
   - Price/monetization model
   - Brief description

3. **Identify patterns:**
   - Which apps have massive ratings (>100K)? These are saturated.
   - Which apps have moderate ratings (1K-50K)? Proven demand, beatable.
   - Which apps have low ratings (<500)? Possible new/underserved niche.

---

## Step 3: Competitor Deep-Dive

For each promising niche area, deep-dive into 5-8 competitor apps:

### Data to Collect Per App
| Field | How to Find |
|-------|------------|
| Name | App Store listing |
| Ratings count | App Store listing |
| Star rating | App Store listing |
| Price / subscription | App Store listing |
| Trustpilot score | Search `{app name} trustpilot` |
| Estimated revenue | Search `{app name} revenue` or use web research |
| Key features | App Store description / screenshots |
| Top complaints | 1-star App Store reviews, Trustpilot reviews |
| Missing features | Compare across competitors |

### Revenue Estimation Techniques
- **Direct sources:** Search "{app name} revenue", "{app name} ARR"
- **Proxy calculation:** `rating_count * 40-80 = approximate installs` (rule of thumb)
- **Industry benchmarks:** 2-5% of free users convert to paid
- **Comparable apps:** Find similar apps with known revenue

### Red Flags (Avoid These Niches)
- Top app has 1M+ ratings (dominated by a giant)
- Category requires hardware integration (Apple Watch data, etc.)
- Heavy regulation (medical devices, financial trading)
- All competitors are free with no monetization path

### Green Flags (Pursue These Niches)
- Top competitors have poor reviews (< 3.0 Trustpilot)
- Solo devs making $50K+/yr (proves indie viability)
- "Editors' Choice" app exists with < 20K ratings (Apple promotes the niche)
- Users complain about the same missing feature across multiple apps
- Clear $5-15/mo willingness to pay

---

## Step 4: Gap Analysis

Create a **feature comparison matrix** across the top competitors:

```markdown
| Feature | App A | App B | App C | App D | YOUR APP |
|---------|-------|-------|-------|-------|----------|
| Core Feature 1 | Yes | Yes | No | Yes | YES |
| Core Feature 2 | No | Yes | Yes | No | YES |
| Missing Feature | No | No | No | No | YES |
| Price | $14.99 | $9.99 | Free | $6.99 | $5.99 |
| UX Quality | Poor | Good | OK | Good | Premium |
```

The winning opportunity is where:
1. Multiple competitors exist (proven demand)
2. They all miss the same 1-2 features
3. Users vocally complain about the gap
4. Pricing is high enough to support indie revenue

---

## Step 5: Top 3 Opportunity Report

Produce a ranked report with this structure:

```markdown
# Top 3 App Opportunities in {Category}

## Opportunity 1: {App Name} (RECOMMENDED)
**One-line pitch:** {What it does in 10 words}
**The gap:** {What's missing in the market}
**Target user:** {Who and why they'd pay}
**Revenue model:** {Price point and conversion assumptions}
**Revenue path:** {How to reach $X/mo}
**Competition:** {Who exists, why you win}
**Build complexity:** {Low/Medium/High}
**Confidence:** {High/Medium/Low with reasoning}

## Opportunity 2: {App Name}
...

## Opportunity 3: {App Name}
...

## Recommendation
{Why #1 is the best bet, with specific reasoning}
```

**Present this to the user and get their pick before proceeding.**

---

## Step 6: Write the MVP PRD

Once the user selects an opportunity, write a comprehensive PRD with these sections:

1. **Executive Summary** — One paragraph pitch
2. **Market Opportunity** — Problem, market size, competitive landscape table, revenue validation
3. **Target Users** — 3 personas with name, age, job, pain points, willingness to pay
4. **MVP Feature Set** — 5-8 feature groups with detailed specs, UI behavior, edge cases
5. **Screen Map** — All screens listed with parent/child relationships
6. **User Flow** — Primary user journey from onboarding to daily use
7. **Monetization** — Free vs Premium feature split, pricing, trial strategy
8. **Tech Stack** — Framework, libraries, state management, persistence
9. **AI Features** — If applicable, what AI does and doesn't do
10. **Data Models** — TypeScript interfaces for core entities
11. **Design Direction** — Color palette (with hex codes), typography, component style, mood
12. **Launch Strategy** — Week 1-12 plan, marketing channels, content strategy
13. **Success Metrics** — KPIs with specific targets
14. **Risks & Mitigations** — Top 5 risks with solutions
15. **Compliance** — Privacy, data handling, App Store guidelines
16. **Future Roadmap** — V2, V3 features beyond MVP

**Save the PRD as:** `PRD-{AppName}.md`

---

## Step 7: Build on Rork (Optional)

If the user has a Rork account, build a working prototype:

1. **Navigate to** [rork.com](https://rork.com/?ref=frederik)
2. **Select model:** Opus 4.6 (or latest available)
3. **Write the prompt** — Condense the PRD into a detailed Rork prompt covering:
   - App name and purpose (1 sentence)
   - Design system (colors with hex codes, card styles, corner radii, typography)
   - Navigation structure (tab names, icons)
   - Each tab/screen with specific UI elements
   - Modal screens with full interaction specs
   - State management approach and mock data
   - Tech stack (Expo SDK, TypeScript, key libraries)
4. **Submit and monitor** the build (typically 5-10 min, 7-10 steps)
5. **Verify the preview** renders correctly (Cmd+R if stuck on loading)
6. **Share the project URL** with the user

### Rork Prompt Template

```
Build "{AppName}" — {one-line description}.

DESIGN: {Theme name}. Background: {color}. Cards: {style}.
Primary accent: {color}. Secondary accent: {color}.
Text: {color}. Corners: {radius}. Effects: {glow/shadow/glass}.

NAVIGATION: {N} tabs — {Tab1} ({icon}), {Tab2} ({icon}), ...

{TAB1 NAME} TAB:
- {Element 1 with full spec}
- {Element 2 with full spec}
...

{TAB2 NAME} TAB:
...

{MODAL SCREEN}:
...

STATE MANAGEMENT: {Approach}. Mock data for {N} days.

TECH: Expo SDK 52+, TypeScript, Expo Router, {styling}, {animations}.
```

---

## Revenue Validation Benchmarks

Use these benchmarks to reality-check opportunity viability:

| App Type | Solo Dev Benchmark | Small Team | Reference |
|----------|-------------------|------------|-----------|
| Niche utility | $1-5K/mo | $5-20K/mo | Rootd ($1M+ total, 1 person) |
| Habit/tracker | $5-15K/mo | $20-80K/mo | Daylio ($50K/mo) |
| Gamified self-care | $10-50K/mo | $100K+/mo | Finch ($2M/mo) |
| Meditation/wellness | $5-20K/mo | $50-500K/mo | Calm ($100M+/yr) |
| Productivity | $3-10K/mo | $20-100K/mo | Various |
| AI-powered tool | $5-30K/mo | $50-300K/mo | Emerging category |

## Pricing Sweet Spots (2025)

| Tier | Monthly | Annual | Best For |
|------|---------|--------|----------|
| Impulse buy | $2.99-4.99/mo | $19.99-29.99/yr | Simple utilities |
| **Standard** | **$5.99-6.99/mo** | **$34.99-44.99/yr** | **Most indie apps** |
| Premium | $9.99-14.99/mo | $59.99-99.99/yr | AI-heavy or professional |

## Marketing Channel Playbook

| Channel | Best For | Cost | Time to Results |
|---------|----------|------|-----------------|
| TikTok organic | Consumer apps, visual demos | Free | 2-4 weeks |
| Reddit (niche subs) | Technical/niche apps | Free | 1-2 weeks |
| Product Hunt | Productivity/dev tools | Free | Launch day spike |
| Apple Search Ads | Any iOS app | $0.50-3/tap | Immediate |
| Instagram Reels | Lifestyle/wellness apps | Free | 2-6 weeks |
| Twitter/X | Dev tools, indie hackers | Free | Ongoing |

---

## Example Session Output

A complete session produces:
1. **Category research notes** — charts analysis, competitor list
2. **Top 3 Opportunity Report** — ranked with revenue validation
3. **MVP PRD** — 16-section document with full specs
4. **Working prototype** — live on [Rork](https://rork.com/?ref=frederik) with shareable URL
5. **Go-to-market notes** — pricing, channels, launch plan

All in ~30-45 minutes of automated research and building.
