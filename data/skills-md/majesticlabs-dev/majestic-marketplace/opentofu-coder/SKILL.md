---
name: opentofu-coder
description: This skill guides writing Infrastructure as Code using OpenTofu (open-source Terraform fork). Use when creating .tf files, managing cloud infrastructure, configuring providers, or designing reusable modules.
allowed-tools: Read Write Edit MultiEdit Grep Glob Bash WebSearch
---

# OpenTofu Coder

## ⚠️ SIMPLICITY FIRST - Default to Flat Files

**ALWAYS start with the simplest approach. Only add complexity when explicitly requested.**

### Simple (DEFAULT) vs Overengineered

| Aspect | ✅ Simple (Default) | ❌ Overengineered |
|--------|---------------------|-------------------|
| Structure | Flat .tf files in one directory | Nested modules/ + environments/ directories |
| Modules | None or only remote registry modules | Custom local modules for simple resources |
| Environments | Workspaces OR single tfvars | Duplicate directory per environment |
| Variables | Inline defaults, minimal tfvars | Complex variable hierarchies |
| File count | 3-5 .tf files total | 15+ files across nested directories |

### When to Use Simple Approach (90% of cases)

- Managing 1-5 resources of each type
- Single provider, single region
- Small team or solo developer
- Standard infrastructure patterns

### When Complexity is Justified (10% of cases)

- Enterprise multi-region, multi-account
- Reusable modules shared across teams
- Complex dependency chains
- User explicitly requests modular structure

**Rule: If you can define everything in 5 flat .tf files, DO IT.**

### Simple Project Structure (DEFAULT)

```
infra/
├── main.tf           # All resources
├── variables.tf      # Input variables
├── outputs.tf        # Outputs
├── versions.tf       # Provider versions
└── terraform.tfvars  # Variable values (gitignored)
```

## Overview

OpenTofu is a community-driven, open-source fork of Terraform under MPL-2.0 license, maintained by the Linux Foundation. It uses HashiCorp Configuration Language (HCL) for declarative infrastructure management across cloud providers.

## Core Philosophy

Prioritize:
- **Declarative over imperative**: Describe desired state, not steps
- **Idempotency**: Apply safely multiple times with same result
- **Modularity**: Compose infrastructure from reusable modules
- **State as truth**: State file is the source of truth for managed resources
- **Immutable infrastructure**: Replace resources rather than mutate in place

## HCL Syntax Essentials

### Resource Blocks

```hcl
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name        = "${var.project}-web"
    Environment = var.environment
  }
}
```

### Data Sources

```hcl
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  owners = ["099720109477"]  # Canonical
}
```

### Variables

```hcl
variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_types" {
  description = "Map of environment to instance type"
  type        = map(string)
  default = {
    dev     = "t3.micro"
    staging = "t3.small"
    prod    = "t3.medium"
  }
}
```

### Outputs

```hcl
output "instance_ip" {
  description = "Public IP of the web instance"
  value       = aws_instance.web.public_ip
  sensitive   = false
}

output "database_password" {
  description = "Generated database password"
  value       = random_password.db.result
  sensitive   = true
}
```

### Locals

```hcl
locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "OpenTofu"
  }

  name_prefix = "${var.project}-${var.environment}"
}
```

## Meta-Arguments

### count - Create Multiple Instances

```hcl
resource "aws_instance" "server" {
  count = var.server_count

  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name = "${local.name_prefix}-server-${count.index}"
  }
}
```

### for_each - Create from Map/Set

```hcl
resource "aws_iam_user" "users" {
  for_each = toset(var.user_names)

  name = each.value
  path = "/users/"
}

resource "aws_security_group_rule" "ingress" {
  for_each = var.ingress_rules

  type              = "ingress"
  from_port         = each.value.port
  to_port           = each.value.port
  protocol          = each.value.protocol
  cidr_blocks       = each.value.cidr_blocks
  security_group_id = aws_security_group.main.id
}
```

### depends_on - Explicit Dependencies

```hcl
resource "aws_instance" "app" {
  ami           = var.ami_id
  instance_type = var.instance_type

  depends_on = [
    aws_db_instance.database,
    aws_elasticache_cluster.cache
  ]
}
```

### lifecycle - Control Resource Behavior

```hcl
resource "aws_instance" "critical" {
  ami           = var.ami_id
  instance_type = var.instance_type

  lifecycle {
    prevent_destroy = true
    create_before_destroy = true
    ignore_changes = [
      tags["LastUpdated"],
      user_data
    ]
  }
}

# Replace when AMI changes
resource "aws_instance" "immutable" {
  ami           = var.ami_id
  instance_type = var.instance_type

  lifecycle {
    replace_triggered_by = [
      null_resource.ami_trigger
    ]
  }
}
```

## Module Design

### Module Structure

```
modules/
└── vpc/
    ├── main.tf          # Primary resources
    ├── variables.tf     # Input variables
    ├── outputs.tf       # Output values
    ├── versions.tf      # Required providers
    └── README.md        # Documentation
```

### Calling Modules

```hcl
module "vpc" {
  source = "./modules/vpc"

  cidr_block  = "10.0.0.0/16"
  environment = var.environment

  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
}

# Remote module with version
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = local.cluster_name
  cluster_version = "1.29"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
}
```

### Module Best Practices

- Expose minimal, clear interface of variables
- Use sensible defaults where possible
- Document all variables and outputs
- Avoid over-generic "god" modules
- Prefer composition over configuration flags
- Version pin remote modules

## State Management

### Remote Backend (S3)

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/network/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### OpenTofu State Encryption (Unique Feature)

```hcl
terraform {
  encryption {
    key_provider "pbkdf2" "main" {
      passphrase = var.state_encryption_passphrase
    }

    method "aes_gcm" "encrypt" {
      keys = key_provider.pbkdf2.main
    }

    state {
      method   = method.aes_gcm.encrypt
      enforced = true
    }

    plan {
      method   = method.aes_gcm.encrypt
      enforced = true
    }
  }
}
```

### State Commands

```bash
# List resources in state
tofu state list

# Show specific resource
tofu state show aws_instance.web

# Move resource (refactoring)
tofu state mv aws_instance.old aws_instance.new

# Remove from state (without destroying)
tofu state rm aws_instance.imported

# Import existing resource
tofu import aws_instance.web i-1234567890abcdef0
```

See [Provider Configuration](references/provider-config.md) for AWS provider setup, authentication methods, and multi-provider patterns.

See [Environment Strategies](references/environment-strategies.md) for workspaces and directory-based environment management.

## CLI Workflow

```bash
# Initialize working directory
tofu init

# Validate configuration
tofu validate

# Format code
tofu fmt -recursive

# Preview changes
tofu plan -out=plan.tfplan

# Apply changes
tofu apply plan.tfplan

# Destroy infrastructure
tofu destroy

# Show current state
tofu show

# Refresh state from actual infrastructure
tofu refresh
```

## Best Practices Checklist

When writing OpenTofu/Terraform code:

- [ ] Use remote backend with locking for team use
- [ ] Enable state encryption (OpenTofu feature)
- [ ] Never commit `.tfstate` or `.tfvars` with secrets to VCS
- [ ] Pin provider and module versions
- [ ] Use `tofu plan` before every `apply`
- [ ] Use `lifecycle.prevent_destroy` for critical resources
- [ ] Document all variables and outputs
- [ ] Use `locals` for computed values and tags
- [ ] Prefer `for_each` over `count` for named resources
- [ ] Use validation blocks for variable constraints
- [ ] Store secrets in secret managers, not in code

## Common Patterns

### Conditional Resources

```hcl
resource "aws_eip" "static" {
  count = var.create_elastic_ip ? 1 : 0

  instance = aws_instance.web.id
}
```

### Dynamic Blocks

```hcl
resource "aws_security_group" "main" {
  name = "${local.name_prefix}-sg"

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

## References

For detailed patterns and examples:
- [references/hcl-patterns.md](references/hcl-patterns.md) - Advanced HCL patterns
- [references/project-scaffolding.md](references/project-scaffolding.md) - Directory structure, .gitignore, next_steps output, security-first variables
- [references/post-provisioning.md](references/post-provisioning.md) - bin/setup-server scripts for post-infra, pre-deployment setup
- [references/state-management.md](references/state-management.md) - State operations and encryption
- [references/provider-examples.md](references/provider-examples.md) - Multi-cloud provider configs
- [references/makefile-automation.md](references/makefile-automation.md) - Makefile workflows for plan/apply/destroy
