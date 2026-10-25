---
name: cold-email-sequence
description: "Use this skill when you need a complete cold email sequence (cadence) for a campaign: \"write a 4-step outbound sequence\", \"build an email campaign for this segment\", \"plan the follow-ups\". Designs the number of steps, spacing and angle of each email so every touch adds something new, writes all emails with subject lines, defines when people leave the sequence, and sets the metrics that decide whether to keep, change or kill it."
license: MIT
metadata:
  title: Cold email sequence
  category: cold-email
  tags: "SDR, Founders, Sales, Agencies"
  author: prosyo
  version: "1.0.0"
  keywords: "cold email sequence template, outbound email cadence, b2b email sequence, claude email sequence skill, 4 step cold email sequence"
  inputs: "Segment and persona, Offer and proof points, Campaign goal"
  outputs: "Full sequence with timing, All emails and subject lines, Exit rules, Success metrics"
---

Use this to build a whole campaign rather than one email. It produces a sequence where each step has its own angle, so follow-ups add value instead of saying "just bumping this".

## Inputs

- Segment, persona and the problem the campaign is about.
- Approved proof: customer stories, numbers, assets you can share.
- Goal: meetings, replies to a question, sign-ups.

## The play

### 1. Set the shape
The default for cold B2B is 4 emails over about 14-18 days:

| Step | Day | Angle | Length |
| --- | --- | --- | --- |
| 1 | 0 | Observation → problem → proof → ask | 50-90 words |
| 2 | 3 | New angle: a different pain or a sharper insight | 40-70 words, same thread |
| 3 | 7-8 | Proof: a short customer story or a useful asset | 60-90 words, new thread |
| 4 | 14-16 | Close the loop: a polite final note, easy out | 25-50 words |

Add LinkedIn or phone steps between emails when the channel fits the persona; the multichannel cadence covers that.

### 2. Give each step one job
No step repeats the previous one. Every follow-up must stand alone: many people only ever see one of the emails. Read [references/sequence-example.md](references/sequence-example.md) for a full annotated 4-step example and step-by-step variations.

### 3. Thread deliberately
Step 2 replies in the same thread (it reads as a natural follow-up). Step 3 starts a new thread with a new subject, which gives a second chance at the inbox. Step 4 can go either way.

### 4. Define exits
People leave the sequence when they reply (any reply, including out-of-office with a return date: pause, not stop), book, bounce, opt out, or when anyone at the same account books a meeting.

### 5. Set the scorecard
Judge after 150-300 contacts per variant:

| Metric | Healthy | Action if below |
| --- | --- | --- |
| Bounce rate | under 2% | Stop; clean the list |
| Reply rate | 5%+ | Rework angle or targeting |
| Positive reply rate | 1.5-3%+ | Rework offer and ask |
| Meetings per 100 contacts | 1+ | Check reply handling speed |

## What good looks like

- Step 3 could be someone's first email and still make sense.
- No "just following up", "bumping this to the top", or "did you see my last email".
- The final email is gracious and gets replies in its own right: "not a priority" answers are useful data.
- The common mistake is seven emails with the same pitch reworded; volume of touches without new value burns the list.

## Rules

- MUST give every step a distinct angle.
- MUST stop the sequence on reply, booking, bounce or opt-out.
- MUST pause, not continue, when an out-of-office names a return date.
- NEVER send more than 5 cold emails to one person in a sequence.
- NEVER guilt-trip in follow-ups.

## Example prompts

- "Write a 4-step sequence for Heads of Finance at 200-1,000 person SaaS companies. Problem: month-end close takes too long."
- "Turn this single cold email into a full sequence."
- "Our sequence gets replies on step 1 only. Rewrite steps 2-4."
