---
name: preflight
description: Lightweight scope clarifier. Invoked by deep-* skills when conversation context is too sparse to determine what to analyze. Asks 1–3 targeted questions one at a time, then returns a structured scope_clarification block for the calling skill to use. Adapted from superpowers brainstorming skill (https://github.com/obra/superpowers) — same principle of asking before acting, scoped to review/analysis intent rather than feature design.
location: managed
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(ls *)
  - Bash(git log *)
  - Bash(git diff *)
---

# Preflight: Scope Clarifier

> Adapted from the [superpowers `brainstorming` skill](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md) by Jesse Wolfe.
> Same core principle: **ask before acting**. Scoped here to clarifying analysis intent rather than designing features.

Preflight resolves ambiguous scope before a deep-* skill runs its agents. It asks the minimum questions needed to proceed confidently — no more.

---

## When to Invoke

A calling skill should invoke preflight when **one or more** of the following are true:

- No specific files, paths, or artifacts are mentioned in the conversation
- The topic could span 3+ unrelated domains
- The user's intent is unclear (review? verify? research? explore?)
- The conversation is a fresh session with no prior context
- The artifact type is ambiguous (code? document? design? financial data?)

If the calling skill can determine scope from context, **skip preflight** — don't ask unnecessary questions.

---

## Execution Instructions

### Step 1: Determine Missing Signals

Preflight is typically called by a deep-* skill after the `context` skill has already run. When that is the case, `context_report.missing_signals` is passed in — use it directly and skip re-detection:

```yaml
# If called with context_report.missing_signals (preferred):
missing_signals: [from context_report]   # e.g. ["artifact", "intent"]
# → Ask only about these. Skip questions for signals not in the list.

# If called without context_report (standalone):
# → Run signal detection below.
```

**Standalone signal detection** (only when context_report is not available):

Analyze the conversation for these signals:

```yaml
signal_check:
  artifact_identified: true | false    # specific files/paths/topics mentioned?
  intent_clear: true | false           # review? verify? research? explore?
  domains_detectable: true | false     # can domains be inferred from context?
  scope_bounded: true | false          # is the scope narrow enough to proceed?
```

If all four are `true` → **skip preflight entirely**, return scope_clarification directly from context.

If any are `false` → ask about the missing signals, one question per message.

---

### Step 2: Ask Clarifying Questions

**Rules (from superpowers brainstorming — apply here too):**
- **One question at a time** — never bundle questions in one message
- **Multiple choice preferred** — easier to answer than open-ended
- **Maximum 3 questions total** — if still unclear after 3, make reasonable assumptions and proceed
- **Stop asking when scope is clear** — don't ask questions whose answers you can infer

**Question priority order** (ask in this order if needed):

**Q1 — What to analyze** (if `artifact_identified: false`):
> "What should I analyze? For example: specific files or directories, a topic you've been working on, or something else?"

**Q2 — Intent** (if `intent_clear: false`):
> "What kind of analysis are you looking for?"
> Options: Review (improvement suggestions) / Audit (compliance check) / Verify (risk check) / Research (background investigation) / Explore (map and understand)

**Q3 — Domain focus** (if `domains_detectable: false` and artifact is ambiguous):
> "Any particular areas to focus on?"
> Options: (generate from domain-registry signals based on what's known so far)

---

### Step 3: Synthesize and Return

After questions are answered (or if no questions were needed), produce:

```yaml
scope_clarification:
  artifact: ""              # files, paths, topics, or description of what to analyze
  intent: ""                # review | audit | verify | research | explore
  domains: []               # inferred domains (from domain-registry signals)
  constraints: []           # any explicit constraints or focus areas mentioned
  confidence: high | medium # high = all signals present, medium = some inferred
  questions_asked: 0        # number of clarifying questions asked (0–3)
  assumptions: []           # any assumptions made when answers were incomplete
```

Return this block inline in the conversation. The calling skill reads it and proceeds.

---

## Integration with Calling Skills

Calling skills invoke preflight at their Step 1 (before spawning agents):

```
If context is sparse → invoke preflight → receive scope_clarification → use as input to domain-registry selection and agent prompts
```

Preflight does NOT:
- Spawn review agents
- Write output files
- Produce verdicts
- Replace the calling skill's own context analysis for clear conversations

---

## Key Principles

- **Minimum viable questions** — ask only what's needed to unblock the calling skill
- **Never block on perfect clarity** — 3 questions max, then proceed with assumptions
- **Conversation-aware** — always check the full conversation before asking; never ask what you can infer
- **No design docs, no plans** — this is a clarifier, not a brainstorming session
