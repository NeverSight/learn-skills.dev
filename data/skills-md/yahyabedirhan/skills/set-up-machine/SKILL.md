---
name: set-up-machine
description: Set up or audit a machine's coding-agent harnesses from one rule table and the user's workstation repo - the shared global instructions every harness reads, the global rules (deny, ask, allow-and-report) each one enforces, the pre-tool hook, memory kept off, declared Codex CLI and Pi defaults, the plugins each harness gets, and the skills and tools the workstation repo lists to install. Use for a new machine or VPS, to audit this machine's agent setup, or when another skill says to check the machine.
---

# Set up machine

Set up every selected harness (Claude Code, Codex, opencode, Cursor's IDE and CLI, Pi) from its sources. Install or update each selected tool to the latest available version. Running the skill again is the **audit**: check configuration and freshness, then propose any required updates.

## Sources

- **Rule table**, [`rules.json`](rules.json).
- **Workstation repo**, `<workstation-repo>`, found through the **pointer**, `~/.config/agents/source.md`, which names the repository and its clone. Each of these files is optional:
  - `agents/instructions.md`: the working agreement, the glossaries, which tool fills each role, and the personal workflow;
  - `agents/permissions.json`: the **personal permissions**, rows each harness carries beside the rule table's;
  - `agents/installs.json`: the skills, plugins and commands every machine gets;
  - `agents/codex.toml`: Codex CLI defaults, declared explicitly;
  - `agents/pi.json`: Pi settings, declared explicitly.

## Outputs

- **Shared global instructions file**, `~/.config/agents/AGENTS.md`, which every harness reads; its personal parts come from `agents/instructions.md`.
- **Harness instructions**, for a harness that has its own `agents/harnesses/<harness>.md` in the workstation repo: today Cursor's `~/.cursor/rules/harness-instructions.mdc` (references/workstation.md).
- Each harness's permission entries, from the rule table and the personal permissions.
- The **pre-tool hook**, `scripts/pre_tool_hook.py`, run before every tool call.
- The **pointer**, when it is missing or records none.
- Codex CLI defaults that `agents/codex.toml` declares, and Pi settings that `agents/pi.json` declares.
- The skills and commands `agents/installs.json` lists for this machine, and its **plugins** in each harness it names: the plugins setup area, a plugin bundle or a standalone MCP server per entry.
- Memory off in every harness.

## Rules for every run

- Reproduce installation choices, configuration and steps, not a snapshot of software versions. Use the latest stable release, or the latest default branch for repository-distributed code. Apply this to harnesses, skills, plugins, packages and command-line tools.
- Record installed versions and source commits as audit evidence, not future installation targets. Keep historical citations and dependency lockfiles separate from machine setup choices.
- Check the current upstream source before calling an installation up to date. A matching declaration or an existing executable proves presence only. Report unavailable freshness checks as `gap`.
- Keep every entry the rule table didn't produce, as it is: it's the user's.
- Harness formats change: check the docs a harness reference links before writing. Where they differ, follow the docs and name the difference in your report.

## Parameters

- `<skills-repo>`: the user's own skills repo on GitHub, as `owner/repo`. Installed only when the workstation repo has no `agents/installs.json`.
- `<workstation-repo>`: the user's own repo for their personal agent setup, usually private, as `owner/repo`.
- `<path-to-workstation-repo>`: where that repo is cloned, e.g. `~/code/agent-setup`.

## Steps

1. **Inspect.** Find each selected harness and tool, compare its installed version with the latest source, and read its current documentation. Preserve its installation channel. Read each harness reference, then the non-secret configuration fields it needs. Leave credentials, authentication stores and runtime state unread. Read the shared file and the pointer too, and when the pointer names a workstation repo, read `references/workstation.md` and the repository's `agents/instructions.md`, `agents/permissions.json` and `agents/installs.json` in `<path-to-workstation-repo>`. For Codex, inspect the optional `agents/codex.toml` as its reference directs; use one resolved config home throughout setup and verification. For Pi, do the same with `agents/pi.json` and one resolved agent folder.
   - **When the pointer is missing:** read `references/workstation.md`, then ask the user once for `<workstation-repo>` and `<path-to-workstation-repo>`, or whether they have none. The diff writes the pointer, recording "none" too, so the next run doesn't ask.
   - **When the pointer records no workstation repo:** set up the machine as `references/workstation.md` says for a run without one, or, when the user names one now, as it says for rewriting the pointer.
   - **When the machine is remote or headless, such as a VPS:** read `references/remote-machine.md` first.
   - **When trying a change without touching the real machine:** run the steps against a copy of the home folder in the project's `.scratch/`, and check it with `verify.py --home <copy>`. Start no harness there, since it would read the real login.
2. **Propose one diff** that brings each harness in line with the rule table, the shared file's shape and personal parts, the pointer, memory off, the hook wired, declared supported Codex defaults, declared Pi defaults, and the installs: every skill and command `agents/installs.json` lists for this machine, each selected installation up to date. Include harness upgrades and plugin updates, not only missing installs. Give every harness found its own section, listing each gap its reference names and the hook's blind spots. Read `references/global-instructions.md` whenever a global instructions file is in the diff.

   Work out what each harness should hold, from `rules.json`, the personal permissions, the shared file's shape and the harness's reference, and compare it with what the machine holds. Write the whole diff: per harness and file, the exact entries or a unified diff, each line marked:

   - `added`, `tightened` (a stricter entry added where it wins), `removed`, `updated` (an installed harness, skill, plugin or tool behind its latest source);
   - `present`, `wired` (the hook), `found` (the MCP tools a row matched);
   - `stricter` (the machine is stricter than the table: kept), `extra` (neither the table's nor a personal permission's: kept), `ignored` (an installed skill `agents/installs.json` leaves out on purpose: kept, never installed or removed), `gap` (what the harness can't express), `none` (no such feature);
   - `personal` beside the mark of every entry a personal permission produced (`added, personal`; `present, personal`), so the user can tell those entries from the table's and never reads them as `extra`;
   - `n/a` (not applicable) for a personal permission whose tool this harness lacks, with why: nothing is written for it there.

   Use `removed` only for memory files, a harness's own global file whose every line is already in the shared file (it becomes a link), and this skill's own wiring that points at an old script. An entry a dropped row, the table's or a personal one, left behind is `extra`, for the user to remove.
   - **When the workstation repo has `agents/installs.json`:** the diff holds a line per entry that applies to this machine, and an `n/a` line, with why, per entry that doesn't. The file is the whole list: install nothing it leaves out. `references/workstation.md` gives the format, the checks and the commands.
   - **Without the file, with a `<skills-repo>` value:** the diff installs that repo's skills globally: `npx --yes skills add <owner>/<repo> -g -a codex -a claude-code -y`, leaving out `-a claude-code` when `~/.claude/skills` is a link to `~/.agents/skills`. Compare the installed skill hashes with the source's latest default branch, as `references/workstation.md` describes. Presence in the lock file alone does not prove freshness. With no value, it's a `none` line.
3. **Ask once** for one approval of the whole diff. A change after that needs a new approval.
   - **When the diff holds only `added` and `updated` installs from `agents/installs.json`:** write it without asking, since the user approved that list by writing it.
4. **Back up** every file the diff changes or removes. Before writing any file, copy each one into `~/.config/agents/backups/<UTC time as YYYYmmddTHHMMSSZ>/`, at its path relative to the home folder (`.claude/settings.json`). Copy a symlink as a link.
5. **Write** exactly the approved diff. Run any install command first, such as a skill the diff installs. If one fails, stop subsequent writes and report what changed before the failure. Check configuration and guardrail compatibility after upgrades; report failures rather than making an old snapshot the desired state. In JSON and TOML files, change only the keys the diff names and keep the rest. Write through a symlink to its target.
6. **Verify** with `scripts/verify.py`, then inspect again until the diff changes nothing: no pending `added`, `updated`, `tightened` or `removed` line, and no unreported freshness gap. Report the backup folder, what's wired, the gaps, and the stricter and extra entries.

   Run `python3 <skill-folder>/scripts/verify.py`, where `<skill-folder>` is this skill's installed folder. It needs Python 3.9+ and the standard library only, and it writes nothing. The run passes when [What verify must show](#what-verify-must-show) passes. Report `config gap` and `config override` lines separately; they limit what the audit proves. The verifier checks persisted configuration, not current upstream releases. Complete the separate freshness checks from Inspect before reporting that every installation is latest.

## What verify must show

Shared lines first. Each harness then has its own section for the lines only that harness adds. A harness with no section of its own is done when its `hook wired` line is present.

### Shared

- `rules ok`
- a `hook wired` line for every harness found
- `personal ok` or `personal none`, and no `personal FAIL`
- no `harness FAIL`; a `harness gap` names instructions for a harness this skill can't deliver to yet
- no `plugin FAIL`; a `plugin gap` names a plugin a harness can't take from this skill yet, and `plugin extra` a Claude Code bundle or a Pi extension the list leaves out

### Claude Code

No further line. The `hook wired` line is the check, and each personal permission is `present`, `n/a` or `gap` on the `personal` lines. Details: [references/claude-code.md](references/claude-code.md).

### Codex

[references/codex.md](references/codex.md)

- Every `codex differs` line is a row that reference says gets no rule.
- Declared defaults match with no `config FAIL` line, or a `config n/a` line says Codex isn't installed.
- In the report, distinguish persisted defaults from effective overrides, and state how a later session picks the change up.

### opencode

No further line. The `hook wired` line is the check. Details: [references/opencode.md](references/opencode.md).

### Pi

[references/pi.md](references/pi.md)

- When Pi's agent folder exists, `pi ok` for the `AGENTS.md` link, and a `pi same` line per key `agents/pi.json` declares, or `pi none` with no such file. A `pi FAIL` means the audit is not done.
- Its `hook wired` line is the extension. Pi has no permission system, so the hook is its only enforcement, and the extension fails closed: name in the report that a missing `python3` or script makes Pi refuse every tool call. A `hook gap` line is an extension someone else wrote at the same path, left alone.
- A `pi extra` line is a broken skill link, for the user to remove.
- A `pi gap` for `packages` in `agents/pi.json` asks the user to move them into `plugins`, where Pi extensions belong.

### Cursor

[references/cursor.md](references/cursor.md)

- When `~/.cursor` exists, `cursor ok`: Auto-review, with the sandbox on. `cursor FAIL` means the audit is not done. No `~/.cursor` is `cursor none`.
- The keys, the Linux sandbox gap and what the skill leaves in `permissions.json` are in that reference.
- With `agents/harnesses/cursor.md` in the workstation repo, `harness ok` for `~/.cursor/rules/harness-instructions.mdc`.

## Rule table

`rules.json` holds each global rule once, by meaning, not in any harness's form. Each harness reference turns a row into that harness's entries; the hook and `verify.py` read it through `scripts/setupmachine/rules.py`, which refuses a malformed row. A workstation repo's `agents/permissions.json` holds personal permissions in the same format, which every harness, the hook and `verify.py` take beside the table's (`references/workstation.md`).

### A row

| Field | Holds |
|---|---|
| `id` | a stable kebab-case name |
| `level` | `deny`, `ask` or `allow-and-report`; a personal permission may also be `allow` |
| `summary` | what the rule covers, shown in rejection messages |
| `match` | what it covers, in one of the three kinds below |
| `reason` | why the rule exists |
| `instruction` | for `deny`, what the agent does instead: an alternative, or "Stop, say why, and give the user the exact command; never work around it."; for `ask` and `allow-and-report`, how to go ahead |
| `samples` | `covers`: calls the row must catch; `leaves`: near misses it must let through. A shell command for a command row, a path for a file row, a tool name for an MCP row. `verify.py` checks them against the hook |
| `gap` | optional: what no harness can catch for the row (`echo $TOKEN`); every audit names it |
| `approver` | optional, on an `ask` row only: `user` when each call needs the user's own approval, which an automatic reviewer's or a remembered answer's doesn't replace |

### `match` kinds

A `match` object's keys say which kind it is:

- **Command:** `program`, a bare name (`rm`) or a list of them, and optionally:
  - `subcommands`: alternative word lists after the program (`[["repo", "delete"], ["repo", "archive"]]`);
  - `flags`: every flag group the command carries, each listing one flag's names without dashes, a one-letter name being the short flag (`["r", "R", "recursive"]`);
  - `operands`: words right after the subcommand and flags (`["777"]`), or alternative word lists (`[["777"], ["a+rwx"]]`);
  - `any_operand`: words any one of which may appear anywhere after the subcommand (`["main", "master"]`);
  - `arguments: "none"`: the program with nothing after it (`env`); `arguments: "flags"`: with flags and nothing else (`declare -x`);
  - `files`: globs one of its operands must match (`cat .env`), with an optional `except`;
  - `variables`: globs over the names of the variables an argument expands (`*TOKEN*` covers `echo $API_TOKEN`, not `echo '$API_TOKEN'`).
- **File:** `paths`, globs relative to the project (`**/.env`), or starting `~/` or `/`; `access`, `read` or `write`; an optional `except` (`**/.env.example`). A `read` row covers writes too.
- **MCP tool:** `server` and `tool`, case-insensitive regular expressions over the two parts of `mcp__<server>__<tool>`. Store the meaning (`mail`, `^(send|reply|forward)`), never one account's server ID, so the row matches on every machine and account.

### Spellings

A harness that matches a command's text catches only the spellings it lists, so give it one entry per way of writing a command row:

- **Programs:** each program as typed, then as `/bin/<program>` and `/usr/bin/<program>`, except shell builtins (`.`, `source`, `set`, `export`, `declare`, `typeset`, `unset`, `eval`, `alias`), which have no path.
- **Flags:** a one-letter name is a short flag (`-r`), a longer one a long flag (`--recursive`). Every order of the groups, every spelling in each group, as separate words; and, when every group has a one-letter name, the one-letter names clustered in every order (`-rf`, `-fr`, `-Rf`, `-fR`).
- **Order:** program, then subcommand words, then flags, then operands (`git push --force`, `chmod -R 777`).
- **`find`'s options** (`-delete`) are one-dash words written after the path, so no prefix entry catches them: a command row on `find` gets no native entry, a gap the hook covers on every harness.

## Pre-tool hook

`scripts/pre_tool_hook.py` (Python 3.9+, standard library only) is the hook every harness runs before each tool call. It reads `rules.json`, and the personal permissions through the pointer, and checks the call:

- **deny** rows: it reads a command the way the shell runs it, and checks file tools, redirects and MCP tools too. It refuses the call, naming each refused part with its rule's reason and instruction.
- **allow-and-report** rows: it writes one JSON line per call to `<report-folder>/<date>.jsonl`, readable by the user alone; the harness's permissions decide.
- **ask** rows: the harness's native ask entries do the asking. A row with `approver: "user"` is refused instead where the call shows that no one will ask the user: Claude Code in `auto`, `dontAsk` or `bypassPermissions` mode, Codex with approval policy `never`, and every call under Cursor and opencode, which can't promise a prompt (their references say why). Cursor has no ask list at all, so there the hook refuses every ask row, `approver` or not. Pi has no ask list either, but its extension can ask: with a UI, the hook names the ask rows and the extension asks the user in Pi's dialog; without one, the hook refuses every ask row (references/pi.md).
- **allow** rows: it says nothing; the harness's native allow entries let the call run without a prompt.

A malformed personal file leaves the table's rows in force: the hook skips the personal permissions and `verify.py` reports the file.

### Wiring

Each harness reference shows its wiring with `<script>` in place of the script's path. Replace it with the absolute path of `scripts/pre_tool_hook.py` in the installed skill (under `~/.agents/skills` or `~/.claude/skills`), never in a checkout or worktree, which can be deleted. If there is no installed copy, name the gap.

The wiring fails open (`[ -f <script> ] && … || true`, or the form a harness reference gives): if the script is gone, each call goes on under the native entries. Without it, `python3` would exit 2 on the missing script, which blocks every call. Pi is the exception: it has no native entries underneath, so its extension fails closed and refuses each call the hook can't check (references/pi.md).

`<report-folder>` is `~/.local/state/agents/reports`, or `report_dir` in `~/.config/agents/hook.json`.

### What it can't see

Name these once in every audit:

- a command inside a script file or another interpreter (`python -c`);
- a command built from variables (`$cmd -rf x`);
- an alias or function defined elsewhere;
- an abbreviated long option (`--recur`);
- a force push by refspec (`git push origin +main`);
- a glob the shell expands (`cat .env*`);
- an automatic reviewer, such as Codex's `auto_review`, answering an `approver: "user"` row, since the call's payload doesn't show the reviewer;
- each row's own `gap`.

## References

- [references/global-instructions.md](references/global-instructions.md): the shared file's shape, the roles table, the working agreement and glossaries, what counts as personal workflow, moving a harness's own file, and why memory stays off.
- [references/rule-table.md](references/rule-table.md): changing a row of the rule table, changing the hook's code and its tests, and adding a harness.
- [references/workstation.md](references/workstation.md): what this skill reads from the workstation repo: the pointer, the `agents/` files and their format, generating the shared file's personal parts and the personal permissions from them, the installs list, and the run without one.
- [references/remote-machine.md](references/remote-machine.md): running agents on any remote or headless machine: signing in without a browser, per-machine settings, keeping sessions alive, and containing a misled agent.
  - [references/new-remote-machine.md](references/new-remote-machine.md): for a brand-new machine, first: the base it needs, done with the user as root, from key access, the dedicated user, keys-only SSH, the firewall, updates, swap and the docker group to the session host's integration, git credentials, `PATH` over SSH and a headless browser.
- One reference per harness, read for each harness found. Each says how the harness is found, where it keeps each setting, a row's native form with worked examples, the hook's wiring, and its gaps:
  - [references/claude-code.md](references/claude-code.md): Claude Code.
  - [references/codex.md](references/codex.md): Codex. Its *Codex MCP* section holds the TOML and OAuth detail.
  - [references/opencode.md](references/opencode.md): opencode.
  - [references/cursor.md](references/cursor.md): Cursor's IDE and CLI.
  - [references/pi.md](references/pi.md): Pi, whose only enforcement is the hook's extension.

## Scripts

- [scripts/verify.py](scripts/verify.py): checks, without writing anything, that the rules work on this machine. Shared checks: each row's samples through the hook, the shared file against the workstation repo, and the `plugins` list against each harness it names. `scripts/setupmachine/plugins.py` dispatches that list through `scripts/setupmachine/harnesses/<harness>.py`. Each adapter exposes `validate`, `check` and `propose`. Harness checks:
  - **Claude Code:** each personal permission's entries.
  - **Codex:** its own policy check, plus declared defaults, installed support and override gaps at the resolved config home.
  - **opencode:** the hook wiring only.
  - **Cursor:** Auto-review and the sandbox, as [references/cursor.md](references/cursor.md) describes.
  - **Pi:** the instructions link, declared defaults, broken skill links and the hook's extension, at the resolved agent folder.
- [scripts/pre_tool_hook.py](scripts/pre_tool_hook.py): the pre-tool hook every harness calls before each tool call.
- [references/opencode-plugin.js](references/opencode-plugin.js): the opencode plugin that calls the hook.
- [references/pi-extension.ts](references/pi-extension.ts): the Pi extension that calls the hook and asks the user for ask rows.
