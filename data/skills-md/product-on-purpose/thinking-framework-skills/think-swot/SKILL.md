---
name: think-swot
description: Runs a SWOT analysis (strengths, weaknesses, opportunities, threats) caveat-first. It leads with the weak evidence (Hill and Westbrook 1997 found real SWOT grids did not amount to analysis), then forces the discipline a bare grid lacks, namely evidence-tagged and prioritized factors plus a TOWS matching step that turns the four lists into strategic options. Use only when a SWOT or TOWS is asked for by name; for genuine situation decomposition prefer think-issue-tree.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.swot
  family: strategy-and-opportunity
  evidence-tier: "X"
  version: 0.1.0
  standard: "0.8"
  caveat-first: true
  posture: run_caveat_first
  recommendation-policy: explicit_request_only
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# SWOT

SWOT sorts a situation into four boxes: internal Strengths and Weaknesses, external Opportunities and Threats. It is famous and frequently requested, and its evidence is weak: the most-cited field study found that bare SWOT grids "did not constitute analysis." This skill runs SWOT honestly. It leads with that caveat, then forces the three things a bare grid omits and that make it worth running at all: each factor tagged as evidence or assumption, each list prioritized to a few load-bearing items, and a TOWS matching step that converts the four lists into named strategic options. The output is a disciplined SWOT plus a TOWS option set, not a long undifferentiated list.

## Before you run this: the evidence caveat

SWOT is tier **X** (weak or contradictory evidence). The single most-cited study of SWOT in practice, Terry Hill and Roy Westbrook, "SWOT Analysis: It's Time for a Product Recall" (*Long Range Planning* 30(1), 1997, 46-52), reviewed SWOT use by 14 consulting firms across more than 20 of 50 UK manufacturing firms and found the grids collapsed into long, undifferentiated lists, averaging over 40 general factors, with no prioritization, no verification of any point, and no connection to the rest of the strategy work. Their verdict: the activity "did not constitute analysis."

So a four-box list is not a deliverable. If you run SWOT here, the value is not the boxes, it is the discipline this skill adds on top: tagging each factor as evidence or assumption, cutting each list to the few that matter, and the TOWS matching step (Weihrich 1982) that turns the lists into options. If what you actually need is to decompose a situation rigorously, `think-issue-tree` is the stronger move; for parallel external futures, `think-scenario-planning`. Do not report a bare grid as analysis, and do not invent quantified claims about SWOT's effectiveness (none are supported).

## When to Use

- The user asks for a SWOT by name and you should run it honestly rather than refuse.
- A quick shared snapshot of internal and external factors is genuinely wanted, and you will add the missing discipline (prioritize, verify, match).
- As a front end to option generation, where the TOWS matching step is the real payload.

## When NOT to Use

- As a substitute for real analysis, or to produce a long unprioritized factor dump (the documented failure mode; the bare grid "did not constitute analysis").
- When the job is rigorous situation decomposition: use `think-issue-tree`.
- When the job is exploring divergent external futures: use `think-scenario-planning`.
- For product strategy specifically: the pm-skills opportunity-solution tree fits better.

## Instructions

When asked to run a SWOT, follow these steps:

1. **Lead with the caveat.** State up front that SWOT's evidence is weak (Hill and Westbrook 1997) and that the value is the discipline below, not the four boxes.
2. **Fill the grid, sparingly.** Strengths and Weaknesses (internal), Opportunities and Threats (external). Cap each box at three to five load-bearing items. Resist the dump.
3. **Tag each factor** as `[evidence]` (you can cite a fact) or `[assumption]` (you cannot yet). An unverified threat is a hypothesis, not a finding.
4. **Prioritize.** Within each box, mark the one or two items that would most change the decision. Drop the filler.
5. **Match (TOWS).** Cross the lists to generate options: Strength-Opportunity (use a strength to seize an opportunity), Strength-Threat (use a strength to counter a threat), Weakness-Opportunity (fix a weakness to seize an opportunity), Weakness-Threat (defend against a weakness meeting a threat). The strategic options are the deliverable.
6. **Emit the disciplined SWOT plus the TOWS options** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the prioritized, evidence-tagged grid plus the TOWS option set, with the caveat leading, not a flat four-box list.

## Quality Checklist

Before finalizing, verify:

- [ ] The evidence caveat leads the output and the skill does not overclaim SWOT's value.
- [ ] Each box holds at most three to five load-bearing items, not a dump.
- [ ] Every factor is tagged `[evidence]` or `[assumption]`.
- [ ] The one or two priority items per box are marked.
- [ ] A TOWS matching step produces named strategic options (the real payload).
- [ ] No invented quantified claim about SWOT's effectiveness appears.

## Evidence

Tier **X** (weak or contradictory evidence; normally would not ship). It ships as a contested lens, caveat-first and explicit-request-only, because users ask for SWOT by name and an honest run that leads with the deficiency and adds the missing discipline beats a flat refusal. The governing finding is Hill and Westbrook (1997): bare SWOT "did not constitute analysis." The TOWS matching step is Heinz Weihrich, "The TOWS Matrix: A Tool for Situational Analysis" (*Long Range Planning*, 1982). Evidence is transferred from human strategy practice, not AI-validated; SWOT's distinctive box structure has no controlled support. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed disciplined SWOT plus TOWS option set.
