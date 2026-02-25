---
name: terraform-gcp-integration
description: |
  Provision and manage GCP resources with Terraform. Use when working with Pub/Sub topics/subscriptions, GKE clusters,
  Cloud SQL, IAM roles, Cloud Storage, VPCs, service accounts, or any GCP service. Covers provider configuration,
  resource patterns, authentication, and GCP-specific best practices.

---

# Terraform GCP Integration Skill

## Table of Contents

**Quick Start** → [What Is This](#purpose) | [When to Use](#when-to-use) | [Simple Example](#quick-start)

**How to Implement** → [Step-by-Step](#instructions) | [Examples](#examples)

**Help** → [Requirements](#requirements) | [See Also](#see-also)

## Purpose

Master GCP resource provisioning with Terraform including provider configuration, Pub/Sub patterns, GKE management, IAM security, and GCP-specific best practices.

## When to Use

Use this skill when you need to:

- **Work with Pub/Sub** - Create topics, subscriptions, and dead letter queues
- **Manage GKE clusters** - Deploy and configure Kubernetes on GCP
- **Configure Cloud SQL** - Set up managed databases with Terraform
- **Set up IAM roles** - Grant service accounts appropriate permissions
- **Work with Cloud Storage** - Create and manage GCS buckets
- **Configure VPCs** - Set up networking infrastructure
- **Manage service accounts** - Create and bind service accounts to resources
- **Import existing GCP resources** - Bring existing infrastructure under Terraform management

**Trigger Phrases:**
- "Create Pub/Sub topic with Terraform"
- "Configure GCP provider authentication"
- "Set up IAM permissions for service account"
- "Deploy GKE cluster"
- "Import existing GCP resource"

## Quick Start

Deploy a Pub/Sub topic with subscription and IAM in 5 minutes:

```bash
# 1. Configure provider
# main.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.26.0"
    }
  }
}

provider "google" {
  project = "ecp-wtr-supplier-charges-prod"
  region  = "europe-west2"
}

# 2. Create resources
# pubsub.tf
resource "google_pubsub_topic" "incoming" {
  name = "supplier-charges-incoming"
}

resource "google_pubsub_subscription" "incoming_sub" {
  name  = "supplier-charges-incoming-sub"
  topic = google_pubsub_topic.incoming.name
}

# 3. Grant permissions
# iam.tf
data "google_service_account" "app" {
  account_id = "app-runtime"
}

resource "google_pubsub_topic_iam_member" "publisher" {
  topic  = google_pubsub_topic.incoming.name
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:${data.google_service_account.app.email}"
}

# 4. Deploy
terraform init
terraform apply
```

## Instructions

### Step 1: Configure GCP Provider

```hcl
# main.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.26.0"  # Pin to minor version
    }
  }
}

provider "google" {
  project = "ecp-wtr-supplier-charges-prod"
  region  = "europe-west2"
  zone    = "europe-west2-a"
}
```

**Version Pinning Best Practices**:
- `>= 5.26.0` - Too loose, allows major updates
- `~> 5.26.0` - Recommended, allows 5.26.x only
- `5.26.0` - Safest, exact version (check updates regularly)

**Authentication** (Terraform auto-detects):
```bash
# Option 1: Application Default Credentials (recommended)
gcloud auth application-default login

# Option 2: Service account
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json

# Option 3: In code (for CI/CD)
provider "google" {
  credentials = file("~/.gcp/credentials.json")
  project     = "ecp-wtr-supplier-charges-prod"
}
```

### Step 2: Work with Pub/Sub Topics

**Create Topic**:
```hcl
resource "google_pubsub_topic" "incoming_charges" {
  name = "supplier-charges-incoming"

  # Retention: How long to keep messages
  message_retention_duration = "604800s"  # 7 days

  # Labels for organization
  labels = {
    environment = "production"
    team        = "charges"
  }

  # KMS encryption (optional)
  kms_key_name = "projects/ecp-wtr-supplier-charges-prod/locations/global/keyRings/key-ring-1/cryptoKeys/key-1"
}
```

**Create Subscription**:
```hcl
resource "google_pubsub_subscription" "incoming_charges_sub" {
  name  = "supplier-charges-incoming-sub"
  topic = google_pubsub_topic.incoming_charges.name

  # Acknowledgment deadline
  ack_deadline_seconds = 60  # 1 minute

  # Message retention for subscription
  message_retention_duration = "86400s"  # 1 day

  # Retry policy (for failed deliveries)
  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "600s"  # 10 minutes
  }

  # Dead Letter Queue for failed messages
  dead_letter_policy {
    dead_letter_topic            = google_pubsub_topic.incoming_dlq.id
    max_delivery_attempts        = 5  # Retry 5 times before DLQ
  }

  labels = {
    environment = "production"
  }
}

# Dead Letter Queue topic
resource "google_pubsub_topic" "incoming_dlq" {
  name   = "supplier-charges-incoming-dlq"
  labels = {
    environment = "production"
  }
}
```

**Filter Messages**:
```hcl
# Only deliver messages matching filter
resource "google_pubsub_subscription" "high_value_charges" {
  name  = "supplier-charges-high-value"
  topic = google_pubsub_topic.incoming_charges.name

  filter = "attributes.amount > 1000"  # CEL filter syntax
}
```

### Step 3: Configure IAM Permissions

**Least Privilege Principle**: Grant minimum required permissions.

**Pub/Sub Roles**:
- `roles/pubsub.editor` - Full control (avoid)
- `roles/pubsub.publisher` - Publish only
- `roles/pubsub.subscriber` - Subscribe only
- `roles/pubsub.viewer` - Read-only

**Grant Permissions**:
```hcl
# Get service account
data "google_service_account" "app_runtime" {
  account_id = "app-runtime"
}

# Grant publisher role
resource "google_pubsub_topic_iam_member" "publisher" {
  topic  = google_pubsub_topic.incoming_charges.name
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:${data.google_service_account.app_runtime.email}"
}

# Grant subscriber role
resource "google_pubsub_subscription_iam_member" "subscriber" {
  subscription = google_pubsub_subscription.incoming_charges_sub.name
  role         = "roles/pubsub.subscriber"
  member       = "serviceAccount:${data.google_service_account.app_runtime.email}"
}

# Grant project-level role (if needed for multiple resources)
resource "google_project_iam_member" "pubsub_editor" {
  project = data.google_project.current.project_id
  role    = "roles/pubsub.admin"
  member  = "serviceAccount:${data.google_service_account.app_runtime.email}"

  # Optional: Add condition for additional security
  condition {
    title       = "Only in production"
    description = "Access only allowed in production environment"
    expression  = "resource.matchTag('environment', 'production')"
  }
}
```

**IAM Data Source**:
```hcl
# Get current project info
data "google_project" "current" {}

# Get existing service account
data "google_service_account" "existing" {
  account_id = "app-runtime"
}

# Use in outputs
output "service_account_email" {
  value = data.google_service_account.existing.email
}
```

### Step 4: Work with Service Accounts

**Create Service Account**:
```hcl
resource "google_service_account" "app_runtime" {
  account_id   = "app-runtime"
  display_name = "Application Runtime Service Account"
  description  = "Service account for application to access Pub/Sub"
}

# Create key
resource "google_service_account_key" "app_runtime_key" {
  service_account_id = google_service_account.app_runtime.name
}

# Export key (for local development)
output "service_account_key_json" {
  value     = base64decode(google_service_account_key.app_runtime_key.private_key)
  sensitive = true
}
```

**Bind Service Account to GKE Node Pool**:
```hcl
resource "google_container_node_pool" "primary" {
  name       = "primary-pool"
  cluster    = google_container_cluster.primary.name
  node_count = 3

  node_config {
    service_account = google_service_account.app_runtime.email
    scopes          = ["cloud-platform"]  # Full API access
  }
}
```

### Step 5: Work with Cloud Storage

**Create Bucket**:
```hcl
resource "google_storage_bucket" "charges_data" {
  name     = "supplier-charges-data-${var.environment}"
  location = "EUROPE-WEST2"

  # Lifecycle rules (auto-delete old objects)
  lifecycle_rule {
    condition {
      age = 30  # Days
    }
    action {
      type = "Delete"
    }
  }

  # Versioning for backup
  versioning {
    enabled = true
  }

  labels = {
    environment = var.environment
  }
}

# Grant service account access
resource "google_storage_bucket_iam_member" "app_reader" {
  bucket = google_storage_bucket.charges_data.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.app_runtime.email}"
}
```

### Step 6: Work with Cloud SQL

**Create Database Instance**:
```hcl
resource "google_sql_database_instance" "charges_db" {
  name             = "supplier-charges-db"
  database_version = "MYSQL_8_0"
  region           = var.region

  settings {
    tier = "db-f1-micro"  # Small instance

    # Backup configuration
    backup_configuration {
      enabled                        = true
      start_time                     = "03:00"
      transaction_log_retention_days = 7
    }

    # IP whitelist
    ip_configuration {
      ipv4_enabled = true
      require_ssl  = true
    }
  }

  deletion_protection = true  # Prevent accidental deletion
}

# Create database
resource "google_sql_database" "charges" {
  name     = "supplier_charges"
  instance = google_sql_database_instance.charges_db.name
}

# Create user
resource "google_sql_user" "app" {
  name     = "app_user"
  instance = google_sql_database_instance.charges_db.name
  password = data.google_secret_manager_secret_version.db_password.secret_data
}
```

### Step 7: Import Existing GCP Resources

**Import into Terraform State**:
```bash
# Find resource ID in GCP
# Example: Pub/Sub topic
gcloud pubsub topics list
# Output: projects/ecp-wtr-supplier-charges-prod/topics/existing-topic

# Import into Terraform
terraform import google_pubsub_topic.existing_topic \
  projects/ecp-wtr-supplier-charges-prod/topics/existing-topic

# Define in Terraform (after import)
resource "google_pubsub_topic" "existing_topic" {
  name = "existing-topic"
}

# Verify
terraform state show google_pubsub_topic.existing_topic
```

**Common Import IDs**:
```bash
# Pub/Sub topic
terraform import google_pubsub_topic.name \
  projects/PROJECT_ID/topics/TOPIC_NAME

# Cloud Storage bucket
terraform import google_storage_bucket.name \
  BUCKET_NAME

# Cloud SQL instance
terraform import google_sql_database_instance.name \
  INSTANCE_NAME

# Service account
terraform import google_service_account.name \
  projects/PROJECT_ID/serviceAccounts/EMAIL

# IAM binding
terraform import google_pubsub_topic_iam_member.name \
  "TOPIC_NAME ROLE MEMBER"
```

## Examples

### Example 1: Complete Pub/Sub Setup with Dead Letter Queue

```hcl
# locals.tf
locals {
  app_name = "supplier-charges"
  prefix   = "${local.app_name}-${var.environment}"
}

# pubsub.tf
resource "google_pubsub_topic" "incoming" {
  name = "${local.prefix}-incoming"
  message_retention_duration = "604800s"
}

resource "google_pubsub_topic" "dlq" {
  name = "${local.prefix}-dlq"
}

resource "google_pubsub_subscription" "incoming_sub" {
  name  = "${local.prefix}-incoming-sub"
  topic = google_pubsub_topic.incoming.name

  ack_deadline_seconds = 60

  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.dlq.id
    max_delivery_attempts = 5
  }
}

# iam.tf
data "google_service_account" "app" {
  account_id = "app-runtime"
}

resource "google_pubsub_topic_iam_member" "publisher" {
  topic  = google_pubsub_topic.incoming.name
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:${data.google_service_account.app.email}"
}

resource "google_pubsub_subscription_iam_member" "subscriber" {
  subscription = google_pubsub_subscription.incoming_sub.name
  role         = "roles/pubsub.subscriber"
  member       = "serviceAccount:${data.google_service_account.app.email}"
}
```

### Example 2: GKE Cluster with Service Account

```hcl
# gke.tf
resource "google_service_account" "gke_nodes" {
  account_id   = "gke-nodes"
  display_name = "GKE Node Service Account"
}

resource "google_container_cluster" "primary" {
  name     = "supplier-charges-cluster"
  location = var.region

  # Cluster configuration
  initial_node_count       = 1
  remove_default_node_pool = true

  # Network
  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name
}

resource "google_container_node_pool" "primary" {
  name       = "primary-pool"
  cluster    = google_container_cluster.primary.name
  node_count = 3

  node_config {
    service_account = google_service_account.gke_nodes.email
    scopes          = ["https://www.googleapis.com/auth/cloud-platform"]
    machine_type    = "n1-standard-1"

    labels = {
      environment = var.environment
    }
  }
}

# Grant Pub/Sub access to GKE nodes
resource "google_pubsub_topic_iam_member" "gke_publisher" {
  topic  = google_pubsub_topic.incoming.name
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:${google_service_account.gke_nodes.email}"
}
```

### Example 3: Multi-Environment Setup

```hcl
# terraform.tfvars.labs
environment = "labs"
region      = "europe-west2"

# terraform.tfvars.prod
environment = "prod"
region      = "europe-west2"

# main.tf
provider "google" {
  project = "ecp-wtr-supplier-charges-${var.environment}"
  region  = var.region
}

# pubsub.tf (uses var.environment in resource names)
resource "google_pubsub_topic" "incoming" {
  name = "supplier-charges-incoming-${var.environment}"
}

# Deploy
terraform apply -var-file=terraform.tfvars.labs
terraform apply -var-file=terraform.tfvars.prod
```

## Requirements

- Terraform 1.x+
- Google Cloud provider v5.26+
- GCP project with appropriate APIs enabled
- gcloud CLI configured
- Service account with necessary permissions

**Enable GCP APIs**:
```bash
gcloud services enable pubsub.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable compute.googleapis.com
gcloud services enable sqladmin.googleapis.com
```

## See Also

- [terraform skill](../terraform-basics/SKILL.md) - General reference
- [terraform-state-management](../terraform-state-management/SKILL.md) - State management
- [terraform-troubleshooting](../terraform-troubleshooting/SKILL.md) - GCP-specific errors
