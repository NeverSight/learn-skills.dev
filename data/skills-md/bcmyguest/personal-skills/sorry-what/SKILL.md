---
name: sorry-what
description: Re-explain the previous response, or chosen numbered items from it, with the missing context, a code snippet of the proposed change, a diagram, or a plain high-level overview. Use when the user runs /sorry-what or says they did not follow the last answer.
argument-hint: "[item numbers, comma-separated] [what to focus on]"
---

# Sorry, what?

The user did not follow your last response. Explain it again so they can act on it.

## Arguments

The text after the command (`$ARGUMENTS` in hosts that substitute it) holds up to two parts, both optional:

- **Item numbers,** comma-separated (`2,4`). They refer to the numbered items in your last response. When it had no numbered items, count its top-level bullets or paragraphs from 1, and state the mapping in one line ("2 = the cache bullet"). Report numbers that match nothing.
- **Focus,** any text after the numbers ("why the cache matters", "show the code", "diagram"). It names what is unclear or which form to use.

No arguments: explain the whole last response.

## Pick one form per item

| The item is | Give |
| --- | --- |
| A proposed code change | The snippet: the current lines with `path:line`, then the changed lines as a diff. |
| A flow, structure, sequence, or set of states | A diagram, built as `to-diagram` says. |
| A claim resting on unstated facts | The missing context: the terms, the constraint, the reason, each in a sentence. |
| A long or dense passage | The overview: what it says in three sentences or fewer, and what the user should do with it. |

The focus text overrides the table.

## Rules

1. Start from what the reader lacks, not from the original wording. Do not restate the original.
2. Define each term on first use.
3. Read the code before you show it. A snippet comes from the file as it is now, never from memory.
4. Add no new claims. When the explanation shows the original was wrong, say so and correct it.
5. Keep each item under one screen. End with the one decision or action the user now faces, if there is one.
