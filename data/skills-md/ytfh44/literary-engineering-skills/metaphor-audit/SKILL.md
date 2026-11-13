---
name: metaphor-audit
description: Use when a metaphor, simile, analogy, or figurative comparison feels generic, ornamental, cliché, overlong, or interchangeable with thousands of objects; use when deciding whether a literal description is stronger than an image, or when a character's habitual metaphor is doing voice work; use before generating new metaphors — audit first, "no metaphor needed" is a valid verdict; use for ablation tests (delete the image, record what disappears).
license: Apache-2.0
---

# Metaphor Audit

## Use when

A comparison spends words to transfer traits from one domain to another.
Test whether those transferred traits sharpen this object in this scene —
before anyone proposes a "better" metaphor.

## Do not use when

Do not add metaphor merely because prose feels plain. The missing mechanism
may be event structure, viewpoint, or evidence. Do not treat this skill as a
metaphor generator: generation happens only when the audit shows a load-
bearing gap and the user asks for wording. "这段太平了" must never route
automatically to "再想三个比喻."

## Core test

**A metaphor earns its words when its source domain selects traits peculiar
to this object here.**

A source that contributes only "dark," "cold," "large," "angry," or "sad"
usually spends too much language on a shared property. The audit question
comes first: why is a comparison here at all?

## Workflow

1. Name the target object and the exact trait the sentence needs.
2. List what the source domain adds beyond that trait: shape, mechanism,
   timing, texture, relation, consequence.
3. Delete the metaphor. Record what information disappears.
4. If nothing disappears except intensity or decoration, prefer the literal
   sentence or a better source — or nothing at all.
5. If the metaphor survives, trim every transferred trait the scene does not
   use.
6. Check whether the image steals agency or viewpoint from the event around
   it.
7. Only when the audit shows a real gap and the user wants one: propose a
   source that contributes the missing trait.

## Utility axes

Metaphor value is not one number. Score what a comparison actually does:

- **semantic gain** — structure, mechanism, or relation the target lacked;
- **perceptual gain** — a way of seeing, not a label;
- **voice gain** — the comparison belongs to this speaker (a cliché in the
  mouth of a cliché-speaking character can be high-value voice work);
- **rhythmic gain** — the image carries the sentence's timing;
- **motif gain** — the image feeds a repeated element that changes work
  state;
- **cultural-memory gain** — an old comparison with real recall weight;
- **comic gain** — the mismatch itself is the event;
- **estrangement gain** — the familiar is made strange on purpose;
- **processing cost** — words and cognition the reader must spend;
- **interference cost** — the image distracts from the scene's actual
  object or agency.

A comparison with `semantic gain = 0` may still be right (voice, comic,
motif). A clever one with high processing cost and no other gain is
decoration. "Delete it" and "keep it" are both complete answers when
accompanied by the axis that decided them.

## Hard rules

- Novelty is not precision.
- Cliché is not automatic failure; a conventional comparison can be exact.
- Do not compare one abstraction to another abstraction and call it
  concrete.
- Do not stack source domains unless the collision itself is the point.
- Prefer one discriminating trait to five atmospheric ones.
- Do not generate a metaphor to fix a sentence that needed a verb, a
  viewpoint, or an event.

## Minimal pair

> 夜色像墨一样黑。
>
> 雨把巷口的灯揉成一团旧墨。

The first buys "black" twice. The second transfers spreading, blurred edges,
and material thickness to a particular optical event. The gain is not
novelty; it is structure.

Audit-first pair:

> 他像一头困兽。
>
> 他在会议桌下把手机攥得发烫。

If the scene's information is the suppressed tension, the second carries it
without importing a zoo. If the character is literally caged and pacing, the
first may be exact. The audit decides; neither is "more literary."

## Counterexamples

- "纸薄得像蝉翼。" Conventional, but if translucence and fragility are the
  exact needed traits, the comparison may be efficient.
- "他像父亲一样停顿了两秒。" Not decorative if the inherited timing is the
  scene's information.
- A character who always speaks in sports metaphors: the clichés are the
  voice. Do not replace them with fresher images.

## Rule strength

**Role/domain tests.** No universal preference for or against metaphor, no
novelty requirement, no frequency threshold. The audit classifies what the
comparison does in context and prices its cost. Deletion and substitution
tests are reliable; "this metaphor is bad" as a standalone claim is not.

## Read next

- [utility-axes.md](references/utility-axes.md) for the axis checklist and
  its failure cases.
- [domain-selection.md](references/domain-selection.md) for choosing source
  domains by relation, not mood.
- [stale-mappings.md](references/stale-mappings.md) for cliché diagnosis
  without blacklist logic.
- [metaphor-ablation.md](references/metaphor-ablation.md) for deletion and
  substitution tests.

## Return shape

Report **target trait -> source contribution -> axis verdict -> keep/revise/
delete/no-metaphor**. If proposing a new metaphor, state the extra trait it
contributes and the axis that justifies it before giving the wording.
