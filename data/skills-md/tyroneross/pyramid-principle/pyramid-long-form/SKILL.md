---
name: pyramid-long-form
description: Drafts or restructures a multi-section document (report, brief, proposal, whitepaper, strategy doc, research writeup) using the Pyramid Principle. Use when the user wants a new document built or an existing one reorganized. Not for critiquing a draft without rewriting it; use `pyramid-audit` instead. Not for single-page notes under 500 words; use `pyramid-short-form` instead.
user-invocable: false
---

# Pyramid Long-Form

## Purpose

Structure or draft a multi-section professional document. Load `pyramid-principle-core` for structure and direct language. Add a `pyramid-source-integrity` check when facts or data materially affect the output; receive a claim packet only when strict trace mode applies.

This skill handles documents that require developed sections or usually exceed about 500 words. It does not audit existing writing or produce slide storylines.

## Route the Request

Use this skill for reports, briefs, proposals, research writeups, decision documents, strategy documents, and whitepapers.

Hand off when:

- the artifact is an email, Slack update, executive summary, or one-pager → `pyramid-short-form`
- the artifact is a deck or presentation storyline → `pyramid-presentation`
- the user wants existing writing diagnosed → `pyramid-audit`
- the user wants the framework explained → `pyramid-principle-core`

## Identify the Inputs

Before structuring the document, the agent identifies:

1. **Reader question:** What must the document answer?
2. **Governing thought:** Which decision, recommendation, or finding did the user supply?
3. **Cleared claims:** When source integrity applies, which facts, calculations, inferences, recommendations, and limitations may the document use, and what source, locator, confidence, and reason accompany each data point?
4. **Requested depth:** Outline, detailed outline, section draft, or full document?
5. **Constraints:** Audience, length, tone, required sections, sensitivity, and citation format.

The agent asks a question only when a missing answer would materially change the document and the supplied evidence does not support a safe choice.

## Return the Requested Depth

- **Outline:** Return the title, actual decision or governing claim, section claims, and nested source-backed supports. The eventual document word budget does not set the outline's length. Do not draft body prose or output framework commentary.
- **Detailed outline:** Add subsection claims, evidence placement, and source notes.
- **Section draft:** Draft only the requested section and preserve its position in the document logic.
- **Full document:** Draft the complete document after the outline passes the internal checks.

Do not output SCQA, key-line, reasoning-mode, assumption, or self-check labels unless the user requests an annotated structure.

When the user requests a source-bound outline or says to use only supplied facts:

- build only from the claim set and evidence limits cleared by `pyramid-source-integrity`;
- omit generic introduction, implementation, expected-outcome, and conclusion sections unless the user requests them and the cleared claim set supplies their content;
- do not add a section merely because it is common in that document type;
- place a requested but unverified expected result under `Evidence limits`, not in the storyline as a prediction.

The source-bound outline starts with the actual title and decision sentence, then uses only asserted section headings with their supplied facts. It may end with one `Evidence limits` section. It must not print the drafting labels `Title`, `Governing Thought`, `Fact`, `Inference`, `Decision`, `Rationale`, or `End of Outline`.

Unless the cleared claim set supplies their content, the agent must not create sections named or serving as `Introduction`, `Implementation`, `Expected Outcomes`, `Benefits`, `Next Steps`, or `Conclusion`.

If the cleared decision includes an intervention whose effect remains unverified, state the intervention in the decision sentence only. Put the missing outcome evidence under `Evidence limits` rather than creating a benefits section.

Use this final syntax for a source-bound outline:

- first line: a Markdown `#` title with no `Title` label;
- second paragraph: the supplied decision sentence with no `Governing Thought`, `Governing Claim`, or `Decision` label;
- remaining `##` sections: source-backed claims and their supplied facts;
- optional final `## Evidence limits` section;
- stop after the final section without an `End of Outline` label.

## Build the Architecture

The agent completes the architecture before drafting prose:

1. **Write the governing thought.** Use the decision, recommendation, or finding cleared for use. Do not replace it with a stronger outcome claim.
2. **Add only necessary introduction context.** Include the minimum Situation or Complication the reader needs, then state the governing thought before the document body. When the context is shared, begin with the governing thought. (`minto-p22-scqa`)
3. **Select section claims.** Use the distinct claims required to support the governing thought. Do not add or remove sections to reach a preferred count.
4. **Test each peer set.** Every section or subsection at one level answers the same parent question and performs the same logical role. Different topics may remain peers when one accurate role label describes all of them. (`minto-p96-mece`)
5. **Choose one order per peer set.** Use deductive, chronological, structural, or comparative order only when the material shows that order. (`minto-p5-pyramid-sorting`, `minto-p63-deduction-induction`)
6. **Place evidence under the claim it supports.** Do not create a separate background or data section when the material belongs under a specific claim.
7. **Nest only when needed.** Add a lower level when a section claim requires multiple distinct supports. Do not create depth to make the outline look complete.

## Draft the Prose

When the user requests prose, the agent:

1. opens each section with the claim that section establishes;
2. places source-backed evidence and explanation beneath that claim;
3. keeps each paragraph tied to one outline node;
4. uses transitions only when they clarify the logical relationship between peer sections;
5. revises the architecture when new evidence changes the governing thought instead of writing around an outdated outline;
6. concludes by restating the governing thought only when the document needs a conclusion, without recapping every section.

## Use the Source-Integrity Handoff

When source integrity applies, use only its cleared facts, derived values, interpretations, recommendations, and limitations. Apply the drafting action defined by each confidence level. This skill may select, group, order, nest, and express the claims; it must not assign or upgrade confidence, replace a source, weaken a locator, or change numbers, scope, status, or certainty.

When strict trace mode applies, create a trace draft by appending the packet's claim ID to every factual or evaluative clause. A clause with no claim ID cannot appear. Hand the trace draft and original packet to a separate `pyramid-source-integrity` post-check, which validates the whole clause and strips the IDs. This skill must not approve its own factual output. If a section requires unsupported content, change the architecture or state the evidence limit.

Treat examples as structural patterns. Do not copy their names, facts, terminology, scenarios, or conclusions into the artifact.

## Format the Outline

For an unannotated outline:

- state the actual governing claim near the top without labeling it `Governing Thought`;
- use asserted section headings, not topic labels;
- place only the facts or qualified interpretations that support each heading beneath it;
- state a source limitation when an aggregate fact cannot support a narrower attribution;
- include an ask, next step, or expected result only when supplied or requested.

For a source-bound outline, stop after the final source-backed section. Do not add prose to approach the eventual document word budget.

## Verify Before Returning

The agent checks the architecture and requested artifact internally and fixes any failure:

1. The cleared governing thought answers the reader question before body support.
2. Every heading is a claim supported by material beneath it.
3. The post-draft source-integrity check approves every factual statement, heading, table entry, and number.
4. No structural rewrite changes a claim's scope, status, or certainty.
5. Every peer set answers one parent question, performs one role, and uses one logical order.
6. The outline retains every material support without forcing a preferred count or depth.
7. Each sentence makes one claim with a specific subject and active verb; sections carry precise key terms from parent claims through their support.
8. No example terminology, framework labels, or self-check appears.
9. The response matches the requested depth and contains only the requested artifact.

## References

- `references/report-skeleton.md` — detailed document patterns; use structure only
- `references/key-line-examples.md` — grouping examples; never use their facts as task evidence
- `${CLAUDE_PLUGIN_ROOT}/skills/pyramid-source-integrity/SKILL.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/pyramid-principle-core/references/rules-of-pyramid.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/pyramid-principle-core/references/scqa-pattern.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/pyramid-principle-core/references/vertical-horizontal-logic.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/pyramid-principle-core/references/mece-grouping.md`
- `${CLAUDE_PLUGIN_ROOT}/docs/source-anchors.md`
