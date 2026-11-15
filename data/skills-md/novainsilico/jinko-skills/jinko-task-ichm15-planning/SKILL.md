---
name: jinko-task-ichm15-planning
description: >-
  From a scientific question of interest, get recommendations on preparing and formatting the documentation related to ICHM15 planning phase, which covers ICH M15 key assessments elements, technical criteria evaluation of model and model outcomes, appropriateness of Proposed MIDD and a Model Analysis Planning (MAP) document. Optionally upload the recommended documentation in Jinkō. 
compatibility: >-
  Jinkō upload requires jinko-document, jinko-sdk-setup, and project write access.
metadata:  
  author: Nova In Silico
  requires_sdk: ">=1.16,<2.0"
license: MIT
---

# ICH M15 MIDD Planning

From a scientific question of interest, use this skill to get guidance and generate ICHM15 documentation related to the planning phase of an MIDD project, as described in the final ICHM15 recommendations (ICHM15 step 5, June 2026).

See `references/terms.md` for the shared terminology used by the ICH M15 review skills.

## When to use this skill
Use this skill when the user wants guidance that frames the assessment correctly, includes all required elements with ratings and justifications, and exposes missing evidence clearly.

Use it for:

- Question of Interest and Context of Use framing (§2.1.1–2.1.2)
- Model Influence, Consequence of Wrong Decision, Model Risk, and Model Impact (§2.1.3–2.1.6)
- Technical Criteria and Appropriateness of Proposed MIDD (§2.2.1–2.2.2, planning stage)
- Recommendation of a Model Analysis Planning (MAP) document

Note that this skill focuses specifically on the planning stage: drug developers are planning MIDD activities, before model outcomes are available. Required: all six key assessment elements + Technical Criteria + Appropriateness of Proposed MIDD. It leaves out the submission stage.


## Frame

This skill needs an explicit Question of Interest and an explicit Context of
Use to write the assessment. Context of Use has three components: the
decision the model is meant to support, the model or MIDD strategy, and the
data feeding it. Do not silently invent the Question of Interest or any
Context of Use component from a bare scientific or business problem
statement.

- If the Question of Interest, or any one Context of Use component (decision
  / model-strategy / data), is not stated, ask one focused question targeting
  whichever single component would most change the ratings — name that
  component directly (e.g. "what decision is this meant to support?"), don't
  ask generically about "the Context of Use." Do not run a broad intake
  interview — one question, on the single most consequential gap.
- If the user has explicitly asked for a best-effort draft without pausing
  (e.g. a batch or dry-run request), proceed, but list every invented or
  assumed element — the Question of Interest itself, and each assumed Context
  of Use component (decision, model/strategy, data), plus anything else
  invented such as a disease — in an explicit "Assumptions" block at the top
  of the output. Never fold an invented element silently into the ratings'
  justification prose as if it had been given.


## What to provide guidance and proposed documentation on: 

### Question of Interest

- explicitly stated
- reflects and informs multidisciplinary assessments and regulatory decision-making

### Context of Use

- concise, clear, explicit description of the model's role and scope
- includes the data used to build the model
- includes any additional data or evidence that will inform the answer to the question of interest

### Model Influence

- the intended weight of model outcomes in decision-making relative to other evidence
- described, rated (low / medium / high), and justified
- high when model outcomes are the sole source of support; low or medium when substantial other evidence exists

### Consequence of Wrong Decision

- the potential negative effect on patient safety and/or lack of efficacy from an incorrect decision
- described, rated (low / medium / high), and justified
- rating combines severity of potential negative effect AND likelihood that a wrong decision produces that effect

### Model Risk

- derived by combining Model Influence and Consequence of Wrong Decision — not assessed independently
- described, rated (low / medium / high), and justified
- combination rule: use the default matrix in `references/terms.md` for every Influence x Consequence pair (including matching non-extreme ratings such as both Medium); deviate from it only with an explicit, stated rationale
- question-specific: not to be interpreted as a risk intrinsic to MIDD or M&S
- determines the required rigor of model evaluation

### Model Impact

- the extent to which the proposed MIDD strategy varies from regulatory standards, or from expectations when no standard exists
- described, rated (low / medium / high), and justified
- rating increases as deviation from regulatory standards increases
- not the model's weight in decision-making — that is Model Influence (§2.1.3)

### Technical Criteria

- key criteria for evaluating the model and model outcomes, specific to the question of interest
- rationale states how criteria are commensurate with model risk
- details expected in the MAP, not only in the assessment table; when both documents are pushed to Jinkō, this is where the reciprocal link back to the MAP document belongs (see the linking instruction under "Optional: Create a Jinkō Document")
- not rated low/medium/high — enter the literal value `Not rated` in the assessment table's Rating column (the MAP template's Section 3 table already pre-fills this). Any table presenting these two elements' ratings must carry the footnote from `references/map.md`'s Section 3 explaining why they're unrated — readers otherwise reasonably read "Not rated" as an omission or error

### Appropriateness of Proposed MIDD — planning stage

- brief rationale for why the MIDD strategy is suitable for the question of interest
- considers the key assessment elements
- explains how technical criteria ensure appropriateness of model outcomes
- not rated low/medium/high — enter the literal value `Not rated` in the assessment table's Rating column (the MAP template's Section 3 table already pre-fills this). Any table presenting these two elements' ratings must carry the footnote from `references/map.md`'s Section 3 explaining why they're unrated — readers otherwise reasonably read "Not rated" as an omission or error


## Safeguards

- Limit yourself strictly to the sections cited above, plus the Frame section's "Assumptions" block when it applies. There is no need for an introduction, a conclusion or a 'next step' sections
- Never leak details about internal implementation (skill names, file paths, or workflow structure) that have no meaning from the regulator's perspective. Do not rely on this instruction alone: before presenting or uploading any generated document (assessment table, MAP document, or Jinkō document draft), write it to a file and run
  `python scripts/check_no_skill_leak.py <file...>`. Fix every reported line and re-run until it exits 0.
- An unlabeled, invented Question of Interest or Context of Use is the same class of problem as a leaked implementation detail: something reaching the regulator-facing document that isn't what it appears to be. Treat the Frame section's Assumptions requirement as the other half of this safeguard, not a separate concern.

## Generate a MAP documentation

Using /references/map.md, generate a Model Analysis Plan (MAP) document.


## Optional: Create a Jinkō Document

> **PREREQUISITE:** Creating Jinkō documents needs an initialized `jinko-sdk`
> connection satisfying this skill's `metadata.requires_sdk` range. Run the
> `jinko-sdk-setup` skill and proceed only once its check passes. A session code
> can be exchanged only once, so call `get_session_code` again before this
> upload. If that skill is not found, install it from `novainsilico/jinko-skills`.
> This prerequisite
> applies only to this optional upload step — the planning guidance above needs
> no SDK access.

After completing the recommendations, offer to create Jinkō documents in Jinkō.

"Would you like to create Jinkō documents from the above recommendations?"

If yes, run `scripts/check_no_skill_leak.py` against the drafted content first, then load the jinko-document skill and follow its workflow.

If pushing several documents to jinko, link them in both directions, not just one: the MAP's Appendices already reference the assessment document (its "Assessment table details" entry), so add the mirror link from the assessment document's Technical Criteria section back to the MAP. Make sure every such link points to the jinko documents, not the source markdown. 


## Reference to the most current ICHM15 documentation. 

A reference to the current version of the ICHM15 documentation can be inserted at the end of the documentation, linking to https://ich.org/page/multidisciplinary-guidelines#15
