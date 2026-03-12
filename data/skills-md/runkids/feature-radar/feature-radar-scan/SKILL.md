---
name: feature-radar-scan
description: |
  Discover new feature opportunities from creative brainstorming, user feedback, ecosystem
  trends, and cross-project research. Writes results to .feature-radar/opportunities/.
  MUST use this skill when the user wants to GENERATE new ideas — not evaluate existing ones.
  Trigger on any request to brainstorm, explore, discover, or find new feature ideas, even
  casual ones like "I wonder what else we could do" or "give me ideas".
  Use when the user:
  - Asks "what else could we build?", "give me feature ideas", "what are we missing?"
  - Wants to brainstorm, explore new directions, or refresh the opportunity backlog
  - Says "scan ecosystem", "scan opportunities", "find new features"
  - Asks to review GitHub issues, community feedback, or adjacent tools for inspiration
  - Mentions "explore", "discover", or "new directions" in a feature context
  - Has a vague idea: "I have an idea", "what if we...", "I was thinking about..."
  Do NOT use for evaluating/prioritizing existing features — that's feature-radar's job.
---

# Scan Opportunities

Discover new feature opportunities and add them to `.feature-radar/opportunities/`.

## Deep Read

<HARD-GATE>
Read and follow `../feature-radar/references/DEEP-READ.md` — complete all 6 steps before proceeding.
</HARD-GATE>

## Behavioral Directives

<HARD-GATE>
Read and follow `../feature-radar/references/DIRECTIVES.md`.

Additional directive for this skill:
- **Filter aggressively** — Do NOT create opportunity files for weak signals. If you can't cite concrete demand evidence, skip it.
</HARD-GATE>

## Brainstorm Intake

<HARD-GATE>
Evaluate whether the user arrived with a vague or exploratory idea.

Enter Brainstorm Intake if ANY of these are true:
- User says "I have an idea", "what if we...", "I was thinking about...", "brainstorm"
- User describes a problem without a clear feature shape
- User's input lacks specific demand signals, impact/effort estimates, or a concrete feature name

Skip Brainstorm Intake if ALL of these are true:
- User gave a specific directive like "scan opportunities", "scan ecosystem", "find new features"
- User's input does not contain a personal idea or vague exploration

If skipping, jump directly to ## Workflow.
</HARD-GATE>

### Phase 1: Core Questions

Ask these one at a time. Prefer multiple-choice when possible.

1. **Problem space** — "What problem are you trying to solve, or what experience do you want to improve?"
   - Cross-reference: search existing `opportunities/` and `archive/` for related themes.
   - If a match is found, surface it: "Is this related to #{nn} {title}, or a completely different direction?"
2. **Target user** — "Who would benefit from this feature?"
   - Offer choices derived from `base.md` Project Context if available.
3. **Spark** — "What triggered this idea?"
   - (A) A pain point from my own usage
   - (B) Saw a similar feature in another tool/project
   - (C) New technical possibilities (new API, new library)
   - (D) Community/user feedback
   - (E) Pure creative exploration

### Phase 2: Adaptive Depth

After Phase 1, assess idea maturity:

**Mature** (has clear problem + user + demand signal):
→ Ask 1 closing question to confirm scope, then proceed to Exit.

**Emerging** (has problem but fuzzy shape):
→ Ask up to 3 more questions to sharpen:
  - "What does the usage look like in your mind?"
  - "Have you seen an implementation you particularly liked?" (if yes, consider creating a `references/` entry)
  - "What's the minimum scope that would feel useful?" (MVP scoping)

**Raw** (pure exploration, no clear problem yet):
→ Switch to open-ended dialogue. Ask up to 5 more questions:
  - Explore adjacent possibilities
  - Challenge assumptions: "If we don't build this, what's the biggest loss?"
  - Seek demand signals: "Has anyone (including yourself) run into this problem repeatedly?"
  - Stop when: a clear feature shape emerges, OR user says "enough"

### Exit: Output Options

Summarize the refined idea:

"Here's a summary of our discussion:
- **Problem:** {problem}
- **Target user:** {target user}
- **Direction:** {feature shape}
- **Demand signal:** {demand evidence or 'creative exploration'}
- **Related items:** {related opportunities/archive/specs, or 'none found'}"

Then ask:

"What would you like to do next?"
- **(A) Proceed to scan** — use this direction as focused context, search all 6 sources for supporting evidence and related opportunities
- **(B) Save as opportunity draft** — write to `opportunities/{nn}-{slug}.md` with Status: Open, decide later whether to scan

If (A): Pass the summary as context into ## Workflow Step 1, with a narrowed focus on the identified direction.
If (B): Create the opportunity file following `../feature-radar/references/SPEC.md` § 3.3, populate fields from the intake summary, then run the Annotation Checkpoint per `../feature-radar/references/WORKFLOW-PATTERNS.md`. After approval, present Completion Summary and suggest "run a focused scan around this direction" as a next step.

## Workflow

1. **Identify sources** — where to look for ideas:
   - **User signals**: issues, discussions, forum posts, support requests
   - **Creative exploration**: "what if we..." brainstorming, combining existing features in new ways
   - **Ecosystem evolution**: adjacent tools, emerging standards, new capabilities in dependencies
   - **Technical possibilities**: new APIs, libraries, or techniques that enable things previously impossible
   - **Cross-project research**: interesting approaches from related projects (from base.md Inspiration Sources)
   - **Community conversations**: Reddit, HN, Discord, blog posts
   - **If Brainstorm Intake was completed**: use the intake summary as the primary focus direction. Prioritize sources most relevant to the identified problem space. Still scan all 6 source types, but weight results toward the intake direction.
2. **Scan and collect** — for each source, look for:
   - Unmet user needs and recurring pain points
   - Feature ideas with demand signals (upvotes, comments, multiple independent asks)
   - Creative approaches that could enhance existing functionality
   - Technical breakthroughs that unlock new possibilities
   - Patterns emerging across multiple tools
3. **Deduplicate** — check against existing `opportunities/` and `archive/` files
4. **Cross-reference codebase** — for each candidate, search the project to check:
   - Already partially implemented? → mark as "Partially Done"
   - Does existing architecture support this? → note in "Design Notes"
   - Related TODOs or FIXMEs in the code? → cite them
5. **Evaluate each candidate**:

<HARD-GATE>
Before creating any opportunity file, evaluate the candidate against ALL 6 criteria.
Each criterion must be explicitly addressed — do not skip any.
</HARD-GATE>

| Criterion | Question |
|-----------|----------|
| **Real user demand** | Are users actually asking for this, or does it solve a latent need? |
| **Value uplift** | Does this meaningfully improve the user experience or unlock new possibilities? |
| **Innovation potential** | Does this introduce a creative breakthrough or unique approach? |
| **Effort / impact ratio** | Is the cost justified by the benefit? |
| **Architectural fit** | Does it align with our core philosophy? |
| **Ecosystem timing** | Is the ecosystem ready? |

6. **Create opportunity files** — for each viable candidate, write `.feature-radar/opportunities/{nn}-{slug}.md`
7. **Checkpoint — Review & Annotate** per `../feature-radar/references/WORKFLOW-PATTERNS.md`

Present scan results using this format:

```
Scan complete: {n} new opportunities
| # | Opportunity | Demand Signal | Impact | Effort | Source |
|---|------------|---------------|--------|--------|--------|
| {nn} | {title} | {evidence} | H/M/L | H/M/L | {where found} |
```

8. **Update base.md** — increment opportunities count, update Value & Innovation Landscape if needed

## Opportunity File Format

Use the format defined in `../feature-radar/references/SPEC.md` § 3.3 (`opportunities/{nn}-{slug}.md`).

## Guidelines

- Don't create opportunities for every idea you find. Filter aggressively — weak signal wastes attention.
- 1 issue with no comments = weak signal. Multiple independent asks = strong signal.
- Creative ideas without existing demand can still be valid — evaluate innovation potential separately.
- Write an honest "Our Position" — it's OK to say "we don't want this" or "not yet."
- Number sequentially from the highest existing number in `opportunities/` and `archive/`.
- If scanning reveals problems others have that we've already solved, add to `references/` instead.

## Example Output

```
→ Created opportunities/07-streaming-output.md (Impact: High, Effort: Medium)
→ Skipped: "hook system" already exists as opportunities/03-hook-system.md
→ Updated base.md: opportunities 6 → 7
```

### Brainstorm Intake Example

```
User: "I was thinking... what if we could automatically detect when a feature is getting stale?"

Phase 1:
  Q1 (Problem): "What problem are you trying to solve?" → Feature opportunities sitting unreviewed
  Cross-ref: Found #05 role-assignment — user confirms: different direction
  Q2 (Target): "Who benefits?" → Project maintainers managing backlogs
  Q3 (Spark): (A) Pain point from own usage

Phase 2 (Emerging → 2 follow-ups):
  Q4: "What does usage look like?" → Periodic check, flag items older than N days with no activity
  Q5: "Minimum useful scope?" → Just a reminder in completion summary, no automation needed

Exit summary:
  Problem: Stale opportunities go unnoticed
  Target user: Project maintainers
  Direction: Staleness detection in completion summaries
  Demand signal: Personal pain point (single user)
  Related: None found

User chose: (B) Save as opportunity draft
→ Created opportunities/06-staleness-detection.md (Impact: Low, Effort: Low)
→ Suggested next step: "run a focused scan around staleness detection"
```

## Completion Summary

Follow the template in `../feature-radar/references/DIRECTIVES.md`, with skill name "Scan Complete".
