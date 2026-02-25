---
name: showcase-export
description: Capture full orchestration details (skills, agents, decisions, compound learning) in your session transcript for YC or investor demos. Use --showcase flag at session start. Works with Claude's built-in /export command.
triggers:
  - "--showcase"
  - "showcase mode"
  - "YC export"
  - "investor demo"
  - "capture orchestration"
  - "visible orchestration"
---

# Showcase Export Mode

Ensures all skill/agent orchestration is VISIBLE in the session transcript when you run the built-in `/export` command.

> **Note:** This skill defines a PROTOCOL for what Claude should narrate during a session. It works WITH the built-in `/export` command, not as a replacement.

## Quick Start

```bash
# At session START
"Build my-project --showcase"

# When done, use built-in export
/export                    # Export to clipboard or file
```

**For OLD sessions, use the `session-reconstruct` skill instead.**

---

## The Problem

```
Default behavior:
- Skills execute silently (instructions inject invisibly)
- Agents work in background (subagent reasoning hidden)
- Compound learning runs as bash commands (semantic meaning lost)
- Decision rationale is implicit (tradeoffs not explained)
- /export only captures visible conversation
- YC doesn't see your orchestration mastery
```

## The Four Structural Gaps

| Gap | What's Hidden | Fix Required |
|-----|---------------|--------------|
| **Skill Logic** | Skill instructions inject into context invisibly | Explain what the skill instructed you to do |
| **Subagent Internals** | Task tool returns only final result | Narrate the agent's internal process |
| **Compound Learning** | DB operations are opaque bash commands | Explain the semantic meaning of patterns |
| **Decision Rationale** | Choices made without explaining tradeoffs | State every significant tradeoff explicitly |

## The Solution

**Every skill, agent, compound update, and decision must be narrated for the transcript.**

This is not optional verbosity—it's **structural visibility** that makes orchestration mastery observable in /export.

---

## Mandatory Orchestration Protocol

When `--showcase` is enabled, you MUST follow ALL of these protocols:

### 1. Announce Skill Activation (with Logic Surfacing)

When a skill loads, its instructions are invisible to the transcript. You MUST explain what the skill is telling you to do:

```markdown
## 🔧 Skill Activated: [skill-name]

**Purpose:** [what this skill does]
**Triggered by:** "[user's words that triggered it]"

**This skill instructs me to:**
1. [First instruction from the skill]
2. [Second instruction from the skill]
3. [Third instruction from the skill]

**I will now execute these instructions...**
```

### 2. Show Skill Execution (with Reasoning)

```markdown
### Executing: [skill-name]

**Step 1:** [what we're doing]
→ Reasoning: [why this step matters]
→ Result: [outcome]

**Step 2:** [what we're doing]
→ Alternative considered: [what else could have been done]
→ Why rejected: [reason]
→ Result: [outcome]
```

### 3. Summarize Skill Output (with Tradeoff Documentation)

```markdown
### ✅ Skill Complete: [skill-name]

**Deliverables:**
- [output 1]
- [output 2]

**Key decisions made (with tradeoffs):**
| Decision | Alternative | Why Chosen |
|----------|-------------|------------|
| [Choice A] | [Alternative B] | [Specific reason] |
```

### 4. Announce Agent Spawning (with Internal Process Narration)

When spawning agents via Task tool, only the final result returns. You MUST reconstruct and narrate what the agent did:

```markdown
## 🤖 Spawning Agent: [agent-name]

**Mission:** [what this agent will do]
**Tools available:** [list of tools]
**Why this agent vs. doing it directly:** [reason for delegation]

---

### Agent Complete: [agent-name]

**Final Result:** [the returned summary]

**Reconstructed Internal Process:**
- **Tool calls made:** ~[estimate] ([list tools likely used])
- **Key reasoning steps:**
  1. [Inferred reasoning step 1]
  2. [Inferred reasoning step 2]

**Decision points the agent navigated:**
| Decision | Agent's Choice | Likely Reason |
|----------|----------------|---------------|
| [Decision 1] | [Choice] | [Reason] |
```

### 5. Document Decision Points

```markdown
### 📋 Decision Point: [Brief Description]

**Options Considered:**
| Option | Pros | Cons |
|--------|------|------|
| [A] | [advantages] | [disadvantages] |
| [B] | [advantages] | [disadvantages] |

**Decision:** [What was chosen]
**Rationale:** [Why this option won]
```

### 6. Show Compound Learning (Semantic Meaning)

```markdown
### 🔄 Compound Learning Update

**Pattern Extracted:**
> "[Natural language description of what was learned]"

**Evidence:**
1. [What demonstrated this]

**How this changes future behavior:**
Before: [old behavior]
After: [new behavior]
```

### 7. Checkpoint Summaries

```markdown
───────────────────────────────────────────────────────
### 📊 Checkpoint: After Phase [N]
───────────────────────────────────────────────────────

**Skills used:** [count] ([list])
**Agents spawned:** [count] ([list])
**Key decisions:** [list with rationale]

**Proceeding to Phase [N+1]...**
```

---

## Export Checklist

Before running `/export`, verify:

- [ ] Every skill activation explains what the skill instructed
- [ ] Every agent spawn includes reconstructed internal process
- [ ] Compound learning includes semantic meaning
- [ ] Every significant decision shows tradeoffs
- [ ] Phase transitions clearly marked
- [ ] Final summary included

---

## Complete Workflow

```bash
# 1. START SESSION with showcase mode
"Build my-project --showcase"

# 2. WORK normally - Claude narrates orchestration per this protocol

# 3. EXPORT using built-in command
/export session.md

# 4. (Optional) RECONSTRUCT if gaps exist
"Fill in any orchestration gaps --reconstruct"
```

---

## Installation

```bash
npx skills add sunnypatneedi/skills
```
