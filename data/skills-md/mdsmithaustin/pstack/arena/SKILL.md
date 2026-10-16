---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
---

# Arena

Open a worklist with one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify) before launching anything.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric, 3-6 concrete gradeable criteria for what success looks like on *this* task. For subjective criteria, use [Eval's criterion and calibration guidance](../poteto-mode/playbooks/eval.md). It is the picker's tool in Phase D. Candidates only see the task.
3. Pick the runners. Use the `arena runners` role, one arm per entry. Its default is one each on `fable`, `opus`, `sonnet`. A rejected entry also follows the required-arm rule below. Spawn more runners when the arena covers multiple design directions. Use the same model N times when the work is generation-bound rather than judgment-sensitive. Use the **pstack-harness** skill for the spawn. Its **Spawn a role** section resolves the role and builds this CLI's spawn call.
4. Give each candidate its own output location (a git worktree where possible, otherwise `candidate-<n>/` inside a fresh `mktemp -d "${TMPDIR:-/tmp}/arena-<slug>.XXXXXX"` made for this run), per the **separate-before-serializing-shared-state** principle skill. Never reuse an earlier run's directory. A native isolation option counts only when it makes a git worktree, where `git -C <its path> rev-parse --path-format=absolute --git-common-dir` prints the project's. Grok Build's `isolation: worktree` can make a standalone clone, so spawn there with `isolation: none`. If you omit the field, a Grok role or persona default can still turn isolation on. Make every other candidate worktree yourself, one at a time, with `git worktree add --detach <run dir>/candidate-<n>`, where `<run dir>` is that fresh `mktemp -d`, and name the path in the candidate's brief. If an add fails, remove the worktrees already made and give every candidate a plain directory there instead, so all candidates start alike. The **pstack-harness** skill's fallback says how to seed and brief a plain directory. Clean up the run when it ends, after saving its outputs per Outputs, and before a re-frame and re-run starts, whether Phase E or Phase F sent you back. To clean up, remove each candidate worktree with `git worktree remove --force <path>`, delete any branch made for it with `git branch -D`, and delete the scratch directory. Going back to Phase E to graft keeps them. Keep the rubric outside every directory a candidate can read, and give it to the cross-judge in its prompt.

## Phase B: Fan out

Spawn all N subagents in one message with `run_in_background: true`, each with the task, the path to the shared grounding, its own output path, and instructions to produce the artifact and a short rationale naming the alternatives it considered and what it rejected.

### Required arms

An arm or exact model requested for this task remains an obligation. If it cannot return a result, retain useful outputs but report the requested comparison as incomplete. Disclose substitutions and the models that actually ran. A replacement does not fulfill an exact model request. Configured defaults and role aliases resolve through the harness as usual. A default or discretionary candidate may drop out with a recorded limitation.

## Phase C: Cross-judge

After all Phase B candidates complete, choose one arm of the `arena cross-judge pool` role. Use the **pstack-harness** skill's **Spawn a role** section to resolve it. Its default pool is `fable`, `opus`, `sonnet`. Prefer a different model family or capability tier from the parent's. Spawn one readonly judge subagent on that model. It sees the rubric and the candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with your reading in Phase D. Don't spawn it while candidates are still writing.

## Phase D: Pick a base

Read every candidate's rationale end to end before picking. Read a candidate's full artifact only when it is the base, or where you and the cross-judge disagree on a criterion. The cross-judge reads every artifact in full.

Score each candidate against the rubric criterion by criterion, not on holistic feel, from its rationale and the cross-judge's evidence for that criterion. Where those cannot settle a criterion, read that part of the artifact. Compare against the cross-judge. Agreement on the base confirms the pick. Name the models you, the runners, and the cross-judge ran on before you call any agreement or convergence confirmation, because arms on one model are one opinion. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API, per the Laziness Protocol.

## Phase E: Graft

Walk each losing candidate's rationale and the cross-judge's scores once more for what is worth porting into the base, usually one or two things per candidate, not most of it. Read only the parts of a losing artifact you will graft. Fold each graft in by hand, per the **redesign-from-first-principles** principle skill, so the result stays coherent under one mental model. Don't paste mechanically.

If the candidates converge on one shape, note the convergence subject to Phase D's actual-model disclosure and one-model limitation. Ship the consensus shape. No graft is needed. If they wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence. Before the re-run, remove this run's candidate worktrees and their branches and delete its scratch directory.

## Phase F: Verify

Verify the synthesized artifact like any other output, per the **prove-it-works** principle skill. If verification finds a problem the arena missed, either Phase A was wrong (re-frame and re-run) or a candidate caught it and you missed the graft (go back to Phase E). Don't paper over it. Before a re-frame and re-run, remove this run's candidate worktrees and their branches and delete its scratch directory. Going back to Phase E keeps them. Once verification passes, save the outputs, then clean up the same way.

## Outputs

One synthesized artifact, saved where the calling task says. Code the calling task ships goes onto the branch it works on. A sketch awaiting the caller's sign-off is not yet code the task ships, so it stays outside the project until sign-off. Any other artifact whose task names no place goes in a fresh `mktemp -d` outside the project. Give a short synthesis note in your reply rather than as a file, naming the base and why, the cross-judge's verdict, each graft with its source candidate, what was rejected and why, any convergence or dropouts, and the verification result.
