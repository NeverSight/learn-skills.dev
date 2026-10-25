---
name: multichannel-cadence
description: "Use this skill when you need an outbound cadence that combines email, LinkedIn, phone and video so each touch builds on the last: \"build a multichannel sequence\", \"combine email and LinkedIn outreach\", \"plan a 3-week cadence for Tier 1 accounts\". Chooses channels by persona and tier, orders and spaces the touches, writes the connecting thread across channels, sets daily capacity and exit rules, and produces a day-by-day cadence ready to load into any sequencing tool."
license: MIT
metadata:
  title: Multichannel cadence
  category: multichannel
  tags: "SDR, Sales, Founders, Sales Leaders"
  author: prosyo
  version: "1.0.0"
  keywords: "multichannel outreach cadence, email and linkedin sequence, omnichannel prospecting, claude multichannel skill, sales cadence template"
  inputs: "Persona and tier, Available channels, Offer and proof"
  outputs: "Day-by-day cadence, Copy per touch, Capacity plan, Exit rules"
---

Use this when one channel is not enough. Prospects who see you in two or three places in a short window remember you; the trick is making the touches feel like one conversation rather than an ambush.

## Inputs

- Persona and tier.
- Channels available and the sender's capacity per day on each.
- Offer, proof and the campaign's central problem.

## The play

### 1. Choose channels by persona
| Persona | Lead channel | Support channels |
| --- | --- | --- |
| Founders, small companies | LinkedIn | Email |
| Sales and marketing leaders | LinkedIn and email | Video |
| Finance, operations, IT | Email | Phone |
| Field and frontline managers | Phone | Email, text where lawful and consented |
| Enterprise executives | Email via champion or referral | LinkedIn, direct mail |

### 2. Scale effort by tier
- **Tier 1**: 10-14 touches over 3-4 weeks, 3-4 channels, 1:1 personalization.
- **Tier 2**: 7-9 touches over 3 weeks, 2-3 channels, segment copy plus a personal line.
- **Tier 3**: 4-6 touches over 2-3 weeks, 1-2 channels, segment copy.

### 3. Order the touches
Start where trust is cheapest: a LinkedIn profile view or connection request before the first email makes the email's sender name familiar. Calls work best right after an email ("I sent you a note on Tuesday about..."). Read [references/cadence-templates.md](references/cadence-templates.md) for day-by-day templates per tier.

### 4. Thread the story
Every touch references the same problem from a new angle: the email names the problem, the LinkedIn message asks a question about it, the call follows up on the email, the video shows a 30-second example.

### 5. Plan capacity
Count touches per day per sender across all active prospects. A Tier 1 cadence for 50 new accounts a week can mean 80+ tasks a day; cut the number of new accounts before cutting quality.

### 6. Exit rules
Any reply on any channel stops every automated step on every channel. Bookings at the account stop all cadences at that account.

## What good looks like

- A prospect who replies says "I saw your note on LinkedIn too", not "why are you messaging me everywhere?".
- Channel order makes each touch easier: connection, then email, then call referencing the email.
- Task load per rep is realistic and finished daily.
- The common mistake is running separate email and LinkedIn campaigns that each think they own the prospect, sending two unrelated first messages on the same day.

## Rules

- MUST stop all channels on a reply in any channel.
- MUST keep each channel inside its safe daily limits.
- MUST respect calling and texting consent rules for the region.
- NEVER send the same message copy across channels.

## Example prompts

- "Build a 3-week multichannel cadence for Tier 1 CFO accounts: email, LinkedIn and phone."
- "We have email and LinkedIn only. Design Tier 2 and Tier 3 cadences."
- "How many new accounts a week can 2 SDRs handle on this cadence?"
