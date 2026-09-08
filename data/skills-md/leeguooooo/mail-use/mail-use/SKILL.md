---
name: mail-use
description: Read, search, send, and manage email across Gmail, QQ, 163, Outlook and any IMAP/SMTP account from the command line. Use when the user asks to "read my email", "查邮件", "look up an Amazon order email", "find the customer review notification", "send an email", "回复邮件", "delete spam", "查未读", "show unread", "synchronize my mailbox", "set up MCP for email", or anything that involves listing / searching / reading / writing / classifying messages from one or more mailboxes.
metadata:
  author: leeguooooo
  version: "0.2.2"
  homepage: https://github.com/leeguooooo/mail-use
keywords:
  - mail-use
  - mailbox
  - email
  - imap
  - smtp
  - gmail
  - qq
  - 163
  - outlook
  - 邮件
  - 邮箱
---

# mail-use CLI Skill

Drives the `@leeguoo/mail-use` Node CLI to read and manage email across
multiple IMAP accounts. Returns a stable JSON contract — every response
includes `success: boolean` and, on failure, `error: string` +
`error_code: string` (machine-readable).

## Compatibility — check the CLI version first

**If `mail-use` is not on PATH** (`command not found` / `mail-use: not found`), install it
non-interactively from GitHub Releases (no npm, no auth) before doing anything else:

```bash
curl -fsSL https://raw.githubusercontent.com/leeguooooo/mail-use/main/install.sh | sh
# installs the prebuilt binary to ~/.local/bin — make sure that's on PATH, then re-probe
export PATH="$HOME/.local/bin:$PATH"; mail-use --version
```

These commands/flags require **mail-use ≥ 2.11.0**:
`--format compact|jsonl`, `email recent`, `cleanup`, `--since`, `--account-unread`,
`--text-only`, the 3-part gid (`account_id:folder:uid`), and `search --timeout`.

Probe before relying on them: `mail-use --version`. Update by re-running the installer above
(`MAIL_USE_VERSION=v2.11.2 …` to pin). On an older CLI, use these fallbacks (all available
since early versions):

| Newer | Fallback on < 2.11 |
|---|---|
| `--format compact` | `--lean` (drops noise; doesn't pin the exact field set) |
| `email recent` | `email list` with no `--account-id` (already spans all accounts) |
| `--since 7d` | `--date-from 7d` |
| `--text-only` | `--no-html` |
| `cleanup` | classify in-agent from `email list` output |

To tell whether a command exists, probe `mail-use <cmd> --help --json` and check
`success` — an unknown command returns `success:false` / `error_code:"invalid_argument"`.

## Setup (one time, by the user)

```bash
# 1. Install the CLI from GitHub Releases (no npm/Node needed; prebuilt binary):
curl -fsSL https://raw.githubusercontent.com/leeguooooo/mail-use/main/install.sh | sh

# 2. Configure accounts (edit credentials):
mkdir -p ~/.config/mailbox
curl -fsSL https://raw.githubusercontent.com/leeguooooo/mail-use/main/examples/accounts.example.json \
   -o ~/.config/mailbox/auth.json
$EDITOR ~/.config/mailbox/auth.json

# 3. (Recommended) install the persistent daemon for ~5-30× faster calls:
mail-use daemon install
mail-use daemon status --json   # confirm it's running

# 4. (Optional) wire into Claude Desktop / Code via MCP:
mail-use mcp config --json   # prints a paste-ready mcpServers entry
```

If the user hasn't done step 1, every CLI call will fail with `command not found`.
Always probe with `mail-use --version` first when in doubt.

## How to drive this CLI from an agent loop

Always pass `--json` so the response is machine-parseable. Check `success`
before continuing.

### The one-shot shortcut: "what's my verification code?"

```bash
mail-use code --json                       # newest OTP across all accounts, last 30m, one live pass
mail-use code --since 2h --json            # widen the window
mail-use code --account-id <id> --all --json   # every code-bearing email, not just the newest
```

Answers the single most common reason an agent opens a mailbox, without the
list → guess → show round-trip. Returns `{ code, newest: {...}, candidates: [...],
scanned, matched }`; `code` is `null` (with a widening `hint`) when nothing matched —
that is a successful call, not an error. Each hit carries `confidence`
(`high`/`medium`/`low`) from how close the token sits to a code keyword.

**Always live** — an OTP served from a cache snapshot is a wrong OTP. Selection
requires a code keyword in the mail (`verification code` / `認証コード` / `验证码` / …),
so ordinary mail carrying stray digits is not mistaken for a code email.

### Read / search

```bash
# List recent emails (cache when warm; pass --live to force IMAP).
# 'list' is INBOX-only — passing --folder all warns you to use 'search' instead.
mail-use email list --account-id <id> --limit 20 --json
mail-use email list --account-id <id> --limit 20 --with-preview 200 --json   # +body snippet, one trip
mail-use email list --since 7d --json                 # --since is an alias of --date-from (7d/today/YYYY-MM-DD)
mail-use email list --account-unread --json           # also compute account_unread_total (unread across all folders)

# Recent across ALL accounts, merged newest-first (omit --account-id == all accounts):
mail-use email recent --limit 30 --json
mail-use email recent --since 3d --json

# Search (server-side IMAP for Gmail; client-side fallback for QQ/163/Outlook):
mail-use email search --from amazon --subject review --folder all --json
mail-use email search --query "interview"  --since 2w --json    # relative dates: 2d/3w/1mo/today/yesterday

# ⚠️ search over QQ/163 (broken IMAP SEARCH) does a client-side scan of the folder and can be
# slow. --timeout (default 60s) is a HARD wall-clock bound — even a single stuck QQ/163 scan
# returns by then with partial results + timed_out:true (+ pending_accounts). Still prefer to
# scope it (--account-id and/or --folder INBOX) and use a short --timeout for snappy results.
mail-use email search --query inv --account-id <id> --folder INBOX --limit 20 --json   # fast, scoped

# NOTE: on QQ/163/126/sina/aliyun/outlook, IMAP TEXT search is broken,
# so the CLI falls back to envelope-only client-side filtering. That
# means `--query` only matches against `subject + from` for those
# providers — pure body-text matches will be missed. Use `--from` /
# `--subject` for predictable results, or use a Gmail account where
# X-GM-RAW does search the body server-side.

# Read one or many emails (AI-friendly defaults: text only, capped 2000 chars, URLs stripped,
# HTML excluded; HTML-only mail is auto-converted to a text body — see body_source).
mail-use email show <gid> --json                    # gid = "<account_id>:<folder>:<uid>"
mail-use email show <gid1> <gid2> <gid3> --json     # batch — one IMAP connection, spans folders
mail-use email show <gid> --full --json             # raw HTML + uncapped + URLs (rarely needed)
mail-use email show <gid> --text-only --json        # force no HTML (alias of --no-html)
mail-use email show <gid> --html-max-len 0 --json   # 0 = strip HTML, -1 = unlimited, >0 = cap

# Folders:
mail-use email folders --account-id <id> --json
```

The **gid is self-describing** (`account_id:folder:uid`), so `email show <gid>` opens the
right mailbox with no `--folder` — even for results from `search --folder all`. The legacy
2-part `account_id:uid` form still works (folder falls back to the cache, then INBOX).

### Mutate (all dry-run by default)

```bash
mail-use email mark <gid> --read --confirm --json
mail-use email delete <gid> --confirm --json        # default moves to Trash; pass --permanent to expunge
mail-use email flag <gid> --set --confirm --json
mail-use email move <gid1> <gid2> --target-folder Archive --confirm --json
mail-use email send --to a@b.com --subject hi --body "..." --confirm --json

# Filtered batch mark/delete by sender/subject (no need to list+collect ids first):
mail-use email delete --from newsletter@shop.com --confirm --json
mail-use email mark   --subject "[ci]" --read --confirm --json
mail-use email delete --from spam@x.com --all-folders --confirm --json   # span folders; grouped per folder
```

`gid`-based and filtered mutations are **folder-aware**: a 3-part gid mutates in *its* folder
(not INBOX), and `--from/--subject` matches carry their folder. The dry-run preview includes a
`groups` breakdown (per `account_id` + `folder`, with sample subjects) so you can eyeball what
will change before `--confirm`. Filters matching >100 emails require `--confirm`.

**Safety:** `--all-folders` skips special-use folders (Sent / Drafts / Junk / Trash) by
default — pass `--include-special` to include them. Without `--confirm`, every destructive
command returns a JSON dry-run preview and changes nothing.

### Triage / cleanup

```bash
# Classify INBOX and propose a deletion plan (read-only; never deletes):
mail-use cleanup --account-id <id> --json
# Then actually delete the marketing + routine_notification candidates:
mail-use cleanup --account-id <id> --confirm --json
mail-use cleanup --categories marketing --confirm --json   # only one category
```

`cleanup` buckets each email into `protected_finance` / `protected_travel` / `security` /
`support_case` (never deleted) vs `marketing` / `routine_notification` (cleanup candidates) vs
`unknown`. Rules are sender/domain/subject based; override the allowlists via
`<configDir>/cleanup_rules.json`. The plan reports `by_category`, `candidates_by_category`, and
`protected_counts`; `--confirm` pipes the candidate categories into `email delete`.

### Discover the surface

```bash
mail-use account list --json
mail-use <cmd> --help --json   # structured help: { name, description, options, arguments, subcommands }
```

## Token-saving tips

- **`--format compact` (global flag)** projects each email to just `{id, gid, account_id, folder, date, from, subject, unread, has_attachments, body_text_preview}` — the lightest useful shape for scanning, and it includes the 3-part `gid` so you can chain straight into `email show <gid>`. `--format jsonl` emits one JSON object per line (composable: `--format compact,jsonl`). `agent` is an alias of `compact`.
- **`--lean` (global flag, before subcommand)** strips ~10 noisy/duplicate top-level fields and per-email duplicates. Typical response shrinks by ~30%.
- **`--with-preview <N>`** on `email list / email search` fetches a body snippet alongside the envelope — saves one `email show` per email.
- **Batch `email show <gid1> <gid2> ...`** reuses one IMAP connection (and spans folders). Use it whenever you need ≥2 emails.
- **`gid`** (returned in every list/search/show response) is the global ID `account_id:folder:uid` — pass it instead of bare UID + `--account-id`, and `show`/mutate auto-target its folder.
- **Relative date shortcuts** (on `--since` / `--date-from`): `7d` (7 days ago), `3w`, `1mo`, `1y`, `12h`, `30m`, `today`, `yesterday`, `last-week`, `last-month`. ISO 8601 / `YYYY-MM-DD` still work.
- **`mail-use <cmd> --help --json`** returns a JSON descriptor of arguments, options, defaults — use to introspect any command instead of parsing human text.

## Output contract

- Every response: `success: boolean`. On failure: `error: string` + `error_code: string`.
- Common `error_code` values: `account_not_found`, `email_not_found`, `folder_not_found`, `invalid_argument`, `invalid_date`, `invalid_limit`, `ambiguous_account`, `size_limit`, `auth_failed`, `network_error`, `imap_error`, `smtp_error`, `operation_failed`, `unknown_error`.
- Exit codes: 0 success, 1 operation failed, 2 invalid usage.
- Every email object carries `gid` ("`<account_id>:<folder>:<uid>`"). Prefer it over bare `id`/`uid`.
- Batch `email show` returns `{ success, emails: [...], failed_ids: [{id, error, folder}], requested, returned }`.
- **Unread counts** on `list`/`recent` are three distinct fields — read the right one:
  `unread_in_result` (unread among the rows actually returned — always trustworthy),
  `folder_unread` (server count for the queried folder; `unread_count` is a back-compat alias),
  `account_unread_total` (across all folders — `null` unless `--account-unread`), plus
  `unread_as_of` + `from_cache` for snapshot freshness.
- **Cache freshness** is always reported on `list`/`recent` (including empty/compact results):
  `from_cache` (bool), `cache_age_seconds` (how stale the snapshot is; `null` = live or unknown),
  and, on a thin cached result, a `hint` string telling you to pass `--live`. So an empty list is
  never a silent "nothing arrived" — check `from_cache`/`cache_age_seconds` before concluding.
- **Self-healing on a thin+stale cache**: when a cached `list`/`recent` comes back with fewer rows
  than `--limit` AND the snapshot is older than the freshness window (default 120s, set via
  `MAILBOX_CACHE_FRESH_SECONDS`; `0` disables), the CLI auto-falls back to a live IMAP fetch — so a
  just-arrived OTP isn't missed between syncs. Pass `--live` to force IMAP outright.
- **Email body**: `body` (text), `body_source` (`text` | `html_derived` | `empty`), `html_body`
  (empty unless `--full`/`--include-html`). HTML-only mail still yields a usable `body`.
- **Attachments**: each carries `is_signature` / `is_inline` / `is_real_attachment`;
  `real_attachment_count` and `has_attachments` count only real attachments (an `smime.p7s`
  S/MIME signature does not flip `has_attachments`).
- `--with-preview` adds `preview: string` and `preview_truncated: bool` per email.
- **Verification / OTP codes**: `email show ... --extract-code` scans subject+body and adds a
  `codes: [...]` array (4–8 digit OTPs plus prefixed `LL-DDDDDD` forms like `QB-046193`). It's a
  candidate list, ordered as found; the field survives `--format compact`.

## Safety rules

- Always pass `--json`. Always check `success`.
- Pass either a `gid` OR `--account-id <id>` for any per-email command.
- Mutating commands (`email send / delete / mark / move / flag`, `digest run`) default to **dry-run**; the agent must explicitly add `--confirm` after the user approves.
- Never leak account credentials in logs or model output.

## MCP server mode

Instead of shelling out to the CLI, an AI client can call mail-use tools
directly over MCP:

```bash
mail-use mcp config --json   # prints an mcpServers entry to paste into the client config
mail-use mcp serve           # run the server manually for testing (stdio)
```

16 tools registered: `account_list`, `account_test_connection`,
`email_list`, `email_search`, `email_show`, `email_folders`,
`email_mark`, `email_delete`, `email_flag`, `email_move`, `email_send`,
`sync_status`, `sync_force`, `inbox_organize`, `cleanup`, `digest_run`.

Each destructive tool defaults to dry-run; pass `confirm: true` to apply. `email_show` and the
mutate tools accept 3-part gids (`account_id:folder:uid`) and auto-target the gid's folder;
`email_list` exposes the `unread_in_result` / `folder_unread` / `account_unread_total` fields
and accepts `include_account_unread`; relative `date_from`/`date_to` shortcuts (`2d`/`3w`/…)
now work on the MCP path. `cleanup` returns a read-only plan unless `confirm: true`.

## Persistent daemon (5-30× faster CLI calls)

Each one-shot CLI invocation otherwise spends 1-3s on TCP+TLS+IMAP LOGIN.
With the daemon running, every CLI call reuses pooled connections, and
the daemon also runs a background SQLite sync so `email list` (without
`--live`) usually doesn't touch IMAP at all.

```bash
mail-use daemon install      # autostart at login (macOS launchd / Linux systemd-user)
mail-use daemon status --json
mail-use daemon reload       # drop pooled connections after editing auth.json
mail-use daemon stop
```

The installer sets the daemon up automatically when accounts are already configured, so
on a machine that has been through `curl … install.sh | sh` it is usually already running.
Check with `mail-use daemon status --json`; install with `mail-use daemon install`.

One process per user, shared by every session over a Unix socket — more agent sessions do
not mean more IMAP connections. Idle cost measured on macOS with 3 accounts: ~0.15% CPU,
3-15 MB RSS. Connections are capped at 3 per account (`MAILBOX_POOL_MAX`) and reaped back
to 1 after 10 minutes idle (`MAILBOX_POOL_IDLE_MS`).

Set `MAILBOX_NO_DAEMON=1` to skip the daemon probe entirely.

Measured (Gmail INBOX, M2 MacBook over residential WAN):

| Operation | No daemon | Daemon (--live) | Daemon (cached) |
|---|---|---|---|
| Single `email list` | 5.0s | 1.0s | 0.17s |
| `email folders` | 5.0s | 0.85s | n/a |
| 5 sequential `email list` | 25s | 5.3s | **0.83s** |
| 3 parallel `email show` | ~15s | 2.7s | **0.88s** |

## Reference

- Install this skill: `npx skills add leeguooooo/mail-use --skill mail-use` (add `-g` for user scope)
- Repo: https://github.com/leeguooooo/mail-use
- JSON contract docs: `docs/CLI_JSON_CONTRACT.md`
