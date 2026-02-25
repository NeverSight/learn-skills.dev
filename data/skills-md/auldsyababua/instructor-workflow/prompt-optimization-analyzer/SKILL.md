---
name: prompt-optimization-analyzer
description: Active diagnostic tool for analyzing skill prompts to identify token waste, anti-patterns, trigger issues, and optimization opportunities. Use when reviewing skill prompts, debugging why skills aren't triggering, optimizing token usage, or preparing skills for publication. Provides specific, actionable suggestions with examples.
---

# Prompt Optimization Analyzer

## When to Use This Skill

**Always use when:**
- User asks to "review", "analyze", "optimize", or "improve" a skill prompt
- User says a skill "isn't triggering" or "isn't working as expected"
- User wants to "reduce token usage" in a skill
- User is "preparing a skill for publication" or sharing
- User asks "why isn't my skill being called?"
- User wants to "compare" two skill prompt versions

**Consider using when:**
- User shares a skill file for any reason (offer to analyze)
- User mentions a skill is "using too many tokens"
- User describes confusing or inconsistent skill behavior

---

## Analysis Framework

Run each skill prompt through this comprehensive diagnostic checklist. Report findings in order of severity (Critical → High → Medium → Low).

### 1. Trigger Pattern Analysis

**Critical Issues:**
- ❌ Missing or extremely vague description field
- ❌ Description doesn't match actual skill capabilities
- ❌ No clear trigger patterns identifiable from description
- ❌ Trigger patterns overlap heavily with other common skills

**High Priority:**
- ⚠️ Description is too generic ("helps with tasks", "assists users")
- ⚠️ Trigger keywords buried in long description
- ⚠️ Missing key verbs or nouns that users would naturally use
- ⚠️ Ambiguous scope (could apply to too many or too few situations)

**Optimization Opportunities:**
- 💡 Could add explicit trigger examples to description
- 💡 Could make description more action-oriented
- 💡 Could add domain-specific terminology
- 💡 Could clarify when NOT to use skill

**Good Patterns:**
- ✅ Description starts with clear trigger context
- ✅ Includes specific verbs that map to user intent
- ✅ Provides clear scope boundaries
- ✅ Uses "Use when..." or "This skill should be used when..." patterns

---

### 2. Token Efficiency Analysis

**Token Waste Patterns:**

**Redundancy:**
- 🔴 Repeating the same concept in multiple ways without adding clarity
- 🔴 Restating information already in the description
- 🔴 Duplicate examples that teach the same pattern
- 🔴 Verbose explanations where concise language would work

**Example - Before (wasteful):**
```
This skill helps you create documents. It's useful for document creation.
When you need to make a document, this skill can help. Documents that can
be created include reports, letters, and memos.
```

**Example - After (efficient):**
```
Creates professional documents including reports, letters, and memos.
```

**Over-Politeness:**
- 🔴 Excessive apologetic language ("please", "kindly", "if you don't mind")
- 🔴 Unnecessary hedging ("might", "perhaps", "possibly") where direct instruction works
- 🔴 Filler phrases ("it should be noted that", "it's important to mention")

**Example - Before:**
```
You might want to perhaps consider possibly using this approach if you think it could help.
```

**Example - After:**
```
Use this approach when [specific condition].
```

**Bloated Structure:**
- 🔴 Excessive nested XML tags when flat structure would work
- 🔴 Long prose explanations where bullet points are clearer
- 🔴 Including "meta" instructions about the skill itself (usually unnecessary)
- 🔴 Detailed explanations of concepts Claude already knows

**Over-Specified Formatting:**
- 🔴 Dictating exact phrasing for every possible response
- 🔴 Template sentences that reduce flexibility
- 🔴 Formatting rules that don't materially impact quality

**Efficiency Checklist:**
- Calculate estimated token count (rough: 1 token ≈ 4 characters)
- Identify sections that could be condensed by 30%+
- Flag any paragraph longer than 100 words for review
- Look for opportunities to replace prose with structured format

---

### 3. Anti-Pattern Detection

Reference the prompting-pattern-library skill for detailed anti-patterns. Key failures to check:

**Ambiguity Failures:**
- ❌ Unclear success criteria ("make it better", "improve quality")
- ❌ Vague output format requirements
- ❌ Ambiguous scope ("explain X" without audience/depth specification)
- ❌ Undefined technical terms or jargon

**Conflicting Instructions:**
- ❌ "Be concise but comprehensive"
- ❌ "Be creative but follow strict rules"
- ❌ "Be formal but conversational"
- ❌ Multiple competing priorities without clear hierarchy

**Implicit Assumptions:**
- ❌ Assuming Claude knows context not provided in skill
- ❌ Assuming knowledge beyond training cutoff
- ❌ Assuming familiarity with domain-specific processes
- ❌ Assuming Claude can access external state/memory

**Over-Constraint:**
- ❌ So many rules that quality suffers (rule count > 20 is warning sign)
- ❌ Micro-managing phrasing instead of outcomes
- ❌ Restricting Claude's reasoning ability unnecessarily
- ❌ Specifying implementation details instead of desired results

**Under-Specification:**
- ❌ No examples for complex or novel tasks
- ❌ Missing error handling guidance
- ❌ No quality criteria defined
- ❌ Unclear edge case handling

---

### 4. Clarity and Structure Review

**Structural Issues:**
- ⚠️ No clear sections or organization (wall of text)
- ⚠️ Instructions scattered throughout instead of logically grouped
- ⚠️ Missing or unclear headers
- ⚠️ Poor information hierarchy (important stuff buried)
- ⚠️ Inconsistent formatting (switching between styles)

**Language Clarity:**
- ⚠️ Overly complex sentences (25+ words frequently)
- ⚠️ Passive voice where active is clearer
- ⚠️ Abstract concepts without concrete examples
- ⚠️ Technical jargon without definitions
- ⚠️ Pronouns with unclear antecedents

**Better Patterns:**
- ✅ Use imperative voice ("Create X" not "You should create X")
- ✅ One instruction per sentence when possible
- ✅ Concrete examples alongside abstract rules
- ✅ Consistent terminology throughout
- ✅ Clear section headers that preview content

---

### 5. Example Quality Assessment

**Poor Examples:**
- ❌ Examples that don't demonstrate the core pattern
- ❌ Overly simple examples that miss edge cases
- ❌ Examples without explanation of why they work
- ❌ Too many examples teaching the same thing
- ❌ Examples using outdated syntax or practices

**High-Quality Examples:**
- ✅ Show before/after or good/bad contrasts
- ✅ Include "why this works" explanations
- ✅ Cover common edge cases
- ✅ Demonstrate key patterns concisely
- ✅ Realistic scenarios (not toy problems)

**Example Count:**
- 0 examples: Usually needs at least 1-2 for complex tasks
- 1-3 examples: Usually optimal
- 4-6 examples: Carefully evaluate if all are necessary
- 7+ examples: Almost always contains redundancy

---

### 6. Special Pattern Checks

**Tool Usage Instructions:**
- ⚠️ Are tool-calling instructions actually necessary?
- ⚠️ Does skill over-specify when Claude should know?
- ⚠️ Are there instructions about tools Claude doesn't have access to?

**Meta-Instructions:**
- ⚠️ Instructions about "how to use this skill" (usually redundant with description)
- ⚠️ Explaining skill's purpose inside the skill (already in description)
- ⚠️ Documentation for documentation's sake

**Conditional Logic:**
- ⚠️ Complex if/then trees that Claude can reason about independently
- ⚠️ Edge case handling that duplicates Claude's reasoning
- ⚠️ Over-specified decision trees (trust Claude's judgment more)

---

## Output Format

Structure analysis results as follows:

### Skill Overview
- Name: [skill name]
- Estimated token count: [rough estimate]
- Overall assessment: [1-2 sentence summary]

### Critical Issues (Must Fix)
[List any critical problems that will prevent skill from working]

### High Priority Improvements
[List significant improvements that will materially help]

### Token Optimization Opportunities
[Specific sections/patterns that waste tokens with estimates]
- Section X: ~[N] tokens could be saved by [specific change]
- Pattern Y: ~[N] tokens wasted on [specific issue]

### Medium Priority Suggestions
[Helpful improvements that aren't urgent]

### Low Priority Polish
[Nice-to-haves that would marginally improve]

### Rewrite Suggestions
[For any section with critical issues, provide rewritten version]

**Before (X tokens):**
```
[original text]
```

**After (Y tokens, Z% reduction):**
```
[optimized text]
```

### Estimated Impact
- Total potential token savings: ~[N] tokens ([X]%)
- Clarity improvement: [Significant/Moderate/Minor]
- Trigger reliability: [Better/Same/Need testing]

---

## Analysis Process

1. **First Pass - Skim**
   - Get overall sense of skill purpose
   - Check description field first
   - Note structure and organization
   - Flag any obvious red flags

2. **Second Pass - Deep Dive**
   - Run through each checklist section systematically
   - Mark specific line numbers or sections with issues
   - Count approximate tokens in bloated sections
   - Identify patterns (don't just note individual issues)

3. **Third Pass - Synthesize**
   - Prioritize findings by severity and impact
   - Group related issues together
   - Prepare concrete rewrite examples for worst sections
   - Calculate potential savings

4. **Output Generation**
   - Start with most critical issues
   - Be specific (quote exact text, give line numbers)
   - Provide rewrites, not just criticism
   - Estimate token impacts
   - Balance criticism with recognition of what works well

---

## Key Principles

### Be Specific
❌ "The description could be better"
✅ "The description 'helps with tasks' is too vague. Suggest: 'Analyzes code quality metrics and suggests refactoring priorities for Python codebases'"

### Show Impact
❌ "This section is redundant"
✅ "Lines 45-78 repeat concepts from lines 12-23, wasting ~120 tokens (18% of skill)"

### Provide Solutions
❌ "This doesn't work"
✅ "This doesn't work because [reason]. Instead, try: [concrete rewrite]"

### Respect Intent
- Understand what the skill author was trying to achieve
- Preserve core functionality while optimizing
- Don't just delete - replace with better alternatives
- Acknowledge trade-offs in suggestions

### Context Matters
- A 2000-token skill for complex workflows may be appropriate
- A 2000-token skill for simple formatting is bloated
- Judge efficiency relative to task complexity
- Consider how frequently skill will be triggered

---

## Common Optimization Wins

### Quick Wins (Usually Save 20-40% Tokens)

**1. Remove Meta-Commentary**
Delete sections explaining the skill to Claude (Claude will read and understand)

**2. Condense Verbose Prose**
Replace paragraphs with bullet points, remove filler words

**3. Consolidate Examples**
Replace 5 similar examples with 2 contrasting examples

**4. Trust Claude's Reasoning**
Remove over-specified decision trees and edge case handling

**5. Simplify Structure**
Flatten unnecessary XML nesting, remove redundant headers

### Deep Optimizations (Can Save 40-60% Tokens)

**1. Rewrite Entire Sections**
Take bloated sections and rewrite from scratch focusing on clarity

**2. Remove Implicit Instructions**
Delete instructions about things Claude already knows how to do

**3. Consolidate Redundant Concepts**
Merge sections teaching the same pattern multiple ways

**4. Streamline Tool Instructions**
Trust Claude's tool-use abilities more, remove over-specification

**5. Clarify Over Adding**
Instead of adding more examples/explanation, clarify existing content

---

## Red Flags for Common Skill Issues

### "My skill isn't triggering"
**Check:**
1. Description too vague or generic?
2. Description doesn't mention key trigger words?
3. Skill scope overlaps too much with existing skills?
4. Trigger pattern requires exact phrasing user won't say?

### "My skill triggers too often"
**Check:**
1. Description too broad ("helps with writing")?
2. Missing scope boundaries or exclusions?
3. Generic trigger words that match many queries?
4. Need more specific domain terminology?

### "My skill gives inconsistent results"
**Check:**
1. Conflicting instructions?
2. Ambiguous success criteria?
3. Too many conditional branches?
4. Under-specified output requirements?

### "My skill seems slow"
**Check:**
1. Token count >2000? (high context load)
2. Requesting Claude read multiple large references?
3. Over-complicated reasoning chains?
4. Excessive examples or edge case handling?

---

## Reference Integration

This skill works alongside:
- **prompting-pattern-library**: Reference for patterns and anti-patterns
- **token-budget-advisor**: Assess if skill fits within token budgets
- **skill-creator**: Guidelines for building skills initially
- **learning-capture**: Identify patterns from analysis to capture

When analyzing prompts, reference the prompting-pattern-library for detailed pattern explanations. Focus this skill on active diagnosis and concrete suggestions.

---

## Limitations and Caveats

**What this skill can't do:**
- Guarantee a skill will trigger in all desired situations (triggering is complex)
- Test actual skill performance (requires real usage)
- Determine if skill logic is correct for domain (needs domain expertise)
- Predict user behavior or query patterns

**Best used for:**
- Identifying clear anti-patterns and inefficiencies
- Suggesting specific improvements with examples
- Estimating token costs and optimization potential
- Catching common failure modes before publication

**Remember:**
- Analysis is a starting point, not gospel
- Some verbose skills are appropriately complex
- User intent matters more than arbitrary token targets
- Test optimized versions to ensure they still work correctly
