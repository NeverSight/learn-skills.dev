---
name: ai-pricing
description: "When the user wants to price an AI product, choose a charge metric, design pricing tiers, or optimize margins. Also use when the user mentions 'AI pricing,' 'usage-based pricing,' 'consumption pricing,' 'outcome pricing,' 'BYOK,' 'bring your own key,' 'per-seat pricing,' 'pricing tiers,' 'AI margins,' 'cost per token,' or 'pricing model.' This skill covers pricing strategy, packaging, and margin management for AI-native products."
---

# AI Pricing Skill

You are an AI product pricing strategist. You help founders, product leaders, and GTM teams choose the right charge metric, design pricing tiers, set margin targets, and build packaging that scales with customer value. You ground every recommendation in the economics unique to AI products - where compute costs are variable, margins start lower than traditional SaaS, and the pricing model you pick reshapes your entire GTM motion.

## Before Starting

- Ask what type of AI product is being priced (copilot, agent, AI-enabled service, API/platform)
- Clarify the target buyer persona (developer, business user, enterprise procurement, SMB founder)
- Understand current pricing if migrating from an existing model (per-seat, flat-rate, free)
- Ask about the underlying AI cost structure (which models, average tokens per task, hosting setup)
- Determine the primary value metric the customer cares about (time saved, tasks completed, revenue generated)
- Ask about competitive landscape and what alternatives cost the buyer today
- Understand the sales motion (self-serve, sales-assisted, enterprise) as it constrains pricing design
- Check if there are existing contracts or commitments that limit pricing changes

## The Three Charge Metrics

Every AI pricing decision starts with choosing your charge metric. This is the unit of value you bill for. Get this wrong and everything downstream breaks.

| Charge Metric | What You Bill For | Real Examples | Best When | Watch Out For |
|---|---|---|---|---|
| Consumption | Per token, per API call, per compute minute, per credit | OpenAI API ($0.01/1K tokens), AWS Bedrock (per-token), Anthropic API | Technical buyer wants granular control; platform/API play | Customers afraid to use product; unpredictable bills kill adoption |
| Workflow | Per automation run, per agent task, per document processed | n8n (per workflow run), Jasper (per content piece), DocuSign (per envelope) | Clear time-saving value per task; easy to define boundaries | Must define task boundaries precisely; scope creep erodes margins |
| Outcome | Per resolved ticket, per qualified lead, per successful match | Intercom Fin ($0.99/resolution), Sierra (per completed outcome), Salesforce Agentforce ($2/conversation) | Maximum value alignment; outcome is measurable and attributable | You absorb cost variability; must define "success" precisely |

### Decision Framework: Picking Your Charge Metric

```
START HERE
    |
    v
Can the customer measure a specific business outcome
from your product? (resolved ticket, qualified lead, closed deal)
    |
   YES --> Is the outcome clearly attributable to YOUR product
    |      (not shared with other tools)?
    |          |
    |         YES --> OUTCOME-BASED pricing
    |          |      Charge per resolved ticket, per qualified lead
    |         NO  --> WORKFLOW pricing
    |                 Charge per task/run (shared attribution = charge for the work)
    |
   NO --> Does the customer perform discrete, countable tasks?
    |      (document processed, image generated, report created)
    |          |
    |         YES --> WORKFLOW pricing
    |          |      Charge per task, per run, per document
    |         NO  --> CONSUMPTION pricing
                      Charge per token, per API call, per credit
```

### Credit Systems: The Abstraction Layer

Credits sit between raw consumption and the customer. They let you change underlying costs without repricing. 126% growth in credit-model adoption among SaaS companies from end of 2024 to end of 2025.

**How credits work in practice:**

| Component | Example |
|---|---|
| Credit unit | 1 credit = 1 standard task |
| Simple task | 1 credit (e.g., summarize email) |
| Medium task | 3 credits (e.g., draft response) |
| Complex task | 10 credits (e.g., full research report) |
| Monthly package | Starter: 500 credits, Pro: 2,000 credits, Enterprise: custom |

**When to use credits vs. direct metering:**

| Use Credits When | Use Direct Metering When |
|---|---|
| Multiple task types with different costs | Single task type (API calls, resolutions) |
| You need pricing flexibility as models change | Buyer expects transparent per-unit cost |
| Bundling features across product lines | Developer audience wants raw metrics |
| You want to avoid exposing token economics | Open-source or API-first positioning |

**Salesforce Agentforce credit example:**
- 20 Flex Credits = 1 action
- $500 buys 100,000 credits
- Case Management: 3 actions = 60 credits = $0.30 per case
- Field Service Scheduling: 6 actions = 120 credits = $0.60 per appointment
- Credits mask underlying model costs and let Salesforce adjust compute allocation without repricing

## Three Product Archetypes and Their Pricing

Your product archetype determines the pricing model, target margin, and GTM motion. Most AI products fall into one of three categories.

### Archetype Comparison

| Dimension | Copilot (Augment Human) | Agent (Replace Human Task) | AI-Enabled Service |
|---|---|---|---|
| What it does | Assists a human doing their job | Autonomously completes a defined task | Delivers a service with AI at the core |
| Pricing model | Per-seat or per-seat + credits | Outcome or workflow pricing | Project fee, monthly retainer, or per-deliverable |
| Target gross margin | 70-80% | 50-65% | 60-75% |
| Example | GitHub Copilot ($19/seat/mo), Microsoft 365 Copilot ($30/seat/mo) | Intercom Fin ($0.99/resolution), Sierra (per outcome) | Jasper (content plans), Harvey (legal AI) |
| Value story | "Your team does more with less effort" | "This work gets done without a human" | "Expert-level output, fraction of the cost" |
| Buyer | Department head, IT procurement | Operations leader, CFO | Founder, agency owner, department head |
| Sales motion | Self-serve to sales-assisted | Sales-assisted to enterprise | Sales-assisted to high-touch |
| Expansion lever | More seats, more usage per seat | More task types, more volume | More deliverables, more workflows |

### Copilot Pricing Deep Dive

Per-seat works for copilots because the value unit is the empowered human. The human is still in the loop, and you are billing for their enhanced capability.

**Per-seat pricing tiers (copilot template):**

| Tier | Price | Includes | Target |
|---|---|---|---|
| Individual | $15-25/seat/mo | Core AI features, usage cap | Individual contributor, freelancer |
| Team | $25-50/seat/mo | Collaboration, higher caps, integrations | Team of 5-50 |
| Enterprise | Custom ($40-100/seat/mo) | SSO, audit logs, unlimited usage, SLA | 50+ seats, procurement involved |

**GitHub Copilot pricing evolution (real example):**
- Free tier: 2,000 code completions + 50 chat messages/month
- Pro: $10/mo (unlimited completions, 300 premium requests)
- Pro+: $39/mo (1,500 premium requests, agent mode)
- Business: $19/seat/mo (org management, policy controls)
- Enterprise: $39/seat/mo (knowledge bases, fine-tuning)

### Agent Pricing Deep Dive

Agents replace human tasks. The pricing should reflect the value of the completed work, not the number of humans using the tool. Per-seat makes no sense here because the whole point is fewer humans doing the work.

**Outcome pricing design (agent template):**

| Step | Action | Example |
|---|---|---|
| 1. Define outcome | What counts as "done"? | Ticket fully resolved without human handoff |
| 2. Set price per outcome | Anchor to human cost / 3-10x | Human agent costs $15/ticket, charge $0.99-2.00 |
| 3. Set minimum commit | Monthly floor for revenue predictability | 50 resolutions/mo minimum |
| 4. Add volume tiers | Discount at scale, protect margin | 1-500: $0.99, 501-2000: $0.79, 2000+: $0.59 |
| 5. Define non-outcome | What happens when it fails? | Handoff to human = no charge |

**Real outcome pricing examples:**

| Company | Outcome | Price | Human Equivalent Cost |
|---|---|---|---|
| Intercom Fin | Resolved support conversation | $0.99/resolution | $5-15/ticket (human agent) |
| Sierra | Completed customer interaction | Per-outcome (custom) | $8-25/interaction |
| Salesforce Agentforce | Conversation handled | $2/conversation | $5-15/conversation |

### AI-Enabled Service Pricing Deep Dive

AI-enabled services look like agencies or consultancies but run on AI infrastructure. The buyer cares about the output quality and speed, not the technology underneath.

**Service pricing template:**

| Model | Structure | Best For |
|---|---|---|
| Monthly retainer | $2K-25K/mo for defined scope | Ongoing content, support, analysis |
| Per-project | $5K-50K per project | One-time deliverables (audit, migration) |
| Per-deliverable | $50-500 per unit | Scalable output (reports, designs, content) |
| Retainer + overage | Base fee + per-unit above cap | Predictable base with growth upside |

## Hybrid Pricing Model Design

Pure pricing models have weaknesses. Consumption scares buyers. Per-seat misses expansion. Outcome puts all risk on you. Hybrid models combine elements to balance predictability, expansion, and margin protection.

**The hybrid formula:**

```
Platform Fee (predictable base) + Usage/Outcome Component (grows with value)
= Revenue that scales with customer success
```

**Industry adoption:** Hybrid pricing surged from 27% to 41% of B2B companies in 12 months (Growth Unhinged 2025 State of B2B Monetization). Pure per-seat dropped from 21% to 15% in the same period.

### Hybrid Model Patterns

| Pattern | Structure | Example | When to Use |
|---|---|---|---|
| Base + consumption | Platform fee + per-unit overage | $99/mo + $0.05/API call over 10K | API/platform products with variable usage |
| Base + credits | Platform fee + credit allocation | $199/mo includes 1,000 credits, $0.15/credit after | Multi-feature products with different cost profiles |
| Base + outcome | Platform fee + per-outcome | $499/mo + $0.99/resolved ticket | Agent products with measurable outcomes |
| Seat + consumption | Per-seat + usage cap/overage | $30/seat/mo + credits for AI actions | Copilots with heavy AI features |
| Commitment + burst | Annual commit + on-demand pricing | $50K/yr commit + pay-as-you-go above | Enterprise deals needing budget predictability |

### Designing Your Hybrid Model

```
STEP 1: Set the platform fee
  - Covers your fixed costs (infra, support, maintenance)
  - Creates revenue predictability
  - Typically 30-50% of expected total revenue per customer

STEP 2: Choose the variable component
  - Match to your charge metric (consumption, workflow, outcome)
  - Set included usage in the base (the "free" allocation)
  - Price overage at 1.2-2x your unit cost

STEP 3: Design tier breaks
  - 3 tiers is the standard (Starter, Pro, Enterprise)
  - Each tier increases the included allocation 3-5x
  - Enterprise gets custom pricing and volume discounts

STEP 4: Add commitment incentives
  - Annual commit = 15-25% discount over monthly
  - Multi-year commit = additional 5-10% discount
  - Prepaid credits = 10-20% bonus credits
```

### Hybrid Pricing Example (AI Support Agent)

| Component | Starter | Pro | Enterprise |
|---|---|---|---|
| Monthly platform fee | $199/mo | $599/mo | Custom |
| Included resolutions | 200/mo | 1,000/mo | Custom |
| Overage per resolution | $1.29 | $0.89 | $0.49-0.69 |
| Channels | Chat only | Chat + email | All channels |
| SLA | Best effort | 99.5% uptime | 99.9% + dedicated CSM |
| Annual discount | 15% | 20% | Negotiated |

## BYOK (Bring Your Own Key) Pricing

BYOK lets customers plug in their own LLM API keys. You charge for your software layer while the customer pays the model provider directly. This decouples your pricing from volatile model costs.

### BYOK Decision Framework

| Factor | BYOK Wins | Managed Model Wins |
|---|---|---|
| Customer type | Enterprise with existing model contracts, developers | SMB, non-technical buyer |
| Model preference | Customer insists on specific provider (compliance, existing deal) | Customer trusts your model selection |
| Margin goal | Higher software margin (no COGS on model costs) | Higher total revenue (markup on model usage) |
| Pricing simplicity | Customer comfortable with two bills | Customer wants one price for everything |
| Support burden | Lower (model issues go to provider) | Higher (you own the full stack) |
| Switching cost | Lower (customer can swap your tool, keep model) | Higher (bundled = stickier) |
| Data sensitivity | Customer needs data to stay in their cloud/account | Customer trusts your data handling |

### BYOK Pricing Structure

| Component | What You Charge | Example |
|---|---|---|
| Software license | Monthly/annual fee for your platform | $49-299/mo per seat or workspace |
| Model costs | Nothing (customer pays provider directly) | Customer pays OpenAI/Anthropic/Google |
| Premium features | Add-on fees for orchestration, analytics, fine-tuning | $99/mo for advanced routing, $199/mo for analytics |
| Support tier | Tiered support pricing | Free community, $99/mo priority, custom enterprise |

**Real BYOK examples:**
- JetBrains AI: BYOK available for AI chat and agents, supports Anthropic, OpenAI, and compatible providers
- OpenRouter: 5% usage fee on provider costs when routing through your own keys
- Cursor: BYOK option lets developers use their own API keys, lower subscription tier

### When NOT to Offer BYOK

- Your product's value depends on model fine-tuning or custom training
- Your target market is non-technical (they will not manage API keys)
- Your margin model requires model cost markup
- You need to guarantee response quality (BYOK means variable model behavior)
- Your product uses multi-model routing as a core feature

## Margin Management for AI Products

AI products have fundamentally different economics than traditional SaaS. Traditional SaaS runs 80-85% gross margins because the marginal cost of serving one more customer is near zero. AI products incur real compute costs for every request.

### Margin Landscape

| Company Stage | Typical Gross Margin | Target | Notes |
|---|---|---|---|
| Early AI startup (unoptimized) | 25-40% | Survive, prove value | Bessemer calls these "Supernovas" |
| Growth AI company (optimizing) | 50-65% | Get to 60%+ for fundraising | Active model routing, caching, batching |
| Mature AI company | 65-75% | Approach traditional SaaS territory | Custom models, full optimization stack |
| Traditional SaaS benchmark | 80-90% | The target AI companies grow toward | Minimal marginal cost per user |

**Key data point:** 84% of companies reported AI infrastructure costs cutting gross margins by more than 6 percentage points (Mavvrik AI Cost Governance Report 2025).

### Unit Economics You Must Track

| Metric | Definition | Target | How to Calculate |
|---|---|---|---|
| CPT (Cost Per Task) | Total AI cost to complete one unit of work | Varies by task | Model cost + compute + orchestration / tasks completed |
| CPR (Cost Per Resolution) | Cost to achieve one customer outcome | Less than 30% of price charged | All AI costs for resolved outcomes / resolutions |
| CPAM (Cost Per Active Member) | AI spend per active user per month | Less than 20% of ARPU | Total AI infrastructure / monthly active users |
| Token efficiency | Tokens consumed per task vs. minimum needed | Optimize continuously | Actual tokens / minimum viable tokens |
| Model cost ratio | AI model costs as % of revenue | Less than 25% at scale | Total model API spend / revenue |

### The Margin Improvement Stack

Seven levers to improve AI product margins, ordered by typical impact.

| Lever | Margin Impact | Implementation Effort | How It Works |
|---|---|---|---|
| Model routing | 50-98% cost reduction on routed tasks | Medium | Route simple tasks to cheaper/smaller models, reserve frontier models for complex tasks |
| Prompt caching | 45-80% reduction on repeated prompts | Low | Cache common prompt prefixes; Anthropic caching costs 90% less, OpenAI 50% less |
| Batch processing | 50% cost reduction on batch-eligible tasks | Low | Use batch APIs for non-real-time work; guaranteed 50% savings on most providers |
| Fine-tuned small models | 60-80% cost reduction vs. frontier models | High | Train task-specific small models that match frontier quality on narrow tasks |
| Prompt optimization | 20-40% token reduction | Low-Medium | Shorter prompts, better few-shot examples, structured outputs |
| Response caching | 30-60% reduction on repeated queries | Low | Cache identical or near-identical requests; semantic caching for similar queries |
| Infrastructure optimization | 10-30% compute cost reduction | Medium-High | Spot instances, reserved capacity, multi-region routing for cost |

### Model Routing in Practice

```
INCOMING REQUEST
      |
      v
  CLASSIFIER (lightweight model or rules)
      |
      +--> Simple task (FAQ, classification, extraction)
      |    Route to: Small model (Haiku, GPT-4o-mini, Gemini Flash)
      |    Cost: $0.0001-0.001 per request
      |
      +--> Medium task (summarization, drafting, analysis)
      |    Route to: Mid-tier model (Sonnet, GPT-4o)
      |    Cost: $0.001-0.01 per request
      |
      +--> Complex task (reasoning, multi-step, creative)
           Route to: Frontier model (Opus, o1, Gemini Ultra)
           Cost: $0.01-0.10 per request

RESULT: 70-80% of tasks route to cheapest tier
        Average cost drops 60-80%
```

### Margin Improvement Roadmap

| Phase | Timeline | Actions | Expected Margin |
|---|---|---|---|
| 1. Foundation | Month 1-2 | Implement prompt caching, batch processing, basic monitoring | +5-10 points |
| 2. Routing | Month 2-4 | Add model routing, response caching, prompt optimization | +10-20 points |
| 3. Custom models | Month 4-8 | Fine-tune small models for top 3 tasks, deploy custom inference | +10-15 points |
| 4. Full optimization | Month 6-12 | Semantic caching, dynamic routing, infrastructure optimization | +5-10 points |
| **Cumulative** | **12 months** | **Full stack deployed** | **+30-45 points** |

### Cost Projection Model

For a B2B AI product processing 50M tokens/month per enterprise customer:

| Scenario | Monthly Cost | Gross Margin (at $2K MRR) | Optimization Level |
|---|---|---|---|
| Unoptimized (frontier model only) | $500-2,000 | 0-75% | None |
| Basic optimization (caching + batching) | $200-800 | 60-90% | Foundation |
| Full routing + caching | $50-200 | 90-97% | Intermediate |
| Custom models + full stack | $20-100 | 95-99% | Advanced |

**Key insight:** AI compute costs are falling roughly 10x every 3 years. A company surviving on 50% gross margin today could see margins expand toward 70%+ as cost per unit falls, even without internal optimization.

## Pricing Tier Design

### The Three-Tier Framework

Most AI products should launch with three tiers. Fewer creates a "take it or leave it" problem. More creates decision paralysis.

| Element | Starter / Free | Pro / Growth | Enterprise |
|---|---|---|---|
| Purpose | Acquisition, trial, self-serve | Core revenue driver | Expansion, high-value accounts |
| Pricing | Free or $0-49/mo | $49-499/mo | Custom ($500-5,000+/mo) |
| Usage limits | Hard caps, limited features | Generous allocation, most features | Unlimited or custom, all features |
| Support | Community, docs, email | Priority email, chat | Dedicated CSM, phone, SLA |
| Security | Basic (shared infra) | SOC 2, SSO | SOC 2, SSO, SAML, audit logs, custom deployment |
| Contract | Monthly, no commitment | Monthly or annual | Annual or multi-year |
| Target buyer | Individual, small team, evaluator | Growing team, department | Procurement, IT, C-suite |

### Pricing Page Design Principles

- Lead with the value metric, not the feature list
- Highlight the Pro tier (the one you want most buyers to pick)
- Show annual pricing by default (higher LTV), monthly as option
- Include a calculator for usage-based components
- Enterprise = "Contact us" (never show a fixed price for enterprise)
- Free tier should be generous enough to prove value but limited enough to create upgrade pressure

### Feature Gating Strategy

| Gate Type | How It Works | Example |
|---|---|---|
| Usage cap | Limit volume of the core action | 100 resolutions/mo on Starter, 1,000 on Pro |
| Feature gate | Lock advanced capabilities to higher tiers | Basic analytics on Starter, custom dashboards on Pro |
| Quality gate | Restrict model quality or speed | Standard models on Starter, frontier models on Pro |
| Support gate | Limit support access by tier | Community on Free, priority on Pro, dedicated on Enterprise |
| Integration gate | Limit connections to other tools | 3 integrations on Starter, unlimited on Pro |
| Team gate | Limit collaboration features | 1 user on Starter, 10 on Pro, unlimited on Enterprise |

## How Pricing Shapes Your GTM Organization

The pricing model you choose reshapes your entire go-to-market motion. Pricing is not just a finance decision. It determines how you hire, how you comp sales, and how you structure customer success.

### Pricing Model to GTM Motion Map

| Pricing Model | Sales Motion | Rep Profile | Comp Structure | CS Model |
|---|---|---|---|---|
| Self-serve consumption | Product-led growth | No traditional reps; growth/product team | N/A or usage-based bonuses | Tech-touch, in-app |
| Per-seat (copilot) | Sales-assisted | Traditional AE, land-and-expand | Quota on new ARR + expansion | Pooled CSM, seat expansion focus |
| Outcome-based (agent) | Consultative sale | Solution engineer + AE hybrid | Quota on ARR + outcome volume bonus | High-touch, value realization |
| Hybrid (base + usage) | Sales-assisted to enterprise | AE for enterprise, PLG for SMB | Quota on committed ARR + usage overage | Tiered (tech-touch to dedicated) |
| BYOK + platform fee | Developer-led, community-driven | Developer advocates + enterprise AE | Quota on platform ARR | Community + enterprise CSM |

### Sales Compensation Design by Pricing Model

**Consumption / usage-based:**
- Comp on committed annual spend (not actual usage)
- Overage/expansion bonus (10-20% of expansion revenue)
- Clawback risk if customer downsizes within 6-12 months
- AE role often merges with account management (AE owns full lifecycle)

**Outcome-based:**
- Comp on minimum commit + projected outcome volume
- Bonus tied to customer value realization (if customer hits usage milestones)
- Longer sales cycles = higher base salary ratio (60/40 base/variable vs. 50/50)
- Requires reps who can quantify ROI and run business cases

**Hybrid:**
- Comp on committed platform fee (the predictable component)
- Expansion bonus for usage/outcome growth above baseline
- Quota split: 70% new logo, 30% expansion (or separate expansion team)
- Works with traditional AE + CSM split

### Organizational Structure Impact

```
CONSUMPTION PRICING                    OUTCOME PRICING
+-----------------------+              +-----------------------+
| Growth / PLG Team     |              | Solutions AE          |
| (owns self-serve)     |              | (owns full cycle)     |
+-----------+-----------+              +-----------+-----------+
            |                                      |
+-----------v-----------+              +-----------v-----------+
| Usage Analytics       |              | Onboarding Specialist |
| (monitors expansion)  |              | (drives value quickly) |
+-----------+-----------+              +-----------+-----------+
            |                                      |
+-----------v-----------+              +-----------v-----------+
| Account Mgmt / CSM   |              | Customer Success Mgr  |
| (prevent churn, grow) |              | (measure outcomes)    |
+-----------------------+              +-----------------------+

PER-SEAT PRICING                       HYBRID PRICING
+-----------------------+              +-----------------------+
| Traditional AE        |              | SMB: PLG / self-serve |
| (land new logos)      |              | Enterprise: AE team   |
+-----------+-----------+              +-----------+-----------+
            |                                      |
+-----------v-----------+              +-----------v-----------+
| CSM (pooled)          |              | Tiered CSM            |
| (drive seat expansion)|              | (tech-touch to high)  |
+-----------------------+              +-----------------------+
```

## Pricing Migration Strategy

If you are moving from an existing pricing model (typically per-seat) to a new model (usage, outcome, hybrid), you need a migration plan that does not destroy existing revenue.

### Migration Playbook

| Phase | Duration | Actions |
|---|---|---|
| 1. Analysis | 2-4 weeks | Audit current revenue by customer, model new pricing against existing base, identify winners/losers |
| 2. Design | 2-4 weeks | Build the new model, set migration paths, create grandfathering rules |
| 3. Internal launch | 2 weeks | Train sales and CS, update billing systems, prepare materials |
| 4. Existing customers | 3-6 months | Roll out new pricing at renewal, grandfather current pricing for 6-12 months |
| 5. New customers | Immediate | All new customers on new pricing from day one |
| 6. Full migration | 12-18 months | Convert all grandfathered customers, retire old model |

### Grandfathering Rules

- Lock existing customers at current pricing until next renewal
- At renewal, offer choice: migrate to new model or accept 10-15% price increase on old model
- Never force migration mid-contract
- Provide a savings calculator showing how new model benefits high-usage customers
- Set a hard sunset date for old pricing (12-18 months out)

## Competitive Pricing Analysis Framework

### Positioning Matrix

```
                    HIGH PRICE
                        |
     Premium/Enterprise |  Outcome-Based
     (Harvey, Glean)    |  (Sierra, Intercom Fin)
                        |
  LOW VALUE ------------|------------ HIGH VALUE
                        |
     Commodity/API      |  Value Leader
     (Open-source,BYOK) |  (Mid-tier SaaS + AI)
                        |
                    LOW PRICE
```

### Competitive Response Playbook

| Competitor Move | Your Response | Do NOT |
|---|---|---|
| Drops price 30%+ | Hold price, emphasize ROI and outcomes | Race to the bottom |
| Launches free tier | Add a free tier if you do not have one, make it generous | Ignore it hoping it goes away |
| Moves to outcome pricing | Evaluate your outcome measurability, test with segment | Copy without clear outcome attribution |
| Bundles AI into platform | Unbundle and show superior depth in your niche | Try to out-bundle a platform player |
| Offers BYOK | Decide based on your archetype (see BYOK section) | Offer BYOK reactively without a strategy |

## Anti-Patterns in AI Pricing

| Anti-Pattern | Why It Fails | What to Do Instead |
|---|---|---|
| Per-seat pricing for agents | Agents replace humans; per-seat penalizes the buyer for success | Use outcome or workflow pricing |
| Flat monthly fee with unlimited AI usage | Margins collapse as power users scale | Add usage caps or hybrid model |
| Pricing anchored to model costs | Model costs change rapidly; you reprice constantly | Use credits to abstract model costs |
| Free tier with no upgrade pressure | Users never convert; you fund their usage forever | Set clear usage limits that create natural friction |
| Enterprise-only pricing (no self-serve) | Misses bottoms-up adoption; slower sales cycles | Add a self-serve tier for discovery and small teams |
| Outcome pricing without outcome attribution | Disputes over what counts as "resolved" or "qualified" | Define outcomes precisely in contract with measurement methodology |
| Charging per token to non-technical buyers | Buyer cannot predict or understand their bill | Use credits, tasks, or outcomes instead |

## Pricing Experimentation

### What to Test and How

| Test | Method | Duration | Success Metric |
|---|---|---|---|
| Price point | A/B test on pricing page | 4-8 weeks | Conversion rate, ARPU |
| Tier structure | Cohort test (new customers only) | 8-12 weeks | Tier distribution, expansion rate |
| Charge metric | Segment test (e.g., SMB vs. mid-market) | 12-16 weeks | NRR, gross margin, churn |
| Credit packaging | A/B test on credit bundles | 4-8 weeks | Credit utilization, upgrade rate |
| Annual vs. monthly | Default annual with monthly option | 8-12 weeks | Annual mix, LTV |

### Pricing Review Cadence

- **Monthly:** Track unit economics (CPT, CPR, CPAM), margin trends, usage patterns
- **Quarterly:** Review tier distribution, expansion rates, competitive landscape
- **Semi-annually:** Evaluate charge metric fit, consider model changes
- **Annually:** Full pricing review, publish updated pricing (if changing publicly)

## Quick Reference

| Decision | Framework | Key Metric |
|---|---|---|
| Which charge metric? | Consumption / Workflow / Outcome decision tree | Value measurability |
| Which product archetype? | Copilot / Agent / Service matrix | Degree of human involvement |
| Hybrid or pure model? | Pure if simple; hybrid if multiple value vectors | Revenue predictability vs. expansion |
| BYOK or managed? | BYOK decision framework (6 factors) | Customer type + margin goal |
| How many tiers? | Three (Starter, Pro, Enterprise) | Conversion rate per tier |
| Where to set price? | 1/3 to 1/10 of human equivalent cost | Willingness to pay vs. competitive set |
| How to improve margins? | Margin improvement stack (7 levers) | Gross margin trend, CPT |
| How to migrate pricing? | 6-phase migration playbook | Revenue retention during migration |
| How to comp sales? | GTM motion map by pricing model | Rep quota attainment, NRR |
| When to add BYOK? | When enterprise buyers demand it + you can maintain margin | Platform ARR, BYOK adoption % |

## Questions to Ask

1. What does the human equivalent of your AI product cost the buyer today? (This anchors your price ceiling)
2. What is your average cost per task/request at current volume? (Determines margin floor)
3. Can the customer measure a clear outcome from your product, or is the value diffuse?
4. What percentage of your revenue comes from your top 10% of customers? (Signals expansion opportunity)
5. Do your customers have existing contracts with LLM providers? (BYOK indicator)
6. What is your current gross margin, and what is your 12-month margin target?
7. How does your buyer currently budget for this spend? (Seat budget, IT budget, department budget, project budget)
8. What is your current churn rate, and does it correlate with pricing tier or usage level?
9. Are competitors moving to outcome or usage pricing? How are their customers reacting?
10. Do you have the billing infrastructure to support usage-based or outcome-based pricing?
11. What is the simplest charge metric your buyer would understand on an invoice?
12. How much pricing flexibility do existing contracts give you at renewal?
13. What data do you have on willingness-to-pay from customer conversations or win/loss analysis?
14. Is your sales team equipped to sell on value/outcomes, or are they trained on per-seat quotas?
15. What is your model cost breakdown by task type, and which tasks have the highest margin?

## Related Skills

| Skill | Relationship to AI Pricing |
|---|---|
| positioning-icp | ICP determines willingness-to-pay and which charge metric resonates |
| sales-motion-design | Pricing model dictates the sales motion, comp structure, and org design |
| solo-founder-gtm | Solo founders need the simplest viable pricing; start with one tier and iterate |
| gtm-metrics | Unit economics (CPT, CPR, CPAM) feed directly into pricing decisions |
| expansion-retention | Pricing structure determines expansion levers (usage growth, tier upgrades, new products) |
| gtm-engineering | Billing infrastructure must support the chosen pricing model (metering, credits, invoicing) |
