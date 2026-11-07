---
name: replit
description: "Replit sandbox toolkit: platform facts ($HOME wiped on recreate, REPL_HOME/XDG/env channels, rc & git persistence), pulling libs from /nix/store (.replit [nix] packages vs replit.nix vs nix-env, transitive LD_LIBRARY_PATH closure), Playwright on Replit's bundled Chromium (no browser download), and the Camoufox anti-detection Firefox server (Cloudflare/Turnstile/WAF sites, cookie persistence, session keep-alive). Use for anything running ON a Replit/Nix workspace."
version: 4.19.0
license: MIT
platforms: [linux]
compatibility: "Replit workspaces (/home/runner containers) with nix. Camofox additionally needs Node >= 18 and GTK3/ALSA/X11 libs in /nix/store — gate: R=\"$(nix eval --raw nixpkgs#gtk3 2>/dev/null)\"; [ -e \"$R/lib/libgtk-3.so.0\" ] && echo warm (~10s; never glob /nix/store/*/lib/* on this box)."
metadata:
  hermes:
    tags: [Replit, sandbox, nix, persistence, XDG, REPL_HOME, bashrc, git, env, secrets, playwright, chromium, camofox, camoufox, scraping, cloudflare]
---

# Replit toolkit — one skill, four lanes

Lane 5 pointer: reaching a *second* box from this one (sshd bootstrap, proxy
port reality, `command -v`/banner-probe traps, path-not-paste delivery) lives in
`references/remote-shell-bridge.md`. Reachability is **per node, not per tailnet**: a
listed peer answers only once it has joined, run the prep there and carries the hop
key. Survey with `scripts/probe-tailnet-peers.sh [port]` and never promise "any
machine on the tailnet". The box's own row is printed as `self` there — resolve self
from the JSON `Self` field, never from a name you remember, since the plain `status`
table labels no row.

Everything here is specific to running **on a Replit/Nix workspace**. The
platform breaks normal Linux assumptions ($HOME wiped, /nix/store GC, npm
firewall), and each lane below is a verified playbook for one job.

**Read `references/platform.md` first if you are new to the box** — every
other lane assumes its persistence rules.

| You want to… | Read | Scripts |
|---|---|---|
| persist data/env/rc/git, understand what survives a restart, fix env-var plumbing | `references/platform.md` | `setup.sh`, `dot_replit.py` |
| get a system lib that isn't installed (GTK, libatomic, any .so), debug `cannot open shared object file` | `references/nix.md` | `scripts/setup/generate-closure.sh`, `libpool.sh` |
| drive Playwright without downloading a browser (the box ships Chromium) | `references/playwright-chromium.md` | `$REPLIT_PLAYWRIGHT_CHROMIUM_EXECUTABLE`, `start-replit-chromium.sh` |
| open bot-hardened sites (Cloudflare/Turnstile/WAF), keep logged-in Firefox sessions alive, **agent browsing on Hermes (camofox MCP — `browser_exec` is broken here)** | `references/camofox.md` | `setup.sh --camofox` (npm lane), `camofox-browser`, `camofox.py` |
| pick the right browser lane (4 exist: Replit Playwright Chromium, Hermes Chrome 145, agent-browser CLI, Camofox) | `references/browser-lanes.md` | `$REPLIT_PLAYWRIGHT_CHROMIUM_EXECUTABLE`, `.hermes/tools/chromium-1208`, `agent-browser`, `:9377` |
| run a desktop GUI app (AppImage/Tauri/GTK) headless — Xvfb, window manager, software GL, EGL/loader traps | `headless-gui-linux` skill | `start.sh`-style launcher, `xwininfo -root -tree` gates |
| tell whether a browser is being detected as a bot; test sites + how to read them | `references/anti-bot-detection.md` | (test pages: sannysoft, CreepJS, BrowserLeaks, NopeCHA) |
| compare every browser lane on this box (versions, loads, webdriver/stealth, WebGL) — full run report | `references/browser-compare-report.md` | `start-replit-chromium.sh`, `resolve-libs.sh`, `launch-hermes-chrome` |
| bridge CLI coding subscriptions (Codex/Claude Code/Antigravity/Gemini CLI/Kimi/xAI) into OpenAI+Claude APIs on the box | `references/cliproxy.md` | `setup.sh --cliproxy` |
| make an HTTPS client (Python, Node, git, uv) trust the Replit proxy without disabling verification | `references/tls-trust.md` | `setup/rc.sh`, `setup/common.sh` (TLS block) |
| expose a service to a browser (declared ports, port-in-URL, HTTP-only router, Tailscale userspace, `[[workflows]]` wiring, hardcoded binds) | `references/exposing-ports.md` | `.replit` `[[ports]]` / `[[workflows]]` |
| decide which ports may be public on Replit, and how to expose one (declared in `.replit`, edge opens only after a restart; supported list = 80, 3000-3003, 4200, 5000, 5173, 6000, 6800, 8000, 8008, 8080, 8081, 8099, 9000) | `references/public-ports.md` | — |
| serve a knowledge base to agents (llm_wiki desktop app headless + MCP over HTTP, read-only token, supervisor) plus a noVNC view of the real desktop UI | `references/llm-wiki-server.md` | `setup.sh --llm-wiki` (bundle: `scripts/llm-wiki/`), `run-public.sh`, `run-ui.sh`, `start-app.sh`, `llmwiki-server.js`. Port lewat `LLM_WIKI_PORT` (default 8319, 8080 milik dashboard; 8319 loopback-only, pakai 8081 untuk publik); client di mesin lain butuh tunnel ssh karena tailscale di sini userspace tanpa TUN |
| own the interactive shell (zsh + oh-my-zsh + powerlevel10k, durable dotfiles, rc wiring rules) | `references/shell-rc-and-zsh.md` | `scripts/setup/zsh.sh`, `scripts/setup/rc.sh`, `scripts/setup/common.sh` (tool-var registry) |
| host a browser-only web terminal / get a real shell on a second box, or reach a fresh disposable box from here | `references/remote-shell-bridge.md` | `scripts/setup.sh --remote-shell` (alias `--e2e`; prepares only: sshd key-only config + tailnet identity, persistent `~/.ssh`, prints one workspace-relative workflow task line) — `--start` launches the daemons, `--wf` = `--remote-shell --start` in workflow mode; set `TAILSCALE_NODE_NAME=<name>` inline on the workflow args (or a Replit secret) to pin the tailnet node name, otherwise the console name is left alone |
| add a tool or flag to `setup.sh` (the ~2 dozen call sites, repair/verify/clean, the rc-writer harness) | `references/setup-tool-checklist.md` | `setup.sh`, `scripts/setup/*.sh` |

Hermes-on-Replit recovery specifically (uv `--locked` trailing-slash failures,
official Node ≥22 tarballs needing libatomic): `references/hermes-on-replit.md`.

## The platform in seven facts (detail in platform.md)

1. **`$HOME` (`/home/runner`) is wiped on recreate; `$REPL_HOME`
   (`/home/runner/workspace`) is persistent.** Anything you want to survive
   lives under the workspace. The XDG vars are pre-set into the workspace, but
   do not trust that implicitly — check with `printenv | grep XDG_`.
   `~/.ssh` and `~/.local/bin` are NOT exceptions even though they usually
   exist and look aged: the boot script rewrites `authorized_keys` and
   re-publishes the launchers, so an intact file proves nothing — compare the
   *directory* mtime with uptime before trusting one. A tailnet node key under
   `$HOME` therefore re-registers on every boot (new `100.x`, new node name)
   and every saved URL / `.ssh/config` entry rots; keep node state in
   `$TAILSCALE_DATA_DIR` (`$REPL_HOME/.local/share/tailscale`), which
   `setup.sh --tailscale` / `--remote-shell` already use. A tool that insists on a
   `$HOME` path (`~/.ssh`, `~/.gnupg`) is **symlinked** into `$REPL_HOME`
   (move the existing dir's contents in first, then `ln -s`) — see
   `references/platform.md` §1.
2. **Daemons never autostart from a shell rc.** `.bashrc` / `.profile` /
   `$REPL_HOME/.config/bashrc` re-source on every terminal the operator opens,
   so a service line there re-fires per terminal and needs a fresh guard in
   each shell. Long-running services (`sshd`, `tailscaled`, the llm-wiki stack)
   go in a `.replit` `[workflows]` entry, which runs once per boot — added in the
   Replit UI by the operator from one printed command, not written into
   `.replit` by the installer: names and ordering stay theirs. rc carries
   PATH/env only. See `references/shell-rc-and-zsh.md`.
   **The installer's whole notice is that one command line, with the path made
   relative to the workspace** (workflows run with the workspace as cwd, so a
   moved/renamed skill dir cannot leave a dead absolute path). When an entry
   already exists, verify the path it names BEFORE checking for its extra flags —
   otherwise a dead path hides behind the "already wired" branch — and grep only
   the line that carries the app's own flag, since other workflows point at the
   same script. Corollary for code: a
   workflow's `args` must point at a **persistent and workspace-relative** path
   (the skill dir under
   `$REPL_HOME`), never at a script copied into `$HOME`, and it must be
   idempotent — re-running is the normal repair path, so skip a live daemon
   instead of killing it (killing `tailscaled` cuts the very SOCKS hop the
   current `ssh` runs over).
3. **Everything system-level comes from `/nix/store`, and store paths get GC'd.**
   A path that worked yesterday may not exist today; long-lived things need a
   durable copy outside the store (see nix.md, hermes-on-replit.md).
4. **`$REPLIT_LD_LIBRARY_PATH` is never enough** for GUI browsers — you need
   the full transitive closure (nix.md §3; `scripts/setup/generate-closure.sh`).
5. **npm is behind a package firewall**; pin `--registry=https://registry.npmjs.org/`.
   It can reject a transitive dependency outright (`403 ... Blocked by Security
   Policy` on a CVE-flagged package), and only the *dev* tree pulls the usual
   offender. This shell also exports `NODE_ENV=production`, and npm then silently
   omits devDependencies — `tsc: command not found` is the tell. Prefix installs
   and builds with `env -u NODE_ENV`.
6. **Replit ships a Playwright-managed Chromium** — `$REPLIT_PLAYWRIGHT_CHROMIUM_EXECUTABLE`;
   never `playwright install`.
7. **Disk splits 4 GB / 256 GB — big files only on the workspace volume.**
   `$HOME`, `/tmp` and `/mnt/scratch` are each a ~4 GB overlay/tmpfs (`/tmp`
   and `/mnt/scratch` are RAM); `$REPL_HOME` is the 256 GB volume and
   `$XDG_DATA_HOME` (`/home/runner/workspace/.local/share`) sits on it, while
   the `~/.local/share` spelling does not. Download anything over a couple of
   GB to `$XDG_DATA_HOME/<slug>/`, never to `/tmp`, `/mnt/scratch` or `~/`.
   See `references/large-files-disk.md`.

Prefer **`rg`** over `grep` when searching the box or this repo (recursive,
gitignore-aware, far faster); it is on PATH and also staged under
`$HERMES_HOME/tools/ripgrep-*`. Use `grep` only in scripts that must run
without ripgrep.

## Scripts (entry point in `scripts/`, modules in `scripts/setup/`)

- `setup.sh` — thin entry point: mode/path/version config, then `source`s the
  modules in `scripts/setup/` (`common` → `ui_menu`/`bin`/`fix`/
  `rc`/`doctor`/installers/`cleanup` → `cli`). All wiring helpers resolve via
  `$SCRIPT_DIR`, so every module and `setup/` must sit beside `setup.sh`.
  It is idempotent toolchain/env provisioning (node/uv/python pins, LD
  paths, rc chain); run it after any recreate. `--doctor` verifies installs +
  wiring read-only (exit 2 = wiring gaps); `--fix` rewrites ALL wiring
  with zero downloads/reinstalls — safe after a $HOME wipe or a partial
  recreate. `--doctor --fix` = report then repair. Re-running `--fix` is a
  byte-identical fixed point.
  - **Install isolation:** each tool installs in its own step
    (`run_install_step`); one failing tool warns and the run CONTINUES to the
    rest, then lists the failures and exits non-zero. `--all` no longer aborts
    at the first broken installer.
  - **Clean safety:** `--clean` prints a pre-flight list of exactly what will
    be removed; tools that own user data are protected — `hermes` is backed up
    with its own CLI (`hermes backup`, restorable via `hermes import`), the
    archive copied to `$XDG_CONFIG_HOME/hermes/hermes-backup.zip` (OUTSIDE the
    removed dir) first and left intact if the backup fails (manual-zip
    fallback when the CLI is unavailable); ollama models + camofox server state
    are preserved; cliproxy keeps config/OAuth logins. A bare non-interactive
    `--clean` is REFUSED (use `--clean all -y`).
  - **Conflict-free installs.** A box normally ALREADY has the tool: hand-installed
    into some arbitrary directory, symlinked onto PATH, often with a `.replit`
    workflow running that copy. The managed install must win without breaking any
    of it — ADOPT the existing user data/state rather than re-initialising it (so
    nothing needs re-auth and no config is lost), make every script and workflow
    that runs the tool prefer the managed binary, report a foreign symlink before
    replacing it, and never leave the old copy silently in charge while `setup.sh`
    reports success. Audit all four sites: `$XDG_BIN_HOME/<bin>`,
    `$XDG_DATA_HOME/<tool>/`, the `.replit` workflow `args`, and any operator
    script that hardcodes a path.
  Pitfall encoded in the script: `--fix` never execs the `hermes` launcher —
  any subcommand can boot the full source-update cycle (venv sync, npm build,
  GB-scale runtime clone). config.yaml is edited with `yq -i` when available
  (awk fallback), then verified. `--cliproxy` installs CLIProxyAPI (its
  `$CLIPROXY_HOME` follows XDG: `$XDG_CONFIG_HOME/cli-proxy`, honoring a
  legacy `$REPL_HOME/cli-proxy`) — see `references/cliproxy.md`;
  `--clean cliproxy` keeps config + OAuth logins.
  `--camofox` installs the **npm-global** Camofox browser
  (`@askjo/camofox-browser` + `camofox-browser-mcp` on PATH, engine in
  `$XDG_CACHE_HOME/camoufox`), applies the Replit lib closure + WebGL
  auto-skip, and writes a runtime env snippet **plus a launcher shim**
  (`$XDG_BIN_HOME/launch-camofox-browser`) for shells that cannot source it
  — workflows, the Run button, MCP/cron children. **A bare `camofox-browser`
  in those shells dies on `libgtk-3.so.0: cannot open shared object file` and
  surfaces as an opaque 500 on cookie import**; use the snippet or the shim.
  See `references/camofox.md` §"npm-global lane".
- `dot_replit.py` — structural `.replit [userenv]` edits (tomlkit, no regex).
  - Verify the pin after every `--fix`: `write_replit_bashrc` needs tomlkit (from `.venv`, `python3`, or `uv`). On a fresh box none of them has tomlkit, so the function prints `python tomlkit not found, write REPLIT_BASHRC manually` and still returns 0. That is a failure: workflow shells then lack the line and break silently. Check with `grep REPLIT_BASHRC $REPL_HOME/.replit`. Install tomlkit into `.venv` before running `setup.sh --fix` on a fresh machine, or add the line by hand under `[userenv.shared]`.
- `camofox.py` — the scraping CLI (open/nav/eval/screenshot, cookie import,
  keep-alive loop). See camofox.md for its env-file contract.
- `scripts/setup/generate-closure.sh` / `libpool.sh` — transitive lib closure (per-process) + pool healing (additive-only).
- `$XDG_BIN_HOME/launch-camofox-browser` — **generated at install** (not a repo
  file): sources the closure `env.sh`, preflights the install, then execs
  `camofox-browser`. The entry point for any shell that cannot inline the
  snippet — `.replit` workflows, the Run button, cron/MCP children.
- `tests/camofox_mcp_check.sh` — one-shot MCP health probe (waits for REST, runs a
  real stdio handshake, asserts the 11 `camofox_*` tools; exit 0 = live). Used
  by the `.replit` "camofox mcp" workflow — the adapter itself is stdio-only,
  running it standalone just idles forever.

## Maintaining this skill (verify, don't trust the edit tool)

- Changes to this skill's repo go on a feature branch in a `.worktrees/<name>` worktree and open a PR for review. Never commit directly to `main`.
- PRs here are **squash-merged**, so a branch's commits never become ancestors of `main`. Two consequences: after a merge, `git rebase origin/main` before opening a follow-up PR, or its diff re-lists the work that already landed (GitHub shows the old commits plus a duplicate change); and if the PR merges while you are still editing, the later commits are stranded on a merged branch — branch off the tip, rebase onto `origin/main`, push that new branch. Confirm with `git diff --stat origin/main..HEAD` that the PR carries only the intended files before you describe it.
- Test against the live target before committing, and commit only after a passing run. Delete throwaway test scripts and key files first, so the PR holds only the fix.
- Keep every commit to your own files. When the tree carries the user's uncommitted edits (a bullet, a whole new reference file), stage by PATH and never `git add -A`; when their hunk sits in a file you also have to edit — SKILL.md is the usual meeting point — save the file aside, patch their hunk out, commit your change, then restore theirs so it stays uncommitted. Commit their work only when they ask, as its own commit whose message describes their change.
- Close the loop on a merged PR: delete its branch locally and on the remote, and remove any worktree it used. The user treats leftover branches and worktrees as clutter to be cleared, not as history to keep.
- Adding or changing a tool flag touches roughly two dozen places in eight files. Work `references/setup-tool-checklist.md` in order and run its test sequence: a half-wired flag does not error, it is invisible, or the tool installs and then cannot be repaired or cleaned.
- Never write a silent fallback (`except ImportError: pass`, a default that hides a failed dependency or trust store). Fail with the name of what is missing; a silent pass hid the real TLS cause here.
- **Retiring a tool var is not "stop registering it".** Dropping the name from `wire_tool`/`record_tool_env_vars` leaves the old `export NAME=` line in place: `emit_managed_block` re-adopts every export it finds inside its own markers and re-emits it, so an inherited value keeps the line alive forever. Add the name to `_FIXED_RC_ENV_VARS` (the suppress list) with a comment saying why — that drops the stale line on the next write and stops it coming back.
- **Per-machine identity does not belong in the rc at all.** A var that describes *this* box (a tailnet node name, a chosen port) is the operator's decision, pinned at the call site — the workflow `args` or a Replit secret — so the script reads it from the env and never writes it into every shell. Only paths identical on every box get exported.
- **Mask a secret wherever the script echoes it.** Tools print their own argv (`tailscale up` includes the auth key verbatim), so pipe such output through a filter before the terminal sees it: `| sed -E 's/(tskey-)[A-Za-z0-9_-]+/\1***/g'`.
- **Only path vars belong in the rc registry; a human choice stays out of it.** A var one operator sets differently per box (node name, persona) is pinned where that machine is described — the workflow `args` or a Replit secret — and read from the environment at use. The managed block re-emits whatever it finds, so once the var has lived in the block it is re-adopted forever; retiring it from `wire_tool`/`record_tool_env_vars` is not enough, add it to the retired list in `rc.sh` or an inherited value resurrects the export on every write.
- **One variable per thing: drop a legacy alias, keep the CLI flag alias.** The old flag spelling is worth keeping as a dispatch alias, but a parallel `OLD_VAR:-NEW_VAR` fallback in the env is not — it hides which one is live and doubles every place the operator must set.
- **Mask secrets in anything streamed or logged.** `tailscale up` echoes the full auth key in its own output; pipe through `sed -E 's/(tskey-)[A-Za-z0-9_-]+/\1***/g'` before it reaches the terminal or a log.
- **Inside a quoted heredoc (`<<'PY'`) do not escape quotes.** Bash passes the text verbatim, so `\"` reaches python as backslash-quote; the same `\"` copied into a shell-level `grep 'name = \"x\"'` then matches nothing, because a single-quoted pattern keeps the backslash. Write plain `"`, and `bash -n` the file after any block-level rewrite.
- **Deleting a directory the box used to run starts with a config sweep, not `rm`.** Grep the config surface for absolute paths into it — `.replit` workflow `args` and `waitForPort`, `$REPLIT_BASHRC`/rc files, `~/.ssh/config`, operator scripts — because a workflow pointing at a removed script still reads as wired and fails only at the next boot, silently (the job is reaped at once). Check whether the path was already dead before the delete: a directory can be gone while two workflows still name it, which is how stale wiring hides. Move the identity/config that must survive (a pinned node name, a port) into the surviving workflow's `args`, never into an rc.
- **Renaming a flag or token is the same sweep, run the other way.** Every site that spells the old token moves in one commit: usage/help, arg parser, cleanup dispatch, menu label plus its mapping, workflow `args` (migrate in place, `sed -E` on the token only), docs and the skill's own tool row. Two per-site constraints: rename a workflow `name` only when nothing else already holds the new name (Replit drops one of two identical names), and leave a state DIR at its old name when moving it would mint a new host key — every client's `known_hosts` then warns. Keep the old flag spelling as an accepted alias so existing `.replit` entries and the operator's habits still work, then verify with `grep -rn '<old>' scripts/ docs/ skills/`: whatever survives must be an intentional alias or a path you chose to keep.
- **Derive a path once; consumers read it from the environment.** A var computed from another (`XA_STATE_DIR` off `XA_DATA_DIR`, the socket inside the state dir) is assigned in `common.sh` alone, and every consumer takes `$XA_SOCKET` from the env instead of re-spelling `$XA_DATA_DIR/state/...` — one re-spelled site is enough to drift the next time the layout moves. Register such vars in the installer **and** in the repair path (`--fix`): a var wired only in the installer evaporates the first time someone repairs instead of installs, which is also why `--doctor` should warn when the export is missing from the rc block.
- **A worktree branch cannot see edits sitting uncommitted in the main checkout.** The worktree shares `.git` but has its own files, so doc or config edits made in the main checkout belong to no branch: the PR from the worktree silently misses them and the later `git pull` into main aborts on the dirty file. `git status` the MAIN checkout before merging; when something is stranded, re-apply it on top of the freshly pulled `origin/main` as a follow-up commit — not a stash pop, because the rename probably moved the file it was written against.
- **A heredoc'd helper inside a shell script must not carry backslash escapes.** Inside `<<'PY'` a backslash is literal, so `\"` reaches Python as an escaped quote (survivable) and reaches a shell-level `grep -qF 'name = \"x\"'` as a literal backslash, which then never matches. Keep quotes raw inside the heredoc and re-read the block with `sed -n '<a>,<b>p'` after patching — `bash -n` passes happily on a pattern that matches nothing.

When one batch touches many files or repeats an `old_string`, VERIFY the effect
on disk before moving on:

- `rg` the new text (a "failed"/"no match" line can be a benign duplicate-key
  retry) and confirm it appears the expected number of times — twice means the
  edit applied twice.
- **Never compose a `sed -E` script by hand once it contains quotes or `\1`**: run the
  exact expression on a scratch copy first. Two failures in a row (`|` rejected as the
  delimiter; `(--start)?` written where the text has a space, so the pattern silently
  never matched while `rc=0` claimed success) look identical to a logic bug, and the
  script "succeeds" without editing anything.
- **`sed -ed -i f1 f2` mengosongkan KEDUA file.** `-ed` menempelkan `d` ke script, jadi setiap
  baris dihapus (`wc -l` = 0) dan `rc=0` tetap terlihat sukses. Tulis `sed -e 's#a#b#' -e 's#c#d#' -i f1 f2`,
  dan `wc -l` tiap file tepat setelah edit multi-`-e`. Pemulihan: `git checkout -- <file>` — patch
  yang belum di-commit di file itu ikut hilang, jadi siapkan untuk meng-apply-ulang.
- Pass **absolute** paths: a `cd` from a previous terminal call persists, so a
  relative path can resolve against the wrong directory.
- Trust base after any edit: `bash -n` on every module (the setup.sh syntax gate
  runs the same check), `shellcheck -S warning` on changed files, and re-run the
  module harness.

## Camofox public access

- With `CAMOFOX_ACCESS_KEY` set, every route except `/health` requires `Authorization: Bearer <access key>`. A browser address bar cannot send that header, so `{"error":"Unauthorized"}` in a browser means the gate works. It is not a fault.
- The global gate checks the access key only; `CAMOFOX_API_KEY` gets 401 on `/tabs`. Cookie import is the reverse: `POST /sessions/<u>/cookies` checks the API key only, so the access key gets 403 there. `camofox.py` sends the access key everywhere except cookie import, which uses the API key.
- Removing the access key opens every route to anyone with the URL. Never do that to clear a 401 on a public server.
- A public test goes through the public URL with a header-capable client (`curl` or `camofox.py`). A localhost pass proves the server works, not the proxy path.
- Keep TLS verification on in every client. Diagnose a public failure in this order: `curl -sS https://<domain>:<port>/health` (verified) first, then `curl -sk` (skip verify). If the verified call fails with curl error 60 and the `-k` call returns 200, the server is fine and this client's trust store lacks the Replit proxy root CA (see the bundle rule below); a `502` from the domain means nothing listens on that port. Run the verified call before naming any cause. A client with verification off proves reachability only; never report it as a pass for auth or the tool path.
- curl and Python can trust different stores on the same box. curl reads `/etc/ssl/certs/ca-certificates.crt`, which holds the Replit proxy root; Python's default context has `cafile=None` and only `capath=/etc/ssl/certs`, so the identical URL fails with `CERTIFICATE_VERIFY_FAILED`. Fix it in the client: `ssl.create_default_context(cafile='/etc/ssl/certs/ca-certificates.crt')` and pass `context=` to every `urlopen`. Confirm the root is in that bundle with a verified `curl` (no `-k`) first. certifi's bundle lacks the proxy root, so `certifi.where()` does not fix it. Do not disable verification; `PYTHONHTTPSVERIFY` is not a Python setting and does nothing. The per-client variable table (Node, Python `urllib`/`httpx`/`requests`, git, uv) and the generator fix are in `references/tls-trust.md`.
- Node has the same split, and `NODE_OPTIONS=--use-system-ca` alone is not enough. `NODE_EXTRA_CA_CERTS` overrides the system store, and the Nix bundle it often points at lacks the proxy root. Set `NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt` for the MCP adapter and any `fetch` client, and keep verification on. Confirm with `fetch(url)` in the same environment before running the adapter.
- `camofox.py` prints "not ready" for every probe failure, including certificate errors. To see the real exception, run `camofox.req(None, 'GET', '/health')` with `CAMOFOX_BASE_URL` set; the `_error` field names the cause.
- The Camofox MCP adapter reports every network failure as `camofox error: fetch failed`, which hides the TLS cause. If `tools/list` works but tool calls fail with that text, the adapter's `fetch` cannot verify the proxy, not the server. Fix the client trust store (above), then rerun the tool call.
- Read a Replit secret into a shell variable with `replit secrets exec --keys NAME -- sh -c 'printf %s "$NAME"'`. The `--` form is required; without it the output is empty and looks like a missing key. `--keys` takes a COMMA-SEPARATED list (`--keys A,B`, or the flag repeated) — passing the names as separate arguments makes the second one the command to exec, which surfaces as `exec: "B": executable file not found in $PATH`.
- A key copy in `.hermes/.env` can differ from the Replit secret. When `/tabs` returns 401 with a key you believe is correct, compare SHA-256 prefixes of both values (never print them) before blaming the server.
- A public port must appear in `.replit` `[[ports]]` with matching `localPort` and `externalPort`, and the server must bind `0.0.0.0` on that port. The URL always carries the port (`https://$REPLIT_DEV_DOMAIN:<port>/`) — only one port can be the default, so a bare domain hits 80 and 502s when nothing listens there. The platform OWNS that list — a hand-appended `[[ports]]` entry gets re-serialized away and the service then 502s while the file looks right, so register a port by starting the listener and loading `https://$REPLIT_DEV_DOMAIN:<port>/` once, and trust the proxied response over the file. The router is HTTP(S)-only, so a non-HTTP protocol (sshd, a DB port) cannot be exposed this way at all. Serve a service on a port nothing else owns: two `.replit` workflows sharing a `waitForPort` cannot both bind, and the Hermes dashboard defaults to 8080, so a second service there silently loses the bind. **Check the port owner before debugging the service**: if `/health` answers with someone else's body (the dashboard returns 302 + `{"error":"unauthenticated",...,"login_url":"/login"}`), your listener never got the port — pick a free declared port and re-point every client at it. Details: `references/exposing-ports.md`.
- Start the server with its env loaded, never with a bare `node server.js` from a shell that has not sourced `$XDG_CONFIG_HOME/camofox/env.sh`. Without it the browser lacks the GTK/X11 library path and fails with `browserType.launch ... libX11-xcb.so.1`; every tab call then returns `503 browser_launch_timeout`. Load secrets in the same command, e.g. `replit secrets exec --keys CAMOFOX_ACCESS_KEY,CAMOFOX_API_KEY -- sh -c '. $XDG_CONFIG_HOME/camofox/env.sh; node server.js'`, with `CAMOFOX_BIND_HOST=0.0.0.0`, and confirm the port is in `.replit` `[[ports]]`.
- Stop a Camofox server that a `.replit` workflow manages through the workflow in the Replit UI. A `kill` of `node server.js` is undone by the workflow, which relaunches both the server and `camofox-browser-mcp`. Kill by explicit PID only; a `pkill -f` pattern can match the calling shell.
- In a test, a 400 on an empty `/tabs` body means the gate passed. A `503 browser_launch_timeout` is a server-side browser launch failure, separate from auth.
- Separate the gate's status from the target page's status. A gate rejection is the server's own JSON error: `{"error":"Unauthorized"}` (401) or `{"error":"Forbidden"}` (403). A `/tabs` call that passes the gate returns 200, and the target page's status is in the `httpStatus` field (for example 404 or 403 from the site). Read `httpStatus` before blaming auth.
- A cookie-import 403 with the correct client code means the running server's keys differ from the secret. The server reads `CAMOFOX_API_KEY` and `CAMOFOX_ACCESS_KEY` only at startup, so changing a Replit secret does nothing until the server restarts. Compare key lengths (never values) between the secret and the server's environment, then restart the server with the same values and retry.
- A `.replit` workflow runs `camofox.py` from its own path. After a fix merges, pull the clone that path points at; a local clone at an older commit runs the old code and reproduces a fixed bug. Check `git log -1 -- <file>` in that clone before debugging the code.
- `env -i` empties PATH, so a following `timeout python3` fails with `No such file or directory`. Pass the absolute interpreter (`PY=$(command -v python3)`) when running in a clean environment.
- **Never assign `PATH` a literal value in an agent shell.** Terminal state persists across calls, so `export PATH=/one/dir:/usr/bin:/bin` (to reach a single tool) silently drops the Nix and `$XDG_BIN_HOME` entries for every LATER call: `python3`, `replit`, `uv` and the platform toolchain then fail with `command not found` several steps after the edit, pointing nowhere near the cause. Append (`PATH="$PATH:<dir>"`) or export into a file under `$HERMES_HOME/cache/scratch/` and `. that-file` at the top of later calls. Recover by reading the platform PATH from a fresh login shell (`bash -lc 'printf %s "$PATH"'`) or re-sourcing the rc.
- **Lost `replit`? It is a Nix store path, not a stable location**: `/nix/store/*replit-cli-*/bin/replit` (plus `-runtime-path/bin` for the platform toolchain). Re-derive it rather than concluding the CLI is gone.
- `env -i bash -lc` does NOT reproduce a Replit shell: it drops `REPLIT_BASHRC`/`REPLIT_MODE`, so the rc chain never sources and the shell looks like it has no aliases or exports — a false failure. To test rc output, run a normal login shell with the variable under test stripped from the inherited PATH instead: `PATH=$(echo "$PATH" | tr ':' '\n' | grep -v 'installs/.*/venv' | paste -sd:) bash -lc '...'`.

## Setup-script env rules (`setup.sh`, `setup/rc.sh`, `setup/common.sh`)

- **Credentials are read from the environment, never baked into a script.** The
  user treats a token quoted into chat or hardcoded in an installer as leaked
  (they rotate/revoke it right after). Take `TAILSCALE_AUTH_KEY=… setup.sh --remote-shell --start`
  style input, and make everything after the first run work off the stored state
  so no second secret is needed. Printing a usage line with a placeholder
  (`tskey-auth-...`) is correct; printing the value is not.
- **A flag that launches a daemon must be separable from the one that prepares.**
  Bundling both means every prepare re-fires listeners and nothing can be inspected or
  repeated without side effects. Split it: the preparing flag (`--remote-shell`) writes config,
  keys, dirs and binaries, prints the follow-up command and exits; the launching flag
  (`--start`) is what brings daemons up; workflow mode (`--wf`) asserts both. A guard file
  or a "skip if alive" check is not a substitute — after the split, the prepare path must
  not call `setsid`, `start_*` or anything else that binds a port.
- Export only what the script owns. Replit already provides `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, and `XDG_CACHE_HOME`; re-exporting them adds nothing. `XDG_BIN_HOME` is the one PATH entry the toolchain owns, always `$REPL_HOME/.local/bin`.
- `HERMES_HOME`, `HERMES_MANAGED_DIR` and the launcher dir are ORDINARY wire-registered tool wiring in the single managed toolchain block (`wire_tool hermes` + `record_tool_env_vars` / `record_tool_path_dirs`, mirrored in `install_hermes` and `fix_derive_wiring`). Never give a tool its own rc block outside the managed markers: a second block has to be re-appended after EVERY rewrite to keep PATH precedence stable, `strip_tool_wiring` cannot see it, and a run that does not install that tool silently drops its lines (the pre-merge `hermes-tools` block had all three problems; `lift_legacy_hermes_wiring` / `strip_legacy_hermes_block` migrate such an rc in one pass). The managed-scope dir defaults to `/etc/hermes`, which does not exist and cannot be created on Replit (`/etc` is a read-only mount, no root), so it is pinned under `$HERMES_HOME/managed`. Keep `HERMES_HOME` OUT of `_FIXED_RC_ENV_VARS`: that list suppresses the tool-var export, which is now the only thing that emits it.
- The only Hermes PATH entry is `$HERMES_HOME/hermes-agent/.hermes/bin` (the stable launcher; it resolves the correct environment itself). Never add `installs/*/environments/*/venv/bin` or `hermes-agent/venv/bin`: those venvs belong to an isolated session run, are not stable across sessions or updates, and a public shell that picks one up calls a binary from a session that may not exist.
- **A service you deploy here must not fall back to a Hermes-managed binary.** `$HERMES_HOME/tools/*` (node, python, ripgrep...) is Hermes' private install: it moves on `hermes update` and disappears with `--clean hermes`, Hermes strips `LD_LIBRARY_PATH` from child processes it spawns (MCP children, terminal children), and on this box those tarball binaries link `libatomic.so.1`, which lives only in `/nix/store`. A wrapper that ends with `command -v node` therefore picks the broken one and the failure surfaces far away as `Connection closed` or a bare exit 127. Pick candidates explicitly (`$VAR`, `$XDG_BIN_HOME/node`, `/usr/local/bin/node`, `/usr/bin/node`), reject any path containing `/.hermes/`, and **fail loudly with the reason** instead of falling through — a silent fallback is what made this take three sessions to find.
- Never put `$HERMES_HOME/tools/*` on the user PATH either. Those dirs (node, npm, python, uv, gh, ffmpeg, ripgrep) are the agent's managed install: `hermes update` replaces them and an uninstall or `--clean hermes` deletes them, so a global install in a user shell follows the binary into Hermes' prefix and dies with Hermes (`npm i -g <pkg>` → `$HERMES_HOME/tools/npm-*/...`), `pip` follows Hermes' interpreter, and PATH order silently decides which node/python a user's script ran under. An rc block that mirrors them looks convenient and is a data-loss trap. User shells get the platform toolchain (`.replit` nodejs-24 / python3.13 modules + `$XDG_BIN_HOME`); Hermes runs its own binaries from its own PATH and does not read the rc.
- Do NOT delete the user-bin launcher forwarders (`hermes`, `hermes-acp`, `hermes-agent` in `$HOME/.local/bin`). Hermes publishes them itself (`_launchers.py::expose_cli` → `_publish_conveniences`) and re-creates them on every install/update, so removing them is futile; and `hermes-agent` exists ONLY as that forwarder (`.hermes/bin` stages `hermes` + `hermes-acp` only), so removing it deletes the command outright. The forwarders exec the durable `$HERMES_HOME/hermes-agent/.hermes/bin/*` launcher, not an ephemeral path — check whether the framework owns and republishes a file before treating it as stale clutter.
- Every tool's wiring has to exist in THREE places, or it is half-wired: the installer (`record_tool_env_vars` / `record_tool_path_dirs`), `fix_derive_wiring`, and a `doctor` gate. `fix_derive_wiring` is what makes `--fix` able to rebuild the line on a box where that tool is present but is not being installed this run; without that branch `--fix` silently cannot restore it, so the wiring survives only until something rewrites the rc. Gate the doctor check on the block's CONTENT (`grep -qE '^export[[:space:]]+ZDOTDIR=' "$BASHRC"`), never on a marker or on a file existing — a marker check passes while the export is gone.
- Do not define `XDG_STATE_HOME`. No script reads it, so it is dead config.
- Point the TLS variables at the platform store, never at `$SYSTEM_CERTIFICATE_PATH`. `SSL_CERT_FILE`, `SSL_CERT_DIR`, `NODE_EXTRA_CA_CERTS` and `REQUESTS_CA_BUNDLE` come from `/etc/ssl/certs/ca-certificates.crt` when it is readable. The Nix cacert bundle has **none** of the Replit roots (0 Replit-named subjects vs 2 in the system bundle: "Replit internal proxy Root CA …", "Replit Localhost Development CA"), so wiring it in replaces a store that knows the proxy with one that does not — public hosts keep answering 200 while proxied ones fail — and being a `/nix/store` path it can be GC'd into a missing `SSL_CERT_FILE`, which breaks every TLS client outright. `NIX_SSL_CERT_FILE` is deliberately not set: nothing we run reads it and nix resolves its own cache without it.
- Never set `npm_config_dangerously_allow_all_scripts`. It bypasses npm's install-script review for every install (upstream: "strongly discouraged"), including packages explicitly denied. npm ≥ 12 blocks unapproved dependency install scripts while npm 10/11 only warn, so the flag buys nothing on a box running npm 11 and silently disables the guard the moment npm 12 shows up. Allow scripts per project: `allowScripts` in `package.json`, or `npm approve-scripts`.
- Generated `hermes` aliases call bare `hermes`, not `$XDG_BIN_HOME/hermes`. The managed block registers the real launcher dir (`$HERMES_LAUNCHER_DIR` = `$HERMES_HOME/hermes-agent/.hermes/bin`), which is the only provider of `hermes` / `hermes-acp` on this box, so bare `hermes` resolves there — or through Hermes' own `$HOME/.local/bin` forwarder, which execs the same binary. A `$XDG_BIN_HOME/hermes` alias points outside both.
- Verify generated rc output before committing: call the emitter directly (`emit_managed_block` with `REPLIT_MODE=true`), `bash -n` the output, grep for the removed names, then source the output in a clean shell and run each alias. A text check passes an alias that cannot run.
- Prove idempotence and no-duplication, not just validity. Run the writer twice and require an identical `md5sum` (a fixed point means the strip/append seam is clean and the file will not churn on every run), and in a clean shell source the rc TWICE counting each entry: `printf '%s\n' "$PATH" | tr ':' '\n' | sort | uniq -c`. An unguarded prepend doubles on the second source while a guarded `case ":$PATH:" in *":dir:"*)` stays at 1 — a single-source check cannot see that difference, and on this box the rc IS sourced more than once per shell (platform bootstrap, the `REPLIT_BASHRC` shim, nested agent shells).
- Double-quote any alias whose body uses a variable, so the variable expands at definition: `alias oc="$XDG_BIN_HOME/opencode"`. Single quotes keep `$VAR` literal, and the alias then fails when called. In a quoted heredoc (`<<'EOF'`) write `$VAR` bare; a backslash is written into the file as-is.
- The block text in `emit_managed_block` sits in an UNQUOTED heredoc (`<<EOF`), so `$VAR` expands at emit time and **backticks or `$(...)` inside it execute**. A backtick pair in a comment (`` `npm i -g` ``) ran `hermes`/`hermes-acp` at emit time, which then hung the whole `setup.sh` run waiting on stdin. Write emitted prose without backticks; escape (`\$VAR`) anything that must reach the file literally. Test the emitter against a COPY of the rc and with stdin closed (`</dev/null`) before running it for real: with `BASHRC` unset, the strip step's `awk "$BASHRC"` reads **stdin** and blocks forever instead of failing. After an emit, grep the file for a stray backtick and the log for `command not found` — those are the fingerprints of a comment that ran (a stray `` `npm approve-scripts` `` in a comment is enough to make `npm` execute during `setup.sh`).
- Test an alias from a sourced file, not on the line that sources it: bash parses the file's aliases only after that line. Run `shopt -s expand_aliases`, then `source rc.sh`, then the alias on its own line.
- Registry settings in the emitted block are plain exports, not `${VAR:-default}`, so the public registries win over a firewall value set earlier. `PIP_TRUSTED_HOST` is also a plain export.
- `--fix` runs the `setup/` code of the checkout it is launched from. Run it from the branch under test. A `main` checkout re-emits the old block, so the live `.config/bashrc` will not show a fix that is still in review.

## Camofox tuning

There is no env-file template to ship — **the interface is exported vars**
(`CAMOFOX_PORT`, `CAMOFOX_ACCESS_KEY`, `TAB_INACTIVITY_MS`, ...), read from the
shell (or exported before `camofox-browser`):

```bash
CAMOFOX_PORT=9000 CAMOFOX_ACCESS_KEY="$(openssl rand -hex 32)" camofox
```

The Camofox tunables (with defaults) are documented in `references/camofox.md`.

## Installing this skill pack

One skill, one command:

```bash
npx -y skills add skynight137/skills -s replit
```
