---
name: mathodology-workbench
description: Use when setting up, running or checking a contest workspace, recording experiments, keeping paper numbers, figures and LaTeX consistent with results, or installing the Mathodology hooks.
---

# Mathodology Workbench

The other skills guide judgment; this one executes. `scripts/mtd.py` (Python 3.9+,
standard library only) links the five stages of a contest through files, so each
stage reads what the previous one actually produced:

| Stage | Produces | Executable support |
|---|---|---|
| Problem brief | `problem/questions.json`: per question, deliverables, metrics, inputs, assumptions, dependencies | `mtd.py brief` lists the numbered questions; you fill in the rest |
| Experiments | code under `code/`, a recorded run per execution | `mtd.py run -- python code/q1.py` logs command, seed, inputs, outputs, exit code; placeholder scripts and stub functions are flagged |
| Results | `results/*.json` in the contract below, written by code | validation, provenance and staleness against the code that produced them |
| Figures | images drawn by scripts that read results | traces script → data → image; flags stale, missing, corrupt or low-resolution figures |
| Paper | LaTeX citing `\res{q1.rmse}`, or Markdown citing `{{res:q1.rmse}}` | `mtd.py sync` writes `paper/results.tex` and booktabs tables in `paper/tables/`; checks numbers, refs, cites, figures and the compile log, and math and citations in Markdown |

Run it from the workspace (or pass `--root`); the path below is relative to a
project with the skill installed:

```bash
python3 .claude/skills/mathodology-workbench/scripts/mtd.py init --paper-template
python3 .claude/skills/mathodology-workbench/scripts/mtd.py brief          # after the statement is in problem/
python3 .claude/skills/mathodology-workbench/scripts/mtd.py run --seed 1 -- python code/q1.py
python3 .claude/skills/mathodology-workbench/scripts/mtd.py status        # every stage; --json for tools
python3 .claude/skills/mathodology-workbench/scripts/mtd.py check --compile   # exit 1 on errors
```

A workspace is a folder with `.mathodology/`, or with `problem/` and `paper/` as
Mathodology Studio creates them. Contracts and every check are described in
[references/contracts.md](references/contracts.md).

## Results contract

Experiment code writes one JSON file per question or analysis:

```json
{"schema": "mathodology.results/1", "question": "Q1",
 "values": {"rmse": {"value": 0.0912, "unit": "kWh", "digits": 3, "ci": [0.081, 0.101]},
            "best_cost": 1532.4},
 "tables": {"compare": {"columns": ["model", "rmse"], "rows": [["ARIMA", 0.12], ["ours", 0.091]]}}}
```

In LaTeX, `\input{results}` in the preamble, then write `\res{q1.rmse}`,
`\resci{q1.rmse}` and `\resunit{q1.rmse}`. Each table becomes
`paper/tables/q1-compare.tex`; put `\input{tables/q1-compare}` inside your own
`table` float. A rerun followed by `sync` updates
every number in the paper. Numbers typed by hand are still compared with the
results, allowing for the rounding shown: a value that no longer matches after a
rerun is reported as a near miss.

## Hooks

`mtd.py install-hooks` (also run by `init` and by Mathodology Studio) merges
four Claude Code hooks into `.claude/settings.json`, preserving other settings:

- Session start: a short status of every stage enters the agent's context.
- Before an edit: hand edits to `results/*.json` and the generated
  `paper/results.tex` and `paper/tables/*.tex` are refused; results change by rerunning code. A user who
  really wants manual results sets `"allow_result_edits": true` in
  `.mathodology/config.json`.
- After an edit or command: an edited paper file is checked at once; when a
  command changed results, the contract is validated and the macros refreshed.
- Stop: if errors remain (unknown `\res` key, missing figure, undefined
  citation or reference, invalid results, LaTeX errors in a current log), the
  agent is asked once to fix them or explain why they remain.

`"stop_gate"` in `.mathodology/config.json` is `errors` (default), `warnings`
or `off`. A check that cannot run (no TeX engine, a crashed checker) is a
note and never blocks. Hooks are silent outside a workspace and never fail the session.
Codex, Gemini CLI and other agents do not load these hooks: run
`mtd.py check` before handing over a draft.

## Judgment the checks cannot make

The checks are mechanical. They do not decide whether a model is appropriate,
whether a baseline is fair or whether a claim follows from the evidence; use
[review questions](../mathodology-award-gates/SKILL.md) for that. When the
report and the paper disagree, correct the paper from the results or rerun the
experiment; never edit results to fit the text. A number reported as unmatched
may be a parameter or a literature value: trace it rather than delete it.
Report failed or abandoned runs that matter for the conclusions. Figures follow
[figure presets](../mathodology-figure-presets/SKILL.md); have figure scripts
read results files rather than retyping values so the staleness check works.
