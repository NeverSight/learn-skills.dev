---
name: autoupgrade-icp-cli
description: One-time installer that keeps a project's Internet Computer CLI toolchain current. Sets up a SessionStart hook plus a script that compares the installed `icp` and `ic-wasm` against the latest release and either reports the upgrade or applies it, using whichever channel each tool was installed from (npm, Homebrew, or the shell installer). Use when a user wants to install, bootstrap, or enable automatic icp-cli / ic-wasm updates, asks to stop running an outdated `icp`, asks how to upgrade or check the version of the ICP CLI, or pastes the link to this skill. This is a one-time setup action, not ongoing IC knowledge. Do NOT use for writing icp.yaml, deploying canisters, or other icp-cli usage questions — load `icp-cli` for those.
license: Apache-2.0
compatibility: "curl, bash; network access to github.com (and formulae.brew.sh for Homebrew installs)"
metadata:
  title: Automatically Upgrade the ICP CLI
  category: Infrastructure
---

# Set up automatic `icp` CLI upgrades

A **one-time installer**: it adds a `SessionStart` hook that checks whether `icp` and
`ic-wasm` are current and — if the user wants — upgrades them before work starts. Once
these steps are done the user never needs this skill again.

`ic-wasm` is covered alongside `icp` because the official recipes (`@dfinity/motoko`,
`@dfinity/rust`, `@dfinity/static-site`, `@dfinity/asset-canister`) invoke it on every
build. An `ic-wasm` left behind while `icp` moves forward produces build failures that
read as recipe bugs, so upgrading only one of the pair is the worse default.

`icp` has its own check (`icp settings update-check`) that is worth leaving on, but it
only speaks once the user runs an `icp` command — by which point the agent has already
chosen what to write. This hook runs before the session's first prompt, so the version
reaches Claude's context up front, and it covers `ic-wasm` too.

## Step 1 — Ask the user which mode they want

The installer cannot make this call for the user, so ask before writing anything:

> "Two options for how the hook behaves when a newer version exists:
> **notify** — it prints the versions and the exact upgrade command, and nothing is
> installed until you run it. **auto** — it runs that upgrade itself at session start.
> Which do you want? You can switch later by editing one flag in the hook."

Default to **notify** if the user has no preference — it is the reversible choice.

Also tell them what adding a hook means, and do not attempt to bypass the approval:

> "I'm adding a `SessionStart` hook that runs `.claude/upgrade-icp-cli.sh`. Claude Code
> will ask you to approve/trust it before it runs automatically."

## Step 2 — Check prerequisites

```bash
command -v curl   >/dev/null 2>&1 && echo "curl: ok" || echo "curl: MISSING"
icp --version     2>/dev/null     || echo "icp: not installed"
ic-wasm --version 2>/dev/null     || echo "ic-wasm: not installed"
```

If either tool is missing, mention the install command
(`npm install -g @icp-sdk/icp-cli @icp-sdk/ic-wasm`) but do not run it unprompted —
installing a toolchain is a different decision from keeping one current.

## Step 3 — Download the script

Fetch the published script verbatim rather than transcribing it, so the channel
detection stays correct as it is updated upstream:

```bash
mkdir -p .claude
curl -fsSL https://skills.internetcomputer.org/.well-known/skills/autoupgrade-icp-cli/scripts/upgrade-icp-cli.sh \
  -o .claude/upgrade-icp-cli.sh
```

Do **not** hand-write or paraphrase it.

## Step 4 — Register the SessionStart hook (idempotently)

If `.claude/settings.json` does not exist, create it with the content below. If it
does, **merge**: preserve every existing key, hook, and permission, add the
`SessionStart` entry only if an equivalent `bash .claude/upgrade-icp-cli.sh` command is
not already there, and write the parsed JSON back. Never overwrite the file.

**Notify mode** (the default):

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "bash .claude/upgrade-icp-cli.sh --mode notify" }
        ]
      }
    ]
  }
}
```

**Auto mode** — same entry with `--mode auto`, plus a raised `timeout`, because
installing a CLI binary can exceed the default 60 s and a timed-out install leaves the
tool half-written:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "bash .claude/upgrade-icp-cli.sh --mode auto", "timeout": 300 }
        ]
      }
    ]
  }
}
```

Whenever you hand someone an auto-mode hook, say the thing that makes it a real
choice: it upgrades the build toolchain **while a project is open** and blocks session
start while it runs, so a session can begin against a different `icp` than the last one
ended with — which can change build behaviour and output for a project that built fine
yesterday. That is what some teams want and what others pin against.

## Step 5 — Run it once, verify, report

```bash
bash .claude/upgrade-icp-cli.sh --mode notify   # or --mode auto, matching the hook
```

Silence means both tools are current — that is the success case, not a failure. A
hand-run always checks the network; the hook throttles (below), so this is also the
command for whenever someone wants an answer now.

Then confirm the hook entry appears exactly once, report the versions found and
whether anything was upgraded, and remind the user of the trust prompt. If the project
commits `.claude/`, add `.claude/.icp-upgrade-check` to `.gitignore` — it is a
per-machine timestamp, not shared configuration.

## How the script decides what to run

It resolves each binary through its symlinks and reads the install channel off the
path, because the upgrade command differs per channel and guessing wrong leaves two
copies of the CLI on `PATH` shadowing each other:

| Where the binary resolves to | Channel | Upgrade command (`icp` / `ic-wasm`) |
|---|---|---|
| `…/node_modules/@icp-sdk/…` | npm | `npm install -g @icp-sdk/icp-cli@latest` / `npm install -g @icp-sdk/ic-wasm@latest` |
| `…/Cellar/…` | Homebrew | `brew upgrade icp-cli` / `brew upgrade ic-wasm` |
| a cargo-dist receipt in `~/.config/<app>/` | shell installer | `icp-cli-update` / `ic-wasm-update` |
| anything else | unknown | *(none — reports the release URL instead)* |

That last row is deliberate: an unrecognised install is reported, never guessed at.

Two consequences worth passing on to users:

- **A shadowed install never moves.** If an upgrade succeeds but `PATH` still resolves
  to the old version, a second copy from another channel is winning — commonly an npm
  global under `nvm` alongside a shell-installer copy in `~/.cargo/bin`. Upgrading one
  channel can never touch the other's copy; resolve the binary (`command -v icp`) to
  see which wins, then remove one or upgrade the one actually on `PATH`.
- **Auto mode never runs `sudo`.** A non-writable npm prefix is reported as a `sudo …`
  command instead, since a password prompt inside a hook has no terminal to answer it.

## Throttling

A check that reached a release feed is stamped in `.claude/.icp-upgrade-check` and not
repeated for 6 hours, so the hook costs ~10 ms on most session starts instead of ~1 s.
Override with `ICP_UPGRADE_CHECK_INTERVAL=<seconds>` (`0` disables it) or bypass once
with `--force`; a run from a terminal always checks. A failed probe is not stamped, so
an offline session retries at the next one.

## What this does *not* upgrade

The hook manages the two CLI binaries only. Recipe versions in `icp.yaml`
(`@dfinity/motoko@v5.0.0` and friends) and the Motoko toolchain (`moc`, `mops`, the
`[toolchain]` pin in `mops.toml`) are pinned per project and stay the user's call —
load `icp-cli` and `mops-cli` respectively for those.

If a build starts failing right after an auto upgrade, check the [icp-cli release
notes](https://github.com/dfinity/icp-cli/releases) before assuming the project broke.

## Additional References

- **`icp-cli`** — using the CLI itself: `icp.yaml`, recipes, environments, deployment.
- **`mops-cli`** — the Motoko toolchain and its own version pinning.
- **`autosync-ic-skills`** — the companion installer that keeps the IC *skills* in
  `.claude/skills/` current. The two are independent; installing both is common.
