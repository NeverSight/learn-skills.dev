---
name: email-composer
description: "Draft professional emails for business and marketing contexts — outreach, client communication, proposals, follow-ups, and internal updates. Includes tone calibration, subject line formulas, and follow-up cadence recommendations."
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: content
  domain: email
  updated: 2026-03-13
  tested: 2026-03-17
  tested_with: "Claude Code v2.1"
---

# Email Composer

Draft professional emails for business and marketing contexts.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/email-composer ~/.claude/skills/
```

## Email Categories

### 1. Outreach & Prospecting
- Cold outreach (personalized, value-first)
- Warm introduction follow-ups
- Partnership proposals
- Speaking and podcast pitches

### 2. Client Communication
- Project kickoff
- Status updates and reports
- Scope change discussions
- Invoice and payment follow-ups
- Deliverable handoffs

### 3. Internal / Team
- Campaign briefs
- Performance recaps
- Cross-functional requests
- Meeting agendas and follow-ups

### 4. Sales & Proposals
- Proposal cover emails
- Pricing discussions
- Objection handling
- Contract and SOW follow-ups
- Win-back campaigns

## Structure Framework

Every email follows this structure:

```
Subject: [Specific, not generic — include key value or action]

[Opening — context in one sentence: why you are writing]

[Body — 2-3 short paragraphs max, bullet points for multiple items]

[CTA — one clear, specific ask]

[Sign-off — matched to relationship level]
```

## Tone Calibration

| Tone | Characteristics | When to Use |
|------|----------------|-------------|
| **Formal** | Complete sentences, no contractions, titles, "Dear..." | C-suite, legal, first contact with enterprise |
| **Professional** | Direct but warm, contractions OK, first names | Clients, colleagues, vendors |
| **Casual** | Conversational, personality OK, still clear | Internal team, close working relationships |
| **Urgent** | ACTION REQUIRED flag, bold deadlines, consequences | Time-sensitive, blocking issues |

## Subject Line Formulas

| Formula | Example |
|---------|---------|
| Action + Topic + Deadline | "Review: Q1 Campaign Brief by Friday" |
| Number + Benefit | "3 Quick Wins from Your GA4 Data" |
| Question | "Can we schedule 15 min to discuss the Shopify migration?" |
| Value + Context | "Your Klaviyo Audit Results (3 Revenue Opportunities)" |
| Urgency + Specificity | "Action needed: Tracking code missing from 4 pages" |

## Key Principles

1. **One email, one CTA.** Do not dilute with multiple asks.
2. **150 words max for most emails.** Respect the reader's time.
3. **Specific subject lines.** "Q4 Campaign Brief — Review by Friday" not "Update."
4. **Add value, not volume.** Never "just checking in" without new information.
5. **Active voice for CTAs.** "Can you review this by Thursday?" not "It would be great if this could be reviewed."
6. **Context first.** Recipient should know why they are reading within the first sentence.

## Anti-Patterns

- "Just checking in" without adding value
- Walls of text (>200 words for a simple ask)
- Passive voice CTAs ("It would be great if...")
- Multiple asks in one email
- Generic subject lines ("Update", "Quick question", "FYI")
- Marking everything as urgent
- Reply-all when only one person needs to respond
- Sending when emotional — draft, wait, re-read

For templates and follow-up cadence, see [REFERENCE.md](REFERENCE.md).

## Brand Context (Optional)

If `brand-profile.json` exists in the working directory, read it before composing emails. Use the `formal_casual` axis to set salutation and sign-off style, voice descriptors to guide subject line personality, and colors for email template accent recommendations. This profile is produced by the `brand-dna` skill.
