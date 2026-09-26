---
name: docker-sandboxes-env
description: Use this skill when authoring, planning, or running a declarative `sbxenv.yaml` file for Docker Sandboxes (`sbx env create/run/plan/exec/rm`), even if the user just says they want to "check in a sandbox config", "make onboarding reproducible for a sandbox", "run a setup script before the agent starts", or "define arguments for a shared sandbox environment". Covers the sbxenv.yaml schema (schemaVersion, agent, kits, workspace/additionalWorkspaces, args, env, secrets, registries, bindings, mcp, ports, sandboxOptions), host `lifecycle:` commands (initialize/postCreate/preRemove) and their approval-plan model, multi-file merge (`-f`-style deep merge and the user-level `.sbxenv.yaml` base layer), and file-write-protection (`sandboxOptions.writableEnvFiles`).
license: Apache-2.0
compatibility: Requires standalone sbx with sbx env support and sbxenv.yaml schemaVersion "1", not the legacy docker sandbox wrapper. Verified against docker/sandboxes df5c96ba60484fa2c375469dbac912c205da6c37; installed-help version and provenance are in references/sources.md. docker_help does not cover standalone sbx.
---

# Docker Sandboxes: Declarative sbxenv.yaml Environments

## Overview

`sbxenv.yaml` (schemaVersion `"1"`, EXPERIMENTAL) declaratively describes one
sandbox environment — agent, mixin kits, workspace mounts, environment
variables, secrets/registries/bindings to provision, MCP servers, ports, and
host-side lifecycle commands — so `sbx env create|run|plan|exec|rm` can stand
it up and tear it down reproducibly instead of a long flag invocation. This
skill owns that file format end to end. It delegates the sandbox lifecycle
semantics it wraps, the credential/network model it provisions into, and the
kit schema its `kits:` entries reference, to their own skills.

## When to use this skill

Activate this skill when:
- The user wants a checked-in, reproducible definition of a sandbox
  environment instead of a long `sbx create`/`sbx run` command line.
- The user wants host-side setup/teardown commands (cloning a repo, seeding
  fixtures, archiving state) tied to a sandbox's create/attach/remove
  lifecycle.
- The user wants to parameterize a shared environment file with named
  arguments (`args:` + `--env-arg`).
- The user is debugging why `sbx env create`/`run` is asking for approval,
  or why a file, kit, or secret it declares was skipped or flagged.

## Do not use this skill when

Do not use this skill when:
- The task is the underlying `sbx create`/`run`/`rm` flag-based workflow with
  no `sbxenv.yaml` file involved — use `docker-sandboxes-lifecycle`.
- The task is choosing network policy or storing a secret/registry
  credential independent of any environment file — use
  `docker-sandboxes-network-credentials` (this skill's `secrets:`/
  `registries:`/`bindings:` blocks provision into that same store, but do not
  redefine its rules here).
- The task is authoring the kit `spec.yaml` a `kits:` entry points at — use
  `docker-sandboxes-kits`.

## Core guidance

### File resolution and required fields

- The file `sbx env` reads from a directory is exactly `sbxenv.yaml` — no
  other name, and a directory-named `.sbxenv.yaml` at the project level is
  **not** read as a project's own file (only the home-directory base layer
  uses that hidden name; see below).
- Every environment file requires `schemaVersion: "1"` and `agent:` (a
  built-in agent name or the manifest name of an agent kit supplied via
  `kits:`). Everything else is optional. `agent: shell` needs no credentials
  and is the simplest way to validate a file's mechanics.
- `sbx env create|run|plan|exec|rm` accept one or more `PATH` arguments.
  Each `PATH` is either a directory (resolved to `<PATH>/sbxenv.yaml`) or the
  file itself. Passing more than one deep-merges them in declaration order —
  **`docker compose -f`-style semantics**: later files override earlier ones,
  mappings merge key-by-key, sequences concatenate.
  ```bash
  sbx env create sbxenv.yaml override.yaml
  ```

### Naming, workspace, and the `.sbxenv.yaml` user base layer

- Unless the file sets `name:` or `--name` overrides it, the sandbox is
  named after the mounted directory (or the project directory when nothing
  is mounted) — so an environment that mounts nothing is still the same
  sandbox every time it is applied. **Two different environment files in the
  same directory derive the same sandbox name and collide** unless each sets
  its own `name:` (or you pass a distinct `--name` per invocation) — always
  give each environment its own explicit `name:` when more than one may
  exist in the same directory.
- `workspace:` names the read/write mount, exactly like `sbx create`'s
  omitted-path behavior: **omitting `workspace:` mounts nothing** at all.
  A relative `workspace:` path resolves against the **directory of the file
  that declares it** — `workspace: .` mounts the directory the file sits
  in. `${{ env.projectDir }}` names the project directory (the one holding
  the first `PATH`, or cwd when none is named); `${{ env.fileDir }}` names
  the declaring file's own directory. Nothing else is expanded — a bare `$`
  is literal text, so a value written for the container
  (`PATH: $PATH:/opt/bin`) reaches it unchanged.
  ```yaml
  workspace: .                       # mounts the directory this file sits in
  # workspace: ${{ env.projectDir }} # mounts the project directory explicitly
  ```
- Relative kit sources follow the same file-directory anchoring rule as
  `workspace:` (see `docker-sandboxes-kits` for kit reference syntax).
- **Files within a mounted workspace get default read-only masking, and that
  protection is complete only when the file sits directly at the mount's own
  root.** A read-only bind at the mount point cannot be renamed by the
  sandbox — there is nothing above it inside the mount to rename. But an
  environment file in a **subdirectory** of a read-write mount is protected
  only at its current path: the sandbox can rename the containing directory
  (which it can write to) and then recreate the original path itself,
  landing a sandbox-controlled file back where the read-only bind no longer
  applies. `sbx env plan` calls this gap out explicitly for a file that is
  not at a mount's root. Do not claim renaming the containing directory
  creates no gap — for anything but the mount root, it does.
- With **no `PATH`** given, an `.sbxenv.yaml` in the **home directory** is
  merged underneath as a base layer for defaults shared across projects;
  naming any `PATH` skips this layer entirely. The base layer may not set
  `name:` (which identifies one project) and its `workspace:` must be rooted
  at `${{ env.projectDir }}` — any other value would mount one fixed
  directory under every project that merges it.

### `args:` — parameterizing a shared file

- Declare named inputs under `args:`, each with a `default` (making it
  optional, `default: ""` counts as a real default) or `required: true`
  (mutually exclusive), plus optional `description`, `enum`, or `pattern`.
- Reference one as `${{ env.args.NAME }}` anywhere a value appears in the
  file, and supply it with `--env-arg NAME=VALUE` (repeatable) or
  `--env-args-file PATH`.

### `lifecycle:` — host commands and the approval plan

- `lifecycle:` declares shell commands that run **on the host, outside the
  sandbox, with your own privileges** — not inside the container. Three
  phases, run in this order per invocation:
  - **`initialize`** — runs on **every** `create` **and** `run`, including
    one that only attaches to an existing sandbox. It is the one phase that
    can produce what the environment needs to exist (a cloned workspace, a
    generated file), so **it must be idempotent** — it reruns on every
    reattach.
  - **`postCreate`** — runs once, after the sandbox exists, before an
    interactive attach takes the terminal.
  - **`preRemove`** — runs before `sbx env rm` deletes the sandbox, while
    `sbx env exec` can still reach it. **A failing `preRemove` is only a
    warning** — the failure itself does not block removal. After the hook,
    removal rechecks the approved destroy plan and sandbox identity. A new
    credential or changed binding not covered by that approval, or a
    replacement sandbox under the same name, stops removal before deletion.
    Review the new destroy plan before retrying.
  - `sbx env exec` **runs no lifecycle commands at all, and requires the
    sandbox to already exist** — it does not create one. Run
    `sbx env create`/`sbx env run` first.
  ```yaml
  lifecycle:
    initialize:
      - command: test -d app || git clone https://github.com/acme/app
    postCreate:
      - command: ./scripts/seed-fixtures.sh
    preRemove:
      - command: ./scripts/archive-state.sh
  ```
- Every command runs through the shell from the **project directory** by
  default (override per-command with `workdir:`; bound its runtime with
  `timeout:`).
- **A file that declares any lifecycle command is asked about on every
  invocation that reaches it, whether or not this particular invocation
  changed anything** — approving a command also trusts whatever it invokes,
  including a script whose contents can change after the answer, so the
  question is repeated rather than remembered by default. The one exception:
  `sbx settings set env.rememberHostCommands true` makes it ask again only
  when the commands actually change. **Never treat an untrusted file's or an
  untrusted kit's lifecycle commands as pre-approved**, and never enable
  `rememberHostCommands` for a file whose commands you have not reviewed. An
  environment that declares **no** host commands at all, and whose config is
  otherwise unchanged from what was last approved, applies silently with no
  prompt. Use `--skip-host-commands` to run none of the declared commands
  for one invocation.

### The environment plan: what it is and is not

- `sbx env plan [PATH...]` prints everything applying the file would set up
  — host commands, credentials/bindings, MCP registrations, directories,
  published ports, the sandbox itself, and its variables — compared against
  what was last applied/approved. **It changes nothing.**
- `sbx env create`/`sbx env run` show the same plan and require approval
  before doing any work (`--auto-approve`/`-y` skips the prompt for
  non-interactive use — **never default to `-y` for a file or kit you have
  not reviewed**). A secret's literal `value:` is the one field shown both
  in the plan and recorded to state as a `sha256:` digest rather than in the
  clear; a `ref:`/`command:` secret shows where the credential comes from,
  not its resolved value.

### Secrets, registries, and bindings scoped to the environment

- `secrets:` and `registries:` provision into the **same credential store**
  `sbx secret set` uses, at this environment's **sandbox scope**, so
  `sbx env rm` can remove exactly what it created. Each entry uses the same
  `value`/`ref`/`command` shape as `sbx secret set` (exactly one of the
  three) — see `docker-sandboxes-network-credentials` for what those mean at
  runtime and why a literal secret value should not otherwise appear in a
  checked-in file.
- `bindings:` are per-service credential bindings merged into the user's
  **global** `credentials.yaml`; unlike `secrets:`/`registries:`, they are
  **left in place by default** by `sbx env rm` (they are user-wide and may
  be shared with other sandboxes/environments) — pass `--prune-bindings` to
  also remove them.
- **Never write a literal secret value directly into a checked-in
  `sbxenv.yaml`.** Use `ref:` (1Password/AWS Secrets Manager) or `command:`
  so the value never lives in the file at all; if a literal `value:` is used
  transiently, both the plan and state show only its digest, but the
  original environment file still contains the plaintext secret. See the labeled `secrets:` fragment below for the
  shape — it is intentionally not part of the minimal asset, which needs no
  credentials at all to validate.
  ```yaml
  # OPTIONAL fragment — add only if this environment actually needs a
  # credential; the minimal asset omits this entirely.
  secrets:
    anthropic:
      ref: op://Private/Anthropic/api-key   # never a literal `value:` in a checked-in file
      refresh: 55m
  ```

### `kits:`, `additionalWorkspaces:`, `mcp:`, `ports:`, and `sandboxOptions:`

- `kits:` composes mixin kits (and, exactly once, an agent kit whose name
  matches `agent:`) onto the base agent; a relative source anchors to the
  **declaring file's own directory**, the same rule as `workspace:`.
- `additionalWorkspaces:` mounts extra directories beyond the primary
  `workspace:` (a file cannot declare one without the other) — the
  `sbxenv.yaml` equivalent of `sbx run`'s extra positional workspace
  arguments with `:ro`.
- `mcp.servers:` registers MCP servers on the host and adds them to the
  sandbox's fixed (static) MCP set at create time; registrations are
  host-global and **left in place** by `sbx env rm`.
- `ports:` pins explicit host-port bindings for container ports the
  sandbox exposes — the equivalent of `sbx ports --publish` — and is torn
  down automatically when `sbx env rm` deletes the sandbox.
- `sandboxOptions:` (beyond `writableEnvFiles`, below) maps onto the
  remaining `sbx create` flags: `template`, `memory`, `cpus`,
  `pullPolicy`, `profile`, `skills`.

See `references/env-schema-fields.md` for the exact field shapes, required
keys, and a YAML example for each of the five blocks above.

### `sandboxOptions.writableEnvFiles` — a deliberate, explicit downgrade

- By default, **every environment file mounted inside the workspace is
  read-only at its own path**, even though the rest of the mount is
  writable. This stops an agent editing the very file that decides what
  host lifecycle commands and secret-resolving commands run on your machine
  on the next invocation.
- Set `sandboxOptions.writableEnvFiles: true` only where an agent is
  deliberately meant to edit its own environment file. This is a real
  security downgrade — the plan then reports the file as writable — so
  treat it the same as any other explicit trust decision, not a default.
- **The protection is complete only at a mount's own root.** A file placed
  directly at the root of a read-write mount cannot be reached even by
  renaming, because the sandbox cannot rename the mount point itself. A file
  in a subdirectory of that mount is a different case: it is read-only at
  its current path, but the sandbox can rename the directory holding it
  (which it can write to) and recreate a file at the original path, ending
  up with a sandbox-controlled file there. `sbx env plan` flags this gap for
  a file that is not directly at a mount's root — read the plan's output
  rather than assuming renaming is always harmless.

## Related skills

- For the `sbx create`/`run`/`rm` flag-based workflow this file wraps, use
  `docker-sandboxes-lifecycle`.
- For what `secrets:`/`registries:`/`bindings:` mean at runtime, and for
  configuring network policy independent of any environment file, use
  `docker-sandboxes-network-credentials`.
- For the schema of the kit `spec.yaml` a `kits:` entry (or `agent:`
  pointing at an agent kit) references, use `docker-sandboxes-kits`.

## References

- `references/sources.md` — provenance for every rule above (help captures, source paths, docs URLs).
- `references/env-schema-fields.md` — exact field shapes and YAML examples for `kits:`, `additionalWorkspaces:`, `mcp:`, `ports:`, and `sandboxOptions:`.

## Assets

- `assets/sbxenv.yaml` — a complete, minimal, safe example: a `shell` agent
  mounting the declaring file's own directory, one static env var, and no
  credentials at all — it validates and plans without any onboarding
  authentication.

## Checks

- `checks/verification.md` — Verification runbook for sbxenv.yaml commands (unexecuted runbook; run manually with an isolated, uniquely-named `--app-name`, never with real secret values or untrusted lifecycle commands auto-approved).
