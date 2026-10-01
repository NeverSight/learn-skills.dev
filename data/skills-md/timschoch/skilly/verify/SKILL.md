---
name: verify
description: The one definition of what each gate runs. Use to run a gate stage, to add or change a check, or to read why a step exists.
---

# Verify

[references/verify.json](references/verify.json) holds the default steps. Sync keeps them current in every Consumer. `.skilly/verify.json` holds only what the repo changes. Hooks and CI call a stage of the merged config, so the local gate and the pipeline cannot drift into disagreeing about what green means.

## Usage

```sh
node .agents/skills/verify/scripts/verify.mjs <stage>           # run the stage
node .agents/skills/verify/scripts/verify.mjs <stage> --steps   # resolved steps as JSON, runs nothing
node .agents/skills/verify/scripts/verify.mjs --config          # merged config as JSON, runs nothing
```

Works from anywhere in the Consumer. Exit 0 passed, 2 config or usage error, anything else is the failing step's code.

## Config

Shape of both files:

```json
{
  "budgetTicket": "https://github.com/owner/repo/issues/1",
  "stages": {
    "commit": { "budgetSeconds": 10, "steps": [{ "name": "lint-staged", "run": "npx lint-staged", "why": "the reason this step exists" }] },
    "push": { "extends": "commit", "budgetSeconds": 120, "steps": [] },
    "ci": { "extends": "push", "budgetSeconds": 600, "steps": [] },
    "nightly": { "tier": "product", "budgetSeconds": 1800, "steps": [{ "name": "e2e", "run": "npm run e2e", "target": "e2e" }] }
  }
}
```

`extends` is cumulative: `push` runs every `commit` step first, so no stage can skip a check the stage below it runs.

A budget warns and never fails. A gate that fails on slowness teaches you to bypass the gate, and the bypass outlives the slowness. `budgetTicket` says where a stage that outgrew its budget gets split.

## Override

`.skilly/verify.json` merges over the defaults ([scripts/merge-config.mjs](scripts/merge-config.mjs)). Steps match by `name`, per stage:

| Repo file | Effect |
| --- | --- |
| `{ "name": "lint", "run": "pnpm lint" }` | changes the default `lint` step, keeps its other fields |
| `"-lint"` | drops the default `lint` step |
| `{ "name": "docs", "run": "…" }` | adds a step after the defaults |
| `"budgetSeconds": 60` on a stage | replaces the default |

The file is optional. Check the result with `--config` or `<stage> --steps`.

## Tier

`tier` in `.skilly/config.json`, default `sandbox`, order `sandbox` < `tool` < `product`. A step's `tier` is the minimum a repo needs to run it; below that the step is skipped. A stage's `tier` is that rule for the whole stage: below it nothing runs and the exit is 0. Tier sets the size of the net, not the standard.

## Target

A step's `target` is a path relative to the repo root; missing, the step is skipped. That is how one stage list fits repos that do not all have an `e2e/` or a Dockerfile.

## Adding a check

One step, never a line in a hook or a workflow. A check for this repo only goes in `.skilly/verify.json`. A check every Consumer needs goes in the hub's `bundles/workflow/skills/verify/references/verify.json`. Give it a `why`: it prints the moment the step goes red, when the reader is least likely to go looking for it.
