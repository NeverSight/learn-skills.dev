---
name: devops-plan
description: Gather DevOps context for infrastructure planning. Detects IaC tools, providers, and recommends skills. Use when /majestic:plan detects infrastructure work.
allowed-tools: Read Grep Glob Bash Task
---

# DevOps Plan Context

Gather infrastructure context for planning. Returns structured findings for the parent plan command.

## When Called

This skill is invoked by `/majestic:plan` when DevOps keywords are detected in the feature description.

## Workflow

### 1. Detect IaC Files

Check for existing infrastructure code:

```bash
# Terraform/OpenTofu
ls *.tf infra/*.tf terraform/*.tf infrastructure/*.tf 2>/dev/null

# Ansible
ls ansible.cfg playbook.yml ansible/*.yml playbooks/*.yml 2>/dev/null
ls -d roles/ ansible/roles/ 2>/dev/null

# Cloud-init
ls cloud-init*.yml user-data*.yml cloud-config*.yml 2>/dev/null
```

**Set flags:**
- `HAS_TERRAFORM: true/false`
- `HAS_ANSIBLE: true/false`
- `HAS_CLOUD_INIT: true/false`

### 2. Detect Providers

If Terraform files exist, extract providers:

```bash
grep -h "provider\s*\"" *.tf infra/*.tf 2>/dev/null | grep -oE '"[a-z]+"' | tr -d '"' | sort -u
```

Common providers to detect:
- `aws`, `google`, `azurerm` - Major clouds
- `hcloud` - Hetzner
- `digitalocean` - DigitalOcean
- `cloudflare` - Cloudflare
- `backblaze` - Backblaze B2

### 3. Map Skills

Based on detection, recommend skills:

| Detection | Skill | Purpose |
|-----------|-------|---------|
| Any `.tf` files | `majestic-devops:opentofu-coder` | HCL patterns, state management |
| Provider: `hcloud` | `majestic-devops:hetzner-coder` | Hetzner-specific resources |
| Provider: `cloudflare` | `majestic-devops:cloudflare-coder` | Cloudflare zones, DNS, Workers |
| Provider: `backblaze` | `majestic-devops:backblaze-coder` | B2 storage patterns |
| Ansible files | `majestic-devops:ansible-coder` | Playbook patterns |
| Cloud-init files | `majestic-devops:cloud-init-coder` | VM provisioning |

### 4. Security Review

If existing IaC files found, run security audit:

```
Task(subagent_type: "majestic-devops:infra-security-review", prompt: "Audit existing infrastructure code for security issues")
```

Capture findings for the plan.

### 5. Return Context

Return structured context to the calling plan command:

```markdown
## Infrastructure Context

### Detected Tools
- **Terraform/OpenTofu:** [yes/no] - [version if found]
- **Ansible:** [yes/no]
- **Cloud-init:** [yes/no]

### Providers
[List detected providers]

### Skills to Apply
| Skill | Purpose |
|-------|---------|
| `majestic-devops:opentofu-coder` | [reason] |
| ... | ... |

### Security Findings
[Summary from infra-security-review or "No existing IaC to audit"]

### Recommendations
- [Any specific recommendations based on detection]
```

## Notes

- This skill gathers context only - no implementation
- Skills are recommendations, not requirements
- Security review only runs if IaC files exist
