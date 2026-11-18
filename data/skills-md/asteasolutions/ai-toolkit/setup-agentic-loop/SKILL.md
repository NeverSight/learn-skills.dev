---
name: setup-agentic-loop
description: Install the /agentic-loop delegated build loop into this repo — orchestrator, implementer, and an independent reviewer that runs in its own context — fitted to the repo's existing layout.
disable-model-invocation: true
---

# Setup — install the `/agentic-loop` build loop

Install a delegated build loop whose code is written by one agent and judged by another in a **fresh context**. The developer approves a spec once, up front; implementation, verification, and review then run without them.

Works under **Claude Code, GitHub Copilot in VS Code, and Cursor** — all three run skills and delegate to sub-agents. One body per agent, translated per harness: see [`references/harnesses.md`](references/harnesses.md).

> **This skill fits the repo; it does not wire it.** Detect where this repo already keeps agents and skills and place the scaffolding there. Creating shared-instruction files or harness projection config is out of scope — this skill installs a loop, not a repo layout. The one editor setting it offers to write is the one the loop cannot run without.

> **Prompt-driven, not a script.** Detect, ask, preview, confirm, write, verify.

## What lands

| Artifact | Role |
|---|---|
| `agentic-loop` skill | The **front gate**: spec + slices, approved in the developer's conversation, then handed off |
| `orchestrator` agent | Runs slices unattended: implement → verify → review → bounded fix rounds → report |
| `implementer` agent | Writes one slice against its clauses |
| `reviewer` agent | Read-only judge in a fresh context; writes findings, returns a **verdict** |
| `security-reviewer` agent | Bundled specialist: trust-boundary changes — untrusted input, authz, secrets, dependencies |
| `architecture-reviewer` agent | Bundled specialist: structural change no clause of the spec asked for |
| `<surface>-reviewer` agents | Optional repo-specific specialists (migrations, API contracts, infrastructure) |

Every specialist is **dispatched by trigger**, never on every slice — a slice that adds no structure never pays for an architecture review.

These are common names. A repo that already has an agent or skill by one of them gets a keep-or-replace decision in step 3, never a silent overwrite.

## Process

### 1. Detect harnesses and placement

Which harnesses this repo uses decides where everything lands — resolve that first, from [`references/harnesses.md`](references/harnesses.md). A repo can use more than one, and then it gets one copy per harness. Then follow [`references/detection.md`](references/detection.md) for the rest: work dir, verify command, diff scope, triggers.

**Criterion:** every harness in use is named and its destinations resolved; every row of the detection table has a value that is either evidenced by a path in this repo or came from the developer.

### 2. Ask what cannot be detected

One question at a time, each with your recommended answer:

1. **Verify command** — only if detection found none. If the developer has no single command, record that and continue; the loop then reports that machine verification was unavailable rather than implying tests passed.
2. **Nested delegation under Copilot** — only where Copilot is a harness in use. Offer the workspace setting in [`references/harnesses.md`](references/harnesses.md) and recommend yes: without it the orchestrator cannot delegate at all. Give the developer both the cost and the decline path that file states.
3. **Commit policy** — commit each passing slice on a branch, or leave everything in the working tree. Repos with signed commits, hooks, or message conventions often want the second.
4. **Bundled specialists** — offer `security-reviewer` and `architecture-reviewer`, each with the triggers you resolved for this repo. Recommend `security-reviewer` wherever the repo handles input it does not control; recommend `architecture-reviewer` wherever the repo has boundaries worth defending. Say what each will cost: a triggered specialist is another review pass on that slice.
5. **Repo-specific specialists** — propose any further surfaces under the evidence rule in `references/detection.md`, and take a separate yes/no for each. Propose none if nothing warrants it.

**Criterion:** every specialist accepted or declined individually; no repo-specific proposal lacks an evidence path; the settings write was offered wherever Copilot is in use; no answer was assumed on the developer's behalf.

### 3. Preview and confirm

Show every file, its destination, and the resolved placeholder values, grouped by harness when there is more than one. Say which read-only constraints the harness **enforces** and which it only **states in the prompt** — a trusted constraint presented as an enforced one is the kind of thing a developer only discovers after a reviewer edits something. A destination that already holds a same-named file is a **keep-or-replace decision for the developer** — never a silent overwrite.

**Criterion:** developer has approved the full file list, per harness.

### 4. Write

Write the loop skill and every accepted agent into each harness's homes, translating the **wrapper** — filename and frontmatter both — per [`references/harnesses.md`](references/harnesses.md). An agent under Copilot is `<name>.agent.md` carrying Copilot tool ids, not the `<name>.md` and `Bash(git diff:*)` the template ships with. **The body is copied verbatim, never rewritten per harness** — a forked prompt drifts, and the drift shows up as a review that passes in one editor and fails in another.

Substitute placeholders:

| Placeholder | Value |
|---|---|
| `{{VERIFY_COMMAND}}` | the repo's verify command, or `none` |
| `{{WORK_DIR}}` | where specs and findings live — always a `.scratch/` path inside the repo |
| `{{COMMIT_MODE}}` | `commit-per-slice` or `no-commits` |
| `{{SPECIALISTS}}` | accepted specialists as `name — trigger`, or `none` |
| `{{SURFACE}}`, `{{GLOBS}}`, `{{FOCUS}}` | per specialist, in its own file |

The `orchestrator` agent is the **single home** for the resolved configuration — it is the agent that runs the command, matches the globs, and applies the commit mode. Do not restate those values in the `agentic-loop` skill. The one thing that may also go elsewhere: when the repo keeps a shared instruction file whose commands section lacks the verify command, append it there too, because it is a project fact that serves every agent in the repo.

Then make sure `.scratch/` is gitignored, as `references/detection.md` describes, and write the Copilot delegation setting if it was accepted — merged into `.vscode/settings.json`, never replacing it.

**Criterion:** no `{{` remains in any written file; every file carries its harness's own filename and tool vocabulary; the work dir is a `.scratch/` path inside the repo and is either ignored by git or deliberately not; under Copilot, nested delegation is either enabled in the repo or the developer knows it is theirs to enable.

### 5. Verify

If the repo already generates one harness's agent files from another's, run that tooling instead of hand-writing the second copy, and report what it required — an orchestrator that delegates to sub-agents is the kind of capability such tooling tends to ask about, and its questions go to the developer, never answered for them.

Check each installed harness against the delegation caps in [`references/harnesses.md`](references/harnesses.md); Copilot's is settled in step 2. A harness capped below the loop's two layers cannot run it, and that is worth saying now rather than at the first halt.

Close with the smoke test, in these words: run `/agentic-loop` on a trivially small goal and confirm two things — the reviewer's verdict reaches the report, and a deliberately failing verify command actually blocks the slice.

**Criterion:** every installed harness has had its delegation cap checked, the developer has been given the smoke test, and any regeneration either succeeded or its absence was reported.

## Re-runs

Re-runnable and converging. Re-detect placement each time — the repo may have gained a layout since the last run. Hand-tuned agent prompts are the expected customization, so a same-named file always goes back through the keep-or-replace decision in step 3.
