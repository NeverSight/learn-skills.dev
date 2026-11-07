---
name: write-agents-md
description: >-
  Create, audit, or reduce root and nested AGENTS.md files for web or desktop
  projects using copy-first templates. Use when establishing repository agent
  guidance or correcting bloated, unstable, or incorrectly scoped instructions.
---

# Write AGENTS.md

Produce a small, durable instruction file for the agents that automatically receive it. This skill authors guidance; it does not implement the application or perform its QA.

## Admission rule

A statement belongs in AGENTS.md only when it passes all three tests:

1. **Audience:** every agent entering this directory must know it, regardless of its task. Root means the whole repository; nested means that entire subtree.
2. **Value:** it changes a decision the agent could otherwise get wrong. It is not standard tooling knowledge, an obvious layout, or something immediately discoverable in manifests/source.
3. **Stability:** it is an enduring convention or invariant, not a session observation, changing version, task status, temporary workaround, or machine fact.

A statement failing audience goes in a task-specific **skill**. Detailed explanations/evidence go in documentation; execution state goes in the project tracker. A stable documentation entry point can stay in AGENTS.md; a task-by-task document/skill catalog cannot. Do not invent skill names or create additional skills without authorization.

TDD, the seven-step Manual QA procedure, fresh endpoint captures, verification, commit policy, and honest completion are standing obligations for every contributor. They distinguish runtime from documentation work without becoming scenario runbooks. Keep those quality gates in AGENTS.md; put commands, fixture recipes, particular flows and recovery procedures in skills.

## Select the relevant workflow

- **Web:** read [the web workflow](references/web-workflow.md); copy [the web template](assets/web-AGENTS.md).
- **Desktop:** read [the desktop workflow](references/desktop-workflow.md); copy [the desktop template](assets/desktop-AGENTS.md).

These are the two canonical templates. They preserve the user's TDD and commit wording; project/client/brand details, technology and human-language choices are generalized. Do not load the other workflow unless the project has both surfaces. For mixed projects use one minimal shared root and surface-specific nested guidance only where distinct enduring rules justify it. Do not force CLI/library-only projects into graphical-app workflows; clarify that boundary.

## Copy first, adapt second

1. Inspect existing instructions, user requirements, the documentation entry point and only the metadata needed to establish non-obvious constraints. Preserve human decisions. Do not request a full source audit merely to write instructions.
2. Choose web/desktop and root/nested scope. **Copy the chosen asset byte-for-byte before any adaptation. Never reconstruct, paraphrase or draft the starting file from memory.**
3. Use the bundled helper (Python 3.9+, standard library only):
   ```sh
   python <skill-directory>/scripts/copy_template.py --workflow web --project-root <project-root> --candidate
   python <skill-directory>/scripts/copy_template.py --workflow desktop --project-root <project-root> --scope <existing-relative-subfolder> --candidate
   ```
   It always stages AGENTS.md.candidate, refuses overwrite and out-of-project targets, verifies bytes and prints a SHA-256 receipt. The explicit --candidate flag is retained for compatibility; omitting it is equally safe. The receipt is execution evidence, not text for AGENTS.md.
4. **Always use `--candidate`, for new and existing root/nested files.** Adapt `AGENTS.md.candidate` while active guidance stays absent or unchanged. After reviewing the diff and validating that no placeholders remain, publish new guidance with a filesystem operation that refuses overwrite, or reconcile existing guidance in a reviewed edit preserving human instructions. An interrupted adaptation leaves only the candidate; report it rather than loading/publishing it. Remove your candidate after successful publication; do not commit candidates or receipts.
5. If the helper cannot run, use an available filesystem copy and compare bytes/hashes before editing. If the template cannot be read/copied, report the blocker; do not invent an approximation.
6. Apply the workflow and admission rule. Fill verified placeholders; remove optional blocks rather than inventing facts. Read [scope and adaptation](references/scope-and-adaptation.md) for fields and nested rules.
7. Compare the final diff with both the template and prior guidance. Check scope, preserved mandatory quality gates, Markdown/links, no unresolved placeholders and no duplicated ancestors. Describe important removals/relocations.

## Non-negotiable testing policy

Preserve the seven TDD steps, seven Manual QA steps and test-layer definitions. **E2E and Manual QA use the fully working application with zero mocks**, including real LLM calls, supporting services and persisted results. Unit/integration tests may isolate dependencies when useful. Before each creation/refresh of an endpoint or database mock, make a fresh real query in the authorized local/test environment and save the complete response verbatim to a file; derive the mock from that file, never documentation or invented objects. Record provenance separately without secrets; existing fixtures do not replace a fresh capture. Outdated documentation can produce mocks whose request/response shapes differ from the real endpoint. Use synthetic authorized test data; never commit private responses or credentials. Read [the endpoint mock policy](references/endpoint-mocks.md) when adapting that contract. Missing access/budget blocks mock creation/refresh and required real checks, not permission to fake a pass.

## Size and scope

Aim for **550-800 words at root** and **40-120 words nested**, smaller when fewer invariants exist. The root budget accommodates the seven-step Manual QA procedure and explicit fresh-capture mock policy alongside unchanged TDD/commit gates; 200-400 words would compress away required checks. These are review targets, not permission to weaken requirements or add filler.

Keep root to purpose/scope, agreed language policy, non-obvious universal constraints, one documentation entry point, and shared quality/commit/completion gates. Nested files need distinct folder-wide rules; do not create one for every standard source/test/resources directory.

Adapt nested copies by removing root/project sections and ancestor quality gates already in force. Retain the subtree purpose and unique invariant instructions. Do not repeat parents, explain automatic instruction loading, or link other AGENTS.md files. Do not promote folder-only rules to root.

## Exclude by default

- Exact dependency/tool versions, source counts, dates, branches, commits, host paths/usernames, local sandbox errors and tool availability.
- Standard layout, package tours, manifest dependency lists, basic Git/tool tutorials, instruction-loading explanations, or generic competence advice.
- Feature/protocol migration plans, incident fixes, conditional test recipes, platform setup and long document-trigger catalogs.
- Unrequested PRD/ADR files, fabricated commands, environment variables, branding, supported-OS lists, or unverified installed skills/tools.

An internal framework, hidden compatibility boundary, or nonstandard root can qualify when every agent in scope needs it. Enforced versions belong in manifests/documentation; refer to a stable compatibility policy only when necessary.

## Completion

Treat `AGENTS.md.candidate` as an internal draft, not the delivered result. Complete adaptation, validation and publication/reconciliation as `AGENTS.md` within the same authoring task, before presenting final files or opening a PR. Commit the finished `AGENTS.md` only; remove your candidate. If interrupted, report the task as incomplete.

Show files actually changed, template copied, adaptations/relocations and checks. Leave application code untouched unless authorized. Preserve unrelated work and tool-specific instructions. Create a CLAUDE.md import only when requested or established; do not duplicate guidance or overwrite tool-specific content.

Require affected instructions and documentation to be updated in the same logical change when enduring facts/policies change. Do not claim enforcement against an agent ignoring the skill: the helper proves the starting copy; final scope and meaning require review.
