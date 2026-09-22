---
name: deep-research
description: >-
  Run structured multi-source research that produces a cited, adversarially
  verified synthesis with explicit confidence. Use when a question needs more
  than a single lookup and being wrong is costly — comparing options,
  validating a claim, surveying a market, briefing a decision.
version: 1.0.0
license: MIT
---

# Deep Research Guide

Covers scoping (and narrowing) the question, fanning out across sources,
judging source quality, adversarially verifying each key claim, separating fact
from inference, and reporting with explicit confidence.

Keywords: deep research, multi-source, fact-check, verify, synthesize, cited
report, source credibility, due diligence.


Produce a **trustworthy synthesized answer**, not a pile of links. The output of research is a
decision-grade brief: a clear claim, the evidence behind it, citations, and an honest map of
what is still unknown. Speed without verification is a liability — a confident wrong answer
costs more than a slow right one.

> Core principle: default to skeptical. Treat every key claim as guilty until corroborated.
> Your job is not to confirm a hypothesis — it's to find what would break it.

## Workflow — plan → gather → verify → synthesize

Run these as distinct phases. Don't start writing the report while you're still gathering, and
don't gather before the question is scoped.

### 1. Plan — scope the question

Before searching, pin down what's actually being asked. Most bad research answers a question
nobody asked.

- **State the question in one sentence.** If you can't, it's not scoped yet.
- **Name the decision it serves.** "Which X should we pick?" needs different evidence than
  "Is X true?". The decision sets the bar for confidence.
- **List the answer's shape.** A number? A recommendation? A comparison table? A yes/no with
  caveats? Knowing the shape tells you when you're done.
- **Set boundaries**: time window (recency that matters), geography, scale, definitions of
  fuzzy terms.

**Narrow an underspecified question before spending effort.** If the ask is "what should I
buy / which tool / is this a good idea" without budget, use-case, constraints, or context, ask
2–3 clarifying questions first. Researching the wrong question thoroughly is still wrong.

Then decompose into **sub-questions** — the 3–7 things that must each be answered for the whole
to hold. Research the sub-questions; assemble the answer.

### 2. Gather — fan out across sources

- **Cast wide before going deep.** Run several differently-worded queries; don't anchor on the
  first source's framing. Search for the *counter*-claim too ("X is overrated", "problems with
  X") — not just confirmation.
- **Go to primary sources.** Prefer the original study, filing, spec, dataset, or official
  doc over an article summarizing it. Summaries drift; numbers get garbled in retelling.
- **Triangulate.** A claim is only as strong as the number of *independent* sources that
  confirm it. Three outlets all citing one press release is one source, not three.
- **Capture as you go**: for each fact, note the source, the date, and a direct quote/figure.
  You cannot cite what you didn't record.

### 3. Verify — adversarial check (the step people skip)

For each **key claim** (the ones the conclusion rests on), actively try to refute it:

- **Find the origin.** Trace the claim to its source. Where did this number actually come
  from? Who measured it, how, and when?
- **Look for the strongest disagreement.** Who says the opposite, and why? A claim you can't
  find any dissent on is either settled or you haven't looked hard enough.
- **Check the math and the units.** Percentages without a base, totals that don't add up,
  growth rates with no time frame, and apples-to-oranges comparisons are the common tells.
- **Test recency.** Is this still true? Prices, rankings, "fastest/largest/only" claims, and
  policy facts decay. A correct 2019 fact can be a wrong 2026 answer.
- **Watch for self-interest.** Vendor benchmarks, sponsored studies, and anything selling
  something get an extra round of scrutiny.

If a claim survives a genuine attempt to break it, it's load-bearing. If it doesn't, demote it
to "reported but unverified" or drop it.

### 4. Synthesize — write the brief

- **Lead with the answer.** First line: the conclusion / recommendation. Decision-makers
  read top-down and may stop after the first paragraph — make it count.
- **Then the why**, structured by sub-question, each point carrying its citation.
- **Separate fact from inference explicitly** (see below).
- **Close with confidence + unknowns.**

## Source-credibility checklist

Score each source before you lean on it:

- **Primary or secondary?** Original data/document > reporting on it > commentary on the
  reporting.
- **Authority** — does the author/org actually have standing on this topic, or are they out of
  their lane?
- **Recency** — is it current enough for a claim that changes over time? Note the date, always.
- **Independence** — funded by, owned by, or selling the thing in question? Conflicts bias.
- **Method transparency** — can you see how they got the number (sample, methodology, sources),
  or are you trusting an assertion?
- **Corroboration** — do independent sources agree? Outliers need explaining, not silent
  dropping.
- **Track record** — has this source been reliable/retracted before?

Rough hierarchy (context-dependent, not absolute): peer-reviewed studies, official
filings/standards, and primary datasets at the top; reputable journalism and expert analysis
in the middle; anonymous posts, marketing, and AI-generated content summaries near the bottom.
A low-tier source can still be right — it just needs corroboration before it carries weight.

## Separating fact from inference

Be ruthless about which is which; conflating them is how research misleads.

- **Fact** — directly stated by a credible source, with a citation. ("Revenue was $4.2M in
  2025 [source].")
- **Inference** — your reasoning *from* facts. Label it. ("This implies ~30% YoY growth,
  assuming the 2024 figure of $3.2M is comparable.")
- **Assumption** — something you're taking as given without evidence. Name it so the reader can
  challenge it. ("Assuming the same accounting basis across years.")
- **Unknown** — a gap you couldn't fill. State it; don't paper over it.

Phrases that signal you're doing it right: "according to…", "this suggests…", "I could not
find…", "sources disagree on…".

## Reporting confidence and unknowns

End every brief with an explicit confidence statement. Vague hedging ("seems like") is useless;
calibrated confidence is actionable.

- **High** — multiple independent primary sources agree; recent; verified the underlying math.
- **Medium** — corroborated but with gaps, dated data, or some reliance on secondary sources.
- **Low** — single source, conflicting evidence, stale data, or heavy inference. Say so loudly.

Always include a short **"What I couldn't verify / what would change this answer"** section.
Naming the unknowns is a feature: it tells the decision-maker where the risk lives and what to
check before betting on it.

## Report template

```
ANSWER:        <the conclusion / recommendation, one or two sentences>
CONFIDENCE:    High / Medium / Low — <one-line why>

KEY FINDINGS
  1. <claim> [source, date]
  2. <claim> [source, date]   (note: sources disagree — see below)
  ...

REASONING / INFERENCE
  <what you concluded from the facts, with assumptions named>

CONTEXT & CAVEATS
  <scope, definitions, anything that bounds the answer>

UNKNOWNS / WHAT WOULD CHANGE THIS
  <gaps you couldn't fill; what to verify before acting>

SOURCES
  [1] <title> — <publisher/author>, <date>, <url> — primary/secondary, why trusted
  ...
```

## Anti-patterns

- **Confirmation hunting** — searching only for what you hope is true. Search the opposite.
- **Citation laundering** — three articles citing one origin presented as three sources.
- **Stale-fact trap** — quoting a "current" superlative that quietly expired.
- **Burying the answer** — making the reader mine paragraphs for the conclusion.
- **False precision** — "$4,231,847" from a source that said "about $4M".
- **Unlabeled inference** — presenting your reasoning as if it were a sourced fact.
- **Over-hedging** — refusing to give an answer when one is warranted. Calibrate, don't dodge.
