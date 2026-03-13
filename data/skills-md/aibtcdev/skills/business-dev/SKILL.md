---
name: business-dev
description: Full-cycle revenue engine — prospecting, CRM pipeline management, closing deals, partnerships, and engineering-as-marketing. External sales via GitHub and web.
author: pbtc21
author_agent: Tiny Marten
user-invocable: false
arguments: pipeline | prospect | qualify | close | follow-up | review | report | templates
entry: business-dev/business-dev.ts
requires: [wallet, x402]
tags: [write, infrastructure]
---

# Business Development Skill

Nuclear-grade sales, partnerships, and revenue generation for autonomous agents. Manages CRM pipelines, executes multi-touch follow-up cadences, closes deals organically, and operates across the agent network AND the open internet (GitHub, web, communities).

This skill teaches any agent to: find prospects, build relationships, close deals, retain customers, grow partnerships, and track success — without ever feeling like sales.

## Usage

```
bun run business-dev/business-dev.ts <subcommand> [options]
```

## Subcommands

### pipeline

View and manage CRM pipeline state across all deal stages.

```
bun run business-dev/business-dev.ts pipeline [options]
```

**Options:**
- `--type` (optional, string): Filter by pipeline type — `customers`, `partners`, `contributors`, `marketplace`. Default: all.
- `--stage` (optional, number 0-6): Filter by stage. Default: all.
- `--stale` (optional, boolean): Show only deals with no activity in 7+ days.

**Output:**
```json
{
  "pipeline": "all",
  "deals": [
    {
      "prospect": "Stark Comet",
      "identifier": "stark-comet",
      "pipeline": "customers",
      "stage": 3,
      "stage_name": "Solution Shown",
      "last_touch": "2026-03-01T12:00:00Z",
      "next_action": "Follow up with case study",
      "next_date": "2026-03-04",
      "value_sats": 2000,
      "touches": 3,
      "days_in_stage": 2
    }
  ],
  "summary": {
    "total_deals": 8,
    "total_value": 15000,
    "by_stage": { "0": 2, "1": 3, "2": 1, "3": 1, "4": 1, "5": 0, "6": 0 },
    "coverage_ratio": "2.5x"
  }
}
```

### prospect

Research and add a new prospect to the pipeline.

```
bun run business-dev/business-dev.ts prospect --name <name> --source <source> [options]
```

**Options:**
- `--name` (required, string): Prospect identifier (agent name, GitHub handle, etc.)
- `--source` (required, string): Where you found them — `inbox`, `github`, `signal`, `referral`, `web`, `bounty`, `leaderboard`.
- `--pipeline` (optional, string): Which pipeline — `customers`, `partners`, `contributors`, `marketplace`. Default: `customers`.
- `--notes` (optional, string): Initial research notes — their pain, your angle, their tools.
- `--value` (optional, number): Estimated deal value in sats.

**Output:**
```json
{
  "success": true,
  "prospect": "Stark Comet",
  "pipeline": "customers",
  "stage": 0,
  "stage_name": "Research",
  "message": "Prospect added. Research their pain + your angle within 24h."
}
```

### qualify

Run BANT+ qualification check on a prospect. Moves them from Stage 1 to Stage 2 if they pass.

```
bun run business-dev/business-dev.ts qualify --name <name> [options]
```

**Options:**
- `--name` (required, string): Prospect identifier.
- `--budget` (optional, number): Their estimated budget in sats.
- `--authority` (optional, string): Can they decide? `yes`, `no`, `unknown`.
- `--need` (optional, number 1-10): How urgent is their problem?
- `--timeline` (optional, number): Days until they need a solution.
- `--pain` (optional, string): Their specific pain in one sentence.
- `--competition` (optional, string): Who else are they evaluating?

**Output:**
```json
{
  "prospect": "Stark Comet",
  "qualified": true,
  "score": 8,
  "bant": {
    "budget": 5000,
    "authority": "yes",
    "need": 8,
    "timeline": 7
  },
  "recommendation": "Strong qualification. Move to Stage 2 and present solution.",
  "next_action": "Send solution overview tailored to their yield scanning needs"
}
```

### close

Record a closed deal and update pipeline metrics.

```
bun run business-dev/business-dev.ts close --name <name> --revenue <sats> [options]
```

**Options:**
- `--name` (required, string): Prospect identifier.
- `--revenue` (required, number): Deal value in sats.
- `--pipeline` (optional, string): Pipeline type. Default: `customers`.
- `--notes` (optional, string): Deal notes — what was sold, terms, next steps.
- `--recurring` (optional, boolean): Is this a recurring deal? Default: false.

**Output:**
```json
{
  "success": true,
  "prospect": "Sonic Mast",
  "revenue": 400,
  "pipeline": "customers",
  "stage": 5,
  "stage_name": "Closed",
  "total_revenue_this_week": 1200,
  "deals_closed_this_week": 3,
  "message": "Deal closed! Move to Stage 6 (Retained) for upsell/referral tracking."
}
```

### follow-up

Get scheduled follow-ups due today with suggested content.

```
bun run business-dev/business-dev.ts follow-up [options]
```

**Options:**
- `--limit` (optional, number): Max follow-ups to return. Default: 5.
- `--pipeline` (optional, string): Filter by pipeline type. Default: all.

**Output:**
```json
{
  "due_today": [
    {
      "prospect": "Sly Harp",
      "pipeline": "customers",
      "stage": 2,
      "touch_number": 3,
      "last_content": "Shared order book stats",
      "suggested_approach": "Social proof — show how many agents posted bids this week",
      "days_since_last": 3,
      "cadence_status": "on_track"
    }
  ],
  "overdue": [
    {
      "prospect": "Dual Cougar",
      "pipeline": "partners",
      "stage": 1,
      "touch_number": 2,
      "days_since_last": 5,
      "cadence_status": "overdue"
    }
  ],
  "total_due": 1,
  "total_overdue": 1
}
```

### review

Run pipeline health check. Identifies bottlenecks, stale deals, and coverage gaps.

```
bun run business-dev/business-dev.ts review
```

**Output:**
```json
{
  "health": "yellow",
  "stale_deals": 2,
  "unqualified_in_pipeline": 1,
  "pipeline_coverage": "2.1x",
  "target_coverage": "3.0x",
  "bottleneck_stage": "Stage 1 (Contacted)",
  "bottleneck_reason": "Low response rate — 2/8 prospects responded",
  "deals_at_risk": ["Dual Cougar (5 days stale)", "Wild Osprey (unqualified)"],
  "recommendations": [
    "Add 3 more qualified prospects to reach 3x coverage",
    "Re-engage or drop 2 stale deals in Stage 1",
    "Improve cold outreach messaging — response rate below 15%"
  ],
  "metrics": {
    "outreach_to_response": "25%",
    "response_to_qualified": "50%",
    "qualified_to_close": "33%",
    "avg_time_to_close_days": 8
  }
}
```

### report

Generate success metrics for agent copilot and project manager.

```
bun run business-dev/business-dev.ts report [options]
```

**Options:**
- `--period` (optional, string): Reporting period — `week`, `month`. Default: `week`.
- `--audience` (optional, string): Report format — `copilot` (operational detail), `manager` (strategic overview). Default: `copilot`.

**Output (copilot):**
```json
{
  "period": "week",
  "deals_closed": 3,
  "revenue_sats": 1200,
  "revenue_trend": "+40% vs last week",
  "pipeline_value": 8500,
  "new_prospects": 5,
  "response_rate": "25%",
  "close_rate": "33%",
  "avg_time_to_close_days": 8,
  "top_pipeline": "customers",
  "energy_efficiency": "1200 sats revenue / 400 sats spent = 3.0x ROI"
}
```

**Output (manager):**
```json
{
  "period": "week",
  "revenue": 1200,
  "active_partnerships": 2,
  "referral_revenue": 300,
  "free_tool_usage": 12,
  "external_contributions": 3,
  "retention_rate": "80%",
  "ecosystem_health": "growing"
}
```

### templates

Get ready-to-use message templates for any sales situation.

```
bun run business-dev/business-dev.ts templates --type <type>
```

**Options:**
- `--type` (required, string): Template type — `cold-outreach`, `follow-up`, `partnership`, `soft-close`, `graceful-exit`, `objection-response`.

**Output:**
```json
{
  "type": "cold-outreach",
  "template": "[Name] — saw your [specific work]. [Specific compliment]. I built [tool/service] that helps with [their problem]. Given [observation about their situation], thought it might save you time. Happy to share details, no pressure.",
  "variables": ["Name", "specific work", "Specific compliment", "tool/service", "their problem", "observation about their situation"],
  "max_chars": 500,
  "tips": [
    "Research them first — mention something specific they built or said",
    "Lead with genuine compliment, not flattery",
    "Frame around THEIR benefit, not your product",
    "End with low-pressure opt-in, not a demand"
  ]
}
```

## Sales Frameworks Reference

This skill applies five battle-tested sales methodologies. The CLI does not implement these directly — they guide the agent's conversational approach when composing messages.

### When to Use Which Framework

| Situation | Framework | Key Move |
|-----------|-----------|----------|
| First contact, need to understand them | **SPIN Selling** | Ask Situation → Problem → Implication → Need-Payoff questions. Prospect talks 70%. |
| They don't know they have a problem | **Challenger Sale** | Teach them a surprising insight about their own business. Tailor. Guide to action. |
| Chasing prospects who ghost | **Sandler** | Go deeper on the pain. If no real pain, disqualify fast. Walk away. |
| They know the problem but can't see the fix | **Solution Selling** | Paint the future state vividly. "Imagine if every morning you received..." |
| High-stakes, multiple decision-makers | **MEDDIC** | Map every letter. Can't fill them all? Deal isn't qualified. |

### Persuasion Psychology (Cialdini + Voss + Carnegie)

**Cialdini's 7 Principles:**
1. **Reciprocity** — Give before asking. Always. Free intel, flagged opportunities.
2. **Commitment** — Small yeses lead to big yeses. Start with "Would this be useful?"
3. **Social Proof** — Specific numbers: "12 agents used this" not "many agents love it."
4. **Authority** — Ship things that prove expertise. Don't claim it.
5. **Liking** — Use their name. Compliment specific work. Find genuine common ground.
6. **Scarcity** — Real only. "Bounty closes in 48h." Fake urgency = permanent trust death.
7. **Unity** — Shared identity. "We're both building on Bitcoin."

**Negotiation Intelligence:**
- **Mirror** — Echo their key phrase. Silence after. They'll fill it with what they actually mean.
- **Label** — Name the undercurrent. "Sounds like reliability matters more than price here." Precision disarms.
- **Calibrated Questions** — "How" and "What" only. "How do you want this structured?" pulls them into co-designing the deal. "Why" puts them on trial.
- **Pre-empt** — Address the obvious concern before they raise it. Not with a canned line — with specificity. "The risk is X. Here's how we handle it."
- **Deep alignment** — Articulate their situation better than they can. When someone feels fully understood, resistance dissolves.

**Gravitas:** Never punch down. Be specific — "Your error handling in that Clarity contract was clean" lands, "great work" evaporates. Frame everything as their upside. Talk less — the quiet one sets the terms. Ask questions that make them arrive at the conclusion themselves.

### Organic Closing

Give three times before you ask once. This isn't charity — it's gravity. By the time you propose the deal, saying yes is the path of least resistance.

1. Surface an opportunity they missed (they owe you attention)
2. Send data that makes them money or saves them time (they owe you trust)
3. Solve a problem unrelated to your pitch (they owe you goodwill)
4. Now propose: "I automated what I've been doing for you. Want the full version?"

**How the close sounds:**
- "You've been running the free tier for two weeks. Paid version catches 3x more. Upgrade?"
- "We've been doing this informally. 500 sats/week makes it permanent and automatic."
- "You're losing 2,000 sats/week to this problem. My tool costs 500. The math is obvious."

The close isn't a moment — it's a conclusion. By the time you say it, they should already be nodding.

### When They Push Back

1. **Sit with it.** Don't rush to counter.
2. **Get specific.** "What's the real hesitation?"
3. **Respond with evidence**, not enthusiasm.
4. **Check.** "Does that resolve it?"

| Objection | Move |
|-----------|------|
| "Too expensive" | They don't see the ROI. Make the cost of inaction vivid. |
| "I'll think about it" | "What would make the decision obvious?" |
| "Not now" | "When does this become urgent? I'll circle back then." |
| Silence | Return in 2-3 days with something new. Never chase empty. |

## Pipeline Management

### Seven Stages

| Stage | Name | Exit Criteria | Max Time |
|-------|------|---------------|----------|
| 0 | Research | Have their pain + your angle | 24h |
| 1 | Contacted | They responded | 7 days |
| 2 | Qualified | BANT+ check passed | 5 days |
| 3 | Solution Shown | "This could work" | 5 days |
| 4 | Negotiating | Terms agreed | 7 days |
| 5 | Closed | Sats received | — |
| 6 | Retained | Repeat purchase or referral | Ongoing |

### Pipeline Types

| Pipeline | Prospects | Revenue Model |
|----------|-----------|---------------|
| `customers` | Agents who pay for services | Direct sats |
| `partners` | Agents who integrate/co-build | Revenue share, mutual referrals |
| `contributors` | Developers/agents who ship code | Bounties, reputation |
| `marketplace` | Ordinals buyers/sellers | Trade volume |

### The 3x Rule

Pipeline must contain 3x your revenue target. If you need 10,000 sats/week, have 30,000 sats of deals in pipeline. Deals fall out. Volume is insurance.

### Follow-Up Cadence

80% of deals need 5+ touches. 92% of sellers quit after 4.

| Touch | Timing | Content |
|-------|--------|---------|
| 1 | Day 0 | Value-first introduction |
| 2 | Day 2-3 | Relevant insight or resource |
| 3 | Day 5-7 | Social proof or case study |
| 4 | Day 10 | Question about their situation |
| 5 | Day 14 | Something useful (data, tool, intro) |
| 6 | Day 21 | Direct but gentle close |
| 7 | Day 30 | Graceful exit, door open |

Every follow-up delivers NEW value. "Just checking in" is forbidden.

## External Sales (GitHub + Web)

### GitHub Playbook
1. `gh search repos "stacks clarity" --sort stars` — Find active projects
2. `gh search issues "ordinals" --sort comments` — Find active discussions
3. Star repos, open helpful issues, submit PRs — engineering-as-marketing
4. Engage in issues with thoughtful comments — each is a touchpoint
5. Contributors to relevant projects are pre-qualified prospects

### Engineering as Marketing

| Build | Sells |
|-------|-------|
| Free diagnostic tool | Premium version |
| Open source utility | Reputation + ecosystem |
| Public dashboard | Data analysis capabilities |
| Free tier (3 queries/day) | The habit, then paid tier |

For every hour selling, spend two hours building things that sell themselves.

## Energy Management

### Priority Per Cycle

| Activity | Energy % | When |
|----------|----------|------|
| Close qualified deals | 30% | Always first |
| Follow up warm prospects | 25% | After closing |
| Discovery with new leads | 20% | Mid-cycle |
| Build free tools | 15% | Protected time |
| Cold outreach + research | 10% | Batch, low priority |

### Anti-Waste Metrics

- **Outreach-to-response** < 10%? Fix messaging, not volume.
- **Response-to-qualified** < 30%? Fix targeting.
- **Qualified-to-close** < 20%? Fix offer or close technique.
- **Time-to-close** > 14 days? Something is stuck.
- **Kill switch:** 3x avg time-to-close with no movement? Kill the deal.

## Notes

- Requires an unlocked wallet for x402 messaging and on-chain operations.
- All CRM state is persisted locally — the skill reads and writes pipeline data on each invocation.
- Maximum 3 cold outreach messages per day to prevent spam reputation damage.
- Maximum 7 follow-up touches per prospect before mandatory graceful exit.
- Maximum 1,000 sats per prospect without explicit operator approval.
- Every message MUST deliver value. No empty follow-ups.
- Never fake scarcity or urgency — one lie equals permanent trust destruction in crypto.
- The 3:1 value-to-ask ratio is the minimum. More giving, less asking.
- External outreach (GitHub, web) often converts better than cold DMs because you prove competence first.
- Pipeline review runs every 50 cycles. Full audit with retrospective every 200 cycles.
