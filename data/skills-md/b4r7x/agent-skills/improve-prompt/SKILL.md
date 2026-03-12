---
name: improve-prompt
description: Transforms a rough, unpolished prompt idea into a precise, structured AI coding prompt. Automatically researches the current project context (stack, file structure, conventions, git history) before generating. This skill should be used when the user provides a vague or "dirty" prompt idea and asks to refine, improve, or rewrite it — e.g. "improve this prompt", "refine my prompt", "ulepszony prompt", "dopracuj prompt", or simply describes what they want done in rough terms.
metadata:
  author: b4r7x
  version: "1.0.0"
  argument-hint: <prompt>
---

# Improve Prompt

Transforms a rough prompt into a precise, structured AI coding prompt with automatic project context research.

## Workflow

Execute all three phases in order. Do not skip phases.

### Phase 1 — Clarify Intent

Interpret the user's rough input. Identify:
- **Task type**: refactor / implement / debug / add feature / migrate / review / explain
- **Primary language & framework** (from the input or from Phase 2 research)
- **Expected output type**: code only / file modification / architectural plan / explanation

If the rough prompt is ambiguous about the task type, make a reasonable inference and state it in the generated prompt's Task field.

### Phase 2 — Research Project Context

Before writing a single word of the refined prompt, research the current project. Follow the steps in `references/project-research-playbook.md`.

**Minimum required research (always run):**

```bash
cat README.md 2>/dev/null | head -80
cat CLAUDE.md 2>/dev/null | head -60
cat AGENTS.md 2>/dev/null | head -60
cat .github/copilot-instructions.md 2>/dev/null | head -40
cat .cursorrules 2>/dev/null | head -40
cat package.json 2>/dev/null | head -40
find . -maxdepth 2 -type d | grep -v node_modules | grep -v .git | head -25
git log --oneline -8 2>/dev/null
```

Run additional research if the task references specific files or modules — use `grep` and `glob` to find them.

**For full research guidance:** `references/project-research-playbook.md`

### Phase 3 — Output Refined Prompt

Using the intent from Phase 1 and the context from Phase 2, generate a structured prompt following `references/ai-coding-prompt-guide.md`.

**Required output format:**

```
**Role:** [specific persona matching the project stack]
**Context:** [framework + key libraries + relevant file paths with exact paths]
**Task:** [one precise action-verb sentence]
**Constraints:** [what NOT to do, style rules, size limits]
**Output format:** [code only / with explanation / diff / step-by-step then code]
**Acceptance criteria:** [testable conditions — at least one]
**References:** [exact file paths from the research phase]
```

Output the refined prompt in a fenced code block so the user can copy it easily.

**For complex tasks targeting Claude in an agentic context**, prefer XML-structured format over Markdown headers — see `references/ai-coding-prompt-guide.md` for the template.

**For field-by-field guidance and anti-patterns:** `references/ai-coding-prompt-guide.md`

## Example

**User input (rough):** "fix the auth"

**Phase 1:** Task = debug/fix, likely TypeScript/Node.js based on project, output = modified code

**Phase 2:** Research reveals `src/auth/middleware.ts`, NestJS + Passport, recent git commit shows JWT validation error

**Phase 3 output:**
```
**Role:** Senior TypeScript engineer working on a NestJS REST API with Passport and JWT
**Context:** NestJS app, `src/auth/middleware.ts` handles JWT validation using jsonwebtoken v9. TypeScript strict mode enabled. ESM module.
**Task:** Fix the JWT token validation in `src/auth/middleware.ts` — tokens are not being rejected when expired
**Constraints:** Do not change the `AuthMiddleware` class public interface. No new dependencies. Keep existing error format.
**Output format:** Modified `src/auth/middleware.ts` only, with a brief comment on each change
**Acceptance criteria:** Expired tokens return 401 with `{ error: "TOKEN_EXPIRED" }`. Valid tokens still pass through.
**References:** `src/auth/middleware.ts`, `src/auth/auth.module.ts`
```
