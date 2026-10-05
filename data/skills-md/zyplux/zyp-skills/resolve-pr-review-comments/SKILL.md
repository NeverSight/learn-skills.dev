---
name: resolve-pr-review-comments
description: >
  Use the bundled live-state script to loop through `ci`,
  `copilot-pull-request-reviewer`, and `copilot-review-complete`: fix actionable
  failures, address every unresolved Copilot thread, retrigger review, and repeat
  until all three are green or one terminates the loop.
  Run only through an explicit /resolve-pr-review-comments invocation; never
  trigger from a natural-language request.
metadata:
  kind: prompt
  version: "0.10.1"
  user-invocable: "true"
---

# Resolve PR Review Comments

1. Resolve the directory containing this `SKILL.md` as `THIS_SKILL_MD_DIR`.
2. With the repo root as `cwd`, execute bundled script:

```bash
<THIS_SKILL_MD_DIR>/scripts/pr_loop_state.py
```
3. Follow its instructions. After `just pr`, wait 3 minutes before the first rerun; Copilot cannot normally finish sooner. For later waits, run `sleep 60`, then rerun the script and follow the new instructions.

## Non-obvious constraints

- At step 40, ensure the full `just c` gate passes, then push only with `just pr` - the only correct way to retrigger Copilot review.
- Validate Copilot findings thoroughly - it is wrong approximately 30% of the time.
- There is normally a separate human-review gate that prevents final auto-merge.
- Fix valid findings and explain why invalid findings should not be applied, then resolve every addressed thread.
- If every thread is resolved but `copilot-review-complete` still shows the previous failure, run `just pr` once: its draft-to-ready transition emits `ready_for_review` and reruns the watcher without an empty commit.
- For a false positive, update `.github/copilot-instructions.md` only when a short, general instruction would reliably prevent it recurring; otherwise leave the file unchanged.
- Do not treat a Copilot review as stuck until it has run for 12 minutes. After that, verify that it is still progressing; stop and inform the user if it is stuck or broken.
- When Copilot findings are valid and you are applying the fix, take extra care to prevent scope creep, minimize new lines of code to your best ability.

## Decision tree

*Which recommendation does the script produce from the state it polls?*

```mermaid
flowchart TD
    Start(["0: start"]) --> CheckPRExists{"10: PR open?"}
    CheckPRExists -->|no| Stop["100: STOP"]
    CheckPRExists -->|yes| CheckWorkingTreeClean{"20: working tree clean<br/>and branch relation safe?"}
    CheckWorkingTreeClean -->|working tree dirty| IsDirty["70: working tree is not clean, do you recognise the changes as yours?<br/>YES - commit, do not push, and rerun this script;<br/>NO - inform user and STOP."]
    IsDirty -. yes .-> Start
    IsDirty -. no .-> Stop
    CheckWorkingTreeClean -->|behind, diverged, or unknown| Stop
    CheckWorkingTreeClean -->|clean; equal or ahead| CheckCIState{"30: assess ci,<br/>copilot-pull-request-reviewer,<br/>and copilot-review-complete"}
    CheckCIState -->|action required| PrintReport["40: fix every reported failure and address every unresolved Copilot thread.<br/>Run just c until it passes, commit resulting changes, then run just pr."]
    PrintReport -. gates restarted .-> Wait
    CheckCIState -->|running| Wait["50: wait until all running gates finish,<br/>then rerun this script to obtain a fresh PR-state recommendation."]
    CheckCIState -->|all green or terminated| Stop
    Wait -. rerun script .-> Start

    subgraph Legend["Legend"]
        direction LR
        LegendCheck{"Script evaluates state"} -->|script logic| LegendNext{"Next script state"}
        LegendInstruction["Instruction shown to agent"] -. agent acts or waits .-> LegendRerun(["Rerun script"])
    end

    Stop ~~~ Legend
```
