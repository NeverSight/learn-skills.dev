---
name: port-permissions
description: "Configure Port's role-based access control: context lake (blueprint/entity) permissions (read, register, update, or delete entities, down to a single property or relation) and page/dashboard view/edit permissions. Use when asked to 'set up Port permissions', 'restrict who can edit an entity', 'only let the owning team modify this blueprint', 'add a dynamic read policy to a blueprint', 'control who can view a Port dashboard or catalog page', or 'why can this user see/edit something they shouldn't'. Out of scope: permissions on a Workflow's `SELF_SERVE_TRIGGER` node, including its dynamic policy (`port-workflows` owns that), permissions for Port's legacy Actions & Automations product (deprecated in favor of Workflows, not covered by any skill in this repo), and inviting users or creating teams themselves (Port's platform administration docs own that, this skill only covers what roles and teams can be granted once they exist)."
license: MIT
compatibility: "Claude Code, Cursor, Codex CLI, GitHub Copilot"
metadata:
  version: "1.0.0"
  author: port-labs
  repository: https://github.com/port-labs/port-skills
  tags: port,permissions,rbac,security,reference
  summary: Configure Port's RBAC across the context lake and pages
---

# Port permissions

Port's RBAC shows up in two independent places that reuse the same
`roles`/`users`/`teams` shape: context lake entities (a blueprint's `read`,
`register`, `update`, `unregister`) and pages/dashboards (`read`, `update`).
This skill covers both, plus the roles and ownership model that backs them.

Permissions on a workflow's own `SELF_SERVE_TRIGGER` node are a separate,
simpler mechanism owned by the `port-workflows` skill, see
[its permissions reference](../port-workflows/references/permissions.md)
instead of this one.

## Prerequisites

- Go over the `port-getting-started` skill first if this is your first time
  working with Port.
- The blueprint or page whose permissions you're changing already exists.
- If Port's MCP server is connected, use `list_blueprints` to read current
  blueprint definitions before editing, and `simulate_blueprint_permissions`
  to test a context lake permission change before applying it. There is no
  MCP tool that writes permissions directly, every step below applies
  changes through the raw API, UI, or Terraform. Search
  `search_port_knowledge_sources` for anything this skill doesn't cover.

## How to configure it

1. **Know the two building blocks every permission type reuses**: Port's
   three roles (Admin, blueprint Moderator, Member) and the `$team`
   ownership meta-property that backs every `ownedByTeam` flag. See
   [references/roles-and-ownership.md](references/roles-and-ownership.md).
2. **Set context lake (blueprint/entity) permissions**: who can `read`,
   `register`, `update`, or `unregister` entities of a blueprint, down to a
   single property or relation, a dynamic `read` policy, and the built-in
   permission simulator. See
   [references/context-lake-permissions.md](references/context-lake-permissions.md).
3. **Set page and dashboard permissions**: who can view or edit a catalog
   or dashboard page. See
   [references/page-permissions.md](references/page-permissions.md).
4. **Setting permissions on a workflow trigger instead?** That's a
   different, simpler shape scoped to one `SELF_SERVE_TRIGGER` node, not
   this skill, use the `port-workflows` skill's
   [permissions reference](../port-workflows/references/permissions.md).

Steps 2 and 3 are independent, do whichever the task needs.

## Examples

- [assets/context-lake-permissions-ownership-and-policy.json](assets/context-lake-permissions-ownership-and-policy.json):
  a blueprint's `entities` permissions combining role/user/team grants,
  `ownedByTeam` registration, and a dynamic `read` policy.
- [assets/page-permissions-patch.json](assets/page-permissions-patch.json):
  a `PATCH` body giving a team `read` access and restricting `update` to
  Admins.

## Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Set `ownedByTeam` and a dynamic `read` policy on the same scope, only one works | When entity owner permissions are configured, the dynamic read policy is ignored | Pick one: `ownedByTeam` for team-based access, `policy` for anything else |
| Granular `updateProperties` grant has no effect | A global `update` permission is also set, global overrides granular | Remove the global `update` grant, or fold the property-level grant into it |
| User can't register a new entity even though `register` allows their role | The entity also has a required property or relation they lack `updateProperties`/`updateRelations` access to | Grant edit access to every required field, not just the top-level `register` scope |
| `PATCH`ing page permissions removed a role's/user's/team's access unexpectedly | `PATCH` replaces each key you include entirely; omitting an existing member of that key removes them | Include the full desired list for every key you send, not just the ones you're adding |
| Terraform permission resource conflicts with UI edits | `port_page_permissions` fully owns the resource once applied | Manage a given page's permissions from one place, Terraform or the UI, not both |
| Trying to add a dynamic `queries`/`conditions` policy to a workflow trigger | That shape belongs to Port's legacy, deprecated Actions & Automations permissions, not Workflows | Use the simpler `policy` (`combinator`/`rules` over `user`/`userTeams`/`form` context) documented in `port-workflows`' [permissions reference](../port-workflows/references/permissions.md) instead |

## Quick reference

- Three roles: Admin (everything), blueprint Moderator (everything on one
  blueprint), Member (read + execute workflows by default).
- Context lake entity permission scopes: `read`, `register`, `unregister`,
  `update`, `updateProperties.<property>`, `updateRelations.<relation>`.
  Each takes `roles`/`users`/`teams`/`ownedByTeam`; `read` also takes a
  dynamic `policy`. API: `GET`/`PATCH /v1/blueprints/{id}/permissions`.
- Page permission scopes: `read`, `update`. Each takes
  `roles`/`users`/`teams`. API: `PATCH /v1/pages/{id}/permissions`.
- For a workflow's `SELF_SERVE_TRIGGER` node permissions (a different,
  simpler shape scoped to one trigger), see the `port-workflows` skill's
  [permissions reference](../port-workflows/references/permissions.md)
  instead of this one.
