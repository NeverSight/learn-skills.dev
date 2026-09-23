---
name: open-loops
description: Extracts the unresolved commitments, deferrals, decisions, and open questions from a conversation transcript into a small JSON ledger — so a different surface (a cron job, a trigger, a fresh session) can pick them up instead of dropping them. Use to hand off context across surfaces, or to gate a session/thread handoff on how much is left open.
when_to_use: A long-lived agent talked to its owner in a thread and made promises or deferred things there, and a scheduled job / trigger / new session is about to act with no knowledge of that thread — you want the still-OPEN loops surfaced so nothing is repeated or forgotten. NOT for summarizing a conversation (it only tracks what's unresolved), and NOT an LLM (it's fast, offline, deterministic triage).
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [context-engineering, memory, handoff, cron, agents]
---

# Open Loops

Carry the thread's unfinished business across the wall between surfaces.

## Overview

A long-lived agent chats in a thread — "I'll charge the car later", "let's go
with plan B", "I'll clean up the README" — then a **scheduled job fires with zero
memory of that thread** and either repeats a finished task or silently drops a
pending one. The conversation and the cron/trigger surfaces don't share a brain.

`open_loops.py` reads a transcript and extracts only what is still **open**:

- **→ commitment** — "I'll do X", "할게요" (closed when a later turn says it's done)
- **⏳ deferral** — "later", "나중에", "follow up" (closed on completion)
- **◆ decision** — "let's go with X", "하기로" (recorded; never auto-closed — it persists)
- **? open_question** — a turn ending in `?` (closed by the first substantive reply)

It emits a small, stable JSON ledger the scheduled surface loads **before it
acts** — the missing handshake between a thread and everything that fires later.
Bilingual (EN + KO), pure standard library, deterministic. A ruler for handoff
hygiene, not an LLM.

## When to use

- **Cross-surface handoff:** a cron job or trigger loads the ledger for the
  relevant thread before running, so it knows what the owner is still waiting on.
- **Session handoff hygiene:** before ending a session or spawning a fresh one,
  gate on open-loop count — refuse a "clean" handoff that leaves 8 promises open.
- **Self-audit:** an agent checks whether it left commitments dangling in a thread.

Not for: summarizing a conversation (this tracks only the unresolved), sentiment,
or verifying that a closed loop was *actually* done (it trusts the "done" signal).

## The method

1. **Get the transcript.** JSONL (`{"role","content"}` per line or a JSON array),
   or plain text with `[speaker] message` / `speaker: message` lines.
2. **Extract the ledger.**
   ```bash
   python scripts/open_loops.py thread.jsonl --json
   # or:  cat thread.txt | python scripts/open_loops.py -
   ```
3. **Feed `open_loops` to the scheduled surface.** In a cron/trigger prep step,
   read the JSON and inject the open commitments/deferrals into that run's context
   so it acts *with* the thread, not blind to it.
4. **Gate a handoff.** Refuse to call a handoff clean when too much is dangling:
   ```bash
   python scripts/open_loops.py thread.jsonl --max-open 5   # exit 1 if >5 open
   ```
5. **Re-run after closing loops.** Say "done"/"끝났어요" in the thread and watch the
   commitment move from open to closed on the next extract. Open count is the score.

## Anti-patterns

- **Treating it as a summarizer.** It deliberately ignores everything that isn't an
  open loop. If you want a recap, use a recap tool.
- **Trusting a closed loop as verified.** A loop closes on a "done" *signal*, not on
  proof the work happened — pair with real verification for anything that matters.
- **Over-tuning the regexes into false positives.** A noisy ledger a cron job trips
  over is worse than a conservative one that misses an edge case. Keep it tight.
- **Auto-closing decisions.** Decisions persist by design — they describe a standing
  choice, not a task; don't "resolve" them just to zero the count.

## Example

```
$ printf '[민서] charge the car tonight\n[bob] set the charge later\n[민서] and what do you think of plan B?\n' \
    | python scripts/open_loops.py -
OPEN LOOPS: 2  (commitments 0, deferrals 1, decisions 0, questions 1)  | closed 0
  ⏳ [deferral] (bob) set the charge later
  ? [open_question] (민서) and what do you think of plan B?
```

The cron job that fires at 9pm can now read that ledger and know the car charge is
still owed — instead of firing blind.
