---
name: positioning-audit
description: >
  Audit a brand's social positioning from its profile, offer, customer proof, and competitor material.
  Use when the user says "audit our positioning", "review our profile", "why do we sound like everyone else",
  or "what should our social message be". NOT for inventing a new identity from intuition or writing a post;
  use audience-personas and social-proof-mining first, then hand approved positioning to the content skills.
user-invokable: true
argument-hint: "[profile, offer, proof, and competitor material]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: marketing
---

# Positioning Audit

A profile can sound polished and still give a stranger no reason to care. This skill finds the actual promise, proof, audience, and category language already present, then identifies the smallest credible change. It does not manufacture differentiation.

## 1. Assemble the evidence

Ask for the current bio/profile, offer or landing-page copy, three to five customer quotes or outcomes approved for use, and two to five competitor profiles or posts. Ask what action the profile should earn: follow, DM, email signup, or purchase.

If customer proof is absent, stop at a diagnosis. A new promise without proof is copywriting, not positioning.

## 2. Map the current message

For the brand and each competitor, record:

- the audience named or implied
- the promised outcome
- the mechanism or category label
- proof shown, if any
- the next action requested
- repeated phrases and empty category language

Quote the source next to each finding. Mark an item "unclear" rather than filling it in from industry assumptions.

## 3. Find the credible difference

Compare the maps. Look for one of three things: a proof point competitors do not show, a specific audience they ignore, or a mechanism the brand can honestly explain. Do not treat silence in a small sample as market-wide white space.

Write one positioning sentence in this shape: **For [specific audience] who need [job], [brand] helps them get [outcome] through [mechanism], with [proof].** Flag any missing proof in brackets.

## 4. Stress-test it on the profile

Test the sentence against four questions:

1. Could a competitor say this unchanged?
2. Is every noun understandable to the target audience?
3. Is the outcome backed by a supplied fact or approved quote?
4. Does the requested next action make sense after reading it once?

Return the smallest profile changes: name field, bio promise, proof, pinned-content role, and link CTA. Keep the current message when evidence does not justify a rewrite.

## Hard rules

- Do not invent customer outcomes, category leadership, demographics, or proof.
- Do not copy competitor wording; map the technique, then use the brand's own language.
- Do not call an unobserved gap "white space".
- Separate facts about the current profile from proposed language.
- A public customer quote needs approval before use.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| The position sounds generic | it names a broad category, not a job and proof | narrow the audience or bring in real proof |
| The claim is stronger than the evidence | the desired outcome replaced the observed one | bracket the claim and collect validation |
| Every competitor sounds the same | only bios were compared | add posts, customer proof, and actual offers |
| The bio improves but conversion does not | the next action is unclear | audit the link destination and pinned content |

## Where it sits

`social-listening` finds demand language → `audience-personas` groups it → **positioning-audit** chooses the credible message → `profile-conversion-audit` tests the profile → `campaign-brief` carries the position into a campaign.
