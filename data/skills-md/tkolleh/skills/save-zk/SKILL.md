---
name: save-zk
description: >
  Only when the user explicitly invokes `save-zk` or `/save-zk`. Do not use for
  generic save, summarize, commit, worktree teardown, daily-briefing, or notebook
  search. Distills this session into one Session Note (create or Living-Head update)
  and appends a best-effort back-link on today's Daily Note.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  tools: "zk, gh"
---

# save-zk

Run **only** on explicit invoke: `save-zk` or `/save-zk`. No other phrases.

Phases **A → I** in order. Never skip or reorder. After Phase A, write immediately (no second confirm). Dry-run only if the user asked.

Load references on demand: `references/note-template.md`, `references/living-head.md`, `references/session-context.md`.

---

## Phase A — Note Key gate

1. Suggest candidates from branch name, open PR/issue, or session materials when present.
2. Human **supplies or confirms** the Note Key (tracker id) or a ≤8-word slug.
3. Never invent or silently pick a key. **Stop until confirmed.**

**Done when:** confirmed Note Key/slug in hand.

---

## Phase B — Gather Session Context

This session only. Fan out reads in parallel when independent.

| In | Out |
|----|-----|
| Session memories, touched markdown/allium, new/updated diagram fences or charts | Whole-repo docs crawl |
| Decisions stated in-session | Secrets, tokens, credentials |
| Branch / PR / issue metadata when available | Unrelated history |

Mark each source **present** or **unavailable**. Details: `references/session-context.md`.

**Done when:** every candidate source is present or marked unavailable.

---

## Phase C — Note Lookup

Prefer **tag** match on the issue key; filename match is fallback.

| Hits | Action |
|------|--------|
| 0 | **Create** |
| 1 | **Update** that note |
| >1 | **Update most recently modified** match — do not ask; do not merge files |

Issue-key Note Keys **must** be (or become) frontmatter tags.

**Done when:** create vs update decided and target path known (or create path planned).

---

## Phase D — Daily Note resolve

```bash
zk daily
```

Record Daily Note path, or mark **unavailable** (do not invent a path).

**Done when:** path known or explicitly unavailable.

---

## Phase E — Distill

Compose per `references/note-template.md` + `references/living-head.md`.

- **Create:** full Living Head + top-level Deep Context `<details>`. **No** Update section.
- **Update:** replacement Living Head + one new `## Update: YYYY-MM-DD` delta only. Do not rewrite prior Updates or frozen create-time Deep Context.
- **Concision:** shortest form that still carries meaning. No Task Matrix section.

**Done when:** markdown body ready to write.

---

## Phase F — Visual Section

Include in Living Head only when multi-component structure/flow or numeric metrics apply:

1. Reuse `d2` / `mermaid` fences already in Session Context.
2. Else draft a **minimal** fence or metric **table** in-note.
3. Omit or clear when N/A.

No asset files, no base64, no hard dependency on diagram/visualize CLIs.

**Done when:** Visual present, cleared, or omitted with reason N/A.

---

## Phase G — Related Links

Best-effort real `[[wikilinks]]` from notebook search + link to today's Daily Note. Never invent titles. Omit non-daily related links if none.

**Done when:** links list final (may be Daily-only).

---

## Phase H — Write

1. **Session Note (primary)**
   - **Create:** prefer `zk new` into the single Session Note Location (key-agnostic; parameterize with Note Key). On `zk new` failure, write markdown under the notebook projects path and report fallback.
   - **Update:** replace **only** the Living Head; append the new Update at the bottom.
2. **Daily Note (best-effort):** append one back-link line that the Session Note was created or updated. On Daily failure: **keep** Session Note, **warn**. On Session Note failure: **skip** Daily.

**Done when:** Session Note write attempted; Daily attempted if Session succeeded.

---

## Phase I — Report

Paths written + BLUF + any Daily warning. If user asked dry-run, show composed markdown and paths only — no writes.

**Done when:** human sees report.

---

## Safety contract

1. May replace **only** the Living Head.
2. Must not alter, delete, or reorder prior Updates or frozen create-time Deep Context.
3. Must not delete Session Note, Daily Note, or session sources.
4. If unsure content already exists → append or mark `<!-- possibly duplicate — review -->`.
5. No worktree removal, git cleanup, tracker transitions, or other notebook edits.
