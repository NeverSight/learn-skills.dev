---
name: dayz-review
description: Meticulous three-axis review of a DayZ change — standards, runtime, and spec.
when_to_use: When the user asks for a review of a DayZ change.
disable-model-invocation: true
---

Three-axis review of a DayZ mod change:

- **Standards** — does the code read like this project's code? Naming, structure, formatting, documented conventions.
- **Runtime** — will it behave in the game? Engine failure modes from the catalogues.
- **Spec** — does it do what was asked?

Each axis runs as its own **sub-agent, all three in parallel**, so they cannot pollute each other's context or each other's judgement. This skill pins the scope, briefs them, and aggregates.

## Process

### 1. Pin the scope

Take the scope from what the user said. Three forms:

| They said | Scope |
|-----------|-------|
| nothing, or "review the changes" | **Staged** — `git diff --staged`. If nothing is staged, fall back to `git diff HEAD` and say so in the report. |
| a commit, branch, tag, `main`, `HEAD~5` | **Since a fixed point** — `git diff <point>...HEAD` (three-dot, against the merge-base), plus `git log <point>..HEAD --oneline` for the commit list. |
| "review the project", "audit the codebase" | **Project** — glob the source files (`**/*.c`, `**/*.layout`, `**/*.styles`, `**/*.imageset`, `config.cpp`) instead of a diff. |

Before going further, confirm the scope produces something: the ref resolves (`git rev-parse <point>`) and the diff is non-empty. A bad ref or an empty diff fails here — not inside three parallel sub-agents. State the scope you used at the top of the report so the user can correct you.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`). If the repo has `docs/agents/issue-tracker.md`, fetch them the way it describes.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. Ask the user where it is. If they say there isn't one, skip the **Spec** sub-agent and say so in the report.

### 3. Identify the standards sources

The project's documented contract is the `dayz-scripting` and `dayz-ui` skills — conventions, invariants, and their reference files. On top of those, collect whatever the repo documents for itself: `CLAUDE.md`, `AGENTS.md`, `CONTEXT.md`, `CONTRIBUTING.md`.

### 4. The engine baseline

The **Runtime** axis reviews against the catalogued DayZ failure modes. Those catalogues are not written out here — they live in the skills that own them, where the people writing the code read them too:

| Invoke this skill | Then read, inside it | Covers |
|---|---|---|
| `dayz-scripting` | `reference/engine-pitfalls.md` | segfaults, compiler quirks, `delete` on entities, load-time `IsClient`/`IsServer`, slow engine APIs, trusting client data, paths that die in the PBO |
| `dayz-ui` | `reference/ui-pitfalls.md` | unpaired acquisitions, missing `Unlink`, wrong call category, unremoved repeating callbacks, unchecked `FindAnyWidget`, unregistered styles and imagesets |
| `dayz-scripting` | `reference/modded-classes.md` | broken `super` chains, load-order assumptions on modded constants |
| `dayz-scripting` | `reference/code-style.md` | localization — user-facing strings behind `#STR_` keys |

The wire has a catalogue of its own, kept in this skill because only this review reads it — `reference/network-pitfalls.md` beside this file: oversize repeating messages, identity strings on streams, events on non-guaranteed sends, unmasked packed fields, broadcasts, whole-collection answers, entity state sent by RPC, RPCs sent before the other side is ready. It applies when the scope sends or reads anything over the wire: `ScriptRPC`, `OnRPC`, `RPCSingleParam`, a packet codec, net-synced variables.

Two rules bind the baseline:

- **The project overrides.** A documented project convention wins; where it endorses something a catalogue would flag, suppress it.
- **Name the symptom.** Every catalogue entry is a concrete failure with a stated symptom, not a heuristic. A finding gives the symptom and the path that reaches it, or it is not a finding.

### 5. Spawn the three sub-agents in parallel

Every brief carries these **house rules** verbatim:

> Read each file in scope end to end before judging it — a hunk out of context is how false findings are made. One root cause, one finding: three symptoms of the same bug are a single entry listing three symptoms. Where code looks strange but works, find out why before flagging it — it may be a deliberate workaround for engine behaviour. Report, do not fix, and stay inside the pinned scope. Be meticulous, not noisy: every real problem, and nothing added to fill space.

**Standards sub-agent** — include:

- The scope command from step 1 and the commit list.
- The list of repo standards files found in step 3.
- The brief: "Your first two actions are to call the Skill tool twice, for `dayz-scripting` and `dayz-ui` — together they are the contract you review against. Judge **how the code reads**: naming, structure, braces and formatting, comment discipline, casting form, collection idiom, and any repo standards file listed above. Cite the rule you are applying. Engine failure modes — leaks, unpaired acquisitions, client trust, packed paths — belong to the Runtime axis; leave them alone even where you spot them. Invent no conventions: where a rule is not written down, it is not a finding on this axis. Distinguish a breach of a stated rule from a judgement call, and skip anything a compiler or formatter already catches. Under 400 words."

**Runtime sub-agent** — include:

- The scope command and commit list.
- The catalogue table from step 4, and the two binding rules under it.
- When the scope touches the wire, the absolute path of this skill's `reference/network-pitfalls.md`.
- The brief: "Your first two actions are to call the Skill tool twice, for `dayz-scripting` and `dayz-ui`, then read the four catalogue files named in the table, and the network catalogue if this brief gives its path — they are your baseline. Report every catalogued failure mode the change reaches, and any other way this code misbehaves at run time. Name the entry, quote the hunk, and give the symptom and the path that reaches it. Where you need to confirm what an engine symbol actually does, call the Skill tool with `dayz-lookup` rather than assuming. Under 400 words."

**Spec sub-agent** — include:

- The scope command and commit list.
- The path or fetched contents of the spec.
- The brief: "Report (a) requirements the spec asked for that are missing or partial; (b) behaviour in the change nobody asked for — scope creep; (c) requirements that look implemented but are implemented wrongly. Quote the spec line behind each finding. Under 400 words."

### 6. Aggregate

Present the three reports under `## Standards`, `## Runtime`, and `## Spec`, verbatim or lightly cleaned. Do **not** merge or rerank across axes — the separation is the point (see *Why three axes*).

Format each finding as:

- **`path/to/file.c:42`** — one sentence on what is wrong.
- **Why it matters** — the consequence. Required on Standards and Runtime findings.
- **Fix** — the minimal snippet that corrects it, without rewriting the surrounding code.

Close with:

- One line per axis: how many findings, and the worst one within that axis. No single winner across axes — that is the reranking the separation exists to prevent.
- A verdict: can this be committed as it stands, or is something blocking.
- Where one error pattern recurs across findings, recommend adding it to `dayz-scripting`, `dayz-ui`, or this skill's network catalogue. Those are the only memory this review has.

## Why three axes

A change can pass on one axis and fail on another, and each axis is blind to the others' failures:

- Follows every convention and implements the wrong feature — **Standards pass, Spec fail.**
- Does exactly what the issue asked, in code that breaks the project's conventions — **Spec pass, Standards fail.**
- Conventional and exactly on spec, and it deadlocks the player's input on close — **Standards and Spec pass, Runtime fail.**

That third case is why DayZ gets an axis the usual two-axis review does not have. Compilation proves nothing here: the engine accepts unpaired acquisitions, dropped `modded` inheritance, and unregistered resources without a word, and the failure only shows up in game. Reporting the axes separately stops a clean one from masking a broken one.
