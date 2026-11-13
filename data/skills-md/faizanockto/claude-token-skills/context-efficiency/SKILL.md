---
name: context-efficiency
description: "Apply per-turn tactics to keep token consumption low across coding sessions — constrain bulk tool outputs at the source, avoid re-reading files within a session, prefer Edit over Write for changes, fire independent tool calls in parallel, and don't quote tool results back in prose. Trigger on any multi-step coding work — debugging, refactors, investigations, anything that involves more than a couple of tool calls. These tactics are individually small but compound across a session: a 10% saving per turn becomes a 10% saving on every future turn too. Use alongside [[delegate-reading]] when bulk reading is also on the path."
---

# Context efficiency

## The principle

Every token in the working context is reprocessed on every subsequent turn. Tactics that keep the context small and stable compound — saving 10% per turn means saving 10% on every future turn too. Most of these tactics are cheap to apply correctly; the cost of forgetting is hidden because it shows up as a slowly growing per-turn bill, not a single visible spike.

This skill collects the per-turn habits worth keeping. For bulk-reading specifically, see [[delegate-reading]] — same principle, applied to the heaviest case.

## Tactics

### 1. Constrain bulk outputs at the source

Many shell commands return unbounded output by default. A bare `git log`, `find .`, `tree`, broad `grep`, `cat large.log`, `npm ls` can dump thousands of lines straight into context, where they stay for the rest of the session.

Pin every command:

| Default (bad) | Pinned (good) |
|---|---|
| `git log` | `git log --max-count=20 --oneline` |
| `find .` | narrow path + `-maxdepth N` |
| `grep -r pattern` | scope to a dir + `--include='*.kt'`, optionally pipe through `head` |
| `cat large.log` | `tail -100 large.log`, or grep for the relevant line first |
| `tree` | `tree -L 2`, or narrow to a subdir |
| `npm ls` | `npm ls --depth=0` |

If the answer is going to be one fact (latest commit message, last error line, top-level package list), the command should return one screen, not the world. A common slip: running an unconstrained command to "just check" something, then dragging the entire output along for the rest of the session.

### 2. Don't re-read the same file in a session

Once a file is in context as a tool result, it stays there. Re-Reading the same file later doesn't refresh anything for the model — it just duplicates the content and can shift the prompt cache boundary.

Before opening Read on a file, scan the conversation for a prior read. If the content is still relevant and the file hasn't been edited since, work from the existing tool result. If it *has* been edited, re-reading is fine — but only if the new content actually matters for the next decision. The Edit tool's success message tells you what changed; trust it for confirmation.

### 3. Edit, not Write, for changes to existing files

Edit sends only the `old_string` / `new_string` diff to the model. Write puts the entire new file content into the tool call. On a 500-line file with a 3-line change, Edit is roughly two orders of magnitude cheaper.

Reserve Write for genuinely new files or true full-file rewrites. The cost asymmetry isn't visible turn-to-turn — it shows up as a much larger conversation history when scrolling back later.

### 4. Parallelize independent tool calls

When the result of tool A is *not* an input to tool B, fire them in the same message. They execute concurrently. The token cost is identical, but the conversation has fewer turns — which means less prompt overhead, less cache decay between turns, and faster wall-clock for the user.

Anti-pattern: a chain of single-tool turns when three could have gone out together.

Independence check: if you don't know what A will return, but you know what B needs to do regardless, they're independent. Fire both. Same for reads, greps, and most status commands (`git status` + `git diff` + `git log` is a classic parallel triple).

### 5. Don't quote tool results back in prose

The tool result is already in the context. Restating its content verbatim — "I see that the file contains the following: \[pastes 40 lines\]" — duplicates the content into the assistant message, which gets reprocessed on every future turn.

State conclusions, not the evidence. A one-sentence synthesis ("the auth middleware is at AuthFilter.kt:42 and is called from three places") is fine and useful. A re-paste of the grep output isn't. The user (and future turns) can scroll back to the raw tool result if needed.

## What's deliberately outside this skill

These help efficiency too, but they aren't per-turn agent behaviors — they're either user actions or one-time setup, so they live elsewhere:

- **`/clear` at task boundaries** — only the user can run it. Useful when starting an unrelated task in the same session.
- **`/model` switching mid-session** — user-side. For routine work, Haiku or Sonnet are 5–15× cheaper than Opus.
- **Trim CLAUDE.md and MEMORY.md** — one-time edits to files that load on every session. The single highest-leverage action available, since the saving is paid forever.
- **Pre-allow safe commands** — use the `fewer-permission-prompts` skill to write an allowlist for read-only Bash commands, cutting approval round-trips.

If the user asks how to reduce token usage and these would help, suggest them — but they aren't tactics this skill applies on its own.

## Why this matters

Prompt caching only helps when the early context is stable. Every large insertion or reordering can invalidate the cache window. Most of the tactics above are about *not adding* — keeping the working set small and predictable. Caching does the rest of the work.

The cumulative effect over a long session is large. A session that runs 50 turns with a 30% bloated context isn't 30% more expensive overall — it's 30% more expensive *per turn*, multiplied by 50 turns of accumulated cost. Small per-turn habits dominate large one-shot optimizations.
