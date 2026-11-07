---
name: hanchou-init
description: >-
  Initialize or update a project's Hanchou responsibilities, sokkin startup
  configuration and tool readiness when explicitly requested. Offer installation
  of missing tools with the user's chosen method. Does not launch agents or scheduling.
metadata:
  version: 2.0.0
---

# Initialize Hanchou

Select the exact Git project root. Resolve existing `.hanchou` paths/symlinks
before writing; preserve existing policy text and custom settings. A selected
external/shared destination must not be overwritten as if it were local.

## Tool readiness

Check Git, Bash 3.2+, jq, Herdr, ccusage and the selected official agent CLI on
the intended execution host. Record resolved executable paths, versions and
existing package-manager ownership. A missing PATH entry is not proof that a
tool is uninstalled; inspect existing installations before adding another copy.
Reuse compatible installed tools. Do not silently upgrade, downgrade or replace
an installation to match a version number.

Herdr 0.9.5 and ccusage 20.0.37 are qualified baselines, not hard-coded minimum
versions or requirements to use a particular installer. For another version,
check installed help and the required local-session/usage contracts; changed
log or output formats need renewed qualification before real work.

If a tool is missing, present the concrete tools, available versions, destination
and installation method for the user to choose. Offer Homebrew when available
and an official direct installation where supported; explain runtime differences
such as native ccusage versus the Node wrapper used by npm. Read current official
[Herdr](https://herdr.dev/docs/install/) and
[ccusage](https://ccusage.com/guide/installation) guidance and package metadata.
Refresh stale package metadata before concluding a version is unavailable.
Do not install a package manager implicitly or default to npm on every platform.

An already explicit installation choice authorizes that installation; do not ask
again. Otherwise wait for the choice, then install the selected missing tools
outside the project using their existing installer/package manager. If declined
or blocked, continue independent project configuration and report the missing
dependency. Do not substitute a different method after failure without agreement.
Keep unrelated packages, shared settings and existing resources intact.

Verify executable resolution, versions and required help after installation.
Check the selected CLI's authentication status without exposing credentials or
starting inference; guide the user only when interactive login is needed.
Claude must use subscription authentication, never an API fallback.
Mission launch creates an owned named server by default; init itself still starts
none. `.hanchou/instances` holds local lifecycle evidence, never credentials or
policy. Preserve existing records and use the project's ignore policy for them.
If an authorized named local Herdr session already exists, check PATH and auth
in an available shell pane without disturbing agents; otherwise report the
in-session checks as pending. Do not create/start a server, service or agent just
to pass initialization. Where existing identified logs are available, verify
offline usage against native records. Missing identity/logs are pending, not
zero usage, and tool installation alone does not establish mission readiness.

## Project configuration

Record settled authority, completion checks and reporting preferences in
`.hanchou/policy.md`, using [the policy template](assets/policy-template.md)
only for relevant sections. Use the user's language and preserve an existing
policy's language unless a translation was requested. Ask only for material
missing choices; settled instructions need no second confirmation.

Write `.hanchou/config.json` with `version: 2` and `sokkin.agent` (`codex` or
`claude`) plus optional `sokkin.model` (null means the CLI's configured default).
For a new configuration without a user preference, use the copyable
[config template](assets/config-template.json): Codex, `gpt-6-astra`, `medium`.
This prioritizes sokkin's planning, delegation, verification and integration
judgment; it is not a measured guarantee of lower total usage.
Explicit user choices and existing settings, including null or omitted optional
values, take precedence. Do not replace them with the template on reinitialization.
For another provider, choose its supported model/effort rather than carrying
Codex model names across. Never infer consent to API billing from a model choice.
Claude is subscription-only. Configuration is JSON data, not shell code.
Budget and allowed model choices may be recorded in `policy.md` or the mission.
Optional `sokkin.effort` is `low`, `medium`, `high` or null; null/omission uses the
CLI default. A bounded routine mission may explicitly choose a lighter sokkin,
such as Sol/low. Worker selection is separate: prefer the least costly approved
model sufficient for the assigned work, with Sol as a candidate when available.
Verify model availability before launch and observed model/effort after startup;
do not silently substitute an unavailable default or start inference during init.

Keep the supervisor focused on purpose, acceptance criteria, authority and budget.
Sokkin owns the execution plan; do not make the supervisor pre-plan every worker
assignment just to support a lighter sokkin. Evaluate total mission usage and
rework, not just the sokkin's own token count.

Keep local configuration ignored by default through the repository's actual
`git rev-parse --git-path info/exclude`; preserve an explicit versioned/shared
choice and already tracked files. Do not change shared `.gitignore` or global
settings merely to initialize a project. Never store credentials in `.hanchou`.

Report source paths, chosen agent/model, delegated authority, tool versions and
installation methods, plus completed and pending readiness checks.
Include a compact reusable readiness handoff with observation time, host, resolved
tool paths/versions, selected named Herdr session and its configuration source
(when checked), provider log-home provenance, authentication route and pending
checks. Omit credentials, full configuration and CLI command listings. If
observed host restrictions require individual approval for Herdr or shared Git
metadata, record the restriction and successful connection route with host/time
evidence. This records a route, not permission for future operations.
When local setup is requested, keep this report at `.hanchou/readiness.md` under the
same local-only policy; preserve unrelated/custom content. It is optional evidence,
not a registry or a claim of future readiness: later missions verify actual
placement, changed sources, live launcher state and new native identity/usage.
Initialization does not create a worktree, start an agent, activate a schedule
or delete old `.hanchou` artifacts.
