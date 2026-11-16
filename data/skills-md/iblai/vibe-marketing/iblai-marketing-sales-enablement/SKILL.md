---
name: iblai-marketing-sales-enablement
description: "When the user wants to create sales collateral, pitch decks, one-pagers, objection handling docs, or demo scripts. Also use when the user mentions 'sales deck,' 'pitch deck,' 'one-pager,' 'leave-behind,' 'objection handling,' 'deal-specific ROI analysis,' 'demo script,' 'talk track,' 'sales playbook,' 'proposal template,' 'buyer persona card,' 'help my sales team,' 'sales materials,' or 'what should I give my sales reps.' Use this for any document or asset that helps a sales team close deals. For competitor comparison pages and battle cards, see iblai-marketing-competitor-alternatives. For marketing website copy, see iblai-marketing-copywriting. For cold outreach emails, see iblai-marketing-cold-email."
globs:
alwaysApply: false
metadata:
  version: 1.1.0
---

# /iblai-marketing-sales-enablement

Build sales collateral reps actually use — decks, one-pagers, objection
docs, demo scripts, playbooks — assets that help close deals.

## Step 0: Context Check

Read `.agents/product-marketing-context.md` (or `.claude/product-marketing-context.md`
on older setups) first. Only ask for what isn't there.

Pull this context:

1. **Value proposition & differentiators**
   - What you sell and who it's for
   - What makes you different from the next best alternative
   - What outcomes you can prove

2. **Sales motion**
   - How you sell (self-serve, inside sales, field sales, hybrid)
   - Average deal size and sales cycle length
   - Key personas in the buying decision

3. **Collateral needs**
   - Specific assets needed
   - Funnel stage
   - Who will use them (AE, SDR, champion, prospect)

4. **Current state**
   - What materials exist today
   - What's working / what's not
   - What reps ask for most

---

## Core Principles

### Sales Uses What Sales Trusts
Involve reps in creation. Use their language, not marketing's. If reps rewrite your deck before sending, you wrote the wrong deck. Test drafts with top performers first.

### Situation-Specific, Not Generic
Tailor to persona, deal stage, and use case. A deck for a CTO should look different from one for a VP of Sales. A post-meeting follow-up one-pager serves a different purpose than a trade-show handout.

### Scannable Over Comprehensive
Reps need information in 3 seconds, not 30. Bold headers, short bullets, visual hierarchy. If a rep can't find the answer mid-call, the doc has failed.

### Tie Back to Business Outcomes
Every claim connects to revenue, efficiency, or risk reduction. Features mean nothing without "so what." Replace "AI-powered analytics" with "cut reporting time by 80%."

---

## Sales Deck / Pitch Deck

### 10-12 Slide Framework

1. **Current World Problem** — the pain your buyer lives with today
2. **Cost of the Problem** — what inaction costs (time, money, risk)
3. **The Shift Happening** — market or tech change creating urgency
4. **Your Approach** — how you solve it differently
5. **Product Walkthrough** — 3-4 key workflows, not a feature tour
6. **Proof Points** — metrics, logos, analyst recognition
7. **Case Study** — one customer story, told well
8. **Implementation / Timeline** — how they get from here to live
9. **ROI / Value** — expected return and payback period
10. **Pricing Overview** — transparent, tiered if applicable
11. **Next Steps / CTA** — clear action with timeline

### Deck Principles

- **Story arc, not feature tour.** Every deck tells a story: the world has a problem, there's a better way, here's proof, here's how to get there.
- **One idea per slide.** Two points → two slides.
- **Design for presenting, not reading.** Slides support the conversation; they don't replace it. Minimal text, strong visuals.

### Customization by Buyer Type

| Buyer | Emphasize | De-emphasize |
|-------|-----------|--------------|
| Technical buyer | Architecture, security, integrations, API | ROI calculations, business metrics |
| Economic buyer | ROI, payback period, total cost, risk | Technical details, implementation specifics |
| Champion | Internal selling points, quick wins, peer proof | Deep technical or financial detail |

Full slide-by-slide guidance: [references/deck-frameworks.md](references/deck-frameworks.md).

---

## One-Pagers / Leave-Behinds

### When to Use

- **Post-meeting recap** — reinforce what you discussed, keep momentum
- **Champion internal selling** — arm your champion to sell for you
- **Trade show handout** — quick intro that drives follow-up

### Structure

1. **Problem statement** — the pain in one sentence
2. **Your solution** — what you do and how
3. **3 differentiators** — why you vs. alternatives
4. **Proof point** — one strong metric or customer quote
5. **CTA** — clear next step with contact info

### Design Principles

- One page, literally. Front only, or front and back max.
- Scannable in 30 seconds. Bold headers, short bullets, whitespace.
- Include logo, website, and a specific contact (not info@).
- Match your brand but keep it clean — this is a sales tool, not a brand piece.

Templates by use case: [references/one-pager-templates.md](references/one-pager-templates.md).

---

## Objection Handling Docs

### Objection Categories

| Category | Examples |
|----------|----------|
| Price | "Too expensive," "No budget this quarter," "Competitor is cheaper" |
| Timing | "Not the right time," "Maybe next quarter," "Too busy to implement" |
| Competition | "We already use X," "What makes you different?" |
| Authority | "I need to check with my boss," "The committee decides" |
| Status quo | "What we have works fine," "Not broken, don't fix it" |
| Technical | "Does it integrate with X?," "Security concerns," "Can it scale?" |

### Response Framework

Per objection, document:

1. **Objection statement** — exactly how reps hear it
2. **Why they say it** — the real concern behind the words
3. **Response approach** — how to acknowledge and redirect
4. **Proof point** — specific evidence that addresses the concern
5. **Follow-up question** — keep the conversation moving forward

### Two Formats

- **Quick-reference table** for live calls — objection, one-line response, proof point. Fits on one screen.
- **Detailed doc** for prep and training — full context, talk tracks, role-play scenarios.

Full objection library: [references/objection-library.md](references/objection-library.md).

---

## ROI Calculators & Value Props

### Calculator Design

**Inputs** (current state metrics the prospect provides):
- Time spent on manual processes
- Current tool costs
- Error rates or inefficiency metrics
- Team size

**Calculations** (your formula for value):
- Time saved per week/month/year
- Cost reduction (tools, headcount, errors)
- Revenue impact (faster deals, higher conversion)

**Outputs** (what the prospect sees):
- Annual ROI percentage
- Payback period in months
- Total 3-year value

### Value Prop by Persona

| Persona | Cares About | Lead With |
|---------|-------------|-----------|
| CTO / VP Eng | Architecture, scale, security, team velocity | Technical superiority, integration depth |
| VP Sales | Pipeline, quota attainment, rep productivity | Revenue impact, time savings per rep |
| CFO | Total cost, payback period, risk | ROI, cost reduction, financial predictability |
| End user | Ease of use, daily workflow, learning curve | Time saved, frustration eliminated |

### Implementation Options

- **Spreadsheet** — fastest to build, easy to customize per deal. Works for inside sales.
- **Web tool** — more polished, captures leads, scales better. Worth building if deal volume is high.
- **Slide-based** — ROI story embedded in the deck. Good for executive presentations.

---

## Demo Scripts & Talk Tracks

### Script Structure

1. **Opening** (2 min) — context setting, agenda, confirm goals for the call
2. **Discovery recap** (3 min) — summarize what you learned, confirm priorities
3. **Solution walkthrough** (15-20 min) — 3-4 key workflows mapped to their pain
4. **Interaction points** — questions during the demo, not just at the end
5. **Close** (5 min) — summarize value, propose next steps with timeline

### Talk Track Types

| Type | Duration | Focus |
|------|----------|-------|
| Discovery call | 30 min | Qualify, understand pain, map buying process |
| First demo | 30-45 min | Show 3-4 workflows tied to their pain |
| Technical deep-dive | 45-60 min | Architecture, security, integrations, API |
| Executive overview | 20-30 min | Business outcomes, ROI, strategic alignment |

### Key Principles

- **Demo after discovery, not before.** If you don't know their pain, you're guessing which features matter.
- **Customize to their use case.** Use their terminology, their data (if possible), their workflow.
- **Leave time for questions.** A demo where the prospect doesn't talk is a demo that doesn't close.

Full script templates: [references/demo-scripts.md](references/demo-scripts.md).

---

## Case Study Briefs (Sales Format)

### How Sales Case Studies Differ

Marketing case studies tell a story. Sales case studies arm reps with fast-access proof. Short, outcome-focused, tagged for retrieval.

### Structure

1. **Customer profile** — industry, company size, buyer role
2. **Challenge** — what they were struggling with (2-3 sentences)
3. **Solution** — what they implemented (1-2 sentences)
4. **Results** — 3 specific metrics (before/after)
5. **Pull quote** — one sentence from the customer
6. **Tags** — industry, use case, company size, persona

### Organization

Organize case studies so reps find the right one instantly:
- **By industry** — "Show me a case study for healthcare"
- **By use case** — "Show me someone who used us for X"
- **By company size** — "Show me an enterprise example"

---

## Proposal Templates

### Structure

1. **Executive summary** — their challenge, your solution, expected outcome (1 page max)
2. **Proposed solution** — what you'll deliver, mapped to their requirements
3. **Implementation plan** — timeline, milestones, responsibilities
4. **Investment** — pricing, payment terms, what's included
5. **Next steps** — how to move forward, decision timeline

### Customization Guidance

- Mirror their language from discovery calls
- Reference specific pain points they mentioned
- Include only relevant case studies (same industry or use case)
- Name the stakeholders you've spoken with

### Common Mistakes

- **Too long** — if it's over 10 pages, it won't get read. Aim for 5-7.
- **Too generic** — templated proposals signal low effort. Customize the exec summary at minimum.
- **Burying the price** — don't make them hunt for it. Be transparent and confident.

---

## Sales Playbooks

### What Goes In

- **Buyer profile** — who you're selling to, their goals and pains
- **Qualification criteria** — BANT, MEDDIC, or your framework
- **Discovery questions** — organized by topic, not a script
- **Objection handling** — top 10 objections with responses
- **Competitive positioning** — how you win against each competitor
- **Demo flow** — recommended sequence per persona
- **Email templates** — follow-up, proposal, check-in, breakup

### When to Build

- **New product launch** — reps need a single source of truth
- **New market segment** — different buyers need different approaches
- **New hire ramp** — playbooks cut ramp time significantly

### Keeping It Living

Playbooks die when they're not updated. Review quarterly, get input from top reps, remove what's outdated. Assign an owner — if nobody owns it, it rots.

---

## Buyer Persona Cards

### Card Structure

| Field | Description |
|-------|-------------|
| Role / title | Common titles and reporting structure |
| Goals | What success looks like for them |
| Pains | What frustrates them daily |
| Top objections | The 3-5 objections you'll hear from this role |
| Evaluation criteria | How they judge solutions |
| Buying process | Their role in the decision, who they influence |
| Messaging angle | The one sentence that resonates most |

### Persona Types

- **Economic buyer** — signs the check. Cares about ROI and risk.
- **Technical buyer** — evaluates the product. Cares about capabilities and integration.
- **End user** — uses it daily. Cares about ease and workflow fit.
- **Champion** — advocates internally. Needs ammunition to sell for you.
- **Blocker** — opposes the purchase. Understand their concern to neutralize it.

---

## Output Format

Deliver the right format for each asset:

| Asset | Deliverable |
|-------|-------------|
| Sales deck | Slide-by-slide outline with headline, body copy, speaker notes |
| One-pager | Full copy with layout guidance (visual hierarchy, sections) |
| Objection doc | Table: objection, response, proof point, follow-up |
| Demo script | Scene-by-scene with timing, talk track, interaction points |
| ROI calculator | Input fields, formulas, output display with sample data |
| Playbook | Structured document with table of contents and sections |
| Persona card | One-page card format per persona |
| Proposal | Section-by-section copy with customization notes |

---

## Task-Specific Questions

If context is missing:

1. What collateral do you need? (Deck, one-pager, objection doc, etc.)
2. Who will use it? (AE, SDR, champion, prospect)
3. What sales stage? (Prospecting, discovery, demo, negotiation, close)
4. Target persona? (Title, seniority, department)
5. Top 3 objections you hear most?

---

## Tool Integrations

For partner sales enablement, see the [tools registry](../../tools/REGISTRY.md):

| Tool | What It Does | Guide |
|------|-------------|-------|
| **Introw** | Partner engagement tracking, deal registration, mutual action plans | [introw.md](../../tools/integrations/introw.md) |

---

## Related Skills

- **iblai-marketing-competitor-alternatives**: Public-facing comparison and alternative pages
- **iblai-marketing-copywriting**: Marketing website copy
- **iblai-marketing-cold-email**: Outbound prospecting emails
- **iblai-marketing-revops**: Lead lifecycle, scoring, routing, pipeline management
- **iblai-marketing-pricing-strategy**: Pricing decisions and packaging
- **iblai-marketing-product-context**: Foundational positioning and messaging
