---
name: relation-scaffolding
description: Use when fiction keeps stating edges between events, states, or propositions — causation, contrast, implication, relationship, process, meaning — that event order or syntax could carry; use for AI-flavored concept-link scaffolds (“并非A而是B,” “不仅而且,” “因此可以看出,” “某种意义上”) and beginner event-link chains (“然后…然后…”); also use when the user wants a frequency/context audit of Chinese function words or relation-heavy content words.
license: Apache-2.0
compatibility: Optional Python script uses jieba for Chinese token/POS measurements; manual analysis works without it.
---

# Relation Scaffolding

## Use when

The prose keeps naming how facts relate instead of letting syntax, event
order, or juxtaposition carry part of the relation. The load-bearing unit
here is not the conjunction — it is any word or construction that declares
an edge between two events, states, or propositions.

## Do not use when

Do not optimize fiction toward a low connector count. Logical argument,
legal prose, technical exposition, and deliberately analytic narrators often
need explicit edges. Do not strip relation marking from a character whose
job or situation genuinely requires it.

## Core test

**Delete the edge marker. If the facts and the intended inference survive
unchanged, the marker may be paying rent only as explanation.**

Frequency is an alarm, not a verdict.

## Three classes of relation scaffolding

1. **Explicit connectors** — 然后, 因此, 于是, 然而, 但是, 同时, 从而, 既然,
   虽然, 尽管. They declare a time, cause, contrast, or concession edge.
2. **Relational constructions** — 不是A而是B, 不仅A而且B, 一方面A另一方面B,
   正因为A所以B, 与其A不如B. They package a contrast or implication as a
   clause-level scaffold.
3. **Relation content words** — 关系, 状态, 过程, 变化, 意义, 影响, 体现,
   反映, 导致, 形成, 层面, 维度. They summarize an edge as a noun or verb.

All three do the same job: **they tell the reader which edge connects two
things.** The engineering question is always the same:

> Is this edge already legible from event order and syntax? If not, stating
> it may be cheaper than forcing the reader to rebuild the wrong edge.

## Two overmarking profiles

- **Event-link overmarking** (beginner-human): every action gets an explicit
  time edge — 我先起床，然后刷牙，然后出门，然后去了学校. The narrator can
  only chain events in order and marks every link.
- **Concept-link overmarking** (first-generation AI voice): every pair of
  facts gets an explicit logic edge — 这并不是简单的X，而是Y；这不仅体现了A，
  也意味着B；因此可以看出；从某种意义上说. This is not a novel-writing
  failure; it is the relation-marking habit of exposition, summary, Q&A, and
  analysis leaking into fiction. The register is the leak, not the words.

## Workflow

1. Mark function words, relational constructions, and relation-heavy
   nouns/verbs.
2. Group by job: cause, contrast, simultaneity, implication,
   state/process naming, metadiscourse.
3. Inspect local concordance, not raw count.
4. For each candidate, delete or demote the marker mentally.
5. Keep it if it changes logic, timing, scope, emphasis, or voice.
6. Remove or recast it if event order already makes the same edge
   unavoidable.
7. Re-read for accidental ambiguity. Compression is not a virtue if the
   causal graph breaks.

## Candidates, not banned words

Chinese prose often deserves inspection around forms such as `因此`, `然而`,
`于是`, `从而`, `同时`, `意味着`, `体现`, `关系`, `状态`, `过程`, `层面`,
`维度`, `某种`, `似乎`, `并非……而是……`, and chain-openers like `然后`.

A necessary “因此” is cheaper than two sentences that force the reader to
reconstruct a non-obvious proof. The audit targets edges, never words.

## Minimal pair

> 他没带伞，因此淋湿了。
>
> 他没带伞。到办公室时，袖口还在滴水。

In ordinary scene prose, the second sentence carries cause through event
order. In an argument about causes of absenteeism, `因此` may be exactly
right.

Concept-link variant:

> 这并不是一次简单的离别，而是一个新的开始。
>
> 她把钥匙放回桌上，没有拿走。

The second lets the altered action carry the edge. The first is only needed
if the distinction between “simple farewell” and “new start” is genuinely
informative in context.

## Counterexamples

- “若阀门关闭，因此压力上升” in a technical derivation: relation marking
  is the content; do not strip it for literary sparsity.
- “他似乎睡着了。” when viewpoint uncertainty matters: `似乎` changes
  epistemic scope and must survive.
- A comic bureaucratic narrator who says “关系进入维护期” as the joke:
  the register is the character's, not a leak.
- “他意识到煤气没关。” The realization is an event with immediate
  informational content; the edge is the point.

## Rule strength

**Strong audit rules.** This is the most engineerable layer: frequency
counting, concordance inspection, and one-variable deletion tests are all
reliable here. Still no blacklist — the audit output is a keep/compress/
rewrite triage, never a ban list.

## Scripts

- `scripts/zh_style_scan.py` — candidate counts, normalized rates, repeated
  scaffolds. Never returns an “AI score.”
- `scripts/concordance.py` — literal/regex concordance with local context.

Use scripts only when the passage is long enough that memory-based counting
becomes unreliable.

## Read next

- [overmarking-classes.md](references/overmarking-classes.md) for the
  event-link / concept-link profiles and their tests.
- [chinese-function-words.md](references/chinese-function-words.md) for
  candidate classes and retention tests.
- [relational-nouns-and-verbs.md](references/relational-nouns-and-verbs.md)
  for content words that summarize edges.
- [relation-constructions.md](references/relation-constructions.md) for
  clause-level scaffolds.

## Return shape

Report candidate spans in three buckets: **keep**, **compress**,
**rewrite the event**. Give one local reason per span; do not dump a
blacklist. If the pattern is concept-link overmarking, name the expository
register that leaked before proposing deletions.
