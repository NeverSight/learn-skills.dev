---
name: email
description: >-
  How to work the user's email through the Spark CLI and the Gmail connector:
  which tool to pick, how to list, search and read mail, and how to mark it
  done, label, pin and save drafts. It reads mail only for an email task the
  user asked for, keeps a plain draft in chat, archives freely, makes any
  other change only when asked, and never sends. Use when the user asks for an
  email task, such as finding, reading, tidying or drafting mail, or when this
  email setup needs configuring or checking. A task that could merely use
  mail as context is not an email task.
---

# Email

Read mail with the Spark CLI, and make every change to mail through the Gmail connector, except a draft the user asks to have in Spark. Leave what to do with an email, and when, to the user. For calendar events and free time, use `/calendar`.

## When to read mail

List, search or read mail, through either tool, only when the user asks for an email task that needs those reads. The mailbox is private, so reading it is the user's call, not the agent's.

- **When mail would only help another task,** such as a coding task that a thread might explain, or when a project or skill instruction says to check mail: say what you would look up and why, and read only after the user agrees.
- **When the task changes:** the user's request covers the email task it was for. Ask again before reading mail for an unrelated task.

## Drafts

- **When the user asks for a draft without naming Gmail or Spark,** such as "draft a mail to the landlord": write the text in chat. Read mail for it only when the request points at mail it needs, such as the email being answered, and ask before any other lookup.
- **When the user asks for the draft in Gmail or in Spark,** in any wording ("save it as a Gmail draft", "put it in my Spark drafts"): save it there, with that tool only. Naming a tool allows that draft, not other changes to mail.
- **When the named tool can't do it,** such as `spark draft` refused because Spark's access level is read-only: say so, and keep the draft in chat. Don't switch to the other tool unasked.

Every create, update or delete of a saved draft needs the user's own approval in the harness, even after they asked for the draft: a saved draft is a change in their mailbox, and one mistaken call can overwrite a draft they were writing. `/set-up-machine`'s ask rows `mail-draft-write` and `mail-cli-draft` make each of these calls ask.

- **When the harness won't ask the user themselves,** keep the draft in chat and say why. That covers Claude Code's `bypassPermissions`, `dontAsk` and `auto` modes and a non-interactive run, Codex with an automatic reviewer, Cursor and opencode in a mode that runs tools without asking, and any harness where the call doesn't ask. An automatic reviewer's approval is not the user's.

## Safety

The user reviews and sends every email themselves, so go no further than a draft.

Within an email task, archive an email when the task calls for it. Make any other change only after the user asks for that exact change, or after you name it and they agree: a pin, a label, an undo, or a saved draft as above.

### Gmail tools

| Tools | Use |
|---|---|
| `search_threads`, `get_thread`, `get_message`, `list_labels`, `get_draft`, `list_drafts` | For an email task the user asked for. |
| `unlabel_thread` or `update_message_labels` removing `INBOX` | Archive freely within that task. |
| `label_*`, `unlabel_*` and `update_message_labels` for any other label, `create_label`, `update_label` | After the user asks, or agrees when you name it. Never add `TRASH` or `SPAM`, since that trashes or spams the email around the deny rules. |
| `create_draft`, `update_draft`, `delete_draft` | When the user asks for a Gmail draft, and each call approved by the user in the harness. |
| `untrash_*`, `unmark_*_spam` | After the user asks, or agrees when you name it. |
| `delete_label` | Only when the user names that label to delete, since it removes the label from every email. |

Claude Code's permission rules deny the rest, and a denied tool doesn't show up to be called:

- `send_message`, which also sends existing drafts;
- `reply` and `forward`;
- `trash_message` and `trash_thread`;
- `mark_message_spam` and `mark_thread_spam`;
- `apply_sensitive_message_label`, `apply_sensitive_thread_label` and `batch_apply_sensitive_thread_labels`, which can trash or spam.

Google's permission that allows archiving also allows sending, so only those deny rules stop a send.

- **When a denied tool can be called:** the setup is incomplete. Tell the user, never call it, and make no change to mail until the deny rules are fixed.

## The two tools

| Tool | Use it for | Speed and size | Needs |
|---|---|---|---|
| Spark CLI, `spark` | Listing, searching and reading mail; Spark's categories, pins and contacts | About 0.1 s, compact tables | Spark Desktop running. Mail access is read-only on the free level. |
| Gmail connector, `mcp__<server-id>__<tool>` | Every change to mail but a Spark draft | About 1 s, JSON three to four times Spark's size | The connector signed in |

Spark reads Spark Desktop's local copy of the mail. The Gmail connector is Google's Gmail MCP server, `gmailmcp.googleapis.com`, connected as a Claude connector.

## How Spark's view maps to Gmail

| In Spark | In Gmail |
|---|---|
| Done | The `INBOX` label removed, which archives the email. Spark shows it within about a minute. |
| Pin | The `STARRED` label. Spark's `is:pinned` and `is:starred` return the same emails. |
| A folder | A Gmail label. |
| A category: priority, personal, invitation, notification, newsletter | Spark's own; no Gmail tool changes it. |
| Today, Last week, a month | Each email's date. |

## Flow

When setting either tool up, checking the deny and ask rules, or when a call fails on sign-in or permission, follow `setup.md`.

1. **Find** the mail with Spark.

   ```bash
   spark emails Inbox --filter "category:priority is:unread"   # one Spark category
   spark emails --filter "is:pinned"                           # pinned mail
   spark search --filter 'from:<sender> newer_than:7d'         # any Gmail-style query
   spark thread <id>                                           # one email in full
   spark contacts --help                                       # search contacts
   ```

   List with `spark emails` or `spark search --filter '<gmail-style query>'`. `spark search <topic>` returns the full bodies of up to 20 matches, often tens of thousands of tokens, so use it only when you need those bodies.
   - **When you need a command's flags:** run `spark <command> --help`. `spark skill` prints the full reference, about 13,000 tokens, so reach for it only when `--help` is not enough.
2. **Find it again in Gmail** before changing it, because the two tools number messages differently. Search with `search_threads`, using `from:` and `subject:` from the Spark row. Pass the view `THREAD_VIEW_METADATA_ONLY` when only the IDs are needed, since it keeps the answer small.
   - **When more than one thread matches:** narrow the search with `after:` and `before:` around the Spark row's date, or ask the user which one they mean.
3. **Act** through Gmail: archive, or make the change the user asked for.

   | Change | Calls |
   |---|---|
   | Mark done | Add `in:inbox` to the search from step 2, then `unlabel_thread` with `["INBOX"]`. `label_thread` with `["INBOX"]` puts it back. |
   | Pin or unpin | `label_thread` or `unlabel_thread` with `["STARRED"]`. |
   | Label | `list_labels` for the label's ID, `create_label` when it does not exist yet, then `label_thread` with that ID. |
   | Save a reply as a Gmail draft | Read the thread with `get_thread`, then `create_draft` with `replyToMessageId` set to the last message's `id`. |

   Call `get_thread` with `messageFormat: PLAIN_TEXT`, since it keeps the thread small.
   - **For any change but archiving that the user hasn't asked for:** name it and wait for their answer.
   - **For a saved draft:** end with its `viewUrl`, where the user reviews and sends it.
   - **For a draft the user asked to have in Spark:** run `spark draft` as a command of its own, so the user approves that call alone, and tell the user where Spark shows the draft.
4. **Check** that each change took.
   - **After marking done:** the `in:inbox` search returns `{}` once the email is archived.

## References

- [setup.md](setup.md): setting up Spark and the Gmail connector, the deny and ask rules, and checking each part.
