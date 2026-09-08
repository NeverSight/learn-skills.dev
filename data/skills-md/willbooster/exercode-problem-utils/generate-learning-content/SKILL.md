---
name: generate-learning-content
description: Use when generating or improving Exercode learning content (Exercodeの学習コンテンツ - course materials, Judge problems, or contests). Not for use outside Exercode/Judge.
---

# Generate or improve exercode learning content

1. Inspect the requested outcome, repository instructions, and existing learning-content layout. When the user is unavailable (e.g. in an automated workflow), make reasonable decisions from the available context instead of pausing for confirmation; the confirmation steps of the workflows below then fall back to the same rule.
2. If the repository is not prepared for Exercode course authoring, follow [setup-exercode-course-repository](../setup-exercode-course-repository/SKILL.md) before authoring.
3. Follow every applicable authoring workflow:
   - [generate-course-materials](../generate-course-materials/SKILL.md) for courses, lecture texts, and embedded questions.
   - [generate-judge-problems](../generate-judge-problems/SKILL.md) for judge v2 problems.
   - [generate-judge-contest](../generate-judge-contest/SKILL.md) for contests and their problem sets.

   Treat both course-material and Judge-problem workflows as applicable when writing, modifying, or executing code is part of the course's learning objective. Do not treat embedded questions or complete code examples as substitutes for graded coding practice.

4. Run the validation and evaluation required by every applicable workflow and fix failures until clean.
5. For each generated or changed judge problem, run every model answer through the `exercode-problem` CLI when `@exercode/problem-utils` is available: from the problem directory, `bunx exercode-problem judge model_answers/<languageId>` (it applies the problem's own `judge.ts` when present and the standard stdio judge otherwise; see [generate-judge-problems/references/problem-format.md](../generate-judge-problems/references/problem-format.md)). Confirm the command exits 0, prints at least one `TEST_CASE_RESULT` line, and every printed line has the accepted decision code `2000`; `bunx exercode-problem <problemsDir>` checks all problems' model answers at once, but runs them without harness params and therefore fails parameterized problems — exclude those with `--skip <substring>` and judge them individually. Judge each starter template too and confirm it does not pass every test case.
6. Report the generated or changed paths, validation and evaluation performed, assumptions made, and intentionally retained warnings.
