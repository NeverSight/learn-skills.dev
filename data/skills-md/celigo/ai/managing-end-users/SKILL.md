---
name: managing-end-users
description: Manage Celigo MCP end users -- people who use an account's MCP servers without workspace access -- and the groups, roles, capability sets, and grants that decide which tools, APIs, prompts, and resources each one can call. Covers inviting and revoking, granting per server, groups and roles, what removing a capability set does to grants, compiled effective access, and end users' own connections. Use when giving people or teams access to a Celigo OAuth MCP server, changing or removing that access, or working out why someone can or can't call a tool.
---

<!-- TIER:1 -->

# Managing End Users

An end user is a **person's access record for MCP servers only**: they sign in to the account's MCP servers through Celigo OAuth (routed to the company's identity provider where one is set up) and get no workspace access. What each one may call is the union of their grants -- direct, through groups, through roles, and through capability sets. Concerns when managing end users:

- **Records** -- invite, accept, revoke; identity-provider provisioning (JIT, SCIM); suspending
- **Grants** -- capability strings per MCP server, on a person, a group, or a role
- **Groups and roles** -- shared access, and memberships that are manual or synced from the identity provider
- **Capability sets** -- named bundles of a server's items, granted as one unit
- **Effective access** -- the compiled result, per person or per server
- **End users' own connections** -- the credentials each person supplies where a server asks for them

End users are a separate record type from workspace users. The same person can hold both -- the end-user record then shows `hasWorkspaceShare: true` -- and changing or removing one never touches the other. The **account owner** is never an end user: the owner reaches every server without a record, is never listed, and can't be invited. Only the owner and administrators manage end users, groups and roles.

## How to Run the Steps

This skill names each step by what it reads or changes; the exact calls depend on how you reach the account. Read the one reference that matches your tools -- both follow the step numbers of How to Manage End Users below:

- **Celigo MCP tools** -- [references/mcp.md](references/mcp.md). The deployed server has no end-user, group, role or grant tools, and its user tools cover workspace users only; it can maintain a server's capability sets, so most steps go to the CLI or the integrator.io UI.
- **The `celigo` CLI** -- [references/cli.md](references/cli.md)

Identity-provider setup (JIT sign-in, SCIM, group claims) and suspending an end user happen in the integrator.io UI on either surface.

## How Access Composes

A person can call an item on a server when any of these grants it -- effective access is their union:

- **Direct grants** on the end user's record
- **Group grants** on each group they belong to
- **Role grants** on each role pinned to one of those groups, or listed on the person's own record
- **Capability sets** named by any of those grants

Each grant names one MCP server, or none -- a wildcard across every server in the account -- and lists capabilities:

| Capability | Grants on that server |
|---|---|
| `tool:all`, `tool:<id>` | Tools -- a `tools[]._toolId`, or an upstream tool row's `_id` |
| `api:all`, `api:<id>` | APIs -- an `apis[]._apiId` |
| `prompt:all`, `prompt:<id>` | Prompts -- a `prompts[]._id` |
| `resource:all`, `resource:<id>` | File resources -- a `resources[]._id` |
| `pset:<id>` | Every member of a capability set -- a `permissionSets[]._id` |

Each `:all` covers only its own kind: grant every kind the server exposes. An id that isn't on the server, or any other shape, is refused with 400. Grant prompts as `prompt:<id>` -- an older `tool:<prompt id>` grant still saves but effective access doesn't report it.

End-user grants decide access on servers that sign people in with Celigo OAuth ([building-mcp-servers > Who may use the server](../building-mcp-servers/SKILL.md#who-may-use-the-server)).

## Quick Reference

### Decision Matrix

| You need to... | Do this |
|---|---|
| Give one person access to one server | Invite them with a grant on it, or grant it to their existing record |
| Give a team access | A group with the grant; add the people as members |
| Reuse one bundle of access across several groups | A role carrying the grants, pinned to each group |
| Maintain "which items" on the server, granted as a unit | A capability set on the server, granted as `pset:<id>` |
| Suspend someone and keep their grants | The UI's toggle on the end user -- no CLI or MCP command |
| Remove someone's MCP access | Revoke their end-user record |
| See who can reach a server, and why | The server's effective access |
| See what one person can reach | That person's effective access |

### Record Fields

- `_id` -- the access-record id (the `ashareId` every end-user call takes); the person's own user id is `_sharedWithUserId`
- `provisionedBy` -- `invite`, `jit` (first sign-in through the identity provider), or `scim` (pushed by the identity provider, which then owns the active state and its synced memberships)
- `accepted`, `dismissed`, `disabled` -- invited until setup completes; declined; suspended
- `groupMemberships[]` -- `{_groupId, source}`, `source` being `manual` or `idp`
- `resourceGrants[]` -- direct grants: `{resourceType: "mcpServer", _resourceId, capabilities}`
- `hasWorkspaceShare`, `lastSignIn` -- read-only, joined into the list

### Field Reference

The full shapes are in the API reference's [End Users](https://developer.celigo.com/api/api-reference/account-and-admin/end-users.md), [Groups](https://developer.celigo.com/api/api-reference/account-and-admin/groups.md) and [Roles](https://developer.celigo.com/api/api-reference/account-and-admin/roles.md) pages (agent-readable markdown).

## Related Skills

- [building-mcp-servers > Who may use the server](../building-mcp-servers/SKILL.md#who-may-use-the-server) -- the server side: sign-in modes, capability sets in the server document, whose login a call runs on
- [managing-users > 5. Disable or remove a user](../managing-users/SKILL.md#5-disable-or-remove-a-user) -- workspace users; offboarding someone means checking both records
- [managing-network-policies > Where a Policy Applies](../managing-network-policies/SKILL.md#where-a-policy-applies) -- restricting where end users can sign in from

<!-- TIER:2 -->

## How to Manage End Users

### 1. Check who has access

List the end users: each row has the access-record id, `provisionedBy`, `accepted`, `disabled` and `hasWorkspaceShare`. Workspace-user lists leave end users out, and reading an end user's id through the workspace-user routes answers 404 "AShare not found.". Then list the groups and roles, and read effective access (step 7) for the server or person in question.

### 2. Decide how to grant

Direct grants suit one-offs; groups suit teams; a role suits one bundle reused across groups; a capability set suits a named subset of one server's items that you'd rather maintain on the server than in every grant. Cover every kind of item the server exposes.

### 3. Invite

Invite one address, or up to 100 at once, optionally adding the same groups and direct grants to each. Every invite sends a real invitation email, so only invite addresses whose owners expect it. The record starts as invited (`accepted: false`) and already counts in effective access; it becomes active when the person completes setup.

- An address that already has an end-user record is refused with 409 `enduser_ashare_exists` -- change that record's access instead. A bulk invite answers 200 with a per-address result, so read each one.
- The owner's address is refused with 400 `owner_self_invite_not_allowed`.
- People can also arrive from the identity provider (`jit`, `scim`); that's configured in the UI.

### 4. Grant access on a server

Granting on a server **replaces** the listed people's or groups' grant on that server with exactly the capabilities you send -- up to 100 targets per call. Their grants on other servers and their wildcard grants stay. A batch stops at the first failure and reports what it completed, and an id that isn't an end user (or group) of the account rejects the whole call before any change. Send the complete list of capabilities each time; to remove someone's grant on a server altogether, use the UI.

Read effective access afterwards (step 7).

### 5. Manage groups and roles

- **Group and role names** are unique in the account, case-insensitively (409 otherwise).
- **Members** are added and removed by access-record id, up to 100 per call. Adding someone already in the group changes nothing, and the reply's `updated` counts every listed id either way. Memberships synced from the identity provider (`source: idp`) can't be removed here (409): change the person's group in the identity provider.
- **Editing a group or role replaces it.** A full update without `resourceGrants` or `_roleIds` empties them -- every member loses the access the group gave, while keeping the membership. Read it first and send everything back, or change single fields with a read-modify-write.
- **Pin roles to groups** through the group's `_roleIds`. An end user's own `_roleIds` isn't writable through the API.
- **Deleting a role** unpins it from every group; **deleting a group** removes it from every member's `groupMemberships`. Neither can be restored from the recycle bin today (Gotchas).

### 6. Grant through capability sets

A capability set lives in the MCP server document (`permissionSets[]`): a `name` unique on the server, case-insensitively, and the ids of items already on the server (`_toolIds`, `_apiIds`, `_promptIds`, `_resourceIds`). Its `_id` is the handle grants use (`pset:<_id>`), and changing its members changes what every grantee can call.

Sets change through a full update of the server, which is where access can shift without a warning:

- **Removing a set** -- leaving it out of the update, or sending it back renamed without its `_id` -- rewrites every grant that names it into its members' own capabilities (`pset:<set>` becomes, say, `api:<id>`). The grantees keep that access, but it no longer follows the set: a set added later, even under the same name, reaches none of them until they're granted it again.
- **A set sent back without its `_id`** keeps its `_id` and its grants when its name still matches the stored set's (ignoring case).
- **`accessLevel`** on a set isn't stored, so it doesn't narrow anything.

Building and updating the server document itself: [building-mcp-servers > Gotchas](../building-mcp-servers/SKILL.md#gotchas).

### 7. Check effective access

- **Per server** -- every end user who can reach it, with each item's source: `direct`, `group:<name>`, `role:<name> (group:<name>)`, or `pset:<set> (direct)` / `pset:<set> (group:<name>)`. An empty result means no end user has been granted the server (the owner is never listed).
- **Per person** -- their groups, roles, and for each server the items they get and the items they're denied, with the reason ("Not in any granted permission set or api grant").

Both are recompiled on every read. Read them after every grant change, and before handing someone a server's URL.

### 8. Suspend, revoke, or offboard

- **Suspend** with the UI's toggle on the end user: access stops and the record, groups and grants stay. There's no CLI or MCP command for it -- the workspace-user disable commands can't find an end-user record.
- **Revoke** to remove the person's MCP access: the record is deleted with its group memberships, the person's own connections for MCP servers are invalidated, and any workspace record they hold is untouched. Inviting the address again creates a fresh record with none of the old grants or groups.
- **A `scim` record** is the identity provider's: deactivate the person or change their groups there, or its next push undoes a change made here. Direct grants and manual memberships are never touched by SCIM.
- **Offboarding** someone with both kinds of access means revoking the end-user record and removing the workspace user ([managing-users > 5. Disable or remove a user](../managing-users/SKILL.md#5-disable-or-remove-a-user)).

### 9. Manage end users' own connections

Where a server requires end-user credentials on a connection, each end user's credentials live in a private copy of it (`connectionRole: mcpChild`) -- see [building-mcp-servers > Whose login a call uses](../building-mcp-servers/SKILL.md#whose-login-a-call-uses). The copies are listed per server and read one at a time, credentials masked. Deleting one makes that person connect again before using the tools that need it; a deleted copy can't be restored, and only the end-user connection route deletes one.

<!-- TIER:3 -->

## Pre-Submit Checklist

Before inviting, granting, or changing groups, roles or sets, verify:

- [ ] Every address invited belongs to someone who expects an invitation email, and none is the account owner's
- [ ] Each grant covers every kind of item the server exposes (`:all` covers only its own kind), with ids that are on that server
- [ ] A per-server grant call carries the complete capabilities for every listed person or group -- it replaces their grant on that server
- [ ] A group or role update carries `resourceGrants` and `_roleIds` (and the description) in full
- [ ] A server update that touches `permissionSets` keeps every set you mean to keep, with its `_id`
- [ ] Effective access shows the intended result before the server's URL goes to anyone

## Gotchas

1. **End users and workspace users are separate records.** Workspace-user lists omit end users, workspace-user commands answer 404 for an end-user id, and removing one record leaves the other in place.
2. **A per-server grant replaces, not appends.** The listed targets end up with exactly the capabilities sent on that server. Nothing on the CLI or MCP removes a grant outright -- that's the UI.
3. **Each `:all` covers one kind.** `tool:all` alone leaves the server's APIs, prompts and resources denied.
4. **Group and role edits are full replaces.** A group updated with only a new name keeps its members and silently drops their access.
5. **Removing a capability set unties its grants.** The grantees keep the access as plain `tool:`/`api:` grants, and a replacement set -- even with the same name -- reaches none of them.
6. **A set without its `_id` is matched by name.** The same name (any case) keeps the set and its grants; a new name makes a new set and removes the old one.
7. **No suspend outside the UI.** The CLI's and MCP server's disable and enable work on workspace users only.
8. **Revoking is final for that record.** A new invite starts from nothing; re-create the groups and grants.
9. **Deleted groups and roles can't be restored from the recycle bin.** The bin currently lists the account's live groups in place of deleted ones, and roles not at all (live-verified 2026-10-21). Read a group or role before deleting it.
10. **The audit log shows little of this.** Changes to end-user records appear as `user` events on the person's user id without the grants or groups that changed, and changes the platform makes on its own -- a removed set's grants rewritten, a deleted role unpinned -- aren't recorded on the group. Group and role edits you make are recorded with their fields.

## Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| 409 "An end-user share for this user already exists in this account." (`enduser_ashare_exists`) | The address already has an end-user record | Change that record's access instead of inviting again |
| 400 `owner_self_invite_not_allowed` | The address is the account owner's | Nothing to do -- the owner reaches every server without a record |
| 400 "Validation failed. Invalid capability: …" | A kind other than `tool`, `api`, `prompt`, `resource`, `pset`, or a malformed id | Use the grammar in How Access Composes |
| 400 "Validation failed. API … is not attached to MCP server …." | The id isn't on that server (or names another kind) | Read the server and use its own entry ids |
| 409 "A group with this name already exists in the account." / "A role with this name already exists in the account." | The name differs only in case from an existing one, or matches it | Pick another name |
| 409 `conflict` removing members | A membership was synced from the identity provider | Change the person's group in the identity provider |
| 404 "AShare not found." | An end user's id passed to a workspace-user command | Use the end-user commands |
| 404 "End-user share not found in this account." | The record was revoked, or the id is wrong | List the end users |
| Signed in, but a tool is missing or every call is refused | No grant covers that item's kind on this server | Read the person's effective access; grant the missing kind |
| Members lost access after a group change | The group update left out `resourceGrants` or `_roleIds` | Restore them from the group's audit entries' old values |
