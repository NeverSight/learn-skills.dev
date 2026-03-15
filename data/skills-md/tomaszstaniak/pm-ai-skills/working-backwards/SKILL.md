---
name: working-backwards
description: 'Amazon''s Working Backwards product development method based on Colin Bryar and Bill Carr''s "Working Backwards". Use when you need to: (1) write a PR/FAQ document for a new product or feature, (2) validate an idea by defining the customer experience first, (3) stress-test a proposal with pre-mortem analysis, (4) align stakeholders around a product vision, (5) decide whether an idea is worth building before writing code.'
license: CC-BY-SA-4.0
metadata:
  author: Tomasz Staniak
  version: "1.0.0"
---

# Working Backwards (PR/FAQ)

A product development method pioneered at Amazon: start from the customer experience and work backwards to the technology. The centerpiece is the PR/FAQ document — a fictional press release and FAQ written before a single line of code, forcing clarity of thought about who benefits, why they care, and what could go wrong. Includes a built-in pre-mortem step based on Gary Klein's prospective hindsight technique.

## Core Principle

**If you can't write a compelling press release, you don't understand the product yet.** Writing forces thinking. A PR/FAQ written at the start — not the end — of a project exposes fuzzy thinking, missing logic, and unjustified assumptions before any resources are committed. If the press release is boring, the product will be boring.

The Working Backwards process inverts the typical development flow:

```
Traditional:  Idea → Build → Launch → Explain to customers
Amazon:       Customer need → PR/FAQ → Debate → Build only if compelling
```

## Scoring

**Goal: 10/10.** When reviewing a PR/FAQ or product proposal, rate it 0-10:

| Score | Description |
|-------|-------------|
| 0-2 | No written proposal. Idea is a verbal pitch or a slide deck with bullet points. |
| 3-4 | Written proposal exists but reads like an internal spec. Customer benefit is vague. No FAQ. |
| 5-6 | PR/FAQ format used but the press release is generic, FAQ avoids hard questions, no pre-mortem. |
| 7-8 | Strong PR/FAQ. Clear customer, specific benefit, honest FAQ, identifies key risks. |
| 9-10 | Exceptional. Press release makes you want the product. FAQ addresses every tough question. Pre-mortem reveals non-obvious risks with mitigations. The document alone could be used to decide go/no-go. |

## The PR/FAQ Document

### Part 1: The Press Release (1 page max)

A fictional press release announcing the finished product. Written in the voice of a real press release, as if the product already exists.

**Structure:**

| Section | Content | Length |
|---------|---------|--------|
| **Heading** | Product name + customer benefit in one line | 1 sentence |
| **Subheading** | Who the customer is + what they can now do | 1 sentence |
| **Opening paragraph** | Summary: what it is, who it's for, why it matters | 3-4 sentences |
| **Problem paragraph** | The customer problem or pain point (in the customer's words) | 3-4 sentences |
| **Solution paragraph** | How the product solves it — specific, concrete, no jargon | 3-4 sentences |
| **Quote from leader** | Why the company built this (vision, mission alignment) | 2-3 sentences |
| **How it works** | Simple explanation a customer can follow | 3-4 sentences |
| **Quote from customer** | A fictional customer describing the benefit they experienced | 2-3 sentences |
| **Call to action** | How to get started | 1 sentence |

**Rules:**
- No internal jargon, no technical architecture, no org chart references
- Every sentence must be understandable by the target customer
- If you can't explain the benefit simply, the idea isn't clear yet
- The customer quote should express the emotional benefit, not feature specs
- Maximum 1 page

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| New product idea | Write PR before any design work | Forces "what's the headline?" thinking before "what's the architecture?" |
| Feature proposal | Write a mini-PR for significant features | "Acme launches auto-save: never lose your work again" |
| Pivot decision | Write PR for the pivot and compare to current direction | If the pivot PR is more compelling, that's a signal |

**Copy patterns:**
- "[Product] launches [headline benefit]: [one-sentence customer outcome]"
- "Until now, [customer segment] had to [painful alternative]. Starting today, [product] [specific benefit]."
- "'[Emotional customer quote about the outcome, not the feature]' — [Name], [Role] at [Company]"

**Ethical boundary:** The press release must describe a product you genuinely intend to build. Never use PR/FAQ as a marketing exercise for vaporware. If the PR describes capabilities you can't deliver, you're not working backwards — you're fabricating forwards.

See: [references/press-release-writing.md](references/press-release-writing.md)

### Part 2: The FAQ (2-5 pages)

Two sections: external FAQ (customer questions) and internal FAQ (stakeholder/business questions).

**External FAQ (customer perspective):**
- How much does it cost?
- How is this different from [alternative]?
- What do I need to get started?
- What happens to my data?
- What if it doesn't work for me?

**Internal FAQ (business perspective):**
- What is the estimated market size / TAM?
- What are the unit economics?
- How long will it take to build? What's the team needed?
- What are the key dependencies and risks?
- How will we measure success? What are the metrics?
- What's the competitive landscape?
- Why now? What changed that makes this the right time?

**Key insights:**
- The FAQ is where honesty lives — the PR is aspirational, the FAQ is realistic
- If you can't answer the internal FAQ convincingly, the project isn't ready
- Update the FAQ as you learn — it's a living document
- The hardest questions to answer are the most important ones to include

**Copy patterns:**
- "Q: How is this different from [competitor]? A: Unlike [competitor], [product] [specific differentiator] because [reason]."
- "Q: What if it doesn't work? A: [Concrete fallback, guarantee, or risk mitigation]."
- "Q: Why now? A: [Market shift / technology change / customer behavior change] makes this the right moment because [evidence]."

**Ethical boundary:** Never omit FAQ questions because the answers are unfavorable. The FAQ's value is proportional to its honesty. If an internal FAQ answer reveals a fatal flaw, that's the FAQ doing its job — not a reason to delete the question.

See: [references/faq-construction.md](references/faq-construction.md)

### Part 3: The Pre-Mortem (1 page)

**Based on Gary Klein's prospective hindsight technique.** After writing the PR/FAQ, assume the product has launched and failed. Work backwards from failure to identify what went wrong.

**The Pre-Mortem Protocol:**

```
Prompt: "It is [12 months from now]. This product launched and failed
to meet its goals. Customers didn't adopt it. The team is disappointed.
What went wrong?"
```

**Generate 5-7 failure scenarios across these categories:**

| Category | Question | Example failure |
|----------|----------|----------------|
| Customer | Did we solve a real problem? | "Users didn't have this problem often enough to change behavior" |
| Market | Is the timing/competition right? | "A well-funded competitor launched the same thing 2 months before us" |
| Execution | Can we actually build and ship this? | "The ML model never achieved the accuracy we assumed in the PR" |
| Business model | Do the economics work? | "Customer acquisition cost was 3x what we modeled" |
| Adoption | Will people switch? | "Users were too entrenched in their current workflow to migrate" |
| Internal | Does the organization support this? | "The sales team couldn't explain the product and stopped selling it" |

**For each failure scenario, specify:**
1. **Likelihood** (High / Medium / Low)
2. **Impact** (High / Medium / Low)
3. **Early warning signal** — how would you detect this is happening?
4. **Mitigation** — what can you do now to prevent it?

**Why pre-mortem works here:** By the time you've written a compelling PR and honest FAQ, you're emotionally invested. The pre-mortem is the structured antidote to optimism bias. It leverages "prospective hindsight" — imagining an event has already happened makes people 30% better at identifying reasons for outcomes (Klein, 1989).

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Go/no-go decision | Pre-mortem reveals deal-breakers before committing resources | "3 of 5 failure scenarios are High likelihood — rethink before proceeding" |
| Risk planning | Convert mitigations into sprint-zero tasks | "Build a competitive monitoring dashboard before launch" |
| Team alignment | Share pre-mortem to build shared understanding of risks | Team sees risks they individually sensed but never voiced |

**Ethical boundary:** The pre-mortem must be genuinely open-ended. Never write it to rubber-stamp a decision already made. If the pre-mortem reveals fatal risks, take them seriously.

See: [references/pre-mortem-protocol.md](references/pre-mortem-protocol.md)

## The Full Working Backwards Process

| Step | Action | Time |
|------|--------|------|
| 1 | Write the Press Release (1 page) | 2-4 hours |
| 2 | Write the FAQ — external + internal (2-5 pages) | 4-8 hours |
| 3 | Run the Pre-Mortem (1 page) | 1-2 hours |
| 4 | Circulate for feedback — silent reading, written comments | 1 week |
| 5 | Revise based on feedback | 2-4 hours |
| 6 | Decision meeting: go / no-go / revise | 1 hour |

**Key insights:**
- Amazon's rule: documents are read silently at the start of the meeting (no pre-reads). This ensures everyone has the same context.
- The document is the thinking, not a summary of the thinking. Narrative forces logical structure that bullet points hide.
- Iteration is expected — most PR/FAQs go through 5-10 revisions before approval
- A rejected PR/FAQ is a success — you avoided building the wrong thing

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Writing the PR after building | Defeats the purpose — it's a rationalization, not a thought tool | Write the PR as the very first step, before any design or code |
| Jargon in the press release | If customers can't understand it, you don't understand it | Read it to someone outside the team. If they're confused, rewrite. |
| Softball FAQ questions | Avoids the hard questions that kill projects later | Include every question that makes you uncomfortable |
| Skipping the pre-mortem | Optimism bias goes unchecked; risks surface too late | Always do the pre-mortem. It takes 1 hour and can save months. |
| Treating PR/FAQ as a formality | Going through motions without genuine debate | If the go/no-go meeting is always "go," the process is broken |
| Solo authorship | One person's blind spots become the project's blind spots | Product trio writes together; diverse perspectives improve quality |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can you state the customer benefit in one sentence? | Idea isn't clear enough | Write the PR headline first — if you can't, keep thinking |
| Would a customer understand your press release? | Too much insider language | Rewrite in the customer's words |
| Does your FAQ include questions you're afraid to answer? | You're avoiding hard truths | Add 3 uncomfortable questions and answer them honestly |
| Have you run a pre-mortem? | Optimism bias is unaddressed | Spend 1 hour imagining failure — identify top 5 risks |
| Has anyone outside the team read the document? | Echo chamber risk | Share with a skeptic and incorporate their feedback |

## Reference Files

- [Press Release Writing Guide](references/press-release-writing.md) — Section-by-section guide to writing the PR, common pitfalls, templates, and worked examples for B2B SaaS, consumer apps, and internal tools
- [FAQ Construction](references/faq-construction.md) — External vs. internal FAQ frameworks, question generation techniques, how to answer hard questions honestly, and FAQ iteration strategies
- [Pre-Mortem Protocol](references/pre-mortem-protocol.md) — Gary Klein's prospective hindsight technique adapted for product development, failure category taxonomy, likelihood/impact scoring, and mitigation planning templates
- [Narrative Decision-Making](references/narrative-decisions.md) — Why Amazon chose narratives over slide decks, the six-pager format, silent reading protocols, and how to run effective document-based decision meetings

## Further Reading

- [Working Backwards by Colin Bryar and Bill Carr](https://www.amazon.com/Working-Backwards-Insights-Stories-Secrets/dp/1250267595?tag=wondelai00-20)
- [Sources of Power by Gary Klein](https://www.amazon.com/Sources-Power-People-Make-Decisions/dp/0262611465?tag=wondelai00-20) (origin of the pre-mortem technique)

## About the Authors

Colin Bryar and Bill Carr are former Amazon executives. Bryar served as Jeff Bezos' "shadow" (Technical Advisor) for two years. Carr led the launch of Amazon's digital media businesses including Prime Video and Amazon Music. Together they spent 27 years at Amazon and witnessed the development of its distinctive management practices firsthand.
