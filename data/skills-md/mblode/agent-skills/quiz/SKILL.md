---
name: quiz
description: Generates interactive codebase quizzes to test understanding of architecture, patterns, and implementation details. Configurable by card count (fewer, standard, more) and difficulty (easy, medium, hard). Use when asked to quiz me, test my knowledge, create flashcards, generate codebase questions, or run a code quiz.
---

# Quiz

Generate interactive quizzes about the current codebase to test understanding.

## Reference Files

| File | Read When |
|------|-----------|
| `references/question-templates.md` | Default: question types by difficulty with concrete examples |
| `references/difficulty-calibration.md` | Applying difficulty and quantity settings, exploration depth, question stems |
| `references/scoring-and-output.md` | Step 5: scoring rubric, result formatting, final output template |

## Configuration

Collect from the user (ask only what was not provided):

### Number of Cards

| Option | Cards | Best for |
|--------|-------|----------|
| Fewer | 5 | Quick check, focused review |
| Standard | 10 | Balanced coverage |
| More | 15 | Deep dive, comprehensive review |

Default: **Standard (10)**

### Difficulty

| Level | Format | Question style |
|-------|--------|---------------|
| Easy | Multiple choice | What does X do? Where is Y defined? |
| Medium | Multiple choice + explanation | How does X interact with Y? What pattern is used for Z? |
| Hard | Open-ended + explanation | What would break if X changed? How would you refactor Y? |

Default: **Medium**

## Workflow

Copy this checklist to track progress:

```text
Quiz progress:
- [ ] Step 1: Gather configuration
- [ ] Step 2: Explore the codebase
- [ ] Step 3: Generate questions
- [ ] Step 4: Present quiz interactively
- [ ] Step 5: Score and summarize
```

### Step 1: Gather configuration

Ask the user for card count and difficulty. Use defaults if not specified. Accept informal phrasing ("give me a hard quiz", "just 5 questions").

If the user provides both values upfront, skip straight to Step 2.

### Step 2: Explore the codebase

Systematically scan the project to build a question pool:

- Read the project structure (directories, key files, entry points)
- Identify the primary language(s), framework(s), and tooling
- Read key files: configuration, entry points, core modules, tests
- Map dependencies and module boundaries
- Note patterns: naming conventions, architecture style, error handling
- Find non-obvious details: edge cases, workarounds, gotchas

Load `references/difficulty-calibration.md` for exploration depth and question strategy per level.

### Step 3: Generate questions

Using `references/question-templates.md`, generate the configured number of questions at the selected difficulty. Apply calibration from `references/difficulty-calibration.md`.

Each question must:
- Reference real code from the current codebase (file paths, function names, patterns)
- Have one clear correct answer
- Be answerable from the codebase alone (no external knowledge required)
- Cover different parts of the codebase (avoid clustering)

For multiple-choice questions, provide 4 options (A, B, C, D) with plausible distractors drawn from real names in the project.

For medium and hard questions, prepare a brief explanation to show after the user answers.

Check every question against the quality checklist below. Remove or rewrite any that fail.

### Step 4: Present quiz interactively

Present one question at a time. For each question:

1. Show the question number and total as a header (e.g., "Question 3/10")
2. For multiple choice (easy/medium): use `AskUserQuestion` with the question text and 4 options so the user can select an answer interactively
3. For open-ended (hard): show the question text and wait for a free-text response
4. After the user responds, show whether the answer was correct
5. Show the explanation with file:line references (medium and hard only)
6. Proceed to the next question

### Step 5: Score and summarize

Load `references/scoring-and-output.md` for the result template.

After all questions are answered, present the final scorecard with score, rating, breakdown by area, and recommended next steps.

## Quality Checklist

Every question must pass all of these:

- [ ] **Codebase-grounded** — References a real file path, function, or pattern from the current project
- [ ] **Single focus** — Tests one concept. If you need "and" to describe it, split it.
- [ ] **Unambiguous** — Has exactly one correct answer. No trick questions.
- [ ] **Self-contained** — Answerable from the codebase alone, no external knowledge required
- [ ] **Plausible distractors** — Multiple-choice options use real names from the project, not random strings
- [ ] **Spread coverage** — Questions cover different files and areas, no clustering
- [ ] **Difficulty-matched** — Matches the cognitive level of the selected difficulty
- [ ] **No generated files** — Never asks about lock files, node_modules, or build output
- [ ] **Explanation ready** — Medium and hard questions have a prepared explanation with file:line references

## Anti-patterns

- Do not ask questions about external libraries or frameworks (only the project's own code)
- Do not ask questions that require running the code to answer
- Do not reveal all questions at once (present one at a time, wait for response)
- Do not skip the explanation on wrong answers (the quiz is for learning)
- Do not ask trick questions or ambiguous questions with multiple valid answers
- Do not repeat questions about the same file or function
- Do not generate questions before exploring the codebase (Step 2 must complete first)

## Related Skills

- `plan-feature` for understanding codebase architecture before quizzing
- `review-pr` for code review exercises on recent changes
