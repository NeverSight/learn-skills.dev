---
name: solution-interview
description: "Test if your solution actually solves the validated problem before building the full product. Master the art of showing concepts and prototypes to get honest feedback on solution fit. Use when: **After problem interviews** to test if your solution addresses validated problems; **Before building MVP** to validate core value proposition; **Prototype testing** to get feedback on concepts and mockups; **Feature validation** to test if new features solve real problems; **Pivoting** to test alterna..."
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Solution Interview

> Test if your solution actually solves the validated problem before building the full product. Master the art of showing concepts and prototypes to get honest feedback on solution fit.

## When to Use This Skill

- **After problem interviews** to test if your solution addresses validated problems
- **Before building MVP** to validate core value proposition
- **Prototype testing** to get feedback on concepts and mockups
- **Feature validation** to test if new features solve real problems
- **Pivoting** to test alternative solutions to the same problem
- **Pricing discovery** to understand willingness to pay

## Methodology Foundation

| Aspect | Details |
|--------|---------|
| **Source** | Cindy Alvarez - "Lean Customer Development" (2014), Steve Blank - Customer Development |
| **Core Principle** | "Show, don't tell. Let customers react to something tangible. Their reactions—not their words—reveal the truth." |
| **Why This Matters** | People can't accurately predict their behavior. By showing a prototype and observing reactions, you get real signal about whether your solution works. |


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Structures solution demos** - How to present concepts effectively
2. **Captures honest reactions** - Gets real feedback, not politeness
3. **Identifies gaps and issues** - What's missing or wrong
4. **Tests willingness to pay** - Early pricing validation
5. **Measures solution fit** - Does this actually solve the problem?
6. **Generates product insights** - What to build, what to skip

## How to Use

### Prepare Solution Interview Script
```
I've validated this problem: [problem]
My proposed solution: [solution concept]
Create a solution interview script to test fit.
Include how to demo and what reactions to look for.
```

### Analyze Solution Interview Results
```
I showed my prototype to [X] people. Here's the feedback: [summary]
Analyze solution fit. Should I proceed to MVP?
```

### Create a Solution Interview Prototype
```
Help me create the minimum viable demo for solution interviews:
Problem: [validated problem]
Solution concept: [idea]
What should I show? What level of fidelity is needed?
```

## Instructions

### Step 1: Confirm Problem Validation First

```
## Pre-Requisite Check

### Do NOT start solution interviews until:
- [ ] Completed 10+ problem interviews
- [ ] Problem validation scorecard passes:
  - [ ] >70% mentioned problem unprompted
  - [ ] Average severity >7/10
  - [ ] >30% actively seeking solutions
- [ ] Clear problem statement documented
- [ ] Target persona defined

### Why This Matters
If you test solutions without validated problems, you'll get:
- False positives ("sure, that looks nice")
- No ability to connect solution to real pain
- Wasted time building the wrong thing

### Problem Summary for This Interview
**Validated Problem:** ________________________________
**Severity Score:** __/10
**Who Has It:** [Persona description]
**What They Do Today:** [Current solution]
```

---

### Step 2: Create Your Solution Demo

```
## What to Demo

### Fidelity Levels

| Level | What It Is | When to Use | Time to Create |
|-------|------------|-------------|----------------|
| **Concept** | Verbal description + whiteboard | Very early, exploring directions | 30 min |
| **Paper** | Sketches, wireframes | Early concept validation | 2-4 hours |
| **Clickable** | Figma/InVision prototype | Testing workflows and features | 1-2 days |
| **Wizard of Oz** | Human behind the curtain | Testing value prop before building | 1-3 days |
| **Concierge** | You do it manually for them | Testing if solution works at all | 1+ week |
| **MVP** | Basic working product | Testing if they'll pay | 2+ weeks |

### What to Show

**DO Show:**
- Core value proposition in action
- The main workflow/interaction
- How it solves their specific problem
- Just enough to get a reaction

**DON'T Show:**
- Every feature you plan to build
- Polished design (distracts from function)
- Pricing (usually—test separately)
- Your roadmap (creates false expectations)

### Demo Script Template

"Before I show you anything, let me make sure I understand your problem.
[Recap validated problem in their words]
Does that sound right? [Confirm]

What I want to show you is rough—it's not a real product yet.
I'm interested in your honest reaction, even if it's negative.
The worst thing you could do is be polite.

[Demo the core concept - 2-3 minutes max]

Now I want to understand your reaction..."
```

---

### Step 3: Run the Solution Interview

```
## Solution Interview Structure (30-45 minutes)

### Part 1: Problem Recap (5 min)
"Last time we talked about [problem]. Since then, has anything changed?"
"What have you tried to solve this?"
Goal: Re-anchor to the problem, confirm it's still relevant

### Part 2: Solution Demo (5-10 min)
"I want to show you something we're exploring..."
[Demo core concept]
"What's your initial reaction?"
Goal: Present solution, capture immediate reaction

### Part 3: Feedback Deep Dive (15-20 min)
"What stood out to you?"
"What concerns you?"
"What's missing?"
"How would this fit into your current workflow?"
Goal: Understand fit, gaps, objections

### Part 4: Comparison to Current (5 min)
"How does this compare to what you do today?"
"Would this replace [current solution] or add to it?"
"What would have to be true for you to switch?"
Goal: Understand switching behavior

### Part 5: Commitment Testing (5 min)
"If this existed today, what would you do?"
"Would you be willing to try an early version?"
"What would it be worth to you if it worked?"
Goal: Test real interest with commitment asks

### Part 6: Next Steps (2 min)
"Can I follow up when we have something more complete?"
"Who else should I show this to?"
Goal: Get permission for follow-up, referrals
```

---

### Step 4: Key Questions by Interview Phase

```
## Solution Interview Questions

### Reaction Questions (Initial)
- "What's your first reaction?"
- "What stood out to you?"
- "What surprised you?"
- "What concerned you?"

**Watch for:**
- Immediate positive vs. confused
- Questions they ask (what do they care about?)
- Body language (leaning in vs. back)

### Understanding Questions (Comprehension)
- "In your own words, what does this do?"
- "How would you explain this to a colleague?"
- "What problem does this solve?"

**Red flags:**
- They can't explain it = too complex
- They describe it differently than intended = messaging problem
- They describe features, not benefits = not connecting to their problem

### Fit Questions (Solution-Problem Fit)
- "Does this solve the problem we discussed?"
- "What would be different about your day/week if you had this?"
- "Where does this fit in your current workflow?"
- "What would you stop doing if you had this?"

**Strong signals:**
- They can immediately see where it fits
- They describe specific situations it would help
- They identify things they'd stop doing (replacing current behavior)

### Gap Questions (What's Missing)
- "What's missing?"
- "What would prevent you from using this?"
- "What would make this a no-brainer?"
- "What's the most important thing we should build first?"

**Listen for:**
- Must-have features vs. nice-to-haves
- Deal-breaker gaps
- Unexpected use cases

### Concern Questions (Objections)
- "What worries you about this?"
- "What could go wrong?"
- "What would your [boss/team/IT] think?"

**Listen for:**
- Technical concerns (security, integrations)
- Organizational concerns (adoption, approval)
- Personal concerns (learning curve, change)

### Comparison Questions (vs. Alternatives)
- "How does this compare to what you do today?"
- "How does this compare to [competitor]?"
- "What would make you switch from your current solution?"

### Commitment Questions (Action)
- "If this was available today, what would you do?"
- "Would you be willing to try an early version?"
- "Would you pay for this? How much would it be worth?"
- "Can I add you to our beta list?"
```

---

### Step 5: Evaluate Solution Fit

```
## Solution Interview Scorecard

### Per Interview Assessment

**Interview #___**
**Participant:** _______________

| Criteria | Rating (1-5) | Notes |
|----------|--------------|-------|
| Understood what it does | | |
| Connected to their problem | | |
| Saw clear value | | |
| Would use/try it | | |
| Would pay (some amount) | | |
| Referred others | | |

**Reaction Type:**
- [ ] Excited ("When can I have this?")
- [ ] Interested (asking good questions)
- [ ] Neutral (polite but not engaged)
- [ ] Confused (didn't understand)
- [ ] Negative (specific concerns)

**Key Verbatim:**
"[Quote showing reaction]"

### Aggregate Analysis (After 10+ Interviews)

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Understood the solution | >90% | | |
| Said it solves their problem | >70% | | |
| Would try/use it | >60% | | |
| Would pay something | >40% | | |
| Made commitment (beta signup, referral) | >30% | | |

### Decision Framework

**VALIDATED - Proceed to MVP if:**
- [ ] 7+ of 10 said it solves their problem
- [ ] 6+ would try an early version
- [ ] 4+ expressed willingness to pay
- [ ] 3+ made real commitment (beta signup, referral, LOI)
- [ ] No critical gaps identified
- [ ] Clear must-have features identified

**ITERATE - Before MVP if:**
- [ ] Solution fit is partial (some love it, some don't)
- [ ] Critical feature gap identified
- [ ] Significant objection pattern emerged
- [ ] Need to test alternative approaches

**NOT VALIDATED - Pivot if:**
- [ ] Fewer than 5 said it solves their problem
- [ ] Widespread confusion about value
- [ ] No one willing to try it
- [ ] Unanimous critical concern
```

---

## Examples

### Example 1: SaaS Solution Interview

**Input:**
> "I validated that marketing managers struggle with cross-channel attribution (8/10 severity). I want to test a dashboard solution. Create the solution interview script."

**Output:**

## Solution Interview: Marketing Attribution Dashboard

### Pre-Interview Prep
**Validated Problem:** Marketing managers can't track campaign ROI across channels
**Severity:** 8/10
**Current Solution:** Manual spreadsheets, multiple tool logins, guessing

### Demo Prep
**What to show:** Figma prototype of dashboard with:
- Single-screen showing all channels
- Attribution by touchpoint
- Campaign ROI at a glance

**Demo duration:** 3 minutes max

---

### Interview Script

**Part 1: Problem Recap (5 min)**
"When we talked last month, you mentioned spending 6 hours a week pulling marketing data together, and that your CFO often asks questions you can't answer immediately. Is that still the case?"

[Wait for confirmation and updates]

"What's changed since then? Have you tried anything new?"

---

**Part 2: Solution Demo (5 min)**

"I want to show you something we're working on. It's rough—not a real product yet—and I want your honest reaction.

[Share screen - show prototype]

Imagine this is your marketing dashboard. You log in and see all your channels—Google, LinkedIn, Facebook, email—in one place.

[Point to attribution view]

Here you can see which touchpoints led to conversions. Not just last-click, but the full journey.

[Point to ROI]

And here's campaign ROI calculated automatically—you could show this to your CFO.

What's your initial reaction?"

---

**Part 3: Feedback Deep Dive (15 min)**

**Reaction:**
- "What stands out to you?"
- "What concerns you?"

**Comprehension:**
- "In your own words, what would this do for you?"

**Fit:**
- "Does this solve the problem we discussed?"
- "Walk me through how you'd use this on a Monday morning..."
- "What would you stop doing if you had this?"

**Gaps:**
- "What's missing?"
- "What would be a deal-breaker?"
- "What's the most important thing we should build first?"

**Objections:**
- "What worries you about this approach?"
- "What would IT say about adding another tool?"
- "What would prevent your team from using this?"

---

**Part 4: Comparison (5 min)**

- "How does this compare to the spreadsheets you use today?"
- "Have you looked at other attribution tools? How would this compare?"
- "What would make you switch from your current approach?"

---

**Part 5: Commitment (5 min)**

- "If this existed today, what would you do?"
- "Would you be willing to try an early version—even if it's rough?"
- "What would you pay for this if it worked? Just a rough range."
- "Can I add you to our early access list?"
- "Who else on your team should I talk to?"

---

### What I'm Listening For

**Strong signals:**
- "Can I have this?" / "When is it ready?"
- Specific questions about how it works
- Already thinking about how they'd use it
- Naming specific situations it would help
- Willingness to pay without prompting

**Weak signals:**
- "That's cool" (polite)
- Generic praise with no specifics
- "Let me know when it's done" (passive)
- Can't articulate how they'd use it

**Red flags:**
- Confusion about what it does
- "We already have something like this"
- "I'm not sure our team would use it"
- Significant feature gaps I can't address

---

### Example 2: Analyzing Solution Interview Results

**Input:**
> "I showed my meal prep app prototype to 10 working parents. Here's the summary. Should I build the MVP?"

**Summary:**
- 8/10 said they understood it
- 6/10 said it would help
- 4/10 said they'd try it
- 2/10 said they'd pay for it
- Main feedback: "Looks nice but I'm not sure I'd actually use it"

**Output:**

## Solution Interview Analysis

### Scorecard

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Understood solution | >90% | 80% | ⚠️ |
| Said it solves problem | >70% | 60% | ❌ |
| Would try it | >60% | 40% | ❌ |
| Would pay | >40% | 20% | ❌ |

### Diagnosis: **NOT VALIDATED**

You're below threshold on every metric. This is a significant warning sign.

### Key Insight
"Looks nice but I'm not sure I'd actually use it" is a critical signal. This usually means:
1. The solution doesn't feel connected to their real problem
2. The problem wasn't severe enough to begin with
3. There's a gap between what they say they want and what they'd actually do

### Analysis Questions

**1. Was the problem actually validated?**
- Go back to problem interviews
- Was severity really 7+? Or were people just being polite?
- Were they actively seeking solutions? Or just acknowledging a problem exists?

**2. Is there a segment mismatch?**
- Who were the 2 who said they'd pay? Are they different?
- Maybe "working parents" is too broad
- Might need: "working parents who already pay for meal services"

**3. Is the solution wrong, not the problem?**
- What did they say was missing?
- What would make it a "no-brainer"?
- Maybe they don't want an app—maybe they want done-for-you meals

### Recommended Next Steps

**Option 1: Diagnose the Gap**
Go back to the 6 who said "it would help" but wouldn't try it. Ask:
- "What's the gap between 'this would help' and actually using it?"
- "What would have to be true for you to actually try this?"
- "What else would need to exist?"

**Option 2: Find Your Champions**
The 2 who said they'd pay—they're your early adopters. Understand them:
- What's different about them?
- What problem do they have that others don't?
- Build for them specifically

**Option 3: Pivot the Solution**
If the problem is validated but solution isn't:
- What else could solve "I can't eat healthy because no time"?
- Maybe it's not meal planning—it's meal prep
- Maybe it's not an app—it's a service
- Test alternative solutions with new solution interviews

### Do NOT Build MVP Yet
You'll spend months building something 80% won't use. Get solution fit above 60% first.

---

### Example 3: Wizard of Oz Solution Test

**Input:**
> "I want to test if customers would pay for AI-generated social media posts before building the AI. How do I run a solution interview without a product?"

**Output:**

## Wizard of Oz Solution Interview

### Concept
"Wizard of Oz" testing means you provide the experience manually while the customer thinks it's automated. This lets you test value before building technology.

### Your Setup

**What the customer sees:**
- Upload a topic/brief
- Receive social media posts within 24 hours
- Appears to be AI-generated

**What actually happens:**
- You (or a freelancer) write the posts manually
- Deliver via email or simple dashboard
- Track reactions and usage

### Solution Interview Flow

**Part 1: Problem Confirm**
"You mentioned spending 4 hours/week writing social posts. Still the case?"

**Part 2: Explain the Concept**
"We're testing an AI that writes social posts for you. You give it your topic, and it generates a week's worth of posts. Here's an example of what it produces..."

[Show sample output you created manually]

"What's your initial reaction?"

**Part 3: Offer the Test**
"We're running a pilot. For the next 2 weeks, I'll generate your social posts. You give me your topics, and I'll send you posts within 24 hours.

There's no charge for the pilot. I just need you to:
1. Actually use the posts (or tell me why not)
2. Give me feedback on what's good/bad
3. Tell me at the end if you'd pay for this

Would you be willing to try it?"

**Part 4: Observe Real Behavior**
During pilot, track:
- Do they actually give you topics?
- Do they actually use the posts?
- What feedback do they give?
- How much editing do they do?

**Part 5: Willingness to Pay**
After pilot:
"Based on the last 2 weeks, would you pay for this?"
"How much would it need to cost for it to be a no-brainer?"
"What would make it more valuable?"

### What This Tests

| What You Learn | How You Learn It |
|----------------|------------------|
| Do they value the output? | Did they use the posts? |
| Is quality good enough? | How much did they edit? |
| Does it save time? | Did they mention time savings? |
| Would they pay? | Asked directly + observed behavior |
| What features matter? | What feedback did they give? |

### Success Criteria for Wizard of Oz

**Proceed to build AI if:**
- 7+ of 10 used all posts provided
- Minimal editing needed (<20% revised)
- Strong qualitative feedback
- 5+ would pay at viable price point
- No critical quality concerns

### Why This Works
- You prove value without writing code
- You get real usage data, not predictions
- You can iterate on the "algorithm" (your human process) cheaply
- Customers who use manual version will use automated version

---

## Checklists & Templates

### Solution Interview Prep Checklist

```
## Before the Interview

□ Problem validation confirmed
□ Solution demo/prototype ready
□ Demo script practiced (under 5 min)
□ Questions prepared
□ Note-taking system ready
□ Commitment asks defined

## What to Demo

□ Core value proposition only
□ Not over-polished (avoid distraction)
□ Relatable to their specific problem
□ Interactive if possible

## During the Interview

□ Recap problem first
□ Set expectation for honest feedback
□ Demo in under 5 minutes
□ Watch for immediate reaction
□ Probe on concerns and gaps
□ Test commitment (beta, pay, referral)
□ Get permission to follow up
```

---

### Solution Interview Notes Template

```
## Solution Interview #___

**Date:** _______________
**Participant:** _______________
**Problem Recap:** Still experiencing issue? Y/N

### Demo Reaction

**Initial reaction:** (excited/interested/neutral/confused/negative)

**First words after demo:**
"[Verbatim]"

**Questions they asked:**
1.
2.
3.

### Fit Assessment

| Question | Response | Signal Strength |
|----------|----------|-----------------|
| Solves problem? | | Strong/Med/Weak |
| Would use it? | | Strong/Med/Weak |
| Replaces current? | | Strong/Med/Weak |
| Would pay? | | Strong/Med/Weak |

### Gaps & Concerns

**Missing features:**
-

**Concerns:**
-

**Deal-breakers:**
-

### Commitment Outcome

□ Would try beta
□ Would pay (amount: $___)
□ Made referral
□ Gave follow-up permission
□ No commitment

### Key Insight
________________________________
```

---

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## References

- Alvarez, Cindy. "Lean Customer Development" (2014) - Solution interview methodology
- Blank, Steve. "The Four Steps to the Epiphany" (2005) - Customer Development
- Fitzpatrick, Rob. "The Mom Test" (2013) - Getting honest feedback
- Constable, Giff. "Talking to Humans" (2014) - Interview techniques
- Torres, Teresa. "Continuous Discovery Habits" (2021) - Ongoing validation

## Related Skills

- [problem-interview](../problem-interview/) - Must complete before solution interviews
- [mom-test](../mom-test/) - Getting honest feedback
- [lean-canvas](../lean-canvas/) - Documenting learnings
- [pricing-validation](../pricing-validation/) - Testing willingness to pay
- [customer-discovery](../customer-discovery/) - Overall framework

---

## Skill Metadata


- **Mode**: cyborg
```yaml
name: solution-interview
category: validation
subcategory: customer-research
version: 1.0
author: MKTG Skills
source_expert: Cindy Alvarez
source_work: Lean Customer Development
difficulty: intermediate
estimated_value: $2,000 product validation consulting
tags: [validation, interviews, solutions, prototypes, MVP, startups, YC]
created: 2026-01-25
updated: 2026-01-25
```
