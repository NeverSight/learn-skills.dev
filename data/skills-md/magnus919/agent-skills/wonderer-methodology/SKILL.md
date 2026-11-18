---
name: wonderer-methodology
description: >-
  Use lateral exploration to find adjacent ideas, overlooked angles, and research paths when the
  user wants to expand a topic, ask what they are overlooking, or remain in a
  divergent ideation phase. Produce tethered leads without prematurely choosing
  an answer. Do not use for factual lookups, rigorous evidence synthesis,
  product validation, or implementation planning.
license: MIT
metadata:
  category: research
  source_repo: https://github.com/magnus919/hermes-profiles
  source_commit: "867a555e13bae53a3945aa5328b1e09d347268cc"
  source_path: skills/wonderer-methodology
  source_treatment: Adapted for host-neutral loading, explicit evidence boundaries, and bounded exploration.
---

# Wonderer Methodology

Find seams worth investigating around a seed. Preserve the user's divergent
intent: offer a map of possibilities rather than a winning answer. These are
conditions for exploration, not a guarantee of novelty or truth.

## When not to use

- For a factual lookup, answer directly with appropriate evidence.
- For a selected question requiring credible evidence and synthesis, use
  `research-methodology`.
- For testing a customer problem or demand, use `product-discovery`.
- For planning an approved change, use `implementation-planning`.
- For capturing sources into durable notes, use `research-and-vault`.

## Explore the periphery

1. **Frame the seed.** Restate the territory in a few sentences, retaining the
   user's scope and exclusions. If the seed is too vague to distinguish center
   from periphery, ask one focused question and stop pending the answer. When a
   question is explicitly offered for expansion, reframe it as a territory;
   do not silently replace an ordinary request for an answer with ideation.
2. **Decompose first.** Name 3–4 fertile dimensions, such as history, adjacent
   fields, contradiction, inversion, scale boundaries, human experience, hidden
   dependencies, or implied futures. Explain why each fits this seed. Use fewer
   if the user's budget requires it.
3. **Set a bound.** Default to one query per selected dimension, at most four
   queries in one pass. Honor tighter user limits. Name the dimensions and bound
   before retrieval. Adapt query syntax to the available search tool.
   Read [wonderer patterns](references/wonderer-patterns.md) when framing is
   difficult, choosing query patterns, or checking an analogy against an example.
4. **Look for fertile connections.** Use available, authorized read-only retrieval
   when the task calls for external leads. If retrieval is unavailable or excluded,
   work from supplied material and label generated leads as speculative; never
   invent searches, sources, or quotations. Do not send private seed details to
   external search; generalize the query or keep that dimension local.
5. **Keep the tether.** For every retained lead, write one sentence connecting it
   to the seed. Remove tangents with no meaningful connection and merge leads that
   repeat the same structure under different names.
6. **Keep evidence honest.** Prioritize interesting connections without presenting
   them as established findings. Separate what a source actually says from your
   inference or analogy; link the source for any retrieved factual claim. An
   analogy is a hypothesis, not proof that a practice transfers between domains.
7. **Stop at the boundary.** Stop when the query bound is reached, new angles
   repeat existing shapes, or investigation would require depth on one lead.
   Aim for 3–5 distinct leads, but return fewer rather than fill a quota. State
   the stop reason and gaps. A bounded pass is not an exhaustive map.

## Deliver a lead map

Use this compact shape, adapting it to the user's requested format:

- **Seed and exclusions:** the territory being explored.
- **Dimensions and search scope:** selected angles, query bound, retrieval actually
  performed, and any access limits. For an offline pass, say no searches were run.
- **Leads:** for each, give its angle, one-sentence tether, source or speculative
  status, why it could be fruitful, and an open question that would test it.
- **Stop and handoff:** explain why this pass stopped; preserve multiple options.
  If the user selects a lead, route deeper investigation to `research-methodology`.
  Do not automatically launch deep research or rank a winner.

## Completion check

Complete when the user receives a bounded lead map with distinct, tethered leads,
visible uncertainty, and a stop reason, or the focused seed clarification needed
to begin. Check for invented provenance, unsupported transfer claims, duplicated
angles, and accidental convergence before returning it. This skill proposes
exploration only; it does not publish, contact people, or change external state.

## Supporting material

- [Wonderer patterns](references/wonderer-patterns.md): conditional framing,
  search, and tether examples.
- [Evaluation review](references/evaluation-review.md): read when reviewing or
  changing the portable eval assertions and separate trigger probes.
- [Source and adaptation](references/source-and-adaptation.md): read when
  auditing provenance or comparing this port with upstream.
