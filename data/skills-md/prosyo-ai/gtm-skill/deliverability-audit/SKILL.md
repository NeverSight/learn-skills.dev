---
name: deliverability-audit
description: "Use this skill when cold emails land in spam or reply rates suddenly drop: \"audit my email deliverability\", \"why are my emails going to spam\", \"check my sending setup\", \"open and reply rates fell off a cliff\". Checks domain setup (SPF, DKIM, DMARC, tracking domain), sending volume and patterns, bounce and complaint rates, list quality, content risks and inbox placement, ranks the problems by impact, and produces a fix plan with a recovery timeline."
license: MIT
metadata:
  title: Deliverability audit
  category: deliverability
  tags: "RevOps, SDR, Founders, Agencies"
  author: prosyo
  version: "1.0.0"
  keywords: "cold email deliverability audit, emails going to spam fix, email deliverability checklist, claude deliverability skill, inbox placement"
  inputs: "Sending domains and mailboxes, DNS records, Campaign metrics, Sample emails"
  outputs: "Ranked problems, Fix plan, Recovery timeline, Monitoring checklist"
---

Use this when results drop and the copy has not changed. Most "the campaign stopped working" problems are deliverability problems: the emails are not being seen.

## Inputs

- Sending domains and the number of mailboxes on each.
- DNS records (SPF, DKIM, DMARC, MX) or permission to look them up.
- Metrics per mailbox: volume per day, bounce rate, reply rate, spam complaints, over the last 30-60 days.
- Two or three sample emails as sent.

## The play

### 1. Check authentication
SPF, DKIM and DMARC must exist, align with the From domain, and pass. Large mailbox providers require all three for bulk senders and reject or junk unauthenticated mail. Read [references/audit-checklist.md](references/audit-checklist.md) for the full checklist and what each failure looks like.

### 2. Check the domain strategy
- Cold email from the primary company domain risks the domain that carries invoices and customer mail. Use separate, aged sending domains that redirect to the main site.
- Each sending domain has 2-5 mailboxes, not 20.
- A custom tracking domain, or no open and click tracking at all for cold outreach.

### 3. Check volume and pattern
- Per mailbox: 30-50 cold emails a day after warm-up is a common safe range.
- Sending spread through the working day, not in one burst.
- Sudden jumps in volume (doubling overnight) are a common trigger for filtering.

### 4. Check list quality
Bounce rate over 2-3% means a list problem. Spam complaints over 0.1% (one in a thousand) are a red flag; 0.3% is the threshold large providers warn about. Old lists, purchased lists and catch-all-heavy lists are usual causes.

### 5. Check content
Links (especially link shorteners), images, attachments, tracking pixels, spam-pattern words and heavy HTML all add risk. Cold email should be plain text-looking with zero or one link.

### 6. Test placement
Send to a seed set of test inboxes across providers, or ask friendly contacts to check folders. Separate "inbox", "promotions or other" and "spam".

### 7. Rank and fix
Order fixes by impact: authentication failures and blacklisting first, then list quality, then volume, then content.

## Output format

```
Verdict: healthy / at risk / damaged
Problems (ranked): <issue - evidence - impact - fix>
Recovery plan: <week by week>
Monitor weekly: bounce %, complaint %, reply rate per mailbox, placement test
```

## What good looks like

- Diagnosis by mailbox and domain, not just campaign averages; one bad mailbox can hide inside a healthy average.
- The fix plan pauses damaged mailboxes rather than pushing more volume through them.
- The common mistake is rewriting copy for weeks while the real cause is a missing DMARC record or a 6% bounce rate.

## Rules

- MUST check authentication before content.
- MUST recommend pausing any mailbox with bounces over 5% or complaints over 0.3%.
- NEVER recommend tactics that disguise the sender or evade provider filters (hidden text, misleading headers, rotating look-alike domains to dodge complaints).
- NEVER change DNS records without the user's approval.

## Example prompts

- "Our reply rate went from 4% to 0.5% in two weeks. Audit our deliverability."
- "Here are our DNS records and per-mailbox stats. What's wrong?"
- "Build a deliverability checklist we run before every campaign."
