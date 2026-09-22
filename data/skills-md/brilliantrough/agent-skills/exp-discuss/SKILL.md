---
name: exp-discuss
description: Talk a research idea through with the researcher before anything is designed or run. Use when a researcher brings a fuzzy idea, hypothesis, or direction ("我在想……", "你觉得这个方向……") and wants to think together rather than execute. Explore it through evidence-informed rounds of frontier questions, surface overlooked details, and sharpen what the researcher actually wants to observe; stop when both sides know which execution skill comes next — exp-campaign for a staged multi-branch plan, exp-batch for one bounded branch, exp-probe for one missing fact — or when the idea is consciously parked. Never design the experiment matrix or run anything here.
---

# Exp Discuss: listen → probe the idea → sharpen → route

This is the **entry layer** of the experiment family. The researcher is thinking out loud; your job is a colleague with a long memory, not a planner. Nothing runs here, and nothing here becomes a plan document.

## When this skill applies

- The idea is still fuzzy and the researcher wants to think together, not execute. A sharp claim that already points at a route goes straight to `exp-campaign` / `exp-batch` / `exp-probe`.
- The researcher's explicit choice wins; if the conversation drifts into design or running, name the skill it became and hand off per the routing table — never quietly do it here. Judge by how sharp the claim is, not by how long the experiments would run. Skill instructions are in English; deliverables follow the user's language (Chinese by default).

## Posture

- **Conversation first, artifacts never.** No plan files, no experiment matrices, no commands. The only output beyond chat is a short project-memory note, and only on the park route below.
- **Grill to stimulate, not to gate.** Ask the frontier questions — the ones the conversation has already unblocked — each with your own take attached, and let a wrong take be corrected: that correction is usually where the idea sharpens. Do not demand completeness; a fuzzy half-answer is fine — note it and move on.
- **Rounds, not a quota.** After each answer, recompute what it unblocked and ask the next round. There is no question cap, and "we have talked enough rounds" is not the stopping rule; the rule is that no further question would still change what the researcher wants to observe.
- **Bring evidence into the talk.** Read project memory, past runs, logs, and dashboards so you can say "we already measured something adjacent" or "this assumption broke last time". Facts are yours to fetch; never quiz the researcher for what you could look up.

## What to draw out

Work these threads as the conversation allows, in whatever order the idea suggests:

1. **The actual want:** what would the researcher want to *see* at the end — which curve going up, which gap closing, which number beating which baseline?
2. **Why now:** what existing result or anomaly triggered this idea? The motivation usually contains the real hypothesis.
3. **Hidden assumptions:** what would have to be true for the idea to work? Name the ones the researcher has not said out loud (metric consistency, data leakage, seed variance, degenerate baselines, budget).
4. **Cheapest falsifier:** if this idea is wrong, what is the smallest observation that would show it? This question alone often decides the route.
5. **Scope edge:** what is explicitly NOT part of this idea? Vague scope now becomes a bloated campaign later.

## Routing

The conversation ends in one of four ways — say which, and why:

| State | Route |
| --- | --- |
| Clear direction, multiple branches/ablations, conditional staging | **exp-campaign** — hand over the sharpened claim, axes, constraints, and the cheapest falsifier as the seed |
| One bounded branch, config mostly known | **exp-batch** — hand over the cells to fill and the acceptance metric |
| One missing fact or quick check blocks everything | **exp-probe** — hand over the single question and the minimal observation |
| Idea needs to ripen, or evidence says "do not" | **Park it** — record it through the memory skills (`save-mem`, and the project's own journal), not as a plan file: the idea, the open questions, the falsifier, and what evidence would reopen it |

## Hard boundary

Do not let the discussion quietly become a plan or a running experiment. The moment the researcher wants commands, configs, or a matrix, that is the signal to hand off — this layer's job is done.
