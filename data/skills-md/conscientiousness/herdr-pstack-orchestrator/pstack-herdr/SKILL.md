---
name: pstack-herdr
description: "Run original pstack workflows through configured Herdr workers. Loaded by installed pstack workflow skills to map their tools and roles to Herdr; also usable as an explicit entry point."
---

# pstack-herdr

Installed workflow skills load this mapping before their original instructions. You can invoke `poteto-mode`, `how`, or `interrogate` directly. The bundle contains selected skills from Lauren Tan's original `cursor/plugins`, their resources, and both Herdr adapters. Read [herdr-tools.md](references/herdr-tools.md) and the companion [herdr-orchestrator skill](../herdr-orchestrator/SKILL.md) before starting. Installed herdr-core is the preferred backend and works headless. Only its absence selects legacy Herdr, which requires a controller pane. Core workers can have optional `hcOrch` viewer tabs in an existing Herdr UI; legacy worker tabs remain `horch`. Tasks keep their recorded backend. Core tasks also pin their endpoint; legacy tasks retain the one-server-per-store requirement. Native core status supplies readiness and ended-turn evidence; result files alone do not complete tasks.

This mapping takes precedence over upstream tool names, model defaults, configuration paths, and delegation instructions. User and project instructions retain precedence over both skills. Preserve bundled upstream instructions; report required compatibility changes separately.

## Enter a workflow

1. Use the sibling skills installed with this adapter. The [bundle provenance](references/bundle.json) records their reviewed source revision; a separate source checkout is unnecessary. If a required sibling is missing, report an incomplete installation and follow [bundle installation](references/compatibility.md#install). Do not fetch missing instructions from a different revision during a workflow.
2. Read the requested sibling `<name>/SKILL.md`, or [poteto-mode](../poteto-mode/SKILL.md) in full for a general goal, then its chosen playbook and required references. Read each applied principle's own file. Resolve relative links from their owning file. Use this installed bundle consistently rather than another same-named skill.
3. Keep planning, guidance, task assignment, and quality control in this controller. Expand exploration, design, implementation, and review phases here, then delegate their substantial execution through `horch`. Follow the companion skill's context and waiting rules: keep concise decisions and evidence pointers in the main thread, and reuse an unbounded wait process when the harness supports it. Put this task-specific rule in every worker brief: **Do not delegate, use native subagents, or run a whole playbook. Complete this assignment yourself; report any need for further delegation to the controller.** This overrides the companion skill's general permission for worker subagents.

The bundle's workflow entries load this mapping automatically; pure guidance keeps its original body. Cursor custom modes and hooks are not installed. Runtime verification is separate from discovery and source compatibility.

## Repository and host boundaries

State the exact repositories, hosts, local worktrees and evidence sources authorized for the task in every delegate brief. These boundaries apply to all investigators, synthesizers, implementers and reviewers. Broad-search instructions in an upstream prompt apply only inside that explicit boundary. An empty or thin result never authorizes an owner-wide, global, cross-repository or cross-host search. Record a broader linked lead without fetching it; ask the controller to resolve whether the user authorized that scope.

When a workflow uses a controller-captured repository snapshot, disclose its repository, capture time, completeness and unavailable categories. Delegates query only that local dataset; snapshot investigation is not live worker forge access or proof that the original live-source workflow was completed. Keep a real investigator for an available source even when its captured result is empty.

A native-command audit after a worker finishes can gate whether its output is read or forwarded. Audit failed calls as well as successful ones, quarantine outputs when the boundary is violated, and stop before synthesis. Such a gate detects workflow violations after execution. It does not prevent the worker from using credentials or making requests, and is not a hard sandbox or credential-containment claim.

## Resolve roles

On Claude Code, Codex, and Pi, read `$XDG_CONFIG_HOME/herdr-orchestrator/workers.toml`, or `~/.config/herdr-orchestrator/workers.toml` when `XDG_CONFIG_HOME` is unset. Its `[roles]` values name workers from `[workers]`. This is the only role configuration. Upstream `setup-pstack` maps to the companion skill's setup and these TOML roles; do not create a separate model sheet or import one.

Keep upstream role names. A single role names one worker, which may handle several fresh tasks. Panels (`interrogate reviewers`, `arena runners`, `architect runners`) are lists with one fresh task per entry, including repeated worker names. `arena cross-judge pool` is also a list, but the controller selects one entry as the skill directs. Configure only roles needed by the selected workflow. Roles may share one worker and model; additional providers or models are optional.

For Arena's cross-judge, select only a configured pool worker from a different model family than the controller. Never use a same-family judge. When no eligible configured worker can run, skip the judge and disclose it as Arena permits; do not substitute an unconfigured model or change worker definitions. If the controller's model is unknown, follow Arena's unknown-family procedure with configured pool entries and disclose that the family check did not run.

Use each worker's configured harness, model, and effort. If a needed role or worker is missing, invalid, or names `auto` or `inherit-parent`, complete setup with the user before dispatch. Never substitute upstream model defaults or native subagents.

Classify the assignment before selecting a worker, including tasks outside a named playbook. Use an applicable configured role first: source mapping fits `how explorer`, root-cause investigation fits `why investigators`, and implementation fits `feature, refactoring`. Using a role does not require running that role's whole playbook. If no configured role fits, select a configured worker using its optional `description` and the assignment's requirements. Worker names are user-defined; never assume a particular name or model family exists. A description explains intended use, not measured capability, price, or a routing override.

Every brief names the matched role (or says no role fits), selected worker, and one concrete reason. If a seemingly related role does not fit, name the task-specific constraint; a generic claim that the work needs judgment is insufficient. When a role applies, use its configured worker or panel. Descriptions and controller model preferences do not authorize replacing that assignment. Do not add automatic retries or model fallbacks.

For formal `interrogate` review, run the entire configured reviewer panel; do not relabel it as an ad-hoc task to omit reviewers. A bounded evidence audit may use one worker and must be reported as that limited audit. Same-model reviewers still use separate processes and independent briefs, but do not provide cross-model validation. If the upstream workflow requires a larger or more diverse panel than configured, disclose that gap and do not claim full workflow compliance; it does not block unrelated work or a clearly identified limited review.

On setup, ask which configured workers should fill each role. For example:

```toml
[roles]
"feature, refactoring" = "glm"
"interrogate reviewers" = ["ds", "haiku"]
```

For a single configured worker named `solo`, these roles can instead use `"solo"` and `["solo", "solo"]`. Each review entry starts a separate process; this provides two review tasks, not two models.

## Review loop

An Interrogate-only request ends with its verified findings and dropped counts; do not apply fixes. The implementation and fix steps below apply only when the user has already authorized delivery of a change.

1. State the intended behavior and create a git worktree for the implementing worker. Give it a complete brief, including the base revision, scope, constraints, verification, and output files. Dispatch the configured implementation worker with `horch run <worker> --cwd <worktree> --brief <file>`. Wait for a valid result, inspect its files and diff, and verify the changed behavior.
2. Read the sibling `interrogate/SKILL.md` and its required Arena phases. State the intent, base revision, target head, and any uncommitted changes in scope. Capture that exact state before dispatch. Create a separate worktree for every `interrogate reviewers` worker and copy the in-scope uncommitted changes into each, including relevant untracked files. Give every adversary the same scope, intent, and source brief. Allow scoped repro and test artifacts only in its own worktree; forbid product fixes, delivery-branch edits, and unauthorized external writes. Start all tasks with separate `horch run` calls before waiting, subject to the configured worker limit. These adversaries need writable worktrees, so do not mark their whole assignments read-only.
3. Wait until `horch wait` reports `state: "done"` for every adversary. A report already on disk does not finish a `running` task; keep waiting, and never close an unfinished reviewer to pass the gate. Read each `result.json` and listed report. Rerun each finding's exact command against the captured target in an isolated worktree. Keep only a reproduced failure that breaks the stated intent, merge duplicate root causes, and report dropped counts and reasons. Skip Arena's judging and candidate-selection phases as Interrogate directs. A completed task or an unrun concern is not a verified finding.
4. If a finding needs a fix, start a fresh implementation worker on the same branch after the prior writer has finished. Include the original goal, all accepted findings, prior reports, and current revision in its brief. Verify its result and changed behavior. Run the reviewer panel again on the new revision; do not reuse a reviewer session.
5. Finish when the independent review has no unresolved blocking finding. Report the final revision, verification, reviewer outcomes, and any remaining concerns. If a worker reports a problem, follow `herdr-orchestrator` problem handling and keep the review gate open.

Writers must never work concurrently in the same worktree. Interrogate adversaries each need their own worktree for repros; other reviewers may share a checkout only when their briefs are read-only. Every `horch run` starts a fresh process, including each fix and second review. These are instruction boundaries, not an enforced sandbox.
