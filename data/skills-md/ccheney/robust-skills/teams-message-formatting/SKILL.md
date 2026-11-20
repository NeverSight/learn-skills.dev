---
name: teams-message-formatting
description: Format or debug Microsoft Teams bot text, Adaptive Card text, and Graph chatMessage bodies. Use for markup, mentions, links, escaping, or client rendering issues; not card layout/actions or ordinary Teams conversation retrieval.
---

# Teams Message Formatting

Format supplied text for the Teams surface that receives it. The user's explicit instructions take precedence over this skill's guidelines.

## Identify the text system

Use the content, destination field, and existing payload or SDK as input. Infer the text system from that context; ask for the destination when the missing choice changes syntax or mention metadata.

| Surface | Text format | Mention metadata |
|---|---|---|
| Bot activity `text` | Bot Markdown or `textFormat: "xml"` subset | Activity `entities` |
| Adaptive Card `TextBlock` / facts | Limited Markdown, no HTML | Root `msteams.entities` |
| Graph `chatMessage.body` | `text` or Teams-restricted `html` | Body `<at id="N">` plus matching `mentions` entry |
| Hero/thumbnail card `text` | XML/HTML subset | Surface-specific; titles/subtitles are unformatted |

Slack mrkdwn is not Teams markup. Adaptive Card Markdown does not support headings, tables, images, code fences, or blockquotes; use supported card elements when those structures are requested. Text-only content does not require a card.

## Preserve text and identity

- Escape for the receiving syntax, then serialize JSON. Do not concatenate unescaped user text into HTML/XML or mention markup.
- Keep visible mention text and its metadata synchronized. Use supplied or resolved IDs; display names are not identity evidence.
- Respect client differences, such as bot-list support on mobile. Do not change a transport just to fix punctuation.
- For a Graph payload, distinguish ordinary delegated sends from migration permissions. An app-only notification requires a supported delivery path; explain a missing capability without pretending the payload creates it.

Return the requested text, corrected string/object, or integration patch, preserving meaning and the known surface. Identify any missing runtime IDs or unverified client behavior. Posting is separate from formatting and requires the user's request or existing authorization.

## References

Load the relevant format or metadata details only.

| Task | Reference |
|---|---|
| Bot Markdown/XML, card Markdown, hero cards, legacy text | [MARKDOWN-HTML.md](references/MARKDOWN-HTML.md) |
| Bot/card/Graph mentions; users, tags, teams, channels | [MENTIONS.md](references/MENTIONS.md) |
| Graph HTML, code/emoji tags, attachments, permissions | [GRAPH-CHATMESSAGE.md](references/GRAPH-CHATMESSAGE.md) |
| Compact surface and syntax lookup | [CHEATSHEET.md](references/CHEATSHEET.md) |

For card layout/actions, use `teams-adaptive-cards` if installed or the [Teams card documentation](https://learn.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-reference). This text-formatting workflow does not depend on another skill being installed.
