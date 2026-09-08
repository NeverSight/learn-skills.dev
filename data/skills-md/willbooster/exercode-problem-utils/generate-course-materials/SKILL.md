---
name: generate-course-materials
description: Use when asked to generate Exercode course materials (Exercodeの教材) such as lectures, textbooks, or embedded quizzes. Not for use outside Exercode/Judge.
---

# Generate exercode course materials

Read these references before authoring any file:

- [references/course-format.md](references/course-format.md) — course directory layout, `course.yaml`, and material frontmatter schemas.
- [references/material-authoring.md](references/material-authoring.md) — pedagogical writing rules for lecture materials.
- [references/question-authoring.md](references/question-authoring.md) — how to write embedded quiz questions.

1. Confirm the course parameters with the user: topic, target audience, number of lectures, target programming language(s), and the output directory. If any are missing, ask before generating when the user is available; otherwise choose reasonable values from the context and list them as open decisions in the final report.
2. Write an outline first: a nested markdown bullet list covering all lectures, each bullet ending with a one-line summary. Show it to the user for approval when the user is available; otherwise proceed with your best outline.
3. Create the course directory structure per [references/course-format.md](references/course-format.md):
   - `<courseId>/course.yaml` listing every lecture (`id`, `name`, `description`).
   - One `<courseId>/<lectureId>/` directory per lecture. Prefix lecture IDs with zero-padded sequence numbers in course order (`01_`, `02_`, ...), followed by a descriptive name.
   - Course-scoped coding problems under `<courseId>/problems/<problemId>/`.
4. Write markdown material files inside each lecture directory, prefixing them with zero-padded sequence numbers that restart at `01_` in every lecture (`01_`, `02_`, ...), following [references/material-authoring.md](references/material-authoring.md). Write material bodies in Japanese unless the user requests another language.
5. Embed quiz questions in the material bodies as fenced `yaml question` blocks per [references/question-authoring.md](references/question-authoring.md). Insert questions right after each newly introduced concept, not in a batch at the end.
6. Decide whether writing, modifying, or executing code is part of the course's learning objective. If it is, create one or more course-scoped Judge problems at meaningful checkpoints with [generate-judge-problems](../generate-judge-problems/SKILL.md). Each problem must require learners to apply concepts already introduced in the course; embedded questions and complete code examples do not satisfy this requirement. Link each problem near its prerequisite material as `[表示名](problems/<problemId>)`. Every linked problem directory must exist under the same course's `problems/` directory. For a course without executable coding objectives, create Judge problems only when the request requires them. Never reference another course's problems.
7. Validate with the `exercode-problem` CLI (it ships with `@exercode/problem-utils`, which must be a declared repository dependency — see [setup-exercode-course-repository](../setup-exercode-course-repository/SKILL.md)) and fix until clean:

   ```bash
   bunx exercode-problem validate-course <courseDir> --problems-dir <problemsDir>
   ```

   For a course without Judge problems, omit `--problems-dir` (an explicitly given directory must exist); the validator then resolves problem references against the problems inside the course directory, so a dangling reference is an error. Fix every reported error and rerun. Repeat until the command reports success. Address warnings too unless they are intentional; if you keep a warning, tell the user why in the final report.

8. Report the created course directory, the lecture list, and any open decisions (e.g., outline items you chose without user confirmation, intentionally kept warnings).
