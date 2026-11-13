---
name: reviewer
description: Get a second-opinion review from Google's Antigravity CLI (agy staffer, fast Gemini) - of code (a diff, PR, working tree) or of a decision, plan, or design. Use when the user says /agy:reviewer, "have agy review this", "second opinion on my diff/PR/plan", or after finishing work and wanting an independent verifier that does not share the host model's blind spots.
argument-hint: '[--restricted|--unrestricted] [--json] [--model <id>|--effort low|medium|high|xhigh] [--prompt-file <path>|--stdin] "what to review"'
allowed-tools: Read, Glob, Grep, Bash(node:*), Bash(git:*), Bash(gh:*)
---

# agy reviewer

Run a second-opinion review through the agy staffer. You are a thin shell: compose the task, run the companion, return agy's review verbatim. Never fix the issues it finds.

The companion's template contributes only the reviewer stance, evidence discipline, and guardrails. Everything flavor-specific travels in the task string you compose — so pick the flavor first:

- **Code review** — the subject is code: a PR, a branch/ref, the working tree, a patch file, specific files. Read `references/code-review.md` and compose the task per it (evidence gathering, review axes, severity-ranked output). `--json` belongs to this flavor only.
- **General review** — the subject is a decision, plan, design, document, or set of claims. Read `references/general-review.md` and compose the task per it (multi-angle challenge). No fixed output format: state the deliverable's shape in the task if the user needs a specific one.

<!-- BEGIN SHARED PERSONA RULES -->
<!-- Generated from templates/persona-skill-rules.md; run npm run generate:skills. Do not edit this block. -->
## Dispatch

- Continue a completed job with `continue --job <id> --prompt "..."` when the task and persona are the same and prior context helps, even if the user does not say "continue". Keep each job ID with its assignment; if the target is unclear, check known jobs before asking the user.
- Start fresh for a different task or persona, an independent opinion, or an explicit fresh start. Carry relevant findings and artifact paths into the new brief.
- Pass the user's task and explicit authorizations verbatim. On follow-up, add decisions and constraints from the host chat that the worker has not seen. Continuation does not expand authorization.
- Run the companion unsandboxed; in Codex, request escalated execution. Follow `../jobs/SKILL.md` for collection and recovery. After an execution timeout, obtain explicit user confirmation before continuing or restarting.
<!-- END SHARED PERSONA RULES -->

## Locating the companion

This skill file lives at `<plugin-root>/skills/reviewer/SKILL.md`; resolve the companion path relative to this skill directory:

```bash
node "<skill-dir>/../../companion/agy-companion.mjs" review [flags] --prompt "what to review"
```

Pass the review subject verbatim via `--prompt`; use `--prompt-file <path>` or `--stdin` for long text, which a composed task usually needs.

## The review subject is the prompt

review is prompt-based: the user's request plus the flavor's framing is the task string. Do not gather diffs, write patch files, or translate the request into flags — agy collects the evidence itself. If the subject is ambiguous, agy reports the ambiguity instead of guessing; relay that and let the user sharpen the request. A task string is required; review with no subject exits with an error.

## Collecting the result

The command returns a job id. Read `../jobs/SKILL.md` for result collection and recovery: dispatch, wait for the final result, then validate as needed. Do not proactively observe progress, read logs or inspect intermediate artifacts while running. Observe only when the user explicitly asks for progress; diagnose a failure or a result requiring intervention under the jobs protocol.

## Flags (all optional)

- `--json` — schema-enforced JSON findings (verdict/summary/findings/could_not_verify) instead of markdown. Code-review flavor only, and only when the user asks for machine-readable output.
- `--restricted` / `--unrestricted` — permission profile. review defaults to unrestricted, so it works out of the box and can run tests or reproduce a bug when the request asks for it. `--restricted` is the opt-in hardening path: agy may then only use allowlisted tools, so it needs the setup flow's evidence-gathering allowlist to be useful — and some native agy tools ignore allow-rules headless, so restricted runs can still come back empty.
- `--model <id>` / `--effort low|medium|high|xhigh` (default `gemini-4-hydrogen-medium`; `--model` accepts aliases `hydrogen`, `carbon`, `argon`, `flash`, `pro`), `--timeout <dur>` (default 60m, maximum 120m hard execution limit).
- `--prompt <text>` / `--prompt-file <path>` / `--stdin` — the task, from exactly one of these three sources. Use file/stdin for long prompts (a composed task with the flavor framing usually is one).

## Reviewing untrusted content

An unrestricted review of code from an untrusted author (a PR from a stranger, a patch from an unknown source) means prompt injection in that content could run arbitrary commands. For those reviews, consider `--restricted` (it may fail closed, and some native tools ignore allow-rules) or run the review in an isolated checkout.

## Rules

- Return the companion stdout verbatim — no commentary, no fixes, no softening of findings.
- Pass the user's explicit authorizations through to the task string verbatim. The prompt template default-denies costly or irreversible side effects (commits/pushes, deleting files outside the workspace, side-effectful network calls, commands that burn paid API quota); that default opens only when the request itself asks for the operation — so keep "run the e2e tests" or "call the staging API" in the prompt instead of trimming it.
- Empty responses from a `--restricted` run: relay the companion's guidance (run the setup flow once, or drop `--restricted`).
- For errors and recovery, follow `../jobs/SKILL.md`.

For an existing session, `continue --job <id>` inherits the job's persona, recorded model, and permission profile unless explicitly overridden. The unrestricted defaults above apply to new tasks.
