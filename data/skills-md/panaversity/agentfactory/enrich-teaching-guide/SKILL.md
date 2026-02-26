---
name: enrich-teaching-guide
description: "Enrich lesson frontmatter with teaching_guide metadata that helps teachers deliver content effectively. Reads previous lesson for progression context. Works on a single lesson, a full chapter, multiple chapters, or N specific lessons. Use when preparing lessons for teachers, adding pedagogical guidance, or enriching frontmatter with key_points, misconceptions, discussion_prompts, teaching_tips, and assessment_quick_check."
---

# Enrich Teaching Guide

Generate `teaching_guide` YAML frontmatter blocks that give teachers what they need to confidently deliver a lesson: what to emphasize, where students stumble, what to discuss, and how to check understanding.

## Quality Bar

This metadata is read by real teachers. Every field must pass this test:

> "Would an experienced educator read this and think: yes, this is genuinely useful — not obvious, not generic?"

**Good**: "Students confuse General Agents with ChatGPT-style chatbots — emphasize the action-taking (agentic) difference"
**Bad**: "Students may find this topic challenging"

**Good**: "Start with the ChatGPT copy-paste pain point — every student has experienced this"
**Bad**: "Begin with an engaging introduction"

## Invocation

```
/enrich-teaching-guide ch 3              # All lessons in chapter 3
/enrich-teaching-guide ch 3 lesson 1     # Single lesson
/enrich-teaching-guide ch 3 lessons 1-5  # Range within chapter
/enrich-teaching-guide ch 1,3,5          # Multiple chapters
/enrich-teaching-guide <path>            # Direct lesson path
```

## Process

### Step 1: Resolve Scope

Parse the user's input to determine which lessons to process.

```bash
# For "ch 3" — discover chapter path:
ls -d apps/learn-app/docs/*/03-*/

# List lesson files (exclude README, summary, quiz):
ls apps/learn-app/docs/<part>/<chapter>/*.md | grep -v README | grep -v summary | grep -v quiz
```

Build an ordered list of lessons to process. **Process sequentially** — each lesson needs the previous one as context.

### Step 2: For Each Lesson — Gather Context

For lesson N, read these files **in this order**:

1. **Lesson N-1** (previous lesson) — read FULL content
   - Purpose: understand what students already know, what vocabulary is established, what concepts are fresh
   - If N=1, skip — note "this is the chapter opener"

2. **Lesson N** (target) — read FULL content + all existing frontmatter
   - Purpose: deep understanding of what this lesson teaches
   - Note which frontmatter fields already exist vs missing

3. **Lesson N+1** (next lesson) — read ONLY the title and first 2 headings
   - Purpose: know where the lesson arc is heading (for "this leads into..." tips)
   - If last lesson, skip — note "this is the chapter closer"

**DO NOT read the chapter README.** The value is in actual lesson content, not chapter metadata.

### Step 3: Analyze the Lesson

Before generating, answer these questions internally:

**For key_points:**

> "If a teacher has 2 minutes to prep, what 3 things must they know about THIS lesson?"

Look for:

- Concepts that are **foundational** (used again later in the chapter or book)
- **Pivotal distinctions** the lesson makes (X vs Y comparisons)
- **Non-obvious connections** to prior lessons ("this builds on the OODA loop from lesson 1")

**For misconceptions:**

> "Where will students confidently get it WRONG?"

Look for:

- Terms that sound familiar but mean something specific here
- Concepts that seem similar but are fundamentally different
- Assumptions students bring from other tools/contexts
- The lesson's own "this is NOT..." warnings

**For discussion_prompts:**

> "What question would make a student STOP and think for 30 seconds?"

Look for:

- Questions that connect lesson content to the student's own experience
- "What if..." counterfactuals that test understanding
- Questions with no single right answer (genuine discussion, not recall)

**For teaching_tips:**

> "What would a veteran teacher of this lesson whisper to a first-time instructor?"

Look for:

- The best entry point (which example/scenario to start with)
- Live demo opportunities
- Whiteboard-worthy diagrams or tables in the lesson
- Pacing advice ("spend more time on X, students breeze through Y")

**For assessment_quick_check:**

> "In 60 seconds at the end of the lesson, how can a teacher know if students got it?"

Look for:

- "Explain X in one sentence" checks for core concepts
- "Draw/diagram Y from memory" for frameworks/processes
- "What's the difference between A and B?" for key distinctions

### Step 4: Generate the YAML Block

Generate a `teaching_guide` block matching this exact schema:

```yaml
teaching_guide:
  lesson_type: "core" # core | supplementary | hands-on | capstone
  session_group: 1 # Which session/class this belongs to (integer)
  session_title: "Session Name" # Human-readable session grouping
  key_points:
    - "Point with specific detail, not generic advice"
    - "Reference to where concept recurs: 'used again in Ch X, lesson Y'"
    - "Maximum 4 points — if you need more, the lesson is too dense"
  misconceptions:
    - "Specific misconception — what students think vs what's true"
    - "Maximum 4 — focus on the dangerous ones"
  discussion_prompts:
    - "Open-ended question connecting to student experience?"
    - "Counterfactual or 'what if' that tests understanding?"
    - "Maximum 3 — quality over quantity"
  teaching_tips:
    - "Specific, actionable advice with lesson reference"
    - "Maximum 4 tips"
  assessment_quick_check:
    - "Quick check that takes <30 seconds per student"
    - "Maximum 3 checks"
```

**Constraints:**

- `lesson_type`: Infer from content — `core` (teaches new concepts), `supplementary` (extends/enriches), `hands-on` (primarily exercises), `capstone` (integrates multiple concepts)
- `session_group`: Infer from lesson position. Lessons 1-3 → session 1, 4-6 → session 2, etc. Adjust based on natural breakpoints.
- Every string must be a single line (no multiline YAML strings)
- No generic advice. Every point must reference specific lesson content.
- Use quotes consistently for all string values.

### Step 5: Inject or Present

**If processing 1-3 lessons**: Present the generated YAML for review before injecting.

**If processing 4+ lessons (batch mode)**: Inject directly into each lesson's frontmatter, placing the `teaching_guide` block after the `differentiation` block (or at the end of frontmatter if `differentiation` doesn't exist).

**Injection rules:**

- If `teaching_guide` already exists: **SKIP** unless user passed `--force`
- Preserve all existing frontmatter — only ADD the `teaching_guide` block
- Maintain YAML indentation (2 spaces)

### Step 6: Report

After processing, output a summary:

```
ENRICHMENT COMPLETE
──────────────────
Lessons processed: X
Lessons skipped (already enriched): Y
Lessons enriched: Z

Files modified:
  ✓ apps/learn-app/docs/.../01-lesson.md
  ✓ apps/learn-app/docs/.../02-lesson.md
  ⊘ apps/learn-app/docs/.../03-lesson.md (already has teaching_guide)
```

## Anti-Patterns

| Don't                                     | Do Instead                                                                                          |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------- |
| "Students may struggle with this concept" | "Students confuse X with Y because [specific reason]"                                               |
| "Start with an engaging introduction"     | "Start with the ChatGPT copy-paste pain point — every student has experienced this"                 |
| "This is an important topic"              | "OODA loop is foundational — referenced again in Chapters 5, 11, and 13"                            |
| "Ask students what they learned"          | "Ask students to explain passive vs agentic AI in one sentence"                                     |
| "Demo the concepts"                       | "Demo the OODA loop live: show Claude reading a file, deciding what to do, acting, then correcting" |
| Generic tips that fit any lesson          | Tips that reference THIS lesson's specific examples, tables, or code                                |

## Handling Edge Cases

- **Lesson has no learning_objectives**: Generate `teaching_guide` anyway — the lesson content is sufficient input
- **First lesson in chapter**: Note "chapter opener" — tips should include "set expectations for the chapter arc"
- **Last lesson in chapter**: Note "chapter closer" — tips should include "connect back to chapter themes"
- **Very short lesson** (<500 words): May only need 2 key_points, 1-2 misconceptions
- **Hands-on/exercise lesson**: Focus `teaching_tips` on facilitation; `assessment_quick_check` on output verification

## Reference: High-Quality Example

From Chapter 3, Lesson 1 (`01-origin-story.md`):

```yaml
teaching_guide:
  lesson_type: "core"
  session_group: 1
  session_title: "Getting Started with Claude Code"
  key_points:
    - "OODA loop is foundational — referenced again in Chapters 5, 11, and 13"
    - "Product Overhang explains why capability existed before the product — this mental model recurs throughout the book"
    - "General Agent vs Custom Agent distinction is the entire thesis of the book"
  misconceptions:
    - "Students confuse General Agents with ChatGPT-style chatbots — emphasize the action-taking (agentic) difference"
    - "Students think 'agentic' means 'smarter' rather than 'can take actions on files and systems'"
    - "Students assume Claude Code requires coding skills — Cowork section addresses this"
  discussion_prompts:
    - "What would change in your daily work if AI could see your actual files instead of you describing them?"
    - "Can you think of other 'product overhangs' in technology — capabilities that existed but needed a better interface?"
    - "Why do you think adoption hit 50% in 5 days internally at Anthropic?"
  teaching_tips:
    - "Start with the ChatGPT copy-paste pain point — every student has experienced this"
    - "Demo the OODA loop live: show Claude reading a file, deciding what to do, acting, then correcting"
    - "The General Agent vs Custom Agent table is a good whiteboard moment"
  assessment_quick_check:
    - "Ask students to explain passive vs agentic AI in one sentence"
    - "Have students draw the OODA loop from memory"
```

Notice: every point is specific to this lesson. No generic teaching advice. A teacher reading this for the first time can immediately use it.
