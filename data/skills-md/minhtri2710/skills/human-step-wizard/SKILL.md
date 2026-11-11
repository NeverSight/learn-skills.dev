---
name: human-step-wizard
description: Generate a resumable bash wizard that walks a human through the steps only they can do, opening each URL, saying what to click and copy, and writing the captured values to .env and CI secrets. Use when a task hits credentials, third-party dashboards, account provisioning, or a one-off manual cutover that the agent cannot perform, instead of writing prose instructions. Do not use for steps the agent can run itself.
---

# Human Step Wizard

Some steps only a human can take: revealing an API key in a dashboard, approving
an OAuth app, provisioning an account. Prose instructions for them get re-explained
every time and skipped halfway. A wizard is a bash script that walks the human
through the procedure stage by stage, opens each URL, captures the values, writes
them where they belong, and shows how many stages remain. It is resumable: a
re-run offers the values already saved.

The UX is already solved by [scripts/wizard-template.sh](scripts/wizard-template.sh):
stage progress, screen clearing, cross-platform URL opening, hidden secret entry,
idempotent `.env` upserts, `gh secret` and `gh variable` writes with a recorded
skip when `gh` is not ready, and a closing summary. The `ask` and `ask_secret`
helpers re-ask when a required answer is empty and no saved value exists; end
of input without a saved value exits non-zero and names the required key. The
library above the `STAGES` marker is identical in every wizard; author only what
sits below it.

## 1. Scope the procedure

Read the repository before asking: `.env*`, the README, compose and framework
config, and every `secrets.*` or `vars.*` reference in the CI workflows, since
each is a value the wizard must produce. For a cutover, read the current state,
the target state, and the irreversible actions between them. Show the user the
ordered stages and the values each produces, and let them add, drop, or reorder.

Done when every stage is named in order and, for each captured value, you know
where the human gets it, where it is written (`.env`, a CI secret, both, or
nowhere for a pure action), and whether it is secret.

## 2. Map each stage's path

For each stage, write the exact route a stranger could follow: which URL, what to
click, where the value appears, which variable it fills ("Dashboard, Developers,
API keys, Reveal test key, copy"). Where the current UI or command is not known,
say so and ask or check the docs; an invented step costs the human more than a
question.

## 3. Author the stages

Copy the template to a scratch path or `scripts/`, replace the example stage with
one `stage` per step in dependency order, each at column 0 so `banner` counts it.
Use the helpers: `stage`, `say`, `step`, `note`, `warn`, `open_url`, `ask`, `ask_secret`,
`write_env`, `set_secret`, `set_var`, `pause`, `confirm`. Open the URL before
asking for its value, hide anything secret, `write_env` every persisted value,
`set_secret` only what CI actually reads, and gate anything irreversible on
`confirm` inside an `if`, never as a bare statement: the script runs under
`set -e`, so an unguarded "n" exits the wizard instead of skipping the step.
One focused task per stage, because each stage clears the screen.

## 4. Verify statically and hand off

`bash -n`, `shellcheck` when available, `chmod +x`. Never run it end to end: it
opens browsers and blocks on input. Trace it instead: every value from step 1 is
captured and lands where step 1 said, and every `set_secret` name matches a
`secrets.*` reference in CI exactly. Tell the user the command to run. The wizard
is deleted when the job is done unless the user wants a repeatable setup path
kept in the repository.
