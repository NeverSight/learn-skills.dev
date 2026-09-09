---
name: delegate-ui-to-claude
description: "Delegate all frontend and UI implementation or review to Claude Code with Impeccable, while Codex owns scope, contracts, coordination, and validation. Explicit invocation only."
---

# Delegate UI to Claude

Claude Code owns the delegated frontend/UI layer end to end, including
component behavior and all resulting UI edits. Codex acts as the PM and
integration owner: settle intent, define boundaries and contracts, launch
Claude, inspect the result, and route revision feedback back to Claude.

## Workflow

1. Define the handoff.
   - Read the applicable instructions, plans, design documents, and current
     working-tree state.
   - Separate Claude-owned frontend/UI paths from Codex-owned backend, domain,
     data, infrastructure, and cross-layer integration work. Stabilize any
     interface contracts Claude needs before delegation.
   - Resolve consequential product or design questions that remain unsettled
     and undelegated with the user first.
     The delegated CLI run is non-interactive, so decisions discovered after
     Claude inspects the project must be relayed through Codex rather than
     inferred silently.
   - Classify the handoff before launching Claude:
     - Apply existing explicit unattended authority within its stated scope;
       it may cover the remaining choices and permit a one-shot run.
     - Use mediated approval when `PRODUCT.md` is missing, the work creates a
       new surface or visual world, the request is a redesign or rebrand, or
       consequential product or design choices remain.
     - Use a one-shot run only for scoped work that inherits an established
       product and visual world, or when the user explicitly authorizes Claude
       to make the remaining decisions unattended.
   - Record concrete acceptance criteria, responsive states, accessibility
     expectations, required validation, and paths or changes that must remain
     untouched.

2. Verify and provision the delegate.
   - Confirm `claude` is available and inspect `claude --version`.
   - Work from the relevant UI repository root. Confirm that repository has a
     Claude-scoped Impeccable installation at
     `.claude/skills/impeccable/SKILL.md` and that Claude resolves
     `/impeccable`; Codex having a similarly named skill does not establish
     that dependency.
   - Keep Impeccable unavailable to Codex. Before provisioning, check for:
     - `.agents/skills/impeccable` in the current repository;
     - `~/.agents/skills/impeccable` or `~/.codex/skills/impeccable` at user
       scope; and
     - Impeccable hook entries in the repository's `.codex/hooks.json`.
   - Report detected Codex-facing artifacts and do not remove them without
     explicit authorization. An instruction naming the exact artifact is
     sufficient. Before removing repo-local `.agents/skills/impeccable`, verify
     that it resolves inside the repository, is not a symlink, and contains no
     unrelated files. In `.codex/hooks.json`, remove only Impeccable entries.
     Require separate authorization for each user-scoped path.
   - Recheck after cleanup and stop until all conflicts are gone. If this task
     already discovered Impeccable, continue only in a fresh task. Create it
     with the requested resume prompt when asked and supported; otherwise tell
     the user to start it.
   - Invoke Impeccable through `npx` with `@latest` so every delegation checks
     the current published CLI instead of relying on a long-lived local
     binary. If the Claude installation is absent, install it before
     delegation:

     ```text
     npx --yes impeccable@latest install -y --providers=claude --scope=project
     ```

   - If the Claude installation already exists, refresh that project-scoped
     copy before delegation:

     ```text
     npx --yes impeccable@latest update -y --providers=claude --scope=project
     ```

   - Install Impeccable only after confirming the current repository contains
     the UI work being delegated. Use only `--providers=claude` with
     `--scope=project`; never install it for Codex, use `--scope=global`, add
     another provider, or provision it in a repository that is only
     coordinating backend or integration work.
   - After installation or refresh, verify that
     `.claude/skills/impeccable/SKILL.md` exists and that no Codex-facing
     artifact listed above was created. The intended repository exposure is
     Claude only.
   - Treat Impeccable-created `.claude` files as project changes: preserve
     pre-existing files, inspect the resulting diff, and include them in the
     final changed-file report.
   - Do not silently fall back to Codex implementing the UI.

3. Build a complete approval or implementation prompt.
   - Choose the Impeccable command that matches the task: a general
     `/impeccable` request for end-to-end creation or redesign, `init` to
     establish missing project design context, `polish` for targeted
     implementation refinement, `critique` for review of hierarchy and UX, or
     `audit` for accessibility, performance, and responsive quality.
   - Start the prompt with `/impeccable`; append the chosen command when the
     task uses one. For review-only work, explicitly prohibit edits.
   - State that Claude owns the frontend/UI implementation end to end.
   - Include the objective, user intent, design/product context, editable
     scope, non-goals, existing contracts, constraints, acceptance criteria,
     validation commands, and relevant pre-existing changes.
   - Require visual iteration in the browser when the project and Claude
     integration support it. Cover representative desktop and mobile states.
   - Tell Claude not to commit, push, rewrite unrelated changes, or alter
     backend/domain logic. If a contract change is needed, it must report the
     need for Codex to resolve.
   - For implementation, require a final report containing changed files,
     design decisions, validation results, and any remaining limitations.

4. Mediate approval when the handoff requires it.
   - Start Claude in `plan` permission mode with an approval-discovery prompt.
     Tell it to inspect the project without editing, avoid opening or waiting
     on an interactive decision page, and return the next product questions or
     design options to Codex instead of choosing or inferring an answer.

     ```text
     claude -p --permission-mode plan --effort high --output-format json < /absolute/path/to/approval-discovery.txt
     ```

   - Require an approval packet with `status` set to `needs_approval` or
     `ready_to_implement`, the exact questions or options, Claude's evidenced
     recommendation and tradeoffs, and the exact proposed contents of any
     PM-owned planning artifact that must exist before it can discover the
     next decision.
   - Capture the JSON `session_id`. Resolve the packet from confirmed decisions
     and delegated authority first. If `needs_approval` identifies a material
     decision outside that authority, relay the exact options and wait for its
     answer; resume the same session in `plan` mode with that answer. When
     `ready_to_implement` has no unresolved material choice, continue without
     another approval request.

     ```text
     claude -p --resume <session-id> --permission-mode plan --effort high --output-format json < /absolute/path/to/approval-response.txt
     ```

   - If Impeccable needs a PM-owned planning artifact such as `PRODUCT.md`
     before it can derive the next options, check Claude's exact proposal against
     approved direction and delegated authority. Ask only for unresolved material
     substance. Within that authority, Codex writes only the PM-owned artifact,
     inspects its diff, and resumes Claude in `plan` mode. Give Claude write
     permission only once all material choices are approved or delegated.
   - If the user authorizes unattended decisions, record that authorization in
     the handoff and let Claude use Impeccable's unattended fallback instead of
     manufacturing an approval.

5. Launch implementation from the repository and working directory that own
   the UI. Resume the approved Claude session when mediation occurred; otherwise
   start a new one-shot session. Prefer the current model-classified permission
   mode so Claude can implement without an unconditional permission bypass:

   ```text
   claude -p --permission-mode auto --effort high --output-format json < /absolute/path/to/handoff.txt
   ```

   - For an approved mediated session, add `--resume <session-id>` to that
     command and include every confirmed answer and choice in the handoff.
   - Write the complete prompt, beginning with `/impeccable`, to a task-scoped
     temporary file and pass it through standard input. Do not interpolate
     user or repository text into a shell command.
   - Add `--chrome` when Claude's Chrome integration is available and visual
     browser iteration is required.
   - If `auto` is unavailable, use `acceptEdits` and add narrowly scoped
     `--allowedTools` entries for the exact repository validation and dev
     commands Claude needs.
   - Never use `--dangerously-skip-permissions` or
     `bypassPermissions` for this workflow.
   - Preserve session persistence and capture the JSON `session_id`; approval
     phases and later revisions must continue the same context.
   - If Codex's sandbox blocks Claude's normal authentication, session, or
     network access, request the narrow escalation needed to run `claude`.

6. Supervise without taking over.
   - Do not edit Claude-owned frontend/UI files while the delegated run is
     active.
   - Inspect Claude's result, the working-tree diff, and the reported
     validation. Check scope, contracts, user intent, and repository
     integration independently.
   - Route incomplete work and visual or UX feedback back to the same Claude
   session instead of patching the UI directly:

   ```text
   claude -p --resume <session-id> --permission-mode auto --effort high --output-format json < /absolute/path/to/revision.txt
   ```

   - Begin the revision prompt with `/impeccable polish`, followed by the
     specific findings and acceptance gaps.
   - Let Claude correct its UI work. Codex may change only the separately
     established PM/integration-owned scope, then resume Claude if the
     frontend must adapt.

7. Finish only after Claude's UI implementation and Codex's integration checks
   both pass. Report the ownership split, changed files, validation evidence,
   and any visual checks that could not be completed.
