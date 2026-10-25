---
name: sales-demo-script
description: "Use this skill when you need to plan or run a B2B product demo that moves the deal forward: \"build a demo script\", \"prep my demo for tomorrow\", \"our demos are feature tours\", \"tailor the demo to this prospect\". Builds a discovery-led demo around the buyer's top two or three problems: a quick recap, the before-and-after story, the moments that matter, proof, and a clear next step. Produces a timed demo plan, talk track, the questions to ask during it and the follow-up email."
license: MIT
metadata:
  title: Sales demo script
  category: deals
  tags: "Sales, Founders, Sales Leaders"
  author: prosyo
  version: "1.0.0"
  keywords: "sales demo script, product demo best practices b2b, demo talk track, claude demo script skill, discovery led demo"
  inputs: "Discovery notes, Attendees and roles, Product and proof"
  outputs: "Timed demo plan, Talk track, In-demo questions, Follow-up email"
---

Use this before any demo. A good demo is not a tour of the product; it is proof that the buyer's specific problems go away, shown in the order they care about.

## Inputs

- Discovery notes: the problems, their impact, the buyer's words, what success looks like.
- Attendees and their roles (the champion, the economic buyer, evaluators, users).
- The product areas that solve those problems, and approved proof.

## The play

### 1. Choose two or three moments
From discovery, pick the problems with the biggest impact. Each becomes one "moment" in the demo: the before (their pain, in their words), the after (the product doing the job), and the proof. Everything else is left out, however impressive.

### 2. Structure the time
| Minutes (of 30) | Section |
| --- | --- |
| 0-3 | Recap: "Here's what we heard. Still right? Anything changed?" |
| 3-6 | The headline outcome: what life looks like after, in one screen |
| 6-22 | Two or three moments, most important first |
| 22-26 | Questions and objections |
| 26-30 | Next step agreed with dates and people |

Start with the most important moment. Executives often leave early.

### 3. Talk track per moment
1. **Set it up**: "You said approvals stall close for a week."
2. **Show it**: the shortest path in the product, with their data or a realistic example.
3. **Land it**: "That's the step that took Contoso from 9 days to 4."
4. **Check it**: "How would this work with your approval rules?"

### 4. Prepare for each role
Evaluators want to see how it works; economic buyers want impact and risk; users want to know it is easy. Plan one line for each role.

### 5. Close with a next step
Propose it, don't ask what they want to do: "Next would be a technical review with Dev and a trial on your data. Does Thursday work?"

## What good looks like

- The buyer talks for at least a third of the demo.
- No screen appears that does not map to a stated problem.
- The demo ends with a dated, agreed next step.
- The common mistake is starting with the login screen and touring every menu, so the moment that matters arrives at minute 25 after the buyer has stopped listening.

## Rules

- MUST start with a recap of the buyer's problems.
- MUST map each demo moment to a stated problem.
- NEVER demo features that are not available, or present roadmap items as live.
- NEVER show other customers' data.

## Example prompts

- "Build a 30-minute demo plan for Lumen from these discovery notes. The CFO joins for the first 10 minutes."
- "Our demos run 60 minutes and buyers drift. Rewrite our standard demo."
- "Write the follow-up email after today's demo with the next steps we agreed."
