---
name: wdym
description: Reframe the previous answer so it lands — plain, distilled, at the reader's level. User-invoked only.
disable-model-invocation: true
argument-hint: "[tldr = too long; didn't read | eli5 = explain like I'm 5 | in <language>]"
---

Someone read the last answer and thought *"wait — what do you mean?"*
Say it again so it lands. Same truth, clearer path in.

## Read the room first

- **Target** the previous answer, or the part the user pointed at.
- **Gauge the reader's level** from the session — their own questions and
  feedback show how technical they are. Reframe to *that* level, not yours.
- **Find the one point** they most need. It leads.

## Pick the technique that fits — not all of them

Match the tool to *why* the answer failed:

- **Reorganize** — content was fine, order buried it. Point first (BLUF),
  then support. Often this alone is enough.
- **Cut jargon** — swap or define every term the reader wouldn't use themselves.
  Apply STE-style rules: one verb per sentence, no nominalizations
  ("perform a calculation" → "calculate"), use the simplest verb that fits.
  Names, identifiers, flags, and error types stay verbatim.
- **Analogy** — one fresh, everyday comparison for the hardest idea. No worn-out metaphors.
- **Show it** — a small table, ASCII diagram, or before/after when structure or
  comparison is the point. A picture beats prose.
- **Layer** — lead with the simple version; add detail only if it's load-bearing.
- **Their language** — if the reader writes in another language, reframe in it.
  Gloss every abstract term you keep; commands and code identifiers stay verbatim.

## Levels — user can pass a hint

- *(default)* — infer the reader's level from the session
- `tldr` — *too long; didn't read*: tight and to the point, keep the terms (for a busy peer)
- `eli5` — *explain like I'm 5*: no jargon, explained with an analogy (for a non-expert)
- `in <language>` — reframe in that language

## Guardrail: distill, never distort

Drop tangents freely. Never change a technical claim, invent an example, or bury
a real caveat or risk. Efficiency is fewer ideas, not shaded truth.

Carry through verbatim what the reader cannot re-derive: numbers and thresholds,
exact identifiers and flags (column names, sort order, `CONCURRENTLY`), named
error types, and the cause→effect link.

Output only the reframe. No "here's what I changed".
