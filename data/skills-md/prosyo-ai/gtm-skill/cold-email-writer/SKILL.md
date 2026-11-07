---
name: cold-email-writer
description: "Use this skill when you need to write a B2B cold email that gets replies: \"write a cold email to a VP of Sales\", \"draft outreach for this prospect\", \"my cold emails get no replies\". Builds the email from the prospect's situation, one pain, one proof point and one low-friction ask, keeps it under 100 words, and returns three variants with different angles plus subject lines. Works for one-to-one emails and for segment templates with personalization slots."
license: MIT
metadata:
  title: Cold email writer
  category: cold-email
  tags: "SDR, Founders, Sales, Agencies"
  author: prosyo
  version: "1.0.0"
  keywords: "cold email writer, ai cold email generator, b2b cold email template, claude cold email skill, write cold email that gets replies"
  inputs: "Prospect or segment, Offer and proof points, Research or trigger"
  outputs: "Three email variants, Subject lines, Why each angle works"
---

Use this for the first email to someone who has never heard of you. It produces three short variants, each built on a different angle, so the sender can choose or test.

## Inputs

- Who: the prospect or segment, their role and company.
- Why now: a trigger or research hook, if any.
- What: the offer in one outcome sentence, plus approved proof (a customer, a number, a before and after).

## The play

### 1. Pick one problem
The email is about one problem the reader probably has. Not three benefits, not the product tour. If you cannot name the problem in the reader's words, go back to research.

### 2. Use the four-part frame
1. **Observation** (why them, why now): the trigger or a sharp role insight. One sentence.
2. **Problem**: what that situation usually causes. One or two sentences.
3. **Proof**: a peer who solved it, with a concrete result. One sentence.
4. **Ask**: low-friction, interest-based. "Worth a look?" beats "Do you have 30 minutes Tuesday at 2pm?"

Read [references/cold-email-frameworks.md](references/cold-email-frameworks.md) for alternative frames, annotated examples and the line-by-line edit checklist.

### 3. Write three angles
Typical set: a trigger angle, a pain angle and a peer-proof angle. Each variant is a real alternative, not the same email with synonyms.

### 4. Edit hard
- Under 100 words; 50-80 is the sweet spot.
- Reading level of a smart 12-year-old: short words, short sentences.
- "You" and "your" outnumber "we" and "our".
- No attachments, no images, at most one link (better: none in the first email).
- Read it on a phone. If it needs scrolling, cut.

### 5. Subject lines
Two to four words, lowercase, looks like an internal email: "ramp time", "new sdr team", "question about payroll". Give three per variant.

## Output format

```
Variant A - <angle>
Subject options: <3>
<email>
Why it works: <one line>
```

Repeat for B and C, then a note on which to send first and why.

## What good looks like

- The first line could only be sent to this person or segment.
- The reader understands what you do without a feature list.
- The ask can be answered with one word.
- The proof is specific and approved: a named customer or a precise number, never "leading companies".
- The common mistake is starting with yourself ("I'm X from Y and we...") and ending with a 30-minute meeting request from a stranger.

## Rules

- MUST keep the email under 100 words.
- MUST use only approved proof points.
- NEVER fake familiarity ("Hope you're well", "As we discussed", "Re:" on a first email).
- NEVER invent personalization; use a role-level opener when research found nothing.
- NEVER use spam-trigger formatting: all caps, multiple exclamation marks, "free", "guarantee".

## Example prompts

- "Write a cold email to Dana Kim, Head of SDR at Lumen. They're hiring 4 SDRs. We sell AI list building."
- "Write a segment template for VPs of Operations at 3PLs, with one personalization slot."
- "Our emails get 0.5% replies. Rewrite this one."
