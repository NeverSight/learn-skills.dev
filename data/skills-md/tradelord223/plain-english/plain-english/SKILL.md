---
name: plain-english
description: >-
  Turn technical evidence into clear, natural, audience-appropriate user-facing
  explanations without changing meaning, certainty, obligations, operational
  state, or exact technical tokens. Use for change summaries, status and error
  reports, walkthroughs, handoffs, release notes, how or why explanations, and
  requests to make an agent's technical communication sound more human.
  Do not rewrite raw code, commands, logs, quoted errors, or specifications;
  explain those artifacts separately.
---

# Plain English for Technical Work

Make the answer easier to understand and act on without changing what the
source proves. Plain English is a translation of behavior for a reader, not a
dictionary of simpler substitutes.

## Work from truth anchors

Before rewriting, identify the details that must survive compression:

- the outcome and current operational state
- the evidence and what was or was not checked
- certainty: confirmed, likely, possible, estimated, or unknown
- obligation: permission, capability, recommendation, or requirement
- scope, conditions, exceptions, negation, and cause-and-effect claims
- numbers, comparisons, sequence, ownership, risks, blockers, and next actions
- exact names, paths, commands, identifiers, configuration keys, and quoted
  errors that the reader may need to find or verify

Do not promote a claim while simplifying it. In particular, never turn:

- possible into confirmed
- *can* into *will*, *should* into *must*, or permission into a commitment
- planned or attempted into completed
- completed into tested, verified in the target environment, live, or
  customer-visible
- local or staging behavior into production behavior
- some, sampled, or one case into all cases
- correlation or sequence into causation

When the source lacks a required detail, preserve the unknown. Ask a focused
question only when the missing answer materially changes what the reader should
believe or do.

For content with uncertainty, obligations, operational-state language,
comparisons, negation, causal claims, or high-stakes consequences, read
[the precision contract](references/precision-contract.md) before drafting.

## Match the reader and depth

Infer the audience from the request and conversation:

- **Expert:** keep standard domain terms and focus on the decision or mechanism.
- **Nontechnical:** lead with the practical outcome, explain the behavior in
  common words, and include the exact term once only when it helps later work.
- **Mixed:** use two layers: a common-language outcome first, then the exact
  technical evidence or mechanism needed by specialists.
- **Unknown:** define one important unfamiliar term at first use, then use one
  consistent name for it.

Honor a requested length or format, but do not compress below the truth anchors.
If the requested brevity would hide a risk, failed check, uncertainty, or
required action, keep that detail and cut background or repetition instead.

Plain does not mean childish. Do not explain basic ideas the reader has already
shown they understand.

## Sound like a person, not a response template

Write to this reader about this situation. Do not flatten every answer into the
same polished corporate voice.

- Preserve a writer's useful voice signals: directness, contractions, sentence
  rhythm, technical density, humor, asides, stance, and honest uncertainty.
- If the user provides a writing sample, follow its habits without copying its
  phrases or preserving errors that obscure meaning.
- Prefer a concrete actor, action, result, or observed detail over abstract
  claims about importance, quality, or progress.
- Trust the reader once a point is clear. Cut throat-clearing, restatements,
  forced takeaways, and generic positive endings.
- Break mechanical symmetry when it is not helping: repeated sentence shapes,
  forced groups of three, synonym cycling, and a bold mini-heading on every
  bullet.
- Vary rhythm by ear and purpose, not randomly. Human does not mean casual,
  quirky, opinionated, or grammatically rough in every context.

When the user asks for a more human, natural, conversational, less corporate,
or less AI-sounding answer; provides a voice sample; or the draft sounds
formulaic, read [the human-voice guide](references/human-voice.md) before
drafting. Do not deliberately introduce mistakes, ban harmless words, or claim
to beat AI detectors.

## Match the job

Choose the smallest response shape that completes the request:

| Job | Lead with | Add only when useful |
|-----|-----------|----------------------|
| Change or release summary | User-visible outcome | Exact behavior, validation, compatibility, remaining risk |
| Status | Done, in progress, or blocked | Evidence, unverified scope, next action |
| Error report | What failed and its impact | Exact error, confirmed or possible cause, recovery step |
| How or why | Direct answer | Mechanism, example, boundary |
| Walkthrough | Goal and first action | Ordered steps, checkpoints, recovery |
| Handoff | Current state | Decisions, evidence, open work, exact next command |

Do not force every answer into the same template. Use headings, lists, or tables
only when they make multiple facts easier to compare or follow.

## Explain behavior, not vocabulary

Prefer common words when they carry the same meaning: *use* instead of
*leverage*, *before* instead of *prior to*, and *to* instead of *in order to*.

Do not apply universal jargon swaps:

- `serialize` means "turn into JSON" only when the format is JSON.
- `deploy` does not mean "put live" when the target is staging or local.
- `schema` can be a database layout, API contract, or validation rule.
- `middleware` can run outside an HTTP request pipeline.
- `idempotent` is not merely "safe to run twice"; explain the actual retry or
  duplicate-effect behavior.

When a term matters, explain what it does here. Keep the exact term when it is
shorter, the reader knows it, or the reader must search for it later.

## Keep artifacts exact

- Put file names, functions, types, flags, commands, and configuration keys in
  code formatting.
- Quote error text exactly, then explain it separately.
- For code changes, prefer: `[file or function]` + what it does + what changed.
- Do not rename a concept in prose if the reader must find that same name in
  code or an interface.
- Do not rewrite source code, commands, raw logs, quoted evidence, or
  load-bearing specifications unless the user explicitly asks to edit that
  artifact. Improve the explanation around it.

Example:

> `auth.ts` checks the login token on each request. It now rejects expired
> tokens. The unit test passed; the browser login flow was not tested.

## Write naturally

- Lead with the outcome, direct answer, or blocker rather than the investigation
  story.
- Use compact paragraphs and sentences that are easy to track.
- Give enough detail to understand, act, or verify. Stop there.
- Cut greetings, praise, repeated conclusions, decorative metaphors, stacked
  hedges, vague claims, and routine tool narration.
- Distinguish confirmed facts, supported inferences, and unknowns in the words
  themselves. Add labels only when the distinction would otherwise be unclear.
- Do not invent an owner, deadline, sequence, cause, recommendation, or next
  step merely to make the answer feel complete.
- Keep a supported opinion or human reaction when it belongs to the writer.
  Do not manufacture one when the source is neutral.

## Final semantic check

Before sending, compare the draft with the source:

1. Does the first useful sentence give the outcome, answer, or blocker?
2. Can this reader understand or act without guessing what a key term means?
3. Did every truth anchor survive, including negation and exceptions?
4. Did any claim become more certain, mandatory, complete, broad, causal, or
   production-ready than the evidence supports?
5. Are exact tokens available wherever the reader needs to find or verify them?
6. Are risks, blockers, failed or skipped checks, and required user actions still
   visible?
7. Can any remaining sentence be removed without losing meaning or usefulness?
8. Does the answer sound written for this reader, or could it have come from a
   generic response template?

If simplifying would fail checks 3 through 6, keep the precise wording and
explain it.
