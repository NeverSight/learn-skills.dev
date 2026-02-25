---
name: exam-curriculum-trainer
description: "Build and run exam-focused study systems for technical courses with lecture notes, exercises, and past exams. Use when a project contains mock exams, previous exams, exercise sheets, or lecture slides and the user wants: (1) a curriculum in the same structure as their SCML-style setup, (2) strong weighting toward previous exams and exercises over theory, and (3) strict interactive practice sessions with no-hint-first attempts, grading, weak-tag tracking, and retake loops."
---

# Exam Curriculum Trainer

Use this skill to create or update an exam-prep workflow in any project that contains course materials.

## Announce And Scope

Start by stating you are using `exam-curriculum-trainer` and that the goal is exam performance, not broad theory coverage.

Collect only the minimum required inventory:
- Curriculum or study-plan files already present.
- Previous/mock exams and exercise sheets (highest priority sources).
- Lecture notes/slides (secondary gap-filling source).

Prefer fast file discovery commands.

## Priority Policy

Apply this weighting in all outputs:
1. Previous exams and mock exams.
2. Exercise/problem sheets and solved tasks.
3. Lecture theory, only when needed to support exam-style solving.

Do not produce long theory digressions.

## Create Curriculum File

Create a `CURRICULUM.md` (or update existing one) with the structure in `references/curriculum_structure.md`.

Hard requirements:
- Keep ASCII only.
- Include explicit training rules: no hints on first attempt, strict grading, weak-tag tracking, retake until 2 consecutive correct answers per weak tag.
- Include a question bank mapped to source material IDs.
- Include a fixed multi-session sequence and retake policy.
- Include a session script with step-by-step runtime behavior.
- Include concise formula sheet and pitfalls list.

If an existing curriculum already follows a strong structure, preserve it and patch gaps instead of rewriting blindly.

## Build Exam-Style Question Bank

Extract and normalize questions from prioritized sources.

Rules for question writing:
- Prefer exam-style prompts with explicit deliverables.
- Keep each question atomic and gradable.
- Add point values and weak-tag mapping.
- Add near-variant follow-ups for remediation.
- Include timed mixed sets after topical blocks.

When source questions are sparse, generate adjacent variants in the same style and notation.

## Run Interactive Sessions

When user says to start a session:
1. Load the configured session range from `CURRICULUM.md`.
2. Ask one question at a time in strict mode.
3. Grade each answer immediately: Correct/Partial/Wrong with points and short reason.
4. If wrong/partial, provide corrected solution and one near-variant follow-up.
5. Update weak tags inline and track streak-to-mastery.
6. Continue automatically until session set completes or user pauses.

Session behavior requirements:
- No hints on first attempt.
- If user requests help, apply hint ladder (light -> medium -> strong).
- Keep notation consistent with curriculum formulas.
- Keep answers concise and terminal-readable ASCII.

Use `references/session_runner.md` for exact runtime protocol.

## Output Standards

Use this response order when reporting session progress:
1. Question result and score.
2. Minimal correction.
3. Weak-tag update.
4. Next question.

At session end provide:
- Total score.
- Wrong/partial IDs.
- Weak-tag status.
- Required retake set.
- 60-second recall prompt (3 formulas, 2 pitfalls, 1 anchor).

## File Update Rules

When creating assets in a new project, generate only what is needed:
- `CURRICULUM.md` mandatory.
- `EXAM_SIM_1.md` and `EXAM_SIM_2.md` optional but recommended for timed full runs.
- Do not create extra docs outside study workflow unless asked.

## Adaptation Rules For New Courses

Keep structure stable but adapt content:
- Rename topic blocks to match the course.
- Preserve fixed sequence concept from fundamentals -> advanced -> timed exams.
- Preserve mastery gating and retake loops.
- Preserve exam-first source weighting.

If user gives a different emphasis, follow user preference while retaining strict grading and interactive practice defaults.
