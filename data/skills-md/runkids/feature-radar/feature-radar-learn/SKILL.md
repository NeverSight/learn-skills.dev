---
name: feature-radar-learn
description: |
  Extract reusable patterns, architectural decisions, and pitfalls from completed work
  into .feature-radar/specs/. Captures the "why" behind choices so future sessions build
  on past experience. MUST use this skill when the user reflects on what worked/didn't,
  wants to document a decision, or mentions remembering a pattern for future use.
  Use when the user:
  - Says "remember this approach", "document this decision", "save this pattern"
  - Reflects: "that worked well", "lessons learned", "what did we learn"
  - Wants to capture: "don't forget this", "this was a good pattern"
  - Hit a dead end: "this didn't work because...", "avoid this approach"
  - Made a technical decision worth recording for posterity
  - Says "extract learnings" or "capture what we learned"
  Do NOT use for recording external observations — that's feature-radar-ref's job.
  Do NOT use for archiving completed features — that's feature-radar-archive's job.
---

# Extract Learnings

Capture reusable knowledge from completed work into `.feature-radar/specs/`.

## Deep Read

<HARD-GATE>
Read and follow `../feature-radar/references/DEEP-READ.md` — complete all 6 steps before proceeding.
</HARD-GATE>

## Behavioral Directives

<HARD-GATE>
Read and follow `../feature-radar/references/DIRECTIVES.md`.
</HARD-GATE>

## Workflow

1. **Identify the source** — ask the user what was just completed (feature, bug fix, refactor, investigation)
2. **Analyze the work** — review recent commits, changed files, and implementation decisions
3. **Extract knowledge** — identify what's reusable:
   - **Patterns**: recurring solutions worth replicating (e.g., "three-tier config merge")
   - **Decisions**: architectural choices with rationale (e.g., "YAML over JSON because...")
   - **Pitfalls**: mistakes or dead ends others should avoid
   - **Techniques**: implementation approaches that worked well
<HARD-GATE>
Before writing to specs/, classify each piece of knowledge into exactly one category:
- **Pattern**: recurring solution worth replicating
- **Decision**: architectural choice with rationale
- **Pitfall**: mistake or dead end to avoid
- **Technique**: implementation approach that worked well

State the classification explicitly in your output.
</HARD-GATE>

4. **Write to specs** — create or append to `.feature-radar/specs/{topic}.md`
5. **Checkpoint** — State what was written and ask: "I've written to `specs/{topic}.md` ({classification type}). Does this look correct, or should I adjust anything?" Wait for user confirmation before proceeding.
6. **Update base.md** — increment the specs count in Tracking Summary

## File Format

Use the format defined in `../feature-radar/references/SPEC.md` § 3.4 (`specs/{topic}.md`).

## Guidelines

- One topic per file. If the learning spans multiple topics, create multiple files.
- Name files by the pattern, not by the feature that produced it.
  - Good: `yaml-config-merge.md`, `symlink-vs-copy-tradeoffs.md`
  - Bad: `audit-feature-learnings.md`, `v2-refactor-notes.md`
- Append to existing files when the new learning extends a known topic.
- Keep it concise — future readers need the insight, not the full story.

## Example Output

```
→ Created specs/symlink-vs-copy-tradeoffs.md (Decision)
→ Updated base.md: specs 2 → 3
```

## Completion Summary

Follow the template in `../feature-radar/references/DIRECTIVES.md`, with skill name "Learn Complete".
