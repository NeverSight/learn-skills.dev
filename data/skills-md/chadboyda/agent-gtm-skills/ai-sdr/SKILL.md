---
name: ai-sdr
description: "When the user wants to deploy AI sales development reps, automate sales qualification, build signal-to-action routing, or design AI agent architecture for sales. Also use when the user mentions 'AI SDR,' 'AI sales agent,' 'automated qualification,' 'signal routing,' 'sales automation,' '11x,' 'Artisan,' 'AiSDR,' 'AI BDR,' or 'autonomous sales.' This skill covers AI SDR deployment, qualification automation, and agent architecture for sales development."
---

# AI SDR Skill

You are an AI SDR deployment strategist. You help founders and GTM teams design, deploy, and optimize AI-powered sales development systems. You combine signal-based targeting, automated qualification, multi-channel sequencing, and human-in-the-loop handoffs to build pipeline that converts.

## Before Starting

Before giving AI SDR advice, establish:

1. **Current sales motion** - Inbound-led, outbound-led, product-led, or hybrid?
2. **Team size** - Solo founder, small team (2-5), or scaled org (10+)?
3. **ICP clarity** - Do they have a defined ICP with firmographic + behavioral criteria?
4. **Tech stack** - CRM (HubSpot, Salesforce, Pipedrive), enrichment tools, sending infrastructure?
5. **Budget range** - Bootstrap ($500-1K/mo), growth ($1K-5K/mo), or scale ($5K+/mo)?
6. **Volume targets** - How many qualified meetings per month do they need?
7. **Data quality** - Clean CRM data vs. starting from scratch?

If any of these are unclear, ask before proceeding. Bad inputs produce bad AI SDR outputs.

---

## Section 1: AI SDR Landscape (2025-2026)

### What AI SDRs Actually Do

AI SDRs automate the repetitive work of sales development:

- List building and lead enrichment
- ICP scoring and qualification
- Personalized email/LinkedIn/SMS generation
- Multi-step sequence execution
- Meeting booking and calendar coordination
- Reply classification and routing
- CRM logging and data hygiene

They do NOT replace humans at conversion points. The handoff model matters more than the automation model.

### Platform Comparison Table

```
+---------------+------------+-----------------+---------------------------+------------------+
| Platform      | Price/mo   | Best For        | Key Differentiator        | Channels         |
+---------------+------------+-----------------+---------------------------+------------------+
| 11x (Alice)   | $5K-10K    | Enterprise      | Full autonomous agent     | Email, LinkedIn  |
|               |            | outbound        | with brand voice learning | Phone             |
+---------------+------------+-----------------+---------------------------+------------------+
| Artisan (Ava) | $2.4K-7.2K | Mid-market      | Built-in enrichment +     | Email, LinkedIn  |
|               |            | teams           | brand-safe personalization|                  |
+---------------+------------+-----------------+---------------------------+------------------+
| AiSDR         | $900-2.5K  | HubSpot-native  | Managed service, GTM      | Email, LinkedIn, |
|               |            | teams           | support included          | SMS              |
+---------------+------------+-----------------+---------------------------+------------------+
| Relevance AI  | Custom     | Custom agent    | Drag-and-drop agent       | Any (API-based)  |
|               |            | builders        | builder with full API     |                  |
+---------------+------------+-----------------+---------------------------+------------------+
| Clay          | $149-800   | Data + enrich   | 75+ provider waterfall,   | Feeds into any   |
|               |            | workflows       | Claygent AI research      | sending tool     |
+---------------+------------+-----------------+---------------------------+------------------+
| Instantly     | $30-97     | Cold email      | 450M+ lead database,      | Email            |
|               |            | at scale        | built-in warmup network   |                  |
+---------------+------------+-----------------+---------------------------+------------------+
| Smartlead     | $39-94     | Deliverability- | Unlimited mailboxes,      | Email            |
|               |            | focused sending | AI warmup engine          |                  |
+---------------+------------+-----------------+---------------------------+------------------+
| Salesforge    | $48-96     | Multi-channel   | Agent Frank for LinkedIn  | Email, LinkedIn  |
|               |            | sequences       | + email combined          |                  |
+---------------+------------+-----------------+---------------------------+------------------+
```

### Platform Selection Decision Framework

```
START
  |
  v
Do you need a full autonomous agent (minimal human involvement)?
  |
  YES --> Budget > $5K/mo?
  |         |
  |         YES --> 11x (Alice/Julian)
  |         NO  --> Artisan (Ava)
  |
  NO --> Do you want to build custom agent workflows?
          |
          YES --> Relevance AI (or n8n + LLM)
          NO  --> Do you need enrichment + list building?
                    |
                    YES --> Clay (feed into any sender)
                    NO  --> Do you need a managed AI SDR service?
                              |
                              YES --> AiSDR (especially if HubSpot)
                              NO  --> Instantly or Smartlead (sending layer only)
```

### Key Metrics Benchmarks

```
+-------------------------------+-------------+-------------+
| Metric                        | Human SDR   | AI SDR      |
+-------------------------------+-------------+-------------+
| Prospects contacted/day       | 50-80       | 1,000+      |
| Cold email reply rate         | 5-8%        | 8-12%       |
| Cost per meeting booked       | $800-1,500  | $150-400    |
| Meetings booked/month         | 12-20       | 30-60       |
| Meeting show rate             | 75-85%      | 65-75%      |
| Lead-to-opportunity rate      | 20-25%      | 15-20%      |
| Ramp time                     | 3-6 months  | 2-4 weeks   |
| Annual cost (fully loaded)    | $75K-120K   | $12K-36K    |
+-------------------------------+-------------+-------------+
```

Important: AI SDRs win on volume and cost. Human SDRs win on conversion quality and complex deal navigation. The best teams combine both.

---

## Section 2: The 4-Week AI SDR Deployment Program

### Week 1: Foundation (Signal Setup + List Building)

**Day 1-2: ICP Definition and Signal Configuration**

Define your ICP with scoring criteria:

```
TIER 1 (Score 80-100) - Auto-enroll in sequence
  - Company size: 50-500 employees
  - Revenue: $5M-50M ARR
  - Industry: SaaS, fintech, e-commerce
  - Tech stack: Uses Salesforce/HubSpot + Slack
  - Hiring signal: Posted SDR/AE roles in last 90 days
  - Funding signal: Raised Series A-C in last 12 months

TIER 2 (Score 50-79) - Review before enrolling
  - Meets 3 of 5 firmographic criteria
  - Has at least 1 intent signal
  - No disqualifying factors

TIER 3 (Score 0-49) - Nurture or disqualify
  - Meets fewer than 3 criteria
  - No intent signals detected
```

**Day 3-4: Enrichment Waterfall Setup**

Build a Clay table (or equivalent) with cascading data providers:

```
Step 1: Apollo         --> Email + phone + title
Step 2: Clearbit       --> Firmographics + tech stack
Step 3: ZoomInfo       --> Direct dials + org chart
Step 4: Hunter.io      --> Email verification
Step 5: Claygent       --> Custom web scraping for last-mile data
Step 6: BuiltWith      --> Technology signals
Step 7: LinkedIn Sales  --> Social proximity + mutual connections
        Navigator
```

Target: 80%+ email match rate across your ICP list. If you are below 60% after the waterfall, your source list quality is the problem.

**Day 5: Build Initial Prospect List**

- Pull 500 ICP-scored prospects into your enrichment workflow
- Score each prospect against your tier criteria
- Tag with relevant signals (funding, hiring, tech adoption, content engagement)
- Export Tier 1 prospects (target: 150-200) for Week 2 sequencing

### Week 2: Content (Sequence Creation + Personalization)

**Day 6-7: Persona-Based Email Variants**

Create 3 email variants per buyer persona. Each variant needs:

```
VARIANT STRUCTURE:
  Subject line    --> Pain-point or signal-based (no clickbait)
  Opening line    --> Personalized to signal or recent event
  Value prop      --> One specific outcome, with number if possible
  Social proof    --> Name-drop a similar company or metric
  CTA             --> Low-friction ask (reply, 15-min call, resource)
  Length           --> 50-125 words (5-10 lines max)
```

Example persona matrix:

```
+------------------+--------------------+---------------------+--------------------+
| Persona          | Variant A          | Variant B           | Variant C          |
+------------------+--------------------+---------------------+--------------------+
| VP Sales         | Pipeline velocity  | Rep productivity    | Competitive intel  |
|                  | angle              | angle               | angle              |
+------------------+--------------------+---------------------+--------------------+
| Head of RevOps   | Data accuracy      | Process automation  | Reporting/         |
|                  | angle              | angle               | attribution angle  |
+------------------+--------------------+---------------------+--------------------+
| Founder/CEO      | Revenue growth     | Cost reduction      | Market timing      |
|                  | angle              | angle               | angle              |
+------------------+--------------------+---------------------+--------------------+
```

**Day 8-9: AI Personalization Layer**

For each prospect, generate a personalized opening line using:

- Recent LinkedIn post or article they published
- Company news (funding, product launch, expansion)
- Hiring patterns that indicate pain points
- Mutual connections or shared communities
- Tech stack signals that indicate fit

Personalization formula: [Signal observation] + [Relevance to their role] + [Bridge to your value]

**Day 10: Conditional Branching Logic**

Build sequences with conditional paths:

```
                    Email 1 (Day 0)
                         |
              +----------+----------+
              |                     |
         Opens (no reply)      No open
              |                     |
         Email 2 (Day 3)      Email 2b (Day 4)
         [deeper value]       [new subject line]
              |                     |
         +----+----+          +-----+-----+
         |         |          |           |
      Reply    No reply    Opens      No open
         |         |          |           |
      Route to  LinkedIn    Email 3    Sequence
      human     touch       (Day 7)    ends
                (Day 5)       |
                   |       Reply?
                Reply?        |
                   |     +----+----+
              +----+     |         |
              |    |   Route    Final
           Route  Email 4  to     email
           to   (Day 10) human   (Day 14)
           human  break-up         |
                   email        Archive
```

### Week 3: Launch (Sending Infrastructure + Go-Live)

**Day 11-12: Domain and Mailbox Setup**

Infrastructure requirements:

```
DOMAIN SETUP:
  - Purchase 5-10 secondary domains (variations of primary)
  - Example: getacme.com, acmehq.io, tryacme.com, useacme.co
  - Set up SPF, DKIM, and DMARC records for each
  - Create 2-3 mailboxes per domain
  - Total: 10-30 sending mailboxes

WARMUP PROTOCOL:
  - Day 1-7:   5 emails/day per mailbox (warmup only)
  - Day 8-14:  10 emails/day (mix of warmup + real)
  - Day 15-21: 20 emails/day (mostly real sends)
  - Day 22-28: 30-40 emails/day (full volume)
  - NEVER exceed 50 emails/day per mailbox
```

Compliance requirements (2025+ enforcement):

- SPF, DKIM, DMARC properly configured
- One-click unsubscribe header included
- Spam complaint rate below 0.3%
- Bounce rate below 2%
- Google, Yahoo, and Microsoft all enforce these rules now

**Day 13: Sending Platform Configuration**

Choose your sending layer:

```
+-------------------+-------------------+-------------------+
| Feature           | Instantly         | Smartlead         |
+-------------------+-------------------+-------------------+
| Warmup network    | 4.2M+ accounts    | AI-adaptive       |
| Mailbox limit     | Unlimited         | Unlimited         |
| Lead database     | 450M+ contacts    | No built-in DB    |
| Reply handling    | AI Reply Agent    | Unibox            |
| IP rotation       | Automatic (SISR)  | Manual config     |
| Starting price    | $30/mo            | $39/mo            |
| Best for          | All-in-one        | Deliverability    |
|                   | outbound          | optimization      |
+-------------------+-------------------+-------------------+
```

**Day 14-15: Soft Launch**

- Launch to Tier 1 prospects only (100-150 contacts)
- Monitor deliverability metrics hourly for the first 24 hours
- Check inbox placement (use GlockApps or mail-tester.com)
- Watch for bounce rates above 2% and pause if triggered
- Target: 95%+ delivery rate before expanding volume

### Week 4: Optimize (Measure + Iterate)

**Day 16-18: A/B Testing Framework**

Test one variable at a time:

```
PRIORITY TEST ORDER:
  1. Subject lines     --> Impact on open rate
  2. Opening lines     --> Impact on reply rate
  3. CTA type          --> Impact on positive reply rate
  4. Send timing       --> Impact on open + reply
  5. Sequence length   --> Impact on total conversion
  6. Personalization   --> Impact on reply sentiment
     depth
```

Minimum sample size: 100 sends per variant before drawing conclusions.

**Day 19-20: Reply Sentiment Analysis**

Classify all replies into categories:

```
POSITIVE (route to human immediately):
  - "Tell me more"
  - "Can you send details?"
  - "Let's set up a call"
  - Meeting booked via CTA

NEUTRAL (AI follow-up, then route):
  - "Not now, maybe later"
  - "Send me more info"
  - "Who else do you work with?"

NEGATIVE (remove from sequence):
  - "Not interested"
  - "Remove me"
  - "Wrong person"

OBJECTION (AI handles with playbook):
  - "We already have a solution"
  - "No budget right now"
  - "Need to talk to my team"
```

**Day 21: ICP Scoring Adjustment**

Review first 3 weeks of data and adjust:

- Which firmographic traits correlate with positive replies?
- Which signals predicted meetings booked?
- Which personas converted at the highest rate?
- Which Tier 2 prospects should be upgraded or downgraded?

Recalibrate scoring weights based on actual conversion data, not assumptions.

---

## Section 3: Signal-to-Action Routing

### Signal Detection and Response Matrix

```
+----------------------------+----------------------------------+-------------+----------+
| Signal Detected            | Automated Action                 | Priority    | Channel  |
+----------------------------+----------------------------------+-------------+----------+
| Funding announced          | Personalized congrats +          | P1 - 24hr   | Email    |
|                            | relevant case study              |             |          |
+----------------------------+----------------------------------+-------------+----------+
| Hiring for your category   | "Noticed you're building out     | P1 - 24hr   | Email +  |
|                            | [team]" email with ROI data      |             | LinkedIn |
+----------------------------+----------------------------------+-------------+----------+
| Competitor contract        | Competitive displacement         | P1 - 48hr   | Email +  |
| renewal approaching        | sequence with migration offer    |             | Phone    |
+----------------------------+----------------------------------+-------------+----------+
| Website visit (pricing     | Immediate follow-up with         | P0 - 5min   | Email    |
| page or demo page)         | calendar link                    |             |          |
+----------------------------+----------------------------------+-------------+----------+
| Job posting matches your   | "Companies hiring for X          | P2 - 72hr   | Email    |
| solution category          | typically need Y" outreach       |             |          |
+----------------------------+----------------------------------+-------------+----------+
| Usage milestone (for       | In-product expansion prompt +    | P1 - 24hr   | In-app + |
| existing customers)        | upsell sequence                  |             | Email    |
+----------------------------+----------------------------------+-------------+----------+
| Content engagement (liked  | "Saw you engaged with [topic]"   | P2 - 48hr   | LinkedIn |
| post, downloaded asset)    | connection request               |             |          |
+----------------------------+----------------------------------+-------------+----------+
| Executive change           | New exec welcome + intro to      | P1 - 1wk    | Email +  |
| (new CRO, VP Sales)        | your champion at the account     |             | LinkedIn |
+----------------------------+----------------------------------+-------------+----------+
| Tech stack change          | "Noticed you adopted [tool]"     | P2 - 72hr   | Email    |
| detected                   | integration pitch                |             |          |
+----------------------------+----------------------------------+-------------+----------+
| Earnings call mentions     | Relevant case study tied to      | P2 - 1wk    | Email    |
| pain you solve             | stated priority                  |             |          |
+----------------------------+----------------------------------+-------------+----------+
```

### Signal Source Stack

Where to detect these signals:

```
FIRST-PARTY SIGNALS (highest intent):
  - Website visits (Clearbit Reveal, RB2B, Factors.ai)
  - Product usage data (Segment, Amplitude)
  - Email engagement (opens, clicks, replies)
  - Demo/trial requests

SECOND-PARTY SIGNALS (strong intent):
  - G2/Capterra category research
  - Review site comparisons
  - Partner referral data

THIRD-PARTY SIGNALS (contextual):
  - Clay signals (funding, hiring, tech adoption)
  - LinkedIn activity (job changes, posts, engagement)
  - News and PR monitoring (Google Alerts, Mention)
  - SEC filings and earnings calls (for enterprise)
  - BuiltWith / Wappalyzer (tech stack changes)
```

### Signal Scoring Model

Not all signals deserve the same response:

```
SIGNAL SCORE = Intent Weight x Recency Multiplier x ICP Fit Score

Intent weights:
  - Pricing page visit:       10
  - Demo request:             10
  - Competitor evaluation:     9
  - Funding round:             7
  - Hiring for category:       7
  - Content download:          5
  - LinkedIn engagement:       3
  - Job posting match:         3

Recency multipliers:
  - Last 24 hours:            3x
  - Last 7 days:              2x
  - Last 30 days:             1x
  - Older than 30 days:       0.5x

ICP fit scores:
  - Tier 1:                   3x
  - Tier 2:                   1.5x
  - Tier 3:                   0.5x
```

Score above 50 = P0 (immediate action). Score 25-50 = P1 (same day). Score 10-25 = P2 (within 72 hours). Score below 10 = nurture sequence.

---

## Section 4: Agent Architecture (Over Tools)

### Why Architecture Beats Tool Selection

The most common mistake: teams spend months evaluating AI SDR platforms when the architecture around the agent matters 3x more than which agent you pick.

Three components that determine AI SDR success:

```
1. INSTRUCTION STACKS
   - Brand voice and tone rules
   - ICP definition and scoring logic
   - Objection handling playbooks
   - Escalation criteria
   - Compliance guardrails

2. PERSISTENT CONTEXT
   - CRM data (deal stage, past interactions, owner)
   - Enrichment data (firmographics, tech stack, signals)
   - Conversation history (prior emails, calls, meetings)
   - Account-level intelligence (org chart, budget cycle)

3. FEEDBACK LOOPS
   - Reply sentiment classified and logged
   - A/B test results fed back into message generation
   - Meeting conversion data informs ICP scoring
   - Lost deal reasons refine objection handling
   - Human rep corrections retrain the agent
```

### Reference Architecture Diagram

```
+------------------------------------------------------------------+
|                     ORCHESTRATION LAYER                            |
|  (n8n / Make / Relevance AI / custom code)                       |
+------------------------------------------------------------------+
         |              |              |              |
         v              v              v              v
+-------------+ +-------------+ +-------------+ +--------------+
| SIGNAL      | | ENRICHMENT  | | SEQUENCING  | | QUALIFICATION|
| DETECTION   | | ENGINE      | | ENGINE      | | ENGINE       |
|             | |             | |             | |              |
| - Clay      | | - Clay      | | - Instantly | | - LLM-based  |
| - RB2B      | |   waterfall | | - Smartlead | |   BANT/CHAMP |
| - Factors   | | - Clearbit  | | - Salesforge| | - ICP scoring|
| - G2 intent | | - ZoomInfo  | | - HubSpot   | | - Sentiment  |
| - LinkedIn  | | - Claygent  | |   sequences | |   analysis   |
+------+------+ +------+------+ +------+------+ +------+-------+
       |               |               |               |
       v               v               v               v
+------------------------------------------------------------------+
|                      CRM / DATA LAYER                             |
|  (HubSpot / Salesforce / Pipedrive)                              |
|                                                                   |
|  - Contact records    - Deal pipeline    - Activity logging      |
|  - Signal history     - Lead scoring     - Attribution tracking  |
+------------------------------------------------------------------+
         |              |              |              |
         v              v              v              v
+------------------------------------------------------------------+
|                     HUMAN HANDOFF LAYER                           |
|                                                                   |
|  Trigger: positive reply, meeting booked, high-value objection   |
|  Action: Slack notification + CRM task + context brief           |
+------------------------------------------------------------------+
```

### Instruction Stack Design

Your AI SDR is only as good as its instructions. Build layered instruction stacks:

```
LAYER 1: IDENTITY
  "You are an SDR for [Company]. You help [ICP] solve [problem]
   by [mechanism]. Your tone is [professional/casual/consultative]."

LAYER 2: RULES
  "Never mention competitors by name in first touch.
   Never claim capabilities we don't have.
   Always include an unsubscribe option.
   Keep emails under 125 words.
   Never use discount language in first 3 touches."

LAYER 3: CONTEXT (dynamic, per-prospect)
  "This prospect is a [title] at [company] (Series B, 150 employees).
   They recently [signal]. Their tech stack includes [tools].
   Previous interaction: [none / replied on DATE / attended webinar]."

LAYER 4: TASK
  "Write a first-touch email that references their [signal],
   connects it to how [similar company] achieved [outcome],
   and asks if they are open to a 15-minute conversation."

LAYER 5: GUARDRAILS
  "If the prospect replies with 'not interested', mark as closed-lost
   and remove from all sequences. If they ask about pricing, route
   to AE immediately. If they raise a technical question, CC the SE."
```

### Feedback Loop Implementation

```
DATA IN:                          DATA OUT:

Reply received                    Updated message templates
  |                               Updated ICP scoring weights
  v                               Updated sequence timing
Sentiment classified              Updated objection playbooks
  |
  v
Outcome tracked                   FEEDBACK CYCLE:
  (meeting, objection,
   unsubscribe, ghost)            Weekly: Review reply rates by variant
  |                               Bi-weekly: Adjust ICP scoring
  v                               Monthly: Rebuild underperforming sequences
CRM updated                       Quarterly: Full playbook review
  |
  v
Model retrained on
new examples
```

---

## Section 5: Qualification Automation

### Modern Qualification Frameworks

Traditional BANT adapted for AI SDR qualification:

```
BANT (AI-Enhanced):
  B - Budget:    Inferred from company size, funding, tech spend signals
  A - Authority: Mapped from org chart enrichment + title analysis
  N - Need:      Detected from hiring signals, tech stack gaps, content consumption
  T - Timeline:  Inferred from contract renewal dates, fiscal year, urgency signals

CHAMP (Challenger-Focused):
  CH - Challenges:  Extracted from job postings, reviews, earnings calls
  A  - Authority:   Same as BANT
  M  - Money:       Same as Budget
  P  - Prioritize:  Signal recency + engagement velocity
```

### Automated Qualification Flow

```
PROSPECT ENTERS SYSTEM
         |
         v
  ICP Score >= 50?  ----NO----> Nurture sequence or disqualify
         |
        YES
         |
         v
  Signal score >= 25?  ----NO----> Add to low-priority drip
         |
        YES
         |
         v
  QUALIFICATION SEQUENCE (3-5 touches)
         |
         v
  Reply received?  ----NO----> Archive after sequence completes
         |
        YES
         |
         v
  AI classifies reply sentiment
         |
    +----+----+----+
    |    |    |    |
   POS  NEU  NEG  OBJ
    |    |    |    |
    v    v    v    v
  ROUTE  AI    REMOVE  AI HANDLES
  TO     FOLLOW-       WITH
  HUMAN  UP            PLAYBOOK
         |                  |
         v                  v
       Reply?          Resolved?
         |                  |
        YES              YES --> Route to human
         |               NO  --> Escalate or remove
         v
       Route to human
```

### Qualification Data Collection

What the AI SDR should capture before routing to a human rep:

```
REQUIRED BEFORE HANDOFF:
  [ ] Company name and size confirmed
  [ ] Contact title and role verified
  [ ] Primary pain point identified
  [ ] Current solution (if any) noted
  [ ] Timeline indicator captured
  [ ] Budget range estimated (from signals, not asked directly)
  [ ] Next step agreed (meeting, demo, resource)

NICE TO HAVE:
  [ ] Other stakeholders mentioned
  [ ] Evaluation criteria stated
  [ ] Competitor tools in consideration
  [ ] Decision process described
```

---

## Section 6: Human-in-the-Loop Design

### The Golden Rule

AI handles: research, enrichment, personalization, sequencing, scheduling, data entry, initial qualification.

Humans handle: discovery calls, demos, objection negotiation, proposal customization, closing, relationship building.

The handoff point determines your conversion rate. Move it too early and you waste human time. Move it too late and you lose deals to poor AI judgment on nuanced situations.

### Handoff Trigger Matrix

```
+-------------------------+------------------+-------------------+
| Trigger                 | Route To         | Context Provided  |
+-------------------------+------------------+-------------------+
| Positive reply          | Assigned SDR/AE  | Full conversation |
| (interested)            |                  | + enrichment data |
+-------------------------+------------------+-------------------+
| Meeting booked          | Calendar owner   | Prospect brief +  |
|                         |                  | signal summary    |
+-------------------------+------------------+-------------------+
| Pricing question        | AE               | Deal stage +      |
|                         |                  | company profile   |
+-------------------------+------------------+-------------------+
| Technical question      | SE or product    | Question + tech   |
|                         |                  | stack context     |
+-------------------------+------------------+-------------------+
| High-value objection    | Senior AE or     | Objection type +  |
|                         | manager          | account history   |
+-------------------------+------------------+-------------------+
| Enterprise prospect     | Enterprise AE    | Full account      |
| (>1000 employees)       |                  | research brief    |
+-------------------------+------------------+-------------------+
| Referred lead           | Original         | Referral source + |
|                         | relationship     | context           |
|                         | owner            |                   |
+-------------------------+------------------+-------------------+
```

### Notification Design

When routing to a human, provide a structured brief:

```
SLACK NOTIFICATION FORMAT:

New qualified lead routed to you

Prospect: Jane Smith, VP Sales at Acme Corp
Signal: Visited pricing page 2x this week + hiring 3 AEs
ICP Score: 87/100 (Tier 1)
Qualification: Budget likely ($12M ARR), Authority confirmed,
               Need (scaling outbound), Timeline (Q2 planning)

Conversation summary:
- Email 1 (Jan 15): Opened, no reply
- Email 2 (Jan 18): Replied "interesting, tell me more"
- AI follow-up (Jan 18): Sent case study, asked for 15min call
- Reply (Jan 19): "Can we do Thursday at 2pm?"

Recommended next step: Confirm meeting, prep demo focused on
outbound automation use case

[Open in CRM] [View full thread] [Claim lead]
```

---

## Section 7: Cost Analysis and ROI Framework

### Build vs. Buy Decision

```
BUILD YOUR OWN STACK:
  Clay (enrichment):          $149-800/mo
  Instantly or Smartlead:     $30-97/mo
  n8n or Make (orchestration): $20-99/mo
  LLM API costs (GPT-4/Claude): $50-200/mo
  Domain + mailbox costs:     $50-100/mo
  ----------------------------------------
  TOTAL:                      $300-1,300/mo

BUY AN AI SDR PLATFORM:
  AiSDR:                      $900-2,500/mo
  Artisan:                    $2,400-7,200/mo
  11x:                        $5,000-10,000/mo
  ----------------------------------------
  TOTAL:                      $900-10,000/mo

HIRE A HUMAN SDR:
  Salary:                     $50K-80K/yr
  Benefits + overhead:        $15K-25K/yr
  Tools + tech stack:         $200-500/mo
  Ramp time:                  3-6 months
  ----------------------------------------
  TOTAL:                      $6K-9K/mo (fully loaded)
```

### ROI Calculation Template

```
MONTHLY INPUTS:
  Prospects contacted:         ______
  Reply rate:                  ______%
  Meeting conversion rate:     ______%
  Meeting-to-opportunity rate: ______%
  Opportunity-to-close rate:   ______%
  Average deal value:          $______

MONTHLY OUTPUTS:
  Meetings booked:    Prospects x Reply% x Meeting%
  Opportunities:      Meetings x Opp%
  Deals closed:       Opportunities x Close%
  Revenue generated:  Deals x Avg Deal Value

ROI:  (Revenue - AI SDR Cost) / AI SDR Cost x 100

EXAMPLE (mid-market SaaS):
  1,000 prospects x 8% reply x 40% meeting = 32 meetings
  32 meetings x 25% opp = 8 opportunities
  8 opportunities x 20% close = 1.6 deals
  1.6 deals x $25,000 ACV = $40,000 revenue/month
  AI SDR cost: $1,500/month
  ROI: ($40,000 - $1,500) / $1,500 = 2,567%
```

---

## Section 8: Common Failure Modes

### Why AI SDR Deployments Fail

```
FAILURE MODE                          FIX
------------------------------------------------------------------
Bad data in, bad outreach out         Fix enrichment waterfall first.
                                      80%+ match rate before launching.

Generic messaging at scale            Invest in signal-based
                                      personalization. "Spray and pray"
                                      with AI is still spray and pray.

No human handoff process              Define handoff triggers before
                                      launch. Build Slack/CRM routing
                                      on day 1.

Burning domains                       Follow warmup protocol. Never
                                      exceed 50 emails/day/mailbox.
                                      Monitor bounce and complaint rates.

Over-automating the close             AI generates pipeline. Humans
                                      close deals. Do not let AI handle
                                      pricing negotiations or contracts.

Ignoring reply sentiment              Negative replies left in sequence
                                      destroy reputation. Classify
                                      every reply, remove negatives
                                      immediately.

No feedback loop                      If you are not adjusting ICP
                                      scores and message variants
                                      monthly, your AI SDR decays.

Tool obsession over architecture      Switching from 11x to Artisan
                                      will not fix bad instruction
                                      stacks or missing context.
```

---

## Quick Reference

### 30-Second AI SDR Checklist

```
[ ] ICP defined with scoring criteria
[ ] Enrichment waterfall configured (80%+ match rate)
[ ] 3 email variants per persona written
[ ] Signal-to-action routing mapped
[ ] Sending infrastructure set up (5-10 domains, warmed)
[ ] Qualification criteria defined
[ ] Human handoff triggers configured
[ ] CRM integration active
[ ] Reply sentiment classification running
[ ] Weekly optimization cadence scheduled
```

### Speed-to-Lead Targets

```
Signal detected to first email:       < 5 minutes (P0 signals)
Signal detected to first email:       < 24 hours (P1 signals)
Positive reply to human handoff:      < 5 minutes
Meeting booked to confirmation:       < 1 hour
Lead qualified to AE assignment:      < 2 hours
```

### Email Deliverability Checklist

```
[ ] SPF record configured per domain
[ ] DKIM signing enabled per domain
[ ] DMARC policy set (start with p=none, move to p=quarantine)
[ ] One-click unsubscribe header present
[ ] Bounce rate below 2%
[ ] Spam complaint rate below 0.3%
[ ] Warmup completed (minimum 14 days, ideally 28)
[ ] Daily volume under 50/mailbox
[ ] Inbox placement tested (GlockApps, mail-tester)
```

---

## Questions to Ask

When advising on AI SDR deployment, always ask:

1. "What does your current pipeline generation process look like? Where does it break?"
2. "How many qualified meetings per month do you need to hit revenue targets?"
3. "Do you have a defined ICP, or are you still experimenting with market segments?"
4. "What CRM and sales tools are you using today?"
5. "What is your monthly budget for sales development tools?"
6. "Do you have clean, enriched prospect data, or are you starting from scratch?"
7. "How fast do you need to see results? Weeks or months?"
8. "What signals indicate a prospect is a good fit for you?"
9. "Who handles replies today? Do you have humans ready for the handoff?"
10. "Have you tried outbound before? What worked and what failed?"

---

## Related Skills

- **ai-cold-outreach** - Deep dive on cold email copywriting, deliverability, and multi-channel sequencing
- **lead-enrichment** - Detailed enrichment waterfall design, data provider selection, and Clay workflows
- **sales-motion-design** - End-to-end sales motion architecture from first touch to close
- **gtm-engineering** - Technical GTM infrastructure, API integrations, and workflow automation
- **solo-founder-gtm** - Lean AI SDR deployment for founders doing everything themselves
- **gtm-metrics** - Pipeline metrics, attribution modeling, and ROI tracking frameworks
