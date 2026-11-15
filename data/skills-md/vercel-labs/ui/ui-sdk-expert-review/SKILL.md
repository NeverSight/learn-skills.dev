---
name: ui-sdk-expert-review
description: Reviews a change with ui-sdk's framework experts (react, vue, svelte, solid, web), only the ones the change reaches, each from its last reviewed commit. Use before merging a branch that touches an adapter, core, specs, examples or framework docs, or when asked for an expert review. Pass a base ref, framework names, or nothing.
metadata:
  internal: true
---

# ui-sdk: expert review

Run the framework experts on what changed. Each expert lives in `.agents/experts/<framework>/`: who it is in `expert.md`, what it knows in `knowledge.md` and what's decided in `decisions.md`. You orchestrate; the experts review.

## 1. Find the scope

```sh
node scripts/expert-scope.mjs --json            # each expert from its "Last reviewed" commit
node scripts/expert-scope.mjs --base origin/main --json   # a branch before merging
```

Arguments narrow it: a ref becomes `--base`; framework names keep only those experts. An empty plan means no expert is needed: say so and stop.

Then run each framework's own lint rules on what changed, so the experts spend their review on what a linter can't catch:

```sh
git diff --name-only <base>...HEAD | xargs npx eslint --no-warn-ignored
```

## 2. Ask the experts

Spawn one background agent per framework in the plan, all at once, as `<framework>-expert` (in a harness without named agents, a general-purpose agent told to read `.agents/experts/<framework>/expert.md` first and act as it). Prompt:

```
Review mode. Scope: git diff <base>...HEAD.
Your files: <own>. Shared files every adapter renders: <shared>.
Review your files, and the shared ones only for what a user of your framework would meet.
Don't report anything decisions.md lists, or these lint findings: <findings, or none>.
```

Each expert works in its own worktree when it writes throwaway tests (`git worktree add ../ui-sdk-expert-<framework> HEAD`), with its own ports.

## 3. Collect

1. One table: framework, verdict, proven findings by rank, suspected, revisit.
2. Dedupe across experts: a finding in core that several experts report is one item, listed once, with every framework it reaches.
3. Hand the table to the user. Don't fix anything unless asked.

## 4. After triage

Each finding goes one of three ways, in the same turn:

- **Fix now**: fix it with its proof as the test.
- **Later**: one line under "Known and open" in that expert's `decisions.md`.
- **Won't do / decided otherwise**: one line under "Settled" in `decisions.md`, with the reason, so no expert raises it again.

Then move `Last reviewed:` in each expert's `decisions.md` to the reviewed `HEAD`. If an expert said its `knowledge.md` was wrong, fix the file and its "Last checked" date.
