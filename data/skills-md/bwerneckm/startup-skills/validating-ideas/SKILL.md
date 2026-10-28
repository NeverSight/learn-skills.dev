---
name: validating-ideas
description: >
  Validates startup ideas through a sequenced workflow of Lean Canvas, Riskiest Assumption Testing,
  Mom Test interviews, and Pretotyping. Use when exploring a new product idea, pivoting an existing
  product, testing a B2B or B2C hypothesis, or when someone says "should we build X?"
---

# Skill: Idea Validation

## When to Use

Invoke this skill when:
- A new product idea or feature bet needs structured validation
- The team is considering a pivot or major direction change
- Someone asks "should we build X?" and the answer requires evidence, not opinion
- The company is evaluating a B2B infrastructure/platform play OR a B2C consumer product
- A strategic bet from the DIBB framework (see: shaping-product-strategy skill) needs ground-truth testing

## Context Detection: B2B vs B2C

Before starting Phase 1, determine the idea's context by checking these signals:

**B2B signals** (API/platform infrastructure for business customers):
- The customer is a company (enterprise, SMB, agency, platform)
- Revenue comes from API usage, platform fees, or transaction volume
- Integration, compliance, and developer experience are central concerns
- Interview targets: CTOs, VP Engineering, Product Heads, Compliance Officers at target companies

**B2C signals** (consumer-facing product):
- The end user is an individual consumer or retail customer
- Revenue comes from consumer subscriptions, spreads, or direct transaction fees
- UX simplicity, trust, and onboarding friction are central concerns
- Interview targets: End users matching your ideal customer profile in [PRIMARY_MARKET]

Label the idea as **B2B**, **B2C**, or **BOTH** and carry this label through all phases. Templates below include variant sections for each.

## Optional Pre-Filter: Kevin Hale (YC) Startup Ideas Framework

Before entering the main workflow, optionally run this 10-minute diagnostic to assess whether the idea is worth validating at all.

Score the idea on these five dimensions (1-5 each):

| Dimension | Question | Score |
|-----------|----------|-------|
| Problem frequency | How often does the target user face this problem? | [1-5] |
| Problem intensity | How painful is this problem when it occurs? | [1-5] |
| Willingness to pay | Would they pay to solve it today? | [1-5] |
| Founder-market fit | Does the founding team have unfair insight or access? | [1-5] |
| Market timing | Why now? What changed that makes this solvable today? | [1-5] |

**Threshold:** Total >= 18 to proceed. Below 15: challenge whether to validate at all. 15-17: proceed with caution, flag weak dimensions.

---

## Phase 1: Lean Canvas (~1 hour)

**Goal:** Articulate the full hypothesis on one page so the team has a shared starting point.

**Instructions:** Fill in all 9 blocks. Be specific to your company's domain and market context. Write falsifiable statements, not aspirations.

### Lean Canvas Template

```
LEAN CANVAS: [IDEA NAME]
Date: [DATE]
Author: [NAME]
Context: [B2B / B2C / BOTH]

1. PROBLEM (Top 3)
   P1: [Specific problem statement -- who has it, how often, how painful]
   P2: [Second problem]
   P3: [Third problem]
   Existing alternatives: [How do they solve it today? Name competitors or workarounds]

2. CUSTOMER SEGMENTS
   Early adopter: [Specific profile -- e.g., "Mid-size companies with 50-500 employees
                    wanting to add [CAPABILITY] without building it in-house"]
   Broader market: [Who comes after early adopters]

3. UNIQUE VALUE PROPOSITION
   Single sentence: [Clear, jargon-free statement of why this is different]
   High-level concept: [X for Y analogy -- e.g., "Stripe for [YOUR_DOMAIN]"]

4. SOLUTION (Map to each problem)
   S1 -> P1: [How your product solves problem 1]
   S2 -> P2: [How your product solves problem 2]
   S3 -> P3: [How your product solves problem 3]

5. CHANNELS
   Awareness: [How do prospects learn about this? -- e.g., industry conferences,
               developer communities, LinkedIn, local community groups]
   Evaluation: [How do they evaluate? -- e.g., sandbox, documentation,
                case studies]
   Conversion: [What triggers signup? -- e.g., demo call, self-serve API key]

6. REVENUE STREAMS
   Model: [Transaction fee / platform fee / subscription / hybrid]
   Pricing: [Specific numbers -- e.g., "0.2% per transaction + $2K/month platform fee"]
   Target unit economics: [Average ARR per client: $__K]

7. COST STRUCTURE
   Fixed: [Team, infrastructure, compliance costs]
   Variable: [Provider fees per transaction, cloud costs, support costs]
   Gross margin target: [__%]

8. KEY METRICS
   North star: [Single metric that captures value delivery]
   Leading indicators: [3-4 metrics that predict the north star]
   Lagging indicators: [Revenue, churn, NPS]

9. UNFAIR ADVANTAGE
   [What cannot be easily copied or bought? -- e.g., [FOUNDER]'s industry network,
    proprietary aggregation layer, regulatory positioning, team's deep
    domain experience]
```

**Output:** Save the completed canvas. Identify the 3-5 blocks where you are least confident -- these feed directly into Phase 2.

---

## Phase 2: Riskiest Assumption Test (~30 minutes)

**Goal:** Identify the single assumption that, if wrong, kills the entire idea. Focus validation effort there.

### Step 2.1: Extract Assumptions

Review the Lean Canvas and extract every implicit assumption. Categorize each one:

| # | Assumption | Category | Confidence | Evidence |
|---|-----------|----------|------------|----------|
| A1 | [Statement phrased as testable belief] | Desirability / Viability / Feasibility | Low / Med / High | [What you know today] |
| A2 | ... | ... | ... | ... |
| A3 | ... | ... | ... | ... |

**Categories defined:**
- **Desirability:** Do customers want this? Will they use it?
- **Viability:** Can we make money? Does the business model work?
- **Feasibility:** Can we build it? Do we have the tech, team, and regulatory path?

### Step 2.2: Rank by Risk

Plot assumptions on a 2x2 matrix:

```
                    HIGH importance (kills the idea if wrong)
                         |
                         |
          VALIDATE       |       VALIDATE
          SECOND         |       FIRST
          (important     |       (important AND
           but we have   |        we don't know)
           some signal)  |
HIGH  -------------------|-------------------  LOW
confidence               |               confidence
          MONITOR        |       INVESTIGATE
          (important     |       (uncertain but
           and we know)  |        not fatal)
                         |
                    LOW importance
```

### Step 2.3: Design the RAT Experiment

For the #1 riskiest assumption, design a test:

```
RAT EXPERIMENT DESIGN

Riskiest Assumption: [Statement]
Category: [Desirability / Viability / Feasibility]

Hypothesis: "We believe that [target user] will [expected behavior]
             because [reasoning]."

Test Method: [Interview / Landing page / Fake door / Concierge / Prototype]
Sample Size: [N -- minimum viable for signal, typically 5-12 for interviews,
              100-500 for landing pages]
Timeline: [X days/weeks]
Budget: [$X or $0 if pure interviews]

Pass Criteria: [Specific threshold -- e.g., "6 of 10 interviewees describe this
                problem unprompted" or "3%+ landing page conversion"]
Fail Criteria: [What result means KILL or PIVOT -- e.g., "fewer than 3 of 10
                mention the problem" or "<1% conversion"]

Owner: [Team member]
Start Date: [DATE]
Review Date: [DATE]
```

**Output:** One clearly defined experiment. Do NOT test multiple assumptions simultaneously.

---

## Phase 3: Mom Test Interviews (~1-2 weeks)

**Goal:** Talk to real potential users/buyers without leading them. Extract truth about their problems, current behavior, and willingness to act.

### Mom Test Core Rules

1. Talk about THEIR life, not YOUR idea
2. Ask about the PAST, not the FUTURE ("Tell me about the last time..." not "Would you use...")
3. Ask about SPECIFICS, not GENERICS ("How much did that cost you?" not "Is cost a problem?")
4. Listen for emotion, workarounds, and money already spent
5. Never pitch. Never explain. Never seek validation.

### Interview Guide: B2B Variant

Use when the idea targets businesses integrating your platform or API.

**Target interviewees:** CTO, VP Engineering, Head of Product, Compliance/Operations leads at companies matching your ideal customer profile.

| # | Question | What You're Learning |
|---|----------|---------------------|
| 1 | "Walk me through how you decided to add [CAPABILITY] to your product." | Purchase process, triggers, timeline |
| 2 | "What providers did you evaluate? What did that process look like?" | Competitive landscape from buyer's POV |
| 3 | "What was the hardest part of that integration?" | Pain points, feasibility concerns |
| 4 | "How long did it take from decision to live in production?" | Time-to-market pain (speed as value prop) |
| 5 | "If you could wave a magic wand and fix one thing about your current provider, what would it be?" | Unmet need, switching triggers |
| 6 | "How many different providers do you use for [DOMAIN] today?" | Multi-provider pain (aggregation thesis) |
| 7 | "Tell me about a time a compliance or regulatory issue blocked a product launch." | Regulatory friction as buying trigger |
| 8 | "What's your budget for [DOMAIN] infrastructure annually?" | Willingness to pay, budget validation |
| 9 | "If this problem disappeared tomorrow, what would you build next?" | Aspirational use case, expansion potential |
| 10 | "Who else in your org would need to approve a provider switch?" | Decision-making unit, sales cycle complexity |

### Interview Guide: B2C Variant

Use when the idea targets individual consumers or end users.

**Target interviewees:** End users matching your ideal customer profile in [PRIMARY_MARKET].

| # | Question | What You're Learning |
|---|----------|---------------------|
| 1 | "Tell me about the last time you [DID RELEVANT ACTIVITY]. Walk me through the process." | Current behavior, tools used, friction points |
| 2 | "What apps or platforms do you use for [ACTIVITY] today?" | Competitive landscape from user's POV |
| 3 | "What's the most frustrating thing about [ACTIVITY] right now?" | Core pain, emotional intensity |
| 4 | "Have you ever wanted to [DO SOMETHING] but couldn't figure out how?" | Access gaps, unmet needs |
| 5 | "Tell me about a time you had a bad experience with [EXISTING SOLUTION]." | Trust barriers, UX pain |
| 6 | "How do you decide what [PRODUCT/SERVICE] to use? Who or what influences you?" | Discovery channels, trust signals |
| 7 | "What would make you switch from [current solution] to something new?" | Switching cost and triggers |
| 8 | "How much do you spend on [ACTIVITY] per month, roughly?" | Wallet size, unit economics viability |
| 9 | "Have you ever tried [ADJACENT SOLUTION]? What was that like?" | Adjacent product perception, education needs |
| 10 | "If a product could give you [KEY BENEFITS] in one place, what questions would you have?" | Objections, trust barriers, feature priority |

### Interview Analysis Template

After completing 8-12 interviews, synthesize:

```
MOM TEST SYNTHESIS

Interviews completed: [N]
Date range: [START] to [END]
Interviewee profile: [Summary of who you talked to]

PATTERN 1: [Theme]
- Frequency: [X of N interviewees mentioned this]
- Representative quote: "[Direct quote]"
- Implication for hypothesis: [Supports / Challenges / Neutral]

PATTERN 2: [Theme]
- Frequency: [X of N]
- Representative quote: "[Direct quote]"
- Implication: [Supports / Challenges / Neutral]

PATTERN 3: [Theme]
- Frequency: [X of N]
- Representative quote: "[Direct quote]"
- Implication: [Supports / Challenges / Neutral]

SURPRISES (things you did NOT expect):
- [Finding 1]
- [Finding 2]

RISKIEST ASSUMPTION UPDATE:
- Original assumption: [From Phase 2]
- Interview evidence: [Supported / Challenged / Inconclusive]
- Confidence shift: [Low->Med / Med->High / etc.]
- Recommended action: [Proceed to Phase 4 / Pivot assumption / Re-interview]
```

---

## Phase 4: Pretotype / Fake Door Test (~1-2 weeks)

**Goal:** Measure actual behavior, not stated intent. People lie in interviews (not maliciously); behavior reveals truth.

### Step 4.1: Select Test Type

Choose based on what you are validating:

| Test Type | Best For | Cost | Timeline | Signal |
|-----------|----------|------|----------|--------|
| Landing page + waitlist | Desirability, messaging | $200-500 ads | 5-7 days | Signup rate |
| Fake door (button in existing product) | Feature demand | $0 | 3-5 days | Click rate |
| Concierge (manual delivery) | Solution quality | $0 (time only) | 1-2 weeks | Retention, WTP |
| Explainer video + CTA | Complex product understanding | $500-1K | 7-10 days | Watch rate, CTA clicks |
| Wizard of Oz (fake automation) | Feasibility perception | $0 (time only) | 1-2 weeks | Completion rate |

### Step 4.2: Design the Test

```
PRETOTYPE SPEC

Test type: [From table above]
What we're measuring: [Desirability / Viability / Feasibility]
Hypothesis: "If we show [target audience] a [test artifact], at least [X%]
             will [desired action]."

TARGET AUDIENCE
- Profile: [Specific description]
- Source: [How you'll reach them -- ads, email list, community, direct outreach]
- Sample size target: [Minimum 100 for landing pages, 200+ for statistical
                       significance on conversion]

TEST ARTIFACT
- Landing page headline: "[Compelling headline that states the value prop]"
- Subheadline: "[One sentence elaborating the benefit]"
- CTA: "[Button text -- e.g., 'Get Early Access', 'Request API Key']"
- Social proof element: [If available -- logos, quotes, numbers]

TRAFFIC PLAN
- Channel: [LinkedIn ads / Google ads / direct email / community post]
- Budget: $[AMOUNT]
- Duration: [X days]
- Target impressions: [N]

SUCCESS CRITERIA
- Primary metric: [e.g., landing page -> CTA conversion rate]
- Pass: [>= X% -- benchmark: 3-5% for cold traffic, 10-15% for warm]
- Inconclusive: [X-Y% -- need more data or different audience]
- Fail: [< X% -- strong signal to pivot or kill]

ANTI-GAMING MEASURES
- [How you prevent false positives -- e.g., require email, not just clicks]
- [How you ensure traffic quality -- e.g., geographic targeting, interest filters]
```

**Output:** A fully specified test that can be launched within 48 hours.

---

## Phase 5: GO / PIVOT / KILL Decision (~1 session)

**Goal:** Make an evidence-based decision. No gut feelings. Score every dimension and let the data speak.

### GO/PIVOT/KILL Scorecard

Score each dimension 1-5 based on evidence gathered in Phases 1-4.

| # | Dimension | Score (1-5) | Evidence Summary | Key Data Point |
|---|-----------|-------------|-----------------|----------------|
| 1 | **Problem-Solution Fit** -- Do real people have this problem and does our solution address it? | [SCORE] | [2-3 sentences from Mom Test + Pretotype data] | [Single strongest data point] |
| 2 | **Willingness to Pay** -- Have prospects indicated they would pay, or shown purchasing behavior? | [SCORE] | [Evidence of budget, current spend, stated WTP] | [Specific $$ or conversion %] |
| 3 | **Market Size** -- Is the addressable market large enough for the company's financial targets ($[X]M ARR Y1)? | [SCORE] | [TAM/SAM estimate with sources] | [SAM number] |
| 4 | **Competitive Advantage** -- Can we win against alternatives (including "do nothing" and "build in-house")? | [SCORE] | [Key differentiators validated in interviews] | [Most cited advantage] |
| 5 | **Feasibility** -- Can we build this with the current team and resources within 3-6 months? | [SCORE] | [Technical assessment, provider readiness, regulatory path] | [Estimated time to MVP] |
| 6 | **Strategic Fit** -- Does this align with the company's vision and long-term strategy? | [SCORE] | [Alignment with strategic plan, product roadmap, team strengths] | [Which OKR does this serve?] |

### Scoring Guide

- **5**: Strong evidence supporting (multiple data points, quantitative signal)
- **4**: Moderate evidence supporting (qualitative signal, some data)
- **3**: Mixed or insufficient evidence (need more data, conflicting signals)
- **2**: Moderate evidence against (warning signs, weak demand signals)
- **1**: Strong evidence against (clear rejection, no market, blocked path)

### Decision Rules

| Total Score | Decision | Action |
|-------------|----------|--------|
| **25-30** | **GO** | Proceed to business model design. Hand off to designing-business-models skill. |
| **19-24** | **CONDITIONAL GO** | Proceed, but address dimensions scored <= 2 before investing heavily. Set kill criteria for 90 days. |
| **13-18** | **PIVOT** | The core insight has value but the current form does not work. Identify which dimension(s) to change and re-enter at Phase 1 with adjusted hypothesis. |
| **7-12** | **KILL** | Insufficient evidence across too many dimensions. Archive learnings and move on. |
| **6** | **KILL** | Nothing validated. Archive and move on immediately. |

### Decision Record

```
DECISION: [GO / CONDITIONAL GO / PIVOT / KILL]

Idea: [Name]
Date: [DATE]
Total Score: [X/30]
Decided by: [Names]

Score Breakdown:
  Problem-Solution Fit:  [X] -- [One-line justification]
  Willingness to Pay:    [X] -- [One-line justification]
  Market Size:           [X] -- [One-line justification]
  Competitive Advantage: [X] -- [One-line justification]
  Feasibility:           [X] -- [One-line justification]
  Strategic Fit:         [X] -- [One-line justification]

If GO: Next step is designing-business-models skill.
If CONDITIONAL GO: Must resolve [DIMENSION] within [TIMEFRAME].
  Kill criteria: [What result in 90 days triggers a KILL]
If PIVOT: New hypothesis is [RESTATED HYPOTHESIS]. Re-enter Phase 1.
If KILL: Key learning to archive: [INSIGHT].

Save this record to your decision log.
```

---

## Cross-References

| Decision | Next Skill |
|----------|-----------|
| GO or CONDITIONAL GO | **designing-business-models** -- Build the Business Model Canvas, pricing architecture, and unit economics |
| Need strategic framing before validation | **shaping-product-strategy** -- Use DIBB framework to structure the bet before entering this workflow |
| Market-specific validation needed | **planning-market-entry** -- Assess regulatory readiness and market attractiveness for a specific geography |

---

## Optional Post-Launch Add-On: Sean Ellis PMF Survey

Not part of core validation. Use only AFTER the product is live with real users (minimum 40 responses needed for signal).

**The question:** "How would you feel if you could no longer use [PRODUCT]?"

| Response | Threshold | Interpretation |
|----------|-----------|---------------|
| "Very disappointed" | >= 40% | Strong PMF signal |
| "Somewhat disappointed" | -- | Moderate engagement, not PMF |
| "Not disappointed" | >= 40% | No PMF -- revisit value prop |

If below 40% "very disappointed": Segment responses by user type. PMF may exist in a subsegment. Narrow focus to that segment before expanding.

---

## Checklist: Full Workflow at a Glance

- [ ] Detect B2B vs B2C context
- [ ] (Optional) Run Kevin Hale pre-filter -- score >= 18 to proceed
- [ ] **Phase 1:** Complete Lean Canvas (all 9 blocks, specific to your domain)
- [ ] **Phase 2:** Extract assumptions, rank on 2x2, design RAT experiment
- [ ] **Phase 3:** Conduct 8-12 Mom Test interviews using the correct variant guide
- [ ] **Phase 3:** Synthesize interview findings, update riskiest assumption
- [ ] **Phase 4:** Design and launch pretotype/fake door test
- [ ] **Phase 4:** Collect data, compare against pass/fail criteria
- [ ] **Phase 5:** Score all 6 dimensions on the GO/PIVOT/KILL scorecard
- [ ] **Phase 5:** Record decision in your decision log
- [ ] If GO: Hand off to designing-business-models skill
