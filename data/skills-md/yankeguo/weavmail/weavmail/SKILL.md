---
name: weavmail
description: Use weavmail CLI to manage emails for the current task. Use when you need to read, send, reply to, or move emails as part of completing a task.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["uv"] }
      }
  }
---

# `weavmail` is a command-line email client designed for AI agents. Use it to read, send, reply to, and organize emails

## Setup

Install once before first use:

```bash
uv tool install weavmail
```

Configure an account (named `default`):

```bash
weavmail account config \
  --imap-host imap.example.com \
  --smtp-host smtp.example.com \
  --username you@example.com \
  --password your-app-password \
  --addresses you@example.com
```

`--username` and `--password` set both IMAP and SMTP credentials at once. The account name defaults to `default` and can be omitted from all subsequent commands.

Each option can be updated independently — only the options you pass are changed, everything else is preserved. For example, to update just the password:

```bash
weavmail account config --password new-password
```

`--addresses` is a comma-separated list of email addresses that are authorized as senders for this account (e.g. `--addresses you@example.com,alias@example.com`). All addresses listed here can be used as the `--from` address when sending mail.

To view the current configuration of an account, run `account config` without any options:

```bash
weavmail account config        # show default account
weavmail account config work   # show account named "work"
```

---

### After Configuring an Account

**After any account is configured, always run the following automatically:**

```bash
weavmail mailbox
```

Inspect the output and identify the Sent and Trash folders (names vary by provider, e.g. `Sent`, `Sent Messages`, `[Gmail]/Sent Mail`, `Trash`, `Deleted Messages`, `[Gmail]/Trash`). Then save them to the account config:

```bash
weavmail account config --sent-mailbox "Sent" --trash-mailbox "Trash" --archive-mailbox "Archive"
```

To sync Spam (or other folders) in addition to INBOX, configure `--sync-mailboxes`:

```bash
weavmail account config --sync-mailboxes "INBOX,Spam"
```

All these fields are optional — if any cannot be identified with confidence, skip it. They do not affect other functionality when unset.

---

## Sync Mail

Fetch the latest emails and save them as local Markdown files. Sync uses all configured accounts and each account's `sync_mailboxes` config (default: `INBOX`):

```bash
weavmail sync
```

Options:

- `--limit N` — number of most-recent messages to fetch per mailbox (default: `10`)

To include Spam (or other folders) in the default sync, run:

```bash
weavmail account config --sync-mailboxes "INBOX,Spam"
```

Each email is saved to `./mails/<account>_<mailbox>/<uid>.md` with YAML front matter:

```yaml
---
uid: "12345"
account: default
mailbox: INBOX
subject: Hello there
from: sender@example.com
to:
- you@example.com
cc: []
date: "01 Jan 2026 12:00:00 +0000"
flags: []
---

Mail body here...
```

**Always sync before reading mail.** After syncing, read `.md` files directly — the body starts after the second `---`.

---

## List Mailboxes

List all available IMAP folders for the account:

```bash
weavmail mailbox
```

Use this to discover exact folder names before syncing a non-INBOX mailbox. Folder names are case-sensitive.

---

## Move a Mail

Move an email to another folder, then automatically sync the source mailbox:

```bash
weavmail move mails/default_INBOX/12345.md "Archive"
```

The source mailbox is synced after the move — the local file will be deleted automatically.

To delete a mail, move it to the Trash folder. The exact name varies by provider (e.g. `Trash`, `Deleted Messages`, `[Gmail]/Trash`). Use `weavmail mailbox` to find the correct name first.

---

## Trash a Mail

Move one or more emails to the account's trash mailbox, then automatically sync the source mailbox:

```bash
weavmail trash mails/default_INBOX/12345.md
weavmail trash mails/default_INBOX/12345.md mails/default_INBOX/67890.md
```

Multiple `MAIL_FILE` arguments can be passed for batch operations. The trash mailbox is read from each mail's account `--trash-mailbox` configuration. An error is raised if `--trash-mailbox` is not configured for the account.

The source mailbox is synced after the move — the local file will be deleted automatically.

---

## Archive a Mail

Move one or more emails to the account's archive mailbox, then automatically sync the source mailbox:

```bash
weavmail archive mails/default_INBOX/12345.md
weavmail archive mails/default_INBOX/12345.md mails/default_INBOX/67890.md
```

Multiple `MAIL_FILE` arguments can be passed for batch operations. The archive mailbox is read from each mail's account `--archive-mailbox` configuration. An error is raised if `--archive-mailbox` is not configured for the account.

The source mailbox is synced after the move — the local file will be deleted automatically.

---

## Send a Mail

Write the body to a file, then send:

```bash
cat > /tmp/body.txt << 'EOF'
Your message here.
EOF

weavmail send \
  --to recipient@example.com \
  --subject "Hello" \
  --content /tmp/body.txt
```

`--to`, `--cc`, and `--bcc` are all repeatable for multiple recipients. `--from` defaults to the first configured address.

---

## Reply to a Mail

```bash
weavmail send \
  --reply mails/default_INBOX/12345.md \
  --content /tmp/reply.txt
```

In reply mode, `subject`, `to`, and `from` are all inferred from the original mail's front matter. The original body is quoted and appended. `In-Reply-To` and `References` headers are set automatically. Override any of them with explicit options if needed.

---

## Notes

- **Never guess UIDs.** Always sync first, then reference files from the output.
- **Mailbox names are case-sensitive.** Use `weavmail mailbox` to list exact names.
- The `mailbox` field in front matter stores the original unescaped name (e.g. `INBOX/Sent`); the directory path uses `_` as a separator.
- Front matter is authoritative for metadata — always read it from the `.md` file.
- All commands support `--help` for full option details, e.g. `weavmail sync --help`.

---

## Multiple Accounts

Configure additional accounts by providing a name:

```bash
weavmail account config work \
  --imap-host imap.work.com \
  --smtp-host smtp.work.com \
  --username you@work.com \
  --password your-password \
  --addresses you@work.com
```

Pass `--account` to target a specific account where supported:

```bash
weavmail mailbox --account work
weavmail send --account work --to someone@example.com --subject "Hi" --content /tmp/body.txt
```

`weavmail sync` always syncs **all** configured accounts using each account's `sync_mailboxes` config.

For `move` and `send --reply`, the account is read from the mail file's front matter — you may pass `--account` as a safeguard: if it doesn't match the account in the front matter, the command will exit with an error. For `trash` and `archive`, the account is always read from each mail file's front matter (no `--account` option).
