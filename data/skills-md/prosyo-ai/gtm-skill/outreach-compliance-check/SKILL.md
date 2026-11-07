---
name: outreach-compliance-check
description: "Use this skill when you need to check that cold email or LinkedIn outreach follows privacy and anti-spam rules before it goes out: \"is this campaign GDPR compliant\", \"CAN-SPAM checklist\", \"can we email people in the EU\", \"check our cold outreach for compliance\". Checks the audience, lawful basis, data source, sender identity, opt-out, frequency and record keeping by region, flags what must change, and produces a pass/fix report. A practical checklist, not legal advice."
license: MIT
metadata:
  title: Outreach compliance check
  category: deliverability
  tags: "RevOps, Founders, Marketing, Agencies"
  author: prosyo
  version: "1.0.0"
  keywords: "cold email gdpr compliance, can spam checklist b2b, cold outreach compliance, claude compliance skill, b2b email privacy rules"
  inputs: "Campaign and audience regions, Data source, Email and message copy"
  outputs: "Pass/fix report by region, Required changes, Record-keeping checklist"
---

Use this before a campaign reaches people in a new region, or when a list comes from a new source. It is a practical pre-flight check; for anything unclear or high-risk, the user should ask their own legal counsel.

## Inputs

- Audience: which countries, B2B or consumer, job roles.
- Where the data came from and what the source says about permitted use.
- The emails and messages as they will be sent.
- How opt-outs and records are handled today.

## The play

### 1. Sort the audience by region
Rules differ. Typical buckets:

| Region | Common baseline for B2B cold email |
| --- | --- |
| United States | Allowed with honest headers and subject, a physical address, a working opt-out honoured promptly |
| EU and UK | Usually relies on legitimate interest for business contacts: relevant offer, role-based targeting, clear identity, easy opt-out, ability to say where the data came from |
| Canada | Stricter consent rules; business-to-business exceptions are narrow |
| Australia and others | Check local rules; consent expectations vary |

Read [references/compliance-checklist.md](references/compliance-checklist.md) for the full checklist per region.

### 2. Check the data source
The source must allow the use, be recent, and be explainable to the recipient if they ask. Personal email addresses and consumer data raise the bar sharply.

### 3. Check relevance
For legitimate-interest outreach, the message must be relevant to the person's job. A finance tool to a CFO passes; the same email to a list of every employee does not.

### 4. Check the message
Real sender name and company, an honest subject, a physical address where required, and a simple opt-out in every commercial email. No misleading "Re:" or "Fwd:" subjects.

### 5. Check operations
Opt-outs honoured across all mailboxes and channels; suppression lists shared; records of source, date and basis kept; a process to answer "where did you get my data?" and deletion requests.

## Output format

```
Region | Audience | Verdict (pass / fix / do not send) | Issues | Required changes
Records to keep: <list>
Open questions for counsel: <list>
```

## What good looks like

- Each region gets its own verdict; one rule is not applied everywhere.
- Every "fix" has a concrete change.
- High-risk cases (consumer data, sensitive sectors, unclear sources) are sent to counsel, not guessed.
- The common mistake is assuming "it's B2B, so anything goes", which ignores regional rules and the recipient's right to object.

## Rules

- MUST state that this is a checklist, not legal advice, when the stakes are high.
- MUST require a working opt-out and identity in every commercial email.
- NEVER approve outreach to data of unknown or unlawful origin.
- NEVER suggest hiding the sender, the source or the commercial nature of a message.

## Example prompts

- "We're emailing 2,000 operations leaders in Germany and the UK. Run a compliance check."
- "Check this cold email and our opt-out process against US and EU rules."
- "Build a pre-send compliance checklist for our SDR team."
