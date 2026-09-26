---
name: docker-sandboxes-lifecycle
description: Use this skill when creating, running, reattaching to, listing, stopping, or removing Docker Sandboxes (the standalone `sbx` CLI that runs AI coding agents in isolated microVMs), even if the user just says they want to "run claude in a sandbox", "isolate an agent from my repo", "give an agent its own git clone", or "clean up old sandboxes". Covers `sbx run`/`sbx create` (including the built-in agents claude, codex, cursor, devin, docker-agent, gemini, opencode, shell), workspace bind-mount vs `--clone` isolation, additional read-only workspaces, reattaching by `--name`, `sbx ls`/`stop`/`rm`/`prune`, `sbx exec`, `sbx cp`, and `sbx ports`.
license: Apache-2.0
compatibility: Standalone `sbx` CLI (not the legacy `docker sandbox` plugin wrapper). Source-verified against docker/sandboxes (github.com/docker/sandboxes) @ commit df5c96ba60484fa2c375469dbac912c205da6c37. Cross-checked against an installed sbx v0.42.0-503-g951b7f6d7 (commit 951b7f6d7f6bb260fac15077b607109ffe8ae012, older than the pinned source); one source-only behavior change is called out explicitly below (`sbx prune --filter`). `docker_help` does not cover standalone `sbx` syntax.
---

# Docker Sandboxes: Local Lifecycle & Workspace Isolation

## Overview

Docker Sandboxes (`sbx`) runs an AI coding agent inside an isolated microVM with
its own filesystem, network, and Docker daemon. This skill owns the local
sandbox lifecycle — creating, reattaching to, listing, stopping, and removing
sandboxes — and the workspace isolation choice (direct bind mount vs.
`--clone`). It does not cover network policy, credentials, `sbxenv.yaml`, or
kit authoring — see Related skills.

## When to use this skill

Activate this skill when:
- The user wants to start, reattach to, stop, or remove a local `sbx` sandbox.
- The user wants an agent to work on a repository without giving it a
  writable bind mount of the host working tree (`--clone`).
- The user wants extra read-only (or write-restricted) workspaces mounted
  alongside the primary one.
- The user is copying files between host and sandbox, publishing a sandbox
  port, or running an ad-hoc command inside a sandbox (`sbx exec`).
- The user wants to clean up stopped sandboxes (`sbx prune`) or remove a
  specific one (`sbx rm`), with the destructive consequences understood.

## Do not use this skill when

Do not use this skill when:
- The task is running `docker agent run --sandbox` or managing its
  `docker agent sandbox` allowlist — use `docker-agent-run`. If the CLI
  is unclear, establish whether the user runs Docker Agent or standalone
  `sbx` before choosing commands.
- The task is about what a sandbox can reach on the network or which
  credentials it uses — use `docker-sandboxes-network-credentials`.
- The task is authoring or running a declarative `sbxenv.yaml` file — use
  `docker-sandboxes-env`.
- The task is authoring, packaging, signing, or composing a kit `spec.yaml`
  — use `docker-sandboxes-kits`.
- The task is about `sbx --cloud` (Docker Cloud Sandboxes) — out of scope for
  this skill set, which covers the local daemon only.

## Core guidance

### Creating vs. running

- Use `sbx run AGENT [PATH...]` to create-if-needed **and** attach in one
  step. Use `sbx create AGENT [PATH...]` to create without attaching, then
  `sbx run --name SANDBOX` to attach later. Pass `--detached`/`-d` to `sbx run`
  to print the sandbox ID and exit without an interactive session.
  ```bash
  sbx run shell                  # create (if needed) and attach, cwd mounted
  sbx create shell .             # create only, cwd mounted, do not attach
  sbx run --name my-sandbox       # reattach later
  ```
- `AGENT` is a built-in name (`claude`, `codex`, `cursor`, `devin`,
  `docker-agent`, `gemini`, `opencode`, `shell`) or a sandbox kit reference
  (local directory, ZIP, git, or OCI). A relative local kit reference MUST be
  an explicit path (`./my-kit`, a parent-relative `.zip` path) — a bare `my-kit` is read as
  an agent/sandbox name, never a directory beside the cwd.
- **Omitting the path is not the same for every subcommand.** `sbx run claude`
  with no path mounts the **current directory**. `sbx create claude` with no
  path mounts **nothing at all** — the agent then works only in the
  container's own filesystem. Always pass a path explicitly with `sbx create`
  if you intend to give the agent a workspace.
- **Prefer `--name` to reattach; a bare positional name still works but is
  deprecated.** `sbx run --name NAME` (agent positional optional, read from
  the sandbox's own spec) is the recommended form. A bare `sbx run NAME` —
  a positional that is neither a known agent nor an explicit kit reference —
  is still **accepted** as a legacy re-attach shorthand, but prints a
  deprecation warning ("`sbx run NAME` is deprecated; use
  `sbx run --name NAME` instead") and may be removed in a future release.
  Always write `--name` explicitly rather than relying on the legacy form.
  ```bash
  sbx run --name existing-sandbox                 # reattach, agent read from spec
  sbx run claude --name existing-sandbox          # reattach, verify expected agent
  ```

### Workspace isolation: bind mount vs. `--clone`

- **Default (bind mount):** the workspace path is mounted read/write inside
  the sandbox at the same path as on the host. The agent can write directly
  to your working tree.
- **`--clone` (creation-time only):** the agent runs against a private
  in-container clone of the host Git repository. The host repo is mounted
  **read-only**; the agent's commits land in the in-container clone and are
  reachable from the host via a `sandbox-<name>` git remote — fetch or pull
  from it to bring commits back.
  ```bash
  sbx create --clone --name demo claude .
  # on the host, later:
  git fetch sandbox-demo
  ```
- **`--clone` has real preconditions, checked at creation time**, and fails
  loudly if any is unmet:
  - an explicit `PATH` must be given (there must be a workspace to clone
    from);
  - that path must be inside a Git repository;
  - it must NOT be a Git worktree (the in-container clone cannot follow a
    worktree's `.git` pointer out to a common dir elsewhere);
  - its `.git` must be a real directory, not a file (a submodule or a
    `--separate-git-dir` setup points `.git` elsewhere, which the read-only
    source mount would not include).
- **`--clone` on `sbx run` when reattaching is a no-op ONLY on a sandbox
  already created in clone mode** — it re-validates nothing new and simply
  keeps running the existing in-container clone. Passing `--clone` while
  reattaching to a sandbox that was created **without** it (a plain
  bind-mounted sandbox) is **not** a silent no-op: it fails with an error
  telling you to recreate the sandbox with `sbx create --clone ...`. Neither
  form can convert an existing sandbox's mode after creation.
- **Removing or pruning a clone-mode sandbox permanently discards every
  commit the agent made that was never fetched back to the host** — the
  in-container clone lives on the sandbox's own filesystem and is deleted
  with it. Before removing a clone-mode sandbox, fetch its work first:
  ```bash
  git fetch sandbox-demo
  ```
  Fetching populates two refspecs: the ordinary `refs/remotes/sandbox-demo/*`
  (deleted along with the remote when the sandbox is removed) and a survivor
  copy at `refs/sandboxes/demo/*` (outside the remote namespace, so it is
  **not** deleted when the remote goes). Recover a branch from the survivor
  copy after removal with:
  ```bash
  git branch <local-name> refs/sandboxes/demo/<branch>
  ```
  `sbx rm`/`sbx prune` print this warning automatically for any clone-mode
  sandbox they are about to remove; read it before confirming, don't
  suppress it with `--force` out of habit.
- Additional workspaces are extra positional paths after the first. Append
  `:ro` to mount one read-only. **`:ro` blocks writes, not reads** — the
  sandbox can still read every file under a `:ro` mount; it is not a way to
  hide sensitive content, only to stop the sandbox from modifying it. A
  read-only argument may name a single file rather than a directory, holding
  just that one path out of reach for writes inside a workspace the sandbox
  can otherwise write.
  ```bash
  sbx run claude . /path/to/docs:ro
  ```
  **Never mount a secrets/credentials file this way** (`:ro` or otherwise) —
  a read-only mount still lets the sandbox (and, through it, the proxy-less
  agent process) read the secret in the clear. Use the credential store
  instead; see `docker-sandboxes-network-credentials`.

### Reattaching, stopping, and removing

- `sbx ls` lists sandboxes with agent, status, published ports, and
  workspace (`--json`, `-q`/`--quiet` for scripting).
- `sbx stop SANDBOX [SANDBOX...]` stops without removing; state is retained
  and the sandbox restarts with `sbx run --name`.
- `sbx rm [SANDBOX...] [--all] [--force]` removes sandboxes, their
  containers, Git worktrees, state, and sandbox-scoped secrets. **This
  cannot be undone**, and for a clone-mode sandbox it discards every
  unfetched commit (see above). Only use `--force` when you have already
  reviewed what will be destroyed and consented — for scripted teardown of
  resources this session itself created and uniquely named, not as a
  default habit.
- `sbx prune [--dry-run] [--filter until=VALUE] [--force]` removes only
  **stopped** sandboxes — a running sandbox is never touched — but this is
  still a destructive, irreversible bulk removal: every matching stopped
  sandbox's state, secrets, and (for clone-mode sandboxes) any unfetched
  commits are gone. Always preview with `--dry-run` first and read the
  clone-commit warning it prints before removing for real; do not pass
  `--force` as a default.
  - **Current source flag is `--filter until=VALUE`**, not `since=`. `VALUE`
    may be an RFC 3339 timestamp, a Unix timestamp, or a Go duration
    relative to now (e.g. `until=168h` keeps anything stopped within the
    last week — i.e. prunes what stopped *before* that point). **This is a
    source-only behavior at the pinned commit that differs from some
    installed builds**: an older installed `sbx` may still advertise
    `--filter since=DURATION` as a legacy alias; prefer `until=` and treat
    `since=` as legacy-only if your installed `--help` output does not show
    `until=`.
  ```bash
  sbx prune --dry-run --filter until=168h
  # after reviewing the dry-run output and any clone-commit warnings:
  sbx prune --filter until=168h
  ```

### Copying files and running ad-hoc commands

- `sbx cp SRC DST` copies between host and sandbox; exactly one side must be
  `SANDBOX:PATH`. Copying between two sandboxes is not supported.
  ```bash
  sbx cp ./config.json my-sandbox:/home/agent/
  sbx cp my-sandbox:/home/agent/output.log ./
  ```
- `sbx exec [flags] SANDBOX COMMAND [ARG...]` runs a command in a sandbox
  (starting it first if stopped); flags mirror `docker exec` (`-it`, `-d`,
  `-u`, `-w`, `-e`, `--env-file`, `--privileged`).
  ```bash
  sbx exec -it my-sandbox bash
  sbx exec -u root my-sandbox apt-get update
  ```
- `sbx ports SANDBOX [--publish SPEC] [--unpublish SPEC]` manages published
  ports after creation; `-p/--publish` on `sbx create`/`sbx run` only takes
  effect when the sandbox is created, not on reattach.

### Sizing and naming

- `--cpus` (0 = auto: all host CPUs) and `--memory`/`-m` (default 50% of
  host memory, clamped 512 MiB–32 GiB) are create-time-only knobs.
- `--name` sets the sandbox name (default `<agent>-<workdir>`); at least two
  characters, starting with a letter or number, letters/numbers/hyphens/
  periods only, at most 63 ASCII characters, ending in a letter or number;
  `default` is reserved.

## Related skills

- For `docker agent run --sandbox` and `docker agent sandbox` commands,
  use `docker-agent-run`.

- For network egress policy and service/registry credentials, use
  `docker-sandboxes-network-credentials`.
- For declarative, checked-in `sbxenv.yaml` environments that wrap this same
  create/run/rm lifecycle, use `docker-sandboxes-env`.
- For authoring or composing the kit `spec.yaml` an `AGENT` reference can
  point to, use `docker-sandboxes-kits`.

## References

- `references/sources.md` — provenance for every rule above (help captures, source paths, docs URLs).

## Assets

- None.

## Checks

- `checks/verification.md` — Verification runbook for sandbox lifecycle commands (unexecuted runbook; run manually with an isolated `--app-name`, never with `--force` except consented cleanup of the runbook's own uniquely-named test sandboxes).
