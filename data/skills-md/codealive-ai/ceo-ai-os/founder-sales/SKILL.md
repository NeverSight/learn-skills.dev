---
name: founder-sales
description: Help founders close their first customers and build repeatable sales processes. Use when someone is doing founder-led sales, trying to get their first customers, running early sales calls, or asking when to hire their first salesperson. For pipeline tracking and scoring, see pipeline-manager. For writing cold outreach, see cold-email.
---
## [YOUR_PRODUCT] Context

Before helping, read `MEMORY.md` for: current wedge, ICP, competitors, PMF stage, system constraint.
Apply all frameworks to the user's specific company and stage (read from MEMORY.md).
Follow output preferences from USER.md (language, format, platform constraints).
For chat platforms: max 15 lines, no markdown tables, be concrete and actionable.


# Founder Sales

Help the user close early customers and codify a repeatable sales process using insights from 16 product leaders.

## How to Help

When the user asks for help with founder sales:

1. **Understand their stage** - Ask how many customers they have, whether they have a repeatable ICP, and whether they're pre-product or have something to demo
2. **Diagnose the bottleneck** - Determine if the problem is lead generation, qualification, discovery, closing, or implementation
3. **Guide the approach** - Help them craft outreach, prepare for discovery calls, or design their sales process based on their specific situation
4. **Document for repeatability** - Encourage them to capture what works so they can eventually hand it off

## Core Principles

### The founder IS the product in early sales
Jen Abel: "Founder led sales is really that first milestone... the founder is the product." In early stages, the founder's novel insight and subject matter expertise are the primary drivers of interest. Leverage your status as founder to gain market access. Use your ability to see "budding moments" in conversations to refine the product vision.

### Your biggest competitor is indecision, not other vendors
April Dunford: "40 to 60% of B2B purchase processes end in no decision... they couldn't figure out how to make a choice confidently." Focus on helping buyers make a choice confidently rather than just pitching features. Act as a guide to help them navigate the market. "No decision" is the safest path for overwhelmed buyers.

### You cannot outsource early sales
Pete Kazanjy: "The founder's got to do that stuff... it's going to be way easier for you to get minimally viable good at selling." Don't hire a VP of Sales until you've closed the first couple dozen customers yourself. Use early sales calls as customer development. Focus on becoming "minimally viable" at selling, not a master.

### Sell it before you build it
Todd Jackson: "I want to sell it before I build it, because I really want the signal from customers to be the guide and the oxygen that drives what I'm building." Use Figma mock-ups to secure the first 5-10 customers before writing extensive code. Determine the fidelity required for a demo based on the product type.

### Close the laptop and diagnose first
Geoffrey Moore: "Shut the laptop. Just don't open it... 'We understand there's this really serious problem and we believe your company might have it, is that true?'" Early sales to pragmatists should be diagnostic and focused entirely on the customer's pain. Use a physical pen and paper so customers can see you capturing their specific words.

### The "Collison Install" - don't leave until it's implemented
Dalton Caldwell: "They would just install Stripe into the customer's website... they basically would not go away until you finish the implementation." Don't consider a sale finished until the product is fully implemented. Offer to manually install or set up the software. Be persistent through the "last mile."

### Founder-led sales is about learning, not revenue
Jen Abel: "Founder led sales is not about revenue on day one. It is about learning as fast as humanly possible to get to that pulse." Treat early sales calls as research sessions. Be vulnerable about being early-stage to elicit more honest feedback. The goal is to find the repeatable pattern.

### Qualify ruthlessly - it's never a bottom-of-funnel problem
Jen Abel: "If you spend your time on the wrong leads, that equates to a zero. It's never a bottom of funnel problem. It's always qualification." Verify if the prospect is measuring or managing the problem today. Stop chasing leads that are "just being nice" but have no intent to buy.

### Manual outreach beats AI tools for high-value deals
Jen Abel: "AI tools are all pulling from the same databases. I want to email someone not in the database... I want to take a back door in." Manual, highly personalized outreach is more effective for enterprise deals than automated tools using saturated databases. Keep emails to 3-4 sentences max. Focus on shock value and relevance over generic personalization.

### Book the next meeting while you're still on this one
Jen Abel: "Get the second call booked on the first call. Pull up calendars. Look at calendars. Who else should be invited?" Maintain momentum by securing the next meeting while still on the current call. Identify other stakeholders who should be included.

### Stay in founder-led sales until you have repeatability
Jeanne Grosser: "Wait until you're around a million in ARR. When you have a repeatable process... there's some repeatability there." Don't hand over sales until you can define an ICP and have documented the discovery questions, objection handling, and demo flow that work.

### Design the process around how they buy, not how you sell
Bob Moesta: "Instead of trying to base the sales process on how we want to sell, we need to actually design the sales process on how they want to buy." Map the buyer's timeline through six phases: first thought, passive looking, active looking, deciding, first use, and ongoing use. Tailor your approach to their phase.

## Questions to Help Users

- "How many customers have you closed personally? What's your ICP?"
- "Where in the funnel are you losing deals - outreach, discovery, closing, or implementation?"
- "Are you talking to people who are actively trying to solve this problem, or just 'interested'?"
- "Can you describe the last deal you lost? What happened?"
- "What does your current outreach message say? What response rate are you getting?"
- "Have you documented what works so someone else could run this process?"

## Common Mistakes to Flag

- **Hiring sales too early** - Don't hire a salesperson to fix messaging that isn't landing. Founders must prove the motion works first, typically to ~$1M ARR
- **Defaulting to product demos** - Discovery should focus on the customer's pain, not your features. Keep the laptop closed in early meetings
- **Treating "yes" as the finish line** - A deal isn't closed until implementation is complete. Follow the Collison Install approach
- **Using generic AI outreach** - Automated tools pull from the same databases everyone else uses. Manual, personalized outreach wins for high-value deals
- **Chasing polite leads** - "That sounds interesting" is not buying intent. Qualify for active problem-solving, not politeness

## Signal-Based Outreach

Instead of cold-blasting lists, scan for buying signals and reach out with context. This workflow chains several skills together.

### What signals to look for

| Signal | Where to find | Why it matters |
|---|---|---|
| Hiring for roles that use your tool category | LinkedIn jobs, job boards | Budget allocated, problem recognized |
| Funding round | Crunchbase, TechCrunch, X | Money to spend, scaling pressure |
| Tech stack changes | GitHub, blog posts, job descriptions | Active evaluation window |
| Pain language in public posts | LinkedIn, X, Reddit, HN | Prospect self-identifies the problem |
| Conference attendance | Event attendee lists, speaker bios | Engaged in the problem space |
| Competitor mentions | Social, reviews, forums | Currently evaluating alternatives |

### The workflow

1. **Detect signal** — Use `exa-company-research` or `exa-people-research` to scan for signals. Search for hiring patterns, tech mentions, or pain language relevant to your wedge (see MEMORY.md).

2. **Qualify** — Run through `sales-qualification` ICP check: right company size (per ICP in MEMORY.md)? Right pain ([YOUR_CUSTOMER_PAIN])? Active problem-solving (not just "interested")?

3. **Research** — Use `exa-personal-site` or `exa-x-search` to find the prospect's recent posts, talks, or writing. Look for specific pain points to reference.

4. **Craft outreach** — Use `cold-email` to write a signal-based email. The signal IS the personalization — "I noticed you're hiring 3 [target role] and your job post mentions [specific pain language]" is 5x more effective than "I came across your profile."

5. **Log** — Record the outreach via `structured-log` for tracking.

### Key principles

- **One signal = one outreach.** Don't batch signals. Each email should reference one specific thing.
- **Speed matters.** A funding announcement is relevant for ~2 weeks. A job posting for ~1 month. Act fast.
- **Manual > automated for high-value targets.** Per Jen Abel: "I want to email someone not in the database."

## Deep Dive

For all 28 insights from 16 guests, see `references/guest-insights.md`

## Related Skills

- **pipeline-manager** — pipeline state, scoring, stage tracking (the orchestrator)
- **signal-scanner** — automated signal detection (cron-driven version of manual signal workflow above)
- **outreach-sender** — send orchestration with follow-up cadence
- **enterprise-sales** — navigating complex buying committees
- **sales-qualification** — qualifying leads before outreach
- **cold-email** — writing the actual outreach messages
- **prospect-demo** — [YOUR_PRODUCT]-specific personalized demos
- **meeting-prep** — pre-meeting intelligence briefings
