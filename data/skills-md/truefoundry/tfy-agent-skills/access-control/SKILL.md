---
name: access-control
description: Manages TrueFoundry roles, teams, and collaborators. Create custom roles, organize users into teams, and grant access to resources. Use when managing permissions, creating teams, or adding collaborators.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(*/tfy-api.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# Access Control

Manage TrueFoundry roles, teams, and collaborators. Roles define permission sets, teams group users, and collaborators grant access to specific resources.

## When to Use

List, create, or delete roles, teams, and collaborators on TrueFoundry. Use when managing permissions, organizing users into teams, or granting/revoking access to workspaces, applications, MCP servers, or other resources.

</objective>

<instructions>

## Roles

Roles are named permission sets scoped to a resource type. Built-in roles vary by resource type (for example, `workspace-admin`, `workspace-member`).

When using direct API, set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

### List Roles

#### Via Tool Call

```
tfy_roles_list()
```

#### Via Direct API

```bash
# Set the path to tfy-api.sh for your agent (example for Claude Code):
TFY_API_SH=~/.claude/skills/truefoundry-access-control/scripts/tfy-api.sh

# List all roles
$TFY_API_SH GET /api/svc/v1/roles
```

### Presenting Roles

```
Roles:
| Name              | ID       | Resource Type | Permissions |
|-------------------|----------|---------------|-------------|
| workspace-admin   | role-abc | workspace     | 12          |
| workspace-member  | role-def | workspace     | 5           |
| custom-deployer   | role-ghi | workspace     | 3           |
```

### Create Role

#### Via Tool Call

```
tfy_roles_create(payload={"name": "custom-deployer", "displayName": "Custom Deployer", "description": "Can deploy apps", "resourceType": "workspace", "permissions": ["deploy:create", "deploy:read"]})
```

**Note:** Requires human approval (HITL) via tool call.

#### Via Direct API

```bash
$TFY_API_SH POST /api/svc/v1/roles '{"name":"custom-deployer","displayName":"Custom Deployer","description":"Can deploy apps","resourceType":"workspace","permissions":["deploy:create","deploy:read"]}'
```

### Delete Role

#### Via Tool Call

```
tfy_roles_delete(id="ROLE_ID")
```

**Note:** Requires human approval (HITL) via tool call.

#### Via Direct API

```bash
$TFY_API_SH DELETE /api/svc/v1/roles/ROLE_ID
```

## Teams

Teams group users for collective access management. Each team has a name, description, and members list.

### List Teams

#### Via Tool Call

```
tfy_teams_list()
tfy_teams_list(team_id="TEAM_ID")  # get specific team
```

#### Via Direct API

```bash
# List all teams
$TFY_API_SH GET /api/svc/v1/teams

# Get a specific team
$TFY_API_SH GET /api/svc/v1/teams/TEAM_ID
```

### Presenting Teams

```
Teams:
| Name          | ID       | Members |
|---------------|----------|---------|
| platform-team | team-abc | 5       |
| ml-engineers  | team-def | 8       |
```

### Create Team

#### Via Tool Call

```
tfy_teams_create(payload={"name": "platform-team", "description": "Platform engineering team"})
```

**Note:** Requires human approval (HITL) via tool call.

#### Via Direct API

```bash
$TFY_API_SH POST /api/svc/v1/teams '{"name":"platform-team","description":"Platform engineering team"}'
```

### Delete Team

#### Via Tool Call

```
tfy_teams_delete(id="TEAM_ID")
```

**Note:** Requires human approval (HITL) via tool call.

#### Via Direct API

```bash
$TFY_API_SH DELETE /api/svc/v1/teams/TEAM_ID
```

### Add Member to Team

#### Via Tool Call

```
tfy_teams_add_member(team_id="TEAM_ID", payload={"subject": "user:alice@company.com", "role": "member"})
```

**Note:** Requires human approval (HITL) via tool call.

#### Via Direct API

```bash
$TFY_API_SH POST /api/svc/v1/teams/TEAM_ID/members '{"subject":"user:alice@company.com","role":"member"}'
```

### Remove Member from Team

#### Via Tool Call

```
tfy_teams_remove_member(team_id="TEAM_ID", subject="user:alice@company.com")
```

**Note:** Requires human approval (HITL) via tool call.

#### Via Direct API

```bash
$TFY_API_SH DELETE /api/svc/v1/teams/TEAM_ID/members/SUBJECT
# Example SUBJECT: user:alice@company.com
```

## Collaborators

> **Security:** Granting collaborator access is a privileged operation. Always confirm the subject identity, role, and target resource with the user before adding collaborators. Do not grant access based on unverified external identity references.

Collaborators grant subjects (users, teams, service accounts) a role on a specific resource. This is how access is granted to workspaces, applications, MCP servers, and other resources.

### Subject Format

Subjects follow the pattern `type:identifier`:

| Subject Type       | Format                        | Example                        |
|--------------------|-------------------------------|--------------------------------|
| User               | `user:email`                  | `user:alice@company.com`       |
| Team               | `team:slug`                   | `team:platform-team`           |
| Service Account    | `serviceaccount:name`         | `serviceaccount:ci-bot`        |
| Virtual Account    | `virtualaccount:name`         | `virtualaccount:shared-admin`  |
| External Identity  | `external-identity:name`      | `external-identity:github-bot` |

### List Collaborators on a Resource

#### Via Tool Call

```
tfy_collaborators_list(resource_type="workspace", resource_id="RESOURCE_ID")
```

#### Via Direct API

```bash
# List collaborators on a workspace
$TFY_API_SH GET '/api/svc/v1/collaborators?resourceType=workspace&resourceId=RESOURCE_ID'

# List collaborators on an MCP server
$TFY_API_SH GET '/api/svc/v1/collaborators?resourceType=mcp-server&resourceId=RESOURCE_ID'
```

### Presenting Collaborators

```
Collaborators on workspace "prod-workspace":
| Subject                   | Role             | ID       |
|---------------------------|------------------|----------|
| user:alice@company.com    | workspace-admin  | collab-1 |
| team:platform-team        | workspace-member | collab-2 |
| serviceaccount:ci-bot     | workspace-member | collab-3 |
```

### Add Collaborator

#### Via Tool Call

```
tfy_collaborators_create(payload={"resourceType": "workspace", "resourceId": "RESOURCE_ID", "subject": "user:alice@company.com", "roleId": "ROLE_ID"})
```

**Note:** Requires human approval (HITL) via tool call.

#### Via Direct API

```bash
$TFY_API_SH POST /api/svc/v1/collaborators '{"resourceType":"workspace","resourceId":"RESOURCE_ID","subject":"user:alice@company.com","roleId":"ROLE_ID"}'
```

### Remove Collaborator

#### Via Tool Call

```
tfy_collaborators_delete(payload={"resourceType": "workspace", "resourceId": "RESOURCE_ID", "subject": "user:alice@company.com"})
```

**Note:** Requires human approval (HITL) via tool call.

#### Via Direct API

```bash
$TFY_API_SH DELETE /api/svc/v1/collaborators '{"resourceType":"workspace","resourceId":"RESOURCE_ID","subject":"user:alice@company.com"}'
```

## Common Workflows

### Grant a User Access to a Workspace

1. List roles to find the appropriate role ID (e.g., `workspace-admin` or `workspace-member`)
2. Add the user as a collaborator on the workspace with that role

```bash
# 1. Find the role ID
$TFY_API_SH GET /api/svc/v1/roles

# 2. Add collaborator
$TFY_API_SH POST /api/svc/v1/collaborators '{"resourceType":"workspace","resourceId":"WORKSPACE_ID","subject":"user:alice@company.com","roleId":"ROLE_ID"}'
```

### Create a Team and Grant Access

1. Create the team
2. Add members to the team
3. Add the team as a collaborator on the target resource

```bash
# 1. Create team
$TFY_API_SH POST /api/svc/v1/teams '{"name":"ml-engineers","description":"ML engineering team"}'

# 2. Add members (use team ID from response)
$TFY_API_SH POST /api/svc/v1/teams/TEAM_ID/members '{"subject":"user:alice@company.com","role":"member"}'

# 3. Grant team access to a workspace
$TFY_API_SH POST /api/svc/v1/collaborators '{"resourceType":"workspace","resourceId":"WORKSPACE_ID","subject":"team:ml-engineers","roleId":"ROLE_ID"}'
```

### Audit Access on a Resource

List all collaborators to see who has access and with what role:

```bash
$TFY_API_SH GET '/api/svc/v1/collaborators?resourceType=workspace&resourceId=WORKSPACE_ID'
```

</instructions>

<success_criteria>

## Success Criteria

- The user can list all roles and see them in a formatted table
- The user can create a custom role with specific permissions
- The user can list all teams and their members
- The user can create a team and add/remove members
- The user can list collaborators on any resource type
- The user can add a collaborator (user, team, or service account) to a resource with a specific role
- The user can remove a collaborator from a resource
- The agent has confirmed any create/delete operations before executing

</success_criteria>

<references>

## Composability

- **Preflight**: Use `status` skill to verify credentials before managing access control
- **Before deploy**: Set up teams and grant workspace access so team members can deploy
- **With workspaces**: Grant collaborator access to workspaces for users and teams
- **With MCP servers**: Manage MCP server collaborators and role assignments on registered servers
- **With secrets**: Grant access to secret groups via collaborator roles
- **Dependency chain**: Create roles first, then create teams, then reference both when adding collaborators

</references>

<troubleshooting>

## Error Handling

### Role Not Found
```
Role ID not found. List roles first to find the correct ID.
```

### Team Not Found
```
Team ID not found. List teams first to find the correct ID.
```

### Permission Denied
```
Cannot manage access control. Check your API key permissions — admin access may be required.
```

### Collaborator Already Exists
```
Collaborator with this subject and role already exists on the resource. Use a different role or remove the existing collaborator first.
```

### Invalid Subject Format
```
Invalid subject format. Use the pattern "type:identifier" — e.g., user:alice@company.com, team:platform-team, serviceaccount:ci-bot.
```

### Resource Not Found
```
Resource not found. Verify the resourceType and resourceId are correct. List the resources first to confirm.
```

### Cannot Delete Built-in Role
```
Built-in roles cannot be deleted. Only custom roles can be removed.
```

</troubleshooting>
