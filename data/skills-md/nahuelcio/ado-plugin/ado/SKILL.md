---
name: ado
description: "Trigger: Azure DevOps PRs, work items, profiles; review/vote/comment a PR; list/create/update work items. Drive Azure DevOps via the `ado` CLI."
license: Apache-2.0
allowed-tools: [Bash, Read]
---

## Activation Contract

Load when the task touches Azure DevOps: pull requests (review, vote, comment,
diff, create, chain), work items (list, get, update, create), or profiles. Use
the `ado` CLI for every operation.

## Hard Rules

- Run every operation through the `ado` CLI (`ado <group> <sub>`). One command per action.
- Inspect before mutating: read PR/WI state before `vote`, `comment`, `update`, `create`, `chain`.
- Never invent IDs, repos, or branch names — discover them with a read command first.
- `[repo]` is optional; omit it to auto-discover a PR by ID. A given repo selects the profile that lists it; `--profile <name>` overrides.
- Only pass flags the command lists: unknown flags are an error (with a "did you mean"). Check with `ado <group> <cmd> --help`.
- Long or multi-line bodies: write them to a file and pass `--comment-file <path>` (pr comment, pr reply, wi comment, wi update).

## Decision Gates

| Need | Command group |
| --- | --- |
| Configure / not yet set up / "no profile" or auth error | `ado init`, `ado config`, `ado show` → see `references/setup.md` |
| Enable/disable or restrict work item creation | edit `[work_item.create]` in `.adoconfig.toml` → see `references/setup.md` |
| Which profile / switch it | `ado profile` · `ado profile use <name>` |
| Inspect a PR | `ado pr get`/`context`/`threads`/`diff`/`file` |
| Act on a PR | `ado pr vote`/`comment`/`reply`/`create`/`chain` |
| Inspect a work item | `ado wi get`/`list`/`related`/`types` |
| Act on a work item | `ado wi update`/`comment`/`create`/`create-child` |

## Execution

1. Confirm context: `ado profile` (and `ado profile use` if the wrong one is active).
2. Read the target: e.g. `ado pr context <prId>` or `ado wi get <id>`.
3. Act with a single mutating command; pass `--comment`/`--state`/etc. as flags.
4. Report the CLI output verbatim; surface any error line to the user.

## References

- `references/commands.md` — full command list, flags, examples, error handling.
- `references/workflows.md` — task playbooks: code review a PR, create/update
  work items, create a PR or chain, find pending work.
- `references/setup.md` — install, `ado init`, profiles/PAT, and `.adoconfig.toml`
  rules (including whether `ado wi create` is enabled, allowed types, required fields).

Setup-related requests ("configure ado", "set up the CLI", "no profile / auth
failing", "allow/disallow creating work items"): read `references/setup.md` first.
