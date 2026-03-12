---
name: feature-radar-ref
description: |
  Record external observations, ecosystem trends, and creative inspiration into
  .feature-radar/references/. MUST use this skill when the user mentions something
  interesting from outside their project — other tools, articles, approaches, or trends.
  Even casual mentions like "I saw a cool thing in X" should trigger this skill.
  Use when the user:
  - Says "I saw this cool thing in X's API", "check out how X handles this"
  - Shares a URL, article, talk, or research finding with relevant insights
  - Notes an ecosystem trend: new tools, standards, community patterns
  - Mentions a related project shipping a notable feature
  - Wants to bookmark external inspiration: "interesting approach", "save this"
  - Says "add reference", "log observation", "track this project"
  Do NOT use for internal learnings/patterns — that's feature-radar-learn's job.
  Do NOT use for prioritizing features — that's feature-radar's job.
---

# Add Reference

Record external observations into `.feature-radar/references/`.

## Deep Read

<HARD-GATE>
Read and follow `../feature-radar/references/DEEP-READ.md` — complete all 6 steps before proceeding.
</HARD-GATE>

## Behavioral Directives

<HARD-GATE>
Read and follow `../feature-radar/references/DIRECTIVES.md`.
</HARD-GATE>

## Workflow

1. **Identify the source** — ask the user what they observed:
   - Interesting project, technique, or creative approach?
   - Ecosystem trend or emerging pattern?
   - Notable feature or solution from a related project?
   - User comparison, feedback, or question?
   - Research, article, or talk with relevant insights?
2. **Gather context** — URL, date, key details. If the user provides a GitHub URL, fetch the issue/PR for full context.
3. **Classify** — determine the right file:
   - Existing reference file → append a new entry
   - New topic → create `.feature-radar/references/{topic}.md`
4. **Assess impact**:

<HARD-GATE>
Before writing to references/, assess impact by answering ALL of these:
- New opportunity or feature idea? → state yes/no, suggest file if yes
- Way to enhance existing features? → state yes/no, suggest update if yes
- Ecosystem trend? → state yes/no, suggest specs/ecosystem-trends.md update if yes
</HARD-GATE>
5. **Checkpoint** — State what was written and the impact assessment results. Ask: "I've updated `references/{topic}.md`. Does this look correct, or should I adjust anything?" Wait for user confirmation before proceeding.
6. **Update base.md** — increment the references count in Tracking Summary

## File Format

Use the format defined in `../feature-radar/references/SPEC.md` § 3.5 (`references/{topic}.md`).

## Naming Convention

Name by the subject being tracked, not the event:

- Good: `vercel-skills-ecosystem.md`, `agent-path-conventions.md`, `cli-ux-patterns.md`
- Bad: `2026-02-18-update.md`, `interesting-finding.md`

## Guidelines

- Always cite source URLs and dates for traceability.
- Append new entries chronologically to existing files — don't create a new file per observation.
- Be objective. Record what happened, then assess implications separately.
- If the observation reveals an unmet need or innovation opportunity, proactively suggest creating an opportunity.
- Look for creative inspiration, not just feature gaps — how others solve problems can spark new ideas.

## Example Output

```
→ Appended to references/cli-ux-patterns.md
→ Suggested: new opportunity "interactive config wizard"
→ Updated base.md: references 3 → 3 (appended, not new file)
```

## Completion Summary

Follow the template in `../feature-radar/references/DIRECTIVES.md`, with skill name "Ref Complete".
