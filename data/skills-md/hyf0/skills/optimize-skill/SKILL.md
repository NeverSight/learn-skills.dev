---
name: optimize-skill
description: Analyzes and optimizes an existing agent skill for conciseness, discoverability, and adherence to best practices. Use when a skill needs improvement, is too verbose, has poor activation rates, or fails to follow progressive disclosure patterns. Do NOT use for creating a new skill from scratch — use create-skill instead.
license: MIT
metadata:
  author: github.com/hyf0
  version: "1.0.0"
---

## Workflow

Follow these 5 steps in order. Copy this checklist into your response and check off each step as you complete it:

```
Task Progress:
- [ ] Step 1: Read the target skill
- [ ] Step 2: Run the quality checklist
- [ ] Step 3: Identify optimization opportunities
- [ ] Step 4: Apply optimizations
- [ ] Step 5: Validate improvements
```

### Step 1: Read the Target Skill

Read the target skill's SKILL.md and all files in its `reference/` directory (if any).

Collect these metrics:
- Total line count of SKILL.md
- Total line count across all reference files
- Frontmatter fields present vs. missing
- Number of reference files and whether all are linked from SKILL.md

Report these metrics to the user before proceeding.

### Step 2: Run the Quality Checklist

Score each item in the quality checklist as PASS, FAIL, or N/A:
-> See [quality-checklist](reference/quality-checklist.md)

Present the full scorecard to the user before making any changes. Ask for confirmation to proceed with optimizations.

### Step 3: Identify Optimization Opportunities

Review all FAIL items from the checklist. Prioritize by impact (highest first):

1. **Description quality** — Most common cause of skill not being invoked. Fix first.
2. **Content compression** — Remove knowledge the agent already has. Reduces token cost and noise.
3. **Progressive disclosure** — Split oversized SKILL.md into reference files, or merge tiny reference files back.
4. **Structure clarity** — Improve headers, cross-references, and flow. Numbered steps for workflows.
5. **Consistency** — Fix terminology, formatting, and style inconsistencies.
6. **Triggering precision** — Under-triggering: add keywords, trigger phrases, concrete use cases. Over-triggering: add negative triggers ("Do NOT use for X"), narrow the scope.

List each optimization opportunity with:
- What is wrong
- Why it matters
- What the fix will be

### Step 4: Apply Optimizations

For each issue identified in Step 3, apply the fix. Use compression techniques where applicable:
-> See [compression-techniques](reference/compression-techniques.md)

For each change, briefly explain what changed and why in your response (one line per change is sufficient).

### Step 5: Validate Improvements

After applying all optimizations:

- [ ] Re-run the quality checklist — all previously FAIL items should now PASS
- [ ] Verify SKILL.md is under 500 lines
- [ ] Verify no content was lost — all original capabilities are preserved
- [ ] Read the final SKILL.md end-to-end for coherence
- [ ] Verify all reference file links resolve to existing files
- [ ] **Triggering test:** Ask yourself "When would you use the [skill-name] skill?" — verify the description clearly communicates the skill's purpose and trigger conditions

Report the before/after metrics:
- Line count: before -> after
- Checklist score: X/Y PASS -> X/Y PASS
- Key improvements made

## Output

Deliver the optimized skill files to the user with a summary of all changes made and their rationale.
