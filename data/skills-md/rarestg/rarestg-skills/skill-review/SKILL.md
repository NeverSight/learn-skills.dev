---
name: skill-review
description: Review an agent skill for quality, completeness, and correctness. Evaluates purpose, approach, implementation, frontmatter, progressive disclosure, and whether scripts or references are needed. Use after creating or modifying a skill.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep
argument-hint: "[path/to/skill]"
---

# Skill Review

Review a skill and propose improvements only if genuinely needed. Bias toward leaving things alone. A short, focused skill is better than a comprehensive one that wastes tokens.

## Process

### 1. Read everything

Read all files in the skill directory: SKILL.md, any scripts, references, assets.

### 2. State the intent

In one sentence: what problem does this skill solve, and for whom? Ground the rest of the review in this.

### 3. First-principles check

- Is this the right approach to the problem?
- Is it the simplest approach that works?
- Does the skill add value beyond what an AI agent already knows?
- If the agent could do this without the skill, the skill may not be needed.

### 4. Review checklist

**Frontmatter:**
- Is `description` specific about WHEN to trigger? Does it include concrete phrases a user would say?
- `disable-model-invocation: true` if the skill has side effects (merges, deploys, sends, deletes).
- `allowed-tools` set to restrict scope to only what's needed?
- `argument-hint` set if the skill takes arguments?
- Are `context`, `agent`, `model`, `user-invocable`, or `hooks` relevant and missing?

**Body:**
- Under 500 lines? If over, move content to reference files.
- Does every paragraph justify its token cost? Cut anything the agent already knows.
- Are instructions concrete and actionable, not vague?
- If files are referenced, is it clear when to load them?

**Progressive disclosure:**
- Is SKILL.md doing too much? Should content move to `references/`?
- Would a bundled script be more reliable than prose instructions? (Yes if the agent would regenerate the same code every invocation.)

**Scripts (if present):**
- Do they actually run? Test them.
- Are they necessary, or would instructions suffice?

**Bloat check:**
- Is anything here that an AI agent already knows? Remove it.
- Are there redundant explanations? Cut them.
- Could the skill be shorter without losing effectiveness?
- If the skill is fine as-is, say so. Do not invent improvements.

### 5. Ask clarifying questions

Before proposing any changes, ask the user about anything ambiguous: intent, scope, preferences, edge cases. Do not assume.

### 6. Present findings

Summarize:
1. The skill's purpose (one sentence)
2. What's working well
3. Specific issues found (if any)
4. Proposed changes with rationale for each

If no changes are needed, say "No changes recommended" and stop. Do not manufacture improvements.

### 7. Apply changes (only with approval)

Only after the user explicitly approves:
1. Make the changes
2. Stage the modified files
3. Commit with a clear message
4. Push

Never commit or push without explicit user approval.
