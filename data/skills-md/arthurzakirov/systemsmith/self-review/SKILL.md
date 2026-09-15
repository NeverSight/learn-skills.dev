---
name: self-review
description: Analyze the current conversation or mine historical chat sessions for correction patterns, wrong conclusions, or unnecessary user intervention. Use when the user wants to improve prompts, skills, workflows, or guardrails based on repeated mistakes.
user-invocable: true
---

# Self Review

If `$ARGUMENTS` is empty or non-numeric, analyze the current conversation. If it is a number, treat it as a request to mine that many days of historical sessions.

## Current Conversation Mode

For each mistake, capture:

1. What the assistant concluded
2. What the actual answer turned out to be
3. What information was missing
4. Whether that information was discoverable
5. What concrete change would prevent the same mistake

Output shape:

```markdown
### Mistake: <what went wrong>
**Assistant said:** "<quoted claim>"
**Actual answer:** "<what turned out to be true>"
**Missing info:** <missing context>
**Findable?** YES / NO
**Fix:** <skill, prompt, hook, data-source, or workflow change>
```

After listing mistakes, propose concrete edits and ask the user which to implement.

## Historical Mode

### Step 1: Pre-Filter

Use a mining script or equivalent search only as a pre-filter to find candidate sessions.

Skip frozen or retry-only sessions caused by infrastructure issues rather than assistant behavior.

### Step 2: Deep Read

Read flagged sessions message by message. For each user intervention, ask whether the assistant could have already done that without being told.

### Step 3: Choose The Right Fix Mechanism

Map the failure to the right control surface:

| Mechanism | Best for |
| --- | --- |
| `CLAUDE.md` or equivalent global instruction | Universal behavior rules |
| Path-scoped rules | File-type-specific behavior |
| Skills | Situational knowledge |
| Memory | Persistent decisions or preferences |
| Hooks | Automated guardrails that must always run |
| Agents | Isolated delegated task types |
| Commands | Explicitly user-invoked prompts |
| Settings | Permissions, env vars, model config |

Decision heuristic:

- "Assistant keeps forgetting X" -> Hook or always-loaded rule
- "Assistant should do X when editing Y" -> Path-scoped rule
- "Assistant lacks knowledge about X during Y" -> Skill
- "Assistant should delegate X" -> Agent plus routing rule
- "I want to run X on demand" -> Command
- "Remember this decision" -> Memory

### Step 4: Present Findings With Examples

Every pattern must include concrete examples from transcripts. Do not present regex counts as findings.

For each pattern include:

- What happens
- Two or three concrete examples
- Proposed fix: bucket, file, specific edit, and why it helps

### Step 5: Validate Against User Experience

Check with the user that the proposed pattern matches real experience before editing prompts or skills.
