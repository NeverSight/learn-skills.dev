---
name: customer-reply
description: Write customer-facing support, outage, billing, bug, feature-request, and escalation replies.
---

## Foundational Communication Principles

1. **Acknowledge before solving.** Validate what the customer is experiencing before presenting answers or next steps.
2. **Front-load the key point.** Busy people skim -- put the most important information in the opening lines.
3. **Tell the truth.** Never promise what you cannot deliver, obscure problems behind jargon, or bury bad news.
4. **Be concrete.** Replace vague language with specific names, dates, and measurable commitments.
5. **Accept responsibility.** Use first-person ownership ("we caused" / "I will") rather than passive deflection ("an error occurred").
6. **End with clarity.** Every message must leave the customer knowing exactly what happens next.
7. **Mirror their emotional register.** Meet frustration with empathy; match enthusiasm with energy.

## Message Architecture

Most customer-facing replies follow four building blocks:

```
1. Recognition (1-2 sentences)
   Show you understand their situation or question.

2. Substance (1-3 short paragraphs)
   Deliver the answer, update, or resolution.
   Be precise and include supporting details.

3. Action Items (1-3 bullets)
   - Steps YOU are taking and by when
   - Steps THEY may need to take
   - When they will next hear from you

4. Sign-off (1 sentence)
   Warm, professional close with an open door.
```

## Channel-Appropriate Sizing

- **Live chat / instant message:** 1-4 sentences. Immediate, conversational, no filler.
- **Ticket reply:** 1-3 compact paragraphs. Easy to scan with clear structure.
- **Email:** Up to 5 paragraphs. Respect their inbox -- omit anything non-essential.
- **Escalation correspondence:** Thorough as needed, but organized under headings for navigation.
- **Executive-level communication:** Concise above all else. 2-3 paragraphs, data-forward.

## Tone Calibration

| Scenario | Register | Characteristics |
|----------|----------|-----------------|
| Positive news | Warm | Congratulatory, forward-looking, genuine |
| Standard update | Friendly-professional | Informative, efficient, approachable |
| Technical explanation | Patient-precise | Structured, detailed, jargon-free |
| Delayed resolution | Accountable | Honest about the delay, specific about new timeline |
| Negative outcome | Straightforward | Direct delivery, empathetic framing, solution-oriented |
| Service interruption | Transparent-urgent | Immediate, factual, calming, action-focused |
| High-stakes escalation | Composed-executive | Ownership-forward, plan-oriented, confident |
| Financial matter | Careful-factual | Precise amounts, clear explanations, empathetic |

### Adjusting for Relationship Maturity

**Early-stage customer (first 90 days):**
- Lean toward formality and thoroughness
- Provide extra context rather than assuming familiarity
- Proactively surface helpful resources
- Prioritize responsiveness to build confidence

**Long-standing customer:**
- Warmer, more conversational register
- Reference shared context and past interactions
- Communicate more directly and efficiently
- Demonstrate awareness of their business objectives

**Upset or escalated customer:**
- Lead with genuine empathy and validation
- Respond with urgency in both speed and substance
- Provide specific, time-bound action plans
- Shorten the feedback loop between updates

## Language Standards

**Prefer:**
- Active voice: "We are investigating" rather than "This is being investigated"
- Personal pronouns: "I" for individual commitments, "we" for team actions
- Named individuals: "Jordan on our infrastructure team will..." builds trust
- Customer vocabulary: adopt their terminology instead of internal labels
- Absolute dates: "by Wednesday March 18" instead of "in a few days"
- Visual structure: headers and bullet points in longer messages

**Avoid:**
- Corporate filler: "synergy," "leverage," "circle back," "paradigm"
- Blame redirection: never point fingers at other departments, vendors, or "the system"
- Ownership-dodging passive voice: "mistakes were made" hides accountability
- Excessive hedging: too many qualifiers erode confidence
- Unnecessary recipients: only loop in people who need to participate
- Overuse of exclamation marks: one per message at most

## Situational Message Frameworks

### Acknowledging a Defect Report

```
Hi [Name],

Thanks for flagging this -- I understand that [concrete impact] is
disrupting your work.

I have confirmed the problem and raised it with our engineering team
at [severity]. Here is what we know at this point:
- [Current understanding of the behavior]
- [Root cause, if identified]
- [Workaround, if one exists]

I will follow up by [date/time] with a timeline for the fix.
[Workaround details if applicable.]

Please reach out if you notice any additional effects.

Best,
[Name]
```

### Addressing a Billing or Account Problem

```
Hi [Name],

Thanks for getting in touch -- I understand that billing concerns
deserve fast answers.

After reviewing your account, here is what I found:
- [Factual summary of what occurred]
- [How it affected charges, access, or service]

To correct this, I am taking these steps:
- [Remediation action with expected timeline]
- [Additional action if needed]

[If already resolved: "The adjustment is complete and should appear
within [window]."]
[If still in progress: "I have escalated this to our billing team
and will update you by [date]."]

Sorry for the hassle. Let me know if anything else on your account
looks off.

Best,
[Name]
```

### Declining a Feature Request

```
Hi [Name],

Thanks for this suggestion -- I see why [capability] would be
useful for [their scenario].

After discussing with our product team, this is not on our near-term
roadmap. The main reason is [straightforward, respectful rationale].

That said, here are some paths that might get you close to your goal:
- [Alternative 1]
- [Alternative 2]
- [API/integration option if relevant]

Your request is captured in our feedback pipeline, and I will let you
know if our plans shift.

Would any of these alternatives work for your team? Happy to explore
them further.

Best,
[Name]
```

### Communicating During an Incident

```
Hi [Name],

I am reaching out because an issue with [affected service/feature]
is impacting functionality your team depends on.

**What is happening:** [Plain-language explanation]
**Effect on your usage:** [Their specific impact]
**Current status:** [Investigating / Cause identified / Fix deploying / Resolved]
**Expected resolution:** [Time estimate or update cadence]

[If applicable: "As a temporary measure, you can [workaround]."]

I am monitoring this directly and will update you when we have
progress. Live status is also available at [status page URL].

I apologize for the disruption. [Mention prevention steps if known.]

[Name]
```

### Re-engaging After No Response

```
Hi [Name],

Just circling back -- I sent [description] on [date] and want to
make sure it reached you.

[One-sentence recap of what is pending or offered.]

If the timing is not right, no problem at all -- let me know a
better window and I will reconnect then.

Best,
[Name]
```

## Contextual Personalization

### Newer Customers
- Supply additional background and explanation
- Point to onboarding resources and getting-started material
- Introduce self-service options proactively

### Experienced Customers
- Skip foundational explanations they already possess
- Acknowledge their depth of product knowledge
- Get to the point quickly and efficiently

### Customers Under Stress
- Prioritize empathy and acknowledgment above all
- Center the reply around resolving their specific problem
- Offer tangible action plans with committed deadlines
- Provide a direct path to further escalation if needed

## Follow-up Timing Reference

| Context | Recommended Follow-up Window |
|---------|------------------------------|
| Unanswered question from customer | 2-3 business days |
| Active support issue (high severity) | Daily or more frequently per SLA |
| Active support issue (standard) | Every 2-3 business days |
| Post-meeting action items | Summary within 24 hours; check at each deadline |
| After delivering unwelcome news | ~1 week to gauge impact and sentiment |

## When to Involve Others

**Bring in your manager when:**
- A customer signals potential cancellation or significant downgrade
- A policy exception is needed beyond your authority
- Resolution has exceeded SLA boundaries
- The customer asks for leadership contact
- Your own error requires senior-level remediation

**Bring in product or engineering when:**
- A defect is blocking the customer's core operations
- A capability gap is causing competitive loss
- Technical requirements exceed standard support scope
- Integration-level investigation is necessary

## Working Principles

1. Determine the scenario type first, then select the matching tone and framework.
2. Factor in relationship maturity and the stakeholder's seniority.
3. For problems, empathy precedes solutions; for wins, energy matches theirs.
4. Anchor every commitment to a specific date or measurable outcome.
5. Guarantee a visible next step in every message.
6. Re-read the draft as the customer would before sending.
7. Secure internal alignment before making commitments on sensitive or cross-team topics.
8. Ruthlessly trim -- every sentence must justify its presence.
