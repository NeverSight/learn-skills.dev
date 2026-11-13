---
name: manage-portal-members-and-prospects
description: |
  Manage the lifecycle of API Experience Hub portal members and prospects.
  Use when an admin needs to approve or reject prospects (candidate users),
  list active members, inspect and update a member's user-group assignments,
  or disable a member. Also create prospects as an alternative to the portal's
  built-in self-registration. Covers the join → approve → assign → disable flow.
---

# Manage Portal Members and Prospects

## Overview

Manage the membership lifecycle of an API Experience Hub (AEH) portal. Prospects normally request access through the portal's built-in self-registration and are not yet portal members; members are active users with assigned user groups. Review and approve or reject those prospects, audit the member list, adjust user-group assignments per member, and disable members who should no longer have access. When you do not want to use the built-in self-registration, optionally create prospects through the management API instead.

**What you'll build:** A governed portal membership list with the right people assigned to the right user groups.

## Prerequisites

Before starting, ensure:

1. **Authentication ready**
   - Valid Bearer token for Anypoint Platform
   - **AEH Administrator** or **AEH Portal Administrator** permissions

2. **Environment already bootstrapped**
   - Connection and portal exist (use the AEH UI if not)
   - At least one user group exists in the portal (see `manage-portal-user-groups`)

## Step 1: List AEH Connections

Retrieve the AEH connections the user has access to.

**What you'll need:**
- Bearer token

**Action:** List connections and pick the one hosting the target portal.

```yaml
api: urn:api:api-experience-hub-management
operationId: getConnections
inputs: {}
outputs:
  - name: connectionId
    path: $[*].id
    labels: $[*].name
    description: AEH connection ID (Salesforce org link) backing the portal
```

**What happens next:** The chosen `connectionId` scopes every subsequent call.

## Step 2: List Portals on the Connection

Pick the target portal whose membership you want to manage.

**What you'll need:**
- `connectionId` from Step 1

```yaml
api: urn:api:api-experience-hub-management
operationId: getAllApiPortalByConnectionId
inputs:
  connectionId:
    from:
      variable: connectionId
    description: Connection ID from Step 1
outputs:
  - name: portalId
    path: $[*].id
    labels: $[*].name
    description: ID of the portal to manage
```

## Step 3: Create a Prospect Instead of Using Self-Registration (Optional)

Normally, users register through the portal's built-in self-registration. Skip this step and continue to Step 4 to review those registrations. When you do not want to use that self-registration flow, create a pending registration on behalf of a new user with `POST /api/v1/connections/{connectionId}/apiPortals/{portalId}/prospects`. API creation is an alternative registration path, not a prerequisite for approving or rejecting prospects. Also skip this step when managing existing members.

**What you'll need:**

- `connectionId`, `portalId` from Steps 1–2; use the portal's AEH `id`, not its Salesforce `targetPortalId`
- `email`, `firstName`, `lastName`, and `username`, each up to 96 characters
- An email-formatted username that does not already exist in the Salesforce organization

```yaml
api: urn:api:api-experience-hub-management
operationId: createProspect
inputs:
  connectionId:
    from:
      variable: connectionId
    description: Connection ID from Step 1
  portalId:
    from:
      variable: portalId
    description: AEH portal ID from Step 2
  prospectRequest:
    userProvided: true
    description: JSON request body containing the new user's required registration details
    example:
      email: bob@example.com
      firstName: Bob
      lastName: Builder
      username: bob@example.com
outputs:
  - name: createdProspectId
    path: $.id
    description: ID of the created prospect, usable as prospectId for approval or rejection
  - name: createdProspectStatus
    path: $.status
    description: PENDING status of the newly created registration
```

**What happens next:** Expect `201 Created` with the prospect's `id` and `status: PENDING`. Creation does not approve the user. Continue to Step 4 to review pending prospects, or use `createdProspectId` as `prospectId` in Step 5 or Step 6 when the admin requests approval or rejection.

## Step 4: List Pending Prospects

Retrieve the list of users who have requested access to the portal but are not yet members.

**What you'll need:**
- `connectionId`, `portalId`

```yaml
api: urn:api:api-experience-hub-management
operationId: getProspects
inputs:
  connectionId:
    from:
      variable: connectionId
    description: Connection ID
  portalId:
    from:
      variable: portalId
    description: Portal ID
outputs:
  - name: prospects
    path: $[*]
    labels: $[*].email
    description: Pending prospects awaiting admin decision
  - name: prospectId
    path: $[*].id
    description: Prospect ID used by the approve/reject operations
```

**What happens next:** Present the prospect list and let the admin choose who to approve or reject.

## Step 5: Approve a Prospect

Promote a prospect to an active portal member and assign them to one or more user groups. Repeat per prospect the admin wants to approve.

**What you'll need:**
- `connectionId`, `portalId`, `prospectId`
- User-group IDs to assign (discover via `manage-portal-user-groups` Step "List User Groups")

```yaml
api: urn:api:api-experience-hub-management
operationId: approveProspect
inputs:
  connectionId:
    from:
      variable: connectionId
    description: Connection ID
  portalId:
    from:
      variable: portalId
    description: Portal ID
  prospectId:
    from:
      variable: prospectId
    description: The prospect being approved
  approvalRequest:
    userProvided: true
    description: User groups to assign to the new member on approval
    example:
      userGroups:
        - id: 00G1a000000abcD
outputs:
  - name: approvedUserId
    path: $.userId
    description: The user ID of the newly approved member
```

**What happens next:** The prospect is now a portal member with the chosen group assignments.

## Step 6: Reject a Prospect (Optional)

Reject prospects who should not be granted access.

**What you'll need:**
- `connectionId`, `portalId`, `prospectId`

```yaml
api: urn:api:api-experience-hub-management
operationId: rejectProspect
inputs:
  connectionId:
    from:
      variable: connectionId
    description: Connection ID
  portalId:
    from:
      variable: portalId
    description: Portal ID
  prospectId:
    from:
      variable: prospectId
    description: The prospect being rejected
outputs:
  - name: rejectedProspectId
    path: $.id
    description: The rejected prospect's ID (for audit)
```

**What happens next:** The prospect is removed from the queue. They can re-request access later.

## Step 7: List Portal Members

Retrieve active portal members to audit who currently has access.

**What you'll need:**
- `connectionId`, `portalId`

```yaml
api: urn:api:api-experience-hub-management
operationId: getCommunityUsers
inputs:
  connectionId:
    from:
      variable: connectionId
    description: Connection ID
  portalId:
    from:
      variable: portalId
    description: Portal ID
outputs:
  - name: members
    path: $.users[*]
    labels: $.users[*].email
    description: Active portal members
  - name: userId
    path: $.users[*].id
    description: Portal-member user ID used by per-member operations
```

## Step 8: Inspect a Member's User-Group Assignments

Fetch the specific group assignments of one member.

**What you'll need:**
- `connectionId`, `portalId`, `userId`

```yaml
api: urn:api:api-experience-hub-management
operationId: getCommunityUser
inputs:
  connectionId:
    from:
      variable: connectionId
    description: Connection ID
  portalId:
    from:
      variable: portalId
    description: Portal ID
  userId:
    from:
      variable: userId
    description: Portal-member user ID
outputs:
  - name: memberUserGroups
    path: $.userGroups[*]
    labels: $.userGroups[*].name
    description: Current user groups assigned to the member
```

**What happens next:** Present the current assignments; let the admin decide new memberships for Step 9.

## Step 9: Update a Member's User-Group Assignments

Replace or extend the user groups assigned to a specific member.

**What you'll need:**
- `connectionId`, `portalId`, `userId`
- Target user-group IDs

```yaml
api: urn:api:api-experience-hub-management
operationId: addGroupMappingToUser
inputs:
  connectionId:
    from:
      variable: connectionId
    description: Connection ID
  portalId:
    from:
      variable: portalId
    description: Portal ID
  targetUserId:
    from:
      variable: userId
    description: Portal-member user ID
  userGroupsRequest:
    userProvided: true
    description: Full replacement set of user groups for this member
    example:
      userGroups:
        - id: 00G1a000000abcD
        - id: 00G1a000000efgH
outputs:
  - name: updatedUserId
    path: $.userId
    description: Confirmed member ID with new assignments applied
```

**What happens next:** The member now has exactly the user groups you specified.

## Step 10: Disable a Portal Member (Optional)

Revoke a member's access without deleting their record — useful for offboarding.

**What you'll need:**
- `connectionId`, `portalId`, `targetUserId`

```yaml
api: urn:api:api-experience-hub-management
operationId: disableCommunityUser
inputs:
  connectionId:
    from:
      variable: connectionId
    description: Connection ID
  portalId:
    from:
      variable: portalId
    description: Portal ID
  targetUserId:
    from:
      variable: userId
    description: The member to disable
outputs:
  - name: disabledUserId
    path: $.userId
    description: Confirmed disabled member ID
```

**What happens next:** The disabled member can no longer sign in to the portal. Their API contracts remain intact for audit.

## Completion Checklist

- [ ] Connection and portal selected
- [ ] If using an alternative to built-in self-registration, prospect created through the API with status PENDING; otherwise, creation step skipped
- [ ] Pending prospects reviewed
- [ ] Approved prospects assigned to correct user groups
- [ ] Unwanted prospects rejected
- [ ] Existing members' group assignments audited
- [ ] Offboarded members disabled (if applicable)

## What You've Built

✅ **Governed Portal Membership** — New prospects are registered when requested, prospects are triaged, and approved members have the right user-group entitlements.

## Troubleshooting

- **Create returns `400`:** Check that all four required fields are present and at most 96 characters, and that email and username have email format. If the username already exists in Salesforce, do not retry creation with the same username.
- **Create returns `409`:** The portal's prospect limit has been reached. Review existing registrations before retrying.
- **Portal listing returns `500`:** Record the response's `requestId` and investigate the connection. Continue only with a known valid connection and AEH portal ID.

## Next Steps

1. **Manage user groups themselves** — See `manage-portal-user-groups` to define the groups referenced here.
2. **Curate the visible catalog** — See `curate-portal-assets` to control which APIs members see.
3. **Monitor contracts** — Track which approved members create consumer contracts against published APIs.

## Related Jobs

- **skill curate-portal-assets** — Control which APIs and minor versions portal members see
- **skill manage-portal-user-groups** — Define and maintain the user groups assigned here
