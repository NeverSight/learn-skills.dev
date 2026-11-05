---
name: sdlc-explore
description: >-
  Thinking partner for a half-formed idea: explore the problem, compare
  approaches, and decide whether it needs an intent at all. Use when the user
  says brainstorm, explore, think this through, or is circling an idea before
  sdlc-plan. Writes nothing and implements nothing.
license: MIT
metadata:
  author: acourtiol
  version: "3.0"
---

# sdlc-explore

Think with the user. Read the code, draw the problem, weigh approaches. Write no files and no code. Answering a design question is not consent to build.

## Triage first

Name the path before your first question so the user can correct you.

- **Spike**: can we, is it possible. Agree the probe in two sentences, find out, recommend. No intent.
- **Fix**: a bug, tweak or small change in an existing flow. Hand to `sdlc-fix` if the user asks for it.
- **Intent-worthy**: a new capability or something that changes what the product does. Explore here, then `sdlc-plan`.

If the flow you would change is not already in the repo, it is not a fix. When two paths are plausible, take the heavier one and say so.

## The stance

- One question at a time, saying which decision it unlocks. Read the code before asking what the code can answer.
- Settle the blocking decision first: outcome and scope before API and data model.
- Recommend a path with its tradeoff when evidence supports one. Say plainly when an idea is weak or the cost outweighs the value.
- Split before refining: a request that is really four subsystems gets decomposed, then explore the first piece.
- Separate what you verified, what you assume, what you could not check. Question your own assumptions.
- Cut what the idea does not need. Use plain ASCII diagrams when they beat a paragraph.

Stop when the user has enough clarity.

## Ending

Offer, and let the user decide what happens to it, the sections of `intent.md` in order: Problem (with evidence or `not checked`), Outcome, Acceptance, Out of scope, open questions with an owner or default. Then `sdlc-plan`. A spike ends at its recommendation.
