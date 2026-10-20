---
name: platform-role-hierarchy-apply
description: "Bulk-realign an existing Salesforce UserRole hierarchy from an external org-chart artifact (PDF, xlsx, or plain-text list of role-and-parent pairs) in one admin-approved manifest. Clarify scope and whether users move with roles, resolve identities that do not match verbatim, diff the artifact against the current tree, and submit create, rename, reparent, empty-role delete, and user-assignment mutations together. Triggers on \"reorganize the role hierarchy\", \"apply this org chart to roles\", \"bulk update role parents\", \"realign roles from PDF\", \"restructure the role hierarchy\", \"reparent roles from this spreadsheet\". Do not trigger for a single role create, rename, or reparent with no other changes, or for asking which roles exist or how they are nested — that is `managing-roles`. Do not trigger for territory, account, or forecast hierarchies, or for authoring sharing rules."
metadata:
  version: "1.0"
---

# Role Hierarchy Restructure

Apply many UserRole changes from an artifact in one admin-approved manifest.

If the admin only asks which roles exist or how they are nested, hand off to `managing-roles`. Do not query, do not ask the step 0 questions, and do not submit.

## Inputs

- PDF org chart (text-selectable), `.xlsx` / `.csv` with `role_name` and `parent_role_name` (empty parent = top-level), or plain text with one `Role: Parent` pair per line.
- Or a pre-parsed list of `{roleName, parentRoleName}` objects.
- Optional mapping hints when a chart name is not the org's `Name` or `DeveloperName`.

## Flow

### 0. Clarify before querying

Ask anything still unresolved. Do not guess.

- **Scope.** Default is selected branches: roles absent from the artifact stay. "Full hierarchy" still does not delete those roles unless the admin asked for each deletion.
- **User reassignment.** Default is no. Do not emit `AssignUser` or `MoveUser` without an explicit yes.
- **Ambiguous identities.** Resolve every role and user in one batch. See step 2.
- **Conflicts.** Two parents for one role, or a role parented to itself: stop until the admin picks.

If the artifact matches fewer than 20% of its roles to the current tree, stop and ask whether it is a greenfield replacement, the wrong file, or a mapping problem. Do not build a manifest until the admin confirms a greenfield replacement. Between 20% and 50%, show the fraction in the preview and continue.

### 1. Read the current hierarchy

```text
SELECT Id, DeveloperName, Name, ParentRoleId
FROM   UserRole
LIMIT  10000
```

Match artifact roles by `DeveloperName`, then case-insensitive `Name`.

### 2. Parse the artifact and resolve identities

Normalize to `{roleName, parentRoleName, users?}` and show that list to the admin before the diff. A PDF that is not text-selectable cannot be parsed. Ask for a plain-text `Role: Parent` list.

Roles: exact `DeveloperName`, then case-insensitive `Name`. No fuzzy match. When more than one role matches, list each candidate's `DeveloperName` and `Id` and wait. Do not pick one. Unresolved names go back to step 0.

Users, only after reassignment was confirmed:

1. 18-character id starting with `005` → `User.Id`
2. Email → `User.Email`
3. Username → `User.Username`
4. Display name → `User.Name`, and only when exactly one active user matches

`IsActive = false` is a non-match. A user listed under two roles is a conflict. Ask which role that user should land under, or whether to drop the reassignment. Do not submit until the admin answers.

Stop on a cycle in the target graph. Report the path, for example `A → B → C → A`, and ask for a corrected artifact. Do not submit.

### 3. Build the manifest

Each mutation has `operationId`, `operationType`, `dependsOnOperationIds`, and one nested payload. `dependsOnOperationIds` is the order that matters.

| operationType | Nested object | Use when |
|---|---|---|
| `CreateRole` | `createRole` | Role is in the artifact and not in the org. Set `roleReference`, `developerName`, `name`, and `parentRoleId` or `parentRoleReference`. Default the three account-owner access fields to the org defaults when the artifact omits them. |
| `ReparentRole` | `reparentRole` | Role exists and the parent differs. Set `targetRoleId` or `targetRoleReference`, `expectedParentRoleId`, and `desiredParentRoleId` or `desiredParentRoleReference`. |
| `RenameRole` | `renameRole` | Same role, different label or developer name. Set the expected and desired name fields. |
| `DeleteRole` | `deleteRole` | Admin asked to remove an empty role. Set `targetRoleId`, `expectedParentRoleId`, `expectedAssignedUserIds`, and `expectedDirectChildRoleIds`. |
| `AssignUser` or `MoveUser` | `userRoleAssignment` | Reassignment was confirmed. Set `userId`, `expectedCurrentRoleId`, and `desiredRoleId` or `desiredRoleReference`. |

`DeleteRole` applies only when the role has no direct children and no assigned users at the moment it runs. Reparent those children and move those users in earlier mutations, and put those `operationId`s in `dependsOnOperationIds`. The delete's expected user and child lists are then empty. If the admin declined reassignment, do not delete a role that still has users.

A mutation that names a role neither in the org nor created in this manifest is `missing-parent`. Name the roles that point at it. Ask whether to add a `CreateRole` for it in this manifest, skip those rows, or abort. Do not submit with that parent missing.

A cycle in `dependsOnOperationIds` blocks the submit. Give every new role a `roleReference` string and point parents and assignments at that string.

### 4. Validate, then preview

Block the submit when any of these remain: a cycle, a missing parent, a duplicate `developerName`, a dependency cycle, an `AssignUser` or `MoveUser` without the step 0 yes, a `DeleteRole` whose expected user or child lists are not empty, or overlap under 20% without a confirmed greenfield replacement.

On a duplicate `developerName`, show both rows and wait until the admin picks one or renames one.

Warn in the preview, and continue only after an explicit yes:

- A changed role is referenced by `Territory2.UserRoleId` or a forecast hierarchy override.
- A changed role has `PortalType != 'None'`.
- A changed role has more than 500 users (`SELECT COUNT() FROM User WHERE UserRoleId = :id`).

```text
Restructure preview
-------------------
  ReparentRole : 42
  CreateRole   :  3
  RenameRole   :  1
  DeleteRole   :  2
  MoveUser     :  2

  Territory / forecast references : 1
  Portal roles                    : 0
  Roles with more than 500 users  : 2

Approve this restructure? [yes / no]
```

`yes` submits. Anything else does not. Roles left in the org and absent from the artifact stay in place.

### 5. Submit

```text
POST /services/data/v{version}/sharing/role-hierarchy-restructure
{
  "operation": "Save",
  "mutations": [
    {
      "operationId": "reparent-sales-vp",
      "operationType": "ReparentRole",
      "dependsOnOperationIds": [],
      "reparentRole": {
        "targetRoleId": "00E000000000001",
        "expectedParentRoleId": "00E000000000002",
        "desiredParentRoleReference": "cro"
      }
    },
    {
      "operationId": "delete-legacy-region",
      "operationType": "DeleteRole",
      "dependsOnOperationIds": ["reparent-legacy-children"],
      "deleteRole": {
        "targetRoleId": "00E000000000003",
        "expectedParentRoleId": "00E000000000002",
        "expectedAssignedUserIds": [],
        "expectedDirectChildRoleIds": []
      }
    }
  ]
}
```

`CreateRole`, `RenameRole`, `AssignUser`, and `MoveUser` use the same envelope with their nested object from step 3.

Send the approved manifest once. Do not edit `UserRole` records one by one.

### 6. Read the response

- `Applied` — structural and sharing changes committed.
- `AppliedSharingPending` — hierarchy is live; sharing catches up on its own. Do not poll.
- `AsyncExecutionRequired` — the server queued the manifest. Do not poll.
- `RoleOperationInProgress` — another restructure is running. Stop. Do not queue the manifest. Ask the admin to retry once the other operation finishes.
- `NotApplied` — nothing committed. Show `reasonCodes` and stop.
- `404` on submit — API not enabled for this client tier. Halt, tell the admin, do not retry, do not fall back to per-record `/sobjects/UserRole` edits.

For each `operationResults[]` entry, `outcome` is `Applied`, `NotApplied`, or `DependencyNotApplied`. Show `reasonCode` for any entry that is not `Applied`. Do not retry and do not roll back.

## Out of scope

- A single role create, rename, or reparent with no other changes, and any request that only asks which roles exist or how they are nested (`managing-roles`).
- Territory, account, and forecast hierarchies.
- Authoring sharing rules.
- Image-only PDFs. Ask for text.
- Rollback. Report what the response says was committed.
---

<!-- skill-validate: ignore-start -->
<!-- codey:operations start -->
## Operations Reference

Operations this skill uses — routing and dependency reference.

| Operation | Purpose | Status | Call | Depends on |
|-----------|---------|--------|------|------------|
| `read-role-hierarchy` | read | — | `GET /services/data/v68.0/query` | — |
| `count-users-per-role` | read | — | `GET /services/data/v68.0/query` | `read-role-hierarchy` |
| `submit-role-hierarchy-restructure` | write | — | `POST /services/data/v68.0/sharing/role-hierarchy-restructure` | `read-role-hierarchy` |
| `verify-role-hierarchy-restructure` | verify | — | `GET /services/data/v68.0/query` | `submit-role-hierarchy-restructure` |
<!-- codey:operations end -->
<!-- skill-validate: ignore-end -->
