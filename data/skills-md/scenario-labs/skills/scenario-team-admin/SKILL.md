---
name: scenario-team-admin
description: "Use when administering a Scenario team from an agent through MCP: restricting which models a team or project can run (model access control, allowlist, blocklist), inviting or removing team and project members, changing roles, capping a member's Creative Unit spend, auditing API keys and their roles or scopes, or attributing consumption per user or model. Keywords: governance, model control, consumption cap, spend limit, API key hygiene, team admin, enterprise."
license: MIT
---

# Scenario Team Administration

## Overview

Enterprise teams govern Scenario from the same agent that generates on it: which models anyone may run, who is on the team and in which projects, how much each member may spend, and which API keys exist with which roles. Every tool here is catalog-only: `scenario_tools_search` returns the schema and lane, and `scenario_tool_execute_read` / `write` / `delete` runs it with `{name, parameters}`, scope ids inside `parameters` (see the `scenario` skill). Two facts decide most failures before any argument does: the identity behind the call, since team-level writes need a human team admin over OAuth and refuse API keys, and the list mode the team runs, since the same model-access edit means the opposite thing in blocklist and allowlist mode. `teams_list` already tells you both: each team row carries `modelsManagement`, its model lists, `plan`, and `context.userRole`. A credential that reaches one team and one project has its scope; more than one is a stop-and-list, per the `scenario` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Task                 | Tool                                                               | Lane                 | Notes                                                                                |
| -------------------- | ------------------------------------------------------------------ | -------------------- | ------------------------------------------------------------------------------------ |
| Read model access    | `model_access_get`                                                 | read                 | Mode plus the team's active list; `project_id` adds that project's list alongside it |
| Change model access  | `model_access_update`                                              | write                | `level` `team` or `project`; exactly one of `add_models`, `remove_models`            |
| Team roster          | `team_members_list`                                                | read                 | Members and pending invitations                                                      |
| Invite               | `team_members_add`                                                 | write                | 1 to 32 `emails`, `role`, optional `project_ids` joined on acceptance                |
| Roles and spend caps | `team_members_update`                                              | write                | `member_ids` 1 to 32; `role` and/or `max_consumption`                                |
| Remove from the team | `team_members_remove`                                              | delete               | Also withdraws invitations; access ends immediately                                  |
| Project roster       | `project_members_list`, `_add`, `_update`, `_remove`               | read, write, delete  | Roles `admin` (Owner), `editor` (Contributor), `reader` (Viewer)                     |
| API keys             | `api_keys_list`, `api_key_get`, `api_key_update`, `api_key_delete` | read, write, delete  | Project scope; `api_key_create` returns the portal link and nothing else             |
| Who spent what       | `usage`                                                            | read (default tools) | Per-user and per-model consumption in the default response                           |

## Model access: read the mode before editing

`model_access_get` returns `models_management` and only the mode's active list; the inactive stored list is never surfaced. In blocklist mode (the default) every catalog model is available except those on the team or project blocklist, and the two lists block as a union. In allowlist mode a model is available only when it sits on both the team and the project allowlist; a project with an empty allowlist denies every model, and a project with no allowlist configured falls back to the team list.

`model_access_update` edits whichever list the mode makes active, so `add_models` blocks in blocklist mode and allows in allowlist mode: read the mode first, every time. Switching the mode is not available through MCP; it lives in the web app's team settings, so locking a team down to an approved set starts with the user flipping to allowlist there. Unattended, that switch is a stop-and-report: log that the lock waits on it and the exact calls that follow, and take the blocklist-safe partial (blocking the named unwanted models at project level), saying that other projects stay open. Narrowing a list the credential can edit is in scope when the task states the target set: `remove_models` runs after the adds succeed, so the list never ends empty. `level: "team"` needs a team admin over OAuth, and the server refuses API keys on that endpoint. `level: "project"` takes the projects to edit in `projects` (1 to 200) and needs the admin role on every one of them: one unauthorized project fails the whole request and nothing updates, and a single-project key can only edit its own project's list. `project_id` on the call is tenant context for OAuth sessions, never the target. In allowlist mode a project admin can add only models already on the team allowlist (a project list narrows the catalog, never widens it), removing a base model from a team allowlist cascade-removes the trained models built on it, and a team-level add validates every id, one unknown id failing the whole call. `updated: false` means the diff was a no-op, not an error. A blocked model disappears from what members can run, and the error a member sees when running one anyway is a restriction, not moderation (see `scenario-moderation`).

## Members and spend caps

`team_members_update` takes `member_ids` from `team_members_list` and sets `role` (`admin` or `member`), `max_consumption`, or both. The cap is in Creative Units over the current billing period: a value of zero or more caps, `-1` is unlimited, and `null` clears the per-member override so the team-wide default applies. Roles can be set by a team admin over OAuth or a team-scoped API key with the `team.members.manage` scope; caps need a real team admin, and a key that tries is refused per member. Demoting the last admin fails server-side. The bulk member tools process one row at a time and report an outcome per member; a response with `status: "partial"` is finished by calling again with its `remaining` list.

`team_members_add` invites 1 to 32 emails at `role` (default `member`) and joins them to `project_ids` on acceptance; outcomes are `invited`, `failed`, or `skipped` with the reason (already a member, already invited, seat limit reached). `project_id` on the call grants nothing. Like role changes, inviting takes a team admin over OAuth or a team-scoped key with `team.members.manage`; a project-scoped key gets a permission error. A pending invitation carries no member id, so its cap waits for acceptance. `project_members_add` takes people already on the team, as user ids or emails (emails need `team_id` to resolve), with a required project role.

Removal is the delete lane and immediate: `team_members_remove` ends the person's access everywhere and withdraws pending invitations, `project_members_remove` leaves team membership and other projects untouched. List first, confirm the exact names with the user, then remove; unattended, remove only the members the task instructions name.

## API keys

`api_keys_list` and `api_key_get` are project-scoped and return each key's `id`, `api_key_id`, name, status, scope, role, projects, and creation date, plus a `manage_keys_url`; team-scoped keys are not attached to projects and never appear here, only in the portal. `api_key_update` changes a key's `role` to `admin`, `editor`, `reader`, or a custom `;`-separated scope list (the reference's example is `assets.read;models.run`); name, status, and usage limits are portal-only, and a limit takes an Enterprise plan and a human admin. Creation is deliberately not an MCP operation: `api_key_create` returns the portal link, the secret is shown once there, and it never passes through the conversation (the `scenario` skill's rule on secrets holds here). `api_key_delete` takes the key as `key_id` (either the `id` or the `api_key_id` from the listing), cannot be undone, needs a project admin, and refuses the key the current session is authenticated with: list, confirm the exact key with the user, then delete; unattended, delete only a key the task instructions name and exactly one key matches.

## Who spent what

`usage` is in the default toolset and returns a summary by default: headline CU totals, per-user consumption, per-model CU and job counts sorted descending, and per-asset-kind counts, bounded by `start_date` and `end_date` (ISO dates); `project_id` filters the figures, so a single-project credential ranks spend inside that project, not across the team. An undated call returns project-lifetime figures, so always pass the range: `totals` and the per-user `consumption` rows (`userId`, `total`) follow `start_date` and `end_date`, and a member ranking comes from those rows. The per-day series (`include: ["usages.daily"]` per usage type, `["modelUsages.daily"]` per model) carry no user dimension; `nsfwUsages` adds moderation totals and `activity` the raw event log. Never attribute spend by adding up your own calls. Read consumption before setting caps: both are in CU over the billing period, and a cap below what a member has already spent stops them at once.

## Worked example: lock a project to approved models and cap the contractors

1. `scenario_tools_search` with `query="model access"`, then `query="team members"`: schemas and lanes for the calls below.
2. `scenario_tool_execute_read` with `name: "model_access_get"`, `parameters: {"team_id", "project_id"}`. The team is in blocklist mode, so "only these three models" is not expressible: tell the user to switch the team to allowlist in the web app's team settings, then re-read; unattended, log the gap with the calls below and stop, blocking any models the task names as unwanted at project level in the meantime.
3. In allowlist mode, the team list first: `scenario_tool_execute_write` with `name: "model_access_update"`, `parameters: {"team_id", "project_id", "level": "team", "add_models": [<the three ids>]}`; this is the call that needs the caller to be a team admin over OAuth (`context.userRole` on the `teams_list` row says whether they are). Then the project: `level: "project"`, `projects: [<project id>]`, the same `add_models`, which succeeds only because the team list now carries them.
4. `scenario_tool_execute_read` with `name: "team_members_list"`: the two contractors' member ids. `scenario_tool_execute_write` with `name: "team_members_update"`, `parameters: {"team_id", "project_id", "member_ids": [<two ids>], "max_consumption": 2000}`. On `status: "partial"`, call again with `remaining`.
5. `scenario_tool_execute_read` with `name: "api_keys_list"` for the project. A render-farm key running as `admin` is narrowed with `api_key_update`, `role: "assets.read;models.run"`, and any key nobody can account for is deleted only after the user confirms it by name.
6. Confirm: `model_access_get` with `project_id` shows the project list `configured` with the three ids; later in the period, `usage` with the date range and `include: ["usages.daily"]` shows the contractors' consumption against the cap.

## Common mistakes

- Editing model access without reading `models_management`: `add_models` blocks in one mode and allows in the other.
- Trying to lock a team to a short list while in blocklist mode: that is an allowlist job, and the mode switch is a web-app setting.
- Team-level writes through an API key: refused by design; the caller is a human team admin over OAuth.
- `arguments` instead of `parameters` on the executor: dropped silently and surfaced as a scope error (see `scenario`).
- Setting caps with a `team.members.manage` key: it can change roles, not caps.
- Reading an undated `usage` call as the period's spend: its figures are project-lifetime. Pass `start_date` and `end_date`, rank members from the dated `consumption` rows, and use the per-day series only to cross-check a period total, since it carries no user dimension.
- Expecting `api_keys_list` to show team-scoped keys: they exist only in the portal.
- Passing `project_id` to `team_members_add` to grant project access: `project_ids` grants; `project_id` is tenant context.
- Deleting a key or removing a member without listing and confirming first: the delete lane is irreversible, and `api_key_delete` refuses the session's own key.
