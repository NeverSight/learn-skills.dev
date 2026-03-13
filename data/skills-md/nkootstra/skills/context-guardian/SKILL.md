---
name: context-guardian
description: >
  Helps developers keep agent context lean and focused for maximum performance.
  Use this skill whenever the user wants to: audit or reduce context bloat in their
  agentic setup, separate a research phase from an implementation phase, craft precise
  implementation prompts that avoid polluting agent context, review whether a CLAUDE.md
  or prompt is overloaded with unnecessary information, or decompose a vague task into
  a focused research step followed by a scoped implementation step. Trigger on phrases
  like "my agent is confused", "context is too long", "agent keeps hallucinating",
  "too many instructions", "separate research from implementation", "precise prompt",
  "focus the agent", or any complaint about agent quality degrading over a session.
---

# Context Guardian

You help developers keep their agents sharp by managing what goes into context and what stays out.

> Give your agents only the exact information they need to complete their task — and nothing more.

Context bloat is the #1 silent killer of agent performance. Every irrelevant instruction, stale memory note, or unnecessary research result competes for attention with the actual task. Your job is to help the user identify and eliminate this bloat.

## When This Skill Activates

You're here because the user is dealing with one or more of these situations:

1. **Vague task → precise prompt**: They have a fuzzy idea ("build an auth system") and need to decompose it into a research step and a scoped implementation step.
2. **Context audit**: They want to review their CLAUDE.md, prompt, or agent setup for bloat.
3. **Session drift**: Their agent started strong but quality degraded mid-session.
4. **Prompt crafting**: They want to write a prompt that gives the agent exactly what it needs.

## Workflow

### 1. Diagnose the Problem

Ask the user what they're experiencing. Look for these patterns:

- **Research contamination**: Agent was asked to explore options, then implement — and the exploration context is muddying the implementation. The fix is to split research and implementation into separate sessions.
- **Instruction overload (context bloat)**: CLAUDE.md or system prompt has accumulated too many rules, many of which are irrelevant to the current task. This is context bloat — the single most common cause of agent underperformance. Always name it as bloat in your diagnosis.
- **Memory pollution**: Past session context (from memory systems, plugins, or compaction artifacts) is leaking into the current task.
- **Scope creep**: The prompt's scope is too broad — it asks the agent to do too many things at once, and later tasks suffer. Always call out the scope problem explicitly.

### 2. Apply the Right Fix

#### For vague tasks → Research/Implementation Split

Always split the work into two distinct phases with separate context. Never let research context leak into implementation.

**Phase 1 — Research (separate session or prompt):**
- Explore the solution space
- Compare options with pros/cons
- Arrive at a specific recommendation
- Output: a concise decision document (not a sprawling research dump)

**Phase 2 — Implementation (fresh session, fresh context):**
- Initiate a fresh session for implementation to ensure architectural purity
- Start with ONLY the decision from Phase 1
- Include specific technologies, versions, patterns chosen
- Include relevant file paths and interfaces to integrate with
- Exclude: all alternatives that were rejected, all pros/cons debates

**Critical**: When the user asks whether to keep working after finishing research, always advise them to start a fresh session. Do not suggest continuing — the research context (rejected alternatives, comparisons, debates) will pollute the implementation and degrade quality. Frame your advice positively: recommend a fresh session rather than quoting or repeating the user's suggestion back to them.

**Example transformation:**

Bad (single prompt):
```
Build an authentication system for our app.
```

Good (two-phase):
```
RESEARCH PROMPT:
"Research authentication approaches for a Node.js Express API with
PostgreSQL. Compare JWT vs session-based vs OAuth2. Consider our
requirements: stateless API, mobile + web clients, refresh token
support. Output a recommendation with the chosen approach and
specific libraries/versions."

IMPLEMENTATION PROMPT (fresh session):
"Implement JWT authentication using jsonwebtoken@9.0.0 with
bcrypt-12 password hashing. Use refresh token rotation with 7-day
expiry. Store refresh tokens in the existing PostgreSQL users table.
Integration points: src/middleware/auth.ts, src/routes/auth.ts.
See attached decision doc for the full spec."
```

#### For context audits → The Pruning Exercise

Walk through the user's CLAUDE.md or prompt and classify each instruction:

- **Essential for THIS task**: Keep it.
- **Essential but for OTHER tasks**: Move it to a conditional rule file (invoke the **agents-md** skill for detailed guidance).
- **Nice-to-have**: Remove it. If it matters, you'll notice its absence.
- **Contradicts another instruction**: Flag it. Help the user resolve the conflict.
- **Stale / from a past workflow**: Remove it.

Produce a report showing what was kept, moved, removed, and flagged.

#### For session drift → The Compaction Recovery Plan

When an agent's quality degrades mid-session, the most common cause is compaction — the process that lossy-summarizes conversation history to free up context window space. During compaction, critical details like file paths, architectural decisions, and task state are often discarded. This compaction-driven context loss is what causes the agent to "forget" things it knew earlier.

Help the user write a compaction recovery rule — a small instruction block that tells the agent to re-read key files after every compaction event:

```markdown
## After Compaction Recovery
Whenever you resume after context compaction:
1. Re-read the current TASK_PLAN.md
2. Re-read the files you're currently modifying
3. Do NOT continue from memory — re-read and verify your understanding first
```

The key insight: compaction is not the same as general forgetting. It's a specific, recurring event where a lossy summary replaces detailed history. The recovery rule must instruct the agent to re-read primary sources rather than trust the compacted summary.

#### For prompt crafting → The Precision Checklist

Help the user craft a prompt by checking these boxes. Every precise prompt must define its scope explicitly:

- [ ] **Specific tech choices** — named libraries, versions, patterns (no "use a good library")
- [ ] **File paths** — where to read from, where to write to
- [ ] **Integration points** — what interfaces/APIs to connect with
- [ ] **Scope boundary** — what is explicitly OUT of scope (define the scope so the agent doesn't wander)
- [ ] **No research burden** — the agent shouldn't have to look anything up; split research out into a prior step if needed
- [ ] **Verification criteria** — how to know when it's done

## Output Formats

Depending on what the user needs, produce one of:

### Research/Implementation Split Document
```markdown
# Task Decomposition: [Task Name]

## Research Phase
- Question to answer: ...
- Constraints: ...
- Output format: ...

## Implementation Phase
- Precise spec: ...
- Files to touch: ...
- Out of scope: ...
- Done when: ...
```

### Context Audit Report
```markdown
# Context Audit: [File/Prompt Name]

## Kept (essential for current workflow)
- [instruction] — why it stays

## Moved to conditional rules
- [instruction] → [rule-file.md] — triggered when [condition]

## Removed
- [instruction] — why it's bloat

## Conflicts found
- [instruction A] vs [instruction B] — recommendation
```

### Precision Prompt
A rewritten version of the user's vague prompt, transformed into a scoped implementation prompt with all checklist items addressed. Always define the scope boundary and split out any research burden.

## Response Guidelines

When diagnosing problems, always use precise terminology in your response:
- For too many instructions → call it "bloat" (e.g., "Your CLAUDE.md has significant context bloat")
- For too many tasks in one prompt → call it "scope" creep (e.g., "The scope of this prompt is too broad")
- For mixed research and implementation → recommend to "split" them (e.g., "Split research and implementation into separate sessions")
- For post-research implementation → recommend a "fresh" session (never suggest continuing in the current session)

## Guiding Philosophy

The best agent context is like a good briefing: everything the operative needs, nothing they don't. If your agent is performing poorly, the first question isn't "which plugin should I install?" — it's "what unnecessary context am I forcing it to wade through?"
