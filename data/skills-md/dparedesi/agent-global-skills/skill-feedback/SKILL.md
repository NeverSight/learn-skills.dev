---
name: skill-feedback
description: Generate improvement reports for skills or CLI packages you authored. Use when ending a session where you worked on your own skill, when the user mentions "skill-feedback", "capture improvements", "session learnings", or when friction was observed during skill/package usage.
---
# Skill Feedback Generator

Generate structured improvement reports for skills or CLI packages based on session learnings.

**Why?** Valuable improvement opportunities emerge during sessions—user corrections, friction points, successful patterns—but they're lost unless explicitly captured. This skill systematically extracts and documents these learnings.

## Quick Start

1. Detect what skill/package was worked on → 2. Analyze session for friction & feedback → 3. Generate structured report → 4. Save report → 5. Offer to implement improvements

## When to Use

- At the end of any session where the user worked on a skill or package they authored
- When the user explicitly requests `/skill-feedback`
- When significant friction was observed during the session

### Decision Threshold

Generate a report when ANY of these conditions are met:
- **1+ user corrections** (explicit "don't do X", "you should have...")
- **3+ friction points** (repeated attempts, clarification loops, rejections)
- **User explicitly requests** feedback capture

> [!WARNING]
> Do NOT generate a report if the session was purely Q&A, informational, or had no actionable friction. A report with empty improvement sections wastes the user's time.

## Workflow

### 1. Identify What Was Worked On

Scan the session to determine what skill or package was the focus:


| Signal                                       | Interpretation                       |
| ---------------------------------------------- | -------------------------------------- |
| Files in`~/.claude/skills/*/` read/edited    | Global skill: extract name from path |
| Files in .claude/skills/*/` read/edited      | Local skill: extract name from path  |
| User says "my skill", "my CLI", "my package" | Explicit ownership confirmation      |
| Skill invoked via`/skill-name`               | That skill was used                  |

If multiple candidates, ask the user which to focus on.

### 2. Analyze the Session

Scan the conversation for each signal type using explicit detection patterns. Every signal must have evidence.

#### Signal Taxonomy

##### 1. User Correction

**Definition:** User explicitly negates, redirects, or overrides a prior agent action.

| Detection Pattern | Example |
|-------------------|---------|
| Negation + redirect | "No, I meant X" / "Not that, do Y instead" |
| Explicit disagreement | "That's wrong" / "That's not what I asked" |
| Undo request with reason | "Undo that, it broke X" |

**NOT a correction (false positives to avoid):**

| Pattern | Example | Why it's not a correction | Caveat |
|---------|---------|---------------------------|--------|
| Standalone directive | "Delete file X" | No prior action being negated | - |
| Clarification request | "What does this do?" | Information seeking, not correction | If the agent could have been clearer → capture as Missed Opportunity |
| Continuation | "Now do Y" | Sequential task, not override | If the agent could have anticipated this → capture as Missed Opportunity |

**Extract verbatim quotes** — these are gold for skill improvement.

> [!TIP]
> Verbatim quotes capture the user's exact mental model and language. Paraphrasing loses nuance and makes improvements less targeted.

##### 2. Workflow Friction

**Definition:** User manually performs work that the tool could/should automate.

| Detection Pattern | Example |
|-------------------|---------|
| Manual ID/path entry | User types `abc-123` when tool could infer it |
| Repeated context | User re-explains something already in conversation |
| Copy-paste from output | User copies value from tool output to feed back in |
| Multi-step manual workaround | User chains commands that could be one operation |

##### 3. Capability Gap

**Definition:** User requests functionality that doesn't exist or discovers a limitation.

| Detection Pattern | Example |
|-------------------|---------|
| Feature request | "Can you add X?" / "It would be nice if..." |
| Discovered limitation | "Why can't it do X?" / Tool responds "I can't do that" |
| Workaround needed | User does something manually because tool can't |

##### 4. Bug/Error

**Definition:** Tool produces incorrect output or fails unexpectedly.

| Detection Pattern | Example |
|-------------------|---------|
| Runtime error | CLI throws exception, stack trace |
| Wrong output | Tool edits wrong file, produces malformed output |
| Silent failure | Tool reports success but action didn't happen |

##### 5. Performance Issue

**Definition:** Tool is slow, resource-intensive, or inefficient.

| Detection Pattern | Example |
|-------------------|---------|
| Explicit complaint | "This is slow" / "Why does this take so long?" |
| Timeout/hang | Operation doesn't complete in reasonable time |
| Resource exhaustion | Out of memory, token limit hit |

##### 6. Missed Opportunity

**Definition:** Agent could have been smarter, clearer, or more proactive—even though the user didn't explicitly correct it.

This is a **second-pass analysis**: after ruling out "Correction," ask *"Could the skill have done better here?"*

| Detection Pattern | Example | What It Reveals |
|-------------------|---------|-----------------|
| User asks for clarification | "What does this do?" | Agent's output was unclear → improve prompts/explanations |
| User provides next step | "Now do Y" | Agent could have anticipated this → add to workflow logic |
| User re-states intent | "I meant for the whole project" | Agent interpreted too narrowly → improve intent parsing |
| User simplifies/rephrases | "Just do X" | Agent over-complicated → simplify default behavior |

**Key distinction from Correction:**
- Correction = user says "that's wrong, undo/redo"
- Missed Opportunity = user moves forward, but agent could have been better

**When to capture:** Only if the improvement is generalizable (can be encoded in the skill), not a one-off preference.

##### 7. Successful Patterns (What Worked)

- Workflows that completed smoothly
- User expressed satisfaction ("perfect", "exactly")
- Patterns worth codifying in the skill

#### Attribution Rules

Feedback must be attributed to the correct target:

| If the issue involves... | Attribute to |
|--------------------------|--------------|
| CLI behavior, installation, binary errors | **Package** |
| API/SDK behavior, library code | **Package** |
| Prompt wording, instruction clarity | **Skill** |
| Workflow logic, step ordering | **Skill** |
| Missing automation, friction | **Skill** (feature request) |
| Agent misunderstanding user intent | **Skill** |

**When unclear:** Note both possibilities. Don't force attribution.

### 3. Generate the Report

Use this structure:

~~~markdown
---
type: skill-feedback
skill: [skill-name]
date: YYYY-MM-DD
session: [Brief description of what was done]
status: pending
---
# Feedback Report: [Skill/Package Name]

## Summary

[1-2 sentences: What was the session about? What's the key takeaway?]

---

## Signals Detected

### User Corrections
[List each with: what was corrected, what the user wanted instead, root cause hypothesis]
- None detected / [specific corrections with verbatim quotes]

### Workflow Friction
[List each with: what manual work occurred, what automation could eliminate it]
- None detected / [specific friction points]

### Capability Gaps
[List each with: what was requested/missing, potential solution]
- None detected / [specific gaps]

### Bugs/Errors
[List each with: what failed, reproduction context]
- None detected / [specific bugs]

### Missed Opportunities
[List each with: what the user did, what the agent could have done better, generalizable improvement]
- None detected / [specific opportunities]

### Successful Patterns
[Patterns worth preserving or codifying]
- [Pattern that worked well]

---

## Recommended Improvements

### Package Improvements
[Improvements to CLI/API/binary - or "None identified"]
- [ ] **[Issue]**: [Description]
  - **Current behavior:** [What happens now]
  - **Proposed fix:** [What should happen]

### Skill Improvements
[Improvements to prompts/logic/workflow - or "None identified"]
- [ ] **[Issue]**: [Description]
  - **Current behavior:** [What happens now]
  - **Proposed fix:** [What should happen]

---

*Generated by /skill-feedback*
~~~

### 4. Save the Report

**Default location:** `~/.claude/skills/skill-feedback/.feedback/skill-feedback-{name}-{YYYYMMDD-HHMM}.md`

### 5. Offer Implementation

> [!CAUTION]
> Only offer implementation if you have time remaining in the session. If context is running low, just provide the path to the saved report.

After saving the report, ask:

> "I've saved the report to [path]. Would you like me to implement any of these improvements now? I can start with the Critical items."

If yes:

- Work through improvements systematically
- Mark each as complete in the report
- Save updated report with implementation status

---

## Status Tracking

Reports use YAML frontmatter and checkboxes to track implementation progress.

### Frontmatter Fields

| Field | Description |
|-------|-------------|
| `type` | Always `skill-feedback` |
| `skill` | Name of the skill/package the feedback is for |
| `date` | Session date (YYYY-MM-DD) |
| `session` | Brief description of what was done |
| `status` | `pending` / `in_progress` / `implemented` |

### Status Values

- **pending** — No items implemented yet
- **in_progress** — Some items implemented
- **completed** — All items done (will be auto-archived)

### Auto-Archiving

When you mark a report as `status: completed`, **immediately move it** to the `completed/` subfolder:

```bash
mv ~/.claude/skills/skill-feedback/.feedback/skill-feedback-{name}-{date}.md \
   ~/.claude/skills/skill-feedback/.feedback/completed/
```

This keeps the main `.feedback/` folder clean with only pending items.

### Updating Status

When implementing feedback items:

1. Toggle the improvement checkbox: `- [ ]` → `- [x]`
2. Update frontmatter status when appropriate:
   - First item done → change to `in_progress`
   - All items done → change to `implemented`

This allows agents to quickly check frontmatter to see if a report still has pending work.

---

## Examples

### Example 1: After an Inbox Triage Session

**Context:** User ran `/inbox-assistant`, agent was too passive, user corrected it twice.

**Report excerpt:**

```markdown
## User Corrections (Verbatim)

> "you didn't make a recommendation of what to do with the summary?"

> "Never suggest full deletion, specially if they are old emails"

## Recommended Improvements

### Critical
- **Agent too passive after summary**: Add post-summary recommendation logic
  - Current: Shows numbers, waits
  - Proposed: Always suggest ONE clear next action based on inbox state
```

### Example 2: After CLI Package Work

**Context:** User added new commands to `inboxd`, discovered missing `--account` flag handling.

**Report excerpt:**

```markdown
## Friction Points

| Step | What Happened | Friction? |
|------|---------------|-----------|
| 3 | Ran `inbox delete --ids "..."` | YES - CLI rejected: "Multiple accounts configured" |

## Recommended Improvements

### High Priority
- **Auto-resolve account from email ID**: CLI should look up which account an ID belongs to
  - Proposed: Add internal mapping or make `--account` optional when ID is unique
```

---

## Common Mistakes to Avoid

| Mistake | Why It's Wrong | What to Do Instead |
|---------|----------------|-------------------|
| Paraphrasing user quotes | Loses the user's exact words and intent | Copy-paste verbatim, even if grammar is imperfect |
| Generating empty reports | Wastes user time, implies problems exist | Skip report if no actionable friction |
| Mixing skill/package fixes | Confuses where to apply changes | Use separate sections, label each improvement |
| Vague improvements like "improve UX" | Not actionable | Be specific: "Add confirmation dialog before delete" |
| Ignoring successful patterns | Misses opportunity to codify what works | Always include "Patterns to Preserve" even if short |
| Forcing Critical priority | Inflation reduces trust in priorities | Use Critical only for blocking issues |

---

## Quality Rules

**Do:**
1. **Verbatim quotes are sacred** — Never paraphrase user corrections; use exact words
2. **Be specific, not vague** — "Add post-summary recommendations" not "improve UX"
3. **Categorize by priority** — Critical/High/Medium/Low based on impact and effort
4. **Distinguish skill vs package** — Clearly label which improvements go where
5. **Preserve what works** — Don't just focus on problems; capture successful patterns
6. **Offer implementation** — The report is useful, but acting on it is better

**Don't:**
- Generate reports for sessions with no friction (see Decision Threshold)
- Invent friction that wasn't observed just to have content
- Mark everything as Critical/High — use the full priority range
- Skip the TL;DR — it's the most-read section

---

## Report Validation Checklist

Before presenting the report, verify:

- [ ] **TL;DR is present** and summarizes key findings in 2-3 sentences
- [ ] **User quotes are verbatim** (copy-pasted, not paraphrased)
- [ ] **Each improvement is specific** (actionable, not vague)
- [ ] **Priorities are distributed** (not all Critical/High)
- [ ] **Skill vs Package is labeled** for each improvement
- [ ] **Successful patterns included** (even if brief)
- [ ] **No empty sections** (omit sections with nothing to report)
- [ ] **Date and session context filled in**

---

## Troubleshooting


| Problem                             | Solution                                                   |
| ------------------------------------- | ------------------------------------------------------------ |
| Can't determine what was worked on  | Ask the user directly                                      |
| No friction observed                | Focus on successful patterns; maybe the session was smooth |
| User doesn't want implementation    | Just save the report for future reference                  |
| Multiple skills/packages in session | Generate separate sections or ask user which to focus on   |

---

## Reference

- **[TESTING.md](./TESTING.md)** — Evaluation scenarios, model coverage, validation commands
