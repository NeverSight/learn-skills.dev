---
name: dotfiles
description: Change the chezmoi-managed dotfiles and ship the change, in sync with GitHub.
argument-hint: "[what to change]"
disable-model-invocation: true
---

# Dotfiles

Carry out the user's request on their dotfiles: the GitHub repository
[seven7thirty3five5/dotfiles](https://github.com/seven7thirty3five5/dotfiles),
cloned at `~/.local/share/chezmoi`. With no request, ask what to change.

A run starts and ends **in sync**: `git status` is clean, local `main` matches
`origin/main`, and `chezmoi verify --exclude=scripts` passes, so the home folder
matches the repository.

## 1. Orient

1. Confirm this machine publishes the dotfiles, since only the repository's
   owner can push: `chezmoi execute-template '{{ .publishDotfiles }}'` prints
   `true`, `git push --dry-run` succeeds, and `gh auth status` shows
   `seven7thirty3five5` as the active account (gh watches the workflow).
2. Start in sync. With `git status` clean and `chezmoi verify --exclude=scripts`
   passing, `chezmoi update` pulls and applies the latest commits; then `main`
   must match `origin/main`.
3. Read `README.md`: its "How it works" section says where each kind of change
   belongs. Then read the files your change touches. For each chezmoi feature
   you use, read its page in chezmoi's reference:
   <https://www.chezmoi.io/reference/>.

When a check fails or the machine is out of sync, stop before editing and show
the user what you found: uncommitted work, edits to deployed files and unpushed
commits are theirs to settle. Done when every check passes and you can name the
owner of each thing your change touches.

## 2. Change

Edit the repository's files: `chezmoi apply` deploys them, replacing edits made
in the home folder (`chezmoi source-path FILE` names a deployed file's source).

The dotfiles serve three kinds of machine: a Mac, Linux with sudo, and Linux
without sudo (a work machine, where Homebrew lives in the home folder). Keep
all three working, and apply YAGNI: make the smallest change that does what the
user asked, for situations these machines actually meet. Reach for a plain
config file first, a template when a value differs between machines, and a
setup script only to install something. When a change needs checking, extend
`scripts/lint.sh` or `scripts/check-install.sh`. Write like the file you are
editing, with comments that say why in a line or two.

Done when `git grep` finds nothing in the README, comments or checks that your
change made untrue.

## 3. Verify

1. `sh scripts/lint.sh` passes.
2. `chezmoi diff` shows only the changes you intended, including the setup
   scripts it will run. Then run `chezmoi apply`.

## 4. Ship

1. Commit in the style of `git log`.
2. `sh scripts/check-install.sh` passes; it checks the applied machine and
   needs a clean tree.
3. Push, and watch the Checks workflow on the pushed commit until it finishes
   (`gh run watch`); its install jobs take about ten minutes. When a job fails,
   fix it and ship again.

Done when the workflow passes and the machine is in sync. Report what changed,
and anything the user must do by hand on other machines.

## Gotchas

- On this machine, chezmoi commits and pushes each source change it makes
  (`chezmoi add`, `chezmoi edit`), before your checks run. Create and edit
  source files yourself, with chezmoi's names (`dot_`, `private_`,
  `executable_`, `.tmpl`).
- When chezmoi stops managing a file, it leaves the file in place on every
  machine; listing it in `.chezmoiremove` deletes it.
- A setup script whose rendered text changes runs again on every machine's
  next apply, `#` comments included; a template's `{{/* */}}` comments don't
  count. On Linux with sudo, rerunning the system-packages script asks for a
  password.
- `update` upgrades everything on the machine: run it when the user asks, and
  test a changed part of it on its own.
