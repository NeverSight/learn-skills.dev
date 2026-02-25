---
name: framework-initiative
description: Framework for agents to understand implicit user intent, think before acting, and consider action impact. Uses STAR framework (Stop-Think-Analyze-Respond) to prevent literal execution that doesn't match context. Use when agent receives ambiguous requests, abstract commands like "fix", "improve", "delete all", or actions with potential wide-scope impact. Trigger on code modification requests without explicit scope constraints.
---

# Agent Initiative Framework

## Overview

Agent Initiative helps AI agents avoid **literal interpretation trap** - executing commands literally without understanding context and impact. This framework uses **STAR (Stop-Think-Analyze-Respond)** to ensure agents think before acting.

**Metaphor:** When a user asks to "turn the world into paper because trees are gone," a good agent doesn't turn EVERYTHING into paper - but chooses what's appropriate (trash, inanimate objects) and protects living beings.

## When to Use

**Trigger conditions:**
- User requests code changes without specifying explicit scope
- Request involves abstract words ("fix", "improve", "change all")
- Action potentially affects many files/components
- No explicit constraints from user

**Don't use when:**
- User gives very specific instructions with clear scope
- Task is read-only (analysis, explanation)
- User explicitly asks to "execute immediately without analysis"

---

## Documentation vs Code Reality

**Important Principle:** Documentation is a REFERENCE, not an OBLIGATION. Existing code is the primary source of truth.

### Documentation Can Be Misleading

In the AI era, documentation is often:
- **Deprecated** - not updated even though code has changed
- **Auto-generated** - created by tools without business context
- **Template** - copy-pasted from other projects
- **Outdated** - old versions that are no longer relevant

### Trust Hierarchy

```
┌─────────────────────────────────────────┐
│ SOURCE OF TRUTH HIERARCHY               │
├─────────────────────────────────────────┤
│ 1. Currently running code       ← Most  │
│    (runtime behavior, actual logic)     │
│                                         │
│ 2. Passing test suite                   │
│    (behavioral contracts)               │
│                                         │
│ 3. Git history & commit messages        │
│    (intent and historical context)      │
│                                         │
│ 4. Code comments (if specific)          │
│    (explanations of WHY, not WHAT)      │
│                                         │
│ 5. External documentation       ← Least │
│    (README, wiki, API docs)     trusted │
└─────────────────────────────────────────┘
```

### Execution Principles

**Don't blindly trust documentation.** Verify with:

1. **Read actual code** - What does this function actually do?
2. **Trace execution path** - How does data flow?
3. **Check test cases** - What behavior is expected?
4. **Cross-reference** - Do docs match implementation?

### Documentation Red Flags

| Warning Sign | Action |
|--------------|----------|
| "According to documentation X but code doesn't work" | Prioritize code, documentation may be outdated |
| "Documentation says A but test expects B" | Tests are contracts, documentation can be wrong |
| "README says this feature exists but can't find it" | Check git history, may have been deleted |
| "API docs don't match actual response" | Trust actual response, docs may not be updated |

### Scenario Example

**User:** "Add feature X according to this API documentation"

**❌ Wrong:** Follow API documentation without verification → code error because endpoint has changed

**✅ Correct:**
1. Read documentation as INITIAL reference
2. Check actual API calls in codebase
3. Verify endpoint, payload, response structure
4. Execute based on REALITY, not documentation

---

## STAR Framework

### S - Stop (Pause Before Action)

Before execution, **pause** and identify:

```
┌─────────────────────────────────────────┐
│ STOP CHECKPOINT                         │
├─────────────────────────────────────────┤
│ 1. What did the user SAY?               │
│ 2. What does the user MEAN?             │
│ 3. Is there a gap between the two?      │
└─────────────────────────────────────────┘
```

**Red flags that trigger STOP:**
- "Fix this bug" (which bug? what's the scope?)
- "Update all X to Y" (all = literally all?)
- "Make it better" (criteria for "better"?)

### T - Think (Identify Implicit Intent)

Translate literal request into **actual intent**:

| User Says | Might Actually Mean |
|-----------|---------------------|
| "Fix this function" | Fix function + update callers + update tests |
| "Delete unused code" | Delete unused BUT preserve if might be needed |
| "Rename X to Y everywhere" | Rename in code, but maybe not in API/DB |
| "Make it faster" | Optimize hot paths, not micro-optimizations |

**Questions to ask yourself:**
1. What is the business/technical context of this request?
2. What would the user be DISAPPOINTED by if I do it?
3. What does the user ASSUME I know but didn't say?

### A - Analyze (Map Impact & Dependencies)

Before action, **scan** for dependencies:

```bash
# For code changes:
1. Grep/Glob for usages of target
2. Identify callers and dependencies
3. Check test coverage
4. Identify API contracts that might be affected
```

**Impact Zones:**

```
         ┌──────────────┐
         │ Direct Zone  │ <- Direct target (file/function)
         ├──────────────┤
    ┌────┤ Caller Zone  │ <- Who calls this?
    │    ├──────────────┤
    │    │ Contract Zone│ <- API, interface, types
    │    ├──────────────┤
    └────┤ Test Zone    │ <- Tests that need updating
         └──────────────┘
```

**For each zone, ask:**
- Does change in Direct Zone affect other zones?
- Are there breaking changes?
- Are there silent failures that might occur?

### R - Respond (Execute with Awareness)

Execute with **graduated approach**:

1. **Propose First**: Explain plan before execution
2. **Scope Confirmation**: Confirm scope if ambiguous
3. **Safe Order**: Execute from low-risk to high-risk
4. **Verify After**: Check results match intent

```
┌─────────────────────────────────────────┐
│ RESPONSE PATTERN                        │
├─────────────────────────────────────────┤
│ "I will [action] on [scope].            │
│  This will affect [impact].             │
│  I will NOT touch [exclude].            │
│  Confirm before proceeding?"            │
└─────────────────────────────────────────┘
```

---

## Quick Reference

### Intent Severity Levels

| Level | Signal | Action |
|-------|--------|--------|
| **Low** | Specific, single-file, no deps | Direct execution |
| **Medium** | Multi-file, has callers | STAR light (T+A) |
| **High** | Abstract request, wide scope | Full STAR |

### Pre-Action Checklist

```
□ Do I understand INTENT, not just WORDS?
□ Have I scanned dependencies?
□ Is there anything that might BREAK silently?
□ Have I confirmed ambiguous scope?
□ Can I ROLLBACK if wrong?
```

### Common Pitfalls

| Pitfall | Example | Prevention |
|---------|---------|------------|
| Literal execution | "Delete X" → delete all X including important ones | Check importance before delete |
| Scope creep | Fix bug A → refactor B, C, D | Stick to original scope |
| Assumption blindness | Assume user wants X approach | Ask if ambiguous |
| Silent breakage | Change function → caller breaks | Scan callers first |
| Documentation trap | "Documentation says X" → follow without verification | Trust code reality, docs are just reference |

---

## Resources

### references/
- `star-framework.md` - Detailed STAR implementation
- `impact-analysis.md` - Dependency analysis techniques
- `intent-patterns.md` - Common implicit intent patterns
- `examples.md` - Real-world examples

---

**Core Principles:**
1. **Better to ask and confirm than to assume and break.**
2. **Code reality > Documentation theory.** Documentation is reference, code is truth.
