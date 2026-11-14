---
name: agent-ready-environments
description: Audit or set up a repository, or a body of engineering guidance, for how well it lets coding agents produce correct work without a human acting as the test suite. Use when starting a project, auditing an existing repository, auditing instruction files, skills, and review gates, or reviewing this skill after a model release or guidance change.
---

# Agent-ready environments

An agent stops when the work *looks* done [A1]. The environment decides whether
"looks done" and "is done" are the same thing. Every pillar in this skill does
one of three jobs:

- **Tell** the agent what it cannot see in the repository.
- **Check** the work with something that comes back red or green.
- **Bound** what the agent can touch, and who signs off.

Each pillar has a reference file with its sources, what good looks like, the
audit check, and anti-patterns; the pillar table links them. When a new model ships or a source changes, review
this skill with [maintenance.md](references/maintenance.md).

## Durable and decaying guidance

Vendor guidance now separates advice that compensates for model weakness from
advice that gives the model something it cannot get for itself [A1, "What you
can stop doing"]. Invest in the durable column.

| Decaying: compensates for the model | Durable: gives the model what it cannot get |
| --- | --- |
| Emphasis, `IMPORTANT`, ALL CAPS | Facts that are not in the repository |
| "Think harder", "keep going", "don't be lazy" | A check that returns pass or fail |
| Architecture tours and file-layout descriptions | Deterministic enforcement of zero-exception rules |
| Aggressive context management | A running, observable, seeded environment |
| Delegating to a subagent "for a better answer" | An independent reviewer that did not see the author's reasoning |

This skill argues the following from that split; the vendors do not rank the
pillars themselves. As models read code better, documentation (pillar 4)
shrinks. No model improvement lets an agent observe an app it cannot start or
data that does not exist. So the reproducible environment (pillar 6) is the
most durable investment, followed by the static and test gates (pillars 2 and 3)
that make the work checkable.

## Placement: advisory or enforced

Guidance travels on two channels [A1]:

- **Advisory**: the prompt, `AGENTS.md` / `CLAUDE.md`, skills. The model weighs it and may decide it does not apply.
- **Enforced**: hooks, deny rules, the sandbox, the type checker, linters, required CI checks. Each runs at its action boundary (a tool call, a commit, a merge) whatever the model decides.

Put each rule on the channel that matches its exceptions:

- A rule with zero exceptions is enforced. OpenAI reported the same move in early 2026: when documentation falls short, the rule becomes code [O1].
- An advisory line that keeps getting missed has one of two causes [A1]. Either it is a rule that cannot bend, so it becomes a hook or deny rule, or the file has grown long enough to bury it, so the file gets shorter. More emphasis fixes neither.
- A preference stays advisory. A large enforced set means preferences have leaked into it; every hook fires wrongly sometimes and someone maintains it [A1].
- An enforced check speaks to the agent. Error messages that state the fix let the agent repair its own work [O1, not yet confirmed by a current source].

## The pillars

| Score | Meaning |
| --- | --- |
| 0 | Absent, or no verified evidence |
| 1 | Present, not yet runnable as a whole: a documented policy, script, or partly working mechanism, with some level-2 criterion unmet or unverified |
| 2 | Runnable: the pillar's Observable audit check is met on runnable evidence (see Evidence). Only pillar 6 requires a fresh checkout |
| 3 | Enforced and measured: it blocks the action it guards (a required check blocks merge; a hook blocks the tool call), and its results are tracked over at least 20 runs or 30 days |
| N/A | Does not apply to this repository; give a one-line reason |

Scoring rules:

- A pillar's score is the highest level whose criteria all verified evidence meets. An unverified check cannot lift a pillar to a level; list it under Unverified.
- Level 2 needs the pillar's Observable audit check, met on runnable evidence. Level 3 also needs that check to block its action and to be tracked over time, as defined above. Reference-file Audit check bullets diagnose the Top gap; they gate a level only where that reference says so.
- When a pillar covers several artifacts (files, skills, or review angles), score the weakest applicable artifact. A missing artifact that the Observable audit check needs keeps the pillar below level 2; it does not by itself score the pillar 0.
- Optional CI that fails loudly but does not block merge is level 2, not 3.
- Mark a pillar N/A when it does not apply, and leave it out of totals. When a pillar applies only in part, score the parts that apply and name the checks you dropped.
- In the Report, `Channel` describes the proposed fix, not the current state.

| # | Pillar | Job | Observable audit check |
| --- | --- | --- | --- |
| [1](references/pillar-1-code-shape.md) | Code shape: reuse, ownership, data flow, one pattern per job | Tell | Each decision in three recent features is made in one place; boundary and duplication tools pass |
| [2](references/pillar-2-static-gates.md) | Static gates: types, lint, dead code, complexity, duplication | Check | One command runs every static gate locally, and CI runs the same command; clean `main` is green; suppressions are counted |
| [3](references/pillar-3-test-gates.md) | Test gates with signal: layered, no duplicate or low-signal tests | Check | A single test file runs with one command; a sample of tests each maps to one contract and one credible regression |
| [4](references/pillar-4-documentation.md) | Documentation: a map, decisions, workflows, glossary | Tell | Every always-loaded line passes the two-question test or the decay test; every documented command runs |
| [5](references/pillar-5-review-gates.md) | Review gates chosen by risk | Check | Each review angle has a trigger, runs read-only in fresh context, and its findings are verified before they are fixed |
| [6](references/pillar-6-reproducible-environment.md) | Reproducible environment: one command, seeded, observable | Check | A fresh worktree, inside the agent's own sandbox, reaches a seeded, healthy, running app with one command; two worktrees run at once without collisions |
| [7](references/pillar-7-bounded-autonomy.md) | Bounded autonomy | Bound | Every "never" rule is a deny rule, hook, or sandbox limit; unattended runs have turn or spend caps and a named sign-off on the result |
| [8](references/pillar-8-guidance-evaluated.md) | Guidance is evaluated | Tell | Each instruction file or skill has evidence that it changes behavior against a no-guidance baseline |

Pillars 7 and 8 extend the original six. Both come from the same vendor
guidance: the pre-flight questions for unattended runs [A1] and
evaluation-first authoring [A4].

## Audit procedure

Pick every mode that applies; a repository that ships guidance needs both
"Existing repository" and "Engineering guidance". Then report.

### Evidence

Use the strongest evidence your authority allows, and name the kind in the
Evidence column:

1. A local run in a fresh checkout, inside the agent's sandbox.
2. CI results on the exact commit audited.
3. CI results on current `main`, labelled as a different commit.
4. Source inspection: the script exists and reads correctly. This supports level 1 at most for runnable checks.

For kind 1, record the sandbox configuration you ran under (host, sandbox
mode, notable deny rules), so a failure can be traced to the repository or to
the auditor's machine.

A failed fresh setup is scored once, in pillar 6. Other pillars can still reach
level 2 on kind 2 evidence, or on a local run with dependencies supplied
another way, labelled as such.

A read-only audit uses kinds 2 to 4 and lists the local runs it skipped.
Required checks, branch rules, and review history need read access to the
forge API (for example `gh api`). Without it, mark them unverified.

### New project

Gates are cheapest to add at zero lines of code.

1. Pillar 6: a one-command setup, run, and teardown with a seed script and a health check. Prove it inside the agent's sandbox.
2. Pillars 2 and 3: strict types, lint, dead-code and boundary tools, and a test runner with a single-file command, all behind one `check` command that CI also runs and requires.
3. Pillar 7: deny rules and sandbox limits for every "never" rule.
4. Pillar 4: a short `AGENTS.md` with the commands from steps 1 and 2. Add lines only after the agent has to be corrected twice [A1, O3].
5. Pillars 1 and 5 grow with the code: record each decision when it is made, and add review angles as risk appears.

### Existing repository

1. Time a fresh worktree to a seeded, running app inside the agent's sandbox. Record cold setup (from nothing) and warm setup (prerequisites already present) separately, with each manual step.
2. Run every gate on clean `main`. Record duration and failures.
3. Count suppressions by kind ([pillar 2](references/pillar-2-static-gates.md) says how).
4. Sample twenty tests and three recent features against pillars 1 and 3.
5. Mine recent human review findings, not replies to bots, for repeats. Treat each repeat as a hypothesis: a missing lint rule, test, or documented decision, or a wrong review. Verify it before you call it a gap.
6. Score every pillar.

### Engineering guidance (instruction files, skills, review gates)

1. Measure the always-loaded footprint as each host actually loads it, not only file sizes: instruction files, skill descriptions, and hook output. In Claude Code, `/context` shows what loaded [A1]. Where a host cannot show it, report file bytes and mark the loaded size unverified.
2. Classify each instruction (a sentence or bullet) as durable or decaying, and as advisory or enforced. An instruction can be mixed; say which part is which.
3. List every "always" or "never" rule that is advisory only. Each is a placement defect or a preference worded too strongly.
4. Find caches: lines that restate the directory layout, `package.json` scripts, or config. Keep the verification commands [A1] and lines whose lookup is expensive.
5. Find duplicated meanings across files.
6. Check review gates for a triage step and a counterweight to over-fixing (pillar 5).
7. Ask for evaluation evidence (pillar 8). Score evaluation results with the pillar 8 levels. Without results, a written evaluation policy scores 1 and no policy scores 0. The decay test in [maintenance.md](references/maintenance.md) works for any guidance, not only this skill.

## Report

Write an Evidence section, then this table, then Skill gaps (where this
skill was hard to apply) and Unverified (checks skipped, and what running
them needs).

| Pillar | Score | Evidence | Top gap | Fix | Channel |
| --- | --- | --- | --- | --- | --- |

Order fixes by blast radius first: any unenforced pillar 7 rule (secrets,
protected paths, irreversible actions) comes first, together with any defect
that can hide such a rule from the agent, such as instructions cut off by a
size limit. Then order by durability (6, 3, 2, 5, 1, 8, 4), then by cost.

## Sources

The current model generation is the Claude 5.5 family (with Fable 5.1) and
GPT-6.x (6.1 Sol, 6 Luna, 6 Astra). Vendor sources are primary unless marked
otherwise. In
the pillar references, the *Why* paragraphs cite sources. *Good looks like*
and *Audit check* are practitioner synthesis unless a source key appears. The
0–3 rubric, the fix order, and the durability ranking are this skill's
synthesis, not vendor guidance. A source marked *predates the current model generation* only
corroborates; a claim it alone supports needs a current source or the decay
test in [maintenance.md](references/maintenance.md).

- **[A1]** Anthropic, *Best practices for Claude Code*. <https://code.claude.com/docs/en/best-practices> Verified 2026-11-01.
- **[A2]** Anthropic Engineering, *Effective context engineering for AI agents*, 2025-09-29. Predates the current model generation. <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents> Verified 2026-11-01.
- **[A3]** Anthropic Engineering, *Effective harnesses for long-running agents*, 2025-11-26. Predates the current model generation. <https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents> Verified 2026-11-01.
- **[A4]** Anthropic, *Skill authoring best practices*. <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices> Verified 2026-11-01.
- **[A5]** Anthropic, *Claude Code skills: Run and verify your app*. <https://code.claude.com/docs/en/skills> Verified 2026-11-01.
- **[O1]** OpenAI (Ryan Lopopolo), *Harness engineering: leveraging Codex in an agent-first world*, February 2026. <https://openai.com/index/harness-engineering/>. Predates the current model generation. Verified 2026-11-03.
- **[O3]** OpenAI, *Codex best practices* (covers GPT-6.1 Sol, GPT-6 Luna, GPT-6 Astra). <https://learn.chatgpt.com/guides/best-practices> Verified 2026-11-01.
- **[O2]** OpenAI, *Codex: AGENTS.md*. <https://learn.chatgpt.com/docs/agent-configuration/agents-md> Verified 2026-11-01.
- **[S1]** Agentic AI Foundation (Linux Foundation), *AGENTS.md*. <https://agents.md/> Verified 2026-11-01.
- **[G1]** GitHub, *Customize the agent environment* (Copilot). <https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/customize-the-agent-environment> Verified 2026-11-01.
