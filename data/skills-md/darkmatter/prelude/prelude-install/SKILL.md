---
name: prelude-install
description: Install and configure Prelude (darkmatter/prelude) in any repository — run the setup wizard, wire the flake-parts module into an existing or new flake, activate packages.prelude-shell in the devshell, and verify with real smoke checks. Use for adding devshell UI (MOTD, x command picker, docs viewer, themed prompt), integrating the generated prelude.nix sidecar, or activation questions (nix develop, direnv, lorri).
---

# Install & configure Prelude

Prelude is a flake-parts module suite: a `nix develop` welcome banner (MOTD),
an interactive command picker (`x`), a Markdown docs viewer, and a themed
Starship prompt. Everything runs from the published flake — no checkout of
the Prelude repo is needed. Print docs without cloning:

```sh
nix run github:darkmatter/prelude#skill -- install   # full consumer walkthrough
nix run github:darkmatter/prelude#skill -- options    # generated prelude.* reference
```

## 0. Inspect what already exists

Before changing anything, look at the repo:

- `flake.nix` — flake-parts (`flake-parts.lib.mkFlake`)? plain flakes need
  small restructuring first. Note existing `inputs`, `imports`, and
  `devShells` to preserve them.
- `prelude.nix` / `title.txt` — inspect any existing sidecar before deciding
  setup is needed. Edit existing configuration in place; wizard reruns
  overwrite both files.
- `.envrc` — preserve its existing loader; add `use flake` only when adopting
  nix-direnv, not alongside another environment-loading strategy.
- Existing README and `docs/` — kept untouched by setup.

## 1. Run the wizard (new installs)

```sh
nix run github:darkmatter/prelude -- wizard
```

Steps: title text + FIGlet font, project name, commands, component toggles
(`motd`/`menu`/`prompt`/`docs`/`.envrc`), MOTD copy and layout, theme,
confirm. Run from the project root; it needs an interactive terminal. It
writes:

- `prelude.nix` — full options template: your choices active, every other
  option present as a commented default (the file doubles as inline docs).
- `title.txt` — the rendered wordmark, written beside the config and
  referenced by bare name, so it resolves from any `-o` directory.
- `.envrc` (content exactly `use flake`) — only if toggled on and none exists.
- With docs enabled: starter `README.md` + `docs/getting-started.md` at the
  project root — existing files are kept.

`-o path` moves the sidecar + `title.txt`, but the emitted docs entries
(`./README.md`, `./docs/getting-started.md`) are sidecar-relative while the
starter files land at the root — with a non-root `-o`, fix those paths before
evaluating. The wizard refuses `-o flake.nix` and never writes or replaces a
flake. No flake at all? `nix flake init -t github:darkmatter/prelude#default`
scaffolds a starter instead (configure `prelude.*` inline, skip to *Verify*).

## 2. Wire it into the flake (merge, don't replace)

The example shows the Prelude-specific lines to merge into the **existing**
`flake.nix` — keep every current input, import, and devshell package:

```nix
inputs.prelude.url = "github:darkmatter/prelude";
# Fresh repo, no pins yet: share one nixpkgs/flake-parts via inputs:
#   inputs.nixpkgs.follows = "prelude/nixpkgs";
#   inputs.flake-parts.follows = "prelude/flake-parts";
# flake.lock pins the resolved revision even with the default-branch URL.
# Preserve an existing lock; use that revision for wizard/reference commands.
# A URL ending in /<rev> may additionally select an explicit commit or tag.

# inside mkFlake's module argument:
imports = [
  inputs.prelude.flakeModules.default
  ./prelude.nix # generated sidecar; import it, never replace flake.nix
];

# inside perSystem, alongside existing packages:
devShells.default = pkgs.mkShell {
  packages = [config.packages.prelude-shell];
};
```

Add only `config.packages.prelude-shell` to the devshell — it bundles every
enabled component and activates via its setup-hook. Do not add
`packages.prelude` (that backs the `prelude` app).

## 3. Activation paths

- `nix develop` — with the prompt component enabled (wizard default) the
  setup hook sources the generated init: MOTD renders, `x`/`docs` land on
  PATH, `STARSHIP_CONFIG` exports. Nothing extra to configure.
- direnv (nix-direnv) — the generated `.envrc` (`use flake`) loads the cached
  environment and renders the MOTD; new developers need only their existing
  direnv hook. Preserve an existing `.envrc` and its environment loader.
- lorri — runs `shellHook` inside the Nix builder, so route it through the
  same `.envrc`: replace `use flake` with `eval "$(lorri export direnv-adapter)"`.
- Custom `shellHook` — `eval "$(prelude-preflight)"` is the loader-aware
  activation line. Never `export -f` in a shellHook (zsh rejects the `%` in
  `BASH_FUNC_…%%` names); shell-specific setup belongs in `prelude hook`.

## 4. Customize

Edit the generated `prelude.nix` (inline config in `flake.nix` works too);
every option sits there as a commented default. Highlights:

- `prelude.theme` — `prelude` (default), `phosphor`, `minted`, `amber`,
  `solarized`, `nord`, `gruvbox`, `paper` (light), `mono`, `apathy`; token
  overrides via `prelude.palette`.
- `prelude.commands.<key>` — catalogue entries behind `x`; the first colon
  infers the menu group (`db:migrate` → `db`). Package-backed commands:
  `prelude.lib.fromPkg packages.dev { description = …; motd = 1; }`.
- `prelude.docs.pages = [{text = ./docs/foo.md;}]` — one page per file.

## 5. Git-track new files, then verify

Git-backed flakes exclude untracked files. Inspect `git status --short` and
stage only the intended files created or edited for this setup; do not stage
unrelated changes or suppress `git add` errors. Include a newly created
`README.md` when referenced, the actual sidecar and sibling `title.txt`
locations (including custom `-o` paths), and any newly referenced docs.
Do not stage a pre-existing `.envrc` merely because the wizard uses it.
No commit is required for local evaluation.

Alternatively, verify with `nix develop path:.` and `nix flake check path:.`
to include the working directory without changing the index. This can include
normally Git-excluded files, so use it only on a trusted local working tree.

Then real smoke checks:

```sh
nix develop     # MOTD renders, themed prompt appears
x --list        # catalogue table prints non-interactively
x               # picker opens (q quits)
docs            # viewer opens when docs pages exist (q quits)
motd            # banner reprints on demand
nix flake check # full build gate (heavier)
```

Non-interactive `nix develop -c …` stays silent by design (no banner in build
logs) — use the interactive shell to see the MOTD.

## Handoff

- `/prelude-just <arg>` — adapt an existing justfile.
- `/prelude-docs` — author docs-viewer pages.
- `/prelude <anything>` — other Prelude work.
