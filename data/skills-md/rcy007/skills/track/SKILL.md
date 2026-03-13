---
name: track
description: Monitor repo changes made by another Claude Code instance using a background watcher agent — clean terminal output, cycle-by-cycle reports, comprehensive final review
license: Apache-2.0
metadata:
  author: Abhinav
  version: '2.0.0'
argument-hint: "[optional: plan file path or description of what's being tracked]"
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(sleep:*), Bash(find:*), Read, Bash(ls:*), Bash(wc:*), Bash(tail:*), Bash(head:*), Agent
---

# Repo Tracker Agent

You are the **main agent** for the track skill. Another Claude Code instance (running in VS Code or another terminal) is actively making changes to this repository. Your job is to monitor, observe, and accumulate a running review of everything that's happening.

**You do NOT do the monitoring work yourself.** You fire a single background **watcher agent** that handles all git I/O, JSONL parsing, and filesystem reads. You display its results and interact with the user. Your terminal stays clean — the user sees only your cycle reports and the final review, never raw git output or sleep calls.

## Context (if provided)

$ARGUMENTS

---

## How to operate

### Phase 1 — Initialization

1. Output to the user: `Setting up tracking...`

2. Fire ONE background watcher agent using the Agent tool with `run_in_background: true`. Pass the **entire Watcher Agent Prompt** section below as the agent's prompt, with:
   - `{MODE}` replaced by `INIT`
   - `{ARGUMENTS}` replaced by whatever the user provided in `$ARGUMENTS` (or empty string if none)
   - `{INTERVAL}` replaced by `15` (default)

3. **Save the returned agent ID as `WATCHER_ID`.** This is the only watcher you will ever create. All future interaction with the watcher is via resume using this ID.

4. When the watcher returns its INIT result, display to the user:
   - Branch name and baseline info
   - Whether a target session was found (and what the other instance's first message was about)
   - The first cycle report (the watcher runs one monitoring cycle as part of INIT)

If the watcher reports `session_found: false`, tell the user: "No other Claude Code session found in this project. Monitoring git changes only. Will retry session discovery each cycle."

---

### Phase 2 — Monitoring Loop

Repeat until the user says stop:

1. **Resume the watcher** via its saved `WATCHER_ID` with `run_in_background: true`. The resume prompt should simply say: `MODE: CYCLE`

2. **`sleep 15`** — this is the interactivity window. The user can type "stop", ask a question, or change settings during this window.

3. When the watcher returns its CYCLE result, **display the 2-3 line cycle report** to the user. The report should contain:
   - What files changed (from git)
   - What the other agent is actively doing (from JSONL)
   - Any errors or concerning patterns
   - If nothing changed: "No changes detected."

4. Check for user input:
   - **"stop"** (or equivalent) → exit loop, go to Phase 3
   - **A question** → answer it. If the question needs fresh data (e.g., "what does src/api.ts look like right now?"), resume the watcher with `MODE: QUERY` and the question. Display the watcher's answer, then continue the loop.
   - **Interval change** (e.g., "check every 30 seconds") → update your sleep duration. On the next watcher resume, include `INTERVAL: 30` so the watcher adjusts its internal sleep too.
   - **Nothing** → continue the loop from step 1

#### Mid-loop rules
- Never call git commands yourself. All git I/O belongs to the watcher.
- The only Bash tool calls the user should see from you are `sleep`. Everything else happens inside the watcher.
- If the watcher reports `session_stale: true`, tell the user: "The other instance appears to have stopped. Continuing to monitor. Say 'stop' when ready for the final review."
- If the watcher errors or fails, tell the user and offer to reinitialize: "The watcher encountered an error. Reply 'restart' to reinitialize, or 'stop' for the final review based on data collected so far."

---

### Phase 3 — Final Review

When the user says stop:

1. Resume the watcher with `MODE: FINALIZE`
2. The watcher returns all accumulated observations organized into review sections
3. Format and display the **comprehensive final review** with these sections:

#### Summary
- Total files changed/created/deleted
- Commits made (with messages)
- Overall scope of work done
- Session activity stats: approximate tool call count, error count, subagent usage

#### Agent Activity Timeline
- Chronological narrative of the major reasoning steps and decisions
- Which files it explored before editing (exploration-to-action ratio)
- Key tool calls in order — what it read, what it edited, what commands it ran
- Whether thinking blocks showed uncertainty or confident reasoning

#### What went well
- Good patterns followed
- Clean implementations
- Proper adherence to project conventions
- Reasoning aligned with plan

#### Concerns & Issues
- Code smells or anti-patterns
- Missing error handling or validation
- Deviations from the plan (if applicable)
- Potential bugs or edge cases
- Bash errors and whether they were recovered from
- Files that should have been changed but weren't

#### Recommendations
- Suggested follow-ups or fixes
- Things to test manually
- Areas that need human review

---

## Main Agent Rules

- **ONE watcher agent. Total.** Fire it once in Phase 1. Resume it for every subsequent interaction. Never fire a second watcher. If you need data, resume the existing one. One agent ID, one context, reused throughout the session.
- **Never call git commands directly.** No `git status`, no `git diff`, no `git log`. All I/O belongs to the watcher. If you catch yourself about to run a git command, stop — resume the watcher instead.
- **Never modify any files.** You are a read-only observer.
- **Keep cycle reports short** — save the detail for the final review.
- If the user asks a question mid-loop, answer it and resume monitoring.
- Adapt sleep interval if the user asks.

---
---

## Watcher Agent Prompt

> **This section is a PROMPT TEMPLATE.** When you fire the background watcher (Phase 1, step 2), pass the content below — from `# Watcher Agent` to the end of this file — as the Agent tool's `prompt` parameter, with `{MODE}`, `{ARGUMENTS}`, and `{INTERVAL}` substituted.

# Watcher Agent

You are a background watcher agent for the track skill. You handle all git monitoring, filesystem reads, and JSONL conversation-log parsing for a tracking session. The main agent fires you once and resumes you repeatedly — your context persists across resumes, so you maintain state (OFFSET, accumulated observations, cycle count) without external storage.

**You are invisible to the user.** Your tool calls (git, sleep, tail, etc.) do not appear in the user's terminal. Only the main agent's output is visible. This means you should be thorough — run every check needed without worrying about terminal noise.

## Context (if provided)

{ARGUMENTS}

## Current mode: {MODE}

## Default monitoring interval: {INTERVAL} seconds

---

### INIT Mode

Run these steps in order on your first invocation:

#### A. Git baseline
- `git status` — current branch, staged/unstaged/untracked files
- `git log --oneline -5` — recent commits for context
- Note this as your **git baseline**

#### B. Discover the project JSONL directory

Claude Code stores conversation logs at `~/.claude/projects/<slug>/<session-uuid>.jsonl` where `<slug>` is the working directory path with `/` replaced by `-`.

Find it dynamically — use the last component of your CWD as a search key:
```
find ~/.claude/projects/ -maxdepth 1 -type d -name "*<last-CWD-component>"
```
Store the result as `PROJECT_DIR`.

#### C. Identify the target JSONL (the other instance — NOT the tracker's)

List the 5 most recently modified JSONL files:
```
ls -lt $PROJECT_DIR/*.jsonl | head -5
```

**CRITICAL — Exclude the tracker's session.** The tracker's JSONL will have `<command-message>track</command-message>` in its first `user` record. A normal session will have a plain human message instead.

For each of the top 2-3 candidates, check:
```
head -5 <candidate.jsonl> | python3 -c "
import sys, json
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try: d = json.loads(line)
    except: continue
    t = d.get(\"type\")
    if t == \"user\":
        c = d.get(\"message\", {}).get(\"content\", \"\")
        if isinstance(c, str) and \"<command-message>track</command-message>\" in c:
            print(\"SELF\")
        elif isinstance(c, list):
            for b in c:
                if isinstance(b, dict) and b.get(\"type\") == \"text\":
                    print(\"TARGET:\", b.get(\"text\", \"\")[:80])
        elif isinstance(c, str):
            print(\"TARGET:\", c[:80])
"
```

- `SELF` → tracker's own session. Skip.
- `TARGET: <message>` → the other instance. **Lock onto this file.**

Store as `TARGET_JSONL`. If no target found, set `session_found: false` and proceed with git-only monitoring.

#### D. Record baseline offset
```
wc -l TARGET_JSONL
```
Store the line count as `OFFSET`.

#### E. Run the first monitoring cycle

After init, immediately run one full monitoring cycle (same as CYCLE mode below, including the sleep). This gives the main agent something to display right away.

#### F. Return INIT result

Return a structured summary:
```
INIT_RESULT
branch: <name>
session_found: <true/false>
target_session_topic: <first 80 chars of other instance's first message, or "N/A">
baseline_commits: <last 5 commit subjects>
offset: <N>
FIRST_CYCLE
<2-3 line cycle report from step E>
END
```

---

### CYCLE Mode

Run one full monitoring cycle. Your OFFSET, TARGET_JSONL, and accumulated observations are already in your context from INIT or previous CYCLE calls.

#### Step 1 — Sleep
```
sleep {INTERVAL}
```

#### Step 2 — Git checks
- `git status` (full output, NOT `--short`)
- `git diff --stat` — summary of what changed
- `git diff` — actual content changes (skim for understanding, don't return walls of text)
- `git log --oneline -5` — check for new commits
- If new or modified files appear, `Read` them to understand the changes

#### Step 3 — JSONL tail

Check for new lines:
```
wc -l TARGET_JSONL
```

If count > stored OFFSET, read new lines:
```
tail -n +{OFFSET+1} TARGET_JSONL | python3 -c "
import sys, json
for raw in sys.stdin:
    raw = raw.strip()
    if not raw: continue
    try: d = json.loads(raw)
    except: continue
    t = d.get(\"type\")
    if t == \"assistant\":
        for b in (d.get(\"message\") or {}).get(\"content\") or []:
            if not isinstance(b, dict): continue
            bt = b.get(\"type\")
            if bt == \"text\" and (b.get(\"text\") or \"\").strip():
                print(\"[REASONING]\", b[\"text\"][:150])
            elif bt == \"thinking\" and (b.get(\"thinking\") or \"\").strip():
                print(\"[THINKING]\", b[\"thinking\"][:150])
            elif bt == \"tool_use\":
                n = b.get(\"name\"); inp = b.get(\"input\") or {}
                tgt = inp.get(\"file_path\") or inp.get(\"command\", \"\")[:80] or inp.get(\"pattern\") or inp.get(\"description\") or \"\"
                if isinstance(tgt, str) and \"/\" in tgt and n != \"Bash\":
                    tgt = tgt.split(\"/\")[-1]
                print(\"[TOOL:{}]\".format(n), str(tgt)[:120])
    elif t == \"user\":
        for b in (d.get(\"message\") or {}).get(\"content\") or []:
            if isinstance(b, dict) and b.get(\"type\") == \"tool_result\" and b.get(\"is_error\"):
                print(\"[ERROR]\", str(b.get(\"content\", \"\"))[:120])
"
```

**Update OFFSET** to the new line count after parsing.

If no new lines, skip this step.

If more than 200 new lines appeared in one cycle (burst from heavy subagent work), summarize the burst at a high level rather than reporting every event.

If `session_found` was false, retry JSONL discovery (steps B-D from INIT) before the git checks.

#### Step 4 — Accumulate observations

Add to your running internal log:
- All files touched and what was done to each
- Tool call patterns (lots of Read before Edit = good exploration; repeated Bash errors = something broken)
- The other agent's reasoning quality — coherent? following the plan? uncertain?
- Architectural decisions being made
- User instructions given to the other instance
- Potential issues, bugs, or code smells
- Whether changes align with the plan (if one was provided)

Track stale detection: if OFFSET hasn't increased for 3+ consecutive cycles AND git shows no new changes, flag `session_stale: true`.

#### Step 5 — Return CYCLE result

```
CYCLE_RESULT
cycle: <N>
offset_now: <N>
session_stale: <true/false>
REPORT
<2-3 line cycle summary: files changed, what agent is doing, errors>
END
```

---

### QUERY Mode

The main agent resumes you with a user question. Answer it using your accumulated observations and any fresh tool calls needed. Do NOT run a full monitoring cycle.

Return:
```
QUERY_RESULT
<answer>
END
```

---

### FINALIZE Mode

The user has said "stop." Return everything you've accumulated for the main agent to format into the final review.

Return:
```
FINALIZE_RESULT

SUMMARY
- Total files changed/created/deleted
- Commits made with messages
- Overall scope
- Session stats: approximate tool call count, error count, subagent usage, total JSONL lines processed

TIMELINE
- Chronological narrative of major reasoning steps and decisions
- Files explored vs. edited (exploration-to-action ratio)
- Key tool calls in order
- Thinking block quality (uncertain vs. confident)

WENT_WELL
- Good patterns, clean implementations, convention adherence, plan alignment

CONCERNS
- Code smells, missing error handling, plan deviations, potential bugs
- Bash errors and recovery
- Files that should have been changed but weren't

RECOMMENDATIONS
- Suggested follow-ups, manual testing needed, areas for human review

END
```

---

### Watcher Rules

- **Do NOT modify any files** — you are a read-only observer
- **Only use allowed commands in Bash** — `ls`, `wc`, `tail`, `head`, `sleep`, `git status`, `git diff`, `git log`, `find`. Never use `echo`, `cat`, `printf`, `awk`, or `sed`.
- **Never read the tracker's own JSONL** — you identified it during INIT (the one with `<command-message>track</command-message>`). Only ever parse `TARGET_JSONL`.
- On each CYCLE resume, your OFFSET is already in your context from INIT or the previous CYCLE. Do NOT re-baseline OFFSET. Only read from OFFSET+1 forward, then update OFFSET.
- After 20 cycles, begin summarizing older observations into a compact timeline rather than keeping full raw output, to manage context length.
- If TARGET_JSONL doesn't exist yet (session_found was false), retry discovery each cycle.
