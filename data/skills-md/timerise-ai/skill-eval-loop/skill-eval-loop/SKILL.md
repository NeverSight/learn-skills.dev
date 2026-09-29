---
name: skill-eval-loop
description: >
  Harden an Agent Skill from its automatic agent evals: score every eval run
  against a fixed fidelity rubric read from the agent's own log, fix the skill at
  the root cause of each deviation, cut a patch release, let the release re-run
  the evals, and repeat until every agent scores full. Use when: (1) a skill's
  evals all "pass" but agents still patch its templates, rewrite its tests,
  widen its defaults or skip its handover, (2) a skill has an eval workflow that
  runs Claude Code, Codex and Gemini on every published release, (3) the user
  mentions: fix the skill based on evals, eval loop, iterate until full score,
  score the eval runs, rubric, agent deviations, "based on last evals fix
  skill", "loop to full score", "2:1 majority". Carries the rubric, the log
  readers for three agents, a root-cause table for deviations, the release
  recipe and the stop rule. Skill repositories with a CHANGELOG, tagged
  releases and an `evals/` folder; GitHub Actions and the gh CLI. Not a way to
  write a new skill and not a way to change the eval harness.
---

# Skill eval loop: from "all pass" to full score

An eval that passes its checks has proved that the app type-checks, builds and
runs its tests. It has not proved that the agent used the skill as written. The
insight that shapes this skill is that **the deviations live in the agent's
log, not in the result's checks**, and every deviation traces back to a
sentence in the skill that allowed it. Score the log against a fixed rubric,
fix the sentence, and let the next release's eval prove the fix.

Written by the maintainer who has run this loop on a published skill, from its
first scored release to a unanimous full score;
[provenance.md](references/provenance.md) has the record.

## When to use

A skill that already has automatic agent evals, with results committed to its
`evals/` folder and a workflow that runs on every published release. Run it
after a release's evals land, or when asked to iterate a skill to a full score.
A target named but not present is cloned from its public repository; that clone
and the package registry are not external services in an eval's sense. Clone it
to a scratch directory, and leave a working directory that is not the target as
it was: no dependency, script, config or copied code, only the loop's notes.

| Invocation | Meaning |
|---|---|
| `/skill-eval-loop` | The skill repository in the working directory, from its latest release |
| `/skill-eval-loop score` | Score the latest release's runs and stop; no fix, no release |
| `/skill-eval-loop <path>` | The skill repository at `<path>` |

Pushing tags and publishing releases is outward-facing. Confirm once, before the
first round, that every round may push and publish unattended; then report per
round and stop early only if a run fails outright or a fix would weaken one of
the skill's non-negotiables.

## When NOT to use

| Instead of this | Use |
|---|---|
| Writing a new skill, or turning an app's module into one | `extract-skill` or `skill-creator` |
| Cutting one release without scoring evals | `bumpv` |
| Checking an app's code against its docs | `code-audit` |
| Changing the eval harness, the prompts or the workflow | the index repository, by a maintainer; never from inside this loop |

## Architecture

```
round n:  release vX.Y.Z --> eval workflow (claude-code, codex, gemini-cli)
              |                     |
              |                     +--> bot commits evals/<date>-<agent>-p1-<k>.md
              v
          collect: gh run watch --> gh run download --> read each agent.log
              |
          score: rubric, item by item, per agent --> notes in each result body
              |
          stop? --yes--> final report
              | no
          fix: root cause in the skill --> verify templates --> fix(skill) commit
              |
          release: CHANGELOG, tag, push, gh release create --> round n+1
```

The seam with the target skill is its own rules and recipes, read, never
rewritten: rubric items 4 to 6 come from the target's non-negotiables
([rubric.md](references/rubric.md)), and the template check and commit
convention from its `CLAUDE.md` ([releasing.md](references/releasing.md)).
There is no `adaptation.md`; this paragraph stands in for it.

## Critical facts

1. **Every check can pass while the skill fails.** In the recorded session, all
   21 runs across six releases passed typecheck, build and tests, while agents
   patched templates, converted the suite to another runner and widened a
   security boundary. The rubric, not `result: pass`, is the score.
2. **An agent's template edit can be a bug report.** One run's edit to a
   sanitiser exposed a real open redirect in the skill. Reproduce the claim
   against the template before calling the edit a deviation.
3. **The logs are not symmetric.** Codex's log carries the diffs; Claude Code's
   and Gemini's carry only the final JSON summary. Score those two from the
   summary, and rerun locally when it hints at a deviation.
4. **Agents obey the skill's words literally.** "List both variables" produced a
   file with two of three variables; "no external services are reachable" was
   read as "no package registry". Fix the words, not the agent.
5. **Only `SKILL.md` is read on every activation.** A section deep in a
   reference did not stop an improvisation; the same rule as a hard rule in
   `SKILL.md` did. A rule that must hold goes where it is always read.

## Hard rules

> **Never edit the frontmatter of an eval result, and never delete a run.** The
> frontmatter is what was measured. A score and its reasons go in the body, as
> the notes of the person who ran it, committed as `chore(evals): ...`.

> **Never fix the eval to make the skill pass.** The prompt, the unattended
> note, the harness and the workflow caller are fixed. Every fix lands in the
> skill: its `SKILL.md`, its references, its templates or its tests.

> **Never adopt an agent's change without reproducing the defect it implies.**
> Probe the template with the agent's input first. A real defect is fixed in
> the template with a test that fails on the old code; an improvisation is
> answered with a sentence that forbids it.

> **Never release a round without the template check.** Extract the code blocks,
> type-check them and run the suite; the test count in every doc must match.

> **Never let evals ride a release commit or bump the version.** Score commits
> are `chore(evals)`; a round with nothing to fix re-runs by dispatch, not by a
> release.

> **Never change the stop rule once round one starts, and never stop before it
> says so.** At least three rounds; unanimous full score through round five;
> after that, two of three agents.

## Quick start

1. Read the target's `CLAUDE.md`, `SKILL.md` hard rules and README
   non-negotiables, then write its rubric: [rubric.md](references/rubric.md).
2. Collect the latest release's runs and score them as the baseline:
   [collecting.md](references/collecting.md).
3. Trace each failed item to the sentence or template that caused it and fix it
   there: [fixing.md](references/fixing.md).
4. Verify the templates, commit, release and wait for the evals:
   [releasing.md](references/releasing.md).
5. Score, apply the stop rule, report, and loop:
   [loop.md](references/loop.md).

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| What counts as a full score | rubric, fidelity, templates intact, suite as written, matcher, handover, 8/8, score | [rubric.md](references/rubric.md) |
| Getting and reading the runs | gh run watch, gh run download, agent.log, artifact, Codex diff, Claude JSON, Gemini JSON, run.mjs, local rerun | [collecting.md](references/collecting.md) |
| Turning a deviation into a fix | root cause, deviation, literal wording, improvisation, open redirect, probe, sandbox offline, line budget | [fixing.md](references/fixing.md) |
| Shipping a round | verify templates, tsc, bun test, vitest, CHANGELOG, annotated tag, gh release create, workflow_dispatch | [releasing.md](references/releasing.md) |
| When to stop, what to report | stop rule, minimum rounds, unanimous, 2:1 majority, round table, autonomy | [loop.md](references/loop.md) |
| Where this came from | provenance, recorded session, scores per round, kept deliberately, added | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
