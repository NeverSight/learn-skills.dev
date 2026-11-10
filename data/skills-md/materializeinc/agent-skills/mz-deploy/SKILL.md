---
name: mz-deploy
description: >-
  Using the mz-deploy CLI to manage a declarative SQL project for
  Materialize — project layout and the stage/wait/promote deployment
  lifecycle. Use this skill whenever the user is working in an
  mz-deploy project (a directory containing project.toml), asks how to
  deploy SQL changes to Materialize safely, or mentions mz-deploy,
  project.toml, profiles.toml, types.lock, staging deployments, deploy
  IDs, `mz-deploy stage`, `mz-deploy promote`, `mz-deploy abort`,
  `mz-deploy apply`, `SET api = stable`, stable API schemas,
  replacement materialized views, EXECUTE UNIT TEST, or per-profile SQL
  file overrides (`name#profile.sql`). Also trigger when a user needs
  to roll back a Materialize deployment or resolve a deployment
  conflict.
---

# mz-deploy

`mz-deploy` is declarative SQL project tooling for Materialize. A project is a
git-tracked directory of `.sql` files describing the desired state of a
Materialize environment; `mz-deploy` compiles it, type-checks it offline, tests
it in a local container, and deploys changes through an atomic
stage-then-promote lifecycle.

```bash
brew install materializeinc/materialize/mz-deploy
```

## Discover Before You Run

The CLI is self-documenting, and its help text is the source of truth. **Do not
guess command names, flags, or argument order.**

1. `mz-deploy help` — all commands, grouped by purpose.
2. `mz-deploy help <command>` — the detailed usage guide for one command:
   behavior, every flag, examples, error recovery, and exit codes.
3. `mz-deploy help profiles` — the configuration topic guide (profiles,
   variables, suffixes, file overrides, TLS).

This skill covers the concepts and the shape of the workflow so you know
*which* command to reach for. Read that command's `help` for the flags before
running it.

Run commands from the project root, or pass `-d <path>`. Global options worth
knowing: `-p/--profile` selects the connection profile, `--output json` for
machine-readable output (supported by most commands, useful in CI), `-v` for
verbose debugging, `-q` to suppress informational output.

## Project Layout

```
project.toml              # project config: mz_version, dependencies, per-profile settings
profiles.toml             # connection profiles (also resolved from ~/.mz)
.mzprofile                # gitignored per-checkout default profile
types.lock                # cached schemas of external dependencies, for offline type checking
target/                   # gitignored local build cache (safe to delete; see `clean`)
models/
  <database>/
    <schema>.sql          # schema mod file — schema-level statements (see below)
    <schema>/
      <object>.sql        # one view, materialized view, table, source, sink, connection, or secret
clusters/<name>.sql       # cluster definitions (+ their GRANTs)
roles/<name>.sql          # role definitions
network-policies/<name>.sql
```

The path determines the object's fully qualified name: an MV in
`models/materialize/catalog/clusters.sql` is
`materialize.catalog.clusters`. A **schema mod file** — `<schema>.sql`
sitting beside the `<schema>/` directory — holds statements that apply to the
schema as a whole, such as `SET api = stable`.

`mz-deploy new <name>` scaffolds this structure in a new directory; `init` does
the same in the current one.

## Command Map

| Group | Commands |
|-------|----------|
| **Getting started** | `new`, `init`, `profile` (list/set/current), `setup`, `debug` |
| **Develop** | `compile`, `clean`, `test`, `explain`, `dev`, `lsp`, `sql`, `mcp` |
| **Infrastructure** | `lock`, `apply`, `delete` |
| **Deploy** | `stage`, `wait`, `promote`, `abort`, `describe`, `list`, `log` |

One-time bootstrap: `mz-deploy setup` creates the `_mz_deploy` tracking
database, its tables, the `_mz_deploy_server` cluster, and three roles. **It
must be run by a superuser when RBAC is enabled**, because it grants system
privileges. Everything after that runs as an ordinary user.

## Workflow

```bash
mz-deploy compile              # parse, resolve dependencies, type-check offline
mz-deploy test                 # run unit tests in a local Materialize container
mz-deploy apply                # converge infrastructure (see below)
mz-deploy stage                # deploy changed views/MVs to suffixed staging schemas
mz-deploy wait <DEPLOY_ID>     # watch clusters hydrate until ready
mz-deploy promote <DEPLOY_ID>  # atomic swap into production
```

`compile` needs no database connection, so it belongs in CI on every commit. A
passing `compile` guarantees `stage` and `apply` will not fail at the SQL
parsing stage. Note that *every* profile variant is validated regardless of
`--profile`, so a syntax error in `foo#staging.sql` still fails
`compile --profile production`.

Alongside: `list` shows unpromoted deployments (like `git branch`), `describe
<ID>` details one, `log` shows promotion history (like `git log`), and `abort
<ID>` destroys a staging deployment without promoting it.

## Key Concepts

**`apply` owns infrastructure; `stage` owns views.** `apply` is declarative,
diff-based, and idempotent, converging clusters, roles, network policies,
secrets, connections, sources, and tables in dependency order. `stage` handles
views and materialized views. Tables and sources are *never* created by
`stage` — they must already exist, so `apply` runs first. `delete <type>
<name>` is the inverse of `apply`: it drops one object **without CASCADE** and
removes its project file.

**Deploy IDs and staging suffixes.** Each deployment gets an ID — by default
the first 7 characters of the current commit SHA — used to suffix its schemas
and clusters (`public` → `public_abc123`). Staging clusters are cloned from the
corresponding production cluster's configuration, including any auto-scaling
strategy, so staged objects hydrate the way production will. Staging runs in
isolation alongside production.

**Change detection is hash-based.** `stage` compares each object's SQL hash
against the last promoted snapshot and deploys only what changed, plus
anything downstream of a change. Unchanged objects are not recreated. Override
with `--redeploy-schema <db.schema>` or `--redeploy-all`.

**Promotion is atomic and resumable.** `promote` executes `ALTER … SWAP` on
schemas and clusters inside a single transaction, then does post-swap work:
creating deferred sinks, applying replacement MVs, repointing sinks at the new
production objects, and dropping the old resources. If it dies mid-flight,
re-running the same command detects the post-swap state and resumes cleanup.

**Sinks are deferred to promote.** They must not start producing until the
deployment is live, so `stage` records them and `promote` creates them.

**Conflict detection works at schema and cluster granularity.** Because a whole
schema is swapped as a unit, two deployments touching *any* of the same schemas
or clusters conflict — even when they modify different objects inside them. The
first to promote wins; the second is rejected and must be re-staged against
current production. `--force` skips the check, and doing so **drops the other
deployer's schemas**, since schemas are swapped wholesale rather than merged.
Only use it when clobbering that work is the intent.

**Stable API schemas.** By default a changed object is recreated in staging and
its whole schema is swapped, which redeploys in-project dependents
automatically but breaks consumers in *other* mz-deploy projects. Adding `SET
api = stable` to a schema mod file marks that schema as an API boundary:
changed MVs are updated in place via `ALTER MATERIALIZED VIEW … APPLY
REPLACEMENT`, preserving object identity. Downstream consumers — in any project
— need no redeployment. Constraints: stable schemas may contain **only**
materialized views, and a changed replacement MV does not propagate dirtiness
to its dependents.

**Type checking is offline.** `compile` and `test` read external dependency
schemas from `types.lock`. Declare external objects in `project.toml` as
`dependencies = ["db.schema.table"]` and run `mz-deploy lock` to refresh the
file. Source tables created by `CREATE TABLE FROM SOURCE` are auto-discovered
and need no declaration; `apply tables` regenerates the lock automatically.

**Roles.** `setup` creates `materialize_deployer` (stage, promote, abort),
`materialize_developer` (read-only deployment state, plus `dev` overlays), and
`materialize_monitor`. Each user must belong to **exactly one** — holding
several is an error. Use separate profiles with distinct users for deploying,
developing, and monitoring.

## Profiles and Per-Profile Configuration

A profile is a named connection target in `profiles.toml`, resolved from
`--profiles-dir`, then `MZ_DEPLOY_PROFILES_DIR`, then `~/.mz`. The **active**
profile resolves from `--profile`, then `MZ_DEPLOY_PROFILE`, then the
gitignored `.mzprofile` in the project root (written by `mz-deploy profile
set`). A built-in `emulator` profile always exists, so a local Materialize
emulator works with zero configuration.

Passwords support `${VAR}` substitution, overridable by
`MZ_PROFILE_<NAME>_PASSWORD`. `sslmode` follows PostgreSQL's vocabulary and
defaults to `prefer` for loopback hosts, `require` otherwise — use
`verify-full` for Materialize Cloud.

The profile does more than pick a host. It also selects, at compile time:

- **`profile_suffix`** (in `project.toml`) — appended to every database and
  cluster name, including `IN CLUSTER` references. Write the delimiter
  yourself: `"_staging"`, not `"staging"`. Staging suffixes stack on top
  (`foo` → `foo_staging` → `foo_staging_a`).
- **SQL variables** — `[<profile>.variables]` in `project.toml`, referenced in
  any `.sql` file with psql syntax: `:name` (raw), `:'name'` (quoted string),
  `:"name"` (quoted identifier). Referencing an undefined variable fails
  compilation.
- **File overrides** — `name#<profile>.sql` replaces `name.sql` when that
  profile is active. All variants are validated at compile time regardless of
  which is active, and all must share the same primary statement type. **Views
  and materialized views cannot have file overrides** — use SQL variables
  instead.

## Rollback

There is no rollback command. Reverse the change in the project and promote the
result:

```bash
git revert <commit>
mz-deploy stage
mz-deploy promote <DEPLOY_ID>
```

Because `promote` swaps atomically, the rollback promotion is itself atomic —
production switches back in a single transaction.

## Unit Tests

`mz-deploy test` runs tests written inline in the same `.sql` file as the view
they cover, using `EXECUTE UNIT TEST` with mocked dependencies. The syntax is
specific to mz-deploy and documented nowhere else — see
[references/unit-tests.md](references/unit-tests.md) for the full grammar,
worked examples, and failure modes.

## Gotchas

- **`stage` requires a clean git tree.** Commit, stash, or pass
  `--allow-dirty`.
- **`setup` needs a superuser under RBAC**, one time only.
- **`test` and `explain` need Docker**, and share one container named
  `mz-deploy-sandbox` across invocations on the host. Reuse is by *name*, not
  by image, so `--docker-image` has no effect until you
  `docker rm -f mz-deploy-sandbox`.
- **`delete` never cascades.** If dependents exist it fails and leaves the
  project file in place.
- **`dev` will not target a production cluster.** Provision a dedicated dev
  cluster.
- **A profile's `cluster` option is ignored.** mz-deploy pins every connection
  to its own internal `_mz_deploy_server` cluster; resize that with a standard
  `ALTER CLUSTER` if needed.
- **`stage` failures roll back automatically.** Pass `--no-rollback` to keep
  the partial deployment for debugging, then clean up with `abort`.
- **A stale `target/` cache** can produce confusing compile or type errors. Run
  `mz-deploy clean`.
