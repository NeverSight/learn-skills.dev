---
name: delegate-reading
description: "Keep raw bulk content out of the working context on multi-file tasks. Trigger whenever a task involves scanning a codebase, locating symbols across many files, summarizing directories, surveying repo state, auditing a branch, answering \"where is X\" or \"which files touch Y\", or any \"read a lot, decide a little\" work — even if the user didn't explicitly mention subagents, cost, or efficiency. Applies whether running as the top-level orchestrator (where subagent delegation is the strongest tactic) or as a subagent that can't recurse (where the same principles apply via search-first, narrow reads, and digesting before propagating). Lean toward applying this whenever bulk reading is on the path — context discipline is the single biggest lever for reducing token consumption."
---

# Delegate reading

## The principle

Every token of raw source pulled directly into the working context stays there for the rest of the session, ages out the prompt cache, and gets reprocessed on every subsequent turn. Bulk reading is grunt work — get the *digest*, not the raw source. The goal isn't "always use subagents." The goal is: **the raw text of large files should never settle into the context that has to keep thinking.**

Subagent delegation is the strongest version of this pattern (the bulk text lands in a context that gets discarded), but the same principle applies even when subagents aren't available. What changes is the tactic, not the discipline.

## Tactics, in priority order

Apply the cheapest tactic that does the job. Escalate only when the cheaper one can't answer the question.

### 1. Search before reading

Grep is dramatically cheaper than Read. Often the grep output *is* the answer — file paths, line numbers, hit counts, a one-line context per match. There's no need to open the file at all.

Run `grep -rn <pattern> <scope>` (or equivalent) first. Inspect the matches. Only Read a file when the grep output isn't enough to act on.

Anti-pattern: reading 5 files to find which one mentions a symbol that a single grep would have located instantly.

### 2. Read narrowly

When a Read is unavoidable, scope it. The `Read` tool supports `offset` and `limit` — use them. If grep said the symbol is on line 312, read lines 290–340, not the whole 2000-line file.

Anti-pattern: Reading entire files "to get context" when the relevant region is 30 lines. The other 1970 lines now live in context, never to be useful, costing tokens on every turn.

### 3. Delegate to a subagent (orchestrator only)

When the task genuinely requires reading many files end-to-end — multi-file surveys, "summarize this module's responsibilities", cross-cutting audits — spawn a subagent with a cheaper model to do the reading. The subagent's context absorbs the raw text and is discarded when it returns. Only its summary (a few hundred tokens) lands in the orchestrator.

This tactic is only available at the orchestrator level. Subagents can't spawn further subagents — if running inside one, fall back to tactics 1 and 2 with extra discipline.

See [Subagent delegation](#subagent-delegation) below for how to do this well.

### 4. Digest before propagating

Tool results land in context whether or not the next message references them. After a large tool result (a `Bash` output, a long grep, a subagent return), extract the few facts that matter for the next step and proceed — don't echo the full result back in your own messages. Subsequent turns will look at the conversation including the orchestrator's own writing; verbose self-narration permanently inflates the working set.

This is a discipline thing, not a mechanism — it just means: act on what you learned, don't re-paste it.

## Subagent delegation

When the orchestrator decides bulk reading is unavoidable, route it through a subagent.

### When to spawn

- Three or more large files (>200 lines each) need to be read to answer one question.
- The user asked for a survey or audit ("what's in this repo?", "what's left to ship?", "anything weird about this branch?").
- The next step is grep + read + cross-reference, and the cross-reference reasoning is more valuable than the raw files.
- A digest is what's actually needed for the next decision — the raw content was never the point.

### When NOT to spawn

- The exact file and line are already known. Read directly.
- The file is about to be edited. Read it firsthand — the edit needs to be grounded in what's actually there, and a subagent's summary is too lossy.
- The whole job is one or two small files. Subagent overhead (prompt + own thinking + round-trip) exceeds the savings.
- The orchestrator already has the answer in its context from a prior turn.

### Picking subagent_type

| Type | Best for |
|---|---|
| `Explore` | Read-only search — "where is X", "find files matching Y", "which callers of Z exist". The default for pure retrieval. Can't write files. |
| `general-purpose` | Multi-step research, or work that needs to read + reason + write its output to disk. Slower and pricier than Explore. |

### Picking model

Match to the judgment the work actually requires.

| Model | When |
|---|---|
| `haiku` | Pure retrieval, grep-style lookups, mechanical summarization, listing matches. |
| `sonnet` | Bulk reading + light reasoning ("explain this module's responsibilities", "summarize what this PR changes"). |
| `opus` | Rare for read-only work. If the work needs Opus-level reasoning, the orchestrator should usually do it directly so the conclusion can immediately shape next steps. |

Inheriting the orchestrator's model is the wrong default for retrieval. Override it explicitly.

### Briefing pattern

The subagent starts cold — no memory of this conversation. Brief it like a colleague who just walked in:

```
Goal: <what's being accomplished overall>
Background: <one or two sentences of context the subagent needs>
Scope: <exact files, dirs, symbols — or "search the repo yourself">
Discipline: <baked-in tactics, see below>
Report back: <the specific format and length wanted>
```

Always cap response length explicitly: "report in under 200 words", "list paths only, no prose", "≤30 entries — if more, group by directory." Without a cap, subagents return verbose write-ups that defeat the savings — the orchestrator now has the long write-up *and* still has to read it.

### The subagent won't see this skill — bake the principles into the brief

Skills are loaded into the orchestrator's context only. A spawned subagent gets its own stripped-down environment and doesn't see anything in `~/.claude/skills/`. If the subagent is doing bulk reads — which it usually is, that's why it was spawned — the relevant discipline has to travel with the brief, not be assumed.

Add a one-line `Discipline:` field to every brief that involves reading. A good default:

> Search before reading. Read with offset/limit, not whole files. Don't paste raw file content in the response — return file:line refs with a one-line description per finding.

Without this, the subagent may load whole files into its own context — which costs its tokens, and produces a verbose report that costs the orchestrator's tokens when it returns. The savings collapse on both sides.

### Example briefs

Underbriefed — broad, no cap, will return paragraphs and probably miss the actual goal:

```
"Find all uses of SessionManager"
```

Briefed well — bounded, scoped, discipline baked in:

```
Goal: I'm about to refactor SessionManager.kt and need every caller.
Background: SessionManager lives in app/src/main/.../domain/scraping/.
Scope: app/src/main/java/nl/ockto/mobile and its subdirs.
Discipline: grep first; Read with offset/limit only when grep isn't enough;
  don't quote file contents in the response.
Report back: For each caller, file path:line and the calling line of code.
No commentary. ≤30 entries — if more, group by directory.
```

### Parallelism

If several independent lookups are needed, spawn them in a single message with multiple `Agent` tool calls. They run concurrently. Sequential subagent calls waste wall-clock time without saving any tokens. Independent = the result of one isn't an input to another.

### After a subagent returns

Its full report lands in context as a tool result — that *is* a cost, just a much smaller one than reading the raw files would have been. Extract what's needed and move on. There's no need to restate the findings back to the user unless they asked for them.

If the summary is missing something, continue the same subagent by name (via `SendMessage`) rather than spawning a new one — that avoids re-reading the same files from scratch.

## Why this matters

Prompt caching only helps when the orchestrator's context is stable. Every large file read directly pushes the cache window and risks invalidation. Keeping bulk content out of the working set keeps the conversation small, keeps the cache warm, and reserves the context budget for the judgment-heavy work that only the orchestrator can do.

Mental model: treat the orchestrator as a senior engineer whose attention is the scarce resource. Bulk reading is grunt work — search first, read narrowly, delegate when justified, digest before passing on. The principle is the same at every level; only the available tactics change.
