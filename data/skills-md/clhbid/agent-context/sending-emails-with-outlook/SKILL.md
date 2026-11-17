---
name: sending-emails-with-outlook
description: "Outlook email bodies through the Microsoft 365 connector: bare HTML, paragraph spacing for a new message or a reply, and changing a draft. Use when drafting, replying to or sending Outlook email."
---

# Sending emails with Outlook

How to write the body of an email made with the Microsoft 365 connector's mail tools. Find the tools
by capability (create draft, reply-all draft, delete draft, send), since their names change between
connector versions.

**Leave a draft for the user to send** unless the task says to send it; then build the draft by
this skill and send that.

## Before drafting

- Settle every open choice with the user first, so the draft is sent as written.
- Show the text in chat as plain text, with a blank line between paragraphs and tables as tables,
  so the user can read it there or paste it into Outlook.
- Unless the caller specifies a fixed body, end with the user's sign-off, taken from their recent sent mail.

## Paragraph spacing

Write bare `<p>`, `<ul>`, `<ol>`, `<li>`, `<b>` and `<table>` tags. The connector rejects the
whole call if any tag carries an attribute, except a link's `<a href="…">`. It stores and sends the
body exactly as written, so spacing depends on who sends the draft:

- **The user sends it from Outlook**: Outlook's editor restyles every `<p>` on send, by whether
  the message starts a thread:

  | Message            | Outlook gives each `<p>` | Write                                                                                    |
  | ------------------ | ------------------------ | ---------------------------------------------------------------------------------------- |
  | New                | a 1em margin             | One `<p>` per paragraph, with nothing between them. A spacer doubles the gap             |
  | Reply or reply-all | no margin                | `<p>&nbsp;</p>` between paragraphs, before and after each table, and before the sign-off |

- **You send it with the connector**: the reader's mail app gives each bare `<p>` its default
  margin, so write one `<p>` per paragraph with nothing between them, new message or reply.

Lists keep their own margin in every case, so they need no spacer.

## Changing a draft

An update replaces the whole body, and the connector rejects the attributes Outlook writes, so
text carried through loses its formatting. Read the draft first: treat Outlook-added `class` or
`style` attributes in the editable body, outside the quoted thread, as a user-saved draft.

- **New message, not saved by the user**: update it in place.
- **Reply or reply-all, not saved by the user**: create a new reply draft, since an update drops
  the quoted thread.
- **Saved by the user**: tell them what to change, so their edits keep their formatting.

Delete a draft you replace, or, when the task forbids deleting mail, name it for the user to delete.

## Without the connector

When the session has no claude.ai connectors, run a CLI session that pre-approves the drafting
tools and denies the sending ones. A deny rule wins over any allow the session inherits from
settings, so the draft stays the user's to send:

```bash
m=mcp__claude_ai_Microsoft_365
claude -p "<task>" \
  --allowedTools "ToolSearch ${m}__outlook_email_search ${m}__outlook_create_draft ${m}__outlook_update_draft ${m}__outlook_create_reply_draft ${m}__outlook_create_reply_all_draft ${m}__outlook_delete_draft" \
  --disallowedTools "${m}__outlook_send_draft ${m}__outlook_send_mail ${m}__outlook_forward_mail"
```
