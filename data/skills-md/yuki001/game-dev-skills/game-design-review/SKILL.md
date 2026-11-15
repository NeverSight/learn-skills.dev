---
name: game-design-review
description: Review, critique, compare, improve, or stress-test an existing game concept, GDD, mechanic, puzzle, economy, level, theme, emotional arc, interface, narrative, social feature, prototype, pitch, or playtest result. Use when the user asks what is weak, risky, unclear, unbalanced, contradictory, insufficiently engaging, or worth validating next in a game design. Produce evidence-based findings, explicit tradeoffs, and the smallest useful prototype or playtest experiment.
---

# Game Design Review

Review a design by tracing how rules and presentation are likely to shape player decisions and experience. Treat the review as a decision aid, not a universal checklist or a substitute for playtesting.

## Responsibility boundary

- Use this skill when a design object or decision already exists and needs examination.
- This skill is self-contained. Do not assume any other skill, workflow, repository layout, document set, or game engine exists.
- When the user needs a new formal design document rather than a review, return the clarified direction, constraints, open questions, and validation criteria needed to author it.
- Do not convert a design recommendation directly into code structure, engine APIs, or implementation tasks.

## Review modes

Every review shares the same spine:

1. **Name the review object.** The whole game, one loop, one mechanic, a level, an interface flow, a narrative beat, a social feature, or a production choice.
2. **State the decision at stake.** A choice or testable question; if none exists, the most consequential unresolved assumption.
3. **Build an evidence baseline.** Audience, rules, constraints, prototype behavior, and playtest observations, separating repeated patterns from anecdotes; mark each material statement as `confirmed`, `assumed`, or `unknown`.
4. **Close the review.** Prioritized findings, the smallest useful intervention, and a validation experiment.

The modes differ in how the examination between these ends is executed. Pick the narrowest mode that fits; when in doubt, use the comprehensive review.

### Comprehensive review (default)

Use when the direction is chosen, formal materials exist to examine (documents, prototypes, telemetry, or playtest records), and the goal is a full-coverage review for weaknesses, risks, and contradictions.

1. **Exclude, then cover.** Exclude only the references the review object clearly makes irrelevant, keeping at least 6; record each exclusion and its reason, and state the unreviewed domains in the final report.
2. **Batch and delegate.** Group the rest into batches of 2 to 4 related domains, one batch per read-only subagent as described in "Delegating a review to subagents" below; work through the batches sequentially yourself when subagents are unavailable.
3. **Trace effects.** Each batch reader connects each design choice to player information, decision, action, feedback, and consequence, distinguishing symptom from cause.
4. **Merge and reconcile.** Merge duplicates that share a root cause, normalize severity, and run a cross-domain contradiction pass, treating each contradiction as a finding of its own; do not emit one undifferentiated checklist.

### Focused review

Use when everything to be reviewed fits in the conversation: the design or the question is short, or exists only as notes or keywords in the user's message, with no formal documents to read.

1. Read 2 or 3 relevant references from the routing table yourself.
2. Trace effects as in the comprehensive review and return only the findings that could change the decision.

### Exploratory review

Use when no direction has been chosen yet: the design is too immature for fault-finding, and the goal is to outline candidate directions plus a test that can distinguish them.

1. Identify the player promise and the central uncertainty.
2. Outline 2 or 3 coherent directions.
3. Define a small test that can distinguish them, and stop before expanding into a full design document.

### Comparative review

Use when the goal is to choose between 2 or more defined options, whatever their material volume.

1. Apply the same evidence and criteria to every option; do not let one option receive a stricter review.
2. When the comparison spans several domains, you may delegate one subagent per option, each applying the same reference set.
3. Merge the per-option findings as in the comprehensive review.

## Delegating a review to subagents

Subagents do not share this conversation, so brief each one with everything it needs:

- the review object and where to find the design materials;
- the decision at stake and the evidence baseline, so it does not re-open settled facts;
- its assigned reference paths, with instruction to read them fully before analyzing;
- the finding-quality bar below, so findings carry enough substance to merge;
- the boundary: return design findings and a recommended smallest intervention per batch, not implementation tasks.

Subagent reports may take any form that carries that substance. Never let a subagent's severity or priority pass through unreviewed; merging is your job, not theirs.

## Reference routing

| Review concern | Read | Focus |
| --- | --- | --- |
| Audience, intended experience, motivation, comprehension | `references/experience-and-audience.md` | Player promise, motivation chain, pleasure inventory, learning assumptions, experience gaps |
| Core concept, theme, emotion, fantasy, aesthetic identity, curiosity and novelty | `references/concept-theme-and-emotion.md` | Concept clarity, imaginative space, thematic coherence, emotional causes, expressive unity, memorable identity |
| Actions, goals, rules, information, agency, complexity and strategy | `references/actions-rules-and-agency.md` | Goal hierarchy, decision quality, performance judgment, rule legibility, structure and state, dominant behavior, systemic character |
| Challenge, skill profile, risk, punishment, rewards, progression, economy and replay depth | `references/challenge-progression-and-economy.md` | Difficulty shape, skill demand, fairness, expected return, reward meaning, time structure, sources/sinks, viable paths |
| Puzzles, deductions, hints, bottlenecks and visible progress | `references/puzzles-and-problem-solving.md` | Problem representation, reasoning chain, solution structure, recovery and hint escalation |
| Level space, encounters, navigation and pacing | `references/space-level-and-pacing.md` | Route choice, readability, rhythm, recovery, spatial pressure |
| Attention curve, memorable moments, indirect guidance and presence | `references/attention-guidance-and-presence.md` | Interest over time, voluntary guidance, freedom, interruption, projection and retelling |
| Controls, UI, feedback and practical accessibility | `references/interface-feedback-and-accessibility.md` | Intention-to-action loop, information timing, feedback richness, error recovery, input and perception barriers |
| Narrative, world, characters and player-authored stories | `references/narrative-world-and-characters.md` | Playable story delivery, story structure, world causality, role, agency, status and character function |
| Competition, cooperation, friendship, community and harmful behavior | `references/social-community-and-safety.md` | Incentives between players, trust, relationship continuity, expression, moderation and spectator clarity |
| Scope, prototypes, playtests, technology, market, distribution, business and responsibility | `references/production-validation-and-responsibility.md` | Production fit, evidence quality, risk retirement, market viability, sustainability and player welfare |

## Finding quality

A useful finding contains:

- **Observation:** what the current design or evidence shows;
- **Mechanism:** how it may alter player understanding, choice, behavior, or feeling;
- **Evidence status:** confirmed fact, supported inference, assumption, or unknown;
- **Impact:** what fails if the issue is real;
- **Recommendation:** the smallest change worth trying;
- **Validation:** what result would support or reject the recommendation.

Avoid findings based only on personal taste. When evidence is missing, write a hypothesis and a test rather than presenting a prediction as fact.

## Report structure

Use the shortest report that resolves the request. For a formal review, use:

```markdown
# Design Review: [object]

## Decision at stake
[The choice or uncertainty this review should resolve.]

## Evidence baseline
- Confirmed: ...
- Assumed: ...
- Unknown: ...

## Priority findings
### [Severity] [Finding]
- Observation:
- Mechanism:
- Evidence status:
- Recommendation:
- Validation:

## Tradeoffs
[What improves, what may get worse, and who is affected.]

## Next experiment
[Smallest build, simulation, or playtest; participants; observable signals; decision rule.]
```

Use `critical`, `major`, or `minor` only when severity helps prioritization:

- `critical`: undermines the core promise or prevents meaningful validation;
- `major`: materially harms a common player path or creates expensive downstream rework;
- `minor`: local friction or polish issue that does not invalidate the current direction.

## Guardrails

- Do not fabricate player reactions, telemetry, market facts, or playtest evidence.
- Do not hide conflicting goals. State the tradeoff and identify who makes the final decision.
- Do not expand the feature set merely to answer a design weakness; removal, clarification, or a smaller rule change may be better.
- Do not prescribe technical architecture. Express confirmed design constraints and validation criteria so a later technical process can consume them without requiring a particular tool or workflow.
