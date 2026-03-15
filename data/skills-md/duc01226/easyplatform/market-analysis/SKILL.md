---
name: market-analysis
version: 1.0.0
description: '[Research] Analyze market landscape: competitors, sizing (TAM/SAM/SOM), trends, SWOT, customer segments. Use for marketing or business evaluation.'
allowed-tools: Read, Write, WebSearch, WebFetch, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/web-research-protocol.md`

## Quick Summary

**Goal:** Analyze market landscape with competitive analysis, sizing, trends, SWOT, and customer segmentation.

**Workflow:**

1. **Define scope** — Industry, geography, segment, timeframe
2. **Research competitors** — WebSearch for players, positioning, strengths/weaknesses
3. **Size the market** — TAM/SAM/SOM from industry reports
4. **Identify trends** — Growth drivers, disruptions, regulatory changes
5. **SWOT analysis** — Synthesize Strengths/Weaknesses/Opportunities/Threats
6. **Segment customers** — Demographics, psychographics, jobs-to-be-done

**Key Rules:**

- Prefer Tier 1-2 sources for market sizing
- Every market size claim must cite source + methodology
- SWOT items linked to evidence, not speculation

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Market Analysis

## Step 1: Define Market Scope

Clarify with user:

- **Industry/vertical** — What market segment?
- **Geography** — Global, regional, or local?
- **Timeframe** — Current state? 3-year projection?
- **Focus** — B2B, B2C, or both?

## Step 2: Competitive Research

For each competitor (identify 5-10):

| Field                       | Source                       |
| --------------------------- | ---------------------------- |
| Company name                | WebSearch                    |
| Positioning/tagline         | Company website              |
| Key products                | Product pages                |
| Pricing model               | Pricing page or reports      |
| Strengths                   | Reviews, analyst reports     |
| Weaknesses                  | Reviews, customer complaints |
| Market share (if available) | Industry reports             |

## Step 3: Market Sizing

Use Tier 1-2 sources (Gartner, Statista, IBISWorld, government data):

- **TAM** (Total Addressable Market) — Maximum possible revenue if 100% market share
- **SAM** (Serviceable Addressable Market) — Portion accessible given constraints
- **SOM** (Serviceable Obtainable Market) — Realistic capture in 3 years

Every number must cite: source, year, methodology.

## Step 4: Trend Analysis

Research and categorize:

- **Growth drivers** — What's fueling market growth?
- **Disruptions** — Technology shifts, new entrants, business model innovations
- **Regulatory** — New laws, compliance requirements, policy changes
- **Consumer behavior** — Changing preferences, demographics shifts

## Step 5: SWOT Analysis

Each item must link to evidence:

| Category        | Item   | Evidence   |
| --------------- | ------ | ---------- |
| **Strength**    | {item} | Source [N] |
| **Weakness**    | {item} | Source [N] |
| **Opportunity** | {item} | Source [N] |
| **Threat**      | {item} | Source [N] |

## Step 6: Customer Segmentation

For each segment:

- **Demographics** — Age, role, income, company size
- **Psychographics** — Values, pain points, aspirations
- **Behavior** — Buying patterns, media consumption
- **Jobs-to-be-Done** — What are they trying to accomplish?

## Output

Market analysis is typically consumed by:

- `strategy-builder` skill (marketing strategy)
- `business-evaluation` skill (business viability)

Write findings to working file or inline with consuming skill's output.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements
