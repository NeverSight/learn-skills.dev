---
name: iblai-marketing-email-sequence
description: When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program. Also use when the user mentions "email sequence," "drip campaign," "nurture sequence," "onboarding emails," "welcome sequence," "re-engagement emails," "email automation," "lifecycle emails," "trigger-based emails," "email funnel," "email workflow," "what emails should I send," "welcome series," or "email cadence." Use this for any multi-email automated flow. For cold outreach emails, see iblai-marketing-cold-email. For in-app onboarding, see iblai-marketing-onboarding-cro.
globs:
alwaysApply: false
metadata:
  version: 1.1.0
---

# /iblai-marketing-email-sequence

Design email sequences that nurture relationships, drive action, and move
people toward conversion.

## Step 0: Context Check

Read `.agents/product-marketing-context.md` (or `.claude/product-marketing-context.md`
on older setups) first. Only ask for what isn't there.

Pin down before drafting:

1. **Sequence Type**
   - Welcome/onboarding
   - Lead nurture
   - Re-engagement
   - Post-purchase
   - Event-based
   - Educational
   - Sales

2. **Audience Context**
   - Who they are
   - What triggered them into this sequence
   - What they already know/believe
   - Current relationship with you

3. **Goals**
   - Primary conversion goal
   - Relationship-building goals
   - Segmentation goals
   - Definition of success

---

## Core Principles

1. **One email, one job.** One primary purpose. One CTA. Don't try to do everything.
2. **Value before ask.** Lead with usefulness. Build trust through content. Earn the right to sell.
3. **Relevance over volume.** Fewer, better emails win. Segment for relevance. Quality > frequency.
4. **Clear path forward.** Every email moves the reader somewhere. Make next steps obvious.

---

## Sequence Strategy

### Length

- Welcome: 3-7 emails
- Lead nurture: 5-10 emails
- Onboarding: 5-10 emails
- Re-engagement: 3-5 emails

Calibrate by:
- Sales cycle length
- Product complexity
- Relationship stage

### Timing/Delays

- Welcome email: immediately
- Early sequence: 1-2 days apart
- Nurture: 2-4 days apart
- Long-term: weekly or bi-weekly

Calibrate by:
- B2B: avoid weekends
- B2C: test weekends
- Time zones: send at local time

### Subject Lines

- Clear > clever
- Specific > vague
- Benefit- or curiosity-driven
- 40-60 characters ideal
- Test emoji (polarizing)

**Patterns that work:**
- Question: "Still struggling with X?"
- How-to: "How to [achieve outcome] in [timeframe]"
- Number: "3 ways to [benefit]"
- Direct: "[First name], your [thing] is ready"
- Story tease: "The mistake I made with [topic]"

### Preview Text

- Extends the subject line
- ~90-140 characters
- Don't repeat the subject line
- Complete the thought or add intrigue

---

## Sequence Types

### Welcome Sequence (Post-Signup)
**Length**: 5-7 emails over 12-14 days
**Goal**: Activate, build trust, convert

Key emails:
1. Welcome + deliver promised value (immediate)
2. Quick win (day 1-2)
3. Story/Why (day 3-4)
4. Social proof (day 5-6)
5. Overcome objection (day 7-8)
6. Core feature highlight (day 9-11)
7. Conversion (day 12-14)

### Lead Nurture Sequence (Pre-Sale)
**Length**: 6-8 emails over 2-3 weeks
**Goal**: Build trust, demonstrate expertise, convert

Key emails:
1. Deliver lead magnet + intro (immediate)
2. Expand on topic (day 2-3)
3. Problem deep-dive (day 4-5)
4. Solution framework (day 6-8)
5. Case study (day 9-11)
6. Differentiation (day 12-14)
7. Objection handler (day 15-18)
8. Direct offer (day 19-21)

### Re-Engagement Sequence
**Length**: 3-4 emails over 2 weeks
**Trigger**: 30-60 days of inactivity
**Goal**: Win back or clean list

Key emails:
1. Check-in (genuine concern)
2. Value reminder (what's new)
3. Incentive (special offer)
4. Last chance (stay or unsubscribe)

### Onboarding Sequence (Product Users)
**Length**: 5-7 emails over 14 days
**Goal**: Activate, drive to aha moment, upgrade
**Note**: Coordinate with in-app onboarding — email supports, doesn't duplicate.

Key emails:
1. Welcome + first step (immediate)
2. Getting started help (day 1)
3. Feature highlight (day 2-3)
4. Success story (day 4-5)
5. Check-in (day 7)
6. Advanced tip (day 10-12)
7. Upgrade/expand (day 14+)

Detailed templates: [references/sequence-templates.md](references/sequence-templates.md).

---

## Email Types by Category

### Onboarding
- New users series
- New customers series
- Key onboarding step reminders
- New user invites

### Retention
- Upgrade to paid
- Upgrade to higher plan
- Ask for review
- Proactive support offers
- Product usage reports
- NPS survey
- Referral program

### Billing
- Switch to annual
- Failed payment recovery
- Cancellation survey
- Upcoming renewal reminders

### Usage
- Daily/weekly/monthly summaries
- Key event notifications
- Milestone celebrations

### Win-Back
- Expired trials
- Cancelled customers

### Campaign
- Monthly roundup / newsletter
- Seasonal promotions
- Product updates
- Industry news roundup
- Pricing updates

Detailed reference: [references/email-types.md](references/email-types.md).

---

## Copy Guidelines

### Structure

1. **Hook** — first line grabs attention
2. **Context** — why this matters to them
3. **Value** — the useful content
4. **CTA** — what to do next
5. **Sign-off** — human, warm close

### Formatting

- Short paragraphs (1-3 sentences)
- White space between sections
- Bullets for scannability
- Bold for emphasis (sparingly)
- Mobile-first (most reads happen on phone)

### Tone

- Conversational, not formal
- First-person (I/we) and second-person (you)
- Active voice
- Read it aloud — does it sound human?

### Length

- 50-125 words for transactional
- 150-300 words for educational
- 300-500 words for story-driven

### CTAs

- Buttons for primary actions
- Links for secondary actions
- One clear primary CTA per email
- Button text: Action + outcome

Detailed copy, personalization, and testing guidelines: [references/copy-guidelines.md](references/copy-guidelines.md).

---

## Output Format

### Sequence Overview

```
Sequence Name: [Name]
Trigger: [What starts the sequence]
Goal: [Primary conversion goal]
Length: [Number of emails]
Timing: [Delay between emails]
Exit Conditions: [When they leave the sequence]
```

### Per Email

```
Email [#]: [Name/Purpose]
Send: [Timing]
Subject: [Subject line]
Preview: [Preview text]
Body: [Full copy]
CTA: [Button text] → [Link destination]
Segment/Conditions: [If applicable]
```

### Metrics Plan
What to measure and benchmarks.

---

## Task-Specific Questions

1. What triggers entry to this sequence?
2. Primary goal / conversion action?
3. What do they already know about you?
4. What other emails are they receiving?
5. Current email performance?

---

## Tool Integrations

See the [tools registry](../../tools/REGISTRY.md). Key email tools:

| Tool | Best For | MCP | Guide |
|------|----------|:---:|-------|
| **Customer.io** | Behavior-based automation | - | [customer-io.md](../../tools/integrations/customer-io.md) |
| **Mailchimp** | SMB email marketing | ✓ | [mailchimp.md](../../tools/integrations/mailchimp.md) |
| **Nitrosend** | AI-native email (sequences via prompts) | ✓ | [nitrosend.md](../../tools/integrations/nitrosend.md) |
| **Resend** | Developer-friendly transactional | ✓ | [resend.md](../../tools/integrations/resend.md) |
| **SendGrid** | Transactional email at scale | - | [sendgrid.md](../../tools/integrations/sendgrid.md) |
| **Kit** | Creator/newsletter focused | - | [kit.md](../../tools/integrations/kit.md) |

---

## Related Skills

- **iblai-marketing-lead-magnets**: Lead magnets that feed nurture sequences
- **iblai-marketing-churn-prevention**: Cancel flows, save offers, dunning (email supports this)
- **iblai-marketing-onboarding-cro**: In-app onboarding (email supports this)
- **iblai-marketing-copywriting**: Landing pages emails link to
- **iblai-marketing-ab-test-setup**: Testing email elements
- **iblai-marketing-popup-cro**: Email capture popups
- **iblai-marketing-revops**: Lifecycle stages that trigger email sequences
