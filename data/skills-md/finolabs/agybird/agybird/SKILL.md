---
name: agybird
description: Delegate code work, image generation or editing, and general tasks to the official Google Antigravity CLI through an existing Gemini subscription. Use this skill only when the user explicitly mentions Agybird, `agy`, Antigravity CLI, or asks to use their Gemini subscription through Antigravity. Do not use or trigger it for generic coding, image, or research requests.
compatibility: Requires Node.js 20+ and the official `agy` CLI authenticated by the user.
---

# Agybird

Use the official Antigravity CLI as a delegated worker while keeping its authentication, permissions, sandbox, model access, and credits under the user's existing configuration.

## Route the request

1. Read [references/common.md](references/common.md) for every invocation.
2. Select exactly one category:
   - Read [references/code.md](references/code.md) for repository inspection, implementation, debugging, refactoring, or tests.
   - Read [references/image.md](references/image.md) for generating a new image or editing reference images.
   - Read [references/general.md](references/general.md) for analysis, research over local context, structured output, or non-code deliverables.
3. Read [references/models.md](references/models.md) before the first run of a new objective that is not image work, and after any run that ends in `error`.
4. Read [references/security.md](references/security.md) before any write-mode or sensitive-repository task.
5. Read [references/troubleshooting.md](references/troubleshooting.md) only when `agy` is missing, authentication fails, permissions block work, quota is exhausted, or output cannot be parsed.
6. Read [references/docs.md](references/docs.md) when deep or specialized official Antigravity documentation is needed.

## Core workflow

1. Resolve this skill's absolute directory and verify Node.js 20 or newer.
2. Check `agy --version`. If `agy` is missing, stop and direct the user to official setup; do not run installation commands.
3. Infer `read` or `write` from the user's requested outcome. Default to `read` when inspection can satisfy the request.
4. Invoke `scripts/agybird.mjs` with an absolute `--cwd` and send the task through standard input. Add `--new-session` on the first run of a new objective, and never on a follow-up.
5. Inspect the normalized result envelope. Treat `partial`, `needs_permission`, `blocked`, and `error` as distinct outcomes; do not describe them as success.
6. Keep the whole objective in one conversation. The runner resumes the workspace's session on its own, so a follow-up needs no extra flag; confirm it worked through `evidence.session_resumed`.
7. On `needs_permission`, put the request in front of the user and wait. Never grant a permission on the user's behalf. Once approved, run again with `--grant` and let the session resume rather than starting over.
8. Independently verify the result according to the selected category.

Choose the model per run with `--model` as [references/models.md](references/models.md) describes: the lowest tier that fits, in a pool that still has quota. A model or reasoning level the user asks for wins, even in their own words such as "use a stronger model" or "think harder"; state the chosen value and never persist it. Pass `--agent` or `--sandbox` only when the user explicitly asks for that exact override. Never change `useG1Credits` or any other credit policy without the user's explicit approval. Never bypass Antigravity permissions.
