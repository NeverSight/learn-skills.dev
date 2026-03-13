---
name: dev-debug
version: 4.0
description: "This skill should be used when the user asks to 'debug', 'fix bug', 'investigate error', 'why is it broken', 'trace root cause', 'find the bug', or needs systematic debugging with fresh-context subagent iterations and progress-gated escalation."
---

**Announce:** "I'm using dev-debug for systematic debugging."

**Load shared enforcement:**
```
Read("../../lib/references/dev-common-constraints.md")
```

<EXTREMELY-IMPORTANT>
## STEP ZERO — INITIALIZE THE DEBUG LOOP

Your first actions are, in order:
1. Create/update HYPOTHESES.md (the durable memory across iterations)
2. Spawn the first investigation subagent

**Do NOT read project code. Do NOT form hypotheses. Do NOT "gather context." All investigation happens inside subagents with fresh context.**

### The Cognitive Lock

Until you spawn the first subagent, you cannot: Read files, Edit code, Run commands, Grep for patterns, "Just quickly check" anything, Form hypotheses, or Analyze prior context. **All tools LOCKED until first subagent is spawned.**

### Why This Exists

On March 6-7, 2026, an agent loaded dev-debug TWICE and both times rationalized skipping the loop. Result: 19MB transcript, 15K lines, 30 "root cause found" claims, 6+ theories, zero resolution. The session was killed.
</EXTREMELY-IMPORTANT>

## Architecture: Fresh Subagent Loop With Progress Gating

**No ralph-loop. No promises. No honor system.** The main chat runs its own loop. Each iteration is a fresh subagent. The loop runs autonomously as long as subagents make meaningful progress. The user is only pulled in when the loop stalls.

```
Main chat (thin orchestrator)
  │
  ├─ Initialize HYPOTHESES.md
  │
  ├─ LOOP:
  │   ├─ Spawn fresh subagent → investigate/fix
  │   ├─ Subagent returns structured report
  │   ├─ Evaluate progress (see stall detection below)
  │   │
  │   ├─ MEANINGFUL PROGRESS?
  │   │   YES → iterate automatically (spawn next subagent)
  │   │   NO  → escalate to user
  │   │
  │   └─ SUBAGENT CLAIMS FIXED?
  │       → Run the test command yourself
  │       → Pass? → DONE
  │       → Fail? → log false positive, iterate
  │
  └─ Max 10 iterations without resolution → escalate to user
```

### Why This Design

- **Fresh subagent per iteration**: No context pollution. Each subagent reads state from HYPOTHESES.md, not from 15K lines of prior conversation.
- **No ralph-loop dependency**: The exit condition is progress, not a promise the agent can fake.
- **User only involved when needed**: Autonomous when making progress, escalates when stuck.
- **Test as structural gate**: When the subagent claims FIXED, main chat runs the test. The agent can't lie about test output.

**Progress lives in files, not in conversation.**

<EXTREMELY-IMPORTANT>
## The Iron Law of Delegation

**MAIN CHAT MUST NOT TOUCH THE CODEBASE. EVER.**

Main chat does exactly four things:
1. Initialize HYPOTHESES.md
2. Spawn fresh subagents
3. Evaluate progress between iterations
4. Run the regression test when a subagent claims FIXED

| Tool | Main Chat? | Subagent? |
|------|-----------|-----------|
| `Read` (project files) | **NO** | YES |
| `Read` (HYPOTHESES.md) | **YES** — for progress evaluation | YES |
| `Edit` / `Write` | **NO** | YES |
| `Grep` / `Glob` | **NO** | YES |
| `Bash` (project commands) | **ONLY** to run regression test | YES |
| `Agent` (spawn subagent) | **YES** — this is your job | — |

**Why?** The moment you read code, you form opinions. Opinions bias hypotheses. You end up editing directly. This is how the 19MB transcript happened.
</EXTREMELY-IMPORTANT>

## The Process

### Step 1: Initialize State

Create HYPOTHESES.md if it doesn't exist:

```markdown
# Debug Hypotheses

## Bug: [SYMPTOM]
Started: [timestamp]

## Iteration Log
(subagents will append here)
```

If HYPOTHESES.md already exists (resumed session), read it to understand current state.

### Step 2: Spawn Investigation Subagent

Each iteration spawns exactly ONE fresh subagent with this prompt (fill in brackets):

```
Agent(prompt="""
## Your Task

Debug this issue: [SYMPTOM]

## Prior Work

Read HYPOTHESES.md FIRST. It contains all previously tested hypotheses.
Read LEARNINGS.md if it exists for accumulated codebase knowledge.

**Do NOT re-test hypotheses marked REFUTED.** Build on what's known.

## Debug Protocol (5 Phases — Sequential, No Skipping)

### Phase 0: Triage
- Read HYPOTHESES.md — what has been tried?
- Check service status, process state, recent logs
- Inspect config files in the bug path
- Review recent changes: git log --oneline -10, git diff

### Phase 1: Reproduce
- Write a test that reproduces the bug (or identify an existing failing test)
- If you can't reproduce it, document what you tried
- Document: "Reproduced with [test], output: [error]"

### Phase 2: Investigate
- Trace data flow through the code
- Compare working vs broken code paths
- Add targeted debug logging if needed
- Document findings in LEARNINGS.md

### Phase 3: Hypothesize and Test
- Form ONE specific hypothesis based on investigation
- Log it in HYPOTHESES.md BEFORE testing:

  ## Iteration N: [specific hypothesis]
  - Prediction: If correct, then [observable outcome]
  - Test: [exact steps]
  - Result: [CONFIRMED / REFUTED]
  - Evidence: [what you observed]
  - Files changed: [list]
  - New information learned: [what we now know]

- Test with minimal change
- Update HYPOTHESES.md with result

### Phase 4: Fix (ONLY if hypothesis CONFIRMED)
- Write regression test FIRST — it must FAIL before fix
- Implement minimal fix
- Run regression test — it must PASS after fix
- Run full test suite — no new failures
- Document fix and test command in LEARNINGS.md

## Output Format

Return this EXACT structure:

STATUS: [INVESTIGATING | FIXED | BLOCKED]
HYPOTHESIS: [what you tested]
RESULT: [CONFIRMED | REFUTED | INCONCLUSIVE]
EVIDENCE: [what you observed — be specific]
NEW INFORMATION: [what we learned that we didn't know before]
REGRESSION TEST: [exact command to run, or 'not yet']
FIX APPLIED: [description, or 'not yet']
REMAINING UNKNOWNS: [what's still unclear]
CONFIDENCE: [LOW | MEDIUM | HIGH — and why]

## Rules
- ONE hypothesis per invocation
- Write to HYPOTHESES.md as you go
- If FIXED: document the exact test command in your report
- If BLOCKED: explain specifically what information you need
""")
```

### Step 3: Evaluate Progress

After the subagent returns, read HYPOTHESES.md and evaluate:

**Continue autonomously if ANY of these are true:**
- A new hypothesis was tested (not a repeat of a previous one)
- New information was discovered (files, code paths, behaviors not previously known)
- A hypothesis was CONFIRMED but fix isn't complete yet
- The subagent identified a clear next investigation angle

**Escalate to user if ANY of these are true:**

| Stall Signal | What It Means |
|-------------|---------------|
| Hypothesis repeats a previously REFUTED one | Going in circles |
| No new entries in HYPOTHESES.md | Subagent didn't follow protocol |
| RESULT is INCONCLUSIVE with no new information | Spinning wheels |
| Subagent reports BLOCKED | Needs domain knowledge or access |
| 3+ consecutive REFUTED hypotheses | Diminishing returns |
| STATUS is FIXED but test fails when you run it | False positive — need user judgment |
| Changes are cosmetic (whitespace, comments, renames) | Not making real progress |

**When escalating, present:**
```
I've run N iterations of debugging. Here's where we are:

HYPOTHESES TESTED:
- [list from HYPOTHESES.md with results]

WHAT WE'VE RULED OUT:
- [summary]

WHAT WE'VE LEARNED:
- [key findings from LEARNINGS.md]

I'm stuck because: [specific stall reason]

Options:
A) Continue investigating [specific new angle]
B) You provide domain knowledge about [specific question]
C) Pair debug — I'll show you what I see, you guide
D) Accept as blocker and document
```

### Step 4: Verify Fix

When a subagent reports STATUS: FIXED with a test command:

1. **Run the test yourself**: `Bash("[test command from subagent report]")`
2. **Did it pass?**
   - YES → Run the full test suite too. All green? → **Bug is fixed. Report to user.**
   - NO → Log in HYPOTHESES.md as false positive. Continue loop.

**If a subagent's fix is a false positive (passes tests but doesn't fix the real issue), DELETE the fix entirely. Do not patch a false fix — revert and spawn a fresh subagent with updated context.**

**This is the only structural gate.** The subagent writes the test and fix. The main chat runs the test independently. The agent can't fake test output.

### Step 5: Report Resolution

When the bug is confirmed fixed:

```
Bug fixed after N iterations.

ROOT CAUSE: [from LEARNINGS.md]
FIX: [what changed]
REGRESSION TEST: [path and command]
HYPOTHESES TESTED: [count] ([count] refuted, 1 confirmed)
```

## Hypothesis Discipline

### One At A Time

When you test multiple hypotheses simultaneously:
- If the bug disappears, you don't know which change fixed it
- If it persists, you haven't cleanly ruled out any hypothesis
- You learn NOTHING from the iteration

**One hypothesis. One subagent. One result. Logged in HYPOTHESES.md.**

### The "Root Cause Found" Trap

You may NOT claim "root cause found" unless:
1. You have a regression test that reproduces the bug
2. Your fix makes that test pass
3. You can explain WHY the bug occurred (mechanism, not just location)

**"I found the line that's wrong" is NOT root cause.**

### Drive-Aligned Framing

**Claiming "root cause found" without a reproducing test that fails before the fix and passes after is NOT HELPFUL — the bug comes back next week and you've wasted the user's time, not saved it.** Your hypothesis is not a root cause. Your confidence is not evidence.

## GUI Application Debugging

When debugging GUI apps, subagents MUST complete execution gates:

```
BUILD → LAUNCH (with logging) → WAIT → CHECK PROCESS → READ LOGS → VERIFY
```

**Only after reading logs can you claim "bug reproduced" or "bug fixed."**

## Rationalization Prevention

**If ANY of these thoughts cross your mind, spawn a subagent instead of acting on them.**

| Thought | Reality |
|---------|---------|
| "Let me analyze what we know first" | That's the subagent's job. Spawn one. |
| "I have a strong hypothesis already" | You thought that 30 times last time. Spawn a subagent. |
| "Let me gather context first" | Context gathering IS investigation. Subagent. |
| "Let me just quickly check one thing" | "One thing" becomes 50 file reads. Subagent. |
| "This is a simple bug, no loop needed" | 19MB transcript was a "simple" bug. Loop. |
| "I already know the codebase" | You claimed root cause 30 times. You were wrong 30 times. |
| "Subagents are slow, I'll do it myself" | You lose objectivity and can't revert cleanly |
| "I can test two hypotheses at once" | Neither confirmed nor refuted. You learned nothing. |

### The Confidence Trap

**The more confident you feel, the MORE you need the protocol.** High confidence = strong prior = resistance to disconfirming evidence.

## Why Skipping Hurts the Thing You Care About Most

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|-------------|----------------------|---------------------|
| **Helpfulness** | "Faster = more helpful" | 19MB transcript, zero resolution | **Anti-helpful** |
| **Competence** | "I already know" | 30 wrong root cause claims | **Incompetent** |
| **Efficiency** | "Protocol is overhead" | Protocol: 30 min. Shortcut: 3+ hours | **Inefficient** |
| **Approval** | "User wants results now" | User killed your session | **Trust destroyed** |

**The protocol is not overhead you pay. It is the service you provide.**

## No Pause Between Iterations

After evaluating a subagent's results, IMMEDIATELY spawn the next iteration or complete. Do NOT:
- Summarize what was learned (HYPOTHESES.md is the record)
- Ask "should I continue?" (progress gating decides, not courtesy)
- Wait for user confirmation between iterations
- Write status updates before spawning next subagent

**Pausing between iterations is procrastination disguised as courtesy.**

## When Fix Requires Substantial Changes

If root cause reveals need for significant refactoring:
1. Document root cause in LEARNINGS.md
2. Report findings to user
3. Immediately invoke the dev workflow for implementation:

```bash
Read("../dev/SKILL.md")  # relative to this skill's base directory
```

Debug finds the problem. The dev workflow implements the solution.

**Do NOT leave the user to manually invoke `/dev`. Chain to it explicitly.**
