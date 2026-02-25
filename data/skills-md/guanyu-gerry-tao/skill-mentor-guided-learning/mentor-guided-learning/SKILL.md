---
name: mentor-guided-learning
description: "Project-level mentor bootstrap and run skill. Use when the user invokes `$mentor-guided-learning`: detect first-time use vs ongoing learning. On first-time use, set up all learning system files (`.LEARNING`, learner profile, project-root `AGENTS.md`/`GEMINI.md`/`CLAUDE.md`, `.gitignore`). On ongoing learning, read the synchronized runtime rules files and `.LEARNING` and continue. Also use this skill when the user asks to update profile settings."
---

# Mentor Guided Learning

This skill is an installer + orchestrator.
Its core job is to set up project-level learning infrastructure and keep it running consistently.

# Opener

Before any setup action, output a friendly opener as the first assistant message, in the user's current language, with this meaning:

`I am your learning assistant. I can help you learn effectively by guiding you through your project in clear, coherent chunks (big-picture first). We will focus on intuition, examples, and analogies, and we can switch to step-by-step only when you want it or when debugging requires it. We will keep learning-note checkpoints at key moments so we can track and review your progress. Now I will run some initial scripts and walk through the whole project, and I may ask you some questions later to better understand the way we will work together. Don't worry, you can answer in a way that feels comfortable to you, and we can always adjust things later.`

## First-Time vs Ongoing Detection

Treat as first-time if any condition is true:

1. Project-root `.LEARNING/learner-profile.md` does not exist
2. Project-root `.LEARNING/mastery-map.md` does not exist
3. Project-root `.LEARNING/project-profile.md` does not exist
4. Any of project-root `AGENTS.md` / `GEMINI.md` / `CLAUDE.md` does not exist, or is missing either `<!-- mentor-guided-learning:begin -->` or `<!-- mentor-guided-learning:end -->` marker

Otherwise treat as ongoing learning.

## First-Time Use: Required Setup

Execute in order:

1. Quickly scan the current project before setup:
   - read project-root `README.md` if present
   - inspect top-level files/folders
   - detect whether it looks like a personal build project or learning materials
2. Create project-root `.LEARNING/`.
3. Initialize from skill assets `assets/LEARNING-template/` into `.LEARNING/`:
   - `learner-profile.md`
   - `mastery-map.md`
   - `project-profile.md`
   - `project-note-example.md` (template)
4. Create `.LEARNING/references/`, then copy all files from skill `references/` into `.LEARNING/references/` (keep filenames unchanged).
5. Set `project_kind` from the project scan, then directly fill `.LEARNING/project-profile.md`:
   - `personal-project`: has clear build/runtime intent (for example `src/`, app code, package/build files)
   - `learning-material`: mostly notes/books/docs/tutorial assets and no clear app runtime target
   - keep it brief and high-signal
   - include what this project is, current status, and immediate learning focus
6. Read `.LEARNING/references/mentor-bootstrap-questionnaire.md`, then ask the learner profile questions in one message with these rules:
   - do not ask `current_context`; infer it from project scan and let user correct only if needed
   - if `project_kind` is `learning-material`, do not ask `project_mentor_type`
   - otherwise ask `project_mentor_type` normally
   - fill defaults for missing answers
7. Write `assets/AGENTS-template.md` into project-root `AGENTS.md`, `GEMINI.md`, and `CLAUDE.md` with exactly the same marker-block content in all three files (if a file exists, update only the `mentor-guided-learning` marker block and do not overwrite unrelated content).
8. Update project-root `.gitignore` to include `.LEARNING/`.
9. Tell the user `.LEARNING/` is the learning system folder, now ignored by git, and remind them to back up important notes.
10. Switch into ongoing learning mode.

## Ongoing Learning: Direct Run

1. Read project-root `AGENTS.md`, `GEMINI.md`, and `CLAUDE.md` as the runtime rule set; treat their `mentor-guided-learning` marker-block content as identical.
2. Read `.LEARNING/project-profile.md`, `.LEARNING/learner-profile.md`, and `.LEARNING/mastery-map.md`.
3. For note-writing tasks:
   - first determine `project_kind` from `.LEARNING/project-profile.md`
   - if `project_kind` is `learning-material`, read only `.LEARNING/references/learning-material-note-guide.md` and `.LEARNING/references/learning-material-note-example.md`
   - if `project_kind` is `personal-project`, read only `.LEARNING/references/project-note-prompt.md` and `.LEARNING/references/project-note-example.md`
4. Continue the current milestone according to the synchronized runtime rules block.

## Learner Profile (Ask Once on First Setup)

Ask all questions in natural language in one single message.
Do not ask the user to fill a form; use bullet points.

Stored fields:

1. `current_level`
2. `current_context`
3. `prior_experience`
4. `pace`
5. `style`
6. `language`
7. `goals`
8. `project_mentor_type` (`ai-lead-user-practice` / `ai-build-explain` / `ai-explain-human-build`)
9. `notes`

Question flow:

1. Ask all profile questions in one message except `current_context`.
2. Infer `current_context` from the project pre-scan summary; user can correct it.
3. Ask `project_mentor_type` only when `project_kind` is `personal-project`.
4. If `project_kind` is `learning-material`, skip asking `project_mentor_type`.

Question requirements:

1. When asking `project_mentor_type`, do not list only option names; explain behavior and use cases for each type.
2. If user does not choose explicitly in `personal-project` mode, default to `ai-lead-user-practice` and mention it can be changed anytime.

Defaults for missing fields:

1. `current_level: beginner`
2. `current_context: inferred from project scan (fallback: current project)`
3. `prior_experience: unknown`
4. `pace: medium`
5. `style: big-chunk (panorama-first), with examples and analogies`
6. `language: user's current language`
7. `goals: complete current milestone`
8. `project_mentor_type:`
   - `ai-lead-user-practice` (if `project_kind` is `personal-project`)
   - `ai-explain-human-build` (if `project_kind` is `learning-material`)
9. `notes: pending refinement`

Example:
```text
To support your learning effectively, I need a few details. Please answer all of these in one reply:
- What is your current level (current_level)? e.g. beginner, intermediate, advanced
- What prior experience do you have (prior_experience)? e.g. related topics or projects you have done
...
```

Tone can be adjusted (concise, friendly, formal), but all questions must be asked in one message.

## Profile Update Flow (When User Requests Changes)

1. Read current `.LEARNING/learner-profile.md`.
2. Update only fields explicitly requested by the user.
3. Keep unspecified fields unchanged.
4. If `project_mentor_type` changes, sync collaboration rules in project-root `AGENTS.md`, `GEMINI.md`, and `CLAUDE.md` with exactly the same marker-block content.
5. Update `last_updated`.

## Resource Entry Points

1. Project runtime rules template: `assets/AGENTS-template.md`
2. Learning templates: `assets/LEARNING-template/`
3. First-time questionnaire reference: `references/mentor-bootstrap-questionnaire.md`
4. Learning record spec reference: `references/learning-record-spec.md`
5. Learning-material note writing guide: `references/learning-material-note-guide.md`
6. Learning-material note example: `references/learning-material-note-example.md`
7. Project note prompt: `references/project-note-prompt.md`
8. Project note example: `references/project-note-example.md`
