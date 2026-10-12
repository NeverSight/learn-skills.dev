---
name: setup-pstack
description: Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes ~/.config/pstack/pstack-models.md, which overrides the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack

Write `~/.config/pstack/pstack-models.md`, the file that sets pstack's model per role. Skills read it when they delegate.

## Steps

### 1. Detect available models

Call `orchestrator_capabilities` and keep the providers whose `canRunChildTask` is true. Their models are what you can pass to a `delegate_task` subagent in this session. That is the only source. If it returns no eligible model, say so and offer `inherit-parent` for every role. An entry is `<providerInstanceId>/<model>`, plus `(<effort>)` when the model lists an effort option (`effort` on Claude, `reasoningEffort` on Codex). Never write an entry it did not return. The aliases `inherit-parent` and `auto` are always valid even though they are not detected models.

### 2. Load current state

The default role-to-model mapping is the rule in step 3(b), over the roles shown in step 5. If `~/.config/pstack/pstack-models.md` already exists, read it and treat its `# budget` line and its role values as the current choices. Otherwise start from those defaults. A line whose role is not in step 5, such as `how critics`, is from a retired role. Drop it.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Ask plainly in the thread. Offer these four options with these exact labels, and name the current budget when the file records one.

- `unlimited - max reasoning`
- `large - xhigh reasoning`
- `medium - high reasoning`
- `small - medium reasoning`

**(b) Apply it.** Build the working table from the skill defaults, and on a re-run keep any role you changed by model, list, or alias (`inherit-parent`, `auto`). By default, code roles (`feature, refactoring`, `bug-fix`, `perf-issue`, `hillclimb`) and the `how explorer`, `why investigators`, `swarm workers`, and `reflect tooling` roles get the fastest strong coding model detected. `judgment and prose`, `hardest tasks`, `how explainer`, `why synthesizer`, and `reflect judgment, divergent, synthesizer` get the most capable model detected. Each panel role (`arena runners`, `arena cross-judge pool`, `architect runners`, `interrogate reviewers`) gets the most capable model of each distinct provider detected, up to three entries. `unlimited`, `large`, `medium`, and `small` set the effort of every real entry, panel entries included, to `max`, `xhigh`, `high`, or `medium`, on the ladder `max` > `xhigh` > `high` > `medium` > `low`. If the model does not list the target, use the highest ladder option at or below it that the model lists, else mark the role as needing a choice. Never pick an option off the ladder, such as `ultra`, `ultracode`, or `ultrathink`. A model with no effort option gets no `(<effort>)`. `inherit-parent` and `auto` do not change. So under `large`, a model that lists `low`, `medium`, `high`, and `max` gets `high`.

**(c) Show the roles and confirm.** Show every role with its model, marking any real entry not in the detected set as needing a choice. Also list each line step 2 dropped. Ask whether to accept as-is or change specific roles, offering the detected models plus `inherit-parent` and `auto` (both mean: this role runs on the parent thread's model) as the options. Ask plainly in the thread. For panel roles (arena runners, architect runners, interrogate reviewers) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one value from it whose model family differs from the parent's when possible. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

### 4. Validate

Every real entry written must be in the `orchestrator_capabilities` result. Its provider has `canRunChildTask` true, its model is listed under that provider, and its effort, when it has one, is one of that model's effort options. A model with no effort option has no `(<effort>)`. `inherit-parent` and `auto` always pass. If a chosen real entry is not available, stop and ask again.

### 5. Write the file

Write `~/.config/pstack/pstack-models.md` (create `~/.config/pstack/` if it is missing) as a plain file with the header comments, a `# budget` line with the chosen label and its target effort, and one line per role, using the same labels poteto-mode uses. Overwrite the whole file so re-runs stay idempotent. Shape:

```
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit-parent` or `auto` as a value: the role runs on the parent thread's model (omit delegate_task `target`). Alias entries in a panel list still count toward its fan-out.
# budget: large (xhigh)
feature, refactoring: <providerInstanceId>/<model> (<effort>)
bug-fix: <entry>
perf-issue: <entry>
hillclimb: <entry>
judgment and prose: <entry>
hardest tasks: <entry>
how explorer: <entry>
how explainer: <entry>
why investigators: <entry>
why synthesizer: <entry>
reflect tooling: <entry>
reflect judgment, divergent, synthesizer: <entry>
arena runners: <entry>, <entry>, <entry>
arena cross-judge pool: <entry>, <entry>, <entry>
swarm workers: <entry>
architect runners: <entry>, <entry>, <entry>
interrogate reviewers: <entry>, <entry>, <entry>
```

### 6. Confirm

Tell the user the file was written and that it applies the next time a skill delegates, since skills read it then. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, read `../create-verification-skill/SKILL.md` from this skill's directory (the one your harness gave when it loaded this file, else `~/.claude/skills/setup-pstack/` on Claude Code and `~/.agents/skills/setup-pstack/` on Codex) and follow it. On no, move on without pushing.
