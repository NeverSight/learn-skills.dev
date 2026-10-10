---
name: pyramid-source-integrity
description: Use to verify sources, factual claims, calculations, or data before or after Pyramid Principle writing. Load for explicit fact checks, strict source-bound work, material data, or consequential factual output; skip ordinary structure-only writing.
user-invocable: false
---

# Pyramid Source Integrity

## Purpose

Check factual content without taking over the writing or storyline. `pyramid-principle-core` and the format skills own structure and expression.

Use the light check by default. Use strict trace mode only when the task needs an audit-ready claim packet, a closed source set, conflicting sources, a high-risk decision, or separate verification around a smaller drafting model.

## Light Check

Run three distinct operations when the artifact materially depends on facts or data:

1. **Check:** Clear each factual claim and derived value before drafting.
2. **Write:** Give the structural skill only the cleared claims and necessary evidence limits.
3. **Recheck:** Compare every factual or evaluative clause, headline, table entry, and number with the cleared claims. Include claims carried by verbs, adjectives, and adverbs. Correct or remove any mismatch.

Keep the check internal unless the user requests a fact-check report or an unresolved evidence gap prevents reliable writing.

For each factual claim or derived value, record only what the writer needs:

- the exact claim;
- its type: supplied fact, derived value, inference, recommendation, or opinion;
- a specific source and exact locator;
- `High`, `Medium`, `Low`, or `Unverified` confidence and a short reason; and
- any population, period, geography, unit, denominator, qualifier, or causal limit that the wording must preserve.

Do not create a separate `permitted use` field. Confidence already determines the drafting action:

| Confidence | Drafting action |
|---|---|
| High | State directly without strengthening the source. |
| Medium | Attribute the source or state the limitation. |
| Low | Keep out of central support; use only as a limitation or verification lead. |
| Unverified | Exclude as fact and name the missing evidence when the gap matters. |

Confidence describes support for the exact claim. It is not a probability or a guarantee. Never invent a numerical confidence score. A user-supplied source that was not independently checked cannot exceed `Medium`.

Treat words such as `significant`, `successful`, `only`, `high`, `low`, `improve`, `reduce`, `solve`, and `likely` as claims when they evaluate scale, quality, effort, cause, effect, or probability. Keep them only when the source supports that exact meaning. Do not combine two concurrent facts into a causal sentence with `because`, `therefore`, `leading to`, `reducing`, or a similar construction unless the source establishes the relationship.

## Require Specific Evidence

A source is specific only when another reviewer can find the evidence again:

- **Prompt:** Identify the current prompt and numbered fact or exact quotation.
- **File:** Give the supplied filename or full path plus page, sheet and cells, table and row, or another exact locator. Include a version, date, or hash when available.
- **Web or publication:** Give the title, publisher or author, URL, section or table, relevant date, and verification date.
- **Database:** Give the dataset or table and the query or exact row locator.
- **Calculation:** Give the input claims, formula or query, named tool, result, rounding, and validation outcome.

`User input`, `company data`, `research`, `derived`, a bare domain, or a dash is not a source.

## Check Data

Apply only the checks the data requires:

1. Preserve every supplied value, sign, unit, denominator, population, period, and qualifier.
2. Recalculate material derived values with a calculator, spreadsheet, query engine, or code execution. Model or mental arithmetic is not a deterministic tool.
3. Keep a derived value at or below the confidence of its weakest required input.
4. Distinguish percentage-point change (`new rate - old rate`) from relative percent change (`(new rate - old rate) / old rate x 100`).
5. Compare values only when their definitions, populations, units, and periods match.
6. Keep missing values missing unless the user requests a labeled estimation method.
7. Preserve correlation as correlation. Do not convert it into cause, impact, benefit, risk, or prediction.
8. Keep conflicting values separate until their definitions, dates, or source authority resolve the conflict.

If a material calculation cannot be reproduced, mark it `Unverified`.

## Check External Facts

When current external verification is required, use an available research tool and prefer a primary or authoritative source that directly supports the claim. Record the source date and verification date, check scope, and use a second independent source for consequential claims when one is available.

If no research tool is available, state `External verification not performed.` and do not answer from model memory.

## Use Strict Trace Mode Only When Needed

Read [references/strict-trace.md](references/strict-trace.md) when any of these conditions applies:

- the user says `use only these facts` or requests a claim packet or visible trace;
- the work is high-risk or must be audit-ready;
- sources conflict or multiple sources make claim-to-source mapping ambiguous;
- a smaller drafting model needs separate pre-check and post-check calls; or
- the user explicitly requests full calculation or provenance records.

Strict mode adds claim IDs, a source register, must-preserve terms, trace tags, and integrity statuses. It does not add a `permitted use` field; the confidence table remains the single drafting rule.

## Hand Off to the Structure Layer

Pass only:

- cleared facts and derived values with their sources, locators, confidence reasons, and required scope;
- requested inferences or recommendations identified as such and linked to their support; and
- material conflicts or evidence limits the reader needs.

The structure layer may select, group, order, and express the cleared claims. It must not assign or upgrade confidence, replace a source, weaken a locator, or change a claim's numbers, scope, status, or certainty.

The source-integrity recheck may correct or delete unsupported wording. It must preserve the approved structure, order, and format; it must not regroup the argument or create a new storyline.

## Return a Fact-Check Report Only When Requested

Use these headings:

1. **RESULT** — State whether the material is supported, needs correction, or cannot be verified.
2. **CLAIMS** — For each material claim, give its status, specific source and locator, confidence, reason, and required correction.
3. **DATA CHECKS** — Show only calculations or data-definition issues that affect use.
4. **UNVERIFIED OR MISSING** — Name unresolved claims and the evidence needed.
5. **SOURCES** — List the sources actually checked. State when no external source was checked.

Do not mix structural findings into this report. If the user requests both checks, return separate `SOURCE INTEGRITY` and `STRUCTURE` sections.

## Capability Boundary

This skill can check consistency with supplied material, validate explicit calculations, preserve data scope, and direct an available research tool. It cannot certify that a supplied source is true, access current information without a tool, recover missing definitions, prove causation from correlation, or make a small model reliable through instructions alone.
