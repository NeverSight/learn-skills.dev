---
name: skill-creator-plus
description: Use when creating, testing, and iterating Agent skills with validation. Extends skill-creator with dual validation modes.
---

# Skill Creator Plus

## Overview

Extends the official `skill-creator` skill by adding **Dual Validation Modes** and **Automated Iteration** capabilities.

**Core Capabilities**:

- Reuse official `skill-creator` for initial skill creation
- Dual Validation Modes: RED-GREEN testing + Example-based validation
- Automated iteration and optimization (up to 3 times)
- Overfitting prevention mechanism (Training/Testing split)

## Workflow

### Step 1: Create Skill

**Use the official `skill-creator` skill directly to complete the creation process (Step 1-4).**

Refer to the first 4 steps of the official documentation:

1. Understanding the Skill with Concrete Examples
2. Planning the Reusable Skill Contents
3. Initializing the Skill
4. Edit the Skill

> [!NOTE]
> **Do not use the official Step 5 (Packaging) and Step 6 (Iterate)**:
>
> - Step 5 (Packaging) will be completed in skill-creator-plus Step 4 (after validation and iteration).
> - Step 6 (Iterate) will be completed in skill-creator-plus Step 3 (automated iteration).

After creation is complete, proceed directly to Step 2 Validation Phase. The format specification validation for `SKILL.md` will be automatically executed during packaging in Step 4.

### Step 2: Validation

**Select Validation Mode**:

1. Ask the user for their preferred validation method.
2. If the user does not specify, infer automatically based on the Skill type:
   - Discipline/Rule-based → Mode A (RED-GREEN)
   - Output Quality-based → Mode B (Example-based)

---

#### Mode A: RED-GREEN Testing (Discipline Skills)

Suitable for "Must Do / Must Not Do" rule-based Skills.

**Examples**: `always-confirm-before-delete`, `test-driven-development`, `verification-before-completion`

**RED Phase - Baseline Test**

1. Design a pressure scenario based on the Skill's purpose.
   - The scenario should simulate "errors the Agent would make without this Skill".
   - Include triggers like time pressure, sunk costs of completed work, etc.
2. Dispatch a specific sub-agent to execute the scenario (**without loading the Skill**).
   ```
   Task("Execute pressure scenario, do not load the skill created by skill-creator-plus")
   ```
3. Record the sub-agent's error behavior and "rationalization/excuses".

**GREEN Phase - Skill Test**

1. Dispatch a sub-agent to execute the same scenario (**loading the Skill**).
   ```
   Task("Execute pressure scenario, load the skill created by skill-creator-plus")
   ```
2. Verify if the sub-agent adheres to the Skill rules.
3. Judgment:
   - ✅ Pass → Proceed to Step 4 (Save).
   - ❌ Fail → Proceed to Step 3 (Iterate).

---

#### Mode B: Example-Based Validation (Output Quality Skills)

Suitable for "Format Optimization / Content Rewriting" quality-based Skills.

**Examples**: `proposal-markdown-formatter`, `code-style-unifier`, `document-translator`

**Preparation Phase**

1. User provides 3-5 example pairs (Input Document → Standard Output Document).
2. Split into:
   - **Training Set** (2-3 pairs): Used for iterating and improving the Skill.
   - **Test Set** (1-2 pairs): Used for final validation to prevent overfitting.

**Training Iteration**

1. Dispatch an execution sub-agent to process the training set input (loading the Skill).
   ```
   Task("Use Skill to process input document: [Training Set Input 1]")
   ```
2. Dispatch a review sub-agent to compare the output with the standard answer.

   ```
   Task("Review output quality by comparing the following two documents:
   - Agent Output: [...]
   - Standard Answer: [...]

   Review Dimensions:
   1. Structural Similarity (heading levels, paragraphs, list formats)
   2. Key Content (retention or conversion of keywords/phrases)
   3. Style Consistency (tone, wording)

   Provide a comprehensive score and improvement suggestions.")
   ```

3. If there is a significant gap → Proceed to Step 3 (Iterate).

**Final Validation (Overfitting Prevention)**

1. Validate using the test set (examples the sub-agent has never seen).
2. Review sub-agent judges the generalization ability.
3. Judgment:
   - ✅ Pass → Proceed to Step 4 (Save).
   - ❌ Fail → Report to user (Skill may need redesign).

---

### Step 3: Iteration (REFACTOR)

1. Analyze the reasons for sub-agent failure:
   - Mode A: Record specific "excuses" and rationalizations.
   - Mode B: Analyze improvement suggestions from the review sub-agent.
2. Add targeted clauses in `SKILL.md`:
   - Mode A: Add explicitly prohibited excuses to the "Rationalization Prevention" table.
   - Mode B: Supplement missing rules or examples.
3. Re-execute validation.
4. **Maximum 3 iterations**. If it still fails, report to the user and request assistance.

**Iteration Counter**:

```
Iteration 1 → Fail → Modify → Iteration 2 → Fail → Modify → Iteration 3 → Fail → Report to User
```

---

### Step 4: Packaging and Saving

**Package Skill**:

After validation and iteration are complete, call the packaging script in the `skill-creator` skill:

1. Locate `scripts/package_skill.py` in the `skill-creator` skill.
2. Run the packaging script, passing in the created Skill directory path.
3. The script will automatically perform the following operations:
   - Call `quick_validate.py` to validate Skill format.
   - Create a `.skill` file (zip format, containing all files).
   - Maintain directory structure for distribution.

If validation fails, the script will report errors and exit. Fix the errors and re-run packaging.

**Save Location**:

- **Default**: `.claude/skills/<skill-name>/` (Project level)
- **Optional**: Ask user if they want to export to user-level directory `~/.claude/skills/<skill-name>/`

**Save Content**:

- `SKILL.md` (Required)
- `scripts/` (If applicable)
- `references/` (If applicable)
- `assets/` (If applicable)

---

## Validation Mode Guide

| Skill Type            | Validation Mode | Examples                                                              |
| --------------------- | --------------- | --------------------------------------------------------------------- |
| Discipline/Rule-based | RED-GREEN       | TDD, Delete Confirmation, Code Review Process                         |
| Output Quality-based  | Example-Based   | Markdown Formatting, Document Style, Code Refactoring Patterns        |
| Hybrid                | Combined        | First RED-GREEN to verify rules, then Example-Based to verify quality |

---

## FAQ

**Q: How do I determine which type my Skill belongs to?**

A: Ask yourself:

- Does this Skill require the Agent to "Must Do / Must Not Do" something? → Discipline type, use RED-GREEN.
- Does this Skill require the Agent to "output consistent with a certain quality standard"? → Quality type, use Example-Based validation.

**Q: What if it still fails after 3 iterations?**

A: Report to the user. Possible reasons:

- The Skill design itself is flawed (needs brainstorming again).
- Pressure scenarios are unreasonable.
- Example quality is poor or quantity is insufficient.

**Q: Can I use both validation modes simultaneously?**

A: Yes! For hybrid Skills, first use RED-GREEN to verify rule compliance, then use Example-Based validation to verify output quality.

---

## Platform Limitations

> [!NOTE]
> This skill relies on sub-agent dispatch functionality and is limited to tools that support this feature, such as **Claude Code**, **OpenCode**, etc.
