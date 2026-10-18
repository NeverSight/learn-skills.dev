---
name: evals-from-sessions
description: Turn your own coding-agent sessions (Claude Code, Codex, Pi, Gemini CLI, or other JSONL session exports) into verified Harbor eval tasks. Covers securing and selecting task episodes, building private tasks from a snapshot of your own repository or shareable re-authored tasks, writing a semantic verifier and reference solution, validating with oracle, nop, broken and alternative solutions, a leak probe, harbor check and one smoke run, with two human review checkpoints. Use when the user wants to build or extend a personal coding-agent benchmark or eval from their own agent sessions.
compatibility: Requires Docker, git, Python 3.11+, a recent Harbor (`uv tool install harbor`; examples use 0.24 syntax) and gitleaks 8. Smoke runs and `harbor check` need credentials for one agent/model.
metadata:
  version: "1.0.4"
---

# Evals from your agent sessions

Goal: for each selected trajectory, produce one Harbor task directory that meets
**Done** (bottom). Stop after the smoke run (or after the optional calibration in
step 8). Model comparisons and leaderboards are out of scope.

Harbor layout, paths, network and commands: [references/harbor-contract.md](references/harbor-contract.md).
Starting files: [assets/task-template/](assets/task-template/). Leak probe:
[assets/leak-probe.sh](assets/leak-probe.sh).

## Modes

- **private** (default): the task is a snapshot of the user's own repository at the
  commit before the episode. The reference solution is the episode's own change.
  Private tasks are never published.
- **shareable**: the task is re-authored with new code, data, names and values. Use it
  when the task may be published, or when private mode is not possible.

## Difficulty

Difficulty is a label, not a reason to reject. Record it in `candidates.md`,
`task.toml` (`[metadata] difficulty`) and `report.md`.

- **discovery**: the agent must reach at least one conclusion by combining evidence
  from the repository or data (the *must be discovered* list is not empty).
- **routine**: the instruction states every rule; the agent must still apply them to
  real code or data. Routine tasks are useful to compare setups by cost, time and
  reliability on everyday work.

Reject only **trivial** episodes: one command typed from the instruction alone reaches
the end state, or the task reduces to knowing one flag.

## Rules

- **Unit = one task episode**: one user request plus the work that satisfied it. Use
  only user-driven sessions.
- **Shareable mode: re-author, never copy.** Keep the *behavior* the episode required.
  No source code, private data, hostnames, usernames, emails, credentials or model
  outputs may appear in the task.
- **No future history (both modes).** The image contains no commit, branch, tag,
  reflog, stash, remote, hook, message or file from the episode or after it.
- **Offline and deterministic.** The task never *needs* the network. `tests/test.sh`
  downloads nothing. Fixtures are fixed files or use fixed seeds and timestamps.
- **Hidden evaluator.** Never `COPY` `tests/`, `solution/` or hidden fixtures into the
  image.
- **Public code needs an allowlist.** If the repository or task is derived from public
  code, set `network_mode = "allowlist"` (see contract) or reject the episode.
- **Keep all evidence** on durable disk, never in `/tmp`. Never delete job directories
  or earlier task versions.
- **Publication boundary.** `provenance.md` holds source paths and names. It never goes
  into the image or a published copy; leak checks cover every other task file.
- **Cite JSONL line numbers** for every request, correction, outcome and evidence claim
  in `candidates.md` and `provenance.md`, not turn numbers.
- No parsers for trajectory formats. Read raw JSONL with `jq`, `head` or a one-liner.

## Workflow

### 0. Secure the sessions

Copy the sessions into a working directory and work only on the copy. Usual locations:

| Agent | Sessions |
|---|---|
| Claude Code | `~/.claude/projects/<project>/<session>.jsonl` |
| Codex CLI | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` |
| Pi | `~/.pi/agent/sessions/` |
| Gemini CLI | `~/.gemini/tmp/<hash>/chats/` |

Some agents delete old sessions (Claude Code after 30 days by default,
`cleanupPeriodDays`), so copy early.
Run `gitleaks dir <copy> --redact --no-banner --report-path <workdir>/gitleaks.json`
and record the number of hits in `candidates.md`. Never write a secret anywhere.
Skip subagent files (`<session>/subagents/`, reviewer or guardian runs): they have no
user request or correction.
Check `harbor --version` and record it in `report.md`. The contract shows Harbor 0.24
syntax. Before the first use of each command, confirm its flags with `--help` on the
installed version, and take `schema_version` from the skeleton that `harbor task init`
creates. If a command does not exist in your version (for example `harbor check`),
record "not available" in `report.md` and continue.

### 1. Inventory, select and choose the mode

Skim each session: every user request, later corrections, final files, commits and
commands, how it ended. Write `candidates.md` with one row per substantive request
(non-coding requests go into one summary line):

| session | lines | user_goal | decisive_correction | outcome | mode | decision / reason |
|---|---|---|---|---|---|---|

Keep an episode only if all hold:
- the result can be checked from final files, git state, or command output;
- a competent human would need about 1 hour or less;
- after removing live services, accounts, GPUs and large data, real work remains;
- **not trivial:** one command typed from the instruction alone does not reach the
  end state;
- it is real recurring work, not a one-off chat question.

Reject open-ended research without a checkable conclusion, taste-only UI work, pure
live-infrastructure operations, and episodes whose only success signal was "the user
said OK". Prefer episodes with a decisive user correction or a real failure of the
source agent. Label each kept episode `discovery` or `routine` (see Difficulty) in the
decision column. If no episode passes, say so and stop; do not lower the bar.

**Mode.** Use `private` if the source repository is available locally and the episode
ended in an identifiable commit or a clean diff. Otherwise use `shareable`, or reject.

**Checkpoint 1** (see below) after `candidates.md`.

### 2. Freeze the behavior spec

Write `<task>/provenance.md` before any other task file (it is never copied into the
image): source session, path and JSONL lines; mode; for private mode the repository, parent
commit and episode commit; **requirements** (3–8 bullets "the solution must ...");
**failure modes** (source agent mistakes, user corrections, edge cases the user stated;
each stays observable and each must be caught by a check); the **must be discovered**
list.

**Must be discovered.** Conclusions the agent reaches only by combining evidence from
the repository or data. Documented API rules, explicit user constraints, the choice
of a standard command, and outputs of a formula or decision tree given to the agent
do not count. A tie-break or convention the source agent chose, and the user never
confirmed, is reference behavior, never an item. For each item, quote the nearest user
sentence and the evidence lines; drop the item if the sentence states it. Each item
counts only if a near-miss solver that skips it fails (step 6). The list freezes when
Checkpoint 2 is approved; review notes may change it once before that, never after. If it
is empty, the task is `routine`: keep it and state every rule in the instruction. If a
later fix must state an item in a task file, reject the episode. Every explicit user constraint
goes into the instruction; withholding one creates a hidden requirement.
- Good: "Python's low pass rate comes from verifier errors, not model failures"; the
  agent finds it in run logs and answers with a closed-set `root_cause`.
- Bad (too easy): the README of a stand-in lists the frozen items as rules.
- Bad (hidden requirement): the user said which run to take the cost from,
  and the instruction left it out so it would look "discovered".

**Checkpoint 2** after `provenance.md`.

### Checkpoints

At each checkpoint stop, print the absolute path of the file, and wait for approval.
If the run is unattended, write `AWAITING_REVIEW` (one line: the file path) next to the
file and end the run without building the task. Continue only after approval in chat
or an `APPROVED` file next to it; then delete `AWAITING_REVIEW`. Apply review notes
once; a second "revise" is a rejection.

### 3. Author the task

Copy `assets/task-template/` into the task directory **except `provenance.md`**: never
overwrite the approved provenance (`rsync -a --exclude provenance.md`, or `cp -n`).

- **instruction.md**: keep the canary line first. Goal; inputs; the required **end
  state** and exact interfaces (CLI arguments, paths, JSON fields and types, exit
  codes); what may change; what is not required. State precise rules only for output
  form (types, rounding, ordering, tie-breaks). Never state the rule that turns
  evidence into a *must be discovered* answer. State every explicit user constraint.
  Scope sentences ("only X is required") need no check; constraints ("do not modify
  `data/`") need one (for example an evaluator-owned hash).
- **Investigative episodes** get a closed-set answer: a JSON file with enum fields
  (with plausible wrong options) plus evidence as record ids or counts. Never grade
  free prose with keywords. Field names must not presuppose the answer. Give the data
  enough records and distractors that the answer cannot be read off a few files in one
  pass.
- **private environment/**: `git archive <parent-commit>` of the repository into
  `environment/repo/`; the Dockerfile re-inits it as one commit (template). Move tests
  added by the episode commit to `tests/` and delete them from `environment/`. Strip
  `.env`, credentials and private data the task does not need. `gitleaks dir
  environment/` must report zero hits.
- **private solution/**: `git diff <parent> <episode-commit>` (minus moved tests) as
  `solution/fix.patch`, applied by `solve.sh`.
- **shareable environment/**: a small new starter repository or data, incomplete or
  buggy the way the episode was.
- **Live services** (both modes): a small local stand-in that enforces the constraint
  that made the episode hard, as readable code with reference-style docs. The docs never
  say which option fixes which error, warn about a failure mode, or give the procedure. Do not
  add difficulty the episode never had. Reject if the task reduces to knowing one flag.
- **task.toml**: name, version `1.0.0`, timeouts, resources; under `[metadata]`:
  `source_session`, `category`, `mode`, `difficulty`, `visibility` (`"private"` in private
  mode; `"public"` for a shareable task you may publish). In shareable mode,
  `source_session` is an opaque label (for example `episode-03`); the real session id
  stays in `provenance.md`.
  Pin the base image tag and language packages; do not pin exact apt versions.

### 4. Write the verifier

Keep the template `test.sh`: it always writes `/logs/verifier/reward.txt`. In
`tests/verify.py` (keep the canary line):

- **Contract in both directions.** Every check follows from an instruction sentence;
  every normative sentence has a check with a fixture that separates right from wrong.
  Hidden fixtures hit every enum value and error exit code. Delete untestable sentences.
- **Use only the stated interface.** Swap hidden fixtures into stated paths; never move
  the agent's code elsewhere.
- **Own the baselines.** Expected outputs live in `tests/` or come from fixed fixtures;
  never from the post-agent state or from files the agent can edit.
- **Compare JSON by meaning** with the template's `same()`. Use a tolerance for computed
  floats. Do not grade formatting the instruction does not fix.
- **Exact lists only when determined.** Grade an evidence array as an exact list only if
  the instruction and data fully determine it. For freely chosen supporting evidence,
  grade membership and coverage (known IDs, at least one of each required kind).
- **No incidental checks**: no file allowlists, helper-file bans or byproduct failures,
  unless file hygiene was part of the episode.
- Print one `PASS`/`FAIL <reason>` line per check. Stdlib only.

### 5. Write the reference solution

`solution/solve.sh` reaches the correct end state legitimately (private: apply
`fix.patch`). It must not touch `/tests` or the verifier output.

### 6. Validate the task

Keep validation files in `<tasks-dir>/../validation/<task-name>/`, never inside the
task. Commands are in the contract. Required evidence:

1. **nop fails**: `-a nop` gives `0.0` (starter state).
2. **Oracle passes**: one job `-a oracle -k 5`, all five `1.0`.
3. **Mutants fail** (`mutants/*.sh`, each run as `solve.sh` of a temp copy, all `0.0`):
   one **near-miss per failure mode and per *must be discovered* item**. Each is a coherent
   solver that makes exactly that mistake and follows it through, not a one-field flip
   of the expected answer. Add `visible-only.sh` if there is a visible sample.
4. **Alternative correct solution passes** (`alt-correct.sh`, `1.0`): a solver that reads
   the inputs, written without the reference or the expected fixture, making different
   free choices (other valid evidence, structure, default formatting). Never hardcode
   the answer.
5. **Leak check**: grep the task directory for source strings (paths, hostnames,
   usernames, emails, repo names, keys); shareable expects no hits, private expects
   only the snapshot itself. `gitleaks dir <task>/environment` gives zero hits.
6. **Leak probe**: run `assets/leak-probe.sh <task> <solution-strings.txt>` (strings
   only the reference diff contains, several per answer value). Expect one commit, one
   reflog entry, no remotes, tags or hooks, and zero string hits inside the built image.
7. **harbor check**: run it, copy every finding into `report.md`, and fix or justify
   each `fail`.

8. **Contract audit before the first smoke**: re-read the instruction sentence by
   sentence against the checks; remove or check every normative sentence now.

If any result is wrong, fix the verifier or the instruction, bump `version`, repeat.

### 7. Smoke run with one real agent

Run one real agent once, with the reasoning effort passed explicitly. The trial must
finish without an `exception_info`. Classify the result:

- **Model mistake** (clear task, wrong answer): the task is final.
- **Ambiguity** (an unstated requirement): if the verifier can grade it without a new
  sentence, fix `tests/`; otherwise reject the episode. Never edit the instruction
  after the first smoke run. A run can have several classes; record each check.
- **Verifier false negative** (a correct end state failed): fix or remove the check;
  never widen a grader just to accept this output.
- **Pass**: record the tool calls, time and cost. For a `discovery` task, note for
  each item whether the agent had to find it. If a `discovery` task passed in fewer
  than ~10 tool calls, relabel it `routine` in `task.toml` metadata and `report.md`,
  and note why. A routine pass is a valid result, not a defect.

After the first smoke run, fix only a reproduced verifier or stand-in defect, and only
in `tests/` or the stand-in. If a fix would state a frozen item, reject the episode.
After any fix: bump `version`, redo step 6, smoke again. **At most two** version bumps
after the first smoke run; a third means reject.

Optional **please-hack smoke**: one more run with the prefix template in the contract.
Any `1.0` without a correct end state is a verifier defect.

### 8. Calibration (optional)

Run 2 configurations × 3 runs. Flag **too-easy** if every run passes in fewer than
~15 tool calls. Flag **audit** if no run passes, and check the task for defects before
keeping it. Record both flags in `report.md`.

## Done

The run always ends by writing `report.md`, also after a rejection or an error. Never
end the run right after a job finishes. Per task, write `<tasks-dir>/../validation/<task-name>/report.md`: source session and
JSONL lines; mode; difficulty; checkpoint decisions; the frozen list; a table *instruction sentence →
check → separating fixture or mutant*; results of nop, oracle ×5, each mutant,
`alt-correct`, leak check, leak probe, `harbor check` findings; every smoke run (agent,
model, effort, reward, steps, cost, job path, classification); calibration flags.

- [ ] both checkpoints approved; difficulty recorded (`discovery` or `routine`); not
      trivial; no frozen item stated;
- [ ] nop `0.0`; oracle `1.0` ×5; `alt-correct` `1.0`; every mutant `0.0`;
- [ ] every normative sentence has a separating check; baselines are evaluator-owned;
- [ ] no leaked strings, zero gitleaks hits, leak probe clean; evaluator files absent
      from the image; `harbor check` findings recorded;
- [ ] the last smoke run finished without infrastructure errors and is classified.

Done means *ready for human review*, not accepted. Reviewer agents and then the user
check the frozen list against the task files and look for hidden requirements before
the task enters the benchmark. Any later material change needs a new `version`; do not
compare scores across task versions.
