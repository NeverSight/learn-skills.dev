---
name: analyze-skill
description: Analyze usage data for a specific skill and suggest improvements to its triggers and prompt. Identify usage patterns, missed triggers, and areas for SKILL.md improvement.
argument-hint: "[skill-name]"
---

# analyze-skill

Analyze the usage of a specified skill and output improvement suggestions for its SKILL.md triggers and prompt.

## Arguments

- `skill-name` (required): The name of the skill to analyze (e.g., `example-skill`, `review-pr`)

If no argument is provided, ask the user for the skill name.

## Execution Steps

### Step 1: Retrieve Usage Data

Execute the following command using the Bash tool and capture the output:

```bash
bunx cc-skills-usage@0.1.1 --conversations --skill <skill-name>
```

The output includes the following data:
- **Skill Stats**: Number of invocations
- **Daily Stats**: Daily usage counts
- **Project Stats**: Per-project usage counts
- **Token Stats**: Token consumption
- **Recent Calls**: Recent invocations (with triggerMessage)
- **Conversation Stats**: Skill usage rate across all sessions
- **Recent Conversations**: User messages from sessions where the skill was not used

### Step 2: Read Skill Definition

Use the Read tool to read `~/.claude/skills/<skill-name>/SKILL.md`. If the file is not found, use Glob to search under `~/.claude/skills/` to locate the skill directory.

### Step 3: Analysis

Perform analysis from the following perspectives:

#### 3a. Analysis of When the Skill Was Used
- Categorize user messages that triggered the skill from the `triggerMessage` field in Recent Calls
- Extract frequently used keywords and phrases

#### 3b. Analysis of When the Skill Was NOT Used
- Review sessions where the skill was not used (`hasSkillCalls: false` or the target skill is not in `skillsUsed`)
- Examine `userMessages` from those sessions to find cases where the skill could have been applicable
- Identify missed trigger patterns

#### 3c. Usage Frequency and Trend Analysis
- Review usage frequency trends from `dailyStats`
- Identify which projects use the skill most from `projectStats`

#### 3d. Adoption Rate Analysis
- From `conversationStats`:
  - Percentage of sessions that used the skill out of total sessions
  - Per-project adoption rate

### Step 4: Output Improvement Suggestions

Output the analysis results in the following format:

```
## Skill Analysis Report: <skill-name>

### Current Usage
- Total invocations: X
- Session usage rate: X% (Y/Z sessions)
- Primary projects: ...
- Usage trend: (increasing/stable/decreasing)

### When the Skill Was Used
- Pattern 1: Messages like "..." (X times)
- Pattern 2: Messages like "..." (Y times)
- ...

### Missed Opportunities
- User message "..." did not trigger the skill (session: ...)
- ...

### Improvement Suggestions

#### Add Trigger Keywords
Based on message patterns not currently captured by the SKILL.md, the following trigger keywords are suggested:
- `keyword1` — Reason: ...
- `keyword2` — Reason: ...

#### Improve Description
Current: "..."
Suggested: "..."
Reason: ...

#### Improve Prompt (SKILL.md Body)
- Improvement 1: ...
- Improvement 2: ...
```

## Notes

- If data is limited (e.g., fewer than 5 invocations), state this explicitly and analyze as much as possible.
- If the skill has never been used, provide improvement suggestions based solely on the SKILL.md content.
- Suggestions must be specific and actionable. Avoid abstract advice.
