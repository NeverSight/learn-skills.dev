---
name: qa-sweep
description: "QA of a whole repo or one feature (a path or a ticket), with no diff needed: finds defects, weak tests and test gaps, proves each one in code, and adds the regression tests that close them to the project's own unit, integration and e2e suites. A behavior nobody wrote down becomes a question to the user, never an assumption. It only adds tests: no product-code edits, no commits. Use for 'find missing tests', 'find weak tests', 'QA this feature', 'regression tests for ...', 'which modules lack e2e tests', or a QA pass over a module or a ticket."
---

# QA Sweep

Finds **defects**, **weak tests** and **test gaps** in a whole repo or one feature, and adds the regression tests that close them to the project's existing suites. Scripts produce every fact; you read and judge them. This file routes; each mode file says only its part.

**Terms.** A *requirement* is a behavior quoted from a spec, a ticket or the user's own answer; a behavior nobody stated is not one. A *defect* is the app behaving differently from a requirement. A *weak test* passes when the behavior it checks is broken. A *test gap* is a requirement that no test checks. A *test tier* is unit, integration or e2e.

**Requires:** Node 18+, Python 3, git, and the sibling skills `zero-trust-review` (mutation, run folder, sandbox) and `paired-agent-tdd` (its `direct-run.mjs`). The `qa-guard` hook comes with the plugin install. Without it the rules below still hold, but nothing enforces them.

## Paths

```bash
export SK=${SK:-$HOME/.claude/skills/qa-sweep}                      # this skill's folder, absolute (the skill loader prints it)
export ZT_DIR=${ZT_DIR:-$SK/../zero-trust-review}                   # mutate.mjs, sandbox-run.mjs
export PTDD_DIR=${PTDD_DIR:-$SK/../paired-agent-tdd}                # direct-run.mjs
export TIERS_PY=${TIERS_PY:-$HOME/.claude/hooks/pr-test-tiers.py}   # plugin install: $SK/../../hooks/pr-test-tiers/pr-test-tiers.py
test -f "$TIERS_PY" || echo "no pr-test-tiers.py at $TIERS_PY"     # then ask the user where it is (the README installs it); never guess
```

Shell variables do not survive between Bash calls: put these lines at the top of each call. Run every command from the repo root. In this skill, `<run>` is the absolute run folder that `run.mjs start` printed: write it out in full in every command. Never put `$RUN` or any other variable in a redirect target (`> <run>/x`): `qa-guard` reads that target as plain text and denies it.

## Progress checklist

```
- [ ] 1 run.mjs start; <run> noted
- [ ] 2 scope picked: repo inventory, or a feature deep-dive (modes C, B, A)
- [ ] 3 deep-dive only: findings.mjs wrote the report; its path and counts given to the user
- [ ] 4 run.mjs end
```

## 1. Open the run first, close it last

```bash
node "$SK/run.mjs" start --repo .   # prints {"run": "<dir>", "marker": "<file>"}; <run> is that dir, in the OS temp dir
node "$SK/run.mjs" end              # the last step, always
```

The session id comes from `CLAUDE_CODE_SESSION_ID`. If `start` exits 2 with `no session id`, tell the user and ask how to go on; never invent a `--session`, because the hook matches only the harness's own id. If it exits 2 with `a run is active: <dir>`, continue in that run, or end it and start again. Everything you write outside the repo goes in `<run>`.

**When the user asks to stop:** run `end` at once. Then stop any app you started and delete any `qa-explore-*` spec you wrote, or tell the user what is still there.

The sweep judges the code as committed at HEAD. If `git status` shows uncommitted changes outside test files, tell the user before you go on: mutants and quotes see HEAD, direct test runs see the working tree.

## 2. Pick the scope

| The user asks for | Scope | Do |
|---|---|---|
| which modules lack a tier, a repo-wide test overview | Repo inventory | `python3 "$TIERS_PY" --inventory > <run>/inventory.json` (`--depth 2` in a monorepo). Report each module missing a tier, and the `unmapped` and `untiered` lists, from that JSON. While `untiered` is not empty, no tier is proven missing: ask the user which tier those files are, or to map them in `.claude/test-tiers.json`. Nothing else. |
| a feature, a path or a ticket | Feature deep-dive | Modes C, B and A, in that order, each only when needed. |

If you cannot tell which, ask.

| Mode | Read | When |
|---|---|---|
| C, requirements and cases | [`requirements.md`](./requirements.md) | always, in a deep-dive |
| B, code and tests | [`code.md`](./code.md) | to map cases to tests, find weak tests and test gaps, and write tests |
| A, running app | [`running-app.md`](./running-app.md) | when a case is visible only through the running app, or the user asks for e2e |

Read only the files the run needs.

## 3. No proof, no finding

Every requirement, finding and written test goes into `<run>/findings.json` with its proof. Each mode file gives its part of the shape. `findings.mjs` re-checks every proof in plain code, and it decides: what fails lands under Unverified, never in your reply as a fact.

```bash
node "$SK/findings.mjs" --run <run> --repo . --head HEAD --findings <run>/findings.json --tiers-py "$TIERS_PY"
```

It runs the tier inventory itself for the report, writes `<run>/report.md` and prints the counts. Give the user that path and the counts, and report only what the file says.

## 4. Never assume, ask

A behavior with no written source, or unclear wording in a spec or a ticket, becomes a question. Ask all of them as one numbered batch (the format is in `requirements.md`), then wait. Save each answer word for word to `<run>/answers.md` as an `A<n>: <answer>` block. No answer means no test: the question is listed under Unconfirmed.

## 5. Add tests only

Never edit product code, never change or remove a line of an existing test, and never commit or push: the user reviews and commits. You may add a test case to an existing test file, add a new test file, and write anything in `<run>`. While the run is open, `qa-guard` denies everything else, and its message prints the end command. Do not work around a deny: tell the user what was denied.

## 6. Run tests through the ledger

Every test, mutation and coverage command runs through `direct-run.mjs` with `ZT_RUN_DIR=<run>` set. Without it no ledger entry is written, and the proof cannot be checked.

```bash
ZT_RUN_DIR=<run> node "$PTDD_DIR/direct-run.mjs" [--timeout SEC] -- <test command>   # default timeout 120 s
```

Its last stderr line is `ZT-RUN <id> exit=<n>`: that `<id>` is the proof's `ref`. No `ZT-RUN` line means no ledger entry: stop and find out why before you go on. It runs with your rights and your network. The sandbox is opt-in, only when the user asks: for mutation, leave out `--runner` (the sandbox is `mutate.mjs`'s default); for a direct run, use `$ZT_DIR/sandbox-run.mjs`, and read its header first for the mounts and grants it needs.

## 7. Tiering

Judgment stays in this session: requirements, questions to the user, judging surviving mutants, writing tests. Mechanical steps (running the inventory and the scripts, reading files, searching) may go to a low-tier subagent (haiku). A subagent cannot ask the user, so it gets no judgment. The policy is `$ZT_DIR/tiering.md`.
