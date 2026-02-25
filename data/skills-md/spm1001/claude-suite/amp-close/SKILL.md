---
name: amp-close
description: Amp end-of-session ritual. Invoke FIRST when session is ending — 4-phase GODAR loop (gather context, orient via reflection, decide now-vs-next, act with handoff and garde extraction) that prevents silent work-dropping, writes cross-harness handoffs CC can discover, and persists searchable memory. MANDATORY before closing any substantial Amp thread. Triggers on 'wrap up', 'let's finish', 'close out', 'end of session'. (user)
---

# amp-close

Capture learnings while context is rich, then persist to memory and exit.

Amp equivalent of the CC `/close` skill. Adapted for Amp's tool names, thread model, and lack of lifecycle hooks — the skill IS the lifecycle event.

## When to Use

- Session ending naturally (work complete)
- Context window nearly full
- User says "wrap up", "let's finish", "one more thing then done"
- Before using the `handoff` tool (close first, then handoff if continuing)

## When NOT to Use

- Mid-session checkpoint (just summarise and continue)
- Quick question that doesn't need closure
- Exploratory work with no conclusions yet

## Structure

```
Gather  → git, bon, drift
Orient  → Agent observes → User reflects → Agent answers
Decide  → crystallise Now vs Next (STOP before executing)
Act     → execute, write handoff, write extraction, index in garde
```

---

## Gather

### Thread ID

Extract from your system prompt. Look for the `Amp Thread URL` line:

```
Amp Thread URL: https://ampcode.com/threads/T-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

The thread ID is the `T-...` portion. Use this for the garde source ID (`amp:T-...`).

### Context

Gather by running commands via Bash:

```bash
# Git status (if in a repo)
git status --porcelain 2>/dev/null
git rev-list --count @{u}..HEAD 2>/dev/null || echo "0"

# Bon status (if .bon/ exists)
[ -d .bon ] && cat .bon/items.jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    item = json.loads(line)
    if item.get('status') in ('open', 'waiting'):
        print(f\"{item['status']}: {item.get('title', '?')}\")
" 2>/dev/null
```

### Drift

Compare what the session set out to do (first user message or handoff context) with what actually happened. Note divergences.

---

## Orient

Three beats. All three must complete before Decide.

### Beat 1: Agent shares observations

Share directly — don't compress into multiple-choice:

> "Before we wrap up, here's what stood out to me this session:
> - [specific observation about the work]
> - [pattern or connection noticed]
> - [something that felt unfinished or risky]
>
> What resonates? What am I missing?"

### Beat 2: The Six Questions — via Oracle

**This is the most important part of the close ritual.** Not a checklist — a genuine interrogation.

In Claude Code, the six questions go through AskUserQuestion — a mandatory pause that forces engagement. Amp has no such gate. Instead, we use **Oracle** (GPT-5.2 reasoning model) to break the self-reflection loop. Without Oracle, the same model that missed something answers "what did you miss?" — a closed loop. Oracle provides genuine cognitive diversity: different model, different priors, different blind spots.

**The six questions** (Oracle will address all of them):

**Looking Back:**
1. **What did we forget?** — Code we read but didn't update. Docs that are now stale. Tests we said we'd write. Files we touched that have downstream effects we didn't trace.
2. **What did we miss?** — Edge cases in the code we wrote. Assumptions we didn't verify. Things that work in tests but might not work in production. Platform-specific behaviour we reasoned about but didn't test.
3. **What could we have done better?** — Approaches that would have been simpler. Abstractions that are in the wrong place. Work we did twice because we didn't plan. Patterns from the codebase we ignored.

**Looking Ahead:**
4. **What could go wrong?** — Race conditions. State that doesn't survive restarts. Dependencies on things outside our control. Silent failures. Things that work now but will break when X changes.
5. **What won't make sense later?** — Why we made a particular choice. Implicit knowledge that isn't written down. Code that looks wrong but is correct for a non-obvious reason. Relationships between files that aren't documented.
6. **What will we wish we'd done?** — Tests we should have written. Manual verification we should have done. Documentation we should have updated. Conversations we should have had with the user.

#### Substantive sessions: dispatch to Oracle

**Gate:** Only invoke Oracle when the session had substance — multiple file changes, architectural decisions, non-trivial work. For trivial sessions (typo fix, config tweak), answer the six questions yourself and move to beat 3.

**Prepare the Oracle prompt.** Like dispatching a Titan reviewer, quality depends on the brief. The prompt must reference *specific* session artifacts — not generic reflection prompts.

```
oracle(
  task: "Session reflection — six questions",
  context: "{see template below}",
  files: ["{key files touched this session}"]
)
```

**Oracle context template** — adapt to the actual session:

```
You are reviewing a coding session that is about to close. Your job is to
find what the working agent (Claude on Amp) may have missed, normalised,
or left fragile. Be specific and reference concrete files and decisions.

SESSION SUMMARY:
- Started with: {initial goal from first user message or handoff}
- Key decisions: {list architectural choices, trade-offs made}
- Files changed: {list with one-line description of each change}
- What felt uncertain: {anything the agent wasn't confident about}
- What drifted: {divergences from original plan}

Answer these six questions with substance. Not bullet points — actual
analysis. If you find yourself writing "Nothing" or "N/A", look harder.
Every session has friction, gaps, and things that could go wrong.

LOOKING BACK:
1. What did we forget? (dropped intentions, stale docs, untested paths)
2. What did we miss? (edge cases, unverified assumptions, platform gaps)
3. What could we have done better? (simpler approaches, ignored patterns)

LOOKING AHEAD:
4. What could go wrong? (race conditions, silent failures, fragile deps)
5. What won't make sense later? (implicit knowledge, non-obvious choices)
6. What will we wish we'd done? (missing tests, skipped verification)
```

**Include files** — pass the key files touched this session via the `files` parameter. Oracle can read them and ground its analysis in actual code, not just your summary. This is what makes the difference between generic advice and genuine second opinion.

#### Report Oracle's findings — don't debate them

**You are a reporter here, not a defendant.** You wrote the code Oracle is critiquing. Your instinct will be to argue — resist it. Oracle's job is to find what you normalised; your job is to relay its findings to the user honestly.

Present Oracle's findings directly, adding context only where it helps the user decide — never to dismiss:

> **Oracle found:**
> - [finding 1 — with file/decision reference]
> - [finding 2]
> - [finding 3]
>
> **Context that might matter:** [facts Oracle didn't have — e.g., "we considered X but ruled it out because Y"]
>
> **What should we act on?**

**The user is the circuit breaker.** Oracle provides the signal; the user converts it to action. Don't filter, don't rank, don't argue. If Oracle flagged it, the user sees it.

#### Trivial sessions: self-reflect

If the session was trivial (single small change, no decisions), skip Oracle. Answer the six questions yourself — briefly. The gate exists to prevent wasting an LLM call on sessions where self-reflection is adequate.

### Beat 3: User reflects

Present the synthesised view (agent observations + Oracle findings). Ask the user what resonates and what's missing. **Wait for their response before proceeding to Decide.** This is the natural pause point — Oracle provided the external signal, now the user closes the loop.

---

## Decide

**STOP.** Do not proceed to Act without user approval.

From Gather + Orient, crystallise actions into two buckets:

### Now vs Next

**Now** = actions that execute immediately, benefiting from current context:
- Incomplete work that can be finished quickly
- Close a bon item with resolution notes
- Quick fixes (< 2 minutes)

**Next** = deferrals that create work for a future session:
- Incomplete work that needs dedicated time
- Create a bon item (by definition, deferring)
- Anything needing fresh thinking

Present both lists to the user. Every piece of incomplete work from the session must appear in one bucket — nothing silently drops.

---

## Act

Execute in this order:

### 1. Execute "Now" items

Do the selected immediate actions.

### 2. Create "Next" items

For each selected deferral, create a bon item:

```bash
bon new "title" --why "..." --what "..." --done "..."
```

### 3. Write handoff for cross-harness continuity

**This is what makes the next CC session aware of Amp's work.** Without it, CC finds the last *CC* handoff — potentially hours or days stale.

Write a handoff file to the same location CC uses:

```bash
# Compute handoff path (same encoding as CC)
ENCODED_PATH=$(pwd -P | sed 's/[^a-zA-Z0-9-]/-/g')
HANDOFF_DIR="$HOME/.claude/handoffs/$ENCODED_PATH"
mkdir -p "$HANDOFF_DIR"

# Filename: amp- prefix + first 8 hex chars of thread ID
# Thread ID: T-019c610d-5d24-7019-b282-6756505b8f66
#                ^^^^^^^^ these 8
FILENAME="amp-${THREAD_ID:2:8}.md"
```

**Handoff template** — same contract as CC, with Amp-specific metadata:

```markdown
# Handoff — {DATE}

session_id: amp:{THREAD_ID}
purpose: {first Done bullet, truncated to ~60 chars}
source: amp
thread_url: https://ampcode.com/threads/{THREAD_ID}

## Done
- [Completions in verb form — include item IDs if closing]

## Gotchas
[What would trip up next Claude]

## Risks
[What could go wrong with what we built]

## Next
[Direction for next session]

## Reflection
**Agent observed:** [Key observations from Orient]
**User noted:** [What they added or emphasized]
```

**Write using a single Bash call:**

```bash
cat > "$HANDOFF_DIR/$FILENAME" << 'HANDOFF'
{the generated handoff markdown}
HANDOFF
```

**Why this matters:** CC's `open-context.sh` discovers handoffs via `ls -t ~/.claude/handoffs/<encoded-path>/*.md`. Same directory, same `.md` extension, same section headings = zero changes to the reader. The `source: amp` and `thread_url:` fields are bonus metadata — CC can mention "last session was Amp" and link back for resumption.

**CWD validation:** Before writing, sanity-check that `pwd` matches the project you actually worked on. If the Amp session spanned multiple repos, write the handoff for the primary one (ask the user if ambiguous).

### 4. Write extraction and index in garde

This is the Remember phase — done inline because Amp has no session-end hook. The handoff (step 3) gives continuity; the extraction gives searchable memory. Both are valuable, don't merge them.

**Generate extraction JSON** matching garde's schema:

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

**Guidelines for extraction:**
- `summary` captures the "so what" — why this session mattered
- `builds` = concrete artifacts: code, config, docs, skills modified
- `learnings` = insights that transfer to other contexts
- `friction` = things harder than expected
- `patterns` = meta-observations about how we worked
- `open_threads` = deferred work, not abandoned

**Write and index:**

Write the extraction JSON to `/tmp/amp-extraction.json` using a Bash heredoc, then send it:

```bash
# Step 1: Write extraction to temp file
cat > /tmp/amp-extraction.json << 'EXTRACTION'
{the generated JSON}
EXTRACTION
```

```bash
# Step 2: Send to garde (scan + store + cleanup in one call)
~/.claude/scripts/send-amp-extraction.sh "{THREAD_ID}" < /tmp/amp-extraction.json \
    && rm /tmp/amp-extraction.json
```

**If garde-manger is not installed** (`~/Repos/garde-manger` doesn't exist): the script degrades gracefully — warns and exits 0. The session still gets value from Orient, triage, and the handoff file.

### 5. Commit (if applicable)

If git dirty in the working directory:
- Stage relevant files
- Commit with standard message
- Push if user approves

Only commit the working directory — never "helpfully" tidy other repos.

### 6. Tell user session is complete

Say: "All done — safe to close this thread."

---

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Skip Orient reflection | Loses the highest-value part | Complete all three beats |
| Silently drop incomplete work | Work disappears | Surface in Decide — finish, defer, or explicit drop |
| Skip handoff, only write extraction | Next CC session finds stale CC handoff | Always write handoff file (step 3) — it's the cross-harness bridge |
| Rush to extraction | Shallow summary | Reflect first, extract from reflection |
| Commit other repos | Unwanted tidying | Only commit working directory |
| Use `handoff` instead of closing | Context pipes forward but nothing persists to memory | Close first, handoff second if needed |
| Forget `garde scan` before `store-extraction` | Thread not yet indexed, extraction orphaned | Always scan first |
| Chain Bash commands with `cd &&` | Amp doesn't persist cwd between calls | Use `cwd` parameter on each Bash call |
| Use `--quiet` on `garde scan` | Flag doesn't exist | Omit it; output is brief anyway |
| Treat "Next" items as notes | They'll be forgotten | File as bon items with --why/--what/--done |
| Generic Oracle prompt | "Did we miss anything?" gets generic answers | Reference specific files, decisions, and uncertainties in the context |
| Oracle on trivial sessions | Wasted call, superficial findings | Gate: only invoke for multi-file changes or architectural decisions |
| Argue with Oracle findings | Agent defends its own work, user never sees the critique | Report findings directly — agent is reporter, user is circuit breaker |
| Write handoff before garde extraction | Garde step could touch the file, messing up mtime | Write handoff last among persist steps (step 3 before 4 is fine — garde writes elsewhere) |

## Integration

**Depends on:**
- `oracle` tool (Amp built-in — GPT-5.2 reasoning model, used in Orient phase)
- `garde` CLI (`uv run garde` from `~/Repos/garde-manger`) — optional, degrades gracefully
- `bon` CLI (if `.bon/` exists in working directory)

**Complements:**
- Amp's `handoff` tool — close captures memory, handoff continues work
- `garde` skill — searching past sessions that amp-close indexed
- CC `close` skill — same ritual, different platform

## GODAR Reference

| Phase | CC /close | amp-close |
|-------|-----------|-----------|
| **G**ather | `close-context.sh` script | Bash commands inline |
| **O**rient | Claude observes → AskUserQuestion → Claude answers | Agent observes → Oracle second opinion → synthesise both → user reflects |
| **D**ecide | AskUserQuestion multi-select | Plain text Now/Next lists |
| **A**ct | Execute, handoff file, `.pending-extractions/`, commit | Execute, handoff file, garde extraction inline, commit |
| **R**emember | Session-end hook → `garde process` | Done in Act (no hook available) |
