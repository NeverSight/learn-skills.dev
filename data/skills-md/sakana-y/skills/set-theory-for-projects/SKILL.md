---
name: set-theory-for-projects
description: Discover evidence-backed ways an existing project could serve more real contexts while preserving necessary specificity. Use only when the user explicitly invokes $set-theory-for-projects.
---

# Set Theory for Projects

Find the deeper seam, not a larger pile.

Run a bounded, read-only discovery around one **Anchor Project**. Look for a stable **Universal Core**, a bounded **Adapter Opportunity**, or a credible **Platform Opportunity** that could make the project's existing value useful in more real contexts. Treat a **No-expansion Result** as a successful outcome.

The user owns the Expansion Aim and every later scope change. The agent owns the search: user-supplied projects are useful seeds, never a prerequisite or a limit on discovery. Stop at a conversational Discovery Report and Exploration Checkpoint. Implementation, prototyping, integration, and changes to other projects begin only after the user explicitly makes one candidate a new or revised User Problem.

## 1. Establish the Anchor

Identify the Anchor Project from the user's request or the active workspace. Establish an **Expansion Aim**: one sentence naming which existing value should become useful in more concrete contexts. Ask one focused question when that value choice is missing or genuinely ambiguous; investigate factual gaps directly.

Build a compact Anchor Profile from current evidence:

- present users and the problem already solved;
- mechanisms and interfaces that create that value;
- framework, platform, domain, workflow, and experience constraints;
- current integrations, verification surface, release model, and maintainers.

Classify each material constraint as:

- **Necessary Boundary** — removing it would change the value or identity worth preserving;
- **Incidental Constraint** — historical or technical coupling that narrows eligible contexts without creating the core value.

Resolve factual classifications from evidence. Put only ambiguous value trade-offs to the user.

**Done when:** the Anchor Project and Expansion Aim are concrete, every material constraint that could change discovery is classified, and any user-owned boundary ambiguity has been resolved.

## 2. Run Bounded Discovery

After the Expansion Aim and necessary boundaries are clear, use [research assignments](references/research-assignments.md) when two or more search paths can make independent progress. The main owner keeps candidate identity, final judgment and one global budget. Do not parallelize an unresolved aim or multiply this skill's limits per worker.

Search proactively through the most relevant available primary sources: project files, official documentation, source repositories, issue trackers, release notes, and maintainer statements. Keep each material claim traceable to a file, URL, or user-provided fact.

Investigate these four paths in the order most likely to produce evidence for this Anchor:

1. **Technical adjacency** — shared protocols, formats, engines, extension points, or duplicated infrastructure.
2. **Shared user problem** — different projects whose users encounter the same underlying job or failure.
3. **Complementary capability** — another project supplies a bounded capability the Anchor can consume or expose through an adapter.
4. **Cross-ecosystem analogue** — another framework, platform, or domain solves an equivalent problem through a comparable seam.

A raw idea qualifies only when **Candidate Evidence** exists on both sides: evidence from the Anchor and at least one real adjacent project shows a shared or complementary problem and a plausible stable mechanism or integration seam. Conceptual resemblance, shared technology, or technical connectability alone does not qualify.

Stop when any bound is reached:

- 15 raw candidates have been examined;
- 5 qualifying finalists have been retained; or
- 2 distinct search paths have produced no new qualifying candidate.

Record unchecked paths and unavailable evidence in the Evidence Boundary instead of extending the search indefinitely.

**Done when:** every retained finalist has bilateral, traceable Candidate Evidence, and the report can state exactly which search paths and stopping condition bounded the result.

## 3. Classify the Seam

Classify each finalist by the smallest credible architectural move:

- **Universal Core** — remove an Incidental Constraint or extract a stable mechanism already supported by at least two concrete contexts, while specific products keep their experience layers.
- **Adapter Opportunity** — keep the Anchor's specific core and add one bounded integration seam for another concrete project or context.
- **Platform Opportunity** — expose a stable interface or protocol through which a family of specific projects could participate while retaining their own integrations.

Reject arbitrary feature bundling: combining feature sets, audiences, or brands without evidence of a shared problem and stable seam makes the project bigger, not more universal.

For every finalist, answer: **Does this reveal a deeper reusable mechanism, or merely add another feature?**

**Done when:** every finalist has exactly one type, its Necessary Boundaries remain visible, and any larger-but-not-more-universal combination has been rejected.

## 4. Judge Evidence-adjusted Value

Compare finalists qualitatively. Do not calculate numeric scores. Consider:

- strength and independence of the bilateral evidence;
- additional concrete contexts served by the same value;
- preservation of Necessary Boundaries;
- stability and testability of the proposed seam;
- coupling, reversibility, and identity dilution;
- maintenance ownership, verification matrix, compatibility commitments, and exit path.

Assign one **Candidate Disposition**:

- **Recommended** — the evidence and seam are credible, and the complete maintenance model is plausible;
- **Needs Evidence** — a named, resolvable evidence gap prevents recommendation;
- **Rejected** — a Necessary Boundary, weak shared problem, unstable seam, or maintenance cost defeats the candidate.

An interesting candidate without a plausible owner, verification surface, compatibility policy, and exit path remains Needs Evidence or Rejected. Reach and abstraction elegance cannot promote it.

**Done when:** every finalist has a reasoned disposition and every Recommended candidate passes the maintenance gate.

## 5. Design the Experiment Ladder

Give each Recommended or Needs Evidence candidate a progressive, falsifiable Experiment Ladder:

1. Verify that the adjacent context and its stated problem are real.
2. Test the proposed seam as a contract or design against the Anchor and the adjacent case.
3. Recommend a throwaway prototype only if both cheaper checks pass.

For each rung, name the evidence sought, the cheapest credible method, the passing observation, and the signal that kills or revises the candidate. Plan the ladder; leave execution to a separately authorized task.

**Done when:** each surviving candidate has a cheaper pre-prototype test and an explicit disconfirming signal.

## Discovery Report

Lead with the result, then include:

1. **Anchor Profile** — Anchor Project, Expansion Aim, preserved value, Necessary Boundaries, and Incidental Constraints.
2. **Search Coverage** — paths checked, raw candidates examined, stopping condition, and Evidence Boundary.
3. **Candidate Cards** — at most five, ordered by Evidence-adjusted Value without scores. Each card contains:
   - disposition and type;
   - adjacent project or context;
   - bilateral Candidate Evidence with sources;
   - shared or complementary problem;
   - preserved Necessary Boundaries;
   - proposed seam and why it is more than feature growth;
   - maintenance model;
   - material risks;
   - Experiment Ladder.
4. **Rejection Records** — up to three decision-relevant rejected candidates and the evidence, boundary, or cost that defeated each.
5. **Exploration Checkpoint** — invite the user to select one candidate, authorize targeted research into one named Evidence Boundary, or accept the No-expansion Result.

When no finalist clears the evidence and maintenance gates, state a No-expansion Result directly and explain why preserving the current scope is stronger than the available alternatives. Keep the report in the conversation unless the user explicitly asks to save it.

At the Exploration Checkpoint:

- A selected candidate ends discovery; state that implementation requires a new or revised User Problem.
- Targeted research receives one evidence question, one bounded source set, and one stopping condition before it begins.
- An accepted No-expansion Result completes the work without manufacturing another direction.

## Origin of the Lens

This independent skill is inspired by Anthony Fu's “The Set Theory”: remove constraints that unnecessarily shrink the target-user intersection; preserve valuable specificity; and extract shared lower layers when real needs reveal a union. “Union” here is not arbitrary project fusion. See Antfu's [React Summit source slides](https://github.com/antfu/talks/blob/main/2024-06-14/src/slides.md#L744-L786) and the [official recording and transcript](https://gitnation.com/contents/anthonys-roads-to-open-source-the-set-theory). This is an independent, unofficial skill; the links attribute the lens rather than imply authorship.
