---
name: generate-judge-contest
description: Use when asked to generate an Exercode/Judge contest (Exercode/Judgeのコンテスト) and its problem set. Not for use outside Exercode/Judge.
---

# Generate a judge contest

Read [references/contest-format.md](references/contest-format.md) before authoring any file.

1. Confirm the contest parameters: contest id and name, target course and lecture, divisions (each with open/close datetimes), which concepts the contest covers, the number of problems (4-6 is typical), and target programming language(s). The contest belongs at `<courseId>/<lectureId>/<contestId>.contest.yaml`, and its problems belong under the same course's `problems/` directory. If any are missing, ask before generating when the user is available; otherwise choose reasonable values from the context and list them as open decisions in the final report.
2. Plan the problem set as drafts (id, name, overview, difficulty, score):
   - Use only concepts the learners have already studied in the covered materials.
   - Span difficulties from 初級 to harder levels so every participant can solve something and strong participants stay challenged; order problems from easy to hard.
   - Assign scores increasing with difficulty (e.g. 100, 200, 300, ...).
3. Generate each problem directory by following the [generate-judge-problems](../generate-judge-problems/SKILL.md) skill workflow (model answer first, run it to produce `.out` files unless the custom judge does not compare stdout, cross-check with a second language, validate).
4. Write `<contestId>.contest.yaml` per [references/contest-format.md](references/contest-format.md), listing every division and every problem with its score. Place the file inside the lecture directory when the contest belongs to a course.
5. Validate with the `exercode-problem` CLI (it ships with `@exercode/problem-utils`, which must be a declared repository dependency — see [setup-exercode-course-repository](../setup-exercode-course-repository/SKILL.md)) and fix until clean; rerun after every fix until both commands report success:

   ```bash
   bunx exercode-problem validate-problem <problemDir>...
   bunx exercode-problem validate-contest <contestYamlPath> --problems-dir <problemsDir>
   ```

   Address warnings too unless they are intentional; if you keep a warning, tell the user why in the final report.

6. Report the contest yaml path, the problem list with scores and difficulties, and any open decisions (e.g. datetimes or scores you chose, intentionally kept warnings).
