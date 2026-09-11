---
name: think-five-whys
description: Runs a Five Whys root-cause trace caveat-first. It leads with the weak evidence (Card 2017 found the single-chain method oversimplifies multi-causal problems), then forces the discipline a bare why-chain lacks, namely flagging at each step whether more than one cause could apply. Use only when Five Whys is asked for by name; for any problem that might have more than one cause prefer think-issue-tree.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.five-whys
  family: problem-framing
  evidence-tier: "X"
  version: 0.1.0
  standard: "0.8"
  caveat-first: true
  posture: run_caveat_first
  recommendation-policy: explicit_request_only
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Five Whys

Five Whys traces a problem to a root cause by asking "why?" of each answer, about five times, until you reach a cause worth fixing. It is famous and frequently requested, and its evidence is weak: the critical literature finds it flattens multi-cause problems into a single chain and discards the rest. This skill runs Five Whys honestly. It leads with that caveat, then forces the one discipline a bare why-chain omits and that makes it safe to run at all: at each step, flag whether more than one cause could apply, and the moment the problem is multi-cause, say so and hand it to `think-issue-tree`. The output is a single linear why-chain with a branch-or-not flag on each step plus one countermeasure aimed at the terminal node, not a confident single root cause presented as the cause.

## Before you run this: the evidence caveat

Five Whys is tier **X** (weak or contradictory evidence). The governing critique is Alan J. Card, "The problem with '5 whys'," *BMJ Quality & Safety* 26(8) (2017): 671-677, which argues the technique oversimplifies complex problems, follows a single causal chain when failures are multi-causal, and limits understanding of how processes actually fail; Card's prescription is to move to branching, systems-oriented causal-tree diagramming. John Allspaw, "The Infinite Hows (or, the Dangers of the Five Whys)" (2014), adds that in socio-technical systems the linear "why" chain drifts toward a person and a counterfactual (the "Bad Apple" blame trap) and recommends "how" over "why" to recover the multi-contributor picture. The method is reliable only for simple, linear, single-cause failures; beyond them its output looks like THE cause when it is one cause among many.

So a single chain is not a verdict. If you run Five Whys here, the value is not the chain, it is the discipline this skill adds: flagging at every step whether more than one cause could apply, and stopping to redirect when it can. For any problem that might have more than one cause - which is most real problems - `think-issue-tree` is the stronger move: it branches with MECE-plus-remainder discipline instead of forcing one path. Do not report a single root cause as the answer to a many-cause problem, and do not invent quantified claims about Five Whys' effectiveness (none are supported).

## When to Use

- The user asks for Five Whys (or "5 whys") by name and you should run it honestly rather than refuse.
- The failure is plausibly a simple, linear, deterministic chain (a machine fault, a single procedural slip) and you will still flag any branch points you hit.
- As a fast teaching prompt for the habit of not stopping at the first explanation, with the multi-cause caveat attached.

## When NOT to Use

- When the problem may have more than one contributing cause (the documented failure mode): use `think-issue-tree`, which branches instead of forcing a single chain.
- When the failure is socio-technical and the chain would terminate at "operator error" (the Bad Apple blame trap): use `think-issue-tree` to keep the conditions, not the person.
- When you need a reproducible, coverage-checked decomposition rather than one investigator's single path: use `think-issue-tree`.

## Instructions

When asked to run a Five Whys, follow these steps:

1. **Lead with the caveat.** State up front that Five Whys' evidence is weak (Card 2017) and that the value is the branch-flagging discipline below, not the chain itself.
2. **State the problem precisely.** One concrete, observable symptom - the thing that actually went wrong, not a vague theme.
3. **Ask "why?" and answer once.** Take the answer as the next link. Then ask "why?" of that answer. Repeat, roughly five times, until you reach a cause you could actually act on.
4. **At every step, flag the branch.** Mark each link `[single cause]` (you are confident this is the only "why" that matters here) or `[branch]` (more than one cause could legitimately apply). A `[branch]` is an honest admission that you are discarding alternatives by walking just one.
5. **Check for multi-cause before you commit.** If any step is `[branch]`, or if the failure is socio-technical, stop: say so plainly and recommend `think-issue-tree` rather than presenting the chain as the answer.
6. **Name one countermeasure at the terminal node.** Aim the fix at the terminal cause, not the original symptom - and only if the chain held as `[single cause]` throughout.
7. **Emit the linear chain with branch flags plus the countermeasure** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the single linear why-chain with a branch-or-not flag on each step, a terminal root cause, and one countermeasure, with the caveat leading - not a confident single root cause stripped of its alternatives.

## Quality Checklist

Before finalizing, verify:

- [ ] Leads with the evidence caveat (Card 2017) before the artifact; does not overclaim the method's value.
- [ ] Each step is flagged `[single cause]` or `[branch]`.
- [ ] If any step is `[branch]` (or the failure is socio-technical), the output says so and redirects to `think-issue-tree` instead of presenting the chain as the cause.
- [ ] When the chain is genuinely single-cause, it terminates at a cause you could act on (not a convenient symptom); when it branches, it stops honestly instead of forcing a terminal cause.
- [ ] A countermeasure is aimed at the terminal node when the chain is single-cause; when it branched, no countermeasure is forced and the problem is handed to `think-issue-tree`.
- [ ] No invented quantified claim about Five Whys' effectiveness appears.

## Evidence

Tier **X** (weak or contradictory evidence; normally would not ship). It ships as a contested lens, caveat-first and explicit-request-only, because users ask for Five Whys by name and an honest run that leads with the deficiency and adds the missing branch-flagging discipline beats a flat refusal. The governing critique is Card (2017): the single-chain technique oversimplifies multi-causal problems. Allspaw (2014) documents the socio-technical blame trap. Evidence is transferred from human investigators in manufacturing, healthcare, and software operations, not AI-validated; Five Whys' distinctive single-chain shape has no controlled support, and the better move (`think-issue-tree`) already ships. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed Five Whys chain with branch flags and a terminal countermeasure.
