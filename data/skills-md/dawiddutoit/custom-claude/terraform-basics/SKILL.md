---
name: terraform-basics
description: |
  Provision and manage cloud infrastructure using Infrastructure as Code. Use when creating or modifying GCP resources,
  managing Pub/Sub topics and subscriptions, configuring IAM bindings, deploying multi-environment infrastructure,
  or tracking infrastructure state. Works with GCP, Kubernetes, and remote state management.
---

# Terraform Skill

## Quick Start

Deploy Pub/Sub topics to GCP in 3 minutes:

```bash
# 1. Initialize (downloads providers, sets up backend)
terraform init

# 2. Preview changes
terraform plan

# 3. Apply
terraform apply -auto-approve
```

Terraform configuration:

```hcl
# main.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.26.0"
    }
  }

  backend "gcs" {
    prefix = "supplier-charges-hub"
    bucket = "my-terraform-state"  # Must exist
  }
}

provider "google" {
  project = "ecp-wtr-supplier-charges-${var.environment}"
  region  = var.region
}

resource "google_pubsub_topic" "incoming" {
  name = "supplier-charges-incoming-${var.environment}"
}
```

## When to Use

- Provision cloud infrastructure (GCP resources)
- Manage infrastructure as code
- Deploy multi-environment setups
- Configure IAM bindings
- Track infrastructure state

**Triggers:**
- "Deploy infrastructure to GCP"
- "Create Pub/Sub topics with Terraform"
- "Set up remote state"
- "Configure GCP provider"

## Key Concepts

### Remote State (Required)

```hcl
terraform {
  backend "gcs" {
    bucket = "terraform-state-prod"
    prefix = "supplier-charges-hub"
  }
}
```

**Why?**
- Team collaboration (single source of truth)
- State locking (prevents concurrent modifications)
- Backup and encryption

### Provider Configuration

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.26.0"
    }
  }
}

provider "google" {
  project = "my-project"
  region  = var.region
}
```

### Variables with Validation

```hcl
# variables.tf
variable "environment" {
  type    = string
  default = "labs"

  validation {
    condition     = contains(["labs", "test", "prod"], var.environment)
    error_message = "Environment must be: labs, test, or prod"
  }
}
```

### Resources

```hcl
# pubsub.tf
resource "google_pubsub_topic" "incoming" {
  name                       = "supplier-charges-incoming"
  message_retention_duration = "604800s"  # 7 days
}

resource "google_pubsub_subscription" "incoming_sub" {
  name  = "supplier-charges-incoming-sub"
  topic = google_pubsub_topic.incoming.name

  ack_deadline_seconds = 60

  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.dlq.id
    max_delivery_attempts = 5
  }
}
```

### IAM Permissions

```hcl
# iam.tf
resource "google_pubsub_topic_iam_member" "publisher" {
  topic  = google_pubsub_topic.incoming.name
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:${data.google_service_account.app.email}"
}
```

### Outputs

```hcl
# outputs.tf
output "pubsub_topic_name" {
  description = "Name of the Pub/Sub incoming topic"
  value       = google_pubsub_topic.incoming.name
}
```

## Common Commands

```bash
# Initialize
terraform init

# Preview changes
terraform plan

# Apply changes
terraform apply

# View current state
terraform state list

# Destroy infrastructure (WARNING!)
terraform destroy

# Format code
terraform fmt -recursive

# Validate syntax
terraform validate
```

## Multi-Environment Pattern

```hcl
# terraform.tfvars.labs
environment = "labs"

# terraform.tfvars.prod
environment = "prod"
```

Apply to different environments:
```bash
terraform apply -var-file="terraform.tfvars.labs"
terraform apply -var-file="terraform.tfvars.prod"
```

## Requirements

- Terraform 1.x+
- GCP credentials (via `gcloud auth application-default login`)
- GCS bucket for remote state (pre-created)
- IAM permissions in GCP (Owner or Editor)

**Installation:**
```bash
# macOS
brew install terraform

# Verify
terraform version
```

## See Also

- **Core Concepts**: Resources, Data Sources, Providers, Backends
- **Best Practices**: Naming Conventions, Variable Validation
- **Security**: Secrets Management, IAM Bindings
- **State Management**: Remote State, Locking
