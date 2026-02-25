---
name: eve-auth-and-secrets
description: Authenticate with Eve and manage project secrets for deployments and workflows.
---

# Eve Auth and Secrets

Use this workflow to log in to Eve and manage secrets for your app.

## When to Use

- Setting up a new project profile
- Authentication failures
- Adding or rotating secrets
- Secret interpolation errors during deploys
- Setting up identity providers or org invites
- Setting up access groups and scoped data-plane authorization
- Configuring group-aware RLS for environment databases

## Authentication

```bash
eve auth login
eve auth login --ttl 30                # custom token TTL (1-90 days)
eve auth status
```

### Challenge-Response Flow

Eve uses challenge-response authentication. The default provider is `github_ssh`:

1. Client sends SSH public key fingerprint
2. Server returns a challenge (random bytes)
3. Client signs the challenge with the private key
4. Server verifies the signature and issues a JWT

### Token Types

| Type | Issued Via | Use Case |
|------|-----------|----------|
| User Token | `eve auth login` | Interactive CLI sessions |
| Job Token | Worker auto-issued | Agent execution within jobs |
| Minted Token | `eve auth mint` | Bot/service accounts |

JWT payloads include `sub` (user ID), `org_id`, `scope`, and `exp`. Verify tokens via the JWKS endpoint: `GET /auth/jwks`.

Role and org membership changes take effect immediately -- the server resolves permissions from live DB memberships, not stale JWT claims. When a request includes a `project_id` but no `org_id`, the permission guard derives the org context from the project's owning org.

### Permissions

Check what the current token can do:

```bash
eve auth permissions
```

Register additional identities for multi-provider access:

```bash
curl -X POST "$EVE_API_URL/auth/identities" -H "Authorization: Bearer $TOKEN" \
  -d '{"provider": "nostr", "external_id": "<pubkey>"}'
```

## Identity Providers

Eve supports pluggable identity providers. The auth guard tries Bearer JWT first, then provider-specific request auth.

| Provider | Auth Method | Use Case |
|----------|------------|----------|
| `github_ssh` | SSH challenge-response | Default CLI login |
| `nostr` | NIP-98 request auth + challenge-response | Nostr-native users |

### Nostr Authentication

Two paths:
- **Challenge-response**: Like SSH but signs with Nostr key. Use `eve auth login --provider nostr`.
- **NIP-98 request auth**: Every API request signed with a Kind 27235 event. Stateless, no stored token.

## Org Invites

Invite external users via the CLI or API:

```bash
# Invite with SSH key registration (registers key so the user can log in immediately)
eve admin invite --email user@example.com --ssh-key ~/.ssh/id_ed25519.pub --org org_xxx

# Invite with GitHub identity
eve admin invite --email user@example.com --github ghuser --org org_xxx

# Invite with web-based auth (Supabase)
eve admin invite --email user@example.com --web --org org_xxx

# API: invite targeting a Nostr pubkey
curl -X POST "$EVE_API_URL/auth/invites" -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"org_id": "org_xxx", "role": "member", "provider_hint": "nostr", "identity_hint": "<pubkey>"}'
```

If no auth method is specified (`--github`, `--ssh-key`, or `--web`), the CLI warns that the user will not be able to log in. The user can self-register later via `eve auth request-access --org "Org Name" --ssh-key ~/.ssh/id_ed25519.pub --wait`.

When the identity authenticates, Eve auto-provisions their account and org membership.

## Token Minting (Admin)

Mint tokens for bot/service users without SSH login:

```bash
# Mint token for a bot user (creates user + membership if needed)
eve auth mint --email app-bot@example.com --org org_xxx

# With custom TTL (1-90 days, default: server configured)
eve auth mint --email app-bot@example.com --org org_xxx --ttl 90

# Scope to project with admin role
eve auth mint --email app-bot@example.com --project proj_xxx --role admin
```

Print the current access token (useful for scripts):

```bash
eve auth token
```

## Self-Service Access Requests

Users without an invite can request access:

```bash
eve auth request-access --org "My Company" --email you@example.com
eve auth request-access --org "My Company" --ssh-key ~/.ssh/id_ed25519.pub
eve auth request-access --status <request_id>
```

Admins approve or reject via:

```bash
eve admin access-requests list
eve admin access-requests approve <request_id>
eve admin access-requests reject <request_id> --reason "..."
```

List responses use the canonical `{ "data": [...] }` envelope.

Approval is atomic (single DB transaction) and idempotent -- re-approving a completed request returns the existing record. If the fingerprint is already registered, Eve reuses that identity owner. If a legacy partial org matches the requested slug and name, Eve reuses it during approval. Failed attempts never leave partial state.

## Credential Check

Verify local AI tool credentials:

```bash
eve auth creds                # Show Claude + Codex cred status
eve auth creds --claude       # Only Claude
eve auth creds --codex        # Only Codex
```

Output includes token type (`setup-token` or `oauth`), preview, and expiry. Use this to confirm token health before syncing.

## OAuth Token Sync

Sync local Claude/Codex OAuth tokens into Eve secrets so agents can use them. Scope precedence: project > org > user.

```bash
eve auth sync                       # Sync to user-level (default)
eve auth sync --org org_xxx         # Sync to org-level (shared across org projects)
eve auth sync --project proj_xxx    # Sync to project-level (scoped to one project)
eve auth sync --dry-run             # Preview without syncing
```

This sets `CLAUDE_CODE_OAUTH_TOKEN` / `CLAUDE_OAUTH_REFRESH_TOKEN` (Claude) and `CODEX_AUTH_JSON_B64` (Codex/Code) at the requested scope.

### Claude Token Types

| Token Prefix | Type | Lifetime | Recommendation |
|---|---|---|---|
| `sk-ant-oat01-*` | `setup-token` (long-lived) | Long-lived | Preferred for jobs and automation |
| Other `sk-ant-*` | `oauth` (short-lived) | ~15 hours | Use for interactive dev; regenerate with `claude setup-token` |

`eve auth sync` warns when syncing a short-lived OAuth token. Run `eve auth creds` to inspect token type before syncing.

### Automatic Codex/Code Token Write-Back

After each harness invocation, the worker checks if the Codex/Code CLI refreshed `auth.json` during the session. If the token changed, it is automatically written back to the originating secret scope (user/org/project) so the next job starts with a fresh token. This is transparent and non-fatal -- a write-back failure logs a warning but does not affect the job result.

For Codex/Code credentials, the sync picks the freshest token across `~/.codex/auth.json` and `~/.code/auth.json` by comparing `tokens.expires_at`.

## Access Groups + Scoped Access

Groups are first-class authorization primitives that segment data-plane access (org filesystem, org docs, environment databases). Create groups, add members, and bind roles with scoped constraints:

```bash
# Create a group
eve access groups create --org org_xxx --slug eng-team --name "Engineering"

# Add members
eve access groups members add eng-team --org org_xxx --user user_abc
eve access groups members add eng-team --org org_xxx --service-principal sp_xxx

# Bind a role with scoped access
eve access bind --org org_xxx --group grp_xxx --role data-reader \
  --scope-json '{"orgfs":{"allow_prefixes":["/shared/"]},"envdb":{"schemas":["public"]}}'

# Check effective access
eve access memberships --org org_xxx --user user_abc
```

### Scope Types

| Resource | Scope Fields | Example |
|----------|-------------|---------|
| Org Filesystem | `orgfs.allow_prefixes`, `orgfs.read_only_prefixes` | `"/shared/"`, `"/reports/"` |
| Org Documents | `orgdocs.allow_prefixes`, `orgdocs.read_only_prefixes` | `"/pm/features/"` |
| Environment DB | `envdb.schemas`, `envdb.tables` | `"public"`, `"analytics_*"` |

### Group-Aware RLS

Scaffold RLS helper functions for group-based row-level security in environment databases:

```bash
eve db rls init --with-groups
```

This creates SQL helpers (`app.current_user_id()`, `app.current_group_ids()`, `app.has_group()`) that read session context set by Eve's runtime. Use them in RLS policies:

```sql
CREATE POLICY notes_group_read ON notes FOR SELECT
  USING (group_id = ANY(app.current_group_ids()));
```

### Membership Introspection

Inspect a principal's full effective access -- base org/project roles, group memberships, resolved bindings, and merged scopes:

```bash
eve access memberships --org org_xxx --user user_abc
eve access memberships --org org_xxx --service-principal sp_xxx
```

The response includes `effective_scopes` (merged across all bindings), `effective_permissions`, and each binding's `matched_via` (direct or group).

### Resource-Specific Access Checks

Check and explain access against a specific data-plane resource:

```bash
eve access can orgfs:read /shared/reports --org org_xxx
eve access explain orgfs:write /shared/reports --org org_xxx --user user_abc
```

The response includes `scope_required`, `scope_matched`, and per-grant `scope_reason` explaining why a binding did or did not match the requested resource path.

### Policy-as-Code (v2)

Declare groups, roles, and scoped bindings in `.eve/access.yaml`. Use `version: 2`:

```yaml
version: 2
access:
  groups:
    eng-team:
      name: Engineering Team
      description: Scoped access for engineering collaborators
      members:
        - type: user
          id: user_abc
  roles:
    app_editor:
      scope: org
      permissions:
        - orgdocs:read
        - orgdocs:write
        - orgfs:read
        - envdb:read
  bindings:
    - subject: { type: group, id: eng-team }
      roles: [app_editor]
      scope:
        orgdocs: { allow_prefixes: ["/groups/app/**"] }
        orgfs: { allow_prefixes: ["/groups/app/**"] }
        envdb: { schemas: ["app"] }
```

Validate, plan, and sync:

```bash
eve access validate --file .eve/access.yaml
eve access plan --file .eve/access.yaml --org org_xxx
eve access sync --file .eve/access.yaml --org org_xxx
```

Sync is declarative: it creates, updates, and prunes groups, members, roles, and bindings to match the YAML. Invalid scope configurations fail fast before any mutations are applied. Binding subjects can be `user`, `service_principal`, or `group`.

## Key Rotation

Rotate the JWT signing key:

1. Set `EVE_AUTH_JWT_SECRET_NEW` alongside the existing secret
2. Server starts signing with the new key but accepts both during the grace period
3. After grace period (`EVE_AUTH_KEY_ROTATION_GRACE_HOURS`), remove the old secret
4. Emergency rotation: set only the new key (immediately invalidates all existing tokens)

## Project Secrets

```bash
# Set a secret
eve secrets set API_KEY "your-api-key" --project proj_xxx

# List keys (no values)
eve secrets list --project proj_xxx

# Delete a secret
eve secrets delete API_KEY --project proj_xxx

# Import from file
eve secrets import .env --project proj_xxx
```

### Secret Interpolation

Reference secrets in `.eve/manifest.yaml` using `${secret.KEY}`:

```yaml
services:
  api:
    environment:
      API_KEY: ${secret.API_KEY}
```

### Manifest Validation

Validate that all required secrets are set before deploying:

```bash
eve manifest validate --validate-secrets    # check secret references
eve manifest validate --strict              # fail on missing secrets
```

### Local Secrets File

For local development, create `.eve/dev-secrets.yaml` (gitignored):

```yaml
secrets:
  default:
    API_KEY: local-dev-key
    DB_PASSWORD: local-password
  staging:
    DB_PASSWORD: staging-password
```

### Worker Injection

At job execution time, resolved secrets are injected as environment variables into the worker container. File-type secrets are written to disk and referenced via `EVE_SECRETS_FILE`. The file is removed after the agent process reads it.

### Git Auth

The worker uses secrets for repository access:
- **HTTPS**: `github_token` secret → `Authorization: Bearer` header
- **SSH**: `ssh_key` secret → written to `~/.ssh/` and used via `GIT_SSH_COMMAND`

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Not authenticated | Run `eve auth login` |
| Token expired | Re-run `eve auth login` (tokens auto-refresh if within 5 min of expiry) |
| Bootstrap already completed | Use `eve auth login` (existing user) or `eve admin invite` (new users). On non-prod stacks, `eve auth bootstrap` auto-attempts server recovery. For wrong-email recovery: `eve auth bootstrap --email correct@example.com` |
| Secret missing | Confirm with `eve secrets list` and set the key |
| Interpolation error | Verify `${secret.KEY}` spelling; run `eve manifest validate --validate-secrets` |
| Git clone failed | Check `github_token` or `ssh_key` secret is set |
| Service can't reach API | Verify `EVE_API_URL` is injected (check `eve env show`) |
| Scoped access denied | Run `eve access explain <permission> <resource> --org <org>` to see scope match details. Check that the binding's scope constraints include the target path/schema |
| Wrong role shown | Role is resolved from live DB memberships. Run `eve auth permissions` to see effective role. If multi-org, check `eve auth status` for per-org membership listing |
| Short-lived Claude token in jobs | Run `eve auth creds` to check token type. If `oauth` (not `setup-token`), regenerate with `claude setup-token` then re-sync with `eve auth sync` |
| Codex token expired between jobs | Automatic write-back should refresh it. If not, re-run `eve auth sync`. Check that `~/.codex/auth.json` or `~/.code/auth.json` has a fresh token |

### Incident Response (Secret Leak)

If a secret may be compromised:
1. **Contain**: Rotate the secret immediately via `eve secrets set`
2. **Invalidate**: Redeploy affected environments
3. **Audit**: Check `eve job list` for recent jobs that used the secret
4. **Recover**: Generate new credentials at the source (GitHub, AWS, etc.)
5. **Document**: Record the incident and update rotation procedures
