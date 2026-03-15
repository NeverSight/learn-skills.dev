---
name: fp-learn
description: Add a learning layer to FP project planning. Use when the user asks to "plan with learning goals", "learn while building", "fp-learn", "add learning to plan", or wants to track what they're learning during a project. Wraps around fp-plan/fp-implement/fp-review to classify tasks as DIY or delegate, track progress per phase, and generate quizzes.
---

# FP Learn — Learning-Augmented Project Management

This skill wraps around the FP workflow (fp-plan, fp-implement, fp-review) to turn project execution into deliberate learning. It classifies tasks as "do it yourself" (DIY) or "delegate to AI", tracks learning progress per phase, and generates quizzes after each phase completes.

## How It Works

FP Learn activates **after** fp-plan creates the initial task breakdown. It adds a learning layer on top:

1. **Learning Goal Setup** — Ask about goals, classify tasks, add title prefixes
2. **During Implementation** — Socratic hints for DIY tasks, normal execution for DELEGATE
3. **Phase Completion** — Reflection journal and conversation context summary
4. **Quiz** — 10-question quiz referencing actual project code

## Files Created in the Project Root

| File | When created | Purpose |
|------|-------------|---------|
| `learning-goals.md` | After goal setup | Stores 3-5 learning goals with skill levels |
| `progress-plan.md` | After plan phase | Phase journal: tasks, decisions, reflections |
| `progress-impl.md` | After impl phase | Phase journal: tasks, decisions, reflections |
| `progress-review.md` | After review phase | Phase journal: tasks, decisions, reflections |
| `quiz-phase-plan.md` | After plan quiz | 10 questions + answers + evaluation |
| `quiz-phase-impl.md` | After impl quiz | 10 questions + answers + evaluation |
| `quiz-phase-review.md` | After review quiz | 10 questions + answers + evaluation |

These files live in the project root, **not** inside `.fp/` (that directory is managed by FP).

## Task Labeling via Title Prefixes

FP has no native label field. Use **title prefixes** on issues:

- `[DIY: <goal-keyword>]` — user implements this to learn
- `[DELEGATE]` — repetitive/boilerplate, AI handles it

Apply via: `fp issue update --title "[DIY: Auth] Original title" FP-X`

These prefixes are visible in `fp tree` output, making classification immediately apparent.

---

## Stage 1: Learning Goal Setup

**Trigger**: Run this stage after fp-plan has created the task breakdown (issue hierarchy exists in FP).

### Step 1: Ask About Learning Goals

Use AskUserQuestion to gather 3-5 learning goals. Ask:

- "What do you want to learn or get better at during this project?"
- "For each goal, how would you rate your current level? (beginner / familiar / intermediate)"
- "What level do you want to reach? (familiar / intermediate / confident)"

Frame this as a quick setup step, not an interrogation. Users can answer conversationally.

### Step 2: Create learning-goals.md

Read the template from `assets/learning-goals.template.md`. Create `learning-goals.md` in the project root, populated with the user's goals.

### Step 3: Classify Tasks

Read `references/labeling-guide.md` for the full classification rules. For each task in the FP plan:

1. Check if it directly exercises a learning goal → `[DIY: <goal>]`
2. Check if it's boilerplate/repetitive → `[DELEGATE]`
3. If ambiguous, ask the user with a brief explanation of the trade-off

Apply the prefix to each task title:

```bash
fp issue update --title "[DIY: Auth] Implement OAuth callback handler" FP-3
fp issue update --title "[DELEGATE] Set up ESLint and Prettier config" FP-7
```

### Step 4: Write Issue Descriptions with Embedded Learning Goals

For each DIY task, write the issue **description** using the format below. The description combines the task instructions with dedicated learning goals, key insights, and a definition of done — so the issue is self-contained.

#### DIY Issue Description Format

```markdown
# <Task Title>

> **🎓 DO YOURSELF** - Learn <concept 1> and understand <concept 2>.

<Brief description of what this task accomplishes.>

## Steps
<Concrete implementation steps: commands, code snippets, config changes>

## Learning Goals
- <Specific thing the user will learn by doing this>
- <Another learning outcome>
- <Focus on the "why", not just the "what">

## Key Insight: <Title the core concept>
- <Explain the key architectural or conceptual insight>
- <Connect it to the broader system>
- <Show why this matters>

## Files to Create/Modify
- <file path> (new / modify)
- <file path> (new / modify)

## Definition of Done
- <Observable outcome 1>
- <Observable outcome 2>
- <What "working" looks like>
```

#### Example: DIY Issue

```markdown
# Install and Configure Keystatic

> **🎓 DO YOURSELF** - Learn how Astro integrations work and understand hybrid rendering mode.

Set up Keystatic in the Astro project.

## Steps
npm install @keystatic/core @keystatic/astro

### 1. Update astro.config.mjs
import keystatic from '@keystatic/astro';

export default defineConfig({
  integrations: [keystatic()],
  output: 'hybrid',  // Required for /admin route
});

### 2. Create keystatic.config.ts
Basic config with local storage mode.

### 3. Add admin route
Create src/pages/admin/[...params].astro

## Learning Goals
- Understand Astro integrations system
- Learn output modes (static vs hybrid vs server)
- Understand why /admin needs SSR (hybrid mode)

## Key Insight: Why Hybrid?
- Most pages: Static (pre-rendered HTML)
- /admin: Server-rendered (needs to run Keystatic)
- Hybrid mode: Choose per-route

## Files to Create/Modify
- astro.config.mjs
- keystatic.config.ts (new)
- src/pages/admin/[...params].astro (new)

## Definition of Done
- Keystatic installed
- Can visit /admin without errors
- See Keystatic UI (even if empty)
```

Apply the description when creating or updating the issue:

```bash
fp issue update --description "<description content>" FP-3
```

### Step 5: Show Summary

After classification, show the user a summary:

```
Learning goals: 3 set
DIY tasks: 5 (linked to goals)
DELEGATE tasks: 4
```

Run `fp tree` so the user can see the prefixed titles.

---

## Stage 2: During Implementation

This stage augments fp-implement behavior based on task type.

### For DIY Tasks

When the user picks up a DIY task:

1. **Remind them of the learning goal**: "This task is linked to your [goal] learning goal. You're practicing [concept]."

2. **Offer Socratic hints instead of solutions**: When the user asks for help on a DIY task, do NOT provide the implementation directly. Instead:
   - Ask a guiding question: "What do you think should happen when the token expires?"
   - Point to relevant docs or examples: "The OAuth2 spec describes this flow in section X. What approach makes sense for our case?"
   - Offer to explain a concept without writing the code: "I can explain how middleware chaining works, then you can implement it."

3. **Escalation path**: If the user is stuck after 2-3 Socratic exchanges, offer to:
   - Show a pseudocode outline (not full implementation)
   - Implement one part and let them do the rest
   - Pair-program: they describe what to write, you type it

4. **After completion**: Prompt a brief reflection (1-2 sentences):
   - "Now that you've finished, what was the trickiest part?"
   - "Anything you'd do differently next time?"

### For DELEGATE Tasks

Implement normally using fp-implement patterns. No special behavior needed.

### Progress Tracking

After each completed task (DIY or DELEGATE), append a row to the current phase's progress file. If `progress-{phase}.md` doesn't exist yet, create it from `assets/progress.template.md`.

---

## Stage 3: Phase Completion

**Trigger**: All tasks in the current phase are marked done in FP.

### Step 1: Confirm Phase Complete

Ask the user: "It looks like all [phase] tasks are done. Ready to wrap up this phase?"

### Step 2: Update Progress File

Finalize `progress-{phase}.md` with:
- Complete task table (all tasks with status and reflection)
- Conversation context section: summarize key decisions and discussions from the phase
- Set the completion date

### Step 3: Prompt Learning Reflection

Use AskUserQuestion to gather reflection. Ask these questions (user can answer conversationally):

1. "Which learning goals did you make progress on during this phase?"
2. "What concepts 'clicked' for you?"
3. "What's still fuzzy or needs more practice?"
4. "Rate your confidence on each goal now (beginner / familiar / intermediate / confident)"

Store the reflection in `progress-{phase}.md`.

### Step 4: Update Learning Goals

Update `learning-goals.md` with the new confidence ratings from the reflection.

---

## Stage 4: Quiz

**Trigger**: Immediately after phase reflection (Stage 3) completes.

### Step 1: Generate Questions

Read these files to generate quiz questions:
- `learning-goals.md` — what the user is trying to learn
- `progress-{phase}.md` — what they did and reflected on
- `references/quiz-generation-guide.md` — question design rules

Generate 10 questions following the guide:
- 5 types: conceptual, code-analysis, debugging, architecture, comparison
- Mix: 3 easy, 4 medium, 3 hard
- Every question must reference actual project code or decisions
- Weight toward goals where the user rated lower confidence

### Step 2: Write Quiz File

Create `quiz-phase-{phase}.md` from `assets/quiz-phase.template.md`. Fill in the questions (leave answer/evaluation/feedback blank).

### Step 3: Administer Quiz

Present questions one at a time using AskUserQuestion. For each question:

1. Show the question with its type and difficulty
2. Let the user answer freely (they select "Other" and type their answer)
3. Evaluate the answer: correct / partial / incorrect
4. Provide immediate feedback (what was good, what was missed, key takeaway)
5. Show running score: "Question 4/10 | Score: 2 correct, 1 partial"
6. Update the quiz file with the answer, evaluation, and feedback

### Step 4: Quiz Summary

After all 10 questions:

1. Complete the score summary tables in the quiz file
2. Update `progress-{phase}.md` with the quiz results section
3. Show the user their results:
   - Overall score
   - Strongest area
   - Area to revisit
   - Specific concepts to review

---

## Handling Edge Cases

### User Wants to Skip the Quiz
That's fine. Note in `progress-{phase}.md` that the quiz was skipped. The learning reflection still has value on its own.

### User Wants to Reclassify a Task
Use `fp issue update --title "[new prefix] title" FP-X` to change the label. Update `learning-goals.md` DIY task IDs accordingly.

### Mid-Project Goal Changes
The user can add or modify learning goals at any time. Update `learning-goals.md` and reclassify affected tasks.

### User Gets Frustrated with DIY
If a DIY task is taking too long, offer to reclassify it as DELEGATE. Learning should feel challenging but not demoralizing. Note the reclassification in the progress file.

### Only Some Phases Apply
Not every project has all three phases (plan/impl/review). Only create progress and quiz files for phases that actually occur.

---

## Resources

### references/
- **`labeling-guide.md`** — Read during Stage 1, Step 3 (task classification). Contains rules for DIY vs DELEGATE classification with examples.
- **`quiz-generation-guide.md`** — Read during Stage 4, Step 1 (quiz generation). Contains question types, difficulty distribution, and evaluation rubrics.

### assets/
- **`learning-goals.template.md`** — Template for the project's learning goals file.
- **`progress.template.md`** — Template for per-phase progress journals.
- **`quiz-phase.template.md`** — Template for phase quiz files.
