---
name: setup-pstack
description: Check installed pstack personas, optionally register native agents, configure which models pstack uses per role and at what reasoning budget, and set up a repository PR template. Use for /setup-pstack, "configure pstack models", "pstack budget", "set up pstack PR templates", or changing pstack's model choices.
---

# Setup pstack

For a request scoped to PR templates, run step 0e only. A full setup runs all applicable steps below.

Write the pstack models config, a file that sets pstack's model and reasoning effort per role. Agents resolve it per role with this skill's resolver. A workspace `.agents/pstack-models.md` sits over the user's `~/.agents/pstack-models.md`, a harness section beats a flat line in either file, and a role neither file names falls back to the shipped default in `examples/pstack-models.md`. So this is an override layer, not a requirement.

The inline defaults are written as short model aliases (`fable`, `opus`, `sonnet`, `haiku`), which translate to gpt-6 models on Codex and to `grok-4.7` on Grok Build. Any other value your harness does not accept for subagents means `inherit-parent`: the role runs on the session model, and multi-model panels become same-model panels. An entry may pin a reasoning effort as `model@effort`, and `## codex`, `## claude-code`, `## grok`, or `## hermes` sections hold lines that apply to one harness only. The grammar, layering, and effort policy are defined once, in [references/models-config.md](references/models-config.md), and `scripts/check-models-config.py --resolve` applies them.

## Steps

### 0a. Check personas and optional native registration

Read the **pstack-harness** skill's [registration reference](../pstack-harness/references/registration.md). Resolve its logical installed skills root through [portable-paths.md](../pstack-harness/references/portable-paths.md), then run:

```sh
python3 "${PSTACK_SKILLS_ROOT:?}/pstack-harness/scripts/subagents.py" check
```

Failure signal: nonzero exit. Repair missing payloads or sibling skills before reporting persona readiness. A ready payload lets a generic delegate receive the full persona without native registration.

That check covers payloads only, and it reports every native file as `not-requested`. Where personas or effort agents are already registered, also run the registration reference's native `check` for each CLI and scope that holds a `poteto-agent`, `comment-sicko`, or `pstack-effort-<level>` file: `~/.claude/agents`, `~/.codex/agents`, or the project's `.claude/agents` or `.codex/agents`. Offer the reference's `install` for that CLI and scope when a row reports `outdated-generated`. When another row in its group reports `conflict`, report the conflict instead, because install writes nothing in that group. The personas form one group and the effort agents another, so a conflict in one does not block the other. A skills update does not refresh registered personas or effort agents.

Offer native registration for Claude Code or Codex when the user wants it. Use the already-authorized scope if the session provides one; otherwise ask for project or user scope once. Recommend the project scope, alone or with the user scope, when the user runs Codex through a wrapper that gives it its own `CODEX_HOME`, per the registration reference. Run the reference's `install` command with the chosen absolute root. Never overwrite a conflict or change model settings to register a persona. For Hermes, use the full briefing through delegation context; do not create native agent files. Grok Build has no registration of its own. It loads the Claude Code wrappers, but its spawn tool cannot name an agent type, so its delegates get the full briefing in the prompt.

For Claude Code, say what registration adds: the two personas and the five `pstack-effort-<level>` agents, which let a written `@effort` apply to subagents here. Before a Claude Code install, read both config layers as step 2 does and list every role whose effort is written for this harness, with that effort. Say those roles run at it once the agents load, and every other role keeps the session effort. Report the `roles` rows and the `efforts` rows separately from live loading. When the install report says `agents_directory: created`, the agents load only in a fresh session, so tell the user to start one. Otherwise a running session picks them up, unless it was started with `--disable-slash-commands` or the directory came from `--add-dir`. In every case check the live catalog before claiming an effort applies.

Report payload readiness, native-file status, and live agent loading separately. Check the requested destination and inspect the live agent catalog before claiming native availability. Filesystem output always leaves activation unverified. Codex project registrations require project trust. Do not edit trust settings automatically. Check a fresh session after registration changes; when a loader requires a restart, say so and use full-brief delegation until loading is confirmed. Keep these observations separate from the model choices below.

### 0b. Check the structured task tools

poteto-mode keeps its worklist in the harness's structured task tool when that tool is on. Whichever CLI runs this skill, check both switches below and report each as on or off. A change applies from the next session. Edit a file only after the user says yes. Then add the key to the existing file and keep every other key.

- **Claude Code** has the task tools on every model when `CLAUDE_CODE_ENABLE_TODO_TOOLS` is `1` in the environment or in the `env` block of `~/.claude/settings.json`, `.claude/settings.json`, or `.claude/settings.local.json`, or when a launch names one of the task tools in `--allowedTools`. When the switch is off, recommend `"env": {"CLAUDE_CODE_ENABLE_TODO_TOOLS": "1"}` in `~/.claude/settings.json` for every project or in `.claude/settings.local.json` for this one, and say that a `settings.local.json` created by hand needs a `.gitignore` line. Also say that with tool search on, the default, the task tools arrive deferred, and Sonnet then kept no worklist in 4 of 4 `/poteto-mode` runs against one task per playbook step in 2 of 2 runs with `ENABLE_TOOL_SEARCH=false`. That setting raised a trivial first turn from 25,770 to 45,907 input tokens on 2.1.284 in 2026-09, so leave the choice to the user.
- **Codex** has the plan tool when `config.toml` under `$CODEX_HOME` or `~/.codex/` holds `[tools.update_plan]` followed by `enabled = true`. Codex's published config reference omits the key, and its shipped `codex-rs/core/config.schema.json` defines it with `enabled` defaulting to false, as of 0.158.0-alpha.2.1. When the switch is off, recommend those two lines. Codex rejects a bare `update_plan = true`.
- **Hermes** has no known switch. Report nothing to change.
- **Grok Build** ships its `todo_write` tool with no known switch. Report nothing to change.

### 0c. Check the Claude Code skill listing

Run this check whenever the user runs pstack on Claude Code. Codex keeps some pstack skills from implicit invocation through `agents/openai.yaml`, and Claude Code ignores that file. Without an override those skills list with their full descriptions and load from them. With `"skillOverrides": {"<skill>": "name-only"}` in `~/.claude/settings.json`, Claude Code lists each by bare name. The skill then loads when the user types `/name` or a pstack skill tells the agent to use it, and never from its description.

Resolve the installed skills root as step 0a does, then run:

```sh
python3 "${PSTACK_SKILLS_ROOT:?}/setup-pstack/scripts/skill-listing.py" check
```

Failure signal: exit 2. The settings file is unreadable or malformed, or the skills root is wrong. Report the stderr line and leave the file alone. Exit 1 means the listing is stale, and the JSON on stdout names the skills in `missing` and `extra`. Exit 0 means it is current. Report any `kept_off` skills as the user's own `off` choice, and say that a pstack skill that names one cannot load it. The check reads only the user file. When the project's `.claude/settings.json` or `.claude/settings.local.json` holds a `skillOverrides` entry for a pstack skill, report that entry too, because a project entry can override the user file.

When the listing is stale, offer `install` and say what it changes. Run the same command with `install` in place of `check` only after the user says yes. It sets `name-only` for each missing skill, replacing an `on` or `user-invocable-only` value. It deletes a `name-only` entry for any pstack skill outside the set, even one the user wrote. It keeps every other key and the user's `off` entries, and it touches only pstack's own skills, so entries for other suites' skills stay as they are. Report `added`, `removed`, and the final `state`, and say the change applies from the next session.

### 0d. Check Codex subagents

On Codex, pstack spawns roles natively through `spawn_agent`. When the tool is unavailable, the **pstack-harness** skill falls back to `codex exec` subprocesses, or to arms run one at a time inline, and an inline review is not independent. Run this check when this skill runs on Codex or the user also runs pstack there.

Whether a session has `spawn_agent` depends on more than config. As of Codex 0.160.0 it also depends on the selected model's own multi-agent setting, launch flags, spawn depth, and config layers this skill cannot read. So config can only show signals, and only a Codex session shows the answer.

- **Inside a Codex session**, the answer is whether `spawn_agent` is callable. When the session defers tools behind a tool search, search for it before calling it missing. If it is missing, list the causes you cannot rule out:
  - a config key
  - a `-c` flag the session started with
  - the selected model
  - spawn depth
  - a config layer you cannot read

  Do not pick one without evidence.
- **The config signals.** Run `codex features list` from the project root, in the environment the user starts Codex in, including any wrapper's `CODEX_HOME`, and report the `multi_agent` and `multi_agent_v2` rows. Then read `[agents]` `enabled` from `config.toml` under `$CODEX_HOME` or `~/.codex/`, and from the project's `.codex/config.toml` when the project is trusted, because `codex features list` does not report it. Report these as signals, not as a verdict on spawning.
- **When `codex` is not on PATH**, as when this skill runs from another CLI or from an app-bundled Codex, report the config signals as unverified. A live session's answer still stands.

A key in a file you read is a possible cause, not a proven one, because `multi_agent_v2` or a layer you cannot read can override it. Offer an edit only when a Codex session confirms `spawn_agent` is missing, and only for a possible cause a config file shows:

- `[agents]` `enabled = false` in a file you read, while the `multi_agent_v2` row reads `false` and no readable file of higher precedence sets it `true` (a trusted project's file beats the user's): offer to delete that line or set it to `true`. When a readable layer overrides it, or the rows are unverified, report the key as unverified and offer nothing. On Codex 0.160.0 this key removes `spawn_agent` even while the `multi_agent` row reads `true`. With `multi_agent_v2` on, the key does not block spawning, so offer nothing for it.
- Both feature rows read `false` and a file you read turns the feature off, as `[features]` `multi_agent = false`, a dotted `features.multi_agent = false`, or the legacy `[features]` `collab = false`: offer to set it to `true` in that file. With the key in the user config, `codex features enable multi_agent` fixes any of the three. When no file you read turns it off, the cause is a layer you cannot read, so name that instead of offering an edit.

```toml
[features]
multi_agent = true
```

Edit a file only after the user says yes, and keep every other key. The change applies from the next session. Without a session to confirm, report the signals and any possible causes, say spawning is unverified, and offer no edit.

### 0e. Set up the repository PR template

For a full setup in a Git repository, follow [references/pr-template.md](references/pr-template.md). Preserve existing repository templates and explicit choices. When none exists, install the bundled poteto template and, when no-mistakes is configured, select it through `pr.template`. Report the files changed and whether trusted-default-branch activation is pending. Skip this step outside a repository or when the request only changes models, budgets, or host settings.

### 1. Detect available models and efforts

Enumerate the model values your session's spawn mechanism accepts, and the reasoning-effort values it accepts per spawn (use the **pstack-harness** skill to find the mechanism). On Claude Code, the per-spawn efforts are the levels whose `pstack-effort-<level>` agent the live catalog lists, and none when no effort agent is loaded. That is the dependable source. If your CLI also exposes a models API or command that lists the user's entitled models, such as `codex debug models` or `grok models`, prefer it for completeness. If you cannot detect any, ask the user to paste the slugs they have access to. Never write a real slug you have not confirmed is available. The aliases `inherit-parent` and `auto` are always valid even though they are not detected slugs.

### 2. Load current state

The default mapping is `examples/pstack-models.md` next to this skill. Read both config layers when they exist, the workspace `.agents/pstack-models.md` and then `~/.agents/pstack-models.md`, including their harness sections, and treat each role's lines and the `# budget` line of the file being configured as the current choices. `--resolve --harness <this CLI>` prints what each role runs as here. Otherwise start from those defaults. Unless the user asked for a per-repo override, the user-level file is the one being configured. A line whose role is not in `examples/pstack-models.md`, such as `how critics`, is from a retired role. Drop it.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Prefer AskQuestion over free text. Offer these five options with these exact labels, and name the current budget when the file records one. With no file, say that `default` keeps the shipped defaults. The first is a port addition, and the other four match upstream.

- `default — keep as written`
- `unlimited — max reasoning`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

On Claude Code, describe `default — keep as written` as "roles without a written effort run at your session effort", and say at the ask that a budget's suffix overrides the session effort in both directions once the effort agents are loaded.

**(b) Apply it.** Build the working table from `examples/pstack-models.md`, and on a re-run keep any role the user changed by model, effort, list, alias (`inherit-parent`, `auto`), or harness section. `default` applies no budget: every written `@effort` suffix stands and unsuffixed entries keep the effort policy in [references/models-config.md](references/models-config.md), which on Claude Code is the session effort. `unlimited`, `large`, `medium`, and `small` set the `@effort` of every real entry, panel entries and harness sections included, to `max`, `xhigh`, `high`, or `medium`, adding the suffix where none was written. If the lint in step 4 rejects that effort for the model, use the model's highest supported effort at or below the target. An entry whose model the lint cannot classify keeps its written effort, or stays unsuffixed, and step (c) names it as untouched. An alias with a written suffix, such as `auto@max`, gets the same rewrite on its suffix, since Codex honors a suffix on an alias. A bare `inherit-parent` or `auto` does not change. No budget changes a model or a list length. So `small` turns `fable` into `fable@medium` and `gpt-6-sol@max` into `gpt-6-sol@medium`, and `unlimited` turns both back into `fable@max` and `gpt-6-sol@max`. On Claude Code, a written suffix applies only while the effort agents are loaded. If the live catalog lacks them, say so. The suffixes still govern Codex and Hermes reading the same file, and subagents here run at the session effort until the agents are registered and the catalog lists them.

**(c) Show the roles and confirm.** The file is shared across CLIs, so a value this harness cannot validate is not wrong — it is another harness's choice (it reads as `inherit-parent` here). Show every role with its model and effort for this harness, marking values outside the detected set as "(set for another harness — kept unless you change it)" rather than as needing a choice. On Claude Code, show a role with no written effort as `session`, and mark a written effort "(inactive until the effort agents load)" when the live catalog lacks its agent. Also list each line step 2 dropped. Ask whether to accept as-is or change specific roles, offering the detected models plus `inherit-parent` and `auto` (both mean: this role runs on the parent chat model, which is how Auto users stay on Auto) as the options. Prefer AskQuestion over free text. For panel roles (arena runners, architect runners, interrogate reviewers) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one value from it whose model family or capability tier differs from the parent's when possible. `swarm workers` runs every swarm worker that runs something, per the **swarm** skill, unless a race or comparison assigns another model per arm. `trail reviewer` runs the show-me-your-work reviewer and every independent verdict and review, including a swarm's audit lanes. For reviewer resolution and model opt-outs, follow [models config rule 7](references/models-config.md#resolution). For execution-identity disclosure, follow [Spawn a role](../pstack-harness/SKILL.md#spawn-a-role). `default` is the entry for any spawn whose skill names no role; keep it `inherit-parent` unless the user wants unmapped spawns on a specific model.

### 4. Validate

Run the lint on the file you are about to write, before writing it: `python3 <this skill's directory>/scripts/check-models-config.py <file>`. Any `error:` line (unknown role, bad effort, an effort the model does not support, a duplicate role or section, `none` or `ultra` under `## claude-code`) stops the write; fix the line and re-run. `notice:` lines mark `max` and `ultra` pins, and a flat-line `none` or `ultra` that Claude Code runs at the session effort. Read each one back to the user, so an expensive tier or a Claude Code fallback is a choice. Every *newly chosen* real slug must be in the detected set. `inherit-parent` and `auto` always pass, and preserved values from another harness are exempt. If a chosen real slug is not available, stop and ask again. Once the lint passes, show the user what each role will run as here. For the user file, run `python3 <this skill's directory>/scripts/check-models-config.py --resolve --harness <this CLI> --user-file <file>` from the project root, which also applies any workspace file there. For a per-repo override, copy the draft to `<temp>/.agents/pstack-models.md` and pass `--project <temp>` instead, so the real user file stays underneath.

### 5. Write the config

The target is `~/.agents/pstack-models.md`, or workspace `.agents/pstack-models.md` when the user asked for a per-repo override (only write roles the user actually wants pinned for this repo — every workspace line shadows the user-level one). A workspace file's `# budget` line covers only the roles written in that file. Roles that still resolve from `~/.agents/pstack-models.md` keep that file's budget. If your file tool cannot write the target (a harness that scopes writes to the workspace), fall back in order: write it through your shell tool; else write the workspace file and say the config is project-local until copied to `~/.agents/`; else print the final content for the user to save. Never silently drop the write.

Write the file with a `# budget` line holding the chosen label and its target effort, and one line per role, using the same labels poteto-mode uses. Start from `examples/pstack-models.md` next to this skill and keep its header comments, replacing the value on its budget line. Rewrite the whole file so re-runs stay idempotent, but carry forward every existing line the user did not change — including sections and values this harness could not validate; overwriting another CLI's choices with `inherit-parent` is the one failure mode to avoid. Leave out the retired-role lines step 2 dropped. Put a harness-specific pick under its `## <harness>` section and leave the flat lines for the other CLIs. Shape (excerpt):

```
# budget: default (keep as written)
feature, refactoring: sonnet
bug-fix: sonnet

## codex
feature, refactoring: gpt-6-sol@high
bug-fix: gpt-6-sol@xhigh
```

### 6. Confirm

Tell the user the config was written and that skills read it the next time they run. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, use the **create-verification-skill** skill. On no, move on without pushing.
