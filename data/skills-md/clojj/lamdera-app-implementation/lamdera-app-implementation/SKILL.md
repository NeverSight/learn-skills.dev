---
name: lamdera-app-implementation
description: Use when building, modifying, running, debugging, checking, or deploying Lamdera applications. Enforces Lamdera-first decisions, beginner-safe Elm guidance, and mandatory verification gates.
---

# Lamdera App Implementation

## Purpose

Use this skill for Lamdera app development workflows from project setup through deployment, with Elm-informed decisions for Lamdera architecture.

This skill is Lamdera-only:
- Do not use `elm ...` commands.
- Do not use LLVM toolchain commands (`clang`, `llc`, `opt`, etc.).

Elm documentation may be used for language/frontend concepts only.

## Required Tools

Use these Lamdera commands as the core toolchain:
1. `lamdera init`
2. `lamdera live`
3. `lamdera check`
4. `lamdera deploy`
5. `lamdera reset`
6. `lamdera login`
7. `lamdera make`

Optional diagnostics:
1. `lamdera backend --help`
2. `lamdera backend ...`

Optional static analysis:
1. `npx elm-review` (preferred, works with local installs)
2. `elm-review` (global-install fallback)

## Task Classification Loop

For every request, classify intent first:
1. `generate` for implementing or changing code.
2. `architecture` for design and module/boundary decisions.
3. `review-debug` for issue analysis, review, or diagnosis.
4. `mixed` when multiple intents are present.

Then run:
1. Apply beginner-safe defaults.
2. Apply the checklist for the classified intent.
3. If intent is `mixed`, apply checklists in this order: `architecture` -> `generate` -> `review-debug`.
4. Load deep references only if needed.
5. Return output using the required response contract.

## Beginner-Safe Defaults

1. Prefer explicit custom types for domain states over ad-hoc flags.
2. Keep messages small and purposeful; avoid catch-all messages.
3. Keep update flows deterministic and side effects explicit.
4. Start with simple module boundaries; add complexity only when forced.
5. Highlight migration-sensitive type changes early.

## Intent Checklists

### Generate
1. Validate model shape against feature intent.
2. Validate message set is minimal but complete.
3. Validate update transitions are explicit and testable.
4. Validate effect boundaries and data flow are clear.

### Architecture
1. Decide frontend/backend/shared type ownership explicitly.
2. Flag boundary leakage and unnecessary coupling.
3. Check likely impact on migrations and deploy safety.
4. Prefer simplest viable boundary split.

### Review-Debug
1. Identify symptom and reproducible path first.
2. Check state transitions and message paths before deep changes.
3. Check boundary mismatches and stale assumptions.
4. Report likely root cause and smallest safe next fix.

## Output Contract

Responses must include:
1. `Decision`
2. `Why`
3. `Risks`
4. `Next checks`

## Hard Gates

1. Do not deploy until account/auth prerequisites are satisfied.
2. Do not deploy until `lamdera check` succeeds.
3. Do not switch to `elm` CLI commands in this workflow.
4. If auth is missing for app-linked operations (`lamdera login`, `lamdera check`, `lamdera deploy`), stop and resolve login/signup first.
5. Do not claim success without verification evidence.
6. Treat `lamdera` git remote as required app context for `lamdera login`, `lamdera check`, and `lamdera deploy`.

## Workflow

1. Validate context.
Confirm this is a Lamdera app workspace. If no app exists yet, start with `lamdera init` in an empty directory.
In non-interactive agent execution, use `printf 'Y\n' | lamdera init` to satisfy the init prompt.
Before login/check/deploy, ensure app context exists: git repository with a configured `lamdera` remote.

2. Start local development.
Run `lamdera live` in an attached PTY session (not detached/background) and iterate using Lamdera compiler feedback and live reload.

3. Resolve build/runtime blockers.
If caches/tooling are inconsistent, run `lamdera reset`, then continue with `lamdera live`.
Only continue with `lamdera check` when app context exists (git repo + `lamdera` remote).

4. Enforce pre-deploy checks.
If `lamdera` app context is present (git repo + `lamdera` remote), run `lamdera check` and address all reported migration/config/type issues.
If app context is missing, report `lamdera check` as blocked by missing `lamdera` remote and run local compile verification with `lamdera make <entry-elm-file> --output=/dev/null` instead.
This local compile fallback is for local verification only and does not satisfy deploy readiness; deploy remains blocked until app context exists and `lamdera check` succeeds.

5. Run optional `elm-review` (only after compile success).
If code changed and compile verification succeeded (`lamdera check` or local `lamdera make` fallback), run `elm-review` only when the project already has `review/` configured or the user explicitly opts in.
For setup/execution, prefer local install with `npm install --save-dev elm-review` and run via `npx elm-review`; global install via `npm install -g elm-review` is allowed but less preferred.
If `review/` is missing and user opts in to `elm-review`, initialize once with `npx elm-review init --template jfmengels/elm-review-config/application` for local installs, or `elm-review init --template jfmengels/elm-review-config/application` for global installs.
When eligible (and initialized when needed), run `npx elm-review --report=json` for local installs, or `elm-review --report=json` for global installs.
Report each finding with a markdown source link using `path:line:column` from `region.start` (prefer absolute file links when workspace path is known), plus rule and message.
If findings are reported, offer the user an optional auto-fix run with `npx elm-review --fix-all-without-prompt --allow-remove-files` for local installs, or `elm-review --fix-all-without-prompt --allow-remove-files` for global installs.
After auto-fix, re-run compile verification, then re-run `elm-review --report=json`, and report what was fixed vs what remains.
If compile verification failed, skip `elm-review` and report it as blocked by compile failure.

6. Enforce deployment prerequisites.
If the user has no account, direct them to sign up first.
If not authenticated, run `lamdera login` from a repository linked to the app via `lamdera` remote.

7. Deploy.
Run `lamdera deploy` once checks and auth are satisfied.
You may mention git-push deployment as informational fallback only after explicitly confirming `lamdera check` succeeded.

## Verification Gate

After providing code or concrete implementation advice:
1. If `lamdera` CLI is available and app context exists (git repo + `lamdera` remote), you must run `lamdera check` as the minimum verification command.
2. If `lamdera` CLI is available but app context is missing, run local compile verification with `lamdera make <entry-elm-file> --output=/dev/null` and report that `lamdera check` was blocked by missing `lamdera` remote.
3. Run relevant build/compile verification and report the result.
4. If code changed and compile verification succeeded, run optional `elm-review` only when `review/` already exists or user explicitly opts in.
5. If `review/` is missing and user opts in, initialize once with `npx elm-review init --template jfmengels/elm-review-config/application` for local installs, or `elm-review init --template jfmengels/elm-review-config/application` for global installs.
6. When eligible (and initialized when needed), run `npx elm-review --report=json` for local installs, or `elm-review --report=json` for global installs.
7. Report `elm-review` findings as markdown links with `path:line:column` using each error's `region.start`.
8. If findings exist, offer optional auto-fix (`npx elm-review --fix-all-without-prompt --allow-remove-files` for local installs, or `elm-review --fix-all-without-prompt --allow-remove-files` for global installs).
9. If auto-fix runs, re-run compile verification, then re-run `elm-review --report=json`, and report resolved vs remaining findings.
10. Then select any additional verification commands from project-local scripts/config.
11. If `lamdera` CLI is not available and no project-defined verification command exists, report "not runnable with current project metadata" instead of guessing commands.
12. If tests are present, run relevant tests and report the result.
13. Keep command guidance Lamdera-first; allow optional `elm-review` commands.
14. If verification cannot run, state exactly what was not run and why.
15. Never say "done/fixed/works" without command-backed evidence.

Use this entry file selection rule for local compile fallback:
1. Prefer `src/Frontend.elm` when present.
2. Otherwise use the project's actual entry module path as `<entry-elm-file>`.
3. If entry file cannot be determined, report verification as partially blocked and state why.

## Error Handling Rules

1. Auth/session issue:
Ensure the repository is linked with `lamdera` remote, then run `lamdera login`, then re-run `lamdera check`.

2. Compiler/cache mismatch:
Use `lamdera reset`, then re-run `lamdera live`.
Only re-run `lamdera check` when app context exists (git repo + `lamdera` remote).

3. Migration/config issue:
Treat `lamdera check` output as blocking and resolve before deploy.

4. Unknown app / missing remote issue:
If Lamdera reports unknown app, configure the `lamdera` git remote for the repository, then retry `lamdera login`/`lamdera check`/`lamdera deploy`.

## Source Policy

Use these sources for guidance:
1. Lamdera docs for commands and platform workflow.
2. Elm guide for Elm language/frontend design concepts only.
3. Elm package catalog (`https://package.elm-lang.org/`) for package discovery in Lamdera frontend code only.
4. `elm-review` docs (`https://github.com/jfmengels/elm-review`) for workflow and configuration concepts.
5. `elm-review` CLI docs (`https://github.com/jfmengels/node-elm-review`) for setup/report formats.

Keep command recommendations aligned with documented Lamdera CLI behavior.

## References

For deeper guidance, load:
- `references/elm-for-lamdera-core.md`
- `references/shared-types-and-boundaries.md`
- `references/evolution-and-migration-safety.md`
- `references/review-and-debug-playbook.md`
- `references/source-map.md`
- `references/commands-and-gates.md`
- `references/sources.md`
- `references/troubleshooting.md`
