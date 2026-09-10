---
name: dotfiles
description: Use when working with the bmthd/dotfiles setup — either changing the repository itself (mise tools, install.sh, docs, the skills that live there) and opening a PR, or applying an available update to THIS machine after the shell printed "dotfiles の更新があります". Invoke as /dotfiles pr <change> or /dotfiles apply.
argument-hint: pr <change> | apply
---

# Dotfiles

Two directions of work against [`bmthd/dotfiles`](https://github.com/bmthd/dotfiles).
They are opposites and must not be confused: `pr` changes the repository for every
machine, `apply` changes this one machine to match the repository.

| Subcommand | Direction | Read |
|---|---|---|
| `pr <change>` | repository ← change, opened as a PR | [pr.md](pr.md) |
| `apply` | this machine ← repository | [apply.md](apply.md) |

**Read the subcommand's file before doing anything.** The procedures are detailed and
neither is safe to improvise.

## Routing

- `args` starts with `pr` — the rest is the change to make. If nothing follows, ask what to change.
- `args` starts with `apply` (or is empty and the user is reacting to an update notification) — read [apply.md](apply.md).
- Neither, and the intent is unclear: ask which one. Do not guess from the current
  directory — being inside a dotfiles checkout does not mean the user wants `pr`.

## Repository facts

Both subcommands rely on these.

- **Setup logic lives in mise**, not `install.sh`. `install.sh` is only a
  bootstrapper (install mise → place the config → `mise install` → `mise run setup`).
  `.mise.toml` is a facade: it declares the tools and names the setup tasks, and each
  `setup:<name>` task runs `.dotfiles/setup/<name>.sh`, which the `setup:scripts` task
  downloads first. Tools and environment are changed in `.mise.toml`; a setup step is
  changed in its script.
- **`.mise.toml` is installed to `~/.config/mise/conf.d/10-dotfiles.toml`**, which mise
  loads as part of the global config, so its tasks run from any directory.
  `~/.config/mise/config.toml` is left to the machine and overrides conf.d.
  That layout — both destinations, plus how the pre-conf.d copy is recognised — is
  defined once in [`.dotfiles/mise-layout.sh`](../../../.dotfiles/mise-layout.sh),
  which `install.sh` and `.dotfiles/apply.sh` both read. Never write one of those
  paths out in a placer again.
- **The shell startup files are mise's too.** `~/.zshrc` and `~/.bashrc` get the
  mise activation and the update-notice source line as marker-delimited blocks,
  declared in `.mise.toml` under `[bootstrap.mise_shell_activate]` and
  `[dotfiles]` and written by `setup:shell`. install.sh no longer appends
  anything to a shell config; changing what a shell gets means changing that
  declaration, not adding shell to a script.
- **Most skills are no longer in this repository.** The portable ones moved to
  [`bmthd/skills`](https://github.com/bmthd/skills). What remains under
  `.agents/skills/` is this `dotfiles` skill, which only makes sense against this
  repository. Third-party skills are installed from their upstream by the
  `setup:skills` task rather than vendored.
- **CI (`.github/workflows/quality.yml`) runs** `mise ls`, `mise tasks ls`, ShellCheck,
  `bash -n`, `zsh -n`, and the scripts under `tests/`.
