---
name: outreach-writer
description: Write personalized cold emails, LinkedIn connection requests, pre-demo emails, and warm intro requests. Use when the user needs to write outreach to a prospect, craft a LinkedIn message, or send a pre-meeting email.
license: MIT
compatibility: Requires internet access for prospect research.
metadata:
  author: toughtongueai
  version: "1.0"
---

# Outreach Writer

Write personalized outreach messages — cold emails, LinkedIn connection requests, pre-demo emails, and warm intro templates. Every message is grounded in research and customized to the user's product positioning.

## When to Use

- User says "write an email to [name] at [company]"
- User needs a LinkedIn connection request or InMail
- User wants a pre-demo email to send before a scheduled call
- User needs a warm intro request to send through a mutual connection
- User asks to write any prospecting or sales communication

## Required Inputs

Ask the user for:

```
Prospect: [Name, title, company]
Outreach Type: [Cold email / LinkedIn connection / Pre-demo email / Warm intro request]
Context: [Why are you reaching out? Any shared connection or trigger event?]
```

If the user just says "write an email to Sarah at Acme," research first, then ask which type of outreach they need.

## Process

### 1. Load Context

Read `company-profile.md` for the user's product positioning, differentiators, and background.

### 2. Research the Prospect

If not already done, use the `research-prospect` process to gather company and contact intelligence. You need at minimum:
- What the prospect's company does
- The contact's role and background
- A personalization hook

### 3. Generate the Message

Use the appropriate template based on outreach type. See [Email Best Practices](references/email-best-practices.md) for style rules.

## Output Formats

### Cold Email

```
Subject: [Short, specific, curiosity-driving — no clickbait]

Hi [First Name],

[HOOK — 1 sentence. Reference something specific: a recent post, a trigger event, a shared connection, or a specific observation about their business.]

[BRIDGE — 1-2 sentences. Connect their situation to the problem you solve. Don't pitch features — describe the outcome.]

[CTA — 1 sentence. One clear ask: a 15-minute call, permission to send a demo, or a yes/no question.]

[Sign-off],
[User Name]
[Title, Company]
```

**Rules:**
- Under 100 words in the body
- No more than 3 sentences before the CTA
- The subject line should make them want to open, not summarize the email
- Never lead with "I" — lead with them

### LinkedIn Connection Request

**Hard constraint: 300 characters maximum.**

```
Hi [First Name],

[SHARED HOOK — if applicable: "Fellow [school] alum" / "Ex-[company] here too"]. [VALUE — one sentence about what you do and why it's relevant to them]. [ASK — "Would love your perspective" or "Worth 15 min?"]

[User First Name]
```

**Priority for opening hooks:**
1. Shared school → "Fellow [school] alum here"
2. Shared company → "Ex-[company] here too"
3. Shared connection → "We both know [name]"
4. Trigger event → "Congrats on [event]"
5. No hook → Skip, start with value

**Always provide the character count** so the user knows it fits.

### LinkedIn InMail / DM (Longer)

```
Hi [First Name],

[HOOK — shared connection or observation about their company. 1-2 sentences.]

[CONTEXT — what you're building and why it's relevant to them. 2-3 sentences. Be specific about their business, not generic.]

[CTA — clear next step. Calendar link or simple question.]

[Sign-off]
```

### Pre-Demo Email

Send 24-48 hours before a scheduled call. Purpose: prime them to come prepared.

```
Subject: Quick ask before our call, [Name]

Hi [Name],

Looking forward to [day/time].

Quick ask: think about [the ONE challenge relevant to your product that their team faces]. Come ready to describe it in a few sentences.

I'll show you how we approach it — and I've already put together some initial thoughts for [Company].

Feel free to bring anyone who'd find this useful.

See you then,
[User Name]
```

### Warm Intro Request

Send to a mutual connection who can introduce you.

**Message to your contact (casual, WhatsApp/text style):**

```
Hey [Connector Name], quick favor.

You know [Prospect Name] at [Company] right? I'm building [one sentence about your product] that could be relevant for them — [one sentence about why].

Could you intro me? I've written a quick blurb below you can forward.
```

**Forwardable blurb (for the connector to send):**

```
Hey [Prospect Name],

Wanted to connect you with [User Name] — [brief credibility: "ex-Google PM" / "fellow IITD alum" / "founder of [Company]"].

[They're building / Their company does] [one sentence about the product and why it's relevant to Prospect's company].

[User Name] mentioned [Company] would be a strong fit because [specific reason]. Worth a 15-min chat?

[Calendar link if appropriate]
```

## Follow-Up Messages

### No Response After 7 Days

```
Hi [Name], following up on my note about [topic]. Worth 15 minutes, or should I check back later?
```

### No Response After 14 Days

```
Hi [Name], last one — just [shipped a new feature / published something relevant / got results with a similar company]. Quick demo relevant, or shall I close the loop?
```

### They Reply With Interest

```
Great to hear! Here's [a quick demo / a link to try it / my calendar]: [URL]

Happy to answer any questions.
```

### They Reply "Not Right Now"

```
Totally understand. Mind if I check back in [3 months]? Also, is there someone else on the team who handles [relevant area] I should connect with?
```

## Output Format

When generating outreach, provide:

```markdown
## Outreach: [Name] @ [Company]

**Type:** [Cold email / LinkedIn / Pre-demo / Warm intro]
**Personalization hook:** [What you're using]

**Message:**

\```
[The actual message in a code block for easy copying]
\```

**Character count:** [For LinkedIn only]
**Subject line alternatives:** [2-3 options for emails]
```

## Instructions

1. **Always research first.** A generic "I noticed your company does X" is worse than no personalization. Be specific.
2. **Read `company-profile.md`.** Your pitch should use the user's actual differentiators and positioning.
3. **Keep it short.** Cold emails under 100 words. LinkedIn requests under 300 characters. Respect their time.
4. **Be curious, not salesy.** Frame as asking for their perspective, not pitching value. "Would love your feedback" beats "Let me show you how we can help."
5. **One CTA only.** Don't give them three options. Give them one clear action.
6. **Output in code blocks.** So the user can copy-paste directly.
7. **Provide subject line alternatives.** The subject line is 50% of whether they open the email.
