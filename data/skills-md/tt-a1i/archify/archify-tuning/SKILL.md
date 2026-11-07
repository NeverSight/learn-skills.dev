---
name: archify-tuning
description: Improve Archify diagram accuracy, visual quality and complete authoring speed with fewer repairs. Use for generation experiments or evaluating changes to layout, routing, diagnostics, authoring instructions and acceptance rules against actual diagrams and agent traces.
metadata:
  internal: true
---

# Archify Tuning

Users describe a system and an agent authors the diagram. Optimize that complete journey, from understanding the source to delivering a usable artifact. Keep this priority:

1. **Accurate**: facts, relationships, directions, conditions, ownership and sources match the system.
2. **Readable and attractive**: a clear reading path, distinguishable connections, legible text and balanced composition.
3. **Efficient**: short complete delivery time, few failed repairs and little repeated work.

**Tests and validators serve these outcomes and are themselves candidates for improvement.** A passing check does not establish a good diagram; a failing check can expose an unsuitable rule. Judge the artifact and authoring experience before choosing what to change.

## Product requirements and adjustable rules

- Protect source facts and supported user behavior. First drafts can be wrong: retain originals and record source-backed corrections or additions. Counts of deleted elements flag a semantic review; they do not decide whether an edit is correct.
- Treat spacing, preferred direction, bend counts and single-screen fit as design strategies to assess in context. An extra bend or readable scrolling can improve the whole diagram. Preserve explicit geometry and supported contracts unless an agreed change covers them.
- Before repairing a failed check, identify the user harm it is meant to prevent and whether that harm is present. For an unsuitable rule, revise its scope, threshold or severity; update or retire obsolete tests with the rationale and actual before/after evidence. Keep the original failure visible. Changing an expected value alone proves no benefit.
- Early diagnostics and browser checks should agree where they measure the same requirement and state their different scopes elsewhere. Neither is an unquestionable oracle. Taste that cannot be judged reliably can remain advice or visual review instead of a hard failure.

## Measures

| Role | Measure | Evidence |
|---|---|---|
| Outcome | Accurate, visually acceptable final delivery | Source audit and actual screenshots; separate machine pass from visual acceptance |
| Outcome | Complete elapsed time, failed repairs and repeated work | Timed trace from task start through reading, first draft, repairs, viewing and delivery |
| Process | First-draft quality and time to first usable result | Preserve the first attempt, every failure and the last verified usable artifact |
| Regression | Fixed-input pass/fail and changed output | `replay.mjs`, affected tests and visual comparisons; render pass excludes finalize/browser acceptance |
| Diagnostic | Bends, crossings, route length, text size and CLI time | Explain an observed benefit or tradeoff; none is a substitute for whole-diagram quality |

Report delivered outcomes and failed/unfinished tasks separately. A failed run ending sooner is not a speed gain. Keep synthetic regressions separate from the frozen first-draft denominator; additions to the corpus form a versioned cohort. Repaired drafts never replace their original benchmark entries.

## Setup

- **Tuning home**: `$ARCHIFY_TUNING_HOME`, default `~/.local/share/archify-tuning`. It holds `journal.md`, `bench/`, `rounds/` and `replays/`. It stays outside the repository because drafts carry content from source projects, which may be private: never commit it.
- **Resume**: read the journal, available checkpoint and current goal state. Respect pauses and prior product decisions; continue an active round instead of duplicating it. Use the user's chosen diagram types; cover others when shared changes affect them.
- **Versions**: refresh the target remote revision and record source, base and candidate identities. Use separate durable worktrees or frozen snapshots. Record remote movement without overwriting a comparison baseline or a running author's runtime.
- **Evidence selection**: follow [Choose evidence by impact](../../../CONTRIBUTING.md#choose-evidence-by-impact). Reuse unchanged evidence with its original revision and scope.
- **Tools**: Node 22.13 or later and Chrome or Chromium for `shots.mjs` (`ARCHIFY_CHROME` overrides discovery). The collector accepts Devin CLI history or a [normalized trace export](references/trace-export.md) from another agent. It does not read other agents' private history databases.

## Loop

1. **Bound the question.** Record one user-visible problem, the hypothesis, evidence that would support or refute it, and a time/attempt budget in the journal. Rank it by frequency, harm, likely benefit and ongoing complexity. Prefer existing evidence before starting another generation.
2. **Choose the experiment.** Use fixed JSON for renderer/rule changes, independent comparable authors for instruction or complete-flow claims, and a new project to discover problems or check transfer. For author runs, timing or screenshot comparisons, read [Experiment design](references/experiment-design.md). Discovery is not proof of improvement.
3. **Attribute.** Read the trace and inspect the complete diagram using [Trace signals](references/trace-signals.md). Record the primary cause, contributing factors and uncertainty. Distinguish source misunderstanding, placement, routing, diagnostics, instruction usability and unsuitable acceptance rules. Reproduce with valid placement before blaming the router; a rule being documented does not establish that it is useful or easy to apply.
4. **Change the smallest responsible scope.** Prefer a minimal reproduction before a runtime fix. Trace other callers before changing a shared path. Evaluate main-path arrangement, interacting modules, branch/merge space and return paths together with routing. Keep experimental placements on copies; an automatic route fix must honor authored pins. Add guidance only for a demonstrated information gap, then evaluate whether authors benefit.
5. **Verify the claim.** Select affected public-behavior tests and fixed inputs; add a regression for a demonstrated runtime defect when existing coverage does not capture it. Inspect changed outputs with the same viewport and state. Investigate each changed pass/fail result: distinguish real regressions, corrected false failures and intended rule changes with evidence. Unexplained failures remain open. A local improvement must survive the complete diagram and relevant contrasting cases before adoption. Rebuild generated outputs only when their authoritative inputs changed.
6. **Conclude and consolidate.** Record confirmed facts, rejected approaches, remaining problems and one disposition: confirmed problem, verified local fix, experimental candidate, rejected approach or candidate ready for independent review. State limits on visual, speed and generalization claims. Prepare small reviewable changes once benefits are established; separate unrelated fixes and prototypes. Follow [CONTRIBUTING.md](../../../CONTRIBUTING.md) for integration; this skill grants no push, PR, merge, release or live-install authority.

### When to stop an experiment

- At the budget limit, record the result and remaining uncertainty. Extend only for a concrete new hypothesis and a fresh bounded test.
- Stop or change focus when attempts repeat without new causal evidence, depend on project-specific coordinate search, improve selected lines while worsening the whole graph, or add complexity disproportionate to the benefit.
- Preserve the last verified artifact separately from an unsuccessful experiment. Ending an experiment does not complete the overall goal. Consolidate useful fixes before accumulating another batch.

## Tools and reporting

Run from the repository root; these tools supply evidence for the selected experiment, not a mandatory sequence every round. `round`, `collect` and `replay` print usage with no arguments.

| Need | Command |
|---|---|
| Fixed-input comparison | `node .agents/skills/archify-tuning/scripts/replay.mjs --base <base>/archify` |
| Prepare author tasks | `node .agents/skills/archify-tuning/scripts/round.mjs <project-path> --types <selected-types> --archify <frozen-runtime>/archify` |
| Collect traces and content-change signals | `node .agents/skills/archify-tuning/scripts/collect.mjs <round> --dump` (add `--trace-export <file.json>` outside Devin) |
| Initial light-theme image comparison | `node .agents/skills/archify-tuning/scripts/shots.mjs <replay-dir> --height 900` |

The collector does not establish semantic correctness or complete elapsed time; supplement it with source review and timing records. Preserve failure logs and unknown outcomes. Diagnostics should name the affected element and a verified repair, or explain why no repair was found. Keep authoring guidance concise and reachable in required reads; avoid accumulating advice that has no observed benefit.
