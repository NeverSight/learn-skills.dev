---
name: staffer
description: Delegate a general-purpose task to Google's Antigravity CLI (agy staffer, fast Gemini) with a minimal, unopinionated prompt. Use when the user says /agy:staffer, "have agy do/handle X", "have agy generate an image", or the task fits none of the specialist personas (researcher / reviewer / implementer / ask) — the template adds no role or output format, only the shared working rules and guardrails, so the task text shapes the output. Also the route to agy-native tools no specialist covers, notably image generation (generate_image).
argument-hint: '[--restricted|--unrestricted] [--model <id>|--effort low|medium|high|xhigh] [--timeout <dur>] [--prompt-file <path>|--stdin] "task"'
allowed-tools: Read, Glob, Grep, Bash(node:*), Bash(git:*), Bash(gh:*)
---

# agy staffer

The general-purpose persona: a clean entry point for tasks that none of the specialists fit. Its prompt template is deliberately minimal — the task text, the environment (cwd, branch, date), the shared working rules, and the safety guardrails, nothing else. No role framing or fixed body format: the task defines its own deliverable, and no domain-specific template context can pull the run off course.

Prefer a specialist when one fits: `researcher` for surveys and deep dives, `reviewer` for second opinions on code or plans, `implementer` for edits to the working tree, `ask` for a cheap one-shot question.

staffer is also the route to agy-native tools no specialist covers — notably **image generation**: agy ships a `generate_image` tool (verified on v1.1.15; a 1024×1024 PNG in ~30s). Name the output path in the task, e.g. `staffer --prompt "generate a pixel-art robot mascot, save it as assets/mascot.png"`.

<!-- BEGIN SHARED PERSONA RULES -->
<!-- Generated from templates/persona-skill-rules.md; run npm run generate:skills. Do not edit this block. -->
## Dispatch

- Continue a completed job with `continue --job <id> --prompt "..."` when the task and persona are the same and prior context helps, even if the user does not say "continue". Keep each job ID with its assignment; if the target is unclear, check known jobs before asking the user.
- Start fresh for a different task or persona, an independent opinion, or an explicit fresh start. Carry relevant findings and artifact paths into the new brief.
- Pass the user's task and explicit authorizations verbatim. On follow-up, add decisions and constraints from the host chat that the worker has not seen. Continuation does not expand authorization.
- Run the companion unsandboxed; in Codex, request escalated execution. Follow `../jobs/SKILL.md` for collection and recovery. After an execution timeout, obtain explicit user confirmation before continuing or restarting.
<!-- END SHARED PERSONA RULES -->

## Locating the companion

This skill file lives at `<plugin-root>/skills/staffer/SKILL.md`; resolve the companion path relative to this skill directory:

```bash
node "<skill-dir>/../../companion/agy-companion.mjs" staffer [flags] --prompt "task"
```

## Collecting the result

The command returns a job id. Read `../jobs/SKILL.md` for result collection and recovery: dispatch, wait for the final result, then validate as needed. Do not proactively observe progress, read logs or inspect intermediate artifacts while running. Observe only when the user explicitly asks for progress; diagnose a failure or a result requiring intervention under the jobs protocol.

## Flags (all optional)

- `--prompt <text>` / `--prompt-file <path>` / `--stdin` — the task, from exactly one of these three sources. Use file/stdin for long prompts instead of shell quoting.
- `--model <id>` or `--effort low|medium|high|xhigh` — default model is `gemini-4-hydrogen-medium`; `--model` also accepts family aliases `hydrogen` (`gemini-4-hydrogen`), `carbon` (`gemini-4-carbon`), `argon` (`gemini-4-argon`), `flash` (`gemini-3.8-flash`), and `pro` (`gemini-3.1-pro`).
- `--restricted` / `--unrestricted` — permission profile; staffer defaults to unrestricted like the other tool-using personas, `--restricted` is the opt-in hardening path.
- `--timeout <dur>` — default 60m, maximum 120m hard execution limit.

## Rules

- Pass the user's task through verbatim. Because the template imposes no output format, state the desired format in the task text when the caller needs a specific one.
- Pass the user's explicit authorizations through verbatim. The template default-denies costly or irreversible side effects (commits/pushes, deleting files outside the workspace, side-effectful network calls, paid-quota commands); that default opens only when the task itself asks for the operation.
- A general task may legitimately edit files. The companion reports any working-tree delta with the result — inspect it (`git diff`) and confirm it is what the task asked for before building on it.
- For errors and recovery, follow `../jobs/SKILL.md`.

For an existing session, `continue --job <id>` inherits the job's persona, recorded model, and permission profile unless explicitly overridden. The unrestricted defaults above apply to new tasks.
