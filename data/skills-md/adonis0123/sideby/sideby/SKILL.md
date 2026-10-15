---
name: sideby
description: Use when the user runs, or wants to run, several AI coding accounts (Claude Code, Codex, Grok Build, pi) side by side. Covers installing sideby and setting up a new account ("install sideby", "set up another Claude account", "add cc008", "配置一个 cc00x", "再加一个 Codex 账号"), explaining what accounts share and what stays separate ("what do my accounts share?", "这些账号共享了什么"), showing which account a session is ("show [cc001] in the status line", "加上账号标识"), seeing accounts, quota and usage, moving on when one hits its 5-hour or weekly limit, adding a short command (alias), and repairing drifted account directories (skills, hooks, rules or settings not shared, wrong symlinks, credential file permissions). Drives the `sideby` CLI with `--json`; the agent does every step except browser sign-in, filling in secrets and starting interactive sessions, which it hands to the user as one command.
metadata:
  version: "0.9.0"
  requires:
    bins: [sideby, node]
  cliHelp: sideby --help
---

# sideby

`sideby` runs each AI coding account from its own directory (`~/.claude-work`, `~/.codex-api`, ...) and keeps skills, hooks and rules shared with the Main Account (`~/.claude`, `~/.codex`, `~/.grok`, `~/.pi/agent`). Requires Node 22.18+. If `sideby` is not installed, follow `references/setup.md`; `sideby <command> --help` shows examples for `new`, `alias`, `login`, `doctor` and `families`.

Do every step you can yourself. Only browser sign-in, secrets and interactive sessions belong to the user: hand each to them as exactly one line to run (in Claude Code they can type `! <command>`), then continue once they say it is done.

## Hard rules

- **Never read credential files**: `proxy.env`, `auth.json`, `.claude.json`, or anything under an account directory that may hold a token. Do not `cat`, `grep`, `head`, open or summarize them. `sideby list --json` gives the signed-in email as `identity.email`; that is all you need.
- **Never sign in for the user.** Give them `sideby login <ref>` as one line to run in their own terminal (Claude Code: `! sideby login <ref>`). OAuth needs their browser and their decision.
- **Never put a secret on the command line or in chat.** For API accounts, the user edits `proxy.env` themselves.
- **Never start a Host session from your shell.** `sideby run`, `sideby next` (without `--dry-run`) and `sideby login` open an interactive session; give the user the command instead.
- **Never switch, rotate or proxy accounts yourself.** Do not work around sideby by editing config, copying session files or moving credentials. `sideby next` only recommends. Moving a running task on its own is Auto Handoff, which the user turns on: use `sideby handoff enable` (exit 10, then their yes), never hand-edit `config.json`. Inside such a session you may run `sideby handoff ready` when the user asks to hand over.
- **Say what you change.** Read-only commands first. What the user asked for (the account they asked to create, its short command, the shell line that makes it work) you do, saying what you do. Changes they did not ask for (`doctor --fix` on other accounts, `quota setup`, `app install`) wait until they have seen the change and agreed.
- Do not edit Host config files (`settings.json`, `config.toml`, symlinks in account directories) by hand when a `sideby` command does the job.

## Output and exit codes

- Every `--json` output has `schemaVersion: 1`. On an error it is `{ "schemaVersion": 1, "error": "<what to do next>", "code": "<reason>" }`; `code` is `usage` for a malformed command line.
- Exit codes: `0` done, `1` failed or found a `fail` problem, `2` malformed command line, `10` **needs the user's confirmation**. `run`, `next` and `login` return the Host's own exit code once it starts.
- On `10`: show the user the change the command printed, ask, and only after a clear yes run the same command again with `--yes` added. Never add `--yes` on your own.

## What do you want to do

Account refs are `<family>:<name>`; a bare `<name>` works only when it is unique. Families: `claude`, `codex`, `grok`, `pi`.

| The user wants to | Run | Then read |
|---|---|---|
| Install sideby, or set up a new account ("add cc008") | `sideby --version`, `sideby list --json`, `sideby new <family> --next --json` | `references/setup.md` |
| Show which account a session is (`[cc001]` in the status line or tab title) | `sideby list --json` for the labels | `references/badge.md` |
| Know what accounts share and what stays separate | `sideby families <family> --json` | `references/sharing.md` |
| See accounts, health, quota and usage | `sideby list --json`, `sideby doctor --json`, `sideby quota --json` | `references/diagnose.md` |
| Repair drift or permissions | `sideby doctor [ref] --json`, then `--fix` after they agree | `references/diagnose.md` |
| Keep working because an account hit its limit | `sideby next <family> --json` | `references/handoff.md` |
| Turn on Auto Handoff ("自动交接", "hand over when quota runs low"), see what it still needs, hand this session over now, or pick an account with room for a subtask | `sideby handoff status --json`, `sideby handoff enable --json` (exit 10 first), `sideby handoff ready`, `sideby next <family> --json` | `references/handoff.md` |
| Create an account with a given name, an API account, or a short command | `sideby new`, `sideby alias add` | `references/accounts.md` |
| Tune the auto-compact threshold ("which compaction setting costs the fewest tokens"), use the suggestion or undo it | `sideby tune --json`, `sideby tune apply` (exit 10 first), `sideby tune undo` | `references/diagnose.md` |
| See or set the model and effort an account starts with ("用哪个模型", "set effort to high for cc002") | `sideby model <acct> --json`; `sideby model <acct> <model\|default> --effort <level\|default>` (exit 10 first, then `--yes` after the user agrees) | — |
| See Claude quota (it shows `not-enabled`) | `sideby quota setup claude` (exits 10) | `references/quota.md` |
| See everything at once | `sideby ui` (local panel on `127.0.0.1:17420`; `--no-open` prints the address) | — |
| Start an account | give them `sideby run <ref> [-- host args]` | — |

Read only the reference the task needs.

## Launching and the panel

`eval "$(sideby shell-init zsh)"` defines one function per account (`sideby-claude-work`) plus the config `aliases`. Users who source a file instead set config `shellInitFile` (for example `{ "zsh": "~/.config/sideby/shell-init.zsh" }`); `new` and `alias add|rm` keep it current, and `sideby shell-init zsh --write` rewrites it. New functions work in a new shell.

When a terminal manager such as Orca reopens a pane with a bare `claude --resume <id>` (or `codex resume <id>`, `grok --resume <id>`) and the Host says `No conversation found`, the session lives in another account. Suggest config `"resumeRouting": true` followed by `sideby shell-init --write` (or a new shell with `eval`): `shell-init` then defines Host-named functions that call `sideby resume <family>`, which starts the account holding that session. For a one-off, find it with `ls -d ~/.claude*/projects/*/<id>.jsonl` and run `sideby run <ref> -- --resume <id>`. When no account has that file, the session was opened but never got a message, so there is nothing to resume: `ls -d ~/.claude*/session-env/<id>` names the account that started it, and with routing on `sideby resume` starts a new session there by itself.

To open Claude Desktop or the Codex app as one account (macOS, subscription accounts), run `sideby desktop <ref> --json` yourself: it opens a new window for that account, or brings its open window to the front, and never closes anything. Relay its `notices`: the first Claude Desktop sign-in should happen while other Claude Desktop windows are closed, and a sign-in screen that suggests the main account ("Welcome back" in the Codex app) must not be used for another account.

For someone who would rather double-click than use a terminal, `sideby app install` adds a panel app (macOS `~/Applications/sideby.app`, Linux app menu) that runs `sideby ui --background`; `sideby ui --stop` stops it and `sideby app uninstall` removes the app. Ask before `app install`: it writes outside sideby's own directories.

## Keeping this skill current

If `sideby doctor --json` reports `skill.outdated`, this skill was written for another sideby version. Tell the user to update it with `npx skills add Adonis0123/sideby -g`.
