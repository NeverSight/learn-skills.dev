---
name: surface-insight
description: Take data, observations, or notes and surface non-obvious insights that click into place — connections, dynamics, and structural truths that were hiding in the data all along.
---

# Surface Insight

Take data, observations, or notes and surface insights that were hiding in the data all along. The goal is not theory — it's the "obvious in hindsight" moment where a connection clicks into place because the evidence was right there, just unseen.

## When to Use

- User provides bullet points, notes, data, or observations and wants to extract meaning
- User asks "what does this mean?" or "what's the insight here?" or "connect the dots"
- User has disparate information and wants to understand how pieces relate
- User wants to reason about implications, predictions, or hidden dynamics

Do NOT use for: summarizing (use sharpen-prompt), writing articles (use write-oped), or evaluating prompts (use think-critically).

## The Grounding Rule

Every insight must be **rooted in the user's actual data**. This is the single most important rule:

- Every insight must cite or quote specific data points the user provided
- If you cannot point to concrete evidence in the input, the insight is theory — discard it
- The test: "Could someone verify this insight by re-reading the user's data?" If no, it fails
- Prefer insights where the evidence is *already present* but the connection is *not yet drawn*

An insight that is well-grounded but modest beats a spectacular insight with no evidentiary anchor.

## Process

### Phase 1: Intake (Silent)

Read the user's data. Silently identify:
- What's surprising, anomalous, or unexplained in the data
- What data points seem unrelated but might not be
- What's conspicuously absent given what is present
- Implicit assumptions or framing the user may have

Do not output Phase 1.

### Phase 2: Data-First Discovery (Silent)

**Do NOT start from the lenses.** Start from the data:

1. Find the 3-7 most interesting tensions, anomalies, or unexplained connections in the data
2. For each, ask: "What would make this click into place?"
3. Only then check the Reasoning Lenses below to find vocabulary and structure for what you already found

The lenses are a toolkit for articulating insights, not a checklist for generating them. If a lens doesn't illuminate something already in the data, skip it.

Do not output Phase 2.

### Phase 3: Insight Development

For each discovery, develop the insight:

1. **Ground it** — Quote or cite the specific data points you're connecting
2. **Name the connection** — State the non-obvious relationship clearly
3. **Show why it clicks** — Walk through the reasoning so the reader can verify it against the data
4. **Assess confidence** — Speculative, plausible, or well-supported

HARD RULE: Output exactly 3-7 insights. If you find yourself generating an 8th, discard the weakest. Three strong insights beat seven mediocre ones.

QUALITY GATE: Before presenting each insight, ask: "If I showed this to the user, would they re-read their own data and say 'how did I miss that?'" If no, discard it.

### Phase 4: Output

Present insights ordered by click-factor (strongest "obvious in hindsight" first).

**Output format:**

```
### [Insight Title]

**From the data:** [quote or cite the specific data points being connected]

[2-4 sentences: the insight and reasoning chain. Every sentence must reference something concrete — a named entity, a number, a mechanism, a specific outcome. No sentence may consist entirely of abstract generalities.]

**Confidence:** [speculative | plausible | well-supported]
```

End with a `## Synthesis` section only if the individual insights compound into a higher-order conclusion none of them states alone. If no such pattern exists, omit entirely rather than forcing one.

ANTI-PATTERN CHECK: Before presenting, scan each insight against the Anti-Patterns below. Revise or discard any that fail.

---

## Reasoning Lenses

Use these as vocabulary for insights you've already found in the data — not as a generation checklist.

### Connect — Find hidden links

- **Convergence.** Independent developments heading toward the same collision point.
- **Cross-Impact.** A affects B through a mediating mechanism not visible on the surface.
- **Triangulation.** Multiple independent signals pointing to the same conclusion.

### Project — Extend data through time

- **Extrapolation.** Current trends projected forward to a concrete prediction.
- **Rate-of-Change.** The velocity or acceleration of a metric is itself the signal (e.g., still growing but decelerating).
- **Regime Change.** The system has shifted qualitatively, not just quantitatively — old rules no longer apply.
- **Temporal Displacement.** What's newly possible (or impossible) because conditions changed?

### Explain — Build and test causal stories

- **Abductive Reasoning.** If A and B are both true, the best explanation is H — and here's evidence for H.
- **Retroduction.** If thesis T is correct, we'd expect evidence E1, E2, E3 — check which exist in the data.
- **Counterfactual.** Remove X from the picture — does the outcome still hold? If yes, X wasn't causal.

### Reframe — See from a different angle

- **Analogy.** Structural parallel to another domain or era, with transferable lessons.
- **Disanalogy.** The popular analogy breaks down — and the breakdown itself is the insight.
- **Inversion.** Flip the question to reveal blind spots.
- **Dialectical Synthesis.** The dominant narrative and its contradiction resolve into a higher-order truth.

### Reveal — Expose hidden structures

- **Second-Order Effects.** The first-order impact is obvious; the second-order consequence is not.
- **Incentive Mapping.** Puzzling behavior becomes rational when you see who benefits.
- **The Dog That Didn't Bark.** The absence of an expected signal is itself a signal.
- **Constraint Identification.** The binding bottleneck that limits the entire system.

---

## Insight Quality

The quality bar is the **click test**: does the insight make the reader re-examine the data and say "of course — how did I miss that?"

- **Fail — Restatement.** Rephrasing a data point. REJECT.
- **Fail — Obvious.** Something anyone would see. REJECT.
- **Pass — Non-obvious connection.** Linking data points that aren't obviously related. MINIMUM.
- **Good — Hidden dynamic.** Revealing a mechanism or feedback loop not visible on the surface.
- **Strong — Assumption inversion.** Overturning a default assumption with evidence from the data.
- **Exceptional — Structural truth.** Reframing the entire dataset.

Aim for "Good" or above on at least half of insights. Never output "Fail" level.

---

## Anti-Patterns

- **Theory without evidence.** An insight that sounds smart but doesn't point to specific data. The #1 failure mode.
- **Forced connections.** Straining to link genuinely unrelated data points. "No strong insight here" is a valid output.
- **Vague gesturing.** "This could have major implications" without saying what they are.
- **Prediction without mechanism.** "X will happen" without showing the causal chain from the data.
- **Pattern over-fitting.** Seeing patterns because you're motivated to find them. Test: "Would I believe this if I hadn't been looking for it?"
- **Hedging into uselessness.** "This might possibly suggest..." — commit to the insight or drop it. Use the confidence label instead of hedging the language.
- **Kitchen-sink analysis.** Using too many lenses. 3-7 insights, not 18.

---

## Key Principles

1. **Data first, lenses second.** Find what's interesting in the data, then use lenses to articulate it. Never the reverse.
2. **Obvious in hindsight.** The best insight makes the reader say "how did I miss that?" because the evidence was right there.
3. **Every insight must point to evidence.** If you can't cite specific data from the input, it's theory, not insight.
4. **Concrete and specific.** Not "this market could grow" but "this creates a $X opportunity in Y segment because Z."
5. **Less is more.** Three grounded insights beat seven theoretical ones.
6. **Connect, don't summarize.** The input is data. The output is meaning. The gap between them is where your work happens.

---

## Input

[User provides data, observations, bullet points, or notes below]
