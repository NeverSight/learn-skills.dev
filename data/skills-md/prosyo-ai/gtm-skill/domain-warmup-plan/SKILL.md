---
name: domain-warmup-plan
description: "Use this skill when you set up new domains or mailboxes for cold email and need a warm-up plan: \"how do I warm up a new domain\", \"warm-up schedule for new inboxes\", \"how fast can I ramp sending\". Plans domain purchase and setup, a week-by-week warm-up and ramp schedule per mailbox, the health checks that gate each step up, and what to do when a mailbox shows trouble. Produces a ramp calendar and capacity forecast for the whole sending infrastructure."
license: MIT
metadata:
  title: Domain warm-up plan
  category: deliverability
  tags: "RevOps, SDR, Founders, Agencies"
  author: prosyo
  version: "1.0.0"
  keywords: "email domain warm up schedule, warm up new mailbox for cold email, inbox warm up plan, claude domain warmup skill, cold email infrastructure setup"
  inputs: "Target daily volume, Number of domains and mailboxes, Start date"
  outputs: "Setup checklist, Week-by-week ramp, Health gates, Capacity forecast"
---

Use this before sending any cold email from new domains or mailboxes. New senders have no reputation; ramping too fast is the most common way to burn a domain in its first month.

## Inputs

- Target cold volume per day across the team.
- Domains and mailboxes planned (or let the plan size them).
- Start date and when the first campaign needs to go out.

## The play

### 1. Size the infrastructure
Mailboxes needed = target daily cold volume ÷ 30-40 per mailbox. Domains needed = mailboxes ÷ 3. Add 20% spare capacity so a mailbox can rest without missing targets.

Example: 600 cold emails a day ÷ 30 = 20 mailboxes; ÷ 3 = 7 domains; plus spare = 24 mailboxes across 8 domains.

### 2. Set up correctly on day 0
- Domains close to the brand (variations of the company name), never misleading look-alikes of other brands.
- SPF, DKIM, DMARC published and passing; MX records set; domain redirects to the main site.
- Real sender names, photos, signatures.

### 3. Warm, then ramp
| Week | Warm-up emails per day | Cold emails per day | Gate to move on |
| --- | --- | --- | --- |
| 1 | 5-10, rising | 0 | Authentication passing |
| 2 | 15-20 | 0 | No spam placement in tests |
| 3 | 20-30 | 5-10 to best-fit verified contacts | Bounces < 2%, replies arriving |
| 4 | 20-30 | 15-20 | Bounces < 2%, complaints ~0 |
| 5 | 20-30 | 25-30 | Placement in inbox |
| 6+ | Keep 10-20 running | 30-40 | Weekly checks stay green |

Warm-up means real, two-way conversations with engaged inboxes. Keep a low level running while cold sending continues.

### 4. Gate every step
Never move up a week if bounces exceed 2%, any spam complaint arrives, or placement tests show spam. Hold the current level for another week instead.

### 5. Plan the capacity curve
Show when the team reaches full volume. Usually week 6. If the campaign must start sooner, start with fewer, better contacts rather than more volume.

## What good looks like

- First cold sends go to the cleanest, best-fit contacts, which builds reputation from real replies.
- The plan includes spare mailboxes and a resting rotation.
- The common mistake is buying ten domains on Monday and sending 50 a day from each by Friday.

## Rules

- MUST wait at least two weeks of warm-up before any cold sends.
- MUST gate each ramp step on bounce, complaint and placement checks.
- NEVER use domains that imitate another company's brand.
- NEVER exceed 50 cold emails per mailbox per day.

## Example prompts

- "We want to send 500 cold emails a day starting next month. Plan the domains, mailboxes and warm-up."
- "I just set up 3 new mailboxes. Give me a week-by-week ramp."
- "Our new domain got 4% bounces in week 3. What now?"
