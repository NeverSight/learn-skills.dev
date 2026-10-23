---
name: fable-spark
description: "Predict the smallest atomic next engineering action from current workspace state, evidence gates, and mutation freshness with situational silence. Use when evaluating what immediate atomic step to take next, checking situational awareness, or determining if the current state requires action or silence — even if the user does not explicitly say \"fable-spark\" (e.g. \"what is my next move\", \"spark hint\", \"check next action\", \"what should I do now\"). Do NOT use as a substitute for broad architectural planning (use fable-plan)."
version: 1.3.0
pack: system
inputs:
  - current_state
requires:
  - situational_context
produces:
  - spark_suggestion
gates:
  - minimal_action_tested
fallback: get-fable
mutatesWorkspace: false
parallelSafe: true
neural_links:
  precursors:
    - get-fable
    - fable-cowork
  continuations:
    - get-fable
  lateral_peers:
    - get-fable
  recovery: fable-recover
---

# Fable Spark

Choose one small next move that improves the state of the current task—or deliberately say nothing.

## Mission
Spark is not a planner, router, motivational assistant, or todo generator. It is a micro-policy for moments when the task is already in motion and the best next action should be small, concrete, and justified by current state.

The quality bar is not "a helpful suggestion." It is **the least action that unlocks the next piece of evidence or safely advances the active Skill**.

## Activate When
- an edit/test/failure/state transition just happened;
- a long session needs the next atomic step rather than another full plan;
- verification freshness/gates determine what should happen next;
- an active specialist has a clear ownership boundary but the immediate move is unclear;
- silence vs intervention itself is a useful decision.

## Do Not Activate When
- no primary Skill has been selected for substantial new work (`get-fable`);
- architecture/decomposition is the unresolved problem (`fable-plan`);
- repeated failure requires a diagnosis (`fable-recover` owns the work; Spark may only point there);
- the user asked for execution, not a suggestion, and the executing Skill already knows its next step.

## Situation Classification
| State signal | Spark posture |
| --- | --- |
| repeated failure | stop mutation; diagnose |
| mutation newer than verification | refresh relevant proof |
| explicit active gate missing | satisfy that gate |
| review finding unresolved | repair/replan finding |
| active card blocked by unknown | discover/research/plan |
| complete/idle with no intent | silence |
| specialist owns next obvious step | usually silence; avoid narration |
| several equally plausible non-atomic moves | defer to orchestrator/plan |

## Next-Move Protocol
### Stage 1 — Read state before intent embellishment
Inspect phase, current Skill/card, mutation/verified generation, failure streak, evidence, unresolved findings, blockers, and latest user intent.

### Stage 2 — Apply safety precedence
Prefer in order when applicable:
1. diagnose repeated/contradictory failure;
2. refresh stale proof after mutation;
3. satisfy explicit blocking gate;
4. resolve a named load-bearing unknown;
5. continue the active specialist's smallest next action;
6. silence.

### Stage 3 — Make the action atomic
A Spark suggestion should usually be one observable verb-object step:
- `run the affected auth tests`;
- `reproduce the race with a barrier`;
- `inspect the registered CLI entrypoint`;
- `review the current diff against the card`;
- `capture the provider response bundle`.

Avoid multi-stage suggestions such as "research, plan, implement, test, and release."

### Stage 4 — Require a reason tied to evidence
The reason should reference state/evidence, e.g. verification stale after mutation, failure streak reached recovery threshold, release gate missing, or active card has unresolved API contract.

### Stage 5 — Check actionability
Before speaking, ask:
- can the action be done now with available context/tools?
- does it preserve current scope?
- is it owned by the active/next Skill?
- will its outcome reduce uncertainty or satisfy a gate?

If not, prefer silence or route back to the orchestrator.

### Stage 6 — Use silence intentionally
Silence is correct when:
- task is idle/complete with no new intent;
- the active agent already has an obvious immediate action;
- only speculative future work can be suggested;
- available context is too ambiguous for a useful atomic step.

## Decision Rules
- Repeated failure outranks "run tests again" if another identical run adds no information.
- Fresh mutation outranks completion/release suggestions until relevant evidence is refreshed.
- Security/research/receipt evidence cannot stand in for required functional verification.
- Do not suggest implementation when a load-bearing fact/contract remains unknown.
- Prefer a targeted affected check over a full suite when the next goal is rapid causal feedback; broader required gates can follow.
- Never invent a new objective because the current task is quiet.
- Confidence is not a license to act outside the current Skill's scope.
- If two next moves depend on an unresolved ordering/architecture choice, route to plan instead of guessing.

## Invariants
- At most one primary Spark suggestion.
- Suggestion is atomic, actionable, and scope-preserving.
- State/evidence—not generic best practice—justifies intervention.
- Silence is allowed and preferred over speculative advice.
- Spark never upgrades stale/incomplete evidence into completion proof.

## Failure Taxonomy
### Scope drift
Suggestion introduces an unrelated improvement. Drop it and return to active card/gate.

### Ceremony
Spark narrates a step the active specialist is already obviously executing. Stay silent.

### Premature action
Suggestion mutates code before discovery/TDD/recovery requirement. Apply precedence.

### Stale-proof blindness
Spark suggests review/release despite mutation newer than verification. Refresh proof first.

### Retry loop
Spark repeats a command after repeated failure without new diagnostic state. Route to recovery.

### Ambiguous macro-action
Suggestion contains several dependent steps. Reduce to first atomic decision or route to plan.

## Anti-Patterns
- turning Spark into a mini project manager;
- always suggesting something;
- generic advice such as "keep testing";
- proposing a full suite when one focused probe is the causal next move;
- suggesting release because tests once passed;
- suggesting implementation from unknown external facts;
- confidence scores unsupported by state;
- outputting three alternatives instead of one next action.

## Spark Packet
```text
State signal:
Blocking gate / uncertainty:
Suggestion: <one action or null>
Why now:
Expected observation:
Owner Skill:
Silent: true|false
```

## Completion Criteria
Spark succeeds when it either:
- names one immediately executable, evidence-grounded action that safely advances the current lifecycle; or
- remains silent because intervention would add noise, scope, or speculation.

## Progressive Resources
- Deep guide: `references/atomic-action-and-silence.md`
- Next-move policy: `references/next-move-policy.md`
- Silence: `references/silence-policy.md`
- Evidence/gates: `references/evidence-and-gates.md`
- Confidence: `references/confidence-policy.md`
- Example: `examples/situational-awareness-walkthrough.md`
