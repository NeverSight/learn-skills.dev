---
name: motherduck-cli
description: Use the MotherDuck CLI for terminal queries, authentication, and file-based Dive or Flight workflows.
license: MIT
---

# Use the MotherDuck CLI

## Source Of Truth

- Prefer the current MotherDuck CLI documentation and command reference. Read command help before relying on remembered flags because the command surface can evolve.
- Before authoring or editing a Dive or Flight, run `motherduck dive guide` or `motherduck flight guide`. Those built-in guides are the current runtime contract.
- Use `motherduck <command> --help` after a parsing or option error instead of guessing at syntax.

## Default Posture

- Reuse an authenticated CLI when available; check with `motherduck status` before starting a login flow.
- For automation, pass `MOTHERDUCK_TOKEN` through the environment and set an absolute, task-specific `MOTHERDUCK_HOME` so parallel agents do not share credentials or assets.
- Request `--output json` for machine-readable resource operations and check both the exit code and returned `success` field. `motherduck query --output json` returns a bare JSON array instead.
- Redirect large query results to a file rather than pulling every row into model context.
- Never run `motherduck new` merely because authentication is missing. Account creation requires an explicit signup request.
- Keep Guides as files with `motherduck guide init|pull|push`; `push` creates or updates and only adds a version when content changes. Record a Git SHA with `--external-id` and the reason with `--version-description`. `pull` overwrites local files, so push or save local edits first.
- Treat `dive push`, `flight push`, `guide push`, scheduling, secret changes, and account creation as external mutations. Perform them only when the user's build/change request includes that outcome.

## Workflow

1. Inspect the host project and existing CLI/authentication state.
2. Install or upgrade only when needed, following the current platform-specific docs.
3. Choose CLI or MCP based on the task shape:
   - files, local edits, CI, large results, or repeated iterations: CLI
   - chat-only exploration, inline answers, or no filesystem: MCP
   - mixed workflow: explore through MCP, then build from local files through the CLI
4. For queries, use `motherduck query` with the smallest suitable output format.
5. For a Dive or Flight, read its built-in guide, pull or initialize the local project, edit files, validate or preview, then push only when publication is requested.
6. Capture the resource ID, URL, or run number from JSON output and verify the remote state after mutation.

For answer, review, or planning requests, recommend commands without logging in, creating an account, or changing remote resources. For explicit build/change requests, complete the in-scope CLI workflow and validate its result; ask before destructive deletes or materially broader external changes.

## References

Read only the reference sections needed for the current task.

- Read `references/CLI_PLAYBOOK.md` for installation, authentication, JSON contracts, query patterns, agent isolation, and complete Dive/Flight file workflows.

## Related Skills

Load related skills only for missing capabilities; reuse established context.

- `motherduck-connect` for choosing the underlying application connection path
- `motherduck-explore` and `motherduck-query` for catalog discovery and SQL behavior
- `motherduck-create-dive` and `motherduck-create-flight` for the product-specific authoring workflow
