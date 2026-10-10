---
name: pyramid-presentation
description: Builds a presentation storyline with slide-by-slide assertion headlines using the pyramid principle. Use when the user wants a deck, slides, ghost deck, or talk structured or outlined. Not for critiquing an existing deck without rewriting it; use `pyramid-audit` instead.
user-invocable: false
---

# Pyramid Presentation

## Purpose

Produce a presentation storyline whose assertion headlines carry the argument. Load `pyramid-principle-core` for structure and direct language. Add a `pyramid-source-integrity` check when facts or data materially affect the output; receive a claim packet only when strict trace mode applies.

This skill produces deck structure. It does not audit an existing deck. When the user requests a visual editing workspace, use the optional local HTML workspace described in `references/workspace.md`; visual design still follows the host's interface-design guidance.

## Visual Workspace

When the user wants to navigate, edit, or arrange slide cards, run the repository's `npm run workspace` and open its printed URL in a browser. Follow `references/workspace.md` for the JSON contract, card-to-reason relationships, and AI handoff. The user chooses each slide's big idea and supporting points. The governing answer and supporting reasons organize the overall presentation. Preserve this hierarchy while changing slide order.

Use the ordinary storyline output below when no visual workspace is requested. Do not start a server for a headlines-only request.

## Route the Request

Use this skill for slide decks, talks, ghost decks, presentation storylines, and slide-flow requests.

Hand off when:

- the artifact is a prose report or multi-section document → `pyramid-long-form`
- the artifact is an email, memo, or one-pager → `pyramid-short-form`
- the user wants an existing deck diagnosed → `pyramid-audit`
- the user wants the framework explained → `pyramid-principle-core`

## Identify the Inputs

Before drafting, the agent identifies:

1. **Audience question:** What must the audience understand or decide?
2. **Governing thought:** Which decision, recommendation, or finding did the user supply?
3. **Cleared claims:** When source integrity applies, which facts, calculations, inferences, recommendations, and limitations may the storyline use, and what source, locator, confidence, and reason accompany each data point?
4. **Shared context:** What does the audience already know?
5. **Requested depth:** Headlines only, evidence placement, transitions, or a fuller outline?

The agent asks a question only when a missing answer would materially change the storyline and the supplied material does not support a safe choice.

## Return the Requested Depth

- **Ghost deck or headlines-only request:** Return only numbered lines in the form `Slide [number] — [assertion headline]`.
- **Evidence-placement request:** Add one source-backed chart, table, quote, diagram, or fact under the headline it supports.
- **Fuller outline request:** Add source-backed evidence placement and requested transitions. Do not add design, speaker notes, or framework commentary unless requested.

The agent runs structural checks internally. It does not output SCQA labels, zone names, section-analysis headings, or self-check results.

## Build the Headline Track

The agent performs these steps in order:

1. **State the governing thought before evidence.** Use the decision, recommendation, or finding cleared for use. When the audience already has the context, make it the first substantive headline. When the audience needs context, include only the minimum Situation or Complication required to understand it first. No universal slide number applies. (`minto-p22-scqa`)
2. **Preserve the cleared claim.** Do not replace a decision with a stronger promise about what it will achieve.
3. **Write support headlines from cleared material.** Every support headline uses a fact or qualified inference permitted by the source-integrity ledger.
4. **Group same-role peers.** Every peer headline answers the same parent question and performs the same logical role. Group reasons with reasons, findings with findings, evidence with evidence, and steps with steps. Different topics may remain peers when one accurate role label describes all of them. (`minto-p96-mece`)
5. **Choose one logical order per peer set.** Use deductive, chronological, structural, or comparative order according to what the set represents. Do not mix order rules within one set. (`minto-p5-pyramid-sorting`, `minto-p63-deduction-induction`)
6. **Make one point per slide.** Each headline states one claim the audience can agree or disagree with. Split only when a headline makes more than one point; do not split solely to meet a word limit.
7. **Use the necessary number of slides.** Do not add slides to reach a preferred count or remove supported points to meet a limit. Regroup when a flat sequence becomes difficult to follow.

## Use the Source-Integrity Handoff

When source integrity applies, use only its cleared facts, derived values, interpretations, recommendations, and limitations. Apply the drafting action defined by each confidence level. This skill may select, group, order, and express the claims as headlines; it must not assign or upgrade confidence, replace a source, weaken a locator, or change numbers, scope, status, or certainty.

When strict trace mode applies, create a trace draft by appending the packet's claim ID to every factual or evaluative headline or note. A clause with no claim ID cannot appear. Hand the trace draft and original packet to a separate `pyramid-source-integrity` post-check, which validates the whole clause and strips the IDs. This skill must not approve its own factual output. If the storyline requires an unsupported bridge, change the storyline or state the limitation.

Treat examples in `references/` as structural patterns. Do not copy their names, facts, slide counts, scenarios, or conclusions into the deck.

## Structure a Full Storyline

When the user requests more than a ghost deck, use these logical functions as needed:

- **Opening:** minimum required context, then the governing thought before evidence
- **Key line:** the distinct same-role claims that support the governing thought
- **Body:** one section per key-line claim, with evidence placed under the assertion it supports
- **Closing:** the governing thought restated with only the confidence the evidence earns; include an ask only when supplied or requested

These functions do not require fixed slide positions or counts.

## Verify Before Returning

The agent checks the storyline internally and fixes any failure:

1. The cleared governing thought appears before supporting evidence; any preceding context is necessary.
2. The post-draft source-integrity check approves every headline, evidence note, and number.
3. No structural rewrite changes a claim's scope, status, or certainty.
4. Every peer set answers one parent question and performs one role.
5. The headline track remains understandable without slide bodies.
6. Each slide makes one point, and the sequence uses a valid logical order.
7. Each headline uses specific nouns and active verbs, and each support headline repeats or resolves the key term in its parent claim.
8. No example terminology, unsupported content, framework labels, or self-check appears.
9. The response matches the requested depth and contains no extra drafting commentary.

## References

- `references/storyline-patterns.md` — deck patterns; slide numbers and facts are illustrative only
- `references/slide-headline-rules.md` — assertion-headline diagnostics and examples
- `${CLAUDE_PLUGIN_ROOT}/skills/pyramid-source-integrity/SKILL.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/pyramid-principle-core/references/scqa-pattern.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/pyramid-principle-core/references/mece-grouping.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/pyramid-principle-core/references/vertical-horizontal-logic.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/pyramid-principle-core/references/rules-of-pyramid.md`
- `${CLAUDE_PLUGIN_ROOT}/docs/source-anchors.md`
