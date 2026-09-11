---
name: prelude-just
description: Use when authoring or editing Justfile recipes in a repository wired to Prelude, when the user asks to add just recipes or make them discoverable in the x menu, or when a recipe needs descriptions, typed arguments, groups, aliases, or module namespacing. Covers recipe authoring for Prelude's runtime Justfile import and verification through x.
argument-hint: <what to add or change, e.g. "add a test recipe wrapping bun run test">
---

# Prelude + Just

The Justfile stays the canonical owner of task semantics; Prelude imports it at
runtime — recipes are never copied into `prelude.commands`. Treat the user's
request as the specification, never as shell text to interpolate. Bind every
recipe to the project's real canonical command — the invocation the tool owner
already uses (`bun run test`, `go test ./...`, `nix flake check`) — and confirm
it actually exists in the repo before writing it; never invent placeholder
scripts.

## Enable the import (once)

In the flake-parts module (sidecar `prelude.nix` or inline configuration):

```nix
prelude.menu.enable = true;
prelude.menu.just.enable = true;
# prelude.menu.just.justfile = ./just/Justfile;  # pin; null = just's own discovery
# prelude.menu.just.group = "tasks";             # menu group for flat recipes
```

With `config.packages.prelude-shell` in the consumer devshell, enabling both
options provides `x` and `just`. The Justfile import flag alone does not enable
the menu. See `/prelude-install` if shell integration is missing.

Attribute support is version-gated in
`just` (`[metadata]` 1.42+, `[arg(long/short)]` 1.46+, `[arg(pattern)]` 1.45+,
`[arg(min/max)]` 1.56+) and the import itself only maps fields the consumer's
locked Prelude revision knows — check `just --version` and confirm against the
locked prelude input before relying on an attribute. An existing
`prelude.commands.<name>` entry always wins over a same-named recipe.

## Author recipes the import understands

The menu reads `just --dump --dump-format json`; only these fields surface:

- `# doc comment` → menu description
- `[group('ci')]` → menu group; the key stays flat (`x check`)
- `alias ship := deploy` → its own entry, inheriting target's doc and group
- `mod ops 'ops.just'` → `x ops::migrate` (module namepath groups the entry)
- `[private]` or leading `_` → omitted from the menu
- `[metadata('just test --fix')]` → one worked Example row in the details pane
- `[arg('package', long)]` → `--package` option in argument entry
- `[arg('dry', long, flag)]` → toggleable flag in argument entry
- `[arg('kind', pattern='staging|production')]` → pickable options (plain pipe
  alternation; a regex like `[a-z-]+` is enforced but renders no options)
- default on the recipe line (`package="./..."`) → optional arg pre-filled

Canonical shape — adapt these commands to the project's actual tooling:

```just
# run the unit test suite
[group('ci')]
test:
    bun run test

# run go tests for one package
# (add [group('go')] if a go group is wanted)
[arg('package', help='import path, or ./... for all')]
test-go $package="./...":
    go test "$package"
```

`$package` exports the parameter into the recipe environment; `"$package"`
preserves it as one shell argument. Raw `{{…}}` interpolation inserts text into
shell source; merely surrounding it with quotes does not make arbitrary values
safe. Prefer exported parameters with quoted shell expansion.

Rules:

- Prefer `[group]` over renaming — the public key stays `x test`.
- Argument attributes can change invocation semantics and require a newer
  Just version; `long`/`short` options in particular change positional usage.
  Preserve existing invocation forms unless the task calls for changing them.
  Private/group/metadata attributes affect visibility or presentation and
  also need support from the installed Just version.
- A parameter with no default is required; argument entry rejects blank submit
  until it is filled.
- Scope edits to the request; never rename recipes — that changes public keys.

## Dispatch contract

`x <recipe> [args…]` currently joins extra arguments with spaces and executes
the assembled command through `sh -c`. Original argument boundaries are lost:
quotes used by the calling shell do not protect multiword values, and embedded
metacharacters can become shell syntax. Use direct `just <recipe> "$value"`
for multiword or untrusted values, with safe parameter handling in the recipe
itself. Do not describe `x` forwarding as argv-preserving.

Bare `x <recipe>` opens interactive argument entry when parameters exist.
Modules dispatch as `x ops::migrate`, aliases as `x ship`.

## Documenting workflows

Menu entries are discovery only. A useful workflow doc covers prerequisites,
arguments, worked examples, effects, and troubleshooting — write that in the
project's docs pages or README (see `/prelude-docs`), and mirror the worked
invocations with one `[metadata('just <recipe> <example>')]` line each so the
menu details pane shows them.

## Verify (no source checkout assumed)

Read the recipe before running anything: `just` evaluates backticks when the
file loads, so even `--dry-run` can execute commands. Then, inside the shell:

```sh
just --summary                  # new recipe listed
just --dump --dump-format json  # the exact payload the menu imports
x --list                        # entry appears under its group
just --dry-run <recipe> [args…] # after inspection: prints lines without running them
x <recipe>                     # exercise a safe no-argument recipe
```

References: Prelude import guide — `nix run github:darkmatter/prelude#skill --
guide command-conventions`; just manual — https://github.com/casey/just.
Initial flake wiring: `/prelude-install`.
