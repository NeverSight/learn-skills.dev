---
name: loop-code-review
description: >-
  Find and fix material code defects and DX issues through risk-based review
  rounds with fresh subagents and regression checks.
---

## Rules

- You are the lead. You own the decisions. Reviewers read code, edit code, and run checks.
- Minimize the total cost of each completed review. Include retries and your own turns.
- To settle a finding, you can read up to 100 lines of code. Do not review or edit.
- Only you start agents. Start each reviewer without parent history. Do not read agent histories.
- If another skill calls this skill, do not start a separate coordinator.
- Do not poll agents. Wait for their reports.
- Write agent messages in English. Write the final report in the user's language.
- Follow project rules. For model and effort, the user's choice comes first, then the calling skill's choice.
- Review only the task changes. Leave unrelated changes untouched.

## Reviewers

A reviewer is a new agent for one round. It reviews the assigned changes and then fixes the accepted findings.

Use the risk from the calling skill. Otherwise, choose the risk.
High risk: migrations, persisted data, security, concurrency, contracts that external code uses, or unclear failures across components. Other changes have normal risk.

| Risk | Claude Code | Codex |
| --- | --- | --- |
| Normal | `subagent_type: effort-medium`, `model: opus` | Sol, `reasoning_effort: medium` |
| High | `subagent_type: effort-high`, `model: opus` | Sol, `reasoning_effort: high` |

- Claude Code: if no agent type matches the chosen effort, use the nearest type and tell the user. If these agent types are missing, use `general-purpose` and tell the user that the reviewer inherits the session effort.
- Codex: set `fork_turns: "none"`. Use the longest `wait` timeout.
- Claude Code, if you run as a subagent: start every agent in the foreground. Do not continue an agent with `SendMessage`, because its report does not return to you. Where this skill says "the same reviewer", start a new foreground agent with the same settings. Send it the brief, the assigned changes, and the finding with your question, the accepted findings, or the failed checks. This agent only answers or only fixes.
- If checks fail after two fix attempts, stop that reviewer. Give a new agent one step higher the brief, the accepted findings, changed ranges, and check results. The new agent only fixes. This is not a new round. The steps are `medium`, `high`, and a stronger model.

## Brief

Send this brief and the finding format in the first message to each reviewer:

- Examine the assigned changes and the code they affect. Look beyond the known risks.
- Report the findings and stop. Fix only the findings that the lead accepts.
- Search before you read. Read only the ranges you need.
- Reuse valid check results. After fixes, rerun the checks that the fixes can affect.
- If a check still fails after two fix attempts, stop and report.
- Fix the root cause with the simplest sufficient change. Where practical, first write a regression test that fails.
- Do not use a browser for visual checks.
- Do not commit, push, create branches, or start agents.
- Report briefly and in English. Use `file:line` references. Do not paste code or full logs. In a fix report, list each changed file and line range.

Add the requirements, accepted clarifications, Definition of Done (DoD), repository path, assigned changes, check results, and known risks.
The assigned changes are all task changes in a full round and the changed ranges from the last fix report in a delta round.
Do not add previous review conclusions or the implementer's reasoning.

## Finding format

Report only material problems: defects or DX regressions that the task causes or worsens.
Do not report style, preferences, scope expansion, or edge cases without a realistic failure scenario.

For each finding, report:

- The location and the failing scenario.
- The violated requirement and the impact.
- The root cause and its evidence. Mark assumptions.
- The simplest fix and its effect on related behavior.
- A regression test or reproduction steps.

Also report important review gaps and a readiness score from 1 to 10 with one reason. The score is advisory.

## Rounds

1. Start a reviewer for a full round.
2. Assess the findings. Treat an important review gap as a finding. Accept material problems with evidence. Reject the other findings with a reason. If the evidence is not sufficient, read the code or ask the same reviewer. If you accept no findings, go to step 5.
3. Tell the same reviewer to fix the accepted findings and run the relevant checks.
4. Choose the next round:
   - If no production code changed, go to step 5.
   - Normal risk: if all fixes are trivial, go to step 5. Otherwise, start a delta round with a new reviewer.
   - High risk: start a full round with a new reviewer.
   - A fix is trivial if it is local, has a regression test, and changes no contract or shared code.
   - A new round continues at step 2.
   - After the third round, go to step 5. Report the last fixes as not re-reviewed.
5. Confirm from the last report that all applicable checks pass. If a check fails, return it to the same reviewer. Then finish.

If there are no task changes, report this and finish.

## Finish

Report the status. The status is passed if all applicable checks pass and no accepted finding is unfixed. Otherwise, the status is open.
Report the fixes, rejected findings with reasons, checks, remaining issues, and the last score.
Report the cost: rounds, models, efforts, and subagent tokens if the runtime reports them.
Pause only if a human action is necessary. State the action.
