---
name: rivet-open-orange
description: Run a Cloudflare Workers project on Rivet with OpenOrange, the orange CLI, and move its Durable Objects and D1 databases off Cloudflare. Use when asked to run, deploy, migrate, or roll back a Cloudflare Worker on Rivet or OpenOrange.
---

# Run a Cloudflare Worker on Rivet with OpenOrange

OpenOrange runs a Cloudflare Workers project on Rivet with no changes to its code. `orange dev` runs it locally, `orange deploy` ships it to a Rivet cluster, and `orange migrate` moves its Durable Objects and D1 databases off Cloudflare while the app keeps serving.

Do the parts the user asks for. Each part needs the parts before it: set up, run locally, deploy, migrate.

## Rules

- **Stop and ask.** At each **Stop and ask**, tell the user what changes and for whom, then wait for a yes. A yes covers that one action.
- **Secrets.** The user creates and types every secret value: `WORKER_MIGRATOR_TOKEN`, `CLOUDFLARE_API_TOKEN`, and Rivet tokens. Write a secret only as its name or `$NAME`, in commands, files, and output. Ask the user to run each command that prompts for a value, such as `wrangler secret put` and `rivet cluster secret set`.
- **The code stays.** Keep the app code and the Wrangler configuration as they are, `compatibility_flags` included: Cloudflare runs the same code until the migration ends. When a fix needs a code change, tell the user first.
- **Cloudflare stays.** Orange deletes nothing on Cloudflare. The user deletes the Cloudflare Worker and its data, after the migration.
- **Look it up.** `orange <command> --help` has every flag, JSON event, and exit code. The [Deploy](https://openorange.dev/docs/deploy/) and [Migrate](https://openorange.dev/docs/migrate/) guides have every step, message, and failure in detail, and each binding has a page under <https://openorange.dev/docs/bindings/>.
- **Bugs.** When a command ends with `Looks like a bug? Report it: <link>`, give the user the link. Orange prints it only for unexpected errors.

## Set up

1. **Install.** `orange --version` prints a version when OpenOrange is installed. Otherwise:

   ```sh
   pnpm add -g open-orange
   ```

   When the shell then cannot find `orange`, run `pnpm setup`, which puts pnpm's global bin on `PATH`, and start a new shell. When the installed version is older than `pnpm view open-orange version`, a pnpm `minimumReleaseAge` limit held back a new release: run `pnpm add -g open-orange@latest`.
   Done when `orange --version` prints the latest version.

2. **Check the project.** Run `orange doctor --json` in the Worker's directory. Fix each `check` event with `"status":"fail"` by its `hint`, and run doctor again. Show the user one table of the `binding` events: name, resource, `support`, and `hint`. For a migration, add the `durable_object_class` events: a class with `"migratable":false` cannot move, and its `hint` says why. When the `summary` event has `"mcp":{"configured":false}`, suggest the Rivet MCP once: `orange mcp` prints the command for the user's agent.
   **Stop and ask:** confirm the bindings that need a service, the ones that are not supported, and, for a migration, the classes and D1 databases that will move.
   Done when doctor exits `0` and the user agrees.

## Run locally

Start `orange dev` in the background. It serves on `http://127.0.0.1:8787` (`--port` picks another) and keeps its data in `.open-orange/`, which belongs in `.gitignore`. For a D1 app, apply the migrations to the local database first: `orange d1 migrations apply <DB> --local`.

Exercise every kind of route the app has: create, read, update, and delete each resource. When the app has its own tests, run them against that URL. A call that fails on Orange and works on Cloudflare is often a known difference: look on that binding's page.

Done when each route answers as it does on Cloudflare. Then stop `orange dev`.

## Deploy

Ask where it runs: a Rivet Cloud cluster, which needs Docker, or the user's own Rivet Engine ([Self-host](https://openorange.dev/docs/deploy/#self-host)). A BYOC cluster is a Rivet Cloud cluster.

1. **Sign in and link.** `orange login` opens a browser for the user to approve, and keeps a session that still works. Get the cluster name from the user or the Rivet MCP.

   ```sh
   orange login
   orange link --cluster <cluster>
   ```

   In CI, a cluster token goes in `RIVET_CLOUD_TOKEN`, as [Deploy from CI](https://openorange.dev/docs/deploy/#deploy-from-ci) says. A cluster token cannot create a runner pool, so with one the pool must already exist: the user creates it in the dashboard, or deploys once with `orange login`.
   Done when `orange whoami` shows the account and the linked cluster.

2. **Check the plan.** `orange deploy --dry-run` writes the build and calls no API. Show the user the cluster, region, pool, image, variables, and secrets that it prints.
   - Secrets go in with `--secrets-file` or `--secret`, because `vars` ship inside the image. Before `--secrets-file .dev.vars`, confirm with the user which names the file holds, without reading the values.
   - When the Worker has `triggers.crons` and its data moves later, add `--var ORANGE_CRONS:off` to every deploy until the domain moves. Otherwise each cron runs on Cloudflare and on Orange.

   Done when the plan names the cluster and pool that the user expects.

3. **Deploy.** **Stop and ask** before the first deploy: it creates or rolls a runner pool, which can cost money.

   ```sh
   orange deploy
   ```

   A deploy takes several minutes: a Docker build, an upload, 3 to 5 minutes for Rivet Cloud to prepare the build, and a rollout. On a failure, read [Fix a failed deploy](https://openorange.dev/docs/deploy/#fix-a-failed-deploy).
   Done when it prints `✓ Deployed`, a `Build` ID, and a `URL`, and a request to the URL works. Record the build ID: `orange deploy --build <id>` rolls the pool back to it.

When the data moves later, test the deployed Worker only as [Test Orange before the migration is on](https://openorange.dev/docs/migrate/#test-orange-before-the-migration-is-on) allows: a request that starts a Durable Object which Cloudflare also has, even a read, blocks that object's move. For a D1 app, the deployed database stays empty, with no migrations applied, until its move.

## Migrate the data

Follow `references/migrate.md`. Start only after the deploy works.

## Roll back

When the user asks to undo a migration step, or a step leaves production broken, follow `references/rollback.md`.
