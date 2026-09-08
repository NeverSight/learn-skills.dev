---
name: use-subagents-codex
description: Orchestrate one or more Codex subagents for a user-requested task.
compatibility: Requires Python 3.11+ in a POSIX environment with advisory file locking for profile installation, and Codex multi-agent tooling that supports the resolved worker model and reasoning effort.
---

# Use Codex Subagents

Orchestrate Codex subagents for the requested task. Keep the skill and custom-agent identity stable across worker-model upgrades. The bundled TOML defines the worker defaults; an explicit worker model or reasoning effort in the user's request overrides the matching default. Parent model and reasoning settings remain outside this managed profile.

## Execution contract

- Use at least one subagent unless multi-agent tooling is unavailable or doing so would violate a safety or permission boundary.
- Do not skip delegation merely because the parent could complete the task alone. For a small or tightly coupled task, use one subagent as the focused executor or independent verifier.
- The parent remains responsible for decomposition, user-facing decisions, synthesis, verification, and the final answer.

## Preserve the parent runtime

- Leave the parent model and reasoning effort exactly as selected for the current Codex CLI or ChatGPT Desktop Work mode session.
- Never set, override, or persist a parent `model` or `model_reasoning_effort` on behalf of this skill.
- Do not change model or reasoning settings in `$CODEX_HOME/config.toml`, a profile, command-line options, application settings, or the active parent session.
- Do not derive the subagent model or effort from the parent, and do not apply the subagent settings to the parent.
- Apply the resolved worker model and reasoning effort only to workers spawned by this skill.

## Resolve the worker profile

Read the top-level `model` and `model_reasoning_effort` values from `assets/use-subagents-codex.toml` as defaults. Resolve the profile before reconciling or spawning:

- An explicit worker model in the user's request replaces the bundled model default.
- An explicit worker reasoning effort replaces the bundled effort default.
- Use the bundled value for either setting the user leaves unspecified. Never inherit the missing setting from the parent.
- Normalize an unambiguous display name to the exact model identifier exposed by the spawn surface. For example, `5.6 sol` means `gpt-5.6-sol` only when that identifier is available.
- Verify that the spawn surface supports the resolved model and effort. If it does not, report the unsupported setting rather than substituting another profile.
- The renderer can represent `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`, and `ultra`. This is a serialization allowlist, not a promise that any particular model or runtime supports every value. Verify the selected pair before installing or spawning it.

Thus, a request to use this skill "but 5.6 sol high" resolves the worker profile to `gpt-5.6-sol` with `high` reasoning, regardless of the bundled defaults.

## Reconcile the managed custom agent

The bundle owns one stable custom-agent identity with a bundle-controlled template:

- bundled source: `assets/use-subagents-codex.toml`
- profile renderer: `scripts/configure_worker_profile.py`
- installed target: `$CODEX_HOME/agents/use-subagents-codex.toml`, falling back to `~/.codex/agents/use-subagents-codex.toml` when `CODEX_HOME` is unset
- custom-agent name: `use_subagents_codex`

Treat the bundled file as canonical for every field except a user-requested worker model or effort. Render the resolved model and effort into the installed target with [scripts/configure_worker_profile.py](scripts/configure_worker_profile.py); do not hand-edit either TOML. This managed target is intentionally replaced when the template, bundled defaults, or explicit worker settings change. Local customizations belong in a different custom-agent file with a different `name`.

1. Resolve this skill directory and the effective Codex home. The renderer requires Python 3.11+, POSIX file permissions, and advisory file locking; use a supported environment for installation rather than claiming native Windows permission guarantees.
2. Run the renderer with the resolved `--model`, `--reasoning-effort`, and `--dry-run`. It compares the fully rendered profile and required `0600` permissions with the installed target and prints intended profile changes without writing files or changing permissions.
3. If both content and permissions already match, continue without writing.
4. If the target is missing, differs, or needs a permission correction, show the dry-run output. Obtain approval through the execution environment before writing outside the workspace, then rerun without `--dry-run`.
5. Rely on the renderer to create a timestamped backup beside a content-differing target, replace it atomically, and restrict the installed file and backup to the current user. For matching content with incorrect permissions, it repairs permissions without rewriting content or creating a redundant backup.
6. Do not modify `$CODEX_HOME/config.toml` preemptively. If the effective runtime reports that multi-agent tools are disabled, explain the blocker and request approval before changing only `[agents].enabled` to `true`. Do not override managed policy or alter any model or reasoning setting.
7. Do not use a Codex version heuristic unless a concrete runtime failure requires compatibility diagnosis.

The renderer resolves the effective Codex home first. Within that home, `agents` must be a real directory and an existing installed profile must be a regular file with a single hard link. Symlinked directories, symlinked profiles (including dangling links), hardlinked profiles, and special files are rejected in dry runs and writes. Report the blocker; do not unlink, follow, or change permissions on a referent to bypass it. Changing that layout requires separate user authorization.

The renderer pins the opened `agents` directory for file operations and creates backups and temporary files with `0600` permissions before writing content. A failed copy removes its incomplete file; backup creation never overwrites an existing backup. Rendering must produce the requested top-level model and effort without changing other parsed TOML fields. A template that fails that check is rejected before installation.

Non-dry-run reconciliation creates or reuses the private sidecar
`$CODEX_HOME/agents/.use-subagents-codex.lock`. The renderer holds its advisory
lock while re-reading the target, checking for changes, creating a backup, and
replacing content or repairing permissions. A competing write fails with an
already-in-progress error; rerun the dry run after that operation finishes rather
than bypassing the lock. Dry runs neither create nor acquire the lock and remain
read-only observations, not reservations for a later install.

Keep the lock file in place: unlinking it could let writers coordinate on
different inodes. A symlinked, hardlinked, special, or other-user-owned lock is
rejected for writes. Report that blocker rather than replacing the lock or
changing a referent. The lock coordinates cooperating renderer invocations; it
does not protect against unrelated programs that ignore the locking protocol.

The renderer changes only the installed custom-agent file, its private backup,
and the private coordination lock, never the bundled template. If it creates or updates the installed content during the current session, do not assume the session reloaded it. Prefer the exact-runtime fallback from the next section, or require a fresh session rather than claiming the new definition ran. A permission-only repair does not change the profile content.

## Select the worker

Use the first available path that preserves both resolved worker settings:

1. Spawn the custom agent named `use_subagents_codex` when the current session has already loaded the resolved profile.
2. Otherwise, when the spawn surface accepts explicit model **and** explicit reasoning-effort overrides, pass both resolved values to a built-in `worker`. Include the worker constraints below in the assignment.
3. Do not use an explicit-model fallback that cannot also preserve the resolved reasoning effort; it could accidentally inherit the parent's effort.
4. If neither exact path is available, report that the requested subagent profile cannot be executed in the current session. Do not silently substitute the parent model, another worker model, or another reasoning level.

When runtime metadata exposes the selected worker model, reasoning effort, or custom-agent path, verify it. Otherwise state only what the runtime actually confirms. Never treat the installed TOML alone as proof of the runtime used.

## Choose the delegation topology

Use the minimum number of workers that satisfies the explicit request:

- **One worker by default.** Use one for a coherent implementation, investigation, transformation, test pass, or independent verification.
- **Multiple workers only for independent work packages.** Parallelize when each package has distinct inputs or read scopes and can return a useful result without another worker's intermediate output.
- **Read-heavy work parallelizes more safely than writes.** For concurrent write work, assign disjoint files or directories and account for shared manifests, lockfiles, generated outputs, and migrations. If ownership overlaps, serialize the work or use one worker.
- Honor a user-specified worker count or decomposition when feasible, but reduce it when concurrency, permissions, or conflicting write scopes make that unsafe or ineffective. State the adjustment.

Do not let workers recursively spawn more agents.

## Build each assignment

Give every worker a self-contained brief containing:

1. objective and acceptance criteria;
2. allowed inputs and relevant context;
3. explicit read-only or write scope;
4. prohibited actions and stop conditions;
5. expected output format;
6. checks or evidence required before returning.

Use these constraints in every brief, including exact-runtime fallback workers:

- Work only on the bounded assignment.
- If the objective, inputs, scope, or acceptance criteria are missing or contradictory, stop and report the ambiguity instead of guessing.
- Remain read-only unless a write scope is explicitly assigned.
- Modify only assigned files or directories and preserve unrelated user changes.
- Do not broaden the task, make unrequested product or architecture decisions, publish changes, push commits, contact people, or perform irreversible external actions.
- Do not spawn subagents.
- Run targeted checks that could falsify the result when useful and permitted.
- Return the result, supporting evidence, files changed or `none`, checks and outcomes, and any blocker or uncertainty.

## Consolidate and verify

Wait for all requested workers. Resolve ambiguity and cross-worker conflicts in the parent rather than widening a worker's scope. Inspect material changes, reconcile outputs, and run proportional final verification. The final response must distinguish worker findings from parent verification and must not overstate worker model, reasoning-effort, or runtime certainty.
