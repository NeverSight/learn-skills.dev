---
name: linkedin-connection-note
description: "Use this skill when you need LinkedIn connection request notes that get accepted: \"write a connection note\", \"my acceptance rate is low\", \"connect with prospects without being salesy\". Writes short notes under the character limit built on a real reason to connect (shared topic, trigger, community, event or their content), with no pitch, and gives variants for cold prospects, event attendees, post engagers and referrals. Includes when to send no note at all."
license: MIT
metadata:
  title: LinkedIn connection note
  category: linkedin
  tags: "SDR, Founders, Sales, Agencies"
  author: prosyo
  version: "1.0.0"
  keywords: "linkedin connection request message, linkedin connection note examples, increase linkedin acceptance rate, claude linkedin connection skill, linkedin invite message"
  inputs: "Prospect profile, Reason to connect, Your role"
  outputs: "Connection note variants, No-note recommendation where better"
---

Use this for the first step of LinkedIn outreach. The note has one job: get accepted by giving a genuine reason to connect. Selling comes later, and only if the conversation earns it.

## Inputs

- The prospect: name, role, company, recent activity.
- The reason to connect: shared topic, trigger, event, community, mutual connection, their content.
- Who you are, in a few words.

## The play

### 1. Find the reason
| Reason | Strength | Note pattern |
| --- | --- | --- |
| Referral from a mutual connection | Strongest | "Sam suggested we connect about..." (only if true) |
| They engaged with your content | Strong | "Thanks for your comment on..." |
| Same event or community | Strong | "Saw you're at <event> next week too..." |
| Their content | Strong | "Your post on <specific point>..." |
| Role or industry peer | Medium | "I work with a lot of <role>s in <industry>..." |
| Trigger (new role, hiring) | Medium | "Congrats on <role>, <specific note>" |

### 2. Write the note
- Under 200 characters; shorter is usually better. Free accounts may have a lower limit and a monthly cap on notes, so check yours.
- One reason, one sentence about it, no ask beyond the connection.
- No links, no product, no "I'd love to tell you about".

### 3. Decide whether to send a note at all
For senior executives with no real hook, and for people who post a lot and connect openly, a blank request often performs as well or better. Test both on 100+ requests before deciding.

### 4. Plan the first message after acceptance
Write it now, so acceptance leads into a conversation within 1-3 days while you are still recognised.

## Examples

- Content: "Your post on why SDR ramp is a data problem made me rethink our onboarding. Would be good to connect."
- Event: "See you're at the RevOps summit next week, I'll be there too. Happy to connect beforehand."
- Peer: "I spend most of my week with heads of ops at multi-site restaurant groups. Would be good to have you in my network."
- New role: "Congrats on the move to Fabrikam. Building ops from scratch at that stage is a fun problem."

## What good looks like

- Acceptance rate of 30-50% on a targeted list. Under 20% means the targeting or the note is wrong.
- Nothing in the note could be called a pitch.
- The common mistake is the "pitch in the invite": a note that ends in "would love to show you how we help companies like yours".

## Rules

- MUST stay under the character limit of the user's account.
- MUST use a real reason; never invent a mutual connection, event or shared interest.
- NEVER pitch or include links in a connection note.
- NEVER exceed safe daily invitation volumes (typically 15-25 per day per account).

## Example prompts

- "Write connection notes for these 25 VPs of Sales. Most have posted about hiring."
- "My acceptance rate is 12%. Rewrite my note."
- "Write notes for people attending the same conference as me."
