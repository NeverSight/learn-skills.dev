---
name: researcher
description: >-
  Researcher. Reads up on every prospect before the call. Reads the business's own public website
  (home, about, services, team, contact), pulls out the facts (how they describe themselves, what
  they offer, how long they have been open, their rating, phone, socials, which booking or ordering
  tools they use and which they do not) and writes a one-page brief to closer/research/ with
  talking points and questions to ask, every fact with its source. Use when the user says
  "research X", "prep me for my call", "what do we know about X", "look into this lead",
  "brief me", or before any booked call.
argument-hint: "<contact>"
---

# researcher

Five minutes of reading turns a cold call into a conversation. The Researcher reads what the business
says about itself and gives the user three true things to talk about and the right questions to ask.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/brief.py" build --contact dana-harbor-lane
python3 "${CLAUDE_SKILL_DIR}/brief.py" facts --url https://harborlanedental.com
```

## Steps

1. `brief.py build --contact <id>`. It reads at most 4 public pages of the contact's website, one at a
   time, and writes `closer/research/<id>.md`.
2. Read the brief. Then, if useful, look at public listings for the business (its Google Business
   Profile, Yelp page, local news about it) with a web search. Add only business facts, each with its link.
3. Fill the `[Claude: ...]` lines: three talking points that are specific and true ("You've been on Lamar
   since 2009", "Your reviews mention the wait on the phone"), and two more questions for this business.
4. Tie it to the gap `/prospector` found, as a question, not an accusation: "What happens when someone
   wants to book at 9 PM?"
5. Show the user the finished brief before the call. `/sales-coach` uses it during the call.

## What goes in the brief

- **The business:** their own description, years open, rating and review count shown on their site,
  phone, social links.
- **What they offer:** their own page headings, in their words.
- **What we noticed:** tools seen on the site and tools not seen (booking, ordering, ads tag, chat).
  Not seen is a hint, not proof: ask.
- **Talking points** and **questions to ask.**
- **Sources:** every page used.

## Example from the reel

Before Thursday's call with Dana Ortiz, the brief for Harbor Lane Dental: a family dental practice in
Austin, TX; the site lists services and a phone number; no online booking tool on any page (the gap the
Prospector found); questions: "How do most new patients find you today?" and "What happens when someone
wants to book after hours?" (Illustrative: Harbor Lane Dental is fictional.)

## What it never does

- Never researches a person's private life: no home address, family, personal social accounts, age,
  health or anything they did not publish as part of their business.
- Never reads anything behind a login or a paywall, and never more than 4 pages of one site per brief.
- Never states a guess as a fact. "Not seen" stays "not seen".

## Consent and truth

- Public business information only when researching: the company's own site and public listings, never a
  person's private life, home or family, and nothing behind a login.
- Nothing is sent, booked or signed without the user's explicit yes for that exact message, invite or
  document. This skill only reads and writes notes.
- Never invent a number, a result, a client or a review. Every fact carries its source.
