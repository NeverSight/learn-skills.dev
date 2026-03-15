---
name: github-script
description: Writes secure actions/github-script workflow steps. Use when GitHub Actions needs inline JavaScript with GitHub API/context.
license: MIT
metadata:
  author: kjanat
  version: "1.0"
---

# github-script

Use for authoring or reviewing `uses: actions/github-script@v8` workflow steps.

`with.script` runs as an async function body; use `await import(...)` for module imports.

## Defaults

- Pin `actions/github-script@v8`
- Runtime is Node 24
- Self-hosted runner minimum is `v2.327.1`
- Prefer `github.rest.*` endpoint methods; use `github.request(...)` for raw requests.
- Prefer ESM modules (`.mjs` or `.js` with `// @ts-check`); avoid CommonJS (`require`, `module.exports`).
- If authoring helpers in TypeScript, compile to `.mjs`/`.js` and import the built file in workflow steps.

## Fast workflow

1. Define step `id` if downstream steps need outputs.
2. Prefer `context` and `context.payload` for event data already provided.
3. Pass only missing values through `env`.
4. Keep inline script tiny; delegate logic to external ESM file.
5. Read env values via `process.env` inside module only when needed.
6. Use `github.rest.*`, `github.graphql`, or `github.request`.
7. Return value only when output needed.
8. Configure retries for flaky API calls.

## ESM-first architecture

- Inline `script` should usually do one thing: `import` + call exported function.
- Put reusable logic in `scripts/*.mjs` modules.
- Share logic across workflows via one core module + small entry modules.
- Typecheck modules locally (enable `checkJs` in `tsconfig.json` or add `// @ts-check` for JS).
- For `.ts` source files, keep runtime imports pointed at compiled JS outputs.

See `references/external-files.md` for patterns.

## Reading order

| Task                 | Read                                                                                           |
| -------------------- | ---------------------------------------------------------------------------------------------- |
| Write new step       | `SKILL.md`, `references/external-files.md`, `references/examples.md`, `references/security.md` |
| Review existing step | `SKILL.md`, `references/security.md`, `references/inputs-outputs-retries.md`                   |
| Migrate old workflow | `SKILL.md`, `references/runtime-and-migrations.md`                                             |

## Security rules

- Never inline `${{ ... }}` expressions directly inside `script`.
- Expressions are evaluated before script; direct interpolation can cause injection or invalid JavaScript.
- If value exists in `context`, use it there; do not mirror into `env`.
- Use `env` boundary and parse/validate in script.

See `references/security.md` for patterns.

## Script arguments available in script body

- `github`: authenticated Octokit client with pagination plugins
- `octokit`: alias for `github`
- `context`: workflow run context
- `core`, `glob`, `io`, `exec`
- wrapped `require` plus escape hatch `__original_require__` (legacy; prefer ESM `import`)

If you need source-level API details, inspect the action repo: `https://github.com/actions/github-script` (for example `action.yml`, `types/async-function.d.ts`, `src/main.ts`).

### This action (upstream model)

`with.script` is the body of an async function. These values are pre-defined (no import needed):

- `github`: pre-authenticated [octokit/rest.js](https://octokit.github.io/rest.js/) client
- `context`: workflow [run context](https://github.com/actions/toolkit/blob/main/packages/github/src/context.ts)
- `core`: [@actions/core](https://github.com/actions/toolkit/tree/main/packages/core)
- `glob`: [@actions/glob](https://github.com/actions/toolkit/tree/main/packages/glob)
- `io`: [@actions/io](https://github.com/actions/toolkit/tree/main/packages/io)
- `exec`: [@actions/exec](https://github.com/actions/toolkit/tree/main/packages/exec)
- `require`: wrapped Node require (cwd-relative + local npm packages); use `__original_require__` for unwrapped require

## Output model

- Function return value becomes `steps.<id>.outputs.result`
- Default result encoding is JSON
- Use `result-encoding: string` for raw string output

## Retry model

- Enable retries with `retries: <n>`
- Default retry-exempt status codes: `400,401,403,404,422`
- Override with `retry-exempt-status-codes`

See `references/inputs-outputs-retries.md` for details.

## Token model

- Default token is the action's `github-token` input default (typically workflow token, repo-scoped)
- Use `github-token` with PAT secret for cross-repo or broader scopes

## In this reference

| File                                   | Purpose                                       |
| -------------------------------------- | --------------------------------------------- |
| `references/security.md`               | injection avoidance and env-boundary patterns |
| `references/inputs-outputs-retries.md` | inputs, outputs, retry semantics              |
| `references/runtime-and-migrations.md` | v5-v8 changes and upgrade checks              |
| `references/external-files.md`         | external ESM architecture, reuse, typecheck   |
| `references/examples.md`               | minimal templates for common tasks            |

## Scope note

Upstream repository currently does not accept general contributions.\
Security fixes and major breakage fixes still maintained.
