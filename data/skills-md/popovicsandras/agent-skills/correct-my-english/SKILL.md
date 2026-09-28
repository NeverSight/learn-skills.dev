---
name: correct-my-english
description: Reviews and corrects English prose for grammar, spelling, and non-native phrasing. Supports guide mode (recommendations, chunk by chunk) and auto mode (applies fixes). Use when the user asks to correct, proofread, or polish their English writing.
disable-model-invocation: true
argument-hint: "[auto|guide] [file-or-text]"
agent: task
model: sonnet
---

# correct-my-english

Corrects or reviews English text in two modes.

## Usage

```
/correct-my-english
/correct-my-english guide path/to/document.md
/correct-my-english auto path/to/document.md
```

## Input sources

1. **Referenced file** — read and edit the file the user `@`-mentions or passes as an argument.
2. **Inline text** — return the fully corrected text in the response (no file to edit).

If no source is given, ask the user for text or a file path.

## Parameters

| Parameter | Values | Required |
| --------- | ------ | -------- |
| `mode` | `guide` \| `auto` | Yes |
| `source` | File path, `@`-referenced file, or inline text | No — ask if missing |

## Mode selection

1. Parse `mode` from the invocation or user message (`guide` or `auto`).
2. If `mode` is **not** provided, **stop** and ask the user to choose. Prefer the host's structured question tool when available; otherwise ask in chat (fallback below).

   | Host | Tool | Notes |
   | ---- | ---- | ----- |
   | Cursor | `AskQuestion` | Multiple-choice UI |
   | Claude Code | `AskUserQuestion` | Multiple-choice UI; not available in subagents (this skill uses `agent: task`) |
   | GitHub Copilot | `AskQuestions` (`#askQuestions`) | Requires `github.copilot.chat.askQuestions.enabled` (experimental) |

   Structured question (adapt to the tool's schema):

   - Prompt: "Which correction mode?"
   - Options: **guide** — recommendations, step by step; **auto** — apply all fixes

   **Fallback** (when no structured tool is available):

   > Which mode? **guide** (recommendations, step by step) or **auto** (apply all fixes)?

3. Do not start reviewing or editing until `mode` is known.

## What to look for

- Grammar errors (subject–verb agreement, articles, incomplete sentences, fragments)
- Spelling and typos
- Non-native or awkward phrasing
- Punctuation (`etc.` vs `etc...`, commas, hyphens in compound adjectives)
- Missing or extra words (`a`, `the`, `from`, `to`)
- Inconsistent terminology within the document

**Do not** rewrite for style, tone, or "better prose" unless something is genuinely unclear or ungrammatical.

## Branching

| Mode | Reference |
| ---- | --------- |
| `guide` | [references/guide-mode.md](references/guide-mode.md) |
| `auto` | [references/auto-mode.md](references/auto-mode.md) |

After mode is resolved, read the matching reference file and follow it for the rest of the session.
