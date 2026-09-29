---
name: decision-summary
description: Summarise what has been decided so far, in plain words, from two angles, what the user will get and how it works. Use when the user asks for a summary, a recap, or "what did we decide", during or after a brainstorm or a plan discussion. It is a capability, not a phase; it changes nothing and the discussion can carry on after it.
argument-hint: "[topic, or blank for the current discussion]"
allowed-tools: Read, Grep, Glob
---

# Decision Summary

A discussion that ran long, with options raised, rejected and revived, leaves its owner holding
the pieces rather than the picture. This skill hands them the picture: everything decided so far,
in words they would use themselves, seen from what they will get and from how it will work.

**It is not a step in the workflow.** It gates nothing, moves no plan, and ends nothing. If the user
keeps discussing afterwards, the discussion simply continues, and they can ask for it again later.

## Where it comes from

- **The discussion as it stands now.** Where the user changed their mind, the latest ruling is the
  decision. Earlier versions appear only under *Changed along the way*, and only when the user
  might still remember the old one.
- **The decision document, if one exists** (`docs/discussions/`), and its *What the User Sees*
  section in particular. Where it and the discussion disagree, say so under *Needs you*; do not
  pick one quietly.
- **Nothing else.** Add no idea that was not discussed. If a gap has to be filled for the summary
  to make sense, fill it and mark it *(my assumption, not discussed)*.

## How it is written

- **Plain words.** No jargon a newcomer to the project would have to look up. Where a technical
  term is unavoidable, explain it in the same sentence.
- **No shorthand made up along the way.** Option letters, decision numbers, ticket IDs, rule tags,
  pass names and code names mean something only to someone who was in the conversation. Name the
  thing by what it does. If a code name is how the user will find it later, give it once, in
  brackets, after the plain description.
- **Short sentences, real numbers.** "About 40 files" rather than "a moderate footprint".
- **Only what was decided.** A section with nothing in it is left out.

## The shape

```markdown
**Needs you**
[Only if something is open: each question, why it matters, and what happens if it is left open.]

**What you'll get**
[The functional view. What the user, or their users, can do or see afterwards that they cannot
today; what changes about what they already do; what deliberately stays the same.]

**How it works**
[The architectural view. The main pieces and how they connect, in plain terms: what is new, what
existing parts are reused, and what is removed and what takes over its job.]

**What it costs**
[The trade-offs accepted: limits, what gets harder, what it takes to build, risks carried.]

**What we ruled out**
[One line each: the option, and why it lost.]

**Changed along the way**
[Only decisions the user might remember differently: what it was, what it is now, and why.]
```

## Afterwards

- **It is said, not saved** (AW-29). Write it to a file only if the user asks, and never into the
  decision document: that records their intent in their words, and a summary is yours.
- **Offer nothing else with it.** It answers the request; the next step is still the user's.
