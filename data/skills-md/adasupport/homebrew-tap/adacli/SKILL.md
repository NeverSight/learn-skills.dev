---
name: adacli
description: Drive the adacli CLI to manage an Ada AI Agent (knowledge, playbooks, guidance, conversations, analytics, config). Use whenever the user wants to inspect or change an Ada agent from the terminal, mentions adacli, an Ada instance/handle, or "my Ada agent".
require-tools:
  - Bash
  - Read
---

# Managing an Ada AI Agent with adacli

`adacli` wraps Ada's management dashboard API. Invocation is always:

```
adacli <instance> <command> [subcommand] [options]
```

`<instance>` is a bare handle (`gennie`), a full domain (`bot.us2.ada.support`), or a URL.

## Always do first

1. **Confirm the instance** with the user if ambiguous — every command targets one.
2. **Check the session**: `adacli <instance> status --json`. If not connected, tell the
   user to run `adacli <instance> login` (it may need interactive email/password/MFA).
3. **Prefer `--json`** for every read so you can parse with `jq`. Output is JSON on
   stdout; errors are a JSON envelope on stderr; the **typed exit code** reflects the failure
   class: `0` ok, `2` usage, `3` auth, `4` forbidden, `5` not-found, `6` rate-limit, `7` read-only,
   `8` network, `9` conflict, `20` walk-partial, `21` walk-empty, `22` audit-degraded. Branch on it to
   self-correct (e.g. `3` → log in; `6` → back off). For the walk codes (`20`/`21`), the
   capped-vs-partial rule, and the exit-22 degraded-read rule, see **Exit-code semantics**
   under Conventions below.
4. **Discover the whole surface** with `adacli <instance> agent-context` — a machine-readable
   dump of every command, flag, exit code, and the error contract. Read it once instead of
   scraping `--help`.
5. **Start a session**: `adacli <instance> session-tracking start --intent "<what you will do>" --quiet`.
   Pass the ID it prints as `--session <id>` on every command after that. Run
   `session-tracking update --session <id> --reason <reason>` when an intent finishes or
   changes, and `--reason completed` when your previous intent is done, with
   `--intent` if you start a new one. `session-tracking --help` lists the
   reasons and limits. Do not put credentials or customer data in an intent or in notes.

## Load the full reference

This skill is the entrypoint. For the complete command-by-command guide, run and read:

```bash
adacli <instance> docs claude-code
```

Do that once at the start of an Ada session, then keep using the commands below.

## Most-used commands

```bash
adacli <instance> client --json                       # instance info / persona
adacli <instance> knowledge list --json               # knowledge base
adacli <instance> playbooks list --json               # playbooks
adacli <instance> guidance list --json                # custom instructions
adacli <instance> conversations search --all --limit 500 --json  # find conversations (see --all note below)
adacli <instance> analytics summary --json            # ClickHouse volume, resolution, and CSAT
adacli <instance> snapshot export -o config.tar.gz    # full config snapshot
```

## Conventions that make you effective

- **Playbook SDK starts.** Read the `playbooks update <id>` section of `adacli <instance> docs guide` for SDK start options and prerequisites.
- **Ask quick replies and image cards.** Before you author them, read the `ask` section of `adacli <instance> playbooks steps-schema`. On an ask with `inputs`, put the data source and card fields on the input, not on the step; the API rejects them on the step. Cards on manual choices use `accepted_values_images`, `_descriptions`, `_button_labels` and `_titles`, keyed by accepted value. After the write, check the `source:`, `card:` and `cards:` lines under the ask in `playbooks get <id>`; `cards:` says if Web Chat shows cards or plain choices.
- **Exit-code semantics (canonical note).** Read `.capped`/`.partial` from `--json`
  (or the table footer), not the exit code, to tell a bounded cohort from a truncated one.
  - A `--limit` (or default) **cap** is not a failure: it sets `capped: true` and exits `0`.
    This covers `search --all --limit`, `recent` (40-row default), and `export --limit`.
  - Only a **read-failure- or safety-limit-truncated (partial) walk** exits `20`
    (walk-partial): it sets `partial: true` and the emitted rows are usable but incomplete.
  - `export` adds file outcomes. A zero-row export writes nothing and exits `21` (walk-empty).
    `export` caps rows by default (50,000 to a file, 10,000 to stdout); pass `--limit <n>` to
    raise the file cap, and read `capped` from `--json` to tell a capped run from a complete one.
    For `export -o <file>`: a clean walk OR a cap (default or `--limit`) writes `<file>` and exits `0`.
    A complete export also clears a stale `<file>.partial`. A capped export leaves any prior
    `<file>.partial` alone. Only a partial (read-failure or safety-limit) walk writes `<file>.partial`
    and exits `20`, leaving `<file>` untouched. A capped `export` to stdout exits `0`.
    For transcript/reasoning export limits, read the Conversations section of
    `adacli <instance> docs claude-code` (canonical export concurrency note).
  - **Exit `22` (audit-degraded — canonical exit-22 note):** the read came back empty with
    no liveness signal after a retry — a degraded read, not a real empty result. Retry it;
    do not treat the empty result as a finding or author a fix on it. Emitters:
    `conversations diagnose` and the single-id readers
    `conversations reasoning`, `transcript`, `log`, `details`, `handoffs`, and `guidance`.
  - **`analytics summary`, `analytics topics` and `conversations handoff-reasons` are NOT degraded-read-guarded.** The
    ClickHouse backend returns the same zeroed payload for a real quiet window and for its
    own read failure, so a zero from them is not verified — corroborate it before acting.
- **The JSON `total` of `conversations search`, `recent` and `export` is the full match count**
  (canonical total note). It is the full count in every mode, also on a capped walk. Read the
  rows returned from `conversations.length`. If the count read fails, `total` is `null` and a
  stderr note says so.
- **Paginate `conversations search` with `--all`; `conversations export` always walks the
  window — bound it with `--limit <n>`** (canonical `--all` note). `export` registers no
  `--all` flag. A bare `search` returns only the first page (30 rows). The JSON `total` of
  `search` and `export` follows the canonical total note. `--all` auto-paginates the whole window; pair it with `--limit <n>` to bound the walk (see Exit-code semantics above
  for how a cap vs a partial walk is reported). List commands (`knowledge list`, etc.) page with
  `--page` plus `--limit` (e.g. `knowledge list --page 2 --limit 25`); `changesets list`
  pages with `--cursor`.
- **`conversations recent` shows the 40 newest by default** (canonical recent note). Widen it
  with `--limit <n>`. It walks pages like `--all`, so the default 40-row cap (or a `--limit`
  cap) sets `capped: true` and exits `0` (see Exit-code semantics above). Its JSON `total`
  follows the canonical total note.
- **Read before you write.** `get`/`list` the resource first; show the user the diff
  you intend before `create`/`update`/`delete`.
- **Destructive ops** (`delete`, `snapshot import`) need confirmation;
  pass `--confirm`/`--force` only after the user agrees.
- **Read-only instances**: production-like instances may be marked read_only in
  `~/.adacli/config`; writes will be refused with a clear error — don't fight it.
- **Pipe to jq** for big lists: `adacli <instance> knowledge list --json | jq '.articles[].title'`.

## Specialized workflows (separate skills)

- **Improve the agent autonomously (the main event)** → **ada-optimize** — example → diagnosis → fix → re-test → hill-climb
- Find what the agent gets wrong (incl. `conversations diagnose`) → **ada-insights**
- Knowledge base at scale → **ada-knowledge**
- Author + run tests, compare runs → **ada-test-agent**
- Version-control / promote / roll back a config → **ada-config-snapshot**
