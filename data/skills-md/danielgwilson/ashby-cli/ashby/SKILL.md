---
name: ashby
description: |
  Use this skill whenever you need to inspect or update Ashby via the official API using the agent-first `ashby` CLI.
  Triggers include: candidate search, candidate lookup, Ashby application review, moving candidates between stages,
  adding candidate notes, listing jobs or stages, or keeping an Ashby hiring pipeline current without using the UI.
---

# Ashby (agent-first CLI)

Use this skill when the task touches Ashby candidates, applications, stages, or notes.

Important naming detail:

- npm package name: `ashby-cli`
- CLI binary name: `ashby`

Resolution order:

1. If `ashby` is already on `$PATH`, use it directly.
2. Otherwise run the published package explicitly with `npx -y ashby-cli <args>`.

Do not guess alternate package names like `@danielgwilson/ashby-cli` or `npx ashby` unless those packages are explicitly published later.

If the binary is missing, install it with `npm install -g ashby-cli`.

Default stance:

- Prefer the official API-backed `ashby` CLI, not browser automation.
- Prefer `--json` for machine-readable output.
- Prefer read-only inspection before mutations.
- Be conservative with candidate data in logs and chat output.

## Default workflow

- If auth is missing, run `ashby auth setup`
- Sanity check auth: `ashby doctor --json`
- Inspect key identity: `ashby whoami --json`
- Search for a candidate: `ashby candidate search --name "Jane Doe" --json`
- Or by email: `ashby candidate search --email "jane@example.com" --json`
- Inspect one candidate: `ashby candidate get <candidate-id> --json`
- List applications: `ashby application list --job-id <job-id> --status Active --json`
- List stages: `ashby stage list --interview-plan-id <plan-id> --json`

For this repo's common Ashby triage flow, the default sequence is:

1. `ashby doctor --json`
2. `ashby whoami --json`
3. `ashby candidate search ... --json`
4. `ashby application list --job-id ... --json`
5. `ashby stage list --interview-plan-id ... --json`

## Common mutations

- Create a candidate:
  - `ashby candidate create --name "Jane Doe" --email "jane@example.com" --json`
- Add a note:
  - `ashby note create --candidate-id <candidate-id> --note "Strong fast-track candidate" --json`
- Create an application:
  - `ashby application create --candidate-id <candidate-id> --job-id <job-id> --interview-stage-id <stage-id> --json`
- Move an application to a new stage:
  - `ashby application stage-change --application-id <application-id> --interview-stage-id <stage-id> --json`

## Auth

Ashby does not expose OAuth for this API. The recommended human path is browser-assisted API key setup.

If `ashby doctor --json` reports missing auth:

- Best interactive path: `ashby auth setup`
- Best ephemeral path: `ASHBY_API_KEY=... ashby doctor --json`
- Saved local config: `printf '%s' "$ASHBY_API_KEY" | ashby auth set --stdin`
- If using `npx`, remember it does not load `.env.local` automatically. Export `ASHBY_API_KEY` first, or explicitly source your env file in the shell before invoking `npx -y ashby-cli ...`.
- In this repo specifically, loading `.env.local` before `npx -y ashby-cli ...` is often the fastest fix.

`ashby auth setup` opens `https://app.ashbyhq.com/admin/api/keys`, tells the user which permissions to enable, and then saves + validates the pasted key.

Avoid pasting full keys into logs or chat.

## Quick verification

If you are unsure which invocation path works in the current shell:

```bash
command -v ashby >/dev/null 2>&1 && ashby doctor --json || npx -y ashby-cli doctor --json
```

## Important constraints

- This CLI covers candidate/application state well, but it does not replace the full Ashby UI.
- Do not assume support for general outbound candidate email.
- Do not assume support for self-serve scheduling links or Ashby automation triggers.
- Do not assume the public FE job and the secret fast-track job share the same interview plan or stage IDs.
- Before mutating candidate/application state, confirm ids and current stage.

## Mutation checklist

Before creating or moving anything:

1. Confirm the candidate does not already exist.
2. Confirm the correct job id.
3. Confirm the correct interview plan and stage ids for that specific job.
4. Only then create the candidate, add notes, create the application, or move the stage.

## Contract

Stable JSON behavior is documented in `docs/CONTRACT_V1.md`.
