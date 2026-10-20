---
name: floci
description: Run, wire up and troubleshoot Floci, the free local emulators for AWS (floci), GCP (floci-gcp), Azure (floci-az) and OCI (floci-oci), driven by floci-cli, docker run or Docker Compose. Use when the user wants to run cloud code or tests locally, mentions floci, localhost:4566/4577/4588/4599, a LocalStack or Azurite alternative, local S3/DynamoDB/Pub/Sub/Blob/Object Storage, asks for a docker-compose.yml or compose.yaml with a cloud emulator, emulator namespaces, or several emulator instances side by side.
---

# Floci

Floci is a family of local cloud emulators that speak the real cloud wire protocols.
The `floci` command (floci-cli) manages their lifecycle; the native tools (`aws`, `gcloud`,
`az`, `oci`, SDKs, Terraform) do the resource work against the emulator. floci-cli never
creates cloud resources itself.

| Cloud | Emulator | CLI tree | Port | Default container | Reference |
|-------|----------|----------|:----:|-------------------|-----------|
| AWS   | floci     | `floci aws` | 4566 | `floci`     | [references/aws.md](references/aws.md) |
| GCP   | floci-gcp | `floci gcp` | 4588 | `floci-gcp` | [references/gcp.md](references/gcp.md) |
| Azure | floci-az  | `floci az`  | 4577 | `floci-az`  | [references/azure.md](references/azure.md) |
| OCI   | floci-oci | `floci oci` | 4599 | `floci-oci` | [references/oci.md](references/oci.md) |

All paths in this skill (`references/`, `scripts/`, `assets/`) are relative to the directory
that holds this file, not to the user's working directory.

When to read what:

- The cloud's reference, before the first resource command for that cloud.
- [references/docs.md](references/docs.md), before writing code against a service you have not
  used in this session, and whenever an operation looks unsupported. It tells you how to fetch
  the right page of the published documentation.
- [references/docker.md](references/docker.md), when the user wants `docker run`, a
  `docker-compose.yml`, or an app container that talks to the emulator.
- [references/namespaces.md](references/namespaces.md), when running more than one instance,
  sharing a Docker host, or cleaning up containers.
- [references/ci.md](references/ci.md) for pipelines and Testcontainers.
- [references/troubleshooting.md](references/troubleshooting.md) when anything fails.

## Prerequisites (check first)

```sh
command -v floci && floci version     # floci-cli present?
docker info >/dev/null && echo ok     # Docker (or Podman via DOCKER_HOST) reachable?
```

If `floci` is missing, **ask the user before installing software**, then run:

```sh
scripts/install-floci.sh                   # brew if available, else official script into ~/.local/bin
scripts/install-floci.sh --version 0.4.0   # pin a version (uses the install script)
```

- Windows: `iwr https://floci.io/install.ps1 | iex` (per-user, no admin). The helper scripts
  here are bash; on Windows run the `floci` commands they wrap directly.
- No native binary for the platform: download `floci.jar` from the latest release and run
  `java -jar floci.jar` (needs Java 25+).
- Do not use `sudo` or edit shell profiles (`~/.bashrc`, `~/.zshrc`) without asking; if the
  install dir is not on `PATH`, export it for the current session only.
- Updates: `floci update --check` exits 0 when up to date, 1 when an update exists and 2 when
  the check itself failed. Run `floci update` only on exit 1 (Homebrew installs:
  `brew upgrade floci`).
- The user does not want the CLI at all: the emulators are plain container images, see
  [references/docker.md](references/docker.md).

floci-cli does not install Docker. If the daemon is missing, tell the user; do not install
Docker yourself. The native cloud CLIs (`aws`, `gcloud`, `az`, `oci`) are only needed for the
clouds the user works with; suggest installing them, do not install them unasked.

## Hard rules

1. **Never touch real cloud.** Use only the fake credentials the emulators accept
   (`test`/`test` for AWS, the dev identities `floci az setup` and `floci oci setup` create).
   Never read, export or reuse the user's real cloud credentials or profiles.
2. **Verify the endpoint before every mutating command.** It must point at the emulator
   (`localhost`, `127.0.0.1`, `localhost.floci.io`, or a Compose service name). If a command
   might reach public cloud (see each reference's "leaks" section), stop and fix the wiring.
3. **Always name the tree explicitly**: `floci aws start`, not `floci start`. Bare commands
   follow `floci config default-product`, which the user may have changed.
4. **Parse with `-o json`**, never scrape text output. Use `-q` to silence noise in scripts.
5. **Do not remove containers, volumes or snapshots you did not create** in this session.
   Scope any cleanup to a namespace (see namespaces.md) and confirm with the user first.
6. **State is ephemeral** unless the instance was started with `--persist <dir>` or a profile
   with `persistDir`. Both `start` on a stopped container and `restart` remove the container
   and create a new one: `restart` keeps the settings (port, image, services, persist dir,
   namespace) but not in-memory state, and on Azure the new container has a new certificate,
   so `floci az setup` must be run again. `start` on a running container fails. Say so before
   recreating anything.
7. **Never add `-q` to `env`**: it suppresses the exports themselves.
8. **Do not guess what an emulator supports.** Check `floci <tree> services -o json` and the
   published docs ([references/docs.md](references/docs.md)) instead of answering from memory.
9. **With a profile, start and wait before `env`.** Until the profile's container is running,
   `env` and `status` fall back to the default port and describe the default instance. Trust
   `"state": "running"` in `status -o json`, not `reachable`.

## Lifecycle (same for every tree)

```sh
floci <tree> start --detach          # pull if needed, start, return immediately
floci <tree> wait --timeout 2m       # block until healthy (exit 0 = ready)
eval "$(floci <tree> env -o text)"   # export SDK/CLI wiring into this shell
# ... run aws / gcloud / az / oci / tests ...
floci <tree> stop --remove           # when done, only if you started it
```

`-o text` keeps the exports correct even when a profile sets `output: json`. In other shells:
`floci <tree> env --shell fish | source`, or
`floci <tree> env --shell powershell | Invoke-Expression`.

Or use the helper, which starts the container only when none exists, then waits and prints
the exports:

```sh
exports="$(scripts/ensure-running.sh <aws|gcp|az|oci> [profile])" && eval "$exports"
```

Keep the two steps: `eval "$(...)"` in one go succeeds even when the helper fails, and the
commands after it would run with missing or stale wiring. The helper exits 3 without
touching anything when the container exists but is stopped, because starting it replaces
it (rule 6). Tell the user, and re-run with `FLOCI_REPLACE_STOPPED=1` once they agree.

One-time per instance, before using the native CLI:
- Azure: `floci az setup` (trusts the emulator cert, registers an az cloud, logs in).
- OCI: `floci oci setup` (writes a throwaway key and a `[FLOCI]` profile in `~/.oci/config`).

`eval` only affects the current shell. If each tool call runs in a fresh shell, prefix every
command: `eval "$(floci aws env -o text)" && aws s3 ls`.

The examples are written for bash. In zsh (the macOS default) an unquoted variable is not
split into words, so `flags="--profile aws-b"; floci aws status $flags` passes one argument
and fails. Write the flags out, or use an array: `flags=(--profile aws-b)` and
`"${flags[@]}"`.

## Inspecting state

| Need | Command |
|------|---------|
| Is it running and healthy? | `floci <tree> status -o json` |
| Which services are enabled? | `floci <tree> services -o json` (Azure: returns an empty list, see azure.md) |
| CLI and server versions | `floci <tree> version -o json` (Azure: read the version from `status -o json`) |
| Recent server logs | `floci <tree> logs --tail 100` or `--since 5m` |
| Environment problems | `floci <tree> doctor -o json` (an array of checks with `status` `ok`, `warn` or `fail`; see troubleshooting.md before acting on a `fix`) |
| Effective config | `floci <tree> config show --profile <name>` (the namespace row appears only with a profile that yields one) |
| All instances | `floci <tree> config profile list -o json` (profiles are shared by all trees; `image` tells the cloud). Also `config profile show`, `edit` and `delete <name>` |
| Any command's flags | `floci <tree> <command> --help` |

## Several instances

An instance is a profile: its container name is its identity, its port must be unique, and
its Docker resource namespace keeps the containers it launches apart from other instances.
Pass the same `--profile <name>` to every command for that instance. Details and the
namespace derivation rules are in [references/namespaces.md](references/namespaces.md).

```sh
floci aws config profile create aws-b --container floci-b --port 14566 --persist ~/.floci/data/aws-b
floci aws start --profile aws-b          # waits up to 30s; or --detach, then wait
eval "$(floci aws env -o text --profile aws-b)"
```

floci-cli keeps its own files under `~/.floci` (profiles in `~/.floci/profiles/`, per-instance
state in `~/.floci/<product>/<container>/`), so instance data goes there too, as
`~/.floci/data/<name>`.

## Choosing the right integration

- **Ad-hoc commands or a dev server**: the CLI lifecycle above.
- **The user asks for `docker run` or a Compose file, or the app itself runs in a container**:
  [references/docker.md](references/docker.md). Start from the templates in
  `assets/compose/` instead of writing YAML from memory.
- **Integration tests in code**: a Testcontainers module where one exists (AWS in Java, Node,
  Python, Go and .NET; Azure in Java only; none for GCP or OCI, see ci.md). Otherwise start
  the emulator with the CLI or Compose before the tests.

## When something is not supported

Coverage differs per service: some are full engines, some are in-process, some answer with
canned responses. Before writing code against a service, check that it is enabled
(`floci <tree> services -o json`) and read its page in the published docs
([references/docs.md](references/docs.md)). If an operation is missing, say so plainly,
suggest a workaround, and point the user to the emulator's issue tracker
(`https://github.com/floci-io/<floci|floci-gcp|floci-az|floci-oci>/issues`) instead of
retrying variations.
