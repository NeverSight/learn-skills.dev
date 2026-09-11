---
name: prelude
description: Context map of Prelude, the Nix devshell UI suite (MOTD banner, x command catalogue, docs viewer, themed prompt). Use for any task in a prelude-enabled repo, or when the user mentions prelude, x/motd/docs commands, the prelude wizard, or its flake-parts options. Enriches the task with accurate public-interface knowledge; never installs or reconfigures on its own.
argument-hint: <your task, in any repo that uses Prelude>
---

# Prelude

Prelude is a [flake-parts module](https://github.com/darkmatter/prelude) that makes a Nix devshell usable: a welcome banner (MOTD), an interactive command picker and non-interactive dispatcher (`x`), a full-screen Markdown docs viewer, and a themed prompt. Configuration is authored in Nix as `prelude.*` options (validated at build time); small Go binaries consume normalized JSON. The only command a developer must remember is `nix develop`.

The argument to this skill is the user's task description — interpret it; do not execute or shell-interpolate it. Answer the task itself first, using the sections below only where they intersect.

## Public architecture

- **Nix owns configuration.** All options live in the consumer's flake as `prelude.*` (typically a wizard-generated sidecar `prelude.nix` imported next to `prelude.flakeModules.default`). Go binaries render; they do not re-own policy.
- **One devshell package.** `packages.prelude-shell` bundles every enabled component and activates via its setup-hook (`$PRELUDE_INIT` for `nix develop`; nix-direnv evaluates the cached `shellHook`). Add only that package to the devshell — never `packages.prelude`.
- **Shell integration.** direnv needs just `use flake` in `.envrc`. For custom rc files, print the hook with `prelude hook [bash|zsh]` — do not `eval` it before Prelude is on PATH. Never `export -f` in a devshell `shellHook` (breaks zsh); use `prelude hook` for shell-specific setup instead.

## Consumer entrypoints

Inside the shell (each with a single-key accelerator): `x` (`m`) opens the picker, `x <key>` dispatches a catalogue command, `x --list` prints the table; `motd` (`?`) reprints the banner; `docs` (`d`) opens the viewer; `portal` (`p`) launches apps with health lights.

Bootstrap from outside: `nix run github:darkmatter/prelude -- wizard` writes a `prelude.nix` sidecar (+ `title.txt`, `.envrc`) without touching `flake.nix`. The flake also exports `apps.prelude` with subcommands `wizard`, `hook`, `preflight`, `title`, `title-previews`, and passthroughs for enabled components. `nix run github:org/repo#prelude -- docs` documents any prelude-enabled dependency.

## Command catalogue rules

- The catalogue key **is** the public identity: globally unique, callable as `x <full-key>`. The first colon only infers the menu group (`go:test` → group `go`, shown as `test`); an explicit `group` field overrides placement without renaming.
- `x <key>` with the complete catalogue key is the guaranteed public form for every command. Prelude generates one `x` dispatcher, not per-command executables.
- **Import; do not export.** Existing `package.json` scripts, Justfile recipes, and flake apps stay authoritative. `prelude.lib.fromPkg pkgs.foo { … }` adapts an existing package (carrying its runtime closure); `prelude.menu.just.enable = true` imports public Justfile recipes at runtime (explicit Nix entries win name clashes). Imports are one-way — never write catalogue entries back to those files.
- **Canonical commands stay canonical.** Nix builds the environment; `x` only discovers and dispatches. The owning tool (`bun`, `just`, `go`, `nix run …`) executes the workflow. Do not translate a project's workflows into new prelude commands when they already have an owner.

## Docs basics

`prelude.docs.pages` embeds Markdown at build time: leaves like `{ text = ./README.md; }`, groups, optional `{ generate = "nixosOptions"; }` nodes, and `prelude.lib.mdSplit ./file.md` for fence-aware H2 splitting. Set `prelude.docs.rootReadme` to the root README path for styled project intro. Viewer keys: digits jump pages, `Tab` steps, `j`/`k` scroll, `q` quits. Docs-regeneration commands like `sync-docs` belong to the upstream prelude repo — a downstream repo regenerates its own docs only per its own project workflow, if it has one.

## Configuration ownership

Do not edit Go internals or generated docs to change behavior — configure supported consumer behavior via the public `prelude.*` options in the consumer's Nix: `prelude.theme`/`prelude.palette` (themes: `prelude`, `phosphor`, `minted`, `amber`, `solarized`, `nord`, `gruvbox`, `paper`, `mono`, `apathy`), `prelude.colorProfile` (`truecolor` default), `prelude.commands`, `prelude.motd.*` (title, tagline, status probes, recipes), `prelude.docs.*`, `prelude.prompt.enable`. The wizard-generated sidecar lists every option as a commented default.

## Version-correct references

Prefer the consumer's own locked input when it matters: check the pinned `prelude` rev in the project's `flake.lock`, then read docs from `nix run github:darkmatter/prelude/<rev>#skill -- <topic>`. Topics: `list`, `install`, `options`, `commands`, `configuration`, `guide command-conventions`, `guide title-rendering`. The `#skill` app prints upstream Markdown with no checkout or TUI. For general reference use the published docs:

- README (quickstart, catalogue, docs usage): https://github.com/darkmatter/prelude/blob/main/README.md
- Consumer walkthrough (flake wiring, packages, shell hooks): https://github.com/darkmatter/prelude/blob/main/docs/your-own-repo.md
- Option reference (generated): https://github.com/darkmatter/prelude/blob/main/docs/reference/options.md
- Command conventions: https://github.com/darkmatter/prelude/blob/main/docs/guides/command-conventions.md
- Complete consumer example: https://github.com/darkmatter/prelude/tree/main/examples/reference

## Handoff to focused skills

- Installing or wiring prelude into a repo (wizard, flake wiring, devshell) → `/prelude-install`.
- Importing or debugging the Justfile integration (`prelude.menu.just`) → `/prelude-just`.
- Authoring or restructuring docs pages/viewer behavior → `/prelude-docs`.

Each works standalone; this skill only routes to them, never requires them.

## Discipline

- The user's original request is primary. Use Prelude knowledge to inform it (e.g. run a project task via `x <key>`, keep changes inside `prelude.*` options), not to expand it.
- Never install, re-run the wizard, or reconfigure theme/commands/docs unless the user asks for exactly that.
- Preserve the project's existing tooling and ownership boundaries: adapt commands with `prelude.lib.fromPkg`, don't duplicate them, and don't rename canonical workflows.
