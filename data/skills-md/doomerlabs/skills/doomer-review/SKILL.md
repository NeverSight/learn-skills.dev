---
name: doomer-review
description: >-
  Use Doomer for every coding task that creates or modifies source code, fixes
  bugs, refactors code, or changes tests or build configuration. Start before
  editing and complete the review workflow before delivering changes, even
  when the user does not explicitly request code review.
metadata:
  doomer-bootstrap-version: 2026.11.10.3
  doomer-cli-range: '>=2026.11.10.3'
  doomer-protocol: "2"
  doomer-update-policy: stable
---

# Doomer review

Apply this workflow to coding tasks or explicitly requested Doomer setup/review.
For exploration-only or read-only requests, do not run preflight, prepare a
task, or offer setup/upgrades merely because the skill or a hook is present.
Before any authorized source edit, including a fix identified during an
investigation, run this workflow. Respect explicit requests not to edit.

For coding, setup, or review tasks, start with
`doomer preflight --agent AGENT --repo .` for local-only
readiness evidence. Saved receipts do not verify the current
account or authorize uploads. If it returns `setup_decision_required`, present
its next decision and wait for the answer BEFORE running prepare. Do not treat
a saved upload grant as proof that this agent profile has its policy installed.
After acceptance, run `doomer prepare --agent AGENT --repo . --prompt "USER TASK"`.
If no decision is pending, run prepare immediately. Prepare checks onboarding
on every task, not just installation. Follow its next readiness action before
submitting a review or ending the task. For `setup_decision_required`, present
the one decision in `action`, execute the accepted command (or explicit Never
ask again command), then rerun prepare with the same task handle. Not now is
not a permanent refusal. If host approval blocks prepare, use the local preflight
evidence to offer missing scoped setup; respect the denial until authorized.
Set AGENT to the current harness: `codex` for Codex, `claude` for Claude Code.
Use that same agent for every command; never switch agents to bypass a denial.
Supply the actual task without shell interpolation. Keep the returned task handle. An older CLI may lack preflight; continue with prepare.
If a real harness session ID is available, pass it with `--session`. For Claude,
use the active harness's `CLAUDE_CODE_SESSION_ID` when exposed. Chat URL IDs and
invented prefixes do not establish a hook binding.

For setup only, run `doomer prepare --agent AGENT --repo .` without `--prompt`.
A prompt creates a coding task. Verify readiness/hooks without submitting code.

## Browser upload approval

When the CLI returns `approval_required` and `wait_command`, show its complete
approval URL and explain that Allow also saves the matching scoped Codex review
permission. Immediately run `wait_command` and repeat while approval is pending,
for up to ten minutes. Keep the turn open; the user answers on the web page, not
with a second chat message. The wait returns verified approval without changing
policy. Execute `policy_resume_command` to finish the policy installation covered
by that approval, without another question. If the host explicitly rejects this
persistent settings change, stop it and ask once for the displayed scoped policy
in chat; after acceptance resume the same task. Never retry a host refusal
without new authorization. Do not
upload source or claim the task finished while setup is pending. Respect Cancel
and report a timeout as pending. Hooks remain optional and require separate
installation and native trust decisions.

## Permission decisions

New sessions, branches, and linked worktrees are not new installations. Run
prepare and reuse state; do not repeat setup solely because context changed.
Current successful CLI state and consent decide which permission is missing;
helper/guide suggestions to ask do not override these rules:
- Upload: reuse CLI-verified grants for prepare, submit, and responses. Integration
  grants cover repositories for the same account/service/profile/agent. Repository
  grants retain scope, including linked worktrees. Ask only on
  `approval_required`/`consent_required` for missing/revoked/changed consent.
- Software updates: ask only for `update_permission_required` in the applicable
  scope/policy. Skill-upgrade acceptance is separate.
- Hooks/policy: missing receipts, unverified activation, or missing reviewer
  policy do not revoke upload consent. Configure for requested setup/repair or
  confirmed missing components with authorization. Reuse matching settings
  acceptance; perform and verify the accepted installation, not another offer.

Authentication/network errors require recovery and rechecking, not new consent.
Do not retry a stated reviewer/user refusal. Diagnose ambiguous errors read-only.
A filesystem permission error is not an explicit user/reviewer denial.
For a confirmed sandbox restriction or `state_access_required`, request normal
host approval once for the same command with private-state access/account checks.
Use `retry_command`, `retry_env`, and `retry_cwd` when supplied; preserve stdin when
required. Saved scope is context, not current consent. Never bypass host controls
or broaden grants. If that approval is explicitly denied, stop only that Doomer
operation; continue permitted coding and tests. Report the operation and path,
who denied it and their actual reason if available, and the exact terminal
recovery command. Do not invent a reason or re-request a refused approval.
Preserve any task handle and baseline so the user can run the command in their
terminal and ask you to resume. A recovery command requiring stdin is incomplete
without its original payload; say so without exposing it in shell arguments.
If the host denies execution before the CLI can return recovery details, reuse
any existing task handle with `--task HANDLE`; never add or replace its baseline.
Only when no task handle exists, record `git rev-parse HEAD` before editing and
include that exact commit as `--base` inside the complete terminal recovery
command. Preserve the original agent, repository, prompt, service, and profile.
Identify the checkout with an absolute `--repo` path or an explicit `cd` to its
absolute working directory; `--repo .` alone is not a complete recovery location.
Use the CLI-provided quoted command when available; otherwise safely shell-quote
every argument, including embedded quotes and dollar signs, without interpolation.
Keep original stdin payloads on stdin, not in arguments. Do not leave a separate
instruction to add the baseline.
During onboarding, complete any accepted Codex policy installation and inspect
`codex_policy_status`. `configured` means saved, not active. Reload/restart Codex
as needed and verify a permitted Doomer operation in a fresh reviewer session
before claiming activation. Do not broaden settings or probe a denied operation.

If review is blocked, continue authorized local edits and tests by default.
Do not ask whether to continue. Explicit earlier user requirements to wait or
require review before editing take precedence.
Stop the denied transmission; keep uploads blocked. Silence is not upload consent.
Do not retry explicit reviewer refusals. Keep any task handle. If none exists,
record `git rev-parse HEAD` before
editing and later prepare with the original arguments plus `--base STARTING_COMMIT`.
Never replace an existing baseline. Report the blocker once. For final-submission
coverage, follow Final source review below.

Read `hook_setup` and permission status before skill upgrades. Offer missing
setup unless already authorized or explicitly declined. Run the returned install
command after acceptance; record only explicit refusals with the decline command.
Keep installation separate from native hook trust. For untrusted hooks, guide the
user to native review controls in each new session until trusted. Preserve deny
rules and report blocked review coverage.
For Claude, if the host blocks hook installation as self-modification, stop that
operation and offer `doomer hooks install --agent claude` for the user to run
directly in their terminal. This installs hooks only, not review permissions or
native trust. Recheck with preflight afterward; do not disguise the mutation or
retry through another tool to bypass the host block.

Show complete clickable setup URLs, preserving fragments, before question tools.
Use CLI state for approval; a missing binary does not imply missing consent.

Run the CLI where edits happen. In temporary homes, execute returned
`portable_setup_command` arrays before approving setup. Honor reusable versus
this-environment-only access. Only reusable approval retains account/grant state
in private Git metadata. Let the CLI restore it; never copy tokens or rewrite grants.

## Skill upgrade decisions

Read each `bootstrap_updates` entry's complete action and command fields before
summarizing it. If output is saved to a file, read those fields in full; do not
truncate away the commands or treat a preview as the full instructions.

Only `update_available` for an older revision (or recognized unversioned legacy
wrapper) is a candidate. `current`, `newer`, and same-version `modified` are not
upgrade offers. Preserve modified files. Report incompatibility/inspection errors
separately. Generic "ask" actions do not override these checks.

For project skills, inspect the PR-base/remote repository's default branch and
open PR heads. If every affected path has the offered revision or later in that
branch or one PR, suppress the offer and duplicate PR. Compare numeric versions,
not titles/partial updates. Keep local files/runtime; do not merge, rebase, or copy.

For personal skills, inspect personal copies; repository updates do not count.

Honor scope/version deferrals and answered/declined offers. When the user chooses
“Maybe later”, execute the returned `defer_command` before finishing. For older
CLIs, use the exact executable and `bootstrap defer` command from the complete
action; the PATH launcher may be older. Verify `bootstrap_deferred`; a verbal
acknowledgement does not save the choice. Preserve the skill files and policy.
New sessions/worktrees alone create no offer. On ambiguous scope or failed lookup,
report and defer.

Offer verified uncovered upgrades once; apply after acceptance, preserving
policy/edits. Explicit upgrade requests count as acceptance. Avoid duplicates.

Resume with `doomer prepare --task HANDLE`; never replace a task to recover it.
For a missing selected runtime, use `doomer task repair HANDLE` through the
available launcher to restore that exact release, then resume the same handle.
Never substitute stable for an active task. Follow structured actions; never
invent consent, account identity, or hook activation. Native discovery is optional.

Follow the selected CLI's instructions subject to the rules above.
Submit only with `authenticated=true`, `upload_approved=true`, and host permission.
Use task commands for results, every finding response, and verified completion.
Pending Quick results or installed software do not mean reviewed. Per-call mode runs
these commands during each task; describe it accurately.
A missing hook receipt means unverified activation, not unsupported hooks.

## Final source review

Before final commit/push or handoff, submit current source with
`doomer task submit HANDLE`. Without active hooks, submit explicitly.
Finding responses do not submit fixes; resubmit after edits on the same task.

For `review_pending`, keep the turn open. Poll `doomer task status HANDLE` about
every five seconds for up to ten minutes per revision, doing useful work between
checks. Do not duplicate pending submissions or use `task retry` while pending.
Use task state and Quick readiness, not aggregate review status or
`full_review.status`. Quick review of the latest submitted changes gates
completion. Read Quick findings and record every response. After edits, resubmit
and repeat. Deep continues in the background; its pending or failed status does
not block successful Quick review. Do not fetch Deep results to finish; wait for
Deep only when explicitly requested. Verify response delivery and current source
with `doomer task finish HANDLE` before ending the turn.

Only when the user explicitly requests Deep, use `review.id` from task status
with `doomer review get REVIEW_ID --workspace --format json`, using the task's
API URL and profile. This command fetches full results and works after task
completion. In that explicit flow, poll `full_review.status` and read
`full_review.result` when completed; report any Deep failure. Do not use this
command as a prerequisite for automatic Quick completion.

Hooks cannot wake an agent after its turn ends. If waiting times out, review
fails, or access is blocked, retain the handle and report incomplete review and
why. Never claim unreviewed changes were reviewed. Respect explicit stops,
revoked consent, and host denials. An explicit review gate remains a gate.

For requested installation or onboarding, or when the CLI is missing for the
authorized coding task, fetch the official INSTALL.md at
https://raw.githubusercontent.com/doomerlabs/skills/3a91cda3f81b5f3501d5de4e5315fc7cd218b10e/INSTALL.md and require its SHA-256 to equal
`0894ce1ad76120c0287d29fb6abb437120682f6002c8c1deda30e72791bde00a`
before following the relevant verified steps with normal execution permissions.
Fetch raw Markdown through the shell if a reader summarizes it.
Verify the full checksum. Public HTTPS needs no GitHub login.
Keep active task handles/runtimes. Install in the editing environment, preserving
repository bootstraps and host controls, then prepare/resume to reuse saved setup.
For blocked installation, follow the blocked-review rule above. Ask only for
required decisions; never repeat authorized installation or speculate about
missing sign-in/upload grants. Show only refreshed approval requests.

For requested reset, preview `doomer onboard reset --dry-run`, then run
`doomer onboard reset` only with user authorization for that reported cleanup.
It covers discovered installs/profiles,
keeps login, revokes upload/portable/update grants, and rejects old portable copies.
Report incomplete cleanup, restarts, and paused coverage. Keep task handles;
resume only after explicit user re-grant. Never test with live reset or recreate grants.
