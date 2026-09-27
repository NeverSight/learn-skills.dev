---
name: docker-sandboxes-kits
description: >-
  Use this skill when authoring, validating, packaging, signing, or composing a Docker Sandboxes kit `spec.yaml` (`sbx kit add/inspect/pack/pull/push/sign/validate/verify`), even if the user just says they want to "add a tool to a sandbox agent", "build a reusable sandbox extension", "publish a kit to a registry", or "give a mixin its own credentials and network access". Covers the kit-spec v2 grammar (`kind: sandbox` vs `kind: mixin`, the `sandbox:` block, `permissions.network`, `ports`, `credentials` apiKey/oauth, `environment`, `setup` install/startup/files, `volumes`, `args`, `extends`, `mixins`, `requires.agent`), composition via `--kit`/`sbx kit add`, and distribution (pack/push/pull/sign/verify/provenance).
license: Apache-2.0
compatibility: Requires standalone sbx with sbx kit support and kit-spec schemaVersion "2", not the legacy docker sandbox wrapper. Verified against docker/sandboxes df5c96ba60484fa2c375469dbac912c205da6c37; installed-help version and provenance are in references/sources.md. docker_help does not cover standalone sbx.
---

# Docker Sandboxes: Kits (spec.yaml)

## Overview

A **kit** is a directory (or ZIP/OCI/git artifact) containing a `spec.yaml`
plus an optional `files/` tree. `sbx` composes a kit into a running or
about-to-be-created sandbox at `sbx create`/`sbx run --kit`/`sbx env` time or
at `sbx kit add` time. This skill owns kit-spec v2 authoring, validation, and
distribution — everything under `spec.yaml`'s own grammar — and defers what a
kit's declarations *mean at runtime* (credential injection, network
enforcement) to `docker-sandboxes-network-credentials`, and the sandboxes a
kit is composed into to `docker-sandboxes-lifecycle`.

## When to use this skill

Activate this skill when:
- The user wants to write, validate, or pack a `spec.yaml` for a `kind:
  sandbox` (complete agent) or `kind: mixin` (extension) kit.
- The user wants a mixin to add a tool, credential, network allowance, or
  files to an existing built-in agent.
- The user wants to publish a kit to (or pull one from) an OCI registry,
  sign it, or verify a signature/provenance attestation.
- The user is debugging a kit-validation error, an argument-substitution
  error, or `sbx kit add`'s recreate-aware requirement.

## Do not use this skill when

Do not use this skill when:
- The task is creating/running/removing the sandbox a kit is composed into,
  independent of the kit's own content — use `docker-sandboxes-lifecycle`.
- The task is what a credential or network rule a kit declares actually
  does at runtime (proxy injection, allow/deny precedence, or what the
  CURRENT network/global policy already permits), or is about secrets/
  policy that have nothing to do with a kit — use
  `docker-sandboxes-network-credentials`.
- The task is the `sbxenv.yaml` file format that references kits via its
  own `kits:` block — use `docker-sandboxes-env` for that file's schema
  (this skill still owns what goes inside the referenced kit itself).

## Core guidance

### `kind: sandbox` vs `kind: mixin` — pick the right one

- Exactly one `kind: sandbox` kit composes into any sandbox (a complete
  agent: base image + launch config). Any number of `kind: mixin` kits
  layer onto it (tools, credentials, network, files). A mixin **must not**
  declare a `sandbox:` block, `extends:`, or `mixins:`.
- Every kit needs `schemaVersion: "2"` (the current clean grammar — no
  legacy shims), `kind`, and `name` matching
  `^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$`. **Decoding is strict**: any
  unrecognized field anywhere is a hard error (e.g. a typo like
  `permissions.netwrok:`), so a kit that validates has no silent typos.
  ```yaml
  schemaVersion: "2"
  kind: mixin
  name: extra-egress
  ```
- Do not redefine a base agent's credential in a mixin: declaring a new
  `apiKey.name` or `proxyManaged` for the same service fails composition.
  `shell`, `docker-agent`, and `opencode` already own `github`. An additive
  routing-only entry (`apiKey.inject`, no name/proxyManaged/oauth, and
  `required: false`) can extend the base credential instead. OAuth belongs
  on sandbox kits, never mixins. See `references/spec-v2-fields.md`.
  Inspect built-in definitions at `sandboxlib/agentkits/agents/<agent>/spec.yaml`
  in the pinned source; `sbx kit inspect` takes artifact references, not
  built-in names. Standalone mixin validation does not test composition.

### The `sandbox:` block (sandbox kits only)

- **Required** for `kind: sandbox` (unless the kit `extends:` a parent that
  already supplies it); **forbidden** for `kind: mixin`.
- `image:` is the pre-built base image. `entrypoint:` is the fixed process
  prefix (`entrypoint[0]` is the binary); `command:` is the mode-specific
  argument tail — either a bare list (sets `default`, `interactive` falls
  back to it) or `{default: [...], interactive: [...]}`.
  For a complete minimal kit, use `assets/spec-sandbox.yaml`, which inherits
  the embedded shell definition rather than inventing an image or command.
- `sandbox.build:` (Dockerfile build) is **accepted but not built by the
  runtime this release** — a kit that sets `build:` must still set `image:`,
  or it is rejected at load with an actionable error.
- **`extends:` (below) is the simplest way to get a real, working image
  without inventing one.** A sandbox kit that extends a built-in agent
  (e.g. `extends: shell`) inherits that agent's real `sandbox.image` and
  may omit `sandbox:` entirely — see the minimal example asset, which does
  exactly this rather than naming a made-up image reference.

### Egress: `permissions.network` — and the all-egress-declared rule

- `permissions.network.allow`/`deny` are the v2 home for what v1 spelled as
  top-level `network:`. Enforced shapes include exact host, exact host+port,
  single-label wildcards (`*.example.com`), multi-label wildcards
  (`**.example.com`), and CIDR prefixes. Port ranges are not supported by
  the runtime matcher; use separate exact ports.
  **Deny wins within domain rules or within CIDR rules.** A decisive domain
  decision is evaluated before CIDR rules: an allowed hostname is not
  checked against a CIDR deny for its resolved IP. Do not rely on a CIDR
  deny alone to block an already-allowed hostname.
  ```yaml
  permissions:
    network:
      allow:
        - registry.npmjs.org
      deny:
        - telemetry.example.com
  ```
- **`permissions.network.allow` is additive across a composition, and a
  kit's own allow list is not the only thing granting a sandbox egress.**
  The sandbox already carries the base agent's own allow list, plus
  whatever the *global* or *per-sandbox* network policy (`sbx policy`,
  independently of any kit) permits — see `docker-sandboxes-network-
  credentials`. **Removing a host from one kit's `allow` list does not by
  itself prove that host is blocked** — the global policy defaults
  (`balanced` allows common package registries and AI services; `allow-all`
  allows everything) or another composed kit may still permit it. Never
  claim a host is blocked without checking the actual effective decision
  with `sbx policy check network --sandbox <name> <host>` on a real
  sandbox.
- Declare the egress a kit requires explicitly for reproducibility. Credential
  injection does not itself grant network access. Omitting an allow entry
  leaves reachability dependent on the existing global/per-sandbox policy;
  it does not necessarily block the host. Check the effective decision.

### `credentials` — what the kit needs, never how the user stores it

- Each entry declares a `service` identity and **where to inject** the
  resolved value (`apiKey` and/or `oauth`); it never declares *how* the
  user obtains or stores the credential — that lives in the user's own
  bindings file, wired through `sbx secret set` (see
  `docker-sandboxes-network-credentials`).
- `apiKey.inject[]` needs a `domain` and either an explicit `header`+
  `format` (`format` must contain exactly one `%s`) or the `scheme:`
  sugar: `scheme: bearer` expands to `Authorization: Bearer %s` (no
  `username`), `scheme: basic` requires `username` and is mutually
  exclusive with `format`. **Pick a `service` name no composed base agent
  already declares** (see the duplicate-service rule above) — see
  `references/spec-v2-fields.md` for a complete fragment.
- `apiKey.proxyManaged: true` sets the in-container env var to the literal
  `proxy-managed` sentinel rather than leaving it unset; the real value is
  substituted only by the proxy, on the allow-listed inject domains.
- `oauth` needs `tokenEndpoint.host`/`.path` and, unless
  `passthrough: true`, non-empty `sentinels.accessToken`/`.refreshToken`.
  `passthrough: true` is a **security downgrade** — the real token reaches
  the container instead of a sentinel — use it only when the kit's own
  design requires it and say so in `description`.

### `setup` — install (once) vs. startup (every start) vs. files (startup-time writes)

| Block | Command shape | Runs |
|---|---|---|
| `setup.install[].command` | **string**, via `sh -c` | Once, synchronously, before the agent first launches. Runs for every kit, built-in or not. |
| `setup.startup[].command` | **list<string>**, exec-style (no shell) | On **every** container start (create, stop/start, daemon restart, host reboot) — **must be idempotent**. |
| `setup.files[]` | file write via shell exec | At container startup; `path` absolute; only `${WORKDIR}` placeholder allowed in `content`. |

Optional fragment for the shell kit in `assets/spec-sandbox.yaml`:
```yaml
setup:
  startup:
    - command: ["sh", "-c", "mkdir -p ~/.my-kit"]
  files:
    - path: /home/agent/.my-kit/config.json
      content: '{"workdir": "${WORKDIR}"}'
```
- **`setup.files` is not the same mechanism as the `files/` directory
  tree (below).** `setup.files` entries are dynamic, `${WORKDIR}`-
  substituted writes performed at startup time; the `files/home/` and
  `files/workspace/` directory tree is a set of **static** files packed
  alongside `spec.yaml` and copied in at container-create time, and it is
  specifically the `files/workspace/` half of that tree — not
  `setup.files` — that is written **after** the workspace is populated
  (e.g. after an in-container `git clone` under `--clone`). Do not
  conflate the two: `setup.files` has no "after workspace population"
  timing guarantee of its own.
- All three `setup:` lists **concatenate in `--kit` order** across composed
  kits.
- Default execution users: install as root (`user: "0"`) unless overridden;
  startup/entrypoint as the agent user (uid `1000`) unless overridden.
  Root install steps writing under `/home/agent` **must** `chown` it back to
  `agent:agent`, or later agent-user writes there fail.

### `volumes` — creation-time only, every volume must set a size

- Each entry needs an absolute `path:`, optional `type: tmpfs` (RAM-backed;
  omit/`""` for the default block-backed volume), optional `size:`
  (byte-size string) and `mode:` (octal).
- **Volumes apply only at sandbox-create time** — `sbx kit add` (runtime
  injection) skips volume changes entirely; a kit that needs one must be
  present at creation.
- **Always set `size:` on a block volume.** An unsized volume inherits a
  50 GiB default and costs real host disk immediately (ext4 inode-table
  zeroing); 512 MiB is the practical floor — below it `mke2fs` switches
  inode density and the space savings mostly disappear.

### `args` — parameterizing a kit

- Declare under top-level `args:` (v2 only — the frozen v1 grammar has no
  `args` block), each with exactly one of `default`/`required: true`, plus
  optional `description`/`enum`/`pattern`. Reference with
  `${{ kit.args.NAME }}` anywhere in `spec.yaml` or `files/`; substitution
  happens **before** the spec is decoded. Every reference **must** be
  declared, or loading fails — that is what makes the block a trustworthy
  list of a kit's inputs. **Quote a placeholder used in a string field**
  (`VERSION: "${{ kit.args.version }}"`), or an unquoted numeric-looking
  value decodes as a number and fails to decode into a string field.
- Supply values with `--kit-arg name=value` (every kit) or
  `--kit-arg kitname.name=value` (one kit only), or `--kit-args-file`.
  **Never pass a secret this way** — `--kit-arg` values are not masked; see
  `docker-sandboxes-network-credentials`.

### `extends` and `mixins` — composition, not runtime injection

- `extends:` resolves only built-in agent names at this pinned release
  (`shell`, `claude`, etc.). Remote git/OCI parents fail to resolve, even
  if pinned; the broader format specification is not an implementation
  guarantee. The minimal asset uses the supported `extends: shell`.
- `mixins:` is accepted with a warning but is not applied by this runtime.
  Use `--kit` or `sbx kit add` for composition. The format's immutable-ref
  requirements do not make unimplemented remote inheritance work.
- Prefer digest/commit-pinned CLI kit references for reproducibility.
  `--kit` and `sbx kit add` still accept mutable tags/branches; the CLI
  parser does not enforce this recommendation.
- `requires.agent` (mixin-only; **rejected** on `kind: sandbox`) pins the
  single base agent a mixin is designed for (e.g. Claude-specific env
  vars). It is well-formedness-checked by the spec library; the actual
  agent-affinity mismatch is enforced by the composition consumer, not by
  `sbx kit validate` alone.

### Validating, packaging, and distributing

| Command | Purpose |
|---|---|
| `sbx kit validate REFERENCE [--kit-arg ...]` | Local directory, ZIP, or git reference; OCI is rejected. Schema-only well-formedness check. **Never composes against a base agent** — cannot catch a duplicate-service credential collision or confirm any domain is reachable at runtime. |
| `sbx kit inspect REFERENCE [--kit-arg ...] [--json]` | Loads and prints the decoded artifact before composing it, including `--kit-arg` substitution preview. |
| `sbx kit pack DIRECTORY [-o OUTPUT.zip]` | Packages a validated directory as a ZIP. |
| `sbx kit pull REFERENCE [-o OUTPUT]` | Pulls a kit's raw layer payload from an OCI registry without composing it. |
| `sbx kit push DIRECTORY REGISTRY/REPO:TAG [--sign]` | Packages and pushes; every push attaches an unsigned-by-default SLSA provenance attestation. |
| `sbx kit provenance REFERENCE [--certificate-identity ...]` | Prints the attestation `push` attached; marked UNSIGNED unless verified against a matching key/identity. |
| `sbx kit sign REFERENCE` / `sbx kit verify REFERENCE` | Sigstore sign/verify (keyless by default); prefer `--identity-token-file` over `--identity-token`. |
| `sbx kit add SANDBOX REFERENCE [--kit-arg ...]` | Injects a **mixin only** into an existing sandbox at runtime (recreate-aware label required); container-immutable settings (`security.privileged`, `volumes:`) cannot take effect this way. |

See `references/kit-distribution-commands.md` for full flag lists and
worked examples of each command above.

## Related skills

- For the sandboxes a kit is composed into (`sbx create`/`run --kit`,
  `sbx kit add SANDBOX`), use `docker-sandboxes-lifecycle`.
- For what a kit's `credentials:`/`permissions.network:` declarations mean
  at runtime — proxy injection, allow/deny precedence, the effective
  policy a sandbox actually has once global/per-sandbox policy is
  included, where the user stores the actual secret value — use
  `docker-sandboxes-network-credentials`.
- For the `sbxenv.yaml` file whose `kits:`/`agent:` fields reference a kit
  by this schema, use `docker-sandboxes-env`.

## References

- `references/sources.md` — provenance for every rule above (spec package, SPEC-v2.md, help captures, docs URLs).
- `references/spec-v2-fields.md` — the complete v2 field table (common fields, sandbox-only fields, mixin-only fields, shared blocks) for lookup without re-reading the full spec.
- `references/kit-distribution-commands.md` — full flags and worked examples for `sbx kit validate/inspect/pack/pull/push/provenance/sign/verify/add`.

## Assets

- `assets/spec-sandbox.yaml` — a genuine minimal `kind: sandbox` kit that
  `extends: shell` to inherit a real, working image rather than inventing
  one.
- `assets/spec-mixin.yaml` — a genuine minimal `kind: mixin` kit with no
  credentials at all (an egress-only extension), which composes cleanly
  with every built-in agent.

## Checks

- `checks/verification.md` — Schema, composition, egress, and kit-add checks (unexecuted integration runbook; isolated `--app-name`, no registry publishing or signing).
