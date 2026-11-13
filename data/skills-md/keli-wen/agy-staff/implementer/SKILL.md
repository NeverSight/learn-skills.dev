---
name: implementer
description: Delegate a coding task to Google's Antigravity CLI (agy staffer, fast Gemini), which edits the working tree directly and can perform explicitly requested Git delivery. Use when the user says /agy:implementer, "have agy fix/build X", or wants to hand a well-scoped coding task to the agy staffer instead of doing it in the host model.
argument-hint: '[--restricted|--unrestricted] [--model <id>|--effort low|medium|high|xhigh] [--prompt-file <path>|--stdin] "task description"'
allowed-tools: Read, Glob, Grep, Bash(node:*), Bash(git:*), Bash(gh:*)
---

# agy implementer

Hand a coding task to the agy staffer. agy edits the real working tree under its unrestricted permission profile; the companion is a thin launcher and job collector. Pass the user's requested delivery through in the task text instead of doing Git work yourself.

<!-- BEGIN SHARED PERSONA RULES -->
<!-- Generated from templates/persona-skill-rules.md; run npm run generate:skills. Do not edit this block. -->
## Dispatch

- Continue a completed job with `continue --job <id> --prompt "..."` when the task and persona are the same and prior context helps, even if the user does not say "continue". Keep each job ID with its assignment; if the target is unclear, check known jobs before asking the user.
- Start fresh for a different task or persona, an independent opinion, or an explicit fresh start. Carry relevant findings and artifact paths into the new brief.
- Pass the user's task and explicit authorizations verbatim. On follow-up, add decisions and constraints from the host chat that the worker has not seen. Continuation does not expand authorization.
- Run the companion unsandboxed; in Codex, request escalated execution. Follow `../jobs/SKILL.md` for collection and recovery. After an execution timeout, obtain explicit user confirmation before continuing or restarting.
<!-- END SHARED PERSONA RULES -->

## Locating the companion

This skill file lives at `<plugin-root>/skills/implementer/SKILL.md`; resolve the companion path relative to this skill directory:

```bash
node "<skill-dir>/../../companion/agy-companion.mjs" implement [flags] --prompt "task description"
```

## Workspace and delivery

- Inside a git repository, dirty workspaces are allowed. When `git status --porcelain` is not clean, the companion injects a bounded pre-run status summary into the implement prompt so agy treats those paths as user-owned context.
- Outside a git repository the companion warns that agy's edits cannot be reviewed or rolled back via git, and proceeds. Relay that warning; there is no diff to fall back on.
- By default, agy leaves a working-tree diff. If the user explicitly asks for a commit, push, or PR, include that request verbatim in the task text and let agy do that exact Git delivery.
- After the run, surface agy's summary and the current workspace state. Do not add your own commit/PR step unless the user separately asks you to do it.

## Collecting the result

The command returns a job id. Read `../jobs/SKILL.md` for result collection and recovery: dispatch, wait for the final result, then validate as needed. Do not proactively observe progress, read logs or inspect intermediate artifacts while running. Observe only when the user explicitly asks for progress; diagnose a failure or a result requiring intervention under the jobs protocol.

## Flags (all optional)

- `--restricted` / `--unrestricted` — permission profile. implement defaults to unrestricted, so it works out of the box with no setup. `--restricted` is the opt-in hardening path: agy may then only use allowlisted tools, so it can usually only propose rather than edit, and it needs the setup flow's evidence-gathering allowlist to be useful.
- `--model <id>` / `--effort low|medium|high|xhigh` (default `gemini-4-hydrogen-high`; `--model` accepts aliases `hydrogen`, `carbon`, `argon`, `flash`, `pro`), `--timeout <dur>` (default 60m, maximum 120m hard execution limit).
- `--prompt <text>` / `--prompt-file <path>` / `--stdin` — the task, from exactly one of these three sources. Use file/stdin for long prompts.

## Rules

- Do not pre-implement, extend, or "clean up" agy's changes without user confirmation.
- Return agy's summary verbatim before presenting the diff.
- Pass the user's explicit authorizations through to the task string verbatim. The prompt template default-denies costly or irreversible side effects; that default opens only when the request itself asks for the operation — so keep "open a draft PR", "run the e2e tests", or "call the staging API" in the prompt instead of trimming it.
- Never commit agy's changes yourself unless the user explicitly asks you, the host agent, to do it.
- For errors and recovery, follow `../jobs/SKILL.md`.

For an existing session, `continue --job <id>` inherits the job's persona, recorded model, and permission profile unless explicitly overridden. The unrestricted defaults above apply to new tasks.
