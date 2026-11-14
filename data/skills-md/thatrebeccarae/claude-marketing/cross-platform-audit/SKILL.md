---
name: cross-platform-audit
description: "Unified multi-platform paid media audit with parallel execution. Spawns scored audits for Google Ads, Meta Ads, and Microsoft Ads simultaneously, merges results into a budget-weighted aggregate health score (A-F), adds cross-platform analysis (budget allocation, tracking consistency, creative alignment, attribution overlap), and produces a prioritized action plan. Optionally generates a client-ready deck via pro-deck-builder. Use when the user asks for a full paid media audit, cross-platform review, or multi-channel ad assessment."
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: paid-media
  domain: cross-platform
  updated: 2026-03-16
  tested: 2026-03-17
  tested_with: "Claude Code v2.1"
---

# Cross-Platform Audit — Unified Paid Media Assessment

Orchestrates parallel scored audits across Google Ads, Meta Ads, and Microsoft Ads, then merges results into a single budget-weighted health score with cross-platform intelligence.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/cross-platform-audit ~/.claude/skills/
```

## Context Intake (Always Do First)

Before running audits, collect this information. Without it, benchmarks will be generic and recommendations may be wrong.

Ask these questions (combine into one prompt):

1. **Business type** — E-commerce/DTC, SaaS/B2B, Local Service, Lead Gen, Agency, Other
2. **Monthly ad spend** — Total and per-platform breakdown (approximate is fine)
3. **Primary goal** — Revenue/ROAS, Leads/CPA, App Installs, Brand Awareness
4. **Active platforms** — Which platforms are they advertising on? (Google, Meta, Microsoft, others)
5. **Data available** — What can they provide? (exports, screenshots, pasted metrics, MCP access)

Use the provided context to:
- Determine which platform audits to run (skip platforms they don't use)
- Calculate budget share per platform for aggregate scoring
- Calibrate severity based on spend level ($5K/mo gets different advice than $100K/mo)

## Orchestration Workflow

### Step 1: Collect Context
Gather business type, platforms, budgets, goals, and available data per the intake above.

### Step 2: Spawn Parallel Audits

Use the Task tool to run platform audits simultaneously. Each audit task should:

1. Load `skills/shared/scoring-system.md` for the scoring algorithm
2. Load the platform-specific `CHECKS.md` for the audit checklist
3. Load the platform-specific `SKILL.md` and `REFERENCE.md` for diagnostic context
4. Evaluate each applicable check as PASS, WARNING, or FAIL
5. Calculate the platform health score using weighted formula
6. Identify Quick Wins
7. Write results to a structured output

**Spawn these tasks in parallel** (adjust based on which platforms the user has):

```
Task 1: Google Ads Audit
  → Read skills/shared/scoring-system.md
  → Read skills/google-ads/CHECKS.md
  → Evaluate 74 checks against provided data
  → Calculate score → Write google-audit-results.md

Task 2: Meta Ads Audit
  → Read skills/shared/scoring-system.md
  → Read skills/facebook-ads/CHECKS.md
  → Evaluate 46 checks against provided data
  → Calculate score → Write meta-audit-results.md

Task 3: Microsoft Ads Audit
  → Read skills/shared/scoring-system.md
  → Read skills/microsoft-ads/CHECKS.md
  → Evaluate 30 checks against provided data
  → Calculate score → Write microsoft-audit-results.md
```

If the user only has 2 platforms, spawn only those 2 tasks.

### Step 3: Merge Results

After all audit tasks complete:

1. Read all `*-audit-results.md` files
2. Extract per-platform scores and grades
3. Calculate budget-weighted aggregate score:
   ```
   Aggregate = Σ(Platform_Score × Platform_Budget_Share)
   ```
4. Run cross-platform analysis (see Cross-Platform Analysis below)
5. Merge Quick Wins from all platforms into a unified priority list
6. Generate the unified report

### Step 4: Cross-Platform Analysis

Add intelligence that no single-platform audit can provide:

**Budget Allocation Analysis**
- Is spend distributed optimally across platforms?
- Are high-performing platforms budget-constrained while low performers have excess?
- Does the platform mix match the business type? (e.g., B2B without LinkedIn, ecom without Shopping)
- Compare platform CPAs and flag reallocation opportunities

**Tracking Consistency**
- Are conversion events defined consistently across platforms?
- Is revenue/value tracking active on all platforms or only some?
- Are attribution windows aligned? (7-day click on Meta but 30-day on Google = inconsistent reporting)
- Is there a single source of truth (GA4) or are platforms reporting independently?

**Creative Alignment**
- Is messaging consistent across platforms or contradictory?
- Are creative formats appropriate per platform? (vertical video for Meta/TikTok, text-heavy for Search)
- Is creative being refreshed at similar cadences or is one platform stale?

**Attribution Overlap**
- Are platforms double-counting conversions? (same user converts, Google and Meta both claim credit)
- What percentage of total reported conversions exceeds actual conversions?
- Is there a de-duplication strategy (UTMs + GA4 as arbiter)?

**Kill List**
- Campaigns/ad sets across ALL platforms with CPA >3x target
- Aggregate wasted spend across platforms
- Quick calculation: total monthly waste = Σ(flagged campaign spend)

**Scaling Opportunities**
- Which campaigns across all platforms have CPA below target AND are budget-constrained?
- What is the estimated incremental revenue from reallocating waste to winners?

### Step 5: Generate Unified Report

Output the unified report in the format specified in EXAMPLES.md.

### Step 6: Deck Generation (Optional)

If the user requests a deck (`--deck` flag, or asks for a presentation/deliverable):
- Take the unified report output
- Pipe to pro-deck-builder skill
- Generate a branded HTML slide deck with:
  - Executive summary slide (aggregate score, grade, key findings)
  - Per-platform score cards
  - Cross-platform analysis slides
  - Quick Wins slide
  - Prioritized action plan slides
  - Budget reallocation recommendation slide

## Hard Rules

These constraints apply across all platforms and must never be violated:

1. **Never recommend changes during active learning phases** on any platform.
2. **3x Kill Rule is universal** — flag ANY campaign on ANY platform with CPA >3x target.
3. **Tracking must be verified before optimization recommendations** — if conversion tracking is broken, that is the only recommendation until fixed.
4. **Budget reallocation recommendations must account for minimum thresholds** — don't recommend shifting $500/mo to a platform that needs $3K/mo minimum.
5. **Attribution overlap must be flagged** — if total platform-reported conversions exceed GA4 by >20%, call it out.
6. **Special Ad Categories apply cross-platform** — if housing/employment/credit/finance on one platform, compliance checks apply to all platforms.

## Relationship to Other Skills

This skill **orchestrates** the following skills — it does not replace them:

| Skill | Role in Orchestration |
|-------|----------------------|
| `google-ads` | Provides CHECKS.md + diagnostic frameworks for Google audit task |
| `facebook-ads` | Provides CHECKS.md + diagnostic frameworks for Meta audit task |
| `microsoft-ads` | Provides CHECKS.md + diagnostic frameworks for Microsoft audit task |
| `account-structure-review` | Complementary — run separately for deep structural analysis |
| `wasted-spend-finder` | Complementary — run separately for detailed waste analysis with CSV output |
| `shared/scoring-system.md` | Provides scoring algorithm used by all audit tasks |
| `pro-deck-builder` | Optional downstream — generates client-ready presentation |

## How to Use This Skill

Ask questions like:
- "Run a full audit across all my ad platforms"
- "Score my Google and Meta accounts and give me one unified health grade"
- "Audit my paid media and build a deck I can present to my client"
- "I spend $20K on Google, $15K on Meta, and $5K on Microsoft — audit everything"
- "Which platform should I shift budget to based on performance?"
- "Give me a cross-platform audit with a prioritized action plan"
