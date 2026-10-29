---
name: outdo
description: Use outdo, the TypeScript task runner for Bun. Use whenever a repo has a do.ts (or the user says outdo, "bunx outdo", "run the gate", "add a task"), and before running, listing, adding or changing tasks, wiring CI (`outdo ci`, `outdo affected`), git hooks, background services (`outdo bg`), modes (--mode prod), env files, replacing package.json scripts, turbo, makefiles or .githooks with outdo, or cleaning up unused, dead or duplicate tasks (`outdo usage`).
---

# outdo

outdo runs the tasks in a repo's `do.ts` (and its `package.json` scripts) as a dependency graph, on Bun. Tasks are typed: dep names, flags and env are checked by TypeScript.

## Ground rules

- Bun only: `bunx outdo ...` or `outdo ...` (a global outdo hands over to the repo's installed copy). Never `npx`/`node`.
- **Look before you act.** `outdo ls --json` lists every task with its deps, steps, flags (types, choices, required), `readonly`/`destructive` tags and whether it asks for confirmation. `outdo <task> --help` shows one task. `outdo explain <task>` shows the plan without running it.
- **Never pass `--yes` on your own.** A task with `protect`/`confirm` asks before running; with no terminal it refuses. Only add `--yes` after the user explicitly agreed to run that task now. Prefer tasks marked `readonly: true` for unattended work; under `OUTDO_READONLY=1` outdo refuses everything else.
- Flags go after the task name (`outdo feed --source eco`), global flags before it (`outdo --dry feed`). `--mode`, `--yes`, `--from`, `--until` work in either place. Arguments after `--` go to the task's command.
- Exit codes: 0 ok, 1 a task failed, 2 usage/refused, 3 config error (bad do.ts / env), 130 interrupted.

## Running

```sh
outdo                         # list tasks
outdo test                    # run a task and its deps
outdo lint test               # several (shared deps run once)
outdo db reset                # namespaced task (same as db:reset)
outdo logs api -f             # positional value + flag
outdo gate --from typegen     # part of a task's steps
outdo up --mode prod          # mode: picks .env.prod etc.
outdo --dry gate              # plan only (--dry=json for machines)
outdo --print-env deploy      # where every env value came from
outdo --affected test         # only if git changes touch it
outdo -w test                 # re-run on file changes
```

In workspaces a bare name runs the root task and every member's task of that name; `pkg#task` runs one package's task. When the root has its own task of that name, member package.json scripts are not added (the root task pulls them in with `deps: ["^name"]`).

## Writing tasks (do.ts)

```ts
import { defineTasks, ns } from "@meslzy/outdo";
import { z } from "zod";

export default defineTasks(
	{
		fix: "bunx biome check --write",                       // one command
		sync: ["bun run syncpack:fix", "bun install"],         // commands in order
		tsc: { desc: "Type-check", run: "bunx tsc --noEmit", readonly: true },
		test: { deps: ["tsc"], run: "bun test" },              // deps run first, in parallel
		gate: { steps: ["fix", "tsc", "test"] },               // one after another
		build: { inputs: ["src/**"], outputs: ["dist/**"], run: "bun build src/index.ts --outdir dist" }, // cached
		dev: { persistent: true, ready: { port: 3000 }, run: "bun --watch src/index.ts" },
		playwright: "bunx playwright test",
		e2e: { steps: ["dev", "playwright"] },                 // server up, tests, server stopped
		shoot: { steps: ["build", "playwright"], finally: ["fix"] }, // finally runs even on failure
		feed: {
			args: {
				source: z.enum(["eco", "all"]).default("all"),   // schema flag: validated + typed
				id: { type: "string", required: true },          // or an ArgSpec
			},
			positional: ["id"],                              // outdo feed C-0007
			run: async ({ $, args, env, mode, root, log }) => {
				await $`bun scripts/feed.ts ${args.source} ${args.id}`;
			},
		},
		deploy: {
			protect: "prod",                                   // asks in prod; --yes skips
			env: z.object({ VPS_HOST: z.string() }),           // validated before anything runs
			run: async ({ ssh, env }) => {
				await ssh(`deploy@${env.VPS_HOST}`).cwd("~/app")`git pull && bunx outdo up --mode prod`;
			},
		},
		db: ns({ reset: { deps: ["backup"], run: "bun db/reset.ts" }, backup: "bun db/backup.ts" }),
	},
	{
		modes: ["dev", "prod"],                              // first is the default
		hooks: { "pre-commit": { steps: ["fix", "tsc"], restage: true } },
		members: { tsc: { deps: ["^tsc"] } },                // workspace defaults (replaces turbo)
	},
);
```

- `task()` is optional: `env`/`args`/`deps` on an object entry already type `run`'s context.
- A do.ts entry with no `run`/`steps` and the same name as a package.json script runs that script (so do.ts can add deps, `readonly`, inputs).
- Dep, step, finally and hook names are checked at compile time; run `bunx tsc --noEmit` after editing do.ts.
- Everything a task needs at runtime: `ctx.$` (Bun Shell in the task's cwd/env), `ctx.args`, `ctx.env`, `ctx.deps` (dep outputs), `ctx.rest`, `ctx.mode`, `ctx.root`, `ctx.cwd`, `ctx.ssh`, `ctx.log`, `ctx.signal`.

Full field list, flag forms and context: [references/do-ts.md](references/do-ts.md).

## CI, hooks, services, MCP

```sh
bunx outdo ci check                  # in GitHub Actions: only what changed, folded logs, annotations
outdo ci init                        # writes .github/workflows/ci.yml
outdo affected deploy --github-output   # deploy=true|false for `if:` conditions
outdo hooks install                  # install the hooks declared in do.ts
outdo bg start dev; outdo bg ps; outdo bg logs dev -f; outdo bg stop
outdo doctor                         # run every task's `requires` checks
outdo prune --docker                 # out/json/: package.jsons + lockfile for a Docker layer
```

`outdo mcp` serves every task as an MCP tool (`.mcp.json`: `{"mcpServers": {"outdo": {"command": "bunx", "args": ["outdo", "mcp"]}}}`).

Commands and flags: [references/cli.md](references/cli.md). Replacing package.json scripts, turbo, makefiles, .githooks, paths-filter and compose wrappers: [references/recipes.md](references/recipes.md).

## Cleaning up tasks

`outdo usage --json` is the evidence: per task `you` / `agent` / `deps` / `hooks` / `typed` (shell history) counts, `status` (`used`, `referenced` = never run but something uses it, `unused`), `usedBy`, `firstSeen`, flags with `given` / `runs` / `unusedValues`, plus `trackedSince` and static `duplicates`. `outdo usage <task>` shows one task.

- Fix `duplicates` first (hidden package.json scripts, `run: "bun run <own name>"`, aliases, same command or steps) — they are facts, not guesses.
- `unused` is a proposal, not a verdict: with a young log (`trackedSince` under a few weeks) or a member script (`pkg#name`, may run in a container or via turbo), say so. List what you would delete and ask before deleting.
- Removing a task: also remove it from other tasks' `deps`/`steps`/`finally`, hooks and CI workflows (`usedBy` lists them), then `bunx tsc --noEmit`.

## When something fails

- `Unknown task "x"` → `outdo ls`; names in namespaces are `ns:task`, workspace ones `pkg#task`.
- `Task "x" requires --flag` / `invalid value` → `outdo x --help` lists flags, choices and positional values.
- `asks for confirmation and there is no terminal` → ask the user; re-run with `--yes` only if they agree.
- `OUTDO_READONLY is set: refusing ...` → only `readonly: true` tasks may run here.
- `Environment validation failed` → `outdo --print-env <task>` shows each value's source file.
- A task skipped as cached → `outdo explain <task>` says why; `--force` re-runs.
