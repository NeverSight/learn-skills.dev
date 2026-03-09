---
name: generate-agent-instructions
description: "Generate or update AGENTS.md for AI coding agents by extracting project-specific architecture, workflows, conventions, and integration details from the repository. Use when the user asks to create, refresh, or improve AGENTS.md or agent instructions for a codebase."
---

Generate or update `AGENTS.md` using evidence from the current repository.

Ignore `CLAUDE.md` entirely if present.

## Workflow

1. Locate existing `AGENTS.md` and treat it as the base when present.
2. Inspect the codebase deeply enough to understand:
   - Architecture across multiple files (major components, boundaries, data flow, and structural intent).
   - Real developer workflows (build, test, lint, run, debug, and release commands).
   - Project-specific conventions and non-obvious patterns.
   - Integrations, external services, and cross-component communication.
3. Extract only discoverable facts from code, config, scripts, and docs.
4. Merge intelligently with existing `AGENTS.md`: keep still-valid guidance, remove stale guidance, fill important gaps.
5. Write concise, actionable instructions targeted to future coding agents.

## Output Requirements

- Target roughly 20-50 lines in markdown.
- Prefer repository-specific guidance over generic best practices.
- Include concrete examples with key file or directory references.
- Document current-state behavior only (no aspirational rules).
- Preserve useful existing conventions from `AGENTS.md` when still accurate.
- Keep wording imperative and easy to execute.

## Quality Bar

- Avoid assumptions that are not supported by repository evidence.
- Prioritize information that prevents costly mistakes for new agents.
- Capture the "why" behind important structure when it is inferable.

Update `AGENTS.md`, then ask the user for feedback on unclear or incomplete sections and iterate.
