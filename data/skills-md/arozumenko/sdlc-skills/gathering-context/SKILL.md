---
name: gathering-context
description: Use when the user says 'what do we know about X', 'find prior discussions with Y', or before drafting any reply where prior history matters. Gathers cross-channel context (local KB, email, Teams, optional web) about a person or topic before responding.
license: Apache-2.0
compatibility: Requires MS Graph tools (search-query, list-mail-messages, get-mail-message, find-chat, list-chat-messages). Web search optional.
metadata:
  authors:
    - Artem Rozumenko <artem_rozumenko@epam.com>
  version: "0.1.0"
---

# Context Gatherer

Find prior discussions, decisions, and commitments across channels — fast. Walk channels in cost order and stop early when you have enough.

## Inputs

- **Person** — name or email
- **Topic** — short phrase
- **Time window** — default: last 2 weeks. Widen only if the topic clearly demands history.

## Search Order (fast → slow)

### 1. Local knowledge base
- If a local index exists (e.g. `.knowledge/threads.json`), `Read` it and `Grep` for the person's email and topic keywords.
- This gives pre-summarized threads — usually enough on its own for routine asks.

### 2. Email
- `search-query` with `from:<email> AND <keywords>` (and `to:<email>` variant).
- Fall back to `list-mail-messages` + manual filter if `search-query` is unavailable.
- Pull bodies with `get-mail-message` only for the top 3–5 hits — never bulk-read.

### 3. Teams chats
- `find-chat` by name → `list-chat-messages` for the matched chats with recent activity.
- **Aggregate consecutive messages** from the same sender within ~2 minutes into one turn before summarizing — people fragment messages and raw dumps are noisy.

### 4. Web (only if needed)
- `tavily_search` for **public** topics (announcements, vendor docs). Never web-search internal/private topics.

Stop as soon as you have enough to answer the question. Don't exhaust every channel by default.

## Output

Max ~500 words. Facts, not essays.

```
## Context for <person> — <topic>

### Prior conversations
- [date] <channel>: <one-line summary>
- [date] <channel>: <one-line summary>

### Decisions & commitments
- <what was agreed, by whom, when>

### Related discussions
- <relevant context from other people/threads>

### Open items
- <anything unresolved or pending>
```

If nothing relevant exists, say so in one line. **Never fabricate context.**

## Rules

- Default window: last 2 weeks. Widen only with explicit need.
- Summarize — never paste raw email bodies or message dumps.
- Mask PII / credentials encountered in searches.
- If channels disagree, flag the conflict rather than picking a side.
- Aggregate Teams message bursts before summarizing.
