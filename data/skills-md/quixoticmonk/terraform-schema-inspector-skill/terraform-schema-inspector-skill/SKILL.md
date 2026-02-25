---
name: terraform-schema-inspector-skill
description: Identify Terraform provider support for resources, data sources, actions, list resources, ephemeral resources, and functions. Use when checking provider capabilities, asking "what resources does X provider support", "does provider Y have actions", or querying specific provider features.
license: MIT
compatibility: Requires Terraform CLI and jq
metadata:
  author: quixoticmonk
  version: "0.3.0"
---

# Terraform Schema Inspector

Identify which capabilities a Terraform provider supports:
- **Resources**: Standard managed resources
- **Data Sources**: Read-only data queries
- **Actions**: Imperative operations during lifecycle events
- **List Resources**: Resources supporting bulk list operations
- **Ephemeral Resources**: Temporary resources for credentials/tokens
- **Functions**: Provider-specific functions

## Workflow

When a user asks about provider capabilities:

1. **Prepare working directory**
   - Create a temporary directory: `/tmp/tf-inspect-$$`
   - Change to that directory

2. **Determine provider source**
   - Use `get_latest_provider_version` tool to find namespace and version
   - Common namespaces: `hashicorp` (aws, google, azurerm), `integrations` (github), `oracle` (oci)

3. **Create provider configuration**
   - Create `main.tf` with provider source:
     ```hcl
     terraform {
       required_providers {
         <provider> = {
           source = "<namespace>/<provider>"
           version = "~> <version>"
         }
       }
     }
     
     provider "<provider>" {}
     ```

4. **Initialize Terraform**
   - Run `terraform init -upgrade` using `execute_bash`
   - This downloads provider binaries from the registry
   - User can see what's being downloaded

5. **Run inspection script**
   ```bash
   /path/to/skill/scripts/check.sh <capability_type> <provider_name>
   ```
   
   The script:
   - Validates inputs
   - Reads existing schema from initialized providers
   - Filters and formats output as JSON

6. **Present results**
   - Display JSON output
   - Empty arrays mean no capabilities of that type

7. **Clean up**
   - Remove temporary directory: `rm -rf /tmp/tf-inspect-*`

## Security

**Agent-Managed Operations:**
- Provider configuration creation (agent creates main.tf)
- Terraform initialization (agent runs `terraform init`)
- Provider binary downloads (visible to user during init)

**Script Operations (Read-Only):**
- Input validation: Provider names restricted to `^[a-zA-Z0-9_-]{1,64}$`
- Schema reading: Queries existing `.terraform/` directory
- Safe string handling: Uses jq's `--arg` to prevent injection

**User Visibility:**
- All provider downloads happen via agent's `terraform init` command
- User sees what's being downloaded before script execution
- Script only reads existing schema data

## Capability Types

- `resources` - Standard managed resources
- `data-sources` - Read-only data sources
- `actions` - Imperative lifecycle actions
- `list` - List resource capabilities
- `ephemeral` - Ephemeral resources (credentials, tokens)
- `functions` - Provider-specific functions

## Examples

### Check Google provider for actions
```bash
# In temporary directory with provider config:
/path/to/skill/scripts/check.sh actions google
```

### Check AWS ephemeral resources
```bash
/path/to/skill/scripts/check.sh ephemeral aws
```

### Check Azure data sources
```bash
/path/to/skill/scripts/check.sh data-sources azurerm
```

### Check all configured providers for a capability
```bash
# Omit provider name to check all:
/path/to/skill/scripts/check.sh functions
```

## Output Format

Returns JSON mapping providers to their supported capabilities:

```json
{
  "aws": [
    "aws_cognito_identity_openid_token_for_developer_identity",
    "aws_ecr_authorization_token",
    "aws_eks_cluster_auth",
    "aws_kms_secrets",
    "aws_lambda_invocation",
    "aws_secretsmanager_random_password",
    "aws_secretsmanager_secret_version",
    "aws_ssm_parameter"
  ]
}
```

## Requirements

- Terraform CLI installed
- jq (JSON processor)

## Notes

- Agent handles provider configuration and initialization
- Script operates in read-only mode on existing schema
- Work in temporary directories to avoid workspace pollution
- Empty arrays mean provider has no capabilities of that type
