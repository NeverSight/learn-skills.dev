---
name: demo-prep
description: Generate a complete demo preparation package for an upcoming meeting. Use when the user has a demo, discovery call, or sales meeting coming up and needs to prepare. Researches the prospect, generates talking points, SPIN questions, objection handling, and email templates — all personalized to the user's product.
license: MIT
compatibility: Requires internet access for prospect research.
metadata:
  author: toughtongueai
  version: "1.0"
---

# Demo Preparation

Generate a complete preparation package for an upcoming sales meeting. This is the flagship skill — it orchestrates research, generates talking points, predicts objections, and produces ready-to-use emails, all customized to your product and the specific prospect.

## When to Use

- User has a demo, discovery call, or follow-up meeting coming up
- User says "prep me for a demo with [name] at [company]"
- User provides meeting details (company, contact, date)
- User needs a structured game plan before a sales conversation

## Required Inputs

Ask the user for:

```
Company: [Name or website URL]
Contact: [Name and title]
Meeting Type: [Discovery call / Product demo / Follow-up / Pilot discussion]
Any Context: [How did this meeting come about? Inbound? Cold outreach? Referral?]
```

Optional but helpful:
- Specific topics they want to cover
- Known pain points or requirements
- Whether others are joining the call

## Process

### 1. Load Your Context

Read `company-profile.md` from the workspace root. This contains the user's company info, product description, ICP, differentiators, objections, and background.

If it doesn't exist, tell the user to run the `setup-company` skill first.

### 2. Research the Prospect

Use the `research-prospect` skill process to gather:
- Company intel (what they do, size, sales model, recent news)
- Contact intel (role, background, tenure, recent activity)
- Personalization hooks (shared connections, schools, companies)
- ICP fit assessment

Visit the company's website and look up the contact on LinkedIn using browser tools. Do not fabricate information.

### 3. Generate the Prep Package

Produce all 8 outputs below, customized to the prospect and the user's product.

## Output Structure

Save the output as `prep/[company]-[contact]-[date].md`.

---

### OUTPUT 1: Meeting Brief

A one-page summary the user can glance at 5 minutes before the call.

```markdown
# Demo Prep: [Company] — [Contact Name]
**Date:** [Meeting date]
**Type:** [Discovery / Demo / Follow-up]
**Duration:** [Estimated]

## Quick Summary
- **Company:** [What they do, in one line]
- **Contact:** [Name, Title — tenure, one notable background fact]
- **Why they're talking to you:** [Inbound? Referral? Cold?]
- **Strongest hook:** [Your best personalization angle]
- **ICP fit:** [Strong / Medium / Weak]
```

---

### OUTPUT 2: Tailored Value Proposition

Write a 2-3 sentence value proposition customized to their role and company. Map the user's product strengths to the prospect's likely needs.

| If Their Role Is... | Angle to Emphasize |
|---------------------|-------------------|
| Sales / Revenue | Impact on pipeline, conversion rates, deal velocity |
| Operations / Enablement | Efficiency, consistency, scalability, reduced manual work |
| Product / Engineering | Integration ease, API/SDK, developer experience, customization |
| Executive / C-Suite | ROI, strategic impact, competitive advantage, cost reduction |
| L&D / Training / HR | Measurable outcomes, engagement, scalability, cost per learner |

---

### OUTPUT 3: Conversation Starter

Write the first 60 seconds of the call. This should:
- Open with the personalization hook (shared connection, recent news, etc.)
- Acknowledge why they're meeting
- Set the agenda
- Transition to discovery

**Template:**

> "Hey [Name], great to connect. [Personalization hook — 1 sentence]. I've been looking at [Company] and [one specific observation about their business]. Before I show you anything, I'd love to understand [transition to discovery question]."

---

### OUTPUT 4: SPIN Questions

Generate 5-7 discovery questions using the SPIN framework, tailored to this prospect's likely situation. See [SPIN Framework Reference](references/spin-framework.md) for details.

| Stage | Question | Why You're Asking |
|-------|----------|-------------------|
| **Situation** | [Question about their current state] | [What you'll learn] |
| **Situation** | [Question about their process/tools] | [What you'll learn] |
| **Problem** | [Question about frustrations or gaps] | [What pain to probe] |
| **Problem** | [Question about what's not working] | [What pain to probe] |
| **Implication** | [Question about consequences of not solving] | [Builds urgency] |
| **Need-Payoff** | [Question that lets them articulate value] | [They sell themselves] |
| **Need-Payoff** | [Question about ideal outcome] | [Frames your solution] |

---

### OUTPUT 5: Demo Focus Areas

Based on the prospect's role, company, and likely pain points, recommend the top 3 things to emphasize in the demo.

```markdown
## Demo Focus
1. **[Feature/Capability]** — [Why this matters to them specifically]
2. **[Feature/Capability]** — [Why this matters to them specifically]
3. **[Feature/Capability]** — [Why this matters to them specifically]

## What to Skip
- [Feature that's not relevant to this prospect — and why]
```

---

### OUTPUT 6: Objection Handling

Predict 2-3 objections this specific prospect is likely to raise, based on their company, role, and industry. Pull from the user's `company-profile.md` objection list and customize.

| Objection | Why They'll Raise It | Response |
|-----------|---------------------|----------|
| [Predicted objection] | [Context — e.g., "they already use a competitor"] | [Specific response using user's positioning] |
| [Predicted objection] | [Context] | [Specific response] |
| [Predicted objection] | [Context] | [Specific response] |

---

### OUTPUT 7: Email Templates

**Pre-Meeting Email** — Send 24-48 hours before the call. Problem-priming: get them thinking about their biggest challenge before you meet.

```
Subject: Quick ask before our call, [Name]

Hi [Name],

Looking forward to [day]. Quick ask to make our time useful:

Think of [the ONE challenge relevant to user's product that their team faces]. Come ready to describe it in a few sentences.

I'll show you how we approach it — and I've already put together some initial thoughts based on what I know about [Company].

Feel free to bring anyone who'd find this useful.

See you then,
[User Name]
```

**Post-Meeting Email Template** — Fill in after the call.

```
Subject: Great chatting, [Name] — here's everything we discussed

Hi [Name],

Thanks for your time today. I enjoyed learning about [PLACEHOLDER: specific thing from the conversation].

Here's a quick recap:

1. [PLACEHOLDER: Key topic 1]
2. [PLACEHOLDER: Key topic 2]
3. [PLACEHOLDER: Key topic 3]

Next steps:
- [ ] [PLACEHOLDER: Their action item]
- [ ] [PLACEHOLDER: Your action item]
- [ ] [PLACEHOLDER: Timeline for follow-up]

Let me know if I missed anything or if you'd like to loop in anyone else.

Best,
[User Name]
```

---

### OUTPUT 8: Reverse Demo Prompt (Optional)

If the user's product supports live demos or co-creation, generate a prompt they can use to build something specific to this prospect during the call. See [Reverse Demo Guide](references/reverse-demo-guide.md) for the methodology.

```markdown
## Reverse Demo Prompt

**Pre-built scenario for this prospect:**
"[A natural language description of a scenario specific to their business — something the user can build or show during the call that makes the prospect say 'that's exactly our problem']"

**Co-creation template (fill in during the call):**
"[Template with placeholders for the prospect's own words — to be completed live based on what they describe]"

**Transition script:**
> "That was a starting point I put together based on what I know about [Company]. But your team's real challenges are probably different. Tell me: what's the ONE [relevant challenge] your team faces? Describe it and I'll [customize/build/configure] it right now."
```

## Instructions

1. **Always research first.** Never generate prep without visiting the company's website and looking up the contact. Fabricated details destroy credibility.
2. **Read `company-profile.md`.** Every output should reference the user's actual product, differentiators, and positioning — not generic advice.
3. **Be specific, not generic.** "They might care about ROI" is useless. "They're a 200-person Series B with 15 SDRs — they likely care about reducing ramp time for new hires" is actionable.
4. **Prioritize the meeting brief and SPIN questions.** If the user is short on time, these two outputs give them 80% of the value.
5. **Save the output.** Write to `prep/[company]-[contact]-[date].md` so they build a library of prep docs over time.
6. **The pre-meeting email is high-leverage.** A good problem-priming email makes the prospect come prepared, which makes the demo 2x more productive.
