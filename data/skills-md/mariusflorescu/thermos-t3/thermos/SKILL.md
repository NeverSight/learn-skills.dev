---
name: thermos
description: "Launch both thermo-nuclear review subagents in parallel, then synthesize their findings. Use for thermos, double thermo review, or combined bug/security and code-quality branch audits."
disable-model-invocation: true
---

# Thermos

A skill named in bold or in backticks, or run as `/<name>`, is the file `../<name>/SKILL.md` beside this skill's directory. Read the file and follow it. These skills are user-only, so your skill tool cannot load them. This skill's directory is the one your harness gave when it loaded this file (Claude Code prints `Base directory for this skill`, Codex attaches the skill's `<path>`), else `~/.claude/skills/thermos/` on Claude Code and `~/.agents/skills/thermos/` on Codex.

Run the two thermo review passes as async background subagents in parallel, then synthesize their results.

## Workflow

1. Determine the review scope from the user request, PR, current branch, or relevant changed files.
2. Gather the diff and any file/context excerpts needed for reviewers to evaluate the change without guessing.
3. Launch both subagents in the same turn as `delegate_task` children with `mode: "async"`, each with a `title` naming its pass and a `clientRequestId` that is stable across retries and new for each review round. They run on your model unless the user names another (omit `target`). A child gets only its brief, so each brief opens with the text of its reviewer file, the file's `SKILL.md` placeholder replaced by the absolute path of that rubric skill's `SKILL.md`:
   - `../thermo-nuclear-review/references/thermo-nuclear-review-subagent.md` for bugs, breakages, security, devex regressions, feature-flag leaks, and other branch-audit risks.
   - `../thermo-nuclear-code-quality-review/references/thermo-nuclear-code-quality-review-subagent.md` for maintainability, structure, file-size growth, spaghetti, abstractions, and codebase-health risks.
4. Pass each subagent the same scoped diff/file context, under `### Git / diff output` and `### Changed file contents`, and ask it to return prioritized findings with file references and evidence.
5. End the turn after spawning. The completion notifications wake you. After both finish, synthesize the results with findings first, deduplicated across reviewers. Weight overlapping findings more heavily, resolve disagreements with your own judgment, and keep summaries brief.

If individual background summaries are already visible to the user, do not restate them wholesale. Surface the unified verdict, the highest-signal findings, and any remaining uncertainty.
