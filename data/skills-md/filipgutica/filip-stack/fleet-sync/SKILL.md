---
name: fleet-sync
description: Sync a shared filip-stack guidance, skill, and plugin baseline across linked T3 Code environments, with per-machine exceptions. Use for fleet updates or to check which machines remain out of sync.
---

# Fleet sync

Run the same per-machine updater on demand, then account for every enrolled machine. Keep the baseline and machine exceptions in one policy file.

## Establish the fleet

Read `$XDG_CONFIG_HOME/filip-stack/fleet.json`, or `~/.config/filip-stack/fleet.json` when unset. It contains user-owned policy and metadata; T3 owns credentials and grants:

```json
{
  "version": 1,
  "baseline": {
    "skills": ["fleet-sync"],
    "plugins": ["workflow", "field-guide", "guardrails"]
  },
  "environments": [
    {
      "environmentId": "an-environment-id", "label": "a-machine",
      "agents": ["codex"],
      "exclude": { "skills": [], "plugins": ["guardrails"] }
    }
  ]
}
```

If no roster exists, enroll the machines the user identifies. In T3, get the local identity with `t3_environment_read` and the agent's existing grants with `t3_environment_links`. A linked-environment list is not the client's saved-connection inventory. Ask for the missing fleet scope when neither the user nor a roster supplies it. Store only confirmed IDs and labels; T3 owns addresses, credentials, and access grants.

When the user requests every linked environment, include the current environment and every existing link. Enroll newly included IDs before starting updates. Retain roster members that are temporarily unlinked or offline in the report. A baseline is an explicit selection; preserve it instead of asking for the same selection each run. Agent targets default to Codex and Claude Code. Per-environment `agents` chooses their skill/plugin targets; `exclude.skills` and `exclude.plugins` leave those items unmanaged. Omissions preserve installed extras.

For every enrolled remote machine, match its ID against the linked list. Request a missing or expired link with `t3_environment_link`, passing its ID and label as the hint. Request only the access needed for the authorized refresh. A pending card is an automatic wait; resume when its result arrives. A permission denial or offline machine remains an explicit incomplete result. Continue reachable machines. Keep valid grants; do not relink each run.

Outside T3, use only a user-configured remote execution method. A fleet roster does not authorize discovering credentials or creating SSH access.

## Run the updater

Use a clean checkout tracking published `main`, with no local commits. Prefer the canonical checkout when it qualifies. When it is on a development branch or has local work, leave it alone and use an independent clone at `$XDG_CACHE_HOME/filip-stack/fleet-source` (default `~/.cache/filip-stack/fleet-source`). Verify an existing clone's repository identity, branch, cleanliness, and upstream; preserve collisions and edits. Create a missing clone from `https://github.com/filipgutica/filip-stack.git` without `--depth`. Use the installed command's `--repo` option to select it. An inspection uses an existing checkout; report missing source as bootstrap required instead of cloning or fetching.

Send the exact policy bytes to each child as data, with its environment ID, for a temporary `--config` file. A refresh saves that policy as the machine's own after validating it, so every machine keeps the shared policy. The updater backs up a differing saved copy beside it as `fleet.json.bak-<UTC time>`, and leaves a symlinked saved copy to the tool that owns its source. For inspection, `--dry-run` leaves local configuration untouched.

Run `filip-stack --repo <checkout> sync --config <policy-file> --environment-id <id> --json`. For inspection, add `--dry-run` and report planned results as a plan. Record the policy digest and effective profile from each result.

For a refresh, if the launcher or checkout predates `sync`, fast-forward the selected clean main checkout and run `node <checkout>/scripts/sync.mjs --config <policy-file> --environment-id <id> --json` directly. For inspection, use existing source and retain `--dry-run` on direct invocation; report unsupported source without updating or bootstrapping it. Report the older launcher separately. Refresh a Homebrew launcher only when authorized, checking that it will not upgrade unrelated dependencies. Leave Claude, Codex, runtimes, services, and unrelated packages at their installed versions.

When chezmoi already transports shared Field Guide preferences, read [preference transport](references/preferences.md) before the updater. Its inspection route is read-only; only refresh may pull or merge preferences. Respect an unfinished setup phase: leave an uninitialized chezmoi installation untouched. No automatic dotfiles commits or pushes belong to fleet refresh.

Use local tools for the current machine. For another linked T3 machine, use `delegate_task` with `target.environmentId` and its filip-stack project ID from `t3_project_list`. Read `orchestrator_capabilities` before the first delegate. Use the host's available Implementer target; disclose any required fallback. Give the child only this outcome, its host's applicable rules, the canonical checkout, the command, the boundaries below, and the required report. The child does its work without further delegation. Follow async completion instructions; do not poll or open a top-level thread.

The updater installs missing baseline items and refreshes existing filip-stack installations. It preserves plugin enabled states, scopes, explicit pins, existing skill host assignments, and local text outside managed guidance blocks. Missing required clients and ownership collisions remain blocked. A local edit or an unverifiable installation is a conflict, not permission to force replacement. Guidance applied from an unmerged or unverified revision is retained until it is contained in the selected source or all managed content already matches. Independent skills/plugins continue.

## Accept the result

Require exit status and the complete JSON result from every machine. Read a delegated result before accepting its claims. Check:

- Source commit and every component's state; a failed component cannot become an overall success.
- One shared policy digest, with each machine's declared exceptions applied. For a refresh, the `configuration` component's `savedPolicy` state is `saved` (report its backup), `current`, or `symlink` (the saved copy stays stale until its owner updates it).
- Guidance applied commit and target count, skills and their host assignments, plugin versions and verified payloads.
- Explicitly pinned, disabled, missing, blocked, and unreachable components.
- Preservation of machine-local rules and unrelated installations.

Compare observed commits and versions across machines. Different pins or installation selections may be intentional; label them. If an upstream update landed during the run, report that difference and rerun the affected machines against the current source when authorized. Do not call different versions synchronized.

Return one row per enrolled machine, including those that could not run. Name the remaining action beside each incomplete result. Keep the per-machine last-run report at the path returned by the command. Tell the user to restart Claude and start a fresh Codex thread to load updated plugins; keep their active sessions running.
