---
name: melech-cost
description: Show what coding-agent sessions cost for every worktree of the current repo — Cursor, Claude Code, and Codex — as handoff-style cards with dollars and tokens. Use when the user asks how much a repo, worktree, task, or session cost, wants a spend breakdown, or invokes `/melech-cost`.
disable-model-invocation: true
---

# Melech Cost

Answer "what did this repo cost me, and which task burned it?" from local
agent history. One script does all the work; the agent only runs it and
relays the result.

```text
/melech-cost                      # every worktree of this repo, top 8 cards
/melech-cost last 10              # 10 most recent sessions across all worktrees
/melech-cost <worktree>           # one worktree, its top 10 sessions
/melech-cost since 2026-09-01     # only sessions active since a date
```

## Run

Set `COST_SCRIPT` to `scripts/cost.py` beside this file (Python 3.9+):

```bash
python3 "$COST_SCRIPT" --cwd "$PWD"                        # default view
python3 "$COST_SCRIPT" --cwd "$PWD" --latest 10            # latest 10 sessions across all worktrees
python3 "$COST_SCRIPT" --cwd "$PWD" --worktree feature-a   # focus one worktree
python3 "$COST_SCRIPT" --cwd "$PWD" --since 2026-09-01     # date filter
python3 "$COST_SCRIPT" --cwd "$PWD" --cards 20             # more cards
```

Relay stdout as-is. It is already Markdown: a repo header, one card per
worktree, and a footnote. Do not recompute, round differently, re-sort, or add
numbers the script did not print. End with the `Full report:` path so the user
can open every worktree. Do not read the full report unless asked.

Card shape:

```text
### `feature-a` · ~$321
26d ago · 22 sessions + 36 subagents · cursor, claude · mostly `gpt-5.6-sol` (79%)
~394.1M tokens read (98% cached) · ~717k written

| Age | Cost | Read / Write Tokens | Model | Agent | Session | Topic |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1.4d ago | **~$187** | ~250.0M / ~400k | `gpt-5.6-sol` | cursor (+20) | `c747b3dc` | Users locked out after the SSO change… |
| 2d ago | **~$51** | ~80.0M / ~150k | `claude-opus-5-5` | claude | `bf32eff9` | Fix mode keeps editing the wrong file… |
```

`(removed)` marks a worktree that no longer exists on disk but still has
history. Subagent spend rolls into the session that spawned it.

## How it works

**Scope: this repo only, every worktree.** `git worktree list` gives the main
checkout and every live worktree, wherever it lives (Superset, Cursor, Codex,
Claude Code, or a plain sibling folder). A folder that holds this repo's
worktrees and no other repo's checkout also counts, so history from removed
worktrees in that folder is included. The main checkout's parent folder
(for example `~/code`) never counts, so sibling repos stay out.

**Sources and accuracy:**

| Agent | Where | Tokens |
|---|---|---|
| Claude Code | `~/.claude/projects/**/*.jsonl` | Exact: logged per message (input, cache write, cache read, output) |
| Codex | `~/.codex/sessions/**`, `archived_sessions/**` | Exact: last `token_count` total per session |
| Cursor CLI | `~/.cursor/chats/*/<id>/store.db` | Estimated: replays the stored ordered conversation |
| Cursor IDE | `state.vscdb` + `~/.cursor/projects/*/agent-transcripts` | Estimated: replay calibrated against Cursor's own context counter |

**Pricing.** Tokens × list price per model from
[`references/prices.json`](references/prices.json) (dated, per 1M tokens,
sourced from Cursor's, Anthropic's, and OpenAI's pricing pages). The first
matching rule wins. Unknown models, such as Auto, use a fallback rate, and the
footnote says how much that affected. Results are **API list-price value**. On
a subscription, part of it is covered by included usage.

**Cursor replay.** Cursor stores no billing counters locally, so each session
is replayed call by call:

- Every model call re-reads the prior prompt at the cached rate.
- New context (your message and tool results since the last call) is billed at
  the cache-write or input rate.
- The model's reply is billed at the output rate.
- When the context passes the model's limit, a summary resets it.

The IDE store drops file-read and search results. The replay therefore scales
each session to match Cursor's own "context tokens used" breakdown; sessions
without that breakdown use the median of this run's sessions, or 2.4× if there
are too few samples. Treat Cursor numbers as about ±30–40%. Hidden reasoning
tokens and cache misses after idle gaps aren't visible, so they push the true
number up.

## What it costs to run

The script is plain local Python: no model tokens and no network. It takes
about 10–40 seconds depending on history size. The only spend is the agent turn
around it: about three model calls that add ~3k new tokens (this skill, the
command, and the printed cards) plus ~1k output tokens, on top of re-reading
whatever the chat already holds.

| Where you run it | Opus 5.5 / GPT-5.6 Sol | Composer 2.5 |
|---|---|---|
| Inside an existing chat (~50k context) | ~$0.05–0.10 | ~$0.03 |
| As the first message of a fresh chat | ~$0.25 (writing the agent's own ~40k system prompt to cache) | ~$0.05 |

More `--cards` means more output tokens: roughly +$0.01 per 3 extra cards on
frontier models.

## Boundaries

- Read-only. Cursor CLI stores are copied to a temp dir to read past SQLite
  locks, then deleted. The only file written is the full report in the system
  temp dir (or `--report PATH`).
- History is private. Never upload, publish, or paste it anywhere else without
  explicit instruction.
- Prices go stale. When a provider changes pricing, update `prices.json` and
  its `as_of` date instead of hand-adjusting printed numbers.
- Agents without a supported local store (for example SQLite-only or
  encrypted histories) are not counted. Say so if the user expects them.
