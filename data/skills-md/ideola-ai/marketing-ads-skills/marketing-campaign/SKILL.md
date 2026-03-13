---
name: marketing-campaign
description: Plan comprehensive ad campaigns with strategy, audience segmentation, creative angles, and measurement framework. Use when user asks to create ad campaign, paid media strategy, advertising plan, or campaign architecture. Triggers on - "campaign planning", "ads strategy", "iklan", "/campaign" command, or requests to plan paid advertising with targeting and creatives.
---

# Ad Campaign Planning

## Overview

This skill creates comprehensive paid advertising campaign strategies including audience segmentation, creative angles, testing frameworks, and measurement plans. It transforms brief outputs into actionable campaign architectures.

## Marketing OS Workflow Position

```
brand-voice → content-brief → content-planning → content-creation
                                          ↓
                                        marketing-campaign
                                          ↓
                                          ads-audit
```

**This skill is FIFTH** - Plan campaigns after brief (can run parallel with content-planning), before auditing ads.

**Input from:**
- `/brand-voice` - Brand attributes and messaging consistency
- `/content-brief` - Audience, angles, messaging, visual direction

**Output for:**
- `/ads-audit` - Campaign structure and KPIs become baseline for audit

## Workflow

### Step 1: Gather Campaign Context

Before planning, collect these inputs:

**From Brief (if available):**
- Target audience profiles
- Content angles and key messages
- Platform strategy
- Visual direction

**Campaign-Specific Information:**
- Campaign objective (awareness, consideration, conversion, retention)
- Budget range
- Campaign duration
- Target platforms for ads
- Success metrics/KPIs

**Ask if not provided:**
1. Apa objective utama campaign ini (awareness/consideration/conversion)?
2. Berapa range budget yang tersedia?
3. Berapa lama campaign akan jalan?
4. Platform ads apa yang akan dipakai?
5. Apa KPI utama yang mau dicapai?

### Step 2: Define Campaign Architecture

See `rules/architecture.md` for campaign structure frameworks.

### Step 3: Audience Segmentation

See `rules/audience.md` for targeting strategies.

### Step 4: Develop Creative Angles

See `rules/creative.md` for ad creative frameworks.

### Step 5: Define Testing Framework

See `rules/testing.md` for A/B testing strategies.

### Step 6: Create Measurement Plan

See `rules/measurement.md` for KPI and analytics setup.

## Output Structure

```markdown
# [Brand/Campaign] Ad Campaign Strategy

## Campaign Overview
- **Objective:** [Awareness/Consideration/Conversion/Retention]
- **Budget:** [Amount]
- **Duration:** [Timeframe]
- **Platforms:** [Ad platforms]

## Campaign Architecture
[From Step 2]

## Audience Segmentation
[From Step 3]

## Creative Strategy
[From Step 4]

## Testing Framework
[From Step 5]

## Measurement Plan
[From Step 6]

## Campaign Calendar
[Weekly breakdown]

## Budget Allocation
[By platform and audience]
```

## Platform-Specific Campaign Guidelines

See `rules/` folder for:
- `rules/platforms/meta-ads.md` - Facebook & Instagram
- `rules/platforms/tiktok-ads.md` - TikTok
- `rules/platforms/linkedin-ads.md` - LinkedIn
- `rules/platforms/google-ads.md` - Google Ads

## Best Practices

1. **Start with objective** - Everything flows from campaign goal
2. **Test everything** - Assume nothing, test hypotheses
3. **Budget for learning** - First 20-30% is learning phase
4. **Iterate quickly** - Weekly optimizations minimum
5. **Document learnings** - What works, what doesn't

## Common Campaign Types

### Awareness Campaign
- **Goal:** Maximum reach and impressions
- **KPI:** CPM, reach, brand lift
- **Strategy:** Broad targeting, video views
- **Budget split:** 60% top of funnel

### Consideration Campaign
- **Goal:** Engagement and interest
- **KPI:** CPC, CTR, engagement rate
- **Strategy:** Mid-funnel audiences, carousel ads
- **Budget split:** 40% top, 60% mid funnel

### Conversion Campaign
- **Goal:** Actions and sales
- **KPI:** CPA, ROAS, conversion rate
- **Strategy:** Bottom funnel, retargeting
- **Budget split:** 30% mid, 70% bottom funnel

### Retention Campaign
- **Goal:** LTV and repeat purchases
- **KPI:** Retention rate, repurchase rate
- **Strategy:** Customer lists, loyalty messaging
- **Budget split:** 100% existing customers

## Integration with Marketing OS Workflow

**Input from:**
- `/brand-voice` - Brand attributes and messaging consistency
- `/content-brief` - Audience, angles, messaging, visual direction

**Output for:**
- `/ads-audit` - Campaign structure and KPIs become baseline for audit
- `/content-plan` - Organic content to complement paid
- `/content-creation` - Ad creative specifications

## Quick Start Example

```bash
# User runs:
/campaign

# Agent asks:
1. Objective? "Conversion - product launch"
2. Budget? "Rp 50 juta untuk 1 bulan"
3. Platform? "Meta ads (IG + FB)"
4. Target? "Sales untuk produk baru"

# Agent produces:
- Campaign architecture with ad sets
- Audience segmentation with targeting
- 5-7 creative angles with hooks
- Testing framework
- Budget allocation
- Measurement plan with KPIs
```
