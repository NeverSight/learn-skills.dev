---
name: reduce
description: "Improve the structure and simplicity of a code change, codebase, or implementation plan. Preserve required behavior, and propose removal of behavior that nothing needs. Use for scoped reduction or untangling."
---

# Reduce

Find what a target can remove, prevent, reuse, or simplify, and report it.

The work has one shape:

1. Scope: collect the facts. Fix the target: a branch, a diff, a repository, or a plan. Read every file, and group the files or hunks into features. A feature is one thing that the code does. List the sources with the goals that they state, and the results of the installed analyzers.
2. Map: describe each feature. Write down each result, its consumers, and what each consumer does with it. State what the feature is for, and the questions about it that only the user can answer.
3. Design review: judge the whole target. State what the target is for and which capabilities it needs. Make a second pass over the design: knowing the current implementation, how would you build it from scratch? Compare, and write `design.md`: the purpose, findings, decisions, directions, and a plan. Check it against the code yourself.
4. Check: judge each feature, one reviewer for each feature. The reviewer gets `design.md`, applies the checks, and then does an open review. Each check gets a line: `absent` with the place examined, or its findings.
5. Report: combine the design and check outputs into one report.
6. Close: act on the report only when implementation is requested.

Each step does its own work only. The scope step and the map step do not judge the target, and the purpose is stated once, in the design review.

The checks are the files in [checks](checks/README.md). They come from good practices, slop patterns, and sourced real cases.
A check that finds nothing still gets a record. A skipped check and a clean check must look different.
A quick run does steps 2 to 5 in one review, without subagents. It looks over every check topic and design reference, and studies only those that apply. See [modes](#modes).

## Boundaries

Review the named target. Access other checkouts, deployed settings, live databases, services, or remote hosts only with assignment authorization.
Keep records and scratch checks outside the target. Change its checkout, plan, or tracker only when implementation is requested.
Use subagents for the map, design, and check steps, as below.
Execute project code only with isolation that excludes credentials and unrelated data. A remote job runner alone is not isolation.

## Match the target

| Requested target | Playbook |
|---|---|
| Diff, branch, PR, commit range, changed paths | `code` |
| Existing paths, package, subsystem, repository, including existing edits | `codebase` |
| Implementation plan | `plan` |

For partly implemented plans, use `plan` and recommend a `code` run for the implemented parts.

## Modes

| Mode | Use it when | Steps |
|---|---|---|
| `unattended` | The default for a target that is too large for `quick` | All steps. Asks the user nothing, and puts every open question in the report. |
| `attended` | The user asks for an in-depth reduce | All steps. Stops twice. After the map step, it asks one merged list of the questions about the features. The design step then uses the powerful model, and asks about the design findings that need the user's decision. |
| `quick` | The user asks for a quick or light reduce, or you can read the whole target in this session: about 30 files and 3,000 changed or reviewed lines or fewer | Scope, one quick review that you do yourself, and close. Asks the user nothing. The code and codebase playbooks only. |

An in-depth request always uses `attended` mode, whatever the size of the target.
In attended mode, ask at most five questions in one message, largest saving first, each with your recommendation. Ask the rest in later rounds.

## Follow the steps

The driver releases one step at a time. In the map and check steps, it releases one packet for each feature. In the design step, it releases one packet for the whole target.
Set `reduce_skill` to this skill's directory.

```sh
"$reduce_skill/scripts/reduce-step" start --playbook <code|codebase|plan> --target <checkout or folder> [--mode attended|quick]
```

To review one section of a checkout, pass its folder as the target. Paths are then relative to that folder, and the files outside it need no rows.

`start` prints the records directory, a new folder in `~/.local/state/reduce/runs/`. Set `records` to it. To use another directory outside the target, pass `--records`.

1. Read the step or check that the driver prints. Do only that work.
2. Fill every field of its record file. Cite evidence for each instruction, or record why it does not apply.
3. Run `"$reduce_skill/scripts/reduce-step" submit --records "$records"`. When it rejects the record, fix the reported problems and submit again. Read its notes, and fix only those that change a conclusion.
4. Continue until the driver reports that all steps are complete.

Do not read step files or check files before the driver releases them. Run `next` to print the current item again, and `status` to list progress.

Write every record and reply by reading and judging. Do not write scripts or programs that create records, replies, or findings.

## Map, design, and check steps

The driver writes packets for these steps. A subagent needs nothing else.
- A map packet holds the map instructions and the feature.
- The design packet holds the design instructions and lists the scope and map records to read.
- A check packet holds the feature's code, its map record, `design.md`, the other features, and the reply format. A second file holds the checks that always apply, in full, and the file and pattern of each check of every topic. The reviewer reads a check's file only when its pattern appears in the feature. After the checks, the reviewer does an open review for what no check covered.

At the start of each of these steps, run `release --records "$records"`. It releases every item of the step and prints JSON with the `model` class and the `packet` and `record` paths, relative to `$records`.

1. Start one subagent for each packet, in parallel. Give it only this task: "Read <packet path>. Follow it, and write your reply in <record path>."
   For the map step, the JSON also gives `subagents`. `feature` is the default: one subagent for each packet. With `one`, give all the map packets to one subagent: "Read these packets: <packet paths>. They differ only in the feature. Follow each one, and write each record in the file that its packet names." One subagent can map about 3,000 lines, so split a larger target among several subagents. An arrangement that the user names takes priority.
   Use the model class that the driver names; see [models](#models). Do not give a subagent the driver or this file.
2. Without subagents, do the packets yourself, one at a time, as each packet says.
3. In attended mode, wait for every map record, and read the `## Questions` of each one. Make one list for the user:
   - Merge the rows that ask the same thing in several features.
   - When an entry of another map record answers a row, write that entry's ID as the answer, such as `F4:B7`, and do not ask the row.
   - Ask the user the merged questions, largest part first.

   Record each answer of the user in every row that it covers. Then submit the records.
4. After the design subagent writes `design.md`, check it against the code yourself. For each finding, read the code that it cites. Correct or remove a finding that the code contradicts. Add the findings that it missed. In `## Parent review`, record what you confirmed, changed, and added.
5. In attended mode, after the design subagent writes `design.md`, ask the user about each row of its `## Decisions`. Record each answer there. Set an accepted finding's decision to `autonomous`, and a rejected finding's rung to `keep`.
6. When a record is written, run `submit --records "$records" --item <step>:<feature>`, such as `--item 2-map:F1`. For the design step, run `submit --records "$records"`.
6. When the driver reports problems, send them to the same subagent to fix. Then submit again.

The driver rejects a record only when a later step cannot use it: the target changed, a section is missing, a feature has no files, a changed file is in no feature, a row ID has no prefix, a check or a line of `leads.md` has no line, or a finding's rung, effect, or decision is not one of the listed values.
In a record, a row is a line that starts with `- ` and has a `|`. Any other line is a note.
It prints other problems, such as a cited file that does not exist, as notes. It does not judge citation form or conclusions.

## Models

The driver names a model class for each packet: the configured class for the map, design, and check steps, and `powerful` for the design step in attended mode.
A run has many check subagents, so the checks use the `cheap` class by default. The map and design steps use the `standard` class.
You are the parent: you do the scope, report, and close steps yourself, on your own model.
The models come from `~/.config/reduce/config.json`. The [reduce-setup](../reduce-setup/SKILL.md) skill asks the user and writes it. Installs and updates do not change it.
When the file does not exist, every subagent uses your own model. A run does not stop for a missing file.
[`config.example.json`](config.example.json) shows the shape.

| Key | Value |
|---|---|
| `map` | `cheap`, `standard`, or `powerful`: the map subagents' class. The default is `standard`. |
| `map_subagents` | `feature`: one map subagent for each feature, in parallel. `one`: one map subagent for all the features. The default is `feature`. |
| `design` | The design subagent's class in unattended mode. The default is `standard`. |
| `checks` | The check subagents' class. The default is `cheap`. |
| `models.<harness>.<class>` | The model for each class, by the tool that starts the subagents: `claude-code` for the Agent tool, `codex` for `spawn_agent`, or `t3` for `delegate_task`. A session that has `delegate_task` uses `t3`. A T3 value is `{"provider": "...", "model": "..."}`. A value can also be a list of models: give each subagent the next model of the list, in turn. When a model of the list cannot start, use the next one, and report it. |

A missing or `null` model means the parent's own model. A model that the user names takes priority.
Run `"$reduce_skill/scripts/reduce-step" config` to validate the file and print the class and the models of each step.

## Steps

| Step | Purpose | Records in `$records` |
|---|---|---|
| `1-scope` | Collect the target, its limits, its features, its sources, and the tool results | `1-scope.md` |
| `2-quick` | Quick mode only: steps 2 to 5 in one review that you do yourself | `review.packet.md`, `review.checks.md`, `review.md` |
| `2-map` | Describe each feature: its results, their consumers, and what it is for | `2-map/<feature>.md` |
| `3-design` | Judge the whole target: its purpose and capabilities, a second pass over its design, and the plan of the changes | `design.md` |
| `4-check` | Judge each feature: its checks, then an open review | `4-check/<feature>.packet.md`, `4-check/<feature>.checks.md`, `4-check/<feature>.md` |
| `5-report` | Combine the design and check outputs into `review.md` | `5-report.md`, `review.md` |
| `6-close` | Act when requested, then clean up | `6-close.md` |

## Files

| Folder | Contents |
|---|---|
| `steps` | One file for each step. The scope and map steps have one file for each playbook. |
| `checks` | One folder for each topic, and one file for each check. The index lists each topic's checks in order. Some checks are sourced real cases. |
| `evidence` | How to collect and judge evidence: tools, execution checks, and cases where shorter code changed behavior. |
| `design` | The design references that the design step applies, from pstack and Matt Pocock's `codebase-design`. Their licenses are in [design/LICENSES.md](design/LICENSES.md). |
| `guides` | Fixed behavior and the ladder, the sources of the cases, rules for the plan playbook, the workflow and phase rules that the steps cite, and the retrospective. |
| `scripts` | The step driver, and `reduce-retro`, which collects a run's evidence for a retrospective. |

## Words in the references

The checks, evidence, and guides keep the words of their sources. Read them with these meanings:

| Word | Meaning in the steps |
|---|---|
| candidate | A place that a signal or case flags, before evidence decides it |
| unit | One part of a feature that the ladder can change: a function, branch, guard, type, file, test, dependency, comment, or plan item |
| group, section | Features or plan parts that share an owner or acceptance context |
| recommendation | A finding |
| inventory, entry | The map step's `## Inventory` or `## Requirements` rows |

## Retrospective

A retrospective finds what a run teaches about this skill. Run one after a run closes, or at any time for a run that is open or stopped.
The driver logs the session of each command, so the retrospective finds the transcripts of the parent and its subagents.

```sh
"$reduce_skill/scripts/reduce-retro" collect --records "$records"
```

1. Give a subagent of the `standard` class only the task that `collect` prints. Without subagents, do it yourself.
2. Run `"$reduce_skill/scripts/reduce-retro" record --records "$records"`. It checks `retro/retro.md` and adds its observations to the ledger, `~/.local/state/reduce/ledger.jsonl`.
3. Show the user the proposals. Change the skill only after the user approves a proposal.

`reduce-retro list` shows each run in the runs folder and the state of its retrospective. Give it folders to search others, such as a records folder passed with `--records`. A run from before the driver logged sessions still works: `collect` searches the transcripts for the run. The packet holds transcript text, so it stays in the records folder.

## Fixed behavior and the ladder

Read [fixed behavior and the ladder](guides/fixed-behavior.md) before the scope step. It gives the class of each result, the decisions that the user owns, and the rungs.
The packets cite that file, so a subagent does not need this one.

Create plans only when requested or required.

Sources: [Desloppify review cycle](https://github.com/peteromallet/desloppify#how-it-works), [make-native design questions](https://github.com/Sloydai/make-native/blob/add-make-native-skill/skills/make-native/SKILL.md).
