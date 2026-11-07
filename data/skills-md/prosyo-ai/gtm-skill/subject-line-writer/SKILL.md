---
name: subject-line-writer
description: "Use this skill when you need cold email subject lines that get opened and do not look like marketing: \"write subject lines for this email\", \"my open rates are low\", \"A/B test subject lines\". Writes short, lowercase, internal-looking subject lines matched to the email's angle, explains the pattern behind each, flags spam and clickbait risks, and sets up a fair subject-line test. For cold outreach, follow-ups and re-engagement emails."
license: MIT
metadata:
  title: Subject line writer
  category: cold-email
  tags: "SDR, Founders, Marketing"
  author: prosyo
  version: "1.0.0"
  keywords: "cold email subject lines, b2b subject line generator, subject lines that get opened, claude subject line skill, email subject line ideas"
  inputs: "The email body, Persona, Trigger or angle"
  outputs: "Subject line options by pattern, Risk notes, Test plan"
---

Use this after the email is written. The subject line's job is to get the email opened by the right person without promising something the body does not deliver.

## Inputs

- The email body (subject lines are written for a specific email, never in a vacuum).
- The persona and seniority.
- The trigger or angle the email uses.

## The play

### 1. Write in the patterns that work for cold B2B
| Pattern | Example | When |
| --- | --- | --- |
| Topic, two to four words | "month-end close" | Default |
| Trigger reference | "new sdr team", "the series b" | Email leads with a trigger |
| Peer or customer | "contoso's close" | Strong, approved proof |
| Question | "manual reconciliations?" | Pain is very common |
| Their initiative | "europe expansion" | Announced plan |
| Mutual context (only if real) | "maria suggested i reach out" | Genuine referral |

### 2. Follow the format rules
- 1 to 5 words; under 40 characters so it is not cut on phones.
- Lowercase or sentence case; it should look like it came from a colleague.
- No first-name merge field in the subject (it reads as automated), no emojis, no exclamation marks, no "quick question".
- The subject must be true to the email. Clickbait wins opens and loses replies and trust.

### 3. Give options per pattern
Return 2-3 options for 3 patterns. Mark the recommended one.

### 4. Test fairly
- Change only the subject; keep body, list and send time the same.
- At least 200 sends per variant before judging.
- Judge on reply rate, not opens. Open tracking is unreliable: privacy features pre-load images and inflate opens, and many teams disable tracking pixels to protect deliverability.

## Output format

```
Recommended: <subject>
Topic: <3 options>
Trigger: <3 options>
Question: <3 options>
Avoid: <any risky phrasing found and why>
Test: A = <..>, B = <..>, judge on reply rate after 200+ sends each
```

## What good looks like

- Reads like a peer's email in a crowded inbox.
- Connects directly to the first line of the email.
- No spam-pattern words: "free", "guarantee", "act now", "limited time", percentages off.
- The common mistake is clever or vague subjects ("thoughts?", "a crazy idea") that get opened out of curiosity and then deleted with irritation.

## Rules

- MUST keep subject lines under 40 characters.
- MUST match the subject to the email's actual content.
- NEVER use fake reply or forward prefixes ("Re:", "Fwd:") on a first email.
- NEVER use a referral subject unless the referral is real.

## Example prompts

- "Write subject lines for this cold email to CFOs."
- "Give me 10 subject lines for a follow-up that shares a case study."
- "Set up a subject line test for our new campaign."
