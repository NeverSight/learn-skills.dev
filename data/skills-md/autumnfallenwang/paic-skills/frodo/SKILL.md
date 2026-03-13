---
name: frodo
description: "frodo CLI (v3.1.0) for managing PingOne Advanced Identity Cloud (AIC). Handles config export/import, journeys/trees, SAML providers, scripts, OAuth2 clients, ESV secrets/variables, log tailing, mappings, themes, services, agents, authorization policies, and tenant promotion. Contains environment shorthands, standard flag combos, and workflow recipes."
---

# Frodo CLI Skill

For full flag details, run `frodo <command> <action> --help`.

- CLI repo: https://github.com/rockcarver/frodo-cli
- Library repo: https://github.com/rockcarver/frodo-lib

## Environments

Use these shorthand substrings with any frodo command (matches against saved connection profiles):

| Shorthand | Tenant | Purpose |
|-----------|--------|---------|
| `sandbox` | yourtenantsandbox | Sandbox |
| `dev` | yourtenantdev | Development |
| `staging` | yourtenantstaging | Staging |
| `prod` | yourtenantprod | Production |

```bash
frodo conn list                  # See all saved profiles
frodo conn describe sandbox          # Describe a specific profile
```

## Config Export/Import

**Syntax**: `frodo config export [options] [host] [realm] [username] [password]`

```bash
# Team standard — snapshot to dated folder
frodo config export -sxoAND ./sandbox_20260227 sandbox

# Everything to single file
frodo config export -a sandbox

# Specific realm only
frodo config export -ar sandbox alpha

# With encrypted secret values for cross-env migration
frodo config export -a --include-active-values --target dev sandbox
```

**Syntax**: `frodo config import [options] [host] [realm] [username] [password]`

```bash
# Import from separate files
frodo config import -A -D ./sandbox_export dev

# Import from single file
frodo config import -a -f sandbox-all.json dev
```

Note: `-g` for global-only, `-r` for realm-only, `-R` for read-only config, `-d` to include default scripts.

## Journey/Tree

**Syntax**: `frodo journey <list|export|import|delete|describe|disable|enable|prune> [options] [host] [realm]`

```bash
frodo journey list sandbox
frodo journey export -i "MyLoginJourney" sandbox               # Single with deps
frodo journey export -i "MyLoginJourney" --no-deps sandbox     # Single without deps
frodo journey export -A sandbox                                 # All to separate files
frodo journey import -i "MyLoginJourney" -f MyLoginJourney.journey.json dev
frodo journey import -A -D ./journeys dev
frodo journey delete -i "MyLoginJourney" sandbox
frodo journey describe -i "MyLoginJourney" sandbox
frodo journey disable -i "MyLoginJourney" sandbox
frodo journey enable -i "MyLoginJourney" sandbox
frodo journey prune sandbox                                     # Clean orphaned artifacts
```

Note: `--no-deps` skips scripts, SAML providers, themes, social IdPs. `--no-coords` skips node positions.

## SAML

**Syntax**: `frodo saml <list|export|import|delete|describe> [options] [host] [realm]`

```bash
frodo saml list sandbox
frodo saml export -A sandbox
frodo saml export -i "https://sp.example.com/saml" sandbox
frodo saml import -i "https://sp.example.com/saml" -f provider.saml.json dev
frodo saml delete -i "https://sp.example.com/saml" sandbox
frodo saml describe -i "https://sp.example.com/saml" sandbox
```

Related — Circles of Trust and metadata:

```bash
frodo saml cot list sandbox
frodo saml cot export -A sandbox
frodo saml cot import -A dev
frodo saml metadata export -i "https://sp.example.com/saml" sandbox
```

## Script

**Syntax**: `frodo script <list|export|import|delete|describe> [options] [host] [realm]`

```bash
frodo script list sandbox
frodo script export -A sandbox                    # All to separate files
frodo script export -n "MyScript" sandbox         # By name
frodo script export -i <script-uuid> sandbox      # By UUID
frodo script import -A dev
frodo script delete -i <script-uuid> sandbox
frodo script describe -i <script-uuid> sandbox
```

## OAuth2 Client

**Syntax**: `frodo oauth client <list|export|import|delete> [options] [host] [realm]`

```bash
frodo oauth client list sandbox
frodo oauth client export -A sandbox
frodo oauth client export -i "myClientId" sandbox
frodo oauth client import -A dev
frodo oauth client delete -i "myClientId" sandbox
```

## ESV (Secrets & Variables)

**Syntax**: `frodo esv <secret|variable> <list|describe|export|import|set> [options] [host]`

```bash
frodo esv secret list -lu sandbox                            # List with usage info
frodo esv secret describe -i "esv-my-secret" sandbox
frodo esv variable list sandbox
frodo esv variable describe -i "esv-my-variable" sandbox
frodo esv apply sandbox                                      # Apply pending changes
```

Note: `esv apply` triggers pod restart, takes up to 10 minutes. `-l` for long format, `-u` for usage info.

## Log

**Syntax**: `frodo log <tail|fetch|list> [options] [host]`

```bash
frodo log tail sandbox                         # All logs, all levels
frodo log tail -l 0 sandbox                    # Errors only (0=ERROR, 1=WARN, 2=INFO, 3=DEBUG, 4=ALL)
frodo log tail -c am-core,idm-core sandbox     # Specific sources
frodo log tail -t <txid> sandbox               # Filter by transaction ID
frodo log tail -d sandbox                      # Default noise filters
frodo log fetch sandbox                        # Historical logs
frodo log list sandbox                         # Available log sources
```

## Other Resources (Same Pattern)

All follow: `frodo <resource> <list|export|import|delete> [options] [host] [realm]`

Consistent flags: `-a` (all/single file), `-A` (all/separate files), `-i` (specific item), `-f` (file), `-D` (directory).

```bash
# Applications (NOT OAuth2 clients — use frodo oauth client for those)
frodo app list sandbox
frodo app export -A sandbox
frodo app import -A dev

# Email templates (delete new in v3.1.0)
frodo email template list sandbox
frodo email template export -A sandbox
frodo email template delete -i <template-id> sandbox

# IDM mappings
frodo mapping list sandbox
frodo mapping export -A sandbox
frodo mapping rename sandbox             # Legacy (sync/) → new (mapping/) naming
frodo mapping rename -l sandbox          # New → legacy

# IDM config objects
frodo idm list sandbox
frodo idm export -A sandbox
frodo idm count -n alpha_user sandbox

# Social identity providers, AM services, themes, realms, roles, agents, authn, authz
frodo idp list sandbox
frodo service list sandbox
frodo theme list sandbox
frodo realm list sandbox
frodo realm describe sandbox
frodo role list sandbox
frodo agent list sandbox
frodo authn describe sandbox
frodo authz policy list sandbox
frodo authz set list sandbox
frodo authz type list sandbox
```

## IDM Endpoint Development (frodo3074)

> **Temporary**: `frodo3074` is a custom build that adds `-x`/`--extract` to `idm export` and `idm import`. This flag splits inline JavaScript from endpoint JSON into separate `.js` files, making endpoint code easier to edit and diff. Use `frodo3074` instead of `frodo` for IDM endpoint work. This will be merged into mainline frodo in the future.

```bash
# Export all IDM configs with JavaScript extraction
frodo3074 idm export -xAND ./exports sandbox

# Export single endpoint with JS extraction, no metadata
frodo3074 idm export -i endpoint/custom_api -f custom_api.idm.json -xN sandbox

# Import after modifications (rehydrates .js back into JSON)
frodo3074 idm import -i endpoint/custom_api -f custom_api.idm.json sandbox
```

```bash
# frodo3074 config export — extracts scripts AND endpoint JS (mainline frodo -x only extracts scripts)
frodo3074 config export -sxoAND ./sandbox sandbox
```

Note: `-x` extracts JS into `.js` files alongside the `.idm.json` on export, and rehydrates them back on import. Without `-x`, endpoint JavaScript is embedded inline in the JSON (hard to read/edit).

## Admin

**Syntax**: `frodo admin <command> [options] [host]`

```bash
frodo admin list-oauth2-clients-with-admin-privileges sandbox
frodo admin grant-oauth2-client-admin-privileges sandbox
frodo admin revoke-oauth2-client-admin-privileges sandbox
frodo admin list-static-user-mappings sandbox
frodo admin repair-org-model sandbox
frodo admin federation list sandbox
frodo info sandbox                                    # Tenant version/connection info
frodo info --json sandbox
```

## Gotchas

- `frodo app` manages AIC application templates (v2+), NOT OAuth2 clients. Use `frodo oauth client` for OAuth2.
- `frodo config help export` works (config has a special `help` subcommand with examples), but other commands need `frodo <cmd> <action> --help`.
- Connection profiles use URL substring matching — `sand` works because it uniquely matches the sandbox tenant URL.
- `esv apply` triggers a pod restart that takes up to 10 minutes. Don't re-run or assume failure if slow.
- Export flags `-a`/`-A` in v3.0.8+ no longer stop prematurely on errors.
- `email template delete` is new in v3.1.0.
- Proxy Connect support (`--authentication-header-overrides` on `conn save`) added in v3.0.10.
