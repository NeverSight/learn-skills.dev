---
name: manage-portal-applications
description: |
  Manage the applications that hold API credentials inside an API Experience
  Hub portal. Use when a portal consumer needs to list their applications,
  check if a name is available, create a new application, update metadata,
  rotate the client secret, or delete an application they no longer use.
---

# Manage Portal Applications

## Overview

Applications are the credential-bearing objects portal consumers use to call APIs. Each application has a `clientId` / `clientSecret` pair and can hold multiple contracts against published APIs. This workflow covers the application lifecycle from a portal-consumer perspective: inventory, name-availability check, create, update, secret rotation, and deletion.

**What you'll build:** A clean application portfolio with the credentials you need to consume portal APIs.

## Prerequisites

Before starting, ensure:

1. **Authentication ready**
   - Valid portal-consumer Bearer token
   - Membership in the portal

2. **Portal context known**
   - `targetOrganizationId` — Anypoint organization hosting the portal
   - `portalId` — the portal you are a member of

## Step 1: List Your Applications

Start by viewing the applications already registered under your portal membership.

**What you'll need:**
- `targetOrganizationId`, `portalId`

```yaml
api: urn:api:api-experience-hub-consumer
operationId: getApplications
inputs:
  targetOrganizationId:
    userProvided: true
    description: Anypoint organization ID hosting the portal
  portalId:
    userProvided: true
    description: Portal ID the user belongs to
outputs:
  - name: applications
    path: $.applications[*]
    labels: $.applications[*].name
    description: Your existing applications in this portal
  - name: applicationId
    path: $.applications[*].id
    description: ID used by the per-application operations
```

## Step 2: Check Application-Name Availability

Before creating a new application, confirm the desired name is not already taken in the portal.

**What you'll need:**
- `targetOrganizationId`, `portalId`
- Proposed application name

```yaml
api: urn:api:api-experience-hub-consumer
operationId: checkExistenceApplicationName
inputs:
  targetOrganizationId:
    from:
      variable: targetOrganizationId
    description: Anypoint organization ID hosting the portal
  portalId:
    from:
      variable: portalId
    description: Portal ID
  nameCheckRequest:
    userProvided: true
    description: The candidate application name to check for uniqueness
    example:
      name: orders-prod-client
outputs:
  - name: nameAvailable
    path: $.available
    description: Whether the proposed name is free to use
```

**What happens next:** If taken, pick a different name and re-check; if free, proceed to Step 3.

## Step 3: Create a New Application

Register a new application to obtain `clientId` / `clientSecret` credentials.

**What you'll need:**
- `targetOrganizationId`, `portalId`
- Application details (name, description, redirect URIs if OIDC/OAuth2)

```yaml
api: urn:api:api-experience-hub-consumer
operationId: createApplication
inputs:
  targetOrganizationId:
    from:
      variable: targetOrganizationId
    description: Anypoint organization ID hosting the portal
  portalId:
    from:
      variable: portalId
    description: Portal ID
  groupId:
    userProvided: true
    description: groupId of the asset to bind the application to (if required by portal policy)
  assetId:
    userProvided: true
    description: assetId of the asset to bind the application to
  minorVersion:
    userProvided: true
    description: minor version of the asset
  applicationRequest:
    userProvided: true
    description: Application metadata and OAuth/OIDC settings
    example:
      name: orders-prod-client
      description: Production client for the Orders API
      redirectUris:
        - https://app.example.com/callback
outputs:
  - name: createdApplicationId
    path: $.id
    description: The new application ID
  - name: clientId
    path: $.clientId
    description: OAuth client ID issued to the application
  - name: clientSecret
    path: $.clientSecret
    description: OAuth client secret (shown only at creation — store it securely)
```

**What happens next:** Capture the `clientSecret` now — it is not retrievable later; you must rotate via Step 5 if lost.

## Step 4: Update Application Metadata

Change an application's name, description, or OAuth redirect URIs after creation.

**What you'll need:**
- `targetOrganizationId`, `portalId`, `applicationId`

```yaml
api: urn:api:api-experience-hub-consumer
operationId: updateApplication
inputs:
  targetOrganizationId:
    from:
      variable: targetOrganizationId
    description: Anypoint organization ID hosting the portal
  portalId:
    from:
      variable: portalId
    description: Portal ID
  applicationId:
    from:
      variable: applicationId
    description: ID of the application to update
  applicationUpdate:
    userProvided: true
    description: Updated application metadata
    example:
      name: orders-prod-client
      description: Production client for the Orders API (v2)
      redirectUris:
        - https://app.example.com/v2/callback
outputs:
  - name: updatedApplicationId
    path: $.id
    description: Confirmed ID of the updated application
```

## Step 5: Reset Client Secret

Rotate the `clientSecret` — e.g., after a suspected leak or as part of key-rotation policy.

**What you'll need:**
- `targetOrganizationId`, `portalId`, `applicationId`

```yaml
api: urn:api:api-experience-hub-consumer
operationId: resetClientSecretForApplication
inputs:
  targetOrganizationId:
    from:
      variable: targetOrganizationId
    description: Anypoint organization ID hosting the portal
  portalId:
    from:
      variable: portalId
    description: Portal ID
  applicationId:
    from:
      variable: applicationId
    description: ID of the application to rotate
outputs:
  - name: newClientSecret
    path: $.clientSecret
    description: Newly generated client secret (store it securely — only shown once)
```

**What happens next:** Update every consumer of this application to use the new secret. The previous secret is invalidated.

## Step 6: View Application Details

Inspect a single application's current state — metadata plus any derived info.

**What you'll need:**
- `targetOrganizationId`, `portalId`, `applicationId`

```yaml
api: urn:api:api-experience-hub-consumer
operationId: getApplicationDetailById
inputs:
  targetOrganizationId:
    from:
      variable: targetOrganizationId
    description: Anypoint organization ID hosting the portal
  portalId:
    from:
      variable: portalId
    description: Portal ID
  applicationId:
    from:
      variable: applicationId
    description: ID of the application to inspect
outputs:
  - name: applicationDetails
    path: $
    description: Current application metadata (clientId present; secret never returned)
```

## Step 7: Delete an Application (Optional)

Remove an application that is no longer in use. All contracts bound to it are revoked.

**What you'll need:**
- `targetOrganizationId`, `portalId`, `applicationId`

```yaml
api: urn:api:api-experience-hub-consumer
operationId: deleteApplication
inputs:
  targetOrganizationId:
    from:
      variable: targetOrganizationId
    description: Anypoint organization ID hosting the portal
  portalId:
    from:
      variable: portalId
    description: Portal ID
  applicationId:
    from:
      variable: applicationId
    description: ID of the application to delete
outputs:
  - name: deletedApplicationId
    path: $.id
    description: Confirmation of the deleted application
```

## Completion Checklist

- [ ] Existing applications reviewed
- [ ] Unique application name confirmed
- [ ] New application created and secret captured
- [ ] Metadata kept up to date (name, description, redirect URIs)
- [ ] Secrets rotated on schedule or after incidents
- [ ] Stale applications deleted

## What You've Built

✅ **Healthy Application Portfolio** — Active applications with fresh credentials, no stale clients lingering.

## Next Steps

1. **Request API access** — See `request-api-access` to create a contract from an application against a published API.
2. **Monitor contracts** — See the contract-listing steps in `request-api-access` to audit which APIs each application consumes.

## Related Jobs

- **request-api-access** — Bind an application to an API via a contract
- **discover-portal-apis** — Find APIs your application should request access to
