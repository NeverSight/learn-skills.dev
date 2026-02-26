---
name: skill-debugging-assistant
description: Debug, diagnose, and troubleshoot skill issues including trigger failures, parameter problems, prompt conflicts, and SKILL.md structural issues. Use when skills don't activate as expected, trigger incorrectly, produce unexpected behavior, conflict with system instructions, or fail packaging validation. Analyzes YAML frontmatter, descriptions, progressive disclosure, token budget, absolute statements, and reference file organization. For skill creators reviewing, validating, or fixing skill problems.
---

# Skill Debugging Assistant

## Overview

This skill helps diagnose why skills aren't triggering or performing as expected. It systematically analyzes trigger patterns, parameter issues, prompt conflicts, and structural problems to identify root causes and recommend fixes.

## When to Use This Skill

Use this skill when encountering any of these issues:

- Skill doesn't trigger when expected
- Skill triggers incorrectly or at wrong times
- Skill behavior doesn't match description
- Conflicts between skill instructions and system prompts
- Unclear when to load references vs. include in SKILL.md
- Validation errors during packaging
- Skill works inconsistently across similar queries

## Diagnostic Workflow

Follow this decision tree to diagnose skill issues:

### 1. Identify the Problem Type

**Skill not triggering?** → Go to "Trigger Failure Diagnostics"

**Skill triggering incorrectly?** → Go to "False Positive Diagnostics"

**Skill behavior unexpected?** → Go to "Instruction Conflict Diagnostics"

**Packaging/validation errors?** → Go to "Structure Validation"

**General review needed?** → Go to "Comprehensive Audit"

### 2. Trigger Failure Diagnostics

When a skill should trigger but doesn't, analyze in this order:

**Step 1: Analyze the description field**
- Read the skill's frontmatter `description`
- Check if description mentions the user's query terms or conceptual triggers
- Verify description includes WHEN to use the skill, not just WHAT it does
- Confirm description is specific enough to differentiate from other skills

**Step 2: Check description quality**
- Does it include key terms the user would naturally use?
- Does it specify triggers (file types, tasks, scenarios)?
- Is it comprehensive enough for selection among 100+ skills?
- Are the trigger scenarios clear and unambiguous?

**Step 3: Review competing skills**
- Identify other skills with overlapping descriptions
- Determine if another skill's description better matches the query
- Check if trigger patterns are too similar between skills

**Step 4: Test edge cases**
- Would the skill trigger for paraphrased versions of the query?
- Does it cover related terminology and synonyms?
- Are there implicit assumptions about when it should trigger?

**Common fixes:**
- Add specific trigger terms to description
- Include file type indicators (.docx, .pdf, .json)
- Specify task types (create, edit, analyze, debug)
- Add domain indicators (finance, legal, technical)
- Include synonym terms users might naturally use

### 3. False Positive Diagnostics

When a skill triggers when it shouldn't:

**Step 1: Check description over-breadth**
- Is the description too general?
- Does it use broad terms that match many queries?
- Are there missing qualifiers or constraints?

**Step 2: Review instruction conflicts**
- Do instructions apply too broadly within SKILL.md?
- Are there "always" or "never" statements that override context?
- Does the skill assume it should handle something beyond its scope?

**Common fixes:**
- Narrow description scope with specific qualifiers
- Add exclusion indicators (e.g., "not for X")
- Move broad utility functions to scripts rather than main workflow
- Add conditional logic: "Only when..." or "If and only if..."

### 4. Instruction Conflict Diagnostics

When skill behavior contradicts expected results:

**Step 1: Read SKILL.md completely**
- Check for absolute statements (always, never, must, required)
- Identify instructions that might conflict with system prompt
- Look for contradictory instructions within the skill

**Step 2: Analyze instruction priority**
- Are there competing instructions without clear precedence?
- Do examples contradict written rules?
- Is the desired behavior stated clearly vs. implied?

**Step 3: Check progressive disclosure structure**
- Is critical information buried in references that weren't loaded?
- Should certain instructions be in SKILL.md instead of references?
- Are references clearly indicated when they're needed?

**Common fixes:**
- Replace absolutes with conditionals
- Add explicit precedence rules
- Move critical instructions from references to SKILL.md
- Clarify when to load each reference file
- Use "Prefer X, unless Y" instead of "Always X"

### 5. Structure Validation

Run automated and manual checks:

**Automated validation:**
```bash
python3 scripts/validate_skill.py path/to/skill-folder
```

**Manual checks:**
- YAML frontmatter properly formatted (name and description present)
- Name follows kebab-case convention
- Description is comprehensive (>50 chars) and specific
- SKILL.md under 500 lines (split to references if needed)
- References clearly indicated in SKILL.md when needed
- No extraneous files (README.md, CHANGELOG.md, etc.)
- Assets/scripts tested and functional

**Common structural issues:**
- Missing or malformed YAML frontmatter
- Description too vague or too brief
- SKILL.md exceeds token budget (>500 lines)
- References not mentioned in SKILL.md
- Unused example files not deleted
- Scripts with syntax errors or missing dependencies

### 6. Comprehensive Audit

For general skill review or quality improvement:

**Trigger analysis:**
1. List 5-10 queries that should trigger this skill
2. For each query, verify the description contains relevant terms
3. Test paraphrased versions of each query
4. Identify gaps in trigger coverage

**Instruction clarity:**
1. Read SKILL.md start to finish
2. Flag any ambiguous or conflicting statements
3. Verify examples align with instructions
4. Check if workflow steps are clear and sequential

**Progressive disclosure:**
1. Ensure SKILL.md contains only essential procedural knowledge
2. Verify detailed reference material is in separate files
3. Confirm references are clearly indicated when needed
4. Check that SKILL.md describes when to load each reference

**Quality checklist:**
- [ ] Description includes specific trigger terms and scenarios
- [ ] SKILL.md uses imperative/infinitive form throughout
- [ ] No conflicting instructions or absolute statements without qualifiers
- [ ] Examples provided for non-obvious operations
- [ ] References clearly indicated and purposefully separated
- [ ] Scripts tested and functional
- [ ] Token budget respected (<500 lines in SKILL.md)
- [ ] No extraneous files included

## Quick Diagnostics Checklist

For rapid troubleshooting, check these common issues first:

**Trigger failures (skill not activating):**
- [ ] Description mentions user's query terms
- [ ] Description includes "when to use" indicators
- [ ] Description differentiates from similar skills
- [ ] Key terms are specific, not generic

**False positives (skill triggers incorrectly):**
- [ ] Description isn't too broad or generic
- [ ] No absolute statements without context limits
- [ ] Scope clearly defined with boundaries

**Behavior issues (skill does unexpected things):**
- [ ] No conflicting "always/never" statements
- [ ] Critical instructions in SKILL.md, not buried in references
- [ ] Examples align with stated rules
- [ ] Conditional logic uses "prefer" vs "always"

**Validation errors:**
- [ ] YAML frontmatter properly formatted
- [ ] Name uses kebab-case
- [ ] Description >50 characters
- [ ] No extraneous documentation files

## Deep Analysis Methods

### Description Analysis Template

For any skill with trigger issues, analyze the description systematically:

```markdown
**Current description:**
[paste description here]

**Analysis:**
1. Specificity: Does it include concrete trigger terms?
2. Differentiation: How does it differ from similar skills?
3. Completeness: Does it mention when/how to use it?
4. Key terms: List the main terms that would trigger selection

**Test queries:**
[List 5 queries that should trigger this skill]
[For each, note if description contains matching terms]

**Recommended improvements:**
[Specific additions or changes to description]
```

### Instruction Conflict Analysis

For skills with behavioral issues:

1. Extract all imperative statements from SKILL.md
2. Flag statements using: always, never, must, required, CRITICAL, NEVER
3. Check each flagged statement for potential conflicts
4. Identify statements that could override user intent
5. Recommend conditional rephrasing

### Token Budget Analysis

For skills approaching context limits:

1. Count lines in SKILL.md (target: <500 lines)
2. Identify sections >100 lines that could move to references
3. Check for repetitive examples or verbose explanations
4. Verify references are actually being used (not duplicated in SKILL.md)
5. Recommend splits: what stays in SKILL.md vs. what moves to references

## Resources

### references/common-issues.md

Detailed examples of common skill problems with before/after fixes. Load this when debugging complex or recurring issues.

### scripts/validate_skill.py

Automated validation script that checks:
- YAML frontmatter format and completeness
- File structure and naming conventions
- Description quality metrics
- Common structural problems

Run before packaging any skill to catch issues early.
