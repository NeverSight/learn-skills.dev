---
name: omni-admin
description: Administer an Omni Analytics instance — manage connections, users, groups, user attributes, permissions, schedules, and schema refreshes via the REST API. Use this skill whenever someone wants to manage users or groups, set up permissions on a dashboard or folder, configure user attributes, create or modify schedules, manage database connections, refresh a schema, set up access controls, provision users, or any variant of "add a user", "give access to", "set up permissions", "who has access", "configure connection", "refresh the schema", or "schedule a delivery".
---

# Omni Admin

Manage your Omni instance — connections, users, groups, user attributes, permissions, schedules, and schema refreshes.

> **Tip**: Most admin endpoints require an **Organization API Key** (not a Personal Access Token).

## Prerequisites

```bash
export OMNI_BASE_URL="https://yourorg.omniapp.co"
export OMNI_API_KEY="your-api-key"
```

## API Discovery

When unsure whether an endpoint or parameter exists, fetch the OpenAPI spec:

```bash
curl -L "$OMNI_BASE_URL/openapi.json" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

Use this to verify endpoints, available parameters, and request/response schemas before making calls.

## Connections

```bash
# List connections
curl -L "$OMNI_BASE_URL/api/v1/connections" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Schema refresh schedules
curl -L "$OMNI_BASE_URL/api/v1/connections/{connectionId}/schedules" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Connection environments
curl -L "$OMNI_BASE_URL/api/v1/connection-environments" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

## User Management (SCIM 2.0)

Endpoint prefix: `/api/scim/v2/`

```bash
# List users
curl -L "$OMNI_BASE_URL/api/scim/v2/users" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Find by email (URL-encode the filter)
curl -L "$OMNI_BASE_URL/api/scim/v2/users?filter=userName%20eq%20%22user@company.com%22" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Create user
curl -L -X POST "$OMNI_BASE_URL/api/scim/v2/users" \
  -H "Authorization: Bearer $OMNI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
    "userName": "newuser@company.com",
    "displayName": "New User",
    "active": true,
    "emails": [{ "primary": true, "value": "newuser@company.com" }]
  }'

# Deactivate user
curl -L -X PATCH "$OMNI_BASE_URL/api/scim/v2/users/{userId}" \
  -H "Authorization: Bearer $OMNI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
    "Operations": [{ "op": "replace", "path": "active", "value": false }]
  }'

# Delete user
curl -L -X DELETE "$OMNI_BASE_URL/api/scim/v2/users/{userId}" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

## Group Management (SCIM 2.0)

```bash
# List groups
curl -L "$OMNI_BASE_URL/api/scim/v2/groups" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Create group
curl -L -X POST "$OMNI_BASE_URL/api/scim/v2/groups" \
  -H "Authorization: Bearer $OMNI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
    "displayName": "Analytics Team",
    "members": [{ "value": "user-uuid-1" }]
  }'

# Add members
curl -L -X PATCH "$OMNI_BASE_URL/api/scim/v2/groups/{groupId}" \
  -H "Authorization: Bearer $OMNI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
    "Operations": [{ "op": "add", "path": "members", "value": [{ "value": "new-user-uuid" }] }]
  }'
```

## User Attributes

```bash
# List attributes
curl -L "$OMNI_BASE_URL/api/v1/user-attributes" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Set attribute on user (via SCIM)
curl -L -X PATCH "$OMNI_BASE_URL/api/scim/v2/users/{userId}" \
  -H "Authorization: Bearer $OMNI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
    "Operations": [{
      "op": "replace",
      "path": "urn:omni:params:1.0:UserAttribute:region",
      "value": "West Coast"
    }]
  }'
```

User attributes work with `access_filters` in topics for row-level security.

## Model Roles

```bash
# User roles on a model
curl -L "$OMNI_BASE_URL/api/v1/models/{modelId}/user-roles" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Group roles on a model
curl -L "$OMNI_BASE_URL/api/v1/models/{modelId}/group-roles" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

## Document Permissions

```bash
# Get permissions
curl -L "$OMNI_BASE_URL/api/v1/documents/{documentId}/permissions" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Set permissions
curl -L -X PUT "$OMNI_BASE_URL/api/v1/documents/{documentId}/permissions" \
  -H "Authorization: Bearer $OMNI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "permissions": [
      { "type": "group", "id": "group-uuid", "access": "view" },
      { "type": "user", "id": "user-uuid", "access": "edit" }
    ]
  }'
```

## Folder Permissions

```bash
# Get
curl -L "$OMNI_BASE_URL/api/v1/folders/{folderId}/permissions" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Set
curl -L -X PUT "$OMNI_BASE_URL/api/v1/folders/{folderId}/permissions" \
  -H "Authorization: Bearer $OMNI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "permissions": [{ "type": "group", "id": "group-uuid", "access": "view" }]
  }'
```

## Schedules

```bash
# List schedules
curl -L "$OMNI_BASE_URL/api/v1/schedules" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Create schedule
curl -L -X POST "$OMNI_BASE_URL/api/v1/schedules" \
  -H "Authorization: Bearer $OMNI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "documentId": "dashboard-identifier",
    "frequency": "weekly",
    "dayOfWeek": "monday",
    "hour": 9,
    "timezone": "America/Los_Angeles",
    "format": "pdf"
  }'

# Manage recipients
curl -L "$OMNI_BASE_URL/api/v1/schedules/{scheduleId}/recipients" \
  -H "Authorization: Bearer $OMNI_API_KEY"

curl -L -X POST "$OMNI_BASE_URL/api/v1/schedules/{scheduleId}/recipients" \
  -H "Authorization: Bearer $OMNI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "recipients": [{ "type": "email", "value": "team@company.com" }] }'
```

## Cache and Validation

```bash
# Reset cache policy
curl -L -X POST "$OMNI_BASE_URL/api/v1/models/{modelId}/cache_reset/{policyName}" \
  -H "Authorization: Bearer $OMNI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "resetAt": "2025-01-30T22:30:52.872Z" }'

# Content validator (find broken field references across all dashboards and tiles)
# Useful for blast-radius analysis: remove a field on a branch, then run the
# validator against that branch to see what content would break.
# See the Field Impact Analysis section in omni-model-explorer for the full workflow.
curl -L "$OMNI_BASE_URL/api/v1/models/{modelId}/content-validator" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Run against a specific branch (e.g., after removing a field)
curl -L "$OMNI_BASE_URL/api/v1/models/{modelId}/content-validator?branchId={branchId}" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Git configuration
curl -L "$OMNI_BASE_URL/api/v1/models/{modelId}/git" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

## Docs Reference

- [Connections](https://docs.omni.co/api/connections.md) · [Users (SCIM)](https://docs.omni.co/api/users.md) · [Groups (SCIM)](https://docs.omni.co/api/user-groups.md) · [User Attributes](https://docs.omni.co/api/user-attributes.md) · [Document Permissions](https://docs.omni.co/api/document-permissions.md) · [Folder Permissions](https://docs.omni.co/api/folder-permissions.md) · [Schedules](https://docs.omni.co/api/schedules.md) · [Schedule Recipients](https://docs.omni.co/api/schedule-recipients.md) · [Content Validator](https://docs.omni.co/api/content-validator.md) · [API Authentication](https://docs.omni.co/api/authentication.md)

## Related Skills

- **omni-model-builder** — edit the model that access controls apply to
- **omni-content-explorer** — find documents before setting permissions
- **omni-content-builder** — create dashboards before scheduling delivery
- **omni-embed** — manage embed users and user attributes for embedded dashboards
