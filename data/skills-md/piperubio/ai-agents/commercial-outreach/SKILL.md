---
name: commercial-outreach
description: >
  Generate personalized multi-channel outreach sequences (email, LinkedIn) for
  B2B technology consulting sales. Produces sequences tailored to consulting
  tone — offering strategic conversations, assessments, and diagnostics rather
  than product demos. Use when launching outreach campaigns, crafting cold
  emails, designing LinkedIn messaging sequences, or re-engaging dormant
  prospects.
---

# Commercial Outreach — B2B Consulting Sales

## Purpose

Generate personalized, multi-touch outreach sequences for technology consulting
prospects. Position the sender as a strategic advisor, NOT a product seller.
Outreach must offer value (assessments, insights, benchmarks) rather than
request demos or meetings.

### Key Differentiation from SaaS Outreach

- Lead with insight, not features.
- Offer a diagnostic/assessment as the CTA, not a demo.
- Position as peer advisor, not vendor.
- Reference industry-specific challenges, not generic pain.
- Tone: executive, consultative, non-pushy.

## Inputs

- **prospect-profile.md** — from `commercial-prospecting` skill.
- **commercial-state.md** — pipeline context.
- **user_input** — campaign parameters (channel, intensity, specific messaging angle).

## Outputs (contract)

### 1. New File: `outreach-sequence.md` (per prospect)

Contents:

- **Sequence overview**: channel, number of touches, timing, objective.
- **5–7 touch sequence**, each touch containing:
  - Timing (day number)
  - Channel (email / LinkedIn / phone)
  - Subject line or hook
  - Full message body
  - CTA
- **A/B variants** for emails 1 and 3.
- **Breakup email** (final touch).
- **Personalization tokens** highlighted — what to customize per recipient.
- **Follow-up triggers** — what response warrants which next step.

### 2. Updated: `commercial-state.md`

Log outreach activity in the opportunity's entry.

## Sequence Framework (7-touch default)

| Touch | Day  | Channel  | Purpose |
|-------|------|----------|---------|
| 1     | 0    | Email    | Value-first — share insight relevant to their industry/challenge |
| 2     | 3    | LinkedIn | Connection request with personalized note |
| 3     | 7    | Email    | Different angle — reference a relevant case or benchmark |
| 4     | 10   | LinkedIn | Engage with their content or share relevant article |
| 5     | 14   | Email    | Offer a free mini-assessment or diagnostic |
| 6     | 21   | Phone    | Voicemail attempt (script provided) |
| 7     | 28   | Email    | Breakup — respectful close, leave door open |

For full templates by service line, subject line formulas, response handling,
and timing guidance, see [references/sequence-templates.md](references/sequence-templates.md).

## Guardrails

1. NEVER use aggressive or pushy sales language.
2. NEVER mention pricing in outreach — the goal is to earn a conversation.
3. Every email must provide standalone value (insight, data point, benchmark).
4. Personalization must go beyond `{{first_name}}` — reference specific company context.
5. All CTAs must be low-commitment (15-min call, not a "sales meeting").
6. Breakup email must be genuinely respectful, not passive-aggressive.
7. LinkedIn messages must be shorter than emails (max 300 chars for connection requests).

## Example

**Touch 1 — Value-first email (Day 0)**
Target: VP of Operations at a logistics company considering data platform modernization.

> **Subject**: Observation about {Company}'s fleet data challenge
>
> Hi {First_Name},
>
> I noticed {Company} is expanding into last-mile delivery — that usually
> surfaces real friction in how fleet telemetry and route-optimization data
> flow through legacy systems.
>
> We recently helped a mid-market logistics firm cut their data-pipeline
> latency by 60 % during a similar expansion. The bottleneck wasn't where
> they expected.
>
> Would a 15-minute call to swap notes be worth your time? Happy to share
> what we found — no strings attached.
>
> Best,
> {Sender}

**Touch 7 — Breakup email (Day 28)**

> **Subject**: Closing the loop
>
> Hi {First_Name},
>
> I've reached out a few times and haven't heard back — completely
> understand; timing is everything.
>
> If modernizing {Company}'s data platform becomes a priority down the road,
> I'd welcome the conversation. Until then, wishing you and the team the
> best with the last-mile expansion.
>
> Best,
> {Sender}
