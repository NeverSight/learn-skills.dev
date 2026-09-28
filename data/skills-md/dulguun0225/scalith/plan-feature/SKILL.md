---
name: plan-feature
description: Plan one spec-kit feature from a clarified spec with no human gate — plan, plan review, tasks, analyze — and hand every question only the spec can answer to its domain expert in QUESTIONS.md, to be answered with /speckit-clarify. Invoke by name (/plan-feature).
disable-model-invocation: true
---
# Plan a feature — plan, tasks and analyze, and the questions for the domain expert

**The process is three loops over stock spec-kit commands.** This skill is step 2.1.

| Step | Who | What | Repeat until |
|---|---|---|---|
| 1 | domain expert, on the base branch | `/speckit-specify`, `/speckit-clarify` | clarify finds nothing to ask |
| 2.1 | technical expert, on the base branch | `/plan-feature`: plan, plan review, tasks, analyze | a run ends `done` |
| 2.2 | domain expert, in Claude Code opened in the project | the `/speckit-clarify` line in `QUESTIONS.md` | clarify finds nothing left to ask |
| 3 | technical expert, on a build branch | `/build-feature`: implement, converge, finish | done, landed on the base branch |

2.1 and 2.2 alternate until no question is open. A `CRITICAL` or `HIGH` question is open until the spec answers it. A `MEDIUM` or `LOW` one is also closed when the technical expert or the domain expert says the build may start on its recommended answer; the domain expert can still answer it later or never.

## Call build-feature's script; write no loop

**Call the Workflow tool with `build-feature`'s `workflow.mjs`, reached as a sibling of this skill's directory, with `until: "analyze"`, and run no `speckit-*` skill from your own context.**

**Planning runs on the base branch.** Preflight checks it out when the run starts elsewhere, refuses a dirty tree, and brings it up to date from origin by fast-forward only. Every stage commits there, only in the feature directory and in what the plan step writes outside it — the agent context file's managed section, an admitted constitution amendment, a `docs/GATES.md` entry. Nothing is pulled between stages, so a spec change pushed during the run is read by the next start. Each push is preceded by `git pull --rebase origin <base>`, which moves only the run's own commits; a refused push is tried again up to 3 times, and a conflict is aborted and stops the run. The plan review records the spec it read in `<featureDir>/spec-reviewed.sha`; a later start whose base spec differs from it restarts at `review-plan`. **A feature's spec is fixed once its build branch, `build/<NNN>-<name>`, exists**: a start refuses while that branch holds commits the base lacks, and a change to what the feature does is specified as a new feature whose spec states the change.

First run, once `spec.md` is written:

```
Workflow({
  scriptPath: "${CLAUDE_SKILL_DIR}/../build-feature/workflow.mjs",
  args: { until: "analyze" }
})
```

After the domain expert has answered, add `from: "review-plan"`, `wall` — the definition-of-done command the project's root `CLAUDE.md` names; a start after preflight must pass it — and `featureDir`, since without it discovery finds only the one feature with a spec and no plan:

```
Workflow({
  scriptPath: "${CLAUDE_SKILL_DIR}/../build-feature/workflow.mjs",
  args: { from: "review-plan", until: "analyze",
          featureDir: "specs/004-product-gl-config",
          wall: "node backend/scripts/wall.mjs" }
})
```

That start brings the base branch up to date, answers included, reviews the plan already on it against the answered spec and repairs it in place; tasks and analyze run again. `from: "plan"` regenerates the plan and discards every review fix. The stages, their tiers, the review and analyze loops and their stops are `build-feature`'s and stated there. `build-feature` installed beside this skill is a precondition: this skill ships no script, because one script exists and it is that one. A workflow starts only from a script the session may read, so a user-level install under `~/.claude/skills/` needs that directory added first — `/add-dir` with the same path, or a `Read` allow rule — where a project-level install under `.claude/skills/` needs nothing. A missing sibling fails at the Workflow call, which refuses a `scriptPath` it cannot read; `npx skills add dulguun0225/scalith -g -a claude-code -y` installs both.

## Every spec question goes to the domain expert, all at once

**The run never edits `spec.md`, and neither do you.** A finding whose only remedy is a change to the spec becomes a question for the domain expert, in plain words, with a recommended answer, what a different answer would change, and a severity:

| Severity | A different answer would change | Build |
|---|---|---|
| `CRITICAL`, `HIGH`, ungraded | what the feature does: a behaviour, the data model, a contract, a state, an error case, a security, money or compliance rule | waits for the answer in the spec |
| `MEDIUM`, `LOW` | a local detail: a message, a label, a default | waits for the answer, or for a person to leave the question open |

A finding whose remedy changes behaviour an earlier feature's spec specifies is still a question for this feature's spec, phrased as a change this feature makes to that feature and naming it. The earlier feature's spec is left as it is, the record of what was built.

Plan review, tasks and analyze collect them instead of stopping at the first, and each later stage works on the recommended answer. After analyze, a run holding an open question returns `status: "needs-human"` with `questions` and `clarifyCommand`, and commits and pushes `<featureDir>/QUESTIONS.md` beside `HANDOFF.md` on the base branch, next to the spec. `/build-feature` refuses while a question is open. Then:

1. **Show the person the questions first, as one table** — number, question, recommended answer, what a different answer would change, severity — built from `questions`, with no paragraph before it. `QUESTIONS.md` and the top of `HANDOFF.md` hold the same table.
2. **When `MEDIUM` or `LOW` questions are open, ask the technical expert one question**, in these words or close to them: "*N* minor questions are left. The build can still start with the recommended answers on them; the domain expert can answer them later or never. Leave them open?" A yes, from the technical expert or relayed from the domain expert, is the only thing that leaves a question open: never on your own judgment, and never under `build-feature`'s high-confidence rule. On a yes, change each `MEDIUM` and `LOW` row's `Left open` cell in `QUESTIONS.md` from `no` to `yes — <who said it>`, commit that file alone on the base branch as `questions: <n> left open by <who>`, then `git pull --rebase origin <base>` and push.
3. **Send the domain expert the line in `clarifyCommand`**, with one sentence saying it is for this feature, is pasted into Claude Code opened in the project, and which questions the build waits for. It is stock `/speckit-clarify`, told to update the base branch from origin first; to write the answers as a new feature with `/speckit-specify` instead when origin has the feature's build branch or every task is ticked; otherwise to ask the questions in `QUESTIONS.md` first; and at the end of every session, whatever is left, to commit `spec.md` on the base branch and push, pulling with `--rebase` and pushing again when the push is refused and stopping in plain words on a conflict. They need no git. They paste it until clarify says nothing is left to ask — five questions per run, each with the recommended answer — and reply. A question left open they answer later or never.
4. **When nothing is open, run `/build-feature`.** When the domain expert replies with a changed spec, run this skill again with `from: "review-plan"` first. That run keeps the questions left open, drops one the spec now answers, and raises again one the spec still leaves open that nobody left open.

A headless session cannot ask: it reports the table and stops.

## Every other stop is yours to resolve

**On any other `needs-human` return — a review finding that survived its fix round, a conflict on push, a missing input — apply `build-feature`'s resolution rule: act on every item you hold a high-confidence recommendation for, record it in `<featureDir>/RESOLUTIONS.md`, restart with the arguments the handoff names, and take an item to a person only as that rule says.** The one thing the rule never allows is an edit to `spec.md`: a spec change is a question for the domain expert, sent as above. The rule and its limits are in `build-feature`; this paragraph repeats it because a session that invokes `/plan-feature` never loads that skill's body.

## What this skill does not do

It does not implement: on `status: "done"` no question is open — `QUESTIONS.md` holds only questions left open, or a stale one has been removed — and the next step is `/build-feature`, which refuses while that file holds an open question. With `push` true, the default, every run that passes preflight pushes its commits to the base branch at its end, after `git pull --rebase`; a pull that brings a change to the spec turns the return into a stop that restarts `from: "review-plan"`. `build-feature` makes the build branch and lands it. It does not write the spec, and it does not message anybody: the technical expert sends the line, on whatever channel the team uses.
