---
name: post-demo
description: Generate post-demo follow-up emails, meeting summaries, and internal debriefs. Use after a sales call or demo when the user needs to send a follow-up, summarize what happened, or plan next steps.
license: MIT
metadata:
  author: toughtongueai
  version: "1.0"
---

# Post-Demo Follow-Up

Generate structured follow-up materials after a sales call or demo. Produces a follow-up email, internal debrief, and follow-up sequence plan — all based on what actually happened in the conversation.

## When to Use

- User says "write a follow-up for my call with [name]"
- User just finished a demo and needs to send a recap
- User wants to create an internal debrief for their team
- User needs to plan the follow-up sequence (nudge, re-engagement)

## Required Inputs

Ask the user for:

```
Who: [Contact name, title, company]
What happened: [Paste meeting notes, transcript, or describe what was discussed]
Outcome: [Positive / Neutral / Negative — what's the next step?]
```

The more detail they provide, the better the output. A transcript is ideal. Bullet points work. Even "it went well, they want a pilot" is enough to generate useful follow-up.

## Process

### 1. Load Context

Read `company-profile.md` for the user's product and positioning.

If a prep file exists for this prospect (e.g., `prep/acme-sarah-chen-2026-03-06.md`), read it for pre-meeting context.

### 2. Extract Key Information

From the meeting notes or transcript, identify:

| What to Extract | Why It Matters |
|----------------|---------------|
| **Topics discussed** | Structure the follow-up email |
| **Pain points mentioned** | Reinforce in follow-up |
| **Objections raised** | Address proactively in email |
| **Questions they asked** | Answer any that were deferred |
| **Buying signals** | Note for internal debrief |
| **Red flags** | Note for internal debrief |
| **Agreed next steps** | Confirm in email |
| **Other stakeholders mentioned** | Multi-thread opportunity |
| **Timeline** | Urgency indicator |
| **Budget discussion** | Qualification data |

### 3. Generate Outputs

Produce all three outputs below.

## Output Structure

### OUTPUT 1: Follow-Up Email

Send within 2-4 hours of the call. Reference specific things discussed — never send a generic follow-up.

```
Subject: Great chatting, [Name] — here's everything we discussed

Hi [Name],

Thanks for your time today. I really enjoyed learning about [SPECIFIC thing from the conversation — not generic].

Here's a quick recap:

**What we discussed:**
1. [Specific topic 1 — use their words where possible]
2. [Specific topic 2]
3. [Specific topic 3]

**Resources:**
- [Link to the product/demo/resource they asked about]
- [Link to anything you promised to send]

**Next steps:**
- [ ] [Their action item — specific and timeboxed]
- [ ] [Your action item — specific and timeboxed]
- [ ] [Follow-up date]

Let me know if I missed anything or if you'd like to loop in anyone else.

Best,
[User Name]
[Title, Company]
```

**Rules:**
- Reference at least one specific thing from the conversation (shows you listened)
- Include direct links to resources, not the homepage
- Action items should be concrete, not vague ("share with your team by Friday" not "think about it")
- Send the same day while the conversation is fresh

### OUTPUT 2: Internal Debrief

A structured summary for the user's own records or to share with their team.

```markdown
# Call Debrief: [Company] — [Contact Name]
**Date:** [Date]
**Duration:** [Estimated]
**Attendees:** [Who was on the call]

## Summary
[2-3 sentence overview of how the call went]

## Buying Signals
- [Signal 1 — e.g., "Asked about pricing unprompted"]
- [Signal 2 — e.g., "Mentioned wanting to start this quarter"]

## Red Flags
- [Flag 1 — e.g., "Mentioned budget freeze until Q3"]
- [Flag 2 — e.g., "Seemed distracted, had to leave early"]

## Objections Raised
| Objection | How You Responded | Better Response for Next Time |
|-----------|-------------------|------------------------------|
| [Objection] | [What you said] | [What might work better] |

## Key Quotes
- "[Exact quote from the prospect that reveals their priorities]"
- "[Exact quote that could be used in the follow-up or proposal]"

## Next Steps
| Action | Owner | Deadline |
|--------|-------|----------|
| [Action item] | [You / Them] | [Date] |

## Deal Assessment
- **Interest level:** [High / Medium / Low]
- **Decision timeline:** [Immediate / This quarter / Next quarter / Unknown]
- **Budget:** [Confirmed / Likely / Unknown / Constrained]
- **Decision maker:** [On the call / Need to involve / Unknown]
- **Recommended follow-up cadence:** [See follow-up sequence]
```

### OUTPUT 3: Follow-Up Sequence Plan

Based on the call outcome, recommend a follow-up cadence. See [Follow-Up Sequence](references/follow-up-sequence.md) for timing guidance.

```markdown
## Follow-Up Plan

| Day | Action | Template |
|-----|--------|----------|
| Day 0 | Send follow-up email (OUTPUT 1 above) | — |
| Day 3-5 | Nudge if no response | [Generated nudge below] |
| Day 10-14 | Second follow-up with new value | [Generated email below] |
| Day 21+ | Re-engagement if gone cold | [Generated email below] |
```

**Nudge (Day 3-5):**
```
Subject: Following up — [specific topic from the call]

Hi [Name],

Circling back on our conversation. [Reference specific next step they agreed to.]

[One sentence offering to help — e.g., "Happy to jump on a quick call if any questions came up."]

Best,
[User Name]
```

**Second Follow-Up (Day 10-14):**
```
Subject: [Something new — a relevant resource, result, or update]

Hi [Name],

Quick update: [new information relevant to their situation — e.g., "We just published a case study with a company in your space" or "I built out the custom scenario we discussed"].

Thought this might be useful as you [evaluate / discuss with your team / plan for next quarter].

Worth a quick chat? [Calendar link]

Best,
[User Name]
```

**Re-Engagement (Day 21+):**
```
Subject: Still interested in [topic from your conversation]?

Hi [Name],

Hope things are going well! I know things get busy — just checking in.

When we spoke, you were exploring [their use case]. Is that still on your radar?

If timing isn't right, totally understand. But if you'd like to pick up where we left off: [Calendar link]

Best,
[User Name]
```

## Instructions

1. **Specificity is everything.** A follow-up that says "Thanks for the great chat" is forgettable. A follow-up that says "Your point about [exact thing] really stuck with me" is memorable.
2. **Use their words.** Quote them back to themselves. It shows you listened and makes them feel heard.
3. **Action items must be concrete.** "Let's reconnect soon" is not an action item. "I'll send the case study by Thursday, and you'll share with your VP by next Monday" is.
4. **The internal debrief is for you.** Be honest about red flags and objections. Don't sugarcoat for yourself.
5. **Send the follow-up the same day.** Every hour you wait reduces the chance of a response.
6. **If the call went poorly, say so in the debrief.** "They were polite but not interested" is useful data. "Great call!" when it wasn't is self-deception.
