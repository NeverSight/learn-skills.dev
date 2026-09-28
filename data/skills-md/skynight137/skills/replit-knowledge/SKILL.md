---
name: replit-knowledge
description: "Replit sandbox platform facts (no Nix): $HOME wiped on recreate, the /run/replit/env env-load channel, the rc chain (~/.bashrc store bootstrap -> $REPL_HOME/.config/bashrc, with .config/replit_bashrc as a REPLIT_MODE shim), GIT_CONFIG_GLOBAL is workspace-persistent not tmpfs, bare python is the platform runtime. Use before persisting data or debugging env/rc/git on Replit."
version: 2.1.0
license: MIT
platforms: [linux]
compatibility: "Replit workspaces (/home/runner containers)."
metadata:
  hermes:
    tags: [Replit, sandbox, persistence, XDG, REPL_HOME, npm, replit-shutdown, bashrc, git, env, secrets]
    related_skills: [replit-nix, camofox-on-replit, replit-playwright-chromium]
---

# Replit sandbox: what platform you're on

Field-verified platform facts only (2026-09-02/03, 2026-09-12, re-verified
2026-09-17, 2026-09-26).
How to actually pull packages out of `/nix/store` (replit.nix, nix-env, closures) is
the **`replit-nix`** skill. Hermes-on-Replit recovery (uv `--locked`
trailing-slash failures, `libatomic` for PM-staged node):
`references/hermes-on-replit.md`.

## 1. What survives a restart (the #1 gotcha)

- `$HOME` (`/home/runner`) is **wiped on container recreate**.
- The **workspace persists** — `$REPL_HOME` (`/home/runner/workspace` on this
  box) is the durable home. Default working dir is the only home for durable files.
- `replit shutdown` stops the container without wiping `$HOME` or deleting
  `replit.nix`; none of these touch **`/nix/store`** (it persists outside all three
  until GC). See `replit-nix` for what that means for libs.
- **`/run` is tmpfs** (RAM, ~50MB — `df -h /run` confirms). Everything under it is
  gone on every recreate. Two subtrees matter:
  - `/run/replit/env/` — the **platform env-load channel** (§3). `latest`,
    `latest.json`, `last`, `last.json`.
  - `/run/replit/user/<id>/` — transient per-user state (`.bash_history`,
    `.config/git/`). Do not treat anything here as durable.

Rules:

- Store persistent data under `$REPL_HOME`, never `$HOME` (and never `/run`).
- **XDG pre-set by platform** — `XDG_*_HOME` point at workspace paths
  (verified: `XDG_DATA_HOME=/home/runner/workspace/.local/share`,
  `XDG_CONFIG_HOME=/home/runner/workspace/.config`; check with
  `printenv | grep XDG_`). Don't override them; use `$XDG_DATA_HOME` in your
  tooling. On non-Replit machines the XDG spec defaults (`$HOME/.config` etc.)
  apply, so the same code works — that's why scripts fall back to *spec* defaults,
  not hardcoded paths, when the vars are unset.
- Tool install dirs (engines, runtimes) belong under `$XDG_DATA_HOME/<tool>/`
  (uv-style): one dir per tool, `rm -rf` one dir to reset. Don't scatter tool
  dirs across the workspace root.
- Config "how to set it up again" belongs in the repo workspace (this skills repo
  is one such).

## 2. Working dir & the `REPL_*` env vars

`$REPL_HOME` = the workspace = default cwd. Everything durable goes under it.
The platform injects a large set of `REPL_*` / `REPLIT_*` vars — list them
anytime with `printenv | rg 'REPL'`. The ones that matter:

| Var | Meaning |
|-----|---------|
| `$REPL_HOME` | workspace dir (persisted; default cwd) |
| `$REPL_OWNER` / `$REPL_USER` / `$REPLIT_USER` | account name (all the same) |
| `$REPL_ID` | repl UUID; `$REPL_SLUG` (e.g. `workspace`) |
| `$REPLIT_DOMAINS` / `$REPLIT_DEV_DOMAIN` | public `<repl>.<cluster>.replit.dev` |
| `$REPLIT_BASHRC` | path to the rc a shell sources — **overridable** in `.replit` (§4); on this workspace it is `$REPL_HOME/.config/replit_bashrc`, NOT the store default |
| `$REPLIT_NIX_CHANNEL` | nixpkgs channel this repl builds against (e.g. `stable-25_05`) |
| `$REPLIT_LD_AUDIT` / `$REPLIT_RTLD_LOADER` | the custom dynamic loader (see `replit-nix` §3) |
| `$REPLIT_PLAYWRIGHT_CHROMIUM_EXECUTABLE` | store Chromium for Playwright (see `replit-playwright-chromium`) |
| `$REPLIT_RUN_PATH` | `/run/replit` (per-user run state) |

Rest are identity/cluster/p2p tokens — don't echo them into logs.

### Config files that matter

- **`.replit`** — TOML. `modules = ["nodejs-24", "python-3.13", …]` (language
  runtimes; the version can be STALE — §9), `[nix] channel = "stable-25_05"`
  (the channel `replit.nix` builds against), `[userenv.shared] KEY=VALUE` (env
  for **every** shell, incl. registry pins — §3/§5), `[[ports]]
  localPort/externalPort` (publishing), `entrypoint`, `run`, `[workflows]`.
- **`replit.nix`** — workspace-root Nix deps; mechanics in `replit-nix`.
- **`$HOME/.bashrc`** — symlink into `/nix/store` (platform-regenerated
  bootstrap, not yours). Your rc is `$REPL_HOME/.config/bashrc` — §4.
- **`.config/replit_bashrc`** — the re-entry shim §4 describes.

## 3. Where env vars actually come from (the env-load channel)

This is the mechanism to reach for when a var "isn't showing up". There are
**three independent sources**, and they are easy to conflate:

| Source | What it is | How to read it |
|--------|-----------|----------------|
| **Platform env snapshot** | Replit's own render of the shell env, incl. **Replit Secrets**. Written to `/run/replit/env/latest` (bash `declare -gx NAME=value` lines) and `/run/replit/env/latest.json` (`{"environment": {...}}`). `last`/`last.json` are the previous generation. | `python3 -c "import json;print(json.load(open('/run/replit/env/latest.json'))['environment'])"` |
| **`.replit [userenv.shared]`** | Project-pinned vars that apply to **every** shell, incl. workflow/run-button shells. The durable place to pin env. | `grep -A40 '\[userenv.shared\]' .replit` |
| **Process env** | What a *live* process actually inherited, incl. vars set after the shell started. | `tr '\0' '\n' < /proc/<pid>/environ` |

- The store bashrc sets `SHELL_ENV="/run/replit/env/latest"` and loads it, so the
  platform snapshot is the base layer; `.replit [userenv.shared]` then overlays.
  Verified: `GOPROXY` is the firewall value
  (`http://package-firewall.replit.internal/go/`) in the platform snapshot but the
  public value (`https://proxy.golang.org,direct`) in a live shell — the `.replit`
  pin wins.
- **Precedence, verified:** `.replit [userenv.shared]` > platform env snapshot >
  shell defaults. `.replit` values reach every shell type; rc-file exports only
  reach shells that source the rc (§4).
- **The `/proc` route is how you audit what a process really got**:
  `tr '\0' '\n' < /proc/<pid>/environ | grep NAME`. Useful when a tool sees a var
  a plain `printenv` in your shell does not (different parent), and it is the only
  way to see the env of a process you did not spawn.
- Replit Secrets land in the **platform snapshot**, not in `.replit` — so a secret
  is present in `/run/replit/env/latest.json` but may be absent from
  `.replit [userenv.shared]`. Distinguish "platform/Secrets-provided" from
  "project-pinned" by diffing the two.

### The 3 reasons a var is invisible (don't conflate them)

When a var "isn't there", it is exactly one of these — identify which before fixing:

1. **Not set at all** — not in `.replit [userenv.shared]`, not in the platform
   snapshot, not exported by any rc. Fix: add it to `.replit [userenv.shared]`.
2. **Scrubbed by the tool that spawned the child** — e.g. a Hermes terminal child
   has provider credentials (`ANTHROPIC_API_KEY`, `ANTHROPIC_BASE_URL`,
   `TELEGRAM_BOT_TOKEN`, `GH_TOKEN`, …) removed by design, even though the parent
   process holds them. Confirm with `tr '\0' '\n' < /proc/<parent-pid>/environ`.
   This is not a Replit behaviour; it is the harness's secret scrub.
3. **Masked in the output you are reading** — the *value* is replaced by a
   redaction placeholder (e.g. `«redacted:sk-…»`) in tool output **and in file
   reads**. Redaction is **value-based, not name-based**: a secret-shaped value is
   masked even under a harmless name, and a harmless value under a secret-shaped
   name prints fine. The substitution is **non-deterministic** — the same file can
   read back differently between two reads, which is what makes it look like the
   file "changed". The var is fine; your view of it is not. Verify with a
   length/hash check (`sha256sum`, `wc -c`, `od -c`) rather than trusting the
   rendered text.

## 4. The shell rc chain (verified 2026-09-17)

`$HOME/.bashrc` is a **symlink into `/nix/store`**
(`readlink -f ~/.bashrc` → `…-replit-bashrc/bashrc`), i.e. platform-regenerated.
That store bashrc is the bootstrap; it is **not** your custom-rc slot. The chain:

1. Store bashrc sets `BASHRC="${REPL_HOME}/.config/bashrc"` (line ~9) and
   `SHELL_ENV="/run/replit/env/latest"`.
2. At the bottom (line ~322) it does:
   `if [[ -f "${BASHRC}" ]] && [[ -z "${REPLIT_MODE}" ]]; then source "${BASHRC}"; fi`
   → **`$REPL_HOME/.config/bashrc` is the native persistent custom-rc slot**, and
   it is only sourced when `REPLIT_MODE` is empty.
3. `REPLIT_MODE` is set to `agent` or `workflow` for those shell types, so the
   store bashrc **skips** the user rc in them. That is by design
   (store comment: "unless we have REPLIT_MODE set, which is used for special
   occasions like agent/assistant/workflow use").
4. **`REPLIT_BASHRC` is NOT reserved — it is overridable, and this workspace
   overrides it.** `.replit [userenv.shared]` sets
   `REPLIT_BASHRC = "/home/runner/workspace/.config/replit_bashrc"`, and the live
   env shows that workspace path. (Replit's own snapshot in
   `/run/replit/env/latest.json` still carries the `/nix/store/.../replit-bashrc/bashrc`
   default; the `.replit` pin wins.) Nothing in the store bashrc even reads
   `REPLIT_BASHRC` — grep confirms zero references.
5. This workspace's `.config/replit_bashrc` exists to defeat the `REPLIT_MODE`
   guard for workflow/agent shells. Its whole body is:
   ```bash
   unset REPLIT_MODE
   source ~/.bashrc
   ```
   Unsetting `REPLIT_MODE` makes the store bashrc's guard pass on the re-source,
   so the real toolchain rc loads in workflow shells too. It is a re-entry shim,
   not the toolchain file.
6. The **actual toolchain rc** is `$REPL_HOME/.config/bashrc` (~43 lines): registry
   pins, `XDG_*`, `GIT_CONFIG_GLOBAL`, a guarded `PATH` prepend, aliases.

Consequences:

- Two different files, two different jobs — do not merge them:
  `.config/replit_bashrc` = re-entry shim (unset guard + re-source);
  `.config/bashrc` = your toolchain/exports.
- Do **NOT** create a bare `$REPL_HOME/.bashrc` and expect shells to source it —
  the store bashrc only sources `$BASHRC` = `.config/bashrc`. That file is dead.
- **Never `source "$HOME/.bashrc"` from inside `.config/bashrc`.** `$HOME/.bashrc`
  is the bootstrap that sourced you; re-sourcing it re-runs its
  `source "${BASHRC}"` and infinitely recurses (verified: hung the terminal until
  the line was removed). The shim in `.config/replit_bashrc` gets away with it only
  because it `unset REPLIT_MODE` first and the guard is the thing that stops the
  loop — do not copy that pattern into `.config/bashrc`.
- A var that must exist in **workflow/run-button** shells cannot rely on the user
  rc alone: pin it in `.replit [userenv.shared]`, which reaches every shell type.
- Verify after editing: open a **fresh** terminal and confirm the block loaded
  (`alias`, `printenv`) and that it does **not** hang.

## 5. npm / package managers package firewall

The sandbox pins package registries through **package firewall**
(`NPM_CONFIG_REGISTRY` → `package-firewall.replit.internal`), and
`.replit [userenv.shared]` deliberately re-pins the **public** registries on top
(§3 precedence: `.replit` wins). Firewall metadata breaks some tarballs (404),
and **env pins beat CLI flags** (`--registry` loses to `npm_config_registry`).
Two verified fixes:

```bash
unset NPM_CONFIG_REGISTRY npm_config_registry; npm install
# or
npm install --registry=https://registry.npmjs.org/
```

pip analog: `PIP_INDEX_URL` is pinned to pypi.org in `.replit [userenv.shared]`
on this workspace (works as-is); if you hit a firewall pip mirror, set
`PIP_INDEX_URL=https://pypi.org/simple/` explicitly.

### Which registry vars are Replit-auto vs project-pinned

- **Replit AUTO-injects** (platform snapshot): the firewall mirror
  (`package-firewall.replit.internal`) for npm/yarn/pip/go, plus
  `npm_config_prefix` (global node-modules dir) and the `/nix/store/...` toolchain
  binaries. You don't set these.
- **Project-pinned on purpose** in `.replit [userenv.shared]` (this workspace): the
  PUBLIC registries that override that firewall — `NPM_CONFIG_REGISTRY` and
  `npm_config_registry` → registry.npmjs.org, `YARN_REGISTRY`/`YARN_NPM_REGISTRY_SERVER`
  → registry.yarnpkg.com, `PIP_INDEX_URL`+`PIP_TRUSTED_HOST` → pypi.org,
  `GOPROXY` → proxy.golang.org, and `PYTHONPATH=""` (un-shadow global
  site-packages). These are deliberate (firewall breaks some tarballs), NOT
  Replit defaults.
- Tell them apart by diffing the live shell against
  `/run/replit/env/latest.json` (§3). If you see `package-firewall.replit.internal`
  come back in a live shell (a shell/CI that didn't get `.replit` env), that's the
  auto default surfacing — re-apply the `.replit` pins.

## 6. Processes & ports

- `replit shutdown` stops the container; the workspace survives, `$HOME`
  does not, `/nix/store` does not change.
- Daemons: run **on demand** (start when needed, kill when done) — no
  always-on background watchers unless the user asks; containers die and
  nothing restarts them.
- `[[ports]]` in `.replit` maps local→external for HTTP publishing; plain
  `curl 127.0.0.1:<port>` works for local verification.
- **`curl`, not `ss`/`netstat`, is the authority for "is it listening".**
  `ss -ltn` on this box prints nothing even while a server answers on that
  port — a `grep` against its output reads as "nothing listening" and sends
  you hunting a bug that does not exist. Probe the port:
  `curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:<port>/health`
  (000 = down, 200 = up). Confirm a *process* with `ps`, never with `ss`.
- **Kill by exact PID from `ps`, not `pkill -f <pattern>`.** `pkill -f`
  matches the invoking shell's own command line (the pattern sits in it), so
  it SIGTERMs your shell — the tool call dies mid-script and the target may
  survive. `ps -eo pid,cmd | grep <name> | grep -v grep`, then
  `kill -9 <pid>`. A `server.js`-style generic name needs the full path
  (`grep 'camofox-browser/server.js'`) so unrelated `node` procs are spared.

## 7. Git identity on Replit (corrected 2026-09-17)

### `GIT_CONFIG_GLOBAL` is NOT tmpfs here

An earlier version of this skill claimed Replit exports
`GIT_CONFIG_GLOBAL=/run/replit/user/<id>/.config/git/config` and that identity
"keeps reverting" because `/run` is wiped. **That is wrong on this workspace.**

- Verified live: `GIT_CONFIG_GLOBAL=/home/runner/workspace/.config/git/config` —
  a **workspace-persistent** path, set by `.replit [userenv.shared]`
  (`.replit` line ~162). It survives recreate like any workspace file.
- `/run/replit/user/<id>/.config/git/` does exist (the platform default location),
  but it is **not** the live value here — the `.replit` pin overrides it.
- `git var GIT_COMMITTER_IDENT` returns the configured identity, and
  `git config --global --list` reads from the workspace file. Nothing is reverting.

So: if you *do* land on a workspace without that `.replit` pin, you get the
platform's `/run` tmpfs default and identity is lost on recreate. The durable fix
is the same one this workspace uses — pin it in `.replit [userenv.shared]`:

```
[userenv.shared]
GIT_CONFIG_GLOBAL = "/home/runner/workspace/.config/git/config"
```

Then fill it with `git config --file /home/runner/workspace/.config/git/config
user.name ...` / `user.email ...`. (Pinning in `.replit` is better than exporting
from `.config/bashrc` because it also reaches workflow/run-button shells, §4.)

- Reminder: `git config --global` does NOT hardcode `~/.gitconfig` — it writes to
  whatever `GIT_CONFIG_GLOBAL` points at. Check that path first when identity
  looks wrong.
- Repo scope still works and is authoritative for one project: `git config
  user.name "You"` (no `--global`) writes `.git/config`, which wins over
  `GIT_CONFIG_GLOBAL`.

### Hooks gotcha

- A stale `core.hookspath` pointing at a **nonexistent** dir makes git **ignore
  `.git/hooks/` entirely** (harmless-looking rename/add of a hook "does
  nothing"). Seen here: `core.hookspath=.husky/_` while no husky was installed
  (no package.json `husky`/`prepare`, no `.husky/`). Fix: `git config --unset
  core.hookspath` (or point it at a real dir). Diagnose: `git config core.hookspath`;
  `ls .husky` / `grep husky package.json` before assuming.
- **Author identity is never set from a pre-commit hook.** Hooks run during the
  commit, too late, and that's not their job. Author = config/env at commit time
  (`user.*`, `GIT_AUTHOR_*`/`GIT_COMMITTER_*`). pre-commit is for checks (e.g.
  `ruff check` on staged `.py`).
- `.git` and `.git/hooks` are normally yours: owned by the `runner` user and
  writable — permission problems there are usually a misconfig (hookspath),
  not ownership.

## 8. Reading files & tool output on this box (corrected 2026-09-17)

An earlier version of this skill claimed the tool output/read transport "strips
spaces, `$`, `as`, `in`, `#`, `=`, and leading whitespace", and told you to
distrust printed bytes. **That diagnosis was wrong** — verified 2026-09-17 with a
control file: spaces (single and runs), tabs, leading indentation, `$`, `#`, `=`,
and `$VAR` all round-trip **byte-exact** (`od -c` and `sha256sum` confirm).

What is actually happening is **secret-value redaction**:

- The transport replaces a **secret-shaped value** with a placeholder such as
  `«redacted:sk-…»`. This applies to tool output *and* to `read_file`/`read`
  results.
- It is **value-based, not name-based**: `MY_KEY=sk-ant-…` gets masked;
  `MY_KEY=hello-world` does not; a fake `ANTHROPIC_API_KEY=fake-not-real-abc123`
  prints unmasked. The name is irrelevant; the *value's shape* decides.
- The substitution is **non-deterministic** — repeated reads of the same bytes can
  render differently. That is the real cause of "the file looks like it changed"
  and of the earlier "concurrent platform rewrites / flip-flop" misdiagnosis.
  `.replit` is stable: two reads a second apart give an identical
  `sha256sum` (`380639516225c163770f8f70ce099d726d5ff44daa8ee9ee8964f784276b76b1`).

Practical rules:

- To verify content, use **byte-level** checks (`sha256sum`, `wc -c`, `od -c`,
  `cmp`), never a visually-inspected repr, when the content may contain a
  secret-shaped value.
- When a config line "looks merged" (e.g. `--host0.0.0.0--port`), suspect
  redaction of a value on that line, not whitespace stripping. Confirm with
  `grep -c` / `bash -n` / a parser (`python3 -c "import tomllib; …"`).
- Editing is unaffected: `patch` replaces the matched bytes verbatim. Keep the
  anchor line in **both** `old_string` and `new_string` when inserting after it,
  or you will silently delete it.

## 9. Python interpreter shadowing on Replit (verified)

Bare `python3` resolves to a **Replit runtime**, not the project venv and not uv:

- `command -v python3` → `/repl/tools/bin/python3`;
  `sys.executable` → `/repl/ctls/<hash>-python3-3.14.6/bin/python3` (verified
  2026-09-17; `python3 -V` = `Python 3.14.6`).
- This is intentional: the project runtime is uv-managed at `.venv/`
  (`uv run` / `source .venv/bin/activate` is the contract). Do NOT auto-prepend
  `.venv/bin` to PATH "to fix" it — that inverts the shadow and makes every
  platform/`replit` tool import your project packages.
- `python` may not exist at all (verified absent); use `python3`.
- Two separate concerns:
  - **site-packages shadowing** → handle EARLY with `PYTHONPATH=""` in
    `.replit [userenv.shared]` (verified present there; live shell shows it
    empty). Stops a project `PYTHONPATH` leaking into bare-`python3` tooling.
  - **interpreter choice** (`python3` = platform vs venv) → keep as a
    note/contract, don't force it. `.venv/bin` PATH prepend is available if a user
    explicitly wants `python3` to be the venv, but it's a deliberate tradeoff.
- The `.replit` `modules` row lists a version (e.g. `python-3.13`) that can be
  **STALE** — verified: `.replit` says `python-3.13` while the live interpreter is
  3.14.6. The module row does not control the active version. Check
  `python3 -c 'import sys;print(sys.executable)'`, never the module list or
  AGENTS notes.

## Quick diagnostic table

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| data/tooling gone after restart | it lived in `$HOME` (or `/run`) | §1: move under `$REPL_HOME` + XDG anchors |
| `npm ERR ... 404` on tarballs | package firewall | §5: unset pins or explicit `--registry` |
| env var missing in a shell | one of 3 causes | §3: check `.replit` → platform snapshot → scrub → redaction, in that order |
| env var missing only in workflow/run-button shell | user rc skipped (`REPLIT_MODE` set) | §4: pin in `.replit [userenv.shared]` |
| var present in `printenv` but a child tool lacks it | harness secret scrub | §3 cause 2: confirm via `/proc/<pid>/environ` |
| file content looks mangled/changed between reads | secret-value redaction, non-deterministic | §8: verify with `sha256sum`/`od -c`, not the rendered text |
| commit author reverts | `GIT_CONFIG_GLOBAL` points at `/run` tmpfs (no `.replit` pin) | §7: pin it in `.replit [userenv.shared]`; here it is already workspace-persistent |
| renamed/added pre-commit hook does nothing | stale `core.hookspath` to missing dir | §7: unset `core.hookspath`; verify `git var` |
| terminal hangs / stuck opening a shell | rc re-sources `$HOME/.bashrc` | §4: delete that line — it recursively re-sources the bootstrap |
| `python`/`python3` isn't the venv interpreter | expected — platform runtime + uv contract | §9: use `uv run` / `source .venv/bin/activate`; don't prepend `.venv/bin` |
| which nix channel is this repl on? | — | `echo $REPLIT_NIX_CHANNEL` |
