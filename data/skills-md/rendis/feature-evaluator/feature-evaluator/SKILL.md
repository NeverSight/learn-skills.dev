---
name: feature-evaluator
description: >-
  Manage feature flags, targeting rules, packs, segments, and experiments via
  MCP tools. Evaluate features, validate expressions, manage workspaces.
  Use for feature flag management, rule-based targeting, A/B experiments,
  segment targeting, pack-based feature bundling, and expression testing.
allowed-tools:
  - mcp__feature-evaluator__*
---

# Feature Evaluator MCP

MCP integration for the Feature Evaluator — a feature flag system with rule-based evaluation, segment targeting, and pack-based feature bundling.

## Setup

### Dev Mode (AUTH_DISABLED=true on backend)

```bash
make server       # Start API on port 8080
make build-mcp    # Build MCP binary
```

`.mcp.json` at project root configures Claude Code to spawn the MCP server with `FE_AUTH_TOKEN=dev-token`.

### OIDC (production)

```bash
make build-mcp                                    # Build MCP binary
./apps/mcp/bin/feature-evaluator-mcp login        # Open browser → Keycloak login
./apps/mcp/bin/feature-evaluator-mcp status       # Verify token is valid
./apps/mcp/bin/feature-evaluator-mcp logout       # Clear stored tokens
```

Remove `FE_AUTH_TOKEN` from `.mcp.json` env so the MCP server reads OIDC tokens from `~/.feature-evaluator/tokens.json` instead. Tokens auto-refresh via refresh token.

For custom OIDC providers set `FE_OIDC_ISSUER` and `FE_OIDC_CLIENT_ID` env vars.

## Quick Start Workflow

```
1. fe_list_workspaces         → discover available workspaces
2. fe_set_workspace           → switch workspace (validates it exists)
3. fe_list_features           → browse existing features
4. fe_create_feature          → create feature (key, name, valueType, defaultValue)
5. fe_create_rule             → add targeting rule with expression
6. fe_validate_expression     → check expression syntax before saving
7. fe_evaluate                → test evaluation with sample context
8. fe_dashboard_stats         → view workspace statistics
```

## Tool Reference

### Workspace

| Tool | Purpose | Key Args |
|------|---------|----------|
| `fe_list_workspaces` | List all workspaces | — |
| `fe_set_workspace` | Switch active workspace | `key` |

### Features

| Tool | Purpose | Key Args |
|------|---------|----------|
| `fe_list_features` | List features (paginated) | `search?`, `value_type?`, `enabled?`, `tag?`, `environment?` |
| `fe_get_feature` | Get feature with rules | `key` |
| `fe_create_feature` | Create feature | `key`, `name`, `value_type`, `default_value`, `access_policy?`, `auth_profile_key?` |
| `fe_update_feature` | Update feature | `key`, `name`, `access_policy?`, `auth_profile_key?` |
| `fe_toggle_feature` | Enable/disable | `key`, `enabled` |
| `fe_delete_feature` | Delete feature | `key` |

### Rules

| Tool | Purpose | Key Args |
|------|---------|----------|
| `fe_list_rules` | List rules for feature | `feature_key` |
| `fe_create_rule` | Create targeting rule | `feature_key`, `name`, `expression`, `value` |
| `fe_update_rule` | Update rule | `feature_key`, `rule_id`, `name`, `expression`, `value` |
| `fe_delete_rule` | Delete rule | `feature_key`, `rule_id` |
| `fe_reorder_rules` | Reorder rules | `feature_key`, `rule_ids` |

### Evaluation

| Tool | Purpose | Key Args |
|------|---------|----------|
| `fe_evaluate` | Evaluate single feature | `feature_key`, `context?` |
| `fe_bulk_evaluate` | Evaluate multiple features | `feature_keys`, `context?` |

### Packs

| Tool | Purpose | Key Args |
|------|---------|----------|
| `fe_list_packs` | List packs | `search?` |
| `fe_get_pack` | Get pack detail | `key` |
| `fe_create_pack` | Create pack | `key`, `name`, `feature_keys?`, `tier_key?`, `inherits_from?`, `trial_until?` |
| `fe_update_pack` | Update pack | `key`, `name?`, `description?`, `feature_keys?`, `tier_key?`, `inherits_from?`, `trial_until?` |
| `fe_toggle_pack` | Enable/disable | `key`, `enabled` |
| `fe_activate_pack` | Activate on target | `key`, `target_type`, `target_id` |
| `fe_deactivate_pack` | Deactivate from target | `key`, `target_type`, `target_id` |

### Tiers

Tiers are predefined (24 total across 6 categories: entry, growth, advanced, top, special, technical). Assign to packs via `tier_key`.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `fe_list_tiers` | List all predefined tiers | — |

### Segments

| Tool | Purpose | Key Args |
|------|---------|----------|
| `fe_list_segments` | List segments | `search?` |
| `fe_get_segment` | Get segment detail | `key` |
| `fe_create_segment` | Create segment | `key`, `name` |

### Expressions

| Tool | Purpose | Key Args |
|------|---------|----------|
| `fe_validate_expression` | Validate syntax | `expression` |
| `fe_test_expression` | Test with context | `expression`, `context` |

### Experiments

| Tool | Purpose | Key Args |
|------|---------|----------|
| `fe_list_experiments` | List experiments | `status?` |
| `fe_get_experiment` | Get experiment | `id` |
| `fe_create_experiment` | Create experiment | `feature_key`, `name` |
| `fe_manage_experiment` | Lifecycle control | `id`, `action` (start/pause/complete) |

### Dashboard & Audit

| Tool | Purpose | Key Args |
|------|---------|----------|
| `fe_dashboard_stats` | Workspace statistics | — |
| `fe_list_tags` | List tags | — |
| `fe_audit_errors` | Evaluation errors | `feature?` |
| `fe_changelog` | Change history | `entity?` |

## Expression Language (expr-lang)

Rules use `expr-lang/expr`. Full reference: [references/expressions.md](references/expressions.md)

### Eval Request

```json
{
  "featureKey": "my-feature",
  "context": {
    "user": { "id": "u-1", "email": "alice@empresa.com", "role": "admin" },
    "tenant": { "id": "t-1" },
    "campus": { "id": "c-1" },
    "program": { "id": "p-1" },
    "custom": { "country": "US" }
  },
  "environment": "production"
}
```

Each `context` key becomes a top-level variable in expressions (`user.*`, `tenant.*`, etc.).

### Expression Variables

| Variable | Source |
|----------|--------|
| `user.*`, `tenant.*`, `campus.*`, `program.*` | `context` in request body |
| `headers.*` | HTTP headers (via feature InputContract) |
| `requestBody.*` | Request body fields |
| `authenticated` | True if auth profile validation passed |
| `derived.email` | JWT `email` claim, fallback `context.user.email` |
| `derived.userId` | JWT `sub` claim, fallback `context.user.id` |
| `derived.subject` | JWT `sub` claim (no fallback) |
| `derived.name` | JWT `name` claim (no fallback) |
| `derived.bearerTokenPresent` | True if Bearer token in request |
| `derived.apiKeyPresent` | True if API key in request |

**JWT auto-extraction:** Send `Authorization: Bearer <jwt>` → claims `sub`, `email`, `name` auto-populate `derived.*`. JWT claims take priority over context body.

### Builtin Functions

| Function | Description |
|----------|-------------|
| `now()` | Current UTC time |
| `dateBefore(date, ref)` | True if date < ref (RFC3339, `YYYY-MM-DD`) |
| `dateAfter(date, ref)` | True if date > ref |
| `contains(val, needle)` | String containment |
| `startsWith(val, prefix)` | String prefix |
| `endsWith(val, suffix)` | String suffix |
| `inSegment(key)` | Segment membership check |
| `externalApi(key)` | External API validation |

### Common Patterns

```
# Email targeting (from JWT)
derived.email == "admin@empresa.com"
endsWith(derived.email, "@empresa.com")

# Email targeting (from context body)
user.email == "admin@empresa.com"

# Auth + role
authenticated && user.role == "admin"

# Segments
inSegment("beta-users")

# Date range
dateAfter(now(), "2025-06-01") && dateBefore(now(), "2025-12-31")

# Combined
tenant.id == "acme" && inSegment("early-access") && authenticated
```

### Security Limits

Max AST depth: 10, max nodes: 100, max `inSegment()` calls: 5, max string length: 1000.
Denied: exec, system, import, require, __proto__, constructor, prototype, eval, Function, process.

## Known API Behaviors

- List responses: `{"data": [...], "pagination": {"page": 1, "pageSize": 20, "total": N, "totalPages": M}}`
- Toggle/Delete: return 204 No Content
- Errors: `{"error": {"code": "...", "message": "...", "messageKey": "..."}}`
- Pack targets: `tenant`, `campus`, `program`
- Value types: `boolean`, `string`, `number`, `json`
- Access policies: `public` (default), `optional`, `required`
