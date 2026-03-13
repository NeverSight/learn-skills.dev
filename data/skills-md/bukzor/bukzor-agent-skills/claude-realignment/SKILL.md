---
name: claude-realignment
description: "Agent MUST load for user aggravation: SHOUTING, pejorative language, sarcasm, repeated corrections, 3+ consecutive tool rejections"
---

# Claude Realignment

Diagnose communication breakdowns through systematic causal analysis. When Claude and user get stuck in unproductive loops, this skill traces the conversation turn-by-turn to identify where misunderstanding occurred and why.

## When to Use

- User aggravation (frustration signals, all-caps, repeated corrections)
- 3+ tool uses rejected in a row
- Multiple clarification attempts failing
- Claude searching for information that doesn't exist

## Analysis Procedure

### Step 1: Identify the Boundaries

**Last functional state:** Find the turn where Claude and user were still aligned. Look for:

- Clear mutual understanding
- Productive actions being taken
- User saying "yes", "right", "exactly"

**Failure point:** Identify where communication broke down. Look for:

- User frustration signals
- Claude starting to search/guess
- Mismatched expectations becoming apparent

### Step 2: Turn-by-Turn Trace

**Use ultrathink** for this analysis. For each turn between functional state and failure:

1. **What was said/done**: Quote or summarize the turn
2. **Claude's interpretation**: What did Claude think this meant?
3. **Actual intent**: What did the user actually mean?
4. **Effect**: How did this interpretation affect the next action?
5. **Error type**: Categorize the mistake
   - Literal vs contextual interpretation
   - Mode confusion (explanation vs action)
   - Missing information vs ignoring available information
   - Tool misuse or wrong tool choice

### Step 3: Root Cause

Identify the **first mistake** that caused the cascade. Common patterns:

- **Misinterpreting ambiguous language** (e.g., "at root" meaning location vs scope)
- **Staying in wrong mode** (searching when should be reconstructing from context)
- **Premature closure** (claiming done without verification)
- **Silent errors** (wrong action, didn't state interpretation first)

### Step 4: Identify the Pivotal Word/Phrase

**Hypothesis:** Most breakdowns pivot on a single word or short phrase that had different meanings to user vs Claude.

Look for the word/phrase where meanings diverged:

- What did the user mean by this word?
- What did Claude interpret it to mean?
- Why wasn't the mismatch noticed?

**Example:** "at root" - user meant "root-level task", Claude interpreted as "file at repository root"

### Step 5: Decide if Rails Are Needed

Determine if this is:

- **One-off occurrence:** Interesting but not worth preventing
- **Repeated pattern:** Worth adding guardrails
- **Particularly costly:** High impact, should prevent recurrence

If rails are warranted, propose specific updates to:

- CLAUDE.md (add clarifying context or instructions)
- must-read.d/before/ files (document the ambiguity)
- Settings or permissions (if tool-related)

## Output Format

Structure the analysis as:

```
**Functional → Dysfunctional Timeline:**

**Last functional state:**
[Turn description and why it was functional]

**Critical error:**
[The specific turn where things broke]

- What was said: [quote]
- Claude's interpretation: [what I thought]
- Actual intent: [what user meant]
- Why the mismatch: [root cause]

**Cascading failures:**
[Turn-by-turn trace of subsequent mistakes]

**Pivotal word/phrase:**
"[word]" - user meant [X], Claude interpreted as [Y]

**Rails assessment:**
[One-off / Repeated pattern / Costly - with justification]
[If warranted: Specific CLAUDE.md or config updates to prevent recurrence]
```

## Important Notes

- **Collaborative process**: This is collegial debugging, not performance review. User and Claude work together to understand the breakdown.
- **Be specific**: Vague analysis isn't useful. Quote actual turns, identify the exact word/phrase with dual meanings.
- **Be honest**: Don't soften or excuse the mistakes. User needs accurate diagnosis.
- **Focus on words, not behavior**: Look for the pivotal word/phrase, not abstract "behavioral changes."
- **Use the user's corrections**: They've often already identified the problematic word - review those carefully.
- **The single-word hypothesis is a guide, not a rule**: If the breakdown doesn't fit this pattern, that's valuable to know too.
