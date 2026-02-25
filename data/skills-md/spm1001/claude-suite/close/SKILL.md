---
name: close
description: Orchestrates end-of-session capture via 5-phase GODAR framework — prevents work loss between sessions by surfacing learnings, triaging incomplete work into Now/Bon/Handoff, writing cross-session handoff, and staging memory extraction while context is rich. MANDATORY before /exit. Invoke FIRST on 'wrap up', 'lets finish', 'close out', '/close'. Pairs with /open. (user)
---

# /close

Capture learnings while context is rich, then commit and exit.

## When to Use

- Session ending naturally (work complete)
- Context window nearly full
- User says "wrap up", "let's finish", "one more thing then done"
- Main task complete and about to summarize

## When NOT to Use

- Mid-session checkpoint (pause and check direction instead)
- Quick question that doesn't need handoff
- Exploratory work with no conclusions yet

## Structure

```
Prerequisites → Verify infrastructure
Pre-flight    → Return to home directory
Gather        → todos, tracker (bon), git, drift, SESSION_ID
Orient        → Claude answers six questions in prose → user responds
Decide        → Claude proposes Now/Next plan → user amends (STOP)
Act           → execute, write handoff, stage extraction, commit
Remember      → index session (background, automatic)
```

---

## Prerequisites

**Before running /close, verify infrastructure is healthy.** Broken scripts mean lost handoffs.

| Check | How | If Broken |
|-------|-----|-----------|
| close-context.sh exists | `[ -x ~/.claude/scripts/close-context.sh ]` | Run `claude-doctor.sh` |
| check-home.sh exists | `[ -x ~/.claude/scripts/check-home.sh ]` | Fix symlinks |
| Handoffs dir writable | `[ -d ~/.claude/handoffs ]` | Create: `mkdir -p ~/.claude/handoffs` |

**Quick pre-flight:**
```bash
[ -x ~/.claude/scripts/close-context.sh ] && [ -x ~/.claude/scripts/check-home.sh ] && echo "OK" || echo "BROKEN"
```

If broken: **STOP, diagnose, then write handoff manually** rather than skipping closure entirely. See `~/Repos/trousse/references/ERROR_PATTERNS.md`.

---

## Pre-flight: Return Home (MANDATORY)

You may have `cd`'d during work. Your system prompt contains `Working directory: /path/...` in the `<env>` block — this is immutable, where the session actually started.

1. Extract that exact path from your system prompt
2. Run: `~/.claude/scripts/check-home.sh "/that/path"`
3. If `CD_REQUIRED=true`, run `cd <HOME_DIR>` immediately

**Do not skip. Do not trust pwd. Do not reason about whether you moved back. The script is authoritative.**

---

## Gather

```bash
~/.claude/scripts/close-context.sh
```

Script outputs: TIME, GIT, BON, LOCATION context, HANDOFF_DIR, SESSION_ID.

Use TIME_OF_DAY for greetings. Use YEAR to anchor the handoff date. **Hold onto HANDOFF_DIR and SESSION_ID — you'll need both in Act.**

### Script Failure Handling

**If the script fails (exit code 127 = file not found, or any error):**

1. **STOP.** Tell the user: "close-context.sh failed. Likely a broken symlink."
2. **Diagnose:** Run `~/.claude/scripts/check-symlinks.sh`
3. **Fallback:** If you can't fix it, write handoff manually to `~/.claude/handoffs/<encoded-path>/` — don't skip closure entirely.

**Why this matters:** Broken scripts (Jan 3-10 2026) meant /close ran without proper context gathering. Never continue silently.

From script output, assess:

- **Work progress** — what's done, what's incomplete?
- **Tracker** — Bon: open items to complete or defer
- **Git** — uncommitted files? unpushed commits?
- **Drift** — what did /open say we'd do vs what we actually did?

Surface stale artifacts: screenshots, temp files, old sketches, superseded plans.

---

## Orient

**This is THE reflection.** What emerges here feeds the handoff and the extraction. There is no second pass later.

Answer all six questions in prose — don't compress into bullets, don't pre-bake options. The point is surfacing what you noticed that the user might not have.

**Looking Back:**
1. **What did we forget?** — Dropped intentions, docs now stale, tests we said we'd write, files touched with untraced downstream effects
2. **What did we miss?** — Edge cases, unverified assumptions, things that work in test but may not in production
3. **What could we have done better?** — Simpler approaches, abstractions in the wrong place, patterns from the codebase we ignored

**Looking Ahead:**
4. **What could go wrong?** — Race conditions, silent failures, fragile dependencies, things that work now but break when X changes
5. **What won't make sense later?** — Why we made a particular choice, implicit knowledge not written down, non-obvious relationships between files
6. **What will we wish we'd done?** — Tests, verification, documentation, conversations we should have had

Share these directly, then ask: **"What resonates? What am I missing?"**

Wait for the user's response. Their additions and corrections go into the handoff Reflection section verbatim.

---

## Decide

**STOP.** Do not execute anything until this phase completes.

From Gather + Orient, identify all incomplete work and draft a concrete plan. **Present it — don't ask the user what they want.** Propose; let them amend.

### Bucket everything

**Now** — executes before /exit, benefits from current context:
- Incomplete work finishable in under 2 minutes
- Close a tracker item with resolution notes
- Update CLAUDE.md (local or global) when a clear pattern emerged
- Quick fixes where the how is obvious

**Bon** — each becomes a tracked item for a future session. Before filing any bon, answer: *"If this never gets done, what breaks?"* If the answer is "not much", it belongs in the handoff Next section, not a bon. This is the gate.

**Handoff only** — direction, context, and risks that don't rise to bon level.

### Present the plan

> "Here's my plan:
>
> **Now:** [concrete list — things I'll do before /exit]
>
> **Bons to file:** [each with one line on what breaks if skipped]
>
> **Handoff only:** [things worth noting but not tracking]
>
> Tell me if anything should move."

Wait for approval. Nothing executes until the user confirms or amends.

---

## Act

Execute in this order.

### Execute "Now" items

Do the approved immediate actions: finish incomplete todos, close tracker items with notes, update CLAUDE.md, quick fixes.

### File bons

For each approved item:

```bash
bon new "title" --why "consequence if not done" --what "concrete actions" --done "definition of done"
```

**`--why` quality gate:** must state the consequence of skipping, not describe the work. "Prevents next Claude rediscovering the problem from scratch" is a consequence. "Because we need to do this" is not.

### Write handoff

**Handoff location is non-negotiable.** The script computes the path; you use it exactly.

```bash
~/.claude/scripts/close-context.sh | grep -E 'HANDOFF_DIR|SESSION_ID'
```

This outputs both — use them directly, never recompute.

| Rule | Why |
|------|-----|
| Write to `{HANDOFF_DIR}/{session-id}.md` | Central location, /open finds it |
| Never write locally (`.handoff.md` in project) | /open won't find it — information becomes invisible |
| Never compute path yourself | Encoding differences cause folder fragmentation |

**Why this matters (Jan 2026 incident):** A Claude wrote to `.handoff-kube-migration.md` locally. The next session's /open loaded a stale handoff instead — the work existed but was invisible to the protocol.

**Fallback:** If SESSION_ID is empty (script failed), use timestamp: `2026-01-04-2215.md`

Filename: first 8 chars of SESSION_ID + `.md`
Example: `SESSION_ID=51d17dc5-b714-481c-9dfb-6d4128800e7b` → `51d17dc5.md`

Handoff template:

```
# Handoff — {DATE}

session_id: {SESSION_ID}
purpose: {first Done bullet, truncated to ~60 chars}

## Done
- [Completions in verb form — include item ID if closing one]
  e.g., "Fixed auth bug (claude-go-xyz)" or "Completed migration (bon-gutowa)"

## Gotchas
[What would trip up next Claude — specific, not generic]

## Risks
[What could go wrong with what we built]

## Next
[Direction for next session]

## Artifacts
[Only if Google Drive work — see Knowledge Work section]

## Commands
  # Optional — verification or continuation commands

## Reflection
**Claude observed:** [Key observations from Orient]
**User noted:** [What they added or emphasized]
```

#### Knowledge Work Context (Google Drive)

**When working in Google Drive (not ~/Repos):** Add an Artifacts section.

You already know what you touched — you called MCP tools during the session. Recall which docs you read (`get_content`), updated (`update_doc`, `append_to_doc`), or browsed (`list_files`).

```
## Artifacts
Working folder: [Project Name](https://drive.google.com/drive/folders/xxx)

This session:
- Updated: [Contract Stewardship Doc](https://docs.google.com/.../d/yyy) — added supplier descriptions
- Created: [Q1 Review Notes](https://docs.google.com/.../d/zzz)
- Referenced: [Budget Template](https://docs.google.com/.../d/www) — read-only
```

Knowledge work doesn't have commits. This is the equivalent. Next Claude can `get_content()` on these links to pull current state — links are stable, content is always fresh.

### Stage extraction for memory

**After writing the handoff, generate a session extraction from your live context.** This replaces the expensive `claude -p` subprocess the session-end hook would otherwise spawn.

**Write the extraction JSON** using the Write tool to `/tmp/garde-extraction.json`:

```json
{
    "summary": "2-3 sentences — what happened and why it matters",
    "arc": {
        "started_with": "initial goal/problem",
        "key_turns": ["pivots, discoveries, changes in direction"],
        "ended_at": "final state"
    },
    "builds": [{"what": "thing created/modified", "details": "context"}],
    "learnings": [{"insight": "what was learned", "why_it_matters": "significance", "context": "how discovered"}],
    "friction": [{"problem": "what was hard", "resolution": "how resolved or 'unresolved'"}],
    "patterns": ["recurring themes, collaboration style, meta-observations"],
    "open_threads": ["unfinished business, deferred work"]
}
```

Guidelines:
- `summary` = the "so what" — why this session mattered, not what was done
- `builds` = concrete artifacts: code, config, docs, skills
- `learnings` = insights that transfer to other contexts (not just "I learned X exists")
- `friction` = things harder than expected and how they resolved
- `open_threads` = deferred, not abandoned

**Then stage it:**

```bash
~/.claude/scripts/stage-extraction.sh < /tmp/garde-extraction.json \
    && rm /tmp/garde-extraction.json
```

The script computes the correct UUID filename and places it where the hook expects. If the script is missing (fresh install before `install.sh` runs), the hook falls back to `garde process` — safe to continue.

### Commit

If git dirty in the working directory:
- Stage relevant files (handoff too if the repo is the project)
- Commit with standard message + co-authorship
- Push if user approves

**Only commit the working directory.** Other repos' dirty state is not your concern.

### Tell user to exit

Say: "Type `/exit` to close." Don't exit programmatically.

---

## Remember

**Automatic — handled by session-end hook.** You don't invoke this.

The hook (`~/.claude/hooks/session-end.sh`) takes one of two paths when the user runs `/exit`:

1. **Staged extraction exists** (the file you wrote above):
   - `garde index` on the session (fast, no LLM)
   - `garde store-extraction` with your pre-generated JSON
   - Staging file removed
   - No subprocess spawned

2. **No staged extraction** (crash, ctrl-c, no /close):
   - Falls back to `garde process` — spawns `claude -p` to extract from the raw transcript
   - Same quality, slower, costs a subprocess

Either way, handoffs are scanned afterward. Just tell the user to `/exit`.

---

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Compress Orient into bullets or options | Misses unexpected observations | Answer six questions in prose |
| Ask "what do you want?" in Decide | Puts burden on user, invites deferral | Propose a concrete plan; user amends |
| File bons with weak `--why` | Future Claude can't prioritise | State the consequence of skipping |
| Skip pre-flight cd check | Handoff written to wrong project | Always run check-home.sh |
| Write handoff locally (.handoff.md) | /open won't find it | Use HANDOFF_DIR from script |
| Silently drop incomplete work | Work disappears | Every piece in Now, bon, or handoff Next |
| Commit other repos | Unwanted "helpful" tidying | Only commit working directory |
| Recompute SESSION_ID or HANDOFF_DIR | Encoding drift, folder fragmentation | Read from close-context.sh output |

---

## GODAR Reference

| Phase | /open | /close |
|-------|-------|--------|
| **G**ather | Handoff, tracker, script | Tracker, git, drift; HANDOFF_DIR + SESSION_ID |
| **O**rient | "Where we left off" | Six questions in prose → user responds |
| **D**ecide | User picks direction | Claude proposes Now/Bon/Handoff plan → user amends |
| **A**ct | Draw-down from Bon | Execute, write handoff, stage extraction, commit |
| **R**emember | — | Index session (background, automatic on /exit) |
