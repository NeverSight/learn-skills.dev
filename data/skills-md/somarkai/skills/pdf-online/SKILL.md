---
name: pdf-online
description: Parse PDF, image, Word, or PPT files with SoMark and publish the result to Feishu, DingTalk, or Notion as editable documents, spreadsheets, record tables, or databases. Also use when an exact matching SoMark Markdown-and-JSON pair must be imported into one or more of these platforms.
---

# PDF Online

Route a publishing request to the existing platform adapter. This file is only
the entry point: do not reproduce, merge, or improvise platform conversion
rules here.

## Select the platform

- Feishu, Lark, a Feishu/Lark destination URL, cloud document, Feishu Sheet,
  or Bitable request: read [platforms/feishu/SKILL.md](platforms/feishu/SKILL.md)
  completely and follow it.
- DingTalk, Alidocs, a DingTalk destination URL, DingTalk document, online
  spreadsheet, or AI Table request: read
  [platforms/dingtalk/SKILL.md](platforms/dingtalk/SKILL.md) completely and
  follow it.
- Notion, a Notion destination URL, Notion page, or Notion database request:
  read [platforms/notion/SKILL.md](platforms/notion/SKILL.md) completely and
  follow it.
- When exactly one platform is implied, route directly. When the platform is
  genuinely ambiguous, ask only which of Feishu, DingTalk, or Notion to use.
- When the user explicitly requests multiple platforms, load only those
  platform modules and execute each independently.

Treat the selected platform directory as that adapter's skill directory.
Resolve every `scripts/...`, `references/...`, and `<skill-dir>` path in its
instructions relative to that platform directory, never relative to this root.
Read platform-specific references only when the selected module directs it.
Do not load or mix rules from an unselected platform.

## Shared parsing boundary

- Never invoke SoMark more than once for the same source in one task.
- For every raw PDF, image, Word, or PPT source, the Agent must invoke the
  separately installed official `somark-document-parser` Skill and obtain its
  Markdown-and-JSON result before running a platform adapter. The adapters do
  not contain the parser and must not search parent or sibling directories for
  a parser script.
- For one platform, give that exact pair to the selected adapter. For multiple
  platforms, invoke the parser Skill once and give the same pair to every
  selected adapter. A retry in one platform must reuse the same pair.
- When the user explicitly supplies an exact matching Markdown-and-JSON pair,
  do not invoke SoMark and do not search for replacements or historical
  results.

## Execution boundary

The selected platform module is authoritative for target-type routing,
conversion, publishing, verification, recovery, degradation, and user-visible
status. Keep its scripts and safety rules unchanged. A success or failure on
one requested platform does not authorize creating a replacement target or
rerunning SoMark for another platform.
