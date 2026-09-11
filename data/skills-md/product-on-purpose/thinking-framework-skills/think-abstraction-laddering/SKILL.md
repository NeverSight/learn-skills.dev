---
name: think-abstraction-laddering
description: Builds an abstraction ladder that moves a problem up ("why / to what end?") and down ("how / what specifically?") to locate the right altitude to work at, then marks one rung as the working level. Use when a problem is stated as a bare solution with an unstated purpose, as a vague aspiration with no concrete handle, when people are arguing past each other at different levels, or before committing effort at an altitude nobody chose on purpose.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.abstraction-laddering
  family: problem-framing
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Abstraction Laddering

Every problem arrives at some altitude, and the altitude is usually accidental: it is wherever someone happened to be standing when they noticed it. Too low and you optimize a detail that does not matter ("make the button blue"); too high and you produce a true but useless aspiration ("delight the customer"). Abstraction laddering moves the problem along one vertical axis - up by asking "why? / to what end?" and down by asking "how? / what specifically?" - to find the altitude at which it is actually workable. The output is an **abstraction ladder**, an ordered set of rungs with one chosen as the working level, not a discussion.

## When to Use

- A request names a bare solution ("add a dashboard", "build an integration") but the purpose it serves is unstated.
- A problem is stated as a vague aspiration ("improve engagement", "be more strategic") with no concrete handle to act on.
- People are arguing past each other and may simply be working at different levels of the same problem.
- Before committing effort, to decide deliberately at what altitude to attack a problem rather than inheriting the accidental one.

## When NOT to Use

- **Altitude is not the issue.** If the problem needs a different kind of reframing - a stakeholder shift, an inversion, an is/is-not boundary, or weighing several rival framings - use `think-problem-restatement`, which generates those moves and converges on a chosen frame. This skill only moves up and down one axis.
- **The right level is already clear and agreed.** Building a ladder for a well-located problem manufactures motion and wastes effort.
- **To generate or choose solutions.** Going down lists more concrete sub-problems to consider, not a chosen solution. Use an ideation skill (Question Burst, SCAMPER) to generate and a decision skill (Decision Option Review) to choose.
- **To decompose a problem into all its parts.** A ladder is a single vertical chain, not a branching breakdown. For that, use an issue tree.

## Instructions

When asked to find the right altitude for a problem, follow these steps:

1. **Capture the entry rung.** Record the problem exactly as given, in one line. This is where the ladder starts; mark it as the entry rung. If the altitude is already clear and agreed, say so and stop.
2. **Climb up: ask "why? / to what end?"** Repeatedly replace the current rung with the broader purpose it serves ("we do this so that..."). Each step up should be a genuine purpose, not a reword. Stop climbing when the next rung is so broad it would be true of almost any project (that rung is too high to work at).
3. **Descend: ask "how? / what specifically?"** From the entry rung, repeatedly replace the current rung with a more concrete instance or sub-problem ("concretely, that means..."). Note where a rung has more than one plausible "how"; that fork is a signal there are options at that altitude. Stop descending when a rung is so specific it is a single implementation detail.
4. **Lay out the ladder.** Order all rungs from most abstract (top) to most concrete (bottom) as a single vertical chain. Keep the why-relationship reading upward and the how-relationship reading downward explicit. Do not let it sprawl sideways into a pile of loosely related ideas; that is a different artifact.
5. **Select the working altitude.** Choose exactly one rung as the level to actually work the problem at - high enough to leave room for real options, low enough to be actionable - and give a one- or two-sentence rationale tied to the user's actual goal. Converge; a ladder with no chosen rung is incomplete.
6. **Emit the abstraction ladder.** Produce the artifact in `references/TEMPLATE.md`: a short summary above an ordered ladder with the entry rung marked and the working rung selected.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the filled ladder plus its summary, with one rung chosen as the working altitude, not a prose essay.

## Quality Checklist

Before finalizing, verify:

- [ ] The entry rung (problem as given) is captured verbatim and marked on the ladder.
- [ ] Up-steps are genuine purposes ("why / to what end"), not rewordings; down-steps are genuinely more concrete ("how / what specifically").
- [ ] The ladder is a single vertical chain ordered abstract-to-concrete, not a sideways pile of related ideas or a branching decomposition.
- [ ] Climbing stopped before the uselessly-universal rung, and descending stopped before bare implementation detail.
- [ ] Exactly one rung is selected as the working altitude, with a rationale tied to the user's actual goal.
- [ ] The output is the ladder artifact, not prose.
- [ ] No overclaiming: the skill makes the altitude choice explicit and deliberate; it does not guarantee a better solution or a correct level (see `evidence/dossier.md`).

## Evidence

Tier **P** (practitioner). That how a problem is framed - including at what level of abstraction - affects the solutions found has moderate support in the problem-framing literature (problem-finding research; Nutt on decision failure from poor definition; Wedell-Wedellsborg, HBR 2017), and abstraction is a well-described dimension of language (Hayakawa, *Language in Thought and Action*, 1939). But there is **no controlled study** isolating "abstraction laddering" as a named technique against a baseline; it is a widely-taught design-facilitation method with face validity and a clear mechanism, not a measured one. The supporting evidence concerns framing in general, not this exercise specifically, and is transferred from human practice, not AI-validated. Full grading, sources, and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed abstraction ladder on a real decision.
