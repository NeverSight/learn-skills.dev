---
name: pyramid-short-form
description: Drafts answer-first short-form writing (email, memo, executive summary, one-pager, BLUF, Slack update, status note) under ~500 words using the pyramid principle. Use when the user wants a quick draft, not a critique. Not for reviewing existing text without rewriting; use `pyramid-audit` instead. Not for multi-section reports; use `pyramid-long-form` instead.
user-invocable: false
---

# Pyramid Short-Form

## Purpose

Draft a requested short-form artifact of about 500 words or fewer. Load `pyramid-principle-core` for structure and direct language. Add a `pyramid-source-integrity` check when facts or data materially affect the output; receive a claim packet only when strict trace mode applies.

This skill drafts. It does not explain the Pyramid Principle or audit existing writing.

## Route the Request

Use this skill for emails, Slack or IM updates, executive summaries, one-pagers, BLUF notes, short decision memos, and status updates.

Hand off when:

- the artifact needs multiple developed sections or exceeds about 500 words → `pyramid-long-form`
- the artifact is a deck or presentation storyline → `pyramid-presentation`
- the user wants existing writing diagnosed → `pyramid-audit`
- the user wants the framework explained → `pyramid-principle-core`

## Return the Requested Shape

- **Factual update or "use only these facts" request:** Return plain prose or user-requested bullets. Start with the factual answer sentence itself, not a heading. Use the cleared fact set once, then stop.
- **Recommendation or decision request:** Return the recommendation and its cleared supporting reasons. Add an ask or next step only when the claim set includes it or the user requests it.
- **Status request:** Return the current status, changes, and cleared actions or decisions.

Do not label sections `Answer`, `Support`, `SCQA`, `Governing thought`, or `Next step` unless the user requests an annotated artifact.

Treat a word limit as a maximum unless the user explicitly requires an exact length. Never add content to fill the available words.

## Identify the Inputs

Before drafting, the agent identifies:

1. **Reader question:** What must the artifact answer for its reader?
2. **Requested outcome:** Does the user want facts, a recommendation, a decision, an ask, or a status update?
3. **Cleared claims:** When source integrity applies, which facts, calculations, inferences, recommendations, and limitations may the artifact use, and what source, locator, confidence, and reason accompany each data point?
4. **Medium:** Email, memo, one-pager, Slack, or another short form?
5. **Constraints:** Audience, length, tone, deadline, and sensitivity.

The agent asks a question only when a missing answer would materially change the artifact and the supplied evidence does not support a safe choice.

## Draft the Artifact

The agent performs these steps in order:

1. **Write the governing thought.** It directly answers the reader question in one declarative sentence.
   - For a factual update, the governing thought synthesizes cleared facts. It does not recommend action.
   - For a recommendation or decision request, the governing thought states the action the user supplied or requested.
   - When the cleared claims support multiple materially different answers, the agent asks rather than choosing one without support.
2. **Add only necessary context.** If the reader cannot understand the governing thought without a Situation or Complication, place the minimum required context first. Otherwise begin with the governing thought. (`minto-p22-scqa`)
3. **Select the supporting points.** Retain every material point required to support the governing thought. Remove repetition. Do not add or delete points to reach a preferred count.
4. **Test the peer set.** Every peer answers the same parent question and performs the same logical role. Group reasons with reasons, facts with facts, risks with risks, and actions with actions. Different topics may remain peers when one accurate role label describes all of them. (`minto-p96-mece`)
5. **Choose prose or bullets.** Use prose when supports depend on sequence or connective reasoning. Use complete-sentence bullets when exposing independent same-role supports makes the logic easier to scan.
6. **Return only the artifact.** Do not expose drafting notes, assumptions, SCQA labels, self-checks, or framework labels.

## Use the Source-Integrity Handoff

When source integrity applies, use only its cleared facts, derived values, interpretations, recommendations, and limitations. Apply the drafting action defined by each confidence level. This skill may select, group, order, and express the claims; it must not assign or upgrade confidence, replace a source, weaken a locator, or change numbers, scope, status, or certainty.

When strict trace mode applies, create a trace draft by appending the packet's claim ID to every factual or evaluative clause. A clause with no claim ID cannot appear. Hand the trace draft and original packet to a separate `pyramid-source-integrity` post-check, which validates the whole clause and strips the IDs. This skill must not approve its own factual output.

Treat examples in `references/` as structural patterns. Do not copy their names, facts, scenarios, or conclusions into the artifact.

## Adapt to the Medium

- **Factual update:** Integrate the factual synthesis and distinct facts without repeating them. Stop after the last supplied fact.
- **Recommendation or decision memo:** State the supplied or requested recommendation, then its same-role reasons. Include an ask or next step only when supplied or requested.
- **Status update:** State the current status, what changed, and cleared actions or decisions.
- **Email:** Use the subject line for the governing thought when that helps the recipient scan. Do not repeat it mechanically in the body.
- **Slack or BLUF:** Remove greetings and sign-offs unless the user requests them. Use bullets only when they improve scanning.

## Verify Before Returning

The agent checks the draft internally and fixes any failure:

1. The governing thought answers the reader question before supporting points; any preceding context is necessary.
2. The post-draft source-integrity check approves every factual sentence and number.
3. Every peer answers one parent question and performs one role.
4. The draft retains all material support without forcing a preferred count.
5. The format exposes the logic instead of decorating it.
6. Each sentence makes one claim with a specific subject and active verb; each sentence or bullet connects clearly to its parent or preceding sentence.
7. No example terminology or unsupported content appears.
8. The response contains only the requested artifact. It does not print `Answer:`, `Support:`, `SCQA:`, `Governing thought:`, `Next step:`, or the self-check.

## References

- `references/patterns.md` — medium-specific patterns; use their structure, not their facts
- `references/examples.md` — paired examples; use them only to recognize structural moves
- `${CLAUDE_PLUGIN_ROOT}/skills/pyramid-source-integrity/SKILL.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/pyramid-principle-core/references/scqa-pattern.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/pyramid-principle-core/references/mece-grouping.md`
- `${CLAUDE_PLUGIN_ROOT}/docs/source-anchors.md`
