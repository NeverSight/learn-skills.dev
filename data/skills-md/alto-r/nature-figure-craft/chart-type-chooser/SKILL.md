---
name: chart-type-chooser
description: >-
  Decide WHICH chart to draw before drawing it. Profiles the data file first, proposes
  the candidate claims that data can actually support (numbers already computed), lets
  the user pick one and choose among the expensive options (map or no map, facets or
  one panel, points or summary), then returns two or three candidate chart types with
  reasons, the rejected alternatives, the encoding plan, and an anti-pattern check. Covers roughly seventy chart types across nine communicative
  intents: comparison, distribution, composition, relationship, trend, spatial, flow
  and network, uncertainty and inference, and conceptual schematics. Use when the user
  asks "which chart should I use", "how should I visualise this", "is a pie chart okay
  here", "my figure does not communicate", when planning a paper's figure set, or
  before writing any plotting code.
license: CC-BY-4.0
---

# Chart Type Chooser

## Client compatibility

Use this skill in Claude Code or OpenAI Codex with the same workflow and resources.
Resolve `assets/` and `references/` relative to this `SKILL.md`, not the user's
working directory; pass the user's data file by its actual path. Run commands in
the user's project so generated files stay with their work.

In Codex, invoke explicitly with `$chart-type-chooser` or let the client select it.
When handing off to `nature-figure-production` or another client session, carry
forward the data paths, computed profile, chosen claim, filters, chart type and
encoding plan. If the production skill is unavailable, return that plan for the
user to use later.

## Overview

Most bad figures are not badly *rendered* — they are badly *chosen*. A beautifully
styled grouped bar chart of a time series is still the wrong figure. Choice comes
before craft, and it is decided by what the figure must say, not by what data happens
to be in the dataframe.

This skill runs an eight-step selection procedure and returns candidates with reasons.
It does not produce final artwork; hand off to `nature-figure-production` for that.

Load references on demand:

- **[references/catalog.md](references/catalog.md)** — the full inventory: nine intents, ~70 chart types, what each can express, when not to use it
- **[references/decision-rules.md](references/decision-rules.md)** — data-structure gates, encoding-channel ranking, and how to break ties
- **[references/antipatterns.md](references/antipatterns.md)** — symptom → cause → prescription table, and the figures that mislead
- **[assets/profile_data.py](assets/profile_data.py)** — Step 0 profiler: column kinds, group sizes, composition sets, repeated-measures structure, and the settled/open decision points

## When to use this skill

- Before writing any plotting code.
- The user asks which chart type fits, or whether a chosen one is appropriate.
- A figure "does not communicate" and the fix may be structural rather than cosmetic.
- Planning the figure set for a whole paper (which figures, in what order).
- A reviewer says a figure is unclear, uninformative, or misleading.

## When NOT to use this skill

- The chart type is already settled and only styling is at issue →
  `nature-figure-production`.
- The figure is a conceptual schematic with no data (method overview, motivated
  example) → intent ⑨ in the catalog gives the paradigms, then use a vector tool.
- Interactive dashboards or web visualisation. Different constraints.

---

## Core procedure

### Step 0 — Profile the data before saying anything

Never ask "what do you want to plot?" before looking. Run the profiler, replacing
`<skill-dir>` and `<project-dir>` with the actual installed skill and project paths:

```bash
python "<skill-dir>/assets/profile_data.py" "<project-dir>/data.xlsx" --sheet Fig2
```

It reports, per column: kind (continuous / categorical / identifier / temporal /
latitude / longitude), cardinality, range, median, tail ratio, whether zero is real
or float noise, group sizes per categorical, verified composition sets (parts that
actually sum to a total), wide-format scenario families, and which of the nine
intents the table can express at all.

This exists because the alternative is guessing from column names, and column names
lie. A continuous measurement is all-unique by construction, so a naive check calls
it an identifier; solver and simulation output routinely carries values like `-1.0e-09`
that are structurally zero, which looks signed and would wrongly recommend a diverging
colour ramp.

Report the profile to the user before proposing anything. It is short, and it is the
evidence for everything that follows.

**Also ask one thing the data cannot tell you: where this figure sits in the paper.**
One question, asked once, at the top:

> Is this Figure 1, or a later figure? (Or: supplement / not decided yet.)

It changes what the figure is *for*, and nothing downstream can recover it. Section 6
of `references/decision-rules.md` gives the job and the typical intents for each
position. Read it now, not at the end — Step 3 uses it. If the answer is "not decided",
carry on and say which position the recommendation assumes.

### Step 1 — Propose the claims the data can support, then let the user choose

The strict version of this step demanded the user supply a one-sentence claim and
refused to continue without one. Right principle, wrong ergonomics: the person who
just exported a spreadsheet often has not yet put the finding into words, and being
interrogated does not help them do it.

So do the work first. From the profile, draft **three to five candidate claims**, and
**compute the number in each one**. Not "there are regional differences" — the actual
ratio, the actual counts, the actual direction. A candidate with a real number is
either obviously worth a figure or obviously not, and the user can tell in seconds; a
candidate phrased as a topic tells them nothing and gets a shrug.

Draw the candidates from what the profile actually found, one per structural feature
it detected — a spread across the levels of a grouping column, a difference in
composition between the extremes, a change across the levels of a repeated-measures
factor, a relationship between two measures, a concentration in space or time. Do not
carry over candidates from a previous dataset, and do not propose one whose supporting
signal is absent from the profile.

**Any candidate whose number depends on a binning or an aggregation level must be
computed at more than one resolution before it is offered — and before it is dropped.**

Most candidates carry a hidden free parameter. A "concentration along latitude" needs
latitude bins. A "change over time" needs a time step. A "spread across groups" needs
a level of the grouping hierarchy. The effect size is a *function* of that parameter,
and picking one value arbitrarily means the candidate's number — and therefore whether
it survives to be offered — was decided by a choice nobody made deliberately.

The rule:

- Compute the candidate at **at least two resolutions**: the one the field
  conventionally uses, and one step finer.
- **Never drop a candidate on a single binning.** "No story" is a claim about the
  data; one arbitrary bin width cannot support it.
- Report the **strongest defensible** resolution, and say which one it is. Strongest
  is not the same as finest — a resolution that leaves most bins with too few
  observations to mean anything is not defensible, and the group counts are right
  there in the profile.
- If the resolutions **disagree materially, that disagreement is itself a finding**
  and belongs in the candidate, not in a footnote. A gradient that appears only at a
  fine resolution is a real but local effect; one that appears only when pooled is
  usually an artefact of the pooling.

Worked example, from a real run of this skill that got it wrong. A table of 1,898
georeferenced sites was tested for a latitude gradient in cost:

```
|lat| bins 0/10/20/30/90   ->  511 / 514 / 515 / 640      ratio 1.25x   "no story", dropped
10-degree bins, n >= 30    ->  ... 525 / 1015 / 785 / 909  ratio 2.0x   real, and poleward
```

Same column, same measure, opposite conclusion. The coarse binning pooled everything
above 30 degrees into one bucket and averaged the poleward rise away. The candidate
was dropped, the spatial intent went with it, and the figure lost a map. Two lines of
extra computation would have caught it.

Offer them as a choice, plus "none of these — here is mine".

**The discipline survives.** Whatever comes back, restate it as one verbatim claim
sentence before continuing. Two claims means two panels or two figures, not one clever
figure. And the escape hatch still applies: if nothing in the profile supports a claim
worth a sentence, say so. If a result does not fit any chart type, the experiment
usually has no clear conclusion.

### Step 2 — Ask only what the data leaves open

The profiler ends with two lists: **settled** and **open**.

**Settled — state, do not ask.** Where the data determines the answer, asking is
noise that makes the real questions harder to see. If the same entity appears under
every level of a factor, the design is paired; say so and move on.

The bar for "settled" is high: the data must *determine* the answer, not merely
suggest one. Sample-size cutoffs are the tempting counter-example and they are not
settled. Dropping the levels of a grouping column below some n changes how many
levels survive, which changes which extremes define the comparison, which changes
the headline number the figure lets the reader state. The profiler therefore reports
group sizes and applies no cutoff at all. Choosing one is Step 2 work, it goes to
the user, and whatever comes back is recorded with its reason in the output.

**Open — ask, but formulate the questions yourself.** The profiler deliberately does
not write question text or option wording. Canned questions drift out of sync with
the data and read as boilerplate; worse, a fixed menu invites asking about things this
particular table never raised. Write each question in the user's own language, using
the real column names and the real numbers from the profile.

Rules for asking:

- **One question per genuinely open choice**, and none for anything outside the
  profiler's open list.
- **Ground it.** Every question carries the fact that generated it — "`X` runs 29× its
  median" — so the user can see it came from their data, not from a template.
- **Options must be a real fork**, with the consequence of each stated. Not
  "log or linear?" but what each one costs the reader.
- **Lead with a recommendation** when the claim already implies one, and say why.
  Offering a naked menu pushes a judgment call back onto someone who came for help.
- **Batch them.** Use the interactive question tool if the environment has one, so the
  user answers several at once rather than in a chain of round trips.
- **Do not ask what the user already told you.** If the chosen claim says "across
  regions", the split question is answered.

Record the answers, then run Steps 3–7 as a **verification pass** on that choice
rather than as a second interrogation. If a pick fails a gate, name the gate and offer
the nearest alternative — never substitute silently.

### Step 3 — Classify the intent

Map the sentence to one of nine communicative intents. The verb usually gives it away.

| Intent | Verb signature | Example claim |
|---|---|---|
| ① **Comparison** | is larger / outperforms / ranks | "Method A beats all baselines" |
| ② **Distribution** | is spread / is skewed / varies | "Response times are bimodal" |
| ③ **Composition** | is made of / accounts for | "One component accounts for 40% of the total" |
| ④ **Relationship** | correlates / predicts / trades off | "Cost rises with remoteness" |
| ⑤ **Trend** | rises / falls / oscillates | "Emissions peak in 2035 then decline" |
| ⑥ **Spatial** | concentrates in / differs across regions | "The gap concentrates in Southeast Asia" |
| ⑦ **Flow & network** | moves from / connects to | "Half of the units cross the threshold" |
| ⑧ **Uncertainty & inference** | is significant / is uncertain / depends on | "Only one coefficient is significant" |
| ⑨ **Concept** | works as follows / fails because | "Existing methods fail on multi-table queries" |

Mixed claims ("A is larger AND rises over time") are almost always two panels.

**A claim may carry a secondary intent, and usually does.** The primary intent is the
one the verb names, and it decides the main panel. The secondary intent is the
question a reader asks *immediately after* reading the claim, and it decides whether
the figure needs a context panel next to the main one.

| Primary claim | Reader's next question | Secondary intent |
|---|---|---|
| "cost differs 2.8× between regions" | *which* regions, and where are they? | ⑥ spatial |
| "the distribution is bimodal" | what separates the two modes? | ① comparison |
| "emissions peak in 2035" | in which scenario, and how uncertain? | ⑧ uncertainty |
| "A outperforms all baselines" | on what, and by how much per case? | ② distribution |

Naming the secondary intent is not permission to add panels freely — Step 6 still has
to justify each one. But an earlier version of this step allowed exactly one intent
per claim, and that silently foreclosed whole chart families: a claim whose verb was
"differs" could never reach intent ⑥, so a paper with 1,898 georeferenced sites got no
map. The catalog for ② and ③ contains no map row, and nothing downstream ever
reconsiders.

Record both:

```
primary   = <intent> -> main panel
secondary = <intent, or none> -> context panel, if Step 6 justifies it
```

**Cross-check against the figure's position** (from Step 0) using the figure-set table
in `references/decision-rules.md` section 6. A Figure 1 is expected to establish the
phenomenon *and its scale* — typically ⑥ spatial + ② distribution — while a Figure 4
is usually ① comparison. If the intents you derived from the verb disagree with the
position's typical intents, that is not an error, but say so and give the reason. The
usual cause is a claim sentence written narrower than the figure's actual job.

### Step 4 — Fix the SCALE before anything else

This gate comes before every other consideration, and it is the one an AI assistant
gets wrong by default.

Given a dataset and the instruction "plot this", a model — and a researcher on
autopilot — reaches for the **most aggregated view available**: the global total, the
grand mean, the pooled distribution across all samples. That view is almost never the
one a paper needs. A paper's claim virtually always lives at an **intermediate**
scale: differences *between* regions, *between* scenarios, *between* subgroups, or
*within* one representative case.

Three decisions, all before choosing a chart type:

| Decision | Question | Example answers |
|---|---|---|
| **Aggregation level** | What does one mark represent? | one site / one region / the whole system |
| **Comparison unit** | Who is being compared with whom? | group vs group / condition vs condition / each unit vs its own baseline |
| **Granularity** | How finely is the axis resolved? | hourly vs annual; site vs region vs global |

Then check the claim sentence against them. If the sentence says "**varies across**
regions" but the plan aggregates to a global total, the plan destroys the claim before
a single line is drawn.

**Symptoms that the scale is wrong**

- The figure has one bar, one line, or one number, and the claim was about variation.
- The claim contains "across", "between", "heterogeneous", "some … while others",
  but the plan has `df.groupby(...).sum()` at the top level with no facet.
- Everything looks flat and unsurprising — aggregation has cancelled opposing trends.
- Reviewers ask "does this hold in all regions?" and the figure cannot answer.

**The standard escalation**: when in doubt, drop one aggregation level. Global total →
per-region small multiples. Pooled distribution → distribution per group (ridgeline,
split violin). Single mean line → one line per scenario, with the ensemble
de-emphasised behind them.

This is why a paper whose central claim is about **heterogeneity** ends up with a
figure set dominated by per-unit small multiples, ridgelines and violins rather than
global summaries: heterogeneity dies under aggregation.

Conversely, do not over-disaggregate. If the claim is "the global total rises", 23
regional panels bury it. Match the scale to the sentence, in both directions.

Record the decision explicitly before moving on:

```
one mark = <entity>
comparison = <unit A> vs <unit B>
granularity = <axis resolution>
```

### Step 5 — Gate on data structure

Read the gates in `references/decision-rules.md`. The relevant facts:

- Number of categories (2 / 3–6 / 7–20 / >20)
- Sample size n (<50 / 50–500 / 500–10k / >10k)
- Are categories **ordered** (time, dose, latitude) or **nominal**?
- Number of variables shown simultaneously (1 / 2 / 3 / >3)
- Is there a meaningful **zero**, **threshold**, or **reference value**?
- Are there repeated measurements (→ uncertainty must be shown)?

These gates eliminate most candidates automatically. Example: intent ② with a
few dozen points per group makes a histogram or KDE hard to defend — there is not
enough there to estimate a density — and points at beeswarm or raincloud instead.

Note what kind of gate that is. It rules out a *chart type* on the evidence
available, which is reversible and visible. It does not silently discard
observations. Any gate that removes rows or levels from the analysis is a
different animal: it belongs in Step 2 as an explicit choice, with the number and
the reason recorded in the output.

### Step 6 — Shortlist two or three candidates

Pull candidates from `references/catalog.md` for the intent, apply the gates, and rank
by:

1. **Faithfulness** — does the encoding preserve the claim without distortion?
2. **Data-ink ratio** — the least ink that carries the claim *in full*. Ink that
   carries no information is waste; ink the reader needs in order to interpret the
   marks is not, and cutting it scores well on this criterion while making the
   figure worse.
3. **Perceptual accuracy** — position > length > angle > area > colour intensity.
   Encode the quantity the claim is about on the most accurate available channel.
4. **Convention in the field** — a familiar chart is read faster; deviate only when
   the gain is real.

Always name the **rejected** alternatives and why. That reasoning is what the user
takes forward to their advisor.

**Criteria 2 and 3 do not apply to a panel whose job is orientation.**

This exemption exists because criteria 2 and 3 measure one thing — how accurately a
reader can *read a value off the page* — and they were never meant to decide whether
a reader knows *what they are looking at*. A map loses on both by construction: a
basemap is a large amount of ink encoding no variable, and a point map puts the
quantity on colour, which sits near the bottom of the Cleveland–McGill ranking. So
any claim that a bar chart could also carry will beat a map on criteria 2 and 3,
every single time, regardless of whether the map was the right figure.

A panel is doing orientation rather than measurement when it answers *where / which
one / what is this*, and the numbers are read off a neighbouring panel. Locator maps,
study-area panels, and schematic insets are all in this category. For those, rank on
faithfulness and convention only, and judge the ink question as "does this help the
reader place the result", not "how many pixels per data point".

Two guards, so this does not become a licence:

- The orientation panel must not be the *only* place a quantity appears. If the
  reader has to estimate a value from the map, it is a measurement panel again and
  criteria 2 and 3 come back.
- If nothing about the claim depends on which entity is which, there is no
  orientation job to do and the exemption does not apply.

The same logic covers any panel added for a secondary intent from Step 3.

### Step 7 — Specify the encoding and run the anti-pattern check

Produce a concrete encoding plan:

```
x           = <variable, scale, range, whether zero is included>
y           = <variable, scale, range>
colour      = <variable, palette family, why colour and not another channel>
size/shape  = <variable, if used>
facets      = <variable, layout>
reference   = <zero line / 1:1 diagonal / median / threshold>
annotation  = <the 1-2 marks the claim points at>
```

Then check every row of `references/antipatterns.md` that applies. Report violations
with severity.

---

## Cross-cutting rules

- **Show the distribution, not just the mean.** A bar of means with error bars hides
  shape, n, and outliers. Raincloud, violin+points, or beeswarm instead. This is now
  a common reviewer demand across fields.
- **Perceptual channel ranking** (Cleveland–McGill): position on a common scale >
  position on unaligned scales > length > slope > angle > area > colour saturation >
  volume. Put the quantity the claim is about as high on this list as possible.
- **Never encode a quantity in 3D.** Perspective distorts magnitude; the only
  exception is genuinely three-dimensional data (a molecular structure, a flow field).
- **Colour is the last resort for a quantitative variable**, and the first resort for
  a nominal one.
- **Over-plotting is a chart-type problem, not a styling problem.** At n > 10,000,
  a scatter is the wrong chart; use hexbin, 2D KDE, or contours.
- **Ordered categories deserve an ordered encoding.** Latitude, dose, year, and
  severity should be sorted and given a sequential ramp, never a qualitative palette.
- **A truncated axis is a claim about relevance** — legitimate when differences are
  small and real, dishonest when it manufactures a difference. Mark breaks explicitly.
- **Small multiples beat a legend with seven entries.** If the eye must track more
  than ~4 overlapping series, facet instead.

## Integrity gate

Before returning a recommendation, verify:

1. **The data was profiled, not guessed at.** Column kinds, group sizes and
   composition sets came from the profiler, not from reading column names.
2. **Every number in a proposed claim was computed**, not estimated from the shape of
   the data. A proposed claim with an invented number is worse than no proposal.
2b. **No candidate was dropped on a single binning.** Every candidate whose number
   depends on a bin width or an aggregation level was computed at two or more
   resolutions, the reported one is named, and any material disagreement between
   resolutions is stated rather than resolved silently.
3. **Questions were generated from this table, not from a template.** Every question
   asked traces to a decision point the profiler reported as open, phrased with this
   table's column names and numbers. Nothing settled by the data was put to the user
   as a question, and nothing outside the open list was asked at all.
4. The one sentence the user settled on is a claim, not a topic.
5. **The scale matches the claim.** If the sentence is about variation between units,
   the plan does not aggregate those units away; if it is about a global total, the
   plan does not bury it in facets. The default most-aggregated view was actively
   rejected or actively chosen, never accepted by inertia.
6. The recommended chart type can express that exact claim (not a neighbouring one).
7. Data structure gates were applied, not skipped.
7b. **Every cutoff that removed data is stated with its number and its reason**, and
   the headline number is reported alongside what it would have been without the
   cutoff. A threshold nobody can see is the easiest way for a figure to state a
   number the data does not support.
8. Rejected alternatives are named with reasons.
9. The encoding plan puts the claim's quantity on a high-accuracy channel — except
   on an orientation panel, where Step 6 waives that criterion and the quantity is
   read off a neighbouring panel instead.
9b. **The secondary intent was named or explicitly ruled out**, and if coordinates
   exist, the decision about a map was made on whether the reader needs to know
   which entity is which — not on ink or channel accuracy.
10. Uncertainty is shown if repeated measurements exist.
11. No anti-pattern from `references/antipatterns.md` is left unflagged.
12. If the claim needs two chart types, that is stated as two panels rather than forced
   into one.

## Output format

### 1. Data profile
- Rows / columns, and the kind of each column that matters
- Grouping columns with their group sizes (no cutoff applied by the profiler)
- Composition sets, repeated-measures structure, long tails, real zeros
- Coordinates present: yes / no

### 2. Candidate claims offered
- a / b / c ... each with its computed number
- For any candidate needing a binning or aggregation level: the resolutions tried,
  the number at each, and which one is being reported
- **Dropped**: <candidate> — <the number, at which resolutions, and why it is weak>
- **Chosen**: <verbatim claim, as the user settled it>

### 3. Choices
- **Settled by the data**: <decision point> → <what it forces, and why>
- **Put to the user**: <question as asked> → <answer> — <the profile fact behind it>

### 4. Intent
- Figure position: <Fig 1 / later figure / supplement / not decided — assumed X>
- Primary intent: <one of the nine> — <one line>
- Secondary intent: <one of the nine, or none> — <the question a reader asks next>
- Agrees with the position's typical intents (decision-rules.md section 6)?
  <yes / no, and why not>

### 5. Scale
- One mark = <entity>
- Comparison: <unit A> vs <unit B>
- Granularity: <axis resolution>
- Aggregation actively chosen, not defaulted: <yes, with reason>

### 6. Data structure
- Categories: <n, ordered or nominal>
- Sample size: <n>
- Variables shown: <list>
- Reference value: <zero / threshold / none>
- Repeated measurements: <yes or no>

### 7. Recommendation
- **Main panel**: <chart type> — <why it carries the claim>
- **Context panel**: <chart type, or none> — <which secondary intent it serves, and
  why the figure needs it>. If it is an orientation panel, say so and note that
  ranking criteria 2-3 were waived per Step 6
- **Alternative**: <chart type> — <when to prefer it>
- **Rejected**: <type> (<reason>), <type> (<reason>)

### 8. Encoding plan
- x / y / colour / size / facet / reference / annotation

### 9. Anti-pattern check
- <n> issues: <list with severity>

### 10. Handoff
- Next: `nature-figure-production` for sizing, style, and export.
- Deliverable from the plotting code is the **data layer only**: marks, axes, ticks.
  Titles, callouts, and explanatory text are added at assembly, not in the script.
