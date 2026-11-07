---
name: email-copy-review
description: "Use this skill when you want an honest review of outreach copy before sending: \"roast my cold email\", \"review this sequence\", \"why is nobody replying\", \"score my email\". Scores the email on relevance, clarity, proof, ask, length and deliverability risk, quotes the exact lines that hurt, explains why from the reader's point of view, and returns a rewritten version. Works for cold emails, LinkedIn messages and whole sequences."
license: MIT
metadata:
  title: Email copy review
  category: cold-email
  tags: "SDR, Founders, Sales Leaders, Agencies"
  author: prosyo
  version: "1.0.0"
  keywords: "cold email review, roast my cold email, email copy feedback, claude email review skill, cold email grader"
  inputs: "The email or sequence, Target persona, Goal"
  outputs: "Scorecard, Line-by-line notes, Rewrite"
---

Use this before a campaign goes out, or when results are poor. It produces a scorecard, exact line-level fixes and a rewrite, judged from the reader's side of the inbox.

## Inputs

- The email, message or full sequence.
- Who it is for and what it should achieve.
- Results so far, if any.

## The play

### 1. Read it as the recipient
A busy person on a phone, between meetings, who has never heard of you. Note the moment you would stop reading.

### 2. Score six dimensions
Score each 1-5 using [references/review-rubric.md](references/review-rubric.md):

| Dimension | Question |
| --- | --- |
| Relevance | Is it clearly about my situation? |
| Clarity | Do I understand what they do and why it matters to me in one read? |
| Proof | Is there a specific, believable reason to trust the claim? |
| Ask | Is the next step easy and low-commitment? |
| Brevity | Is every sentence earning its place? |
| Deliverability | Does anything look like spam or marketing? |

### 3. Quote and fix
For every issue, quote the exact line, say why it hurts from the reader's side, and give the replacement. Prioritise: fix the top three issues first; polishing a weak angle is wasted effort.

### 4. Rewrite
Return a rewritten version that keeps the sender's offer and proof. Show the word count before and after.

### 5. Diagnose results (if provided)
| Symptom | Most likely cause |
| --- | --- |
| High bounce | List quality, not copy |
| Low replies, few opt-outs | Weak relevance or targeting |
| Replies mostly negative | Offer or ask mismatch, or wrong persona |
| Positive replies but few meetings | Slow or weak reply handling |
| Spam complaints | Volume, targeting or misleading subject |

## Output format

```
Score: <total>/30  |  Verdict: send / fix first / rewrite
Top 3 issues: <quoted line - why - fix>
Other notes: <short>
Rewrite (<words before> → <words after>):
<email>
```

## What good looks like

- Feedback quotes the email; it never says "make it more personal" without showing how.
- Honest but useful: "this reads like a brochure" is followed by the line that proves it and a better line.
- The review separates copy problems from list and deliverability problems.
- The common mistake is rewriting the whole thing in the reviewer's voice and losing the sender's facts and proof.

## Rules

- MUST quote the exact line for every criticism.
- MUST keep the sender's facts, offer and proof in the rewrite.
- NEVER add claims, numbers or customers the sender did not provide.

## Example prompts

- "Roast this cold email. Be brutal but useful."
- "Review our 4-step sequence; replies dropped to 1%."
- "Score these three variants and tell me which to send."
