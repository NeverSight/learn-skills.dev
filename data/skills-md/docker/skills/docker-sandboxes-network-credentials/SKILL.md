---
name: docker-sandboxes-network-credentials
description: Use this skill when configuring what a Docker Sandboxes (`sbx`) sandbox can reach on the network or which credentials it authenticates with, even if the user just says they want to "let the agent call an internal API", "block all network access", "give the agent a GitHub token", or "use a private registry image for a sandbox". Covers `sbx policy init/allow/deny/ls/inspect/log/check/rm network` (global and per-sandbox egress rules, deny-over-allow precedence) and `sbx secret set/set-custom/ls/rm/import` (service secrets, dynamic secrets via --ref/--command, and registry pull credentials with their host-pulls-only-by-default injection scope).
license: Apache-2.0
compatibility: Standalone `sbx` CLI (not the legacy `docker sandbox` plugin wrapper). Source-verified against repository docker/sandboxes (github.com/docker/sandboxes) @ commit df5c96ba60484fa2c375469dbac912c205da6c37. Cross-checked against an installed sbx v0.42.0-503-g951b7f6d7 (commit 951b7f6d7f6bb260fac15077b607109ffe8ae012, older than the pinned source); no source-only differences were found for the commands this skill covers. `docker_help` does not cover standalone `sbx` syntax.
---

# Docker Sandboxes: Network Policy & Credentials

## Overview

This skill owns `sbx policy` (network egress) and `sbx secret` (service
secrets and registry credentials). The proxy enforces egress policy and
injects stored credentials on matching domains. Proxy-managed sentinels are
not usable upstream credentials, but OAuth passthrough can expose real
tokens to the sandbox. Egress policy does not protect a real credential
once leaked outside the sandbox; revoke or rotate a leaked credential.

## When to use this skill

Activate this skill when:
- The user wants to allow, deny, or inspect which hosts a sandbox (or all
  sandboxes) can reach.
- The user wants to give an agent an API key, OAuth token, or other service
  credential without exposing the raw value inside the sandbox.
- The user wants to pull a private template image or kit from a registry
  that requires authentication.
- The user is debugging a blocked network request or a credential that
  isn't being injected.

## Do not use this skill when

Do not use this skill when:
- The task is running `docker agent run --sandbox` or managing its
  `docker agent sandbox` allowlist — use `docker-agent-run`. If the CLI
  is unclear, establish whether the user runs Docker Agent or standalone
  `sbx` before choosing commands.
- The task is creating, reattaching to, or removing a sandbox itself — use
  `docker-sandboxes-lifecycle`.
- The task is declaring secrets/registries/bindings inside a checked-in
  `sbxenv.yaml` file — use `docker-sandboxes-env` for the file format (this
  skill's rules on precedence and injection scope still apply to what that
  file provisions).
- The task is declaring a kit's own `credentials:`/`permissions.network:`
  block in a `spec.yaml` — use `docker-sandboxes-kits` for the schema (this
  skill's model of what those declarations mean at runtime still applies).

## Core guidance

### Network policy: global, per-sandbox, and precedence

- The global network policy must be initialized once before creating the
  first sandbox: `sbx policy init <allow-all|balanced|deny-all>`. `balanced`
  is the recommended starting point (typical dev traffic — AI services,
  package registries — allowed). This is a one-time setup.
- **`sbx policy reset` is destructive: it deletes the entire local policy
  store and stops the daemon and every currently running sandbox.** The
  daemon restarts on the next daemon-backed command. It is not a lightweight way to "start over" or a
  routine diagnostic step — never propose it as a first troubleshooting
  move for a single misbehaving rule. Use targeted `sbx policy rm network`
  (by `--id` or `--resource`) to remove one rule instead; reserve
  `sbx policy reset` for when the policy store itself needs to be rebuilt
  from scratch, and warn the user that it will stop running sandboxes
  before running it.
- Add rules with `sbx policy allow network RESOURCES` /
  `sbx policy deny network RESOURCES`. `RESOURCES` is a comma-separated list
  of exact hosts, `*.example.com` single-label wildcards, `**.example.com`
  multi-label wildcards, optional `:port` suffixes, CIDR prefixes, or `**`
  for "all hosts".
  ```bash
  sbx policy init balanced
  sbx policy allow network "api.example.com,cdn.example.com"
  sbx policy deny network ads.example.com
  ```
- **Deny always wins over allow** for the same hostname/CIDR when both
  match. An allowed hostname is not checked against CIDR deny rules for its
  resolved IP.
- A rule applies globally by default. Pass `--sandbox NAME` to scope it to
  one sandbox's local policy instead:
  ```bash
  sbx policy allow network --sandbox my-sandbox api.example.com
  ```
- At **creation time only**, `sbx create`/`sbx run` accept
  `--deny-network RESOURCE` (repeatable) to add a per-sandbox deny rule. This
  is safe to expose even under centralized (org) governance because a local
  deny can only narrow, never widen, egress — it can never override an
  org-level allow into a broader grant.
- Use `sbx policy check network [--sandbox NAME] TARGET` to test what the
  **current** policy would do for a host/URL before it matters, and
  `sbx policy log [SANDBOX]` to see what was actually allowed or blocked
  historically, with the matching rule.
  ```bash
  sbx policy check network --sandbox my-sandbox api.example.com:443
  sbx policy log my-sandbox --json
  ```
- `sbx policy ls [SANDBOX] [--wide]` lists active policies/rules; `--wide`
  adds rule IDs (needed for `sbx policy rm network --id`) and per-resource
  status. `sbx policy inspect <policy-or-rule>` gives full detail including
  each rule's exact removal command or the reason it is read-only (e.g.
  org-managed). To remove a sandbox-scoped rule, retain `--sandbox NAME`;
  omitting it targets the global policy instead:
  ```bash
  sbx policy rm network --sandbox my-sandbox --resource api.example.com
  sbx policy check network --sandbox my-sandbox api.example.com
  ```
  Removing one rule does not determine the final decision; other matching
  rules still apply.

### Service secrets: how injection works

- `sbx secret set [SERVICE]` stores a credential the **proxy** uses to
  authenticate outbound requests on behalf of the agent. In the normal
  proxy-managed flow, the sandbox sees a sentinel rather than the raw
  secret; the proxy substitutes the real value on requests to the domains
  the matching kit/binding declares.
  ```bash
  sbx secret set github                       # interactive
  printf '%s' "$ANTHROPIC_API_KEY" | sbx secret set anthropic
  ```
  **Storing a secret does not grant network access.** Egress is governed
  separately by `sbx policy`; check the target domain in the intended scope
  before debugging authentication:
  ```bash
  sbx policy check network --sandbox my-sandbox api.anthropic.com
  ```
- **OAuth passthrough is an exception, not a no-secret-exposure guarantee.**
  When a kit sets `oauth.passthrough: true` without a refresh sentinel, the
  proxy forwards the real token response to the sandbox. The built-in
  `devin` kit uses this mode. Review the agent's credential configuration
  before promising that it cannot read a token; do not enable passthrough
  merely to bypass an authentication failure. Even with sentinels, the
  agent can exercise the credential's permissions on allowed services —
  restrict token privileges as well as network access.
- Service secrets are global by default; `--sandbox NAME` scopes one to a
  single sandbox.
- **Dynamic secrets** resolve the value on the host at use time instead of
  storing it directly: `--ref` (1Password `op://...` or an AWS Secrets
  Manager ARN — requires an authenticated `op`/`aws` CLI) or `--command`
  (runs a shell command and uses its stdout). `--refresh` controls the
  resolution/cache policy (default `55m`, or `on-demand`).
  ```bash
  sbx secret set anthropic --ref 'op://Private/Anthropic/api-key'
  sbx secret set github --command 'gh auth token'
  ```
  **`--command` and `--ref` are resolved on the host, with your own
  privileges, and treated as trusted execution** — never point `--command`
  at anything an untrusted file or an agent's own output could influence.
- **Never pass a secret as a plain `--env` value or as a `--kit-arg` /
  `--env-arg` value.** Both land as literal, unmasked text — in the
  sandbox's environment, in `sbx env plan`'s state file, and potentially in
  shell history — defeating the entire point of the credential store. Use
  `sbx secret set` (or `sbxenv.yaml`'s `secrets:`/`registries:` blocks, which
  route through the same store) instead.
- `sbx secret set-custom` (experimental) covers a service sbx has no
  built-in support for: the sandbox sees a placeholder value in an env var
  you name (`--env`), and the proxy swaps in the real secret only on
  requests to the `--host` pattern(s) you declare.
- `sbx secret ls [--global|--sandbox NAME] [--service NAME] [--json]` lists
  what is stored, without revealing values. `sbx secret rm [SERVICE]
  [--sandbox NAME] [--all|--registry HOST] [--force]` removes it.
- `sbx secret import [SERVICE] [--all] [--dry-run] [--force]` offers to
  import secrets already sitting in host environment variables (e.g.
  `OPENAI_API_KEY`, `GH_TOKEN`) into the global store, prompting per entry
  unless `--all`/`--force`. A service with an OAuth token already configured
  is skipped — OAuth takes precedence at runtime over an imported API key.

### Registry credentials: host-pulls-only by default, two distinct injection scopes

- `sbx secret set --registry HOST --password-stdin` (optionally
  `--username`) stores **pull** credentials for a container registry, used
  to pull private template images and kit artifacts. **Unlike service
  secrets, registry credentials are host-only by default: they authenticate
  pulls on the host and are never injected into any sandbox.**
  ```bash
  gh auth token | sbx secret set --registry ghcr.io --password-stdin
  ```
- **`--all-sandboxes` and `--sandbox` widen this differently — do not
  confuse them:**
  - `--all-sandboxes`: credentials are used for host pulls **and** injected
    by the proxy into **every new sandbox's** registry login (the
    credential itself never enters the sandbox filesystem).
  - `--sandbox NAME`: credentials are injected into **that one sandbox
    only**.
  - Neither flag: host-pulls-only, injected nowhere.
  ```bash
  gh auth token | sbx secret set --all-sandboxes --registry ghcr.io --password-stdin
  gh auth token | sbx secret set --sandbox my-sandbox --registry ghcr.io --password-stdin
  ```
- For a registry whose Bearer auth endpoint lives on a different hostname
  than the registry itself, pass `--registry-auth-endpoint` naming the exact
  trusted HTTPS URL — otherwise the cross-host token exchange is rejected.
- `sbx secret rm --registry HOST --sandbox NAME` removes only that sandbox's
  registry credential; host-only and global (all-sandboxes) entries are
  untouched. This does not revoke the upstream token or prevent use of
  another applicable credential.
  ```bash
  sbx secret rm --registry ghcr.io --sandbox my-sandbox
  ```
- Without `--sandbox`, `sbx secret rm --registry HOST` removes both the
  host-only and global entries. Add `--all-sandboxes` to remove only the
  global entry instead.

## Related skills

- For `docker agent run --sandbox` and `docker agent sandbox` commands,
  use `docker-agent-run`.

- For creating, reattaching to, and removing the sandboxes these policies
  and secrets apply to, use `docker-sandboxes-lifecycle`.
- For declaring `secrets:`/`registries:`/`bindings:` inside a checked-in
  `sbxenv.yaml` file that provisions them at environment-create time, use
  `docker-sandboxes-env`.
- For a kit's own `credentials:` and `permissions.network:` declarations
  (what a kit *asks for*, as opposed to what the user has *approved*), use
  `docker-sandboxes-kits`.

## References

- `references/sources.md` — provenance for every rule above (help captures, source paths, docs URLs).

## Assets

- None.

## Checks

- `checks/verification.md` — Verification runbook for network policy and secret commands (unexecuted runbook; run manually with an isolated `--app-name`, no real secret values).
