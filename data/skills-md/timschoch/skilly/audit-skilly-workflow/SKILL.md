---
name: audit-skilly-workflow
description: Find where the repo's own instructions, the user's global instructions, hooks, lint and CI contradict or duplicate what skilly installed. Writes an HTML report, edits nothing.
disable-model-invocation: true
---

# Audit skilly workflow

The harness loads every instruction file side by side. No file wins by default: on a conflict the agent follows either one. This audit finds those conflicts between skilly-installed files and everything else, and reports them. It edits nothing.

## 1. Run the script

```sh
node .agents/skills/audit-skilly-workflow/scripts/audit.mjs
```

`consumer: false` → tell the user the `reason`, stop.

| Field | Holds |
| --- | --- |
| `sources` | every instruction file: `owner` (`skilly`, `overlay`, `repo`, `global`), `loaded` (`always`, `on-demand`), `bytes` |
| `skills` | name and description of each installed skill |
| `tier` | the repo's tier from `.skilly/config.json`; a `verify` step with its own `tier` runs only at that tier |
| `gates` | skilly commit gate values; `verify` stages (commit, push, ci, nightly) with their steps; other commit gates and naming linters found in config |
| `findings` | config defects: `kind`, `where`, `detail` |
| `report` | `file` to write; `ignored` says whether git ignores it |

## 2. Confirm the findings

Open each finding at `where`. A false positive (e.g. a path the text names as optional) → drop it, count it. Done when every finding is kept with a one-line fix or dropped. A config defect you spot later while reading → add it as a kept finding.

## 3. Extract claims

Read every source in full, `always` first. A skill description is a claim too: its trigger → use that skill. Read a full `SKILL.md` only when a source names that skill. Gate values and `gates.*.others` configs are claims with their own `file:line`.

Write each instruction as a claim: situation → required action, with `file:line`. Skip lines with no action.

- Bad: "Delegation" (no action)
- Good: "task finishes in one pass → no subagent" (`.claude/rules/<bundle>-delegation.md:3`)

An `overlay` merges with its base rule. Judge other sources against the merged rule, not the base alone.

Non-skilly sources over 150 KB in total → split them into a few batches of similar size, one subagent per batch, model and effort per the repo's model rule. Pass each the skilly claim list; it returns matched pairs only.

Done when every source has its claims.

## 4. Match and judge

Match every skilly claim against every other claim by situation, never by shared words. "Stage the work and stop" and "push and open the PR once it is ready" share no word and still collide.

Also match:

- a number or list in text against `gates` (text allows 90 chars, the gate allows 72)
- an instruction to skip a gate (`-n`, a disabled hook) against that gate
- a text that says when to run a check ("run the tests before each commit") against the `gates.verify` stage that runs it
- a hook or CI job that runs a check itself instead of the `verify` stage
- each entry in `gates.*.others`: read its config, compare its values with the skilly gate

Give each pair one kind:

| Kind | Test | Report |
| --- | --- | --- |
| contradiction | following both at once is impossible | flag |
| restatement | same action in other words; drifts on the next edit | flag |
| override | an `overlay` changes its own base rule | show, never flag: the repo's sanctioned override |
| precedence stated | one side says which source wins | show |
| complement | different situation, or both hold | drop, count |

A value that differs (limit, list, model name) makes a restatement a contradiction.

Done when every skilly claim is matched or marked unmatched.

## 5. Name the fix owner

Synced skilly files are overwritten on every sync.

| Losing side lives in | Fix |
| --- | --- |
| `owner: skilly` | never edit in place. Repo deviates on purpose → `.claude/rules/<rule>.local.md`. Skilly is wrong → issue in `timschoch/skilly` |
| `owner: repo` | delete the restatement and link the skilly rule, or rewrite to agree, or move a deliberate deviation into `.local.md` |
| gate config (commitlint, lint, CI, hooks) | one enforcer per rule; align values with the skilly gate |
| `owner: global` | the user edits it; propose the wording |
| a script finding | the file at `where`; one line of fix |

## 6. Write the report and stop

Write one self-contained HTML file to `report.file`. Create its directory. A hook or sandbox blocks the write → tell the user the path and the block, stop. Never write the report somewhere else.


Content:

- flagged: contradictions, restatements, kept findings; each row both quotes with `file:line`, kind, fix owner
- shown: overrides, precedence stated
- counts: complements and dropped findings
- sources read, with owner

`report.ignored` is false → tell the user git does not ignore the report. Do not edit `.gitignore`.

In chat: the report path, counts per kind, and one numbered line per flagged item. Stop. Fix only the items the user picks.
