---
name: infrastructure-cicd-data-engineering
description: Deploy data infrastructure changes using CI/CD patterns with GitHub Actions, Terraform, and AWS OIDC authentication
triggers:
  - "set up CI/CD for data infrastructure"
  - "deploy terraform with github actions"
  - "configure OIDC for AWS deployments"
  - "automate infrastructure changes for data engineering"
  - "implement terraform CI/CD pipeline"
  - "set up github actions for terraform"
  - "configure infrastructure deployment workflow"
  - "automate data infrastructure provisioning"
---

# Infrastructure CI/CD for Data Engineering

> Skill by [ara.so](https://ara.so) — Data Skills collection

This project demonstrates practical CI/CD patterns for deploying data infrastructure changes using GitHub Actions, Terraform, and AWS. It uses OpenID Connect (OIDC) for secure, keyless authentication between GitHub Actions and AWS, eliminating the need for long-lived AWS credentials.

## What This Project Does

- **Bootstraps infrastructure**: Creates S3 backend for Terraform state and OIDC provider for GitHub Actions
- **Automates deployments**: Uses GitHub Actions workflows to plan and apply Terraform changes
- **Enforces reviews**: Requires manual approval before production deployments
- **Validates code**: Runs Terraform formatting and validation checks on PRs

## Project Structure

```
.
├── terraform/
│   ├── bootstrap/          # Initial setup (S3 backend, OIDC)
│   │   └── main.tf
│   └── main/              # Main infrastructure definitions
│       └── main.tf
├── .github/
│   └── workflows/
│       ├── ci.yml         # Format and validation checks
│       └── deploy.yml     # Deployment workflow
└── tear-down.sh           # Cleanup script
```

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **Terraform** installed locally (v1.0+)
3. **GitHub Account** and repository access
4. **AWS CLI** configured with credentials

```bash
# Verify Terraform installation
terraform version

# Verify AWS credentials
aws sts get-caller-identity
```

## Bootstrap Setup

### Step 1: Create S3 Backend and OIDC Provider

The bootstrap process creates:
- S3 bucket for Terraform state storage
- DynamoDB table for state locking
- IAM OIDC provider for GitHub Actions
- IAM role that GitHub Actions will assume

```bash
# Initialize and apply bootstrap configuration
terraform -chdir=terraform/bootstrap init
terraform -chdir=terraform/bootstrap apply

# Capture the outputs
terraform -chdir=terraform/bootstrap output
```

**Expected output:**
```
github_actions_role_arn = "arn:aws:iam::123456789012:role/github-actions-role"
state_bucket_name = "my-terraform-state-bucket"
```

### Step 2: Configure GitHub Repository Secrets

Create a repository secret named `AWS_ROLE_ARN`:

1. Navigate to: `Settings → Secrets and variables → Actions → New repository secret`
2. Name: `AWS_ROLE_ARN`
3. Value: The ARN output from bootstrap (without quotes)

```bash
# Example ARN format (don't include quotes when pasting)
arn:aws:iam::123456789012:role/github-actions-role
```

### Step 3: Create GitHub Environment

Set up a production environment with manual approval:

1. Navigate to: `Settings → Environments → New environment`
2. Name: `production`
3. Configure protection rules:
   - ✅ Required reviewers (minimum 1)
   - Add yourself or team members as reviewers

## Bootstrap Terraform Configuration

**terraform/bootstrap/main.tf** (simplified example):

```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# S3 bucket for Terraform state
resource "aws_s3_bucket" "terraform_state" {
  bucket = "${var.project_name}-terraform-state-${var.environment}"
  
  tags = {
    Name        = "Terraform State Bucket"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

# DynamoDB table for state locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "${var.project_name}-terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }
  
  tags = {
    Name        = "Terraform State Lock Table"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# OIDC provider for GitHub Actions
resource "aws_iam_openid_connect_provider" "github_actions" {
  url = "https://token.actions.githubusercontent.com"
  
  client_id_list = [
    "sts.amazonaws.com"
  ]
  
  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1"
  ]
}

# IAM role for GitHub Actions
resource "aws_iam_role" "github_actions" {
  name = "github-actions-terraform-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github_actions.arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:${var.github_org}/${var.github_repo}:*"
          }
        }
      }
    ]
  })
}

# Attach policies to the role
resource "aws_iam_role_policy_attachment" "github_actions_admin" {
  role       = aws_iam_role.github_actions.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

# Outputs
output "github_actions_role_arn" {
  value       = aws_iam_role.github_actions.arn
  description = "ARN of the IAM role for GitHub Actions"
}

output "state_bucket_name" {
  value       = aws_s3_bucket.terraform_state.bucket
  description = "Name of the S3 bucket for Terraform state"
}

output "state_lock_table_name" {
  value       = aws_dynamodb_table.terraform_locks.name
  description = "Name of the DynamoDB table for state locking"
}
```

**terraform/bootstrap/variables.tf**:

```hcl
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "data-infra"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "github_org" {
  description = "GitHub organization or username"
  type        = string
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
}
```

## Main Infrastructure Configuration

**terraform/main/main.tf** (example data infrastructure):

```hcl
terraform {
  required_version = ">= 1.0"
  
  backend "s3" {
    bucket         = "data-infra-terraform-state-production"
    key            = "main/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "data-infra-terraform-locks"
    encrypt        = true
  }
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
      DeployedBy  = "GitHub-Actions"
    }
  }
}

# Example: S3 bucket for data lake
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-data-lake-${var.environment}"
}

resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Example: Glue database for data catalog
resource "aws_glue_catalog_database" "analytics" {
  name        = "${var.project_name}_analytics_${var.environment}"
  description = "Analytics data catalog database"
}

# Example: IAM role for Glue jobs
resource "aws_iam_role" "glue_job" {
  name = "${var.project_name}-glue-job-role-${var.environment}"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "glue_service" {
  role       = aws_iam_role.glue_job.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# Outputs
output "data_lake_bucket" {
  value       = aws_s3_bucket.data_lake.bucket
  description = "Name of the data lake S3 bucket"
}

output "glue_database" {
  value       = aws_glue_catalog_database.analytics.name
  description = "Name of the Glue catalog database"
}
```

## GitHub Actions Workflows

### CI Workflow: Format and Validation

**.github/workflows/ci.yml**:

```yaml
name: Terraform CI

on:
  pull_request:
    branches:
      - main
    paths:
      - 'terraform/**'
      - '.github/workflows/ci.yml'

permissions:
  contents: read
  pull-requests: write

jobs:
  terraform-checks:
    name: Terraform Checks
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.5.0
      
      - name: Terraform Format Check
        id: fmt
        run: terraform fmt -check -recursive terraform/
        continue-on-error: true
      
      - name: Terraform Init (Main)
        run: terraform -chdir=terraform/main init -backend=false
      
      - name: Terraform Validate (Main)
        run: terraform -chdir=terraform/main validate
      
      - name: Comment PR
        if: steps.fmt.outcome == 'failure'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ Terraform formatting check failed. Run `terraform fmt -recursive terraform/` to fix.'
            })
      
      - name: Fail if format check failed
        if: steps.fmt.outcome == 'failure'
        run: exit 1
```

### Deploy Workflow: Plan and Apply

**.github/workflows/deploy.yml**:

```yaml
name: Deploy Infrastructure

on:
  push:
    branches:
      - main
    paths:
      - 'terraform/main/**'
  workflow_dispatch:

permissions:
  id-token: write
  contents: read
  pull-requests: write

jobs:
  terraform-plan:
    name: Terraform Plan
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.5.0
      
      - name: Terraform Init
        run: terraform -chdir=terraform/main init
      
      - name: Terraform Plan
        id: plan
        run: |
          terraform -chdir=terraform/main plan -no-color -out=tfplan
          terraform -chdir=terraform/main show -no-color tfplan > plan.txt
      
      - name: Upload plan
        uses: actions/upload-artifact@v4
        with:
          name: terraform-plan
          path: |
            terraform/main/tfplan
            plan.txt
          retention-days: 5
  
  terraform-apply:
    name: Terraform Apply
    needs: terraform-plan
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.5.0
      
      - name: Terraform Init
        run: terraform -chdir=terraform/main init
      
      - name: Download plan
        uses: actions/download-artifact@v4
        with:
          name: terraform-plan
          path: terraform/main/
      
      - name: Terraform Apply
        run: terraform -chdir=terraform/main apply -auto-approve tfplan
```

## Common Workflows

### Adding New Infrastructure

1. **Create/modify Terraform files** in `terraform/main/`:

```hcl
# terraform/main/kinesis.tf
resource "aws_kinesis_stream" "events" {
  name             = "${var.project_name}-events-${var.environment}"
  shard_count      = 1
  retention_period = 24
  
  shard_level_metrics = [
    "IncomingBytes",
    "IncomingRecords",
    "OutgoingBytes",
    "OutgoingRecords",
  ]
}

output "kinesis_stream_name" {
  value       = aws_kinesis_stream.events.name
  description = "Name of the Kinesis stream"
}
```

2. **Format Terraform files**:

```bash
terraform fmt -recursive terraform/
```

3. **Validate locally** (optional but recommended):

```bash
terraform -chdir=terraform/main init -backend=false
terraform -chdir=terraform/main validate
```

4. **Create a pull request**:
   - CI workflow runs format check and validation
   - Review the checks before merging

5. **Merge to main**:
   - Deploy workflow runs `terraform plan`
   - Manual approval required in GitHub UI
   - After approval, `terraform apply` executes

### Checking Deployment Status

```bash
# View workflow runs
gh run list --workflow=deploy.yml

# View specific run logs
gh run view <run-id> --log

# Check specific job
gh run view <run-id> --job=<job-id>
```

### Testing Changes Locally

```bash
# Initialize with backend
terraform -chdir=terraform/main init

# Plan changes
terraform -chdir=terraform/main plan

# Apply (be careful in production!)
terraform -chdir=terraform/main apply
```

## Environment Variables and Configuration

### Required GitHub Secrets

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `AWS_ROLE_ARN` | IAM role ARN for GitHub Actions | `arn:aws:iam::123456789012:role/github-actions-role` |

### Terraform Variables

Create **terraform/main/terraform.tfvars**:

```hcl
aws_region   = "us-east-1"
project_name = "my-data-platform"
environment  = "production"

# Additional configuration
enable_monitoring = true
data_retention_days = 90
```

### Using Environment-Specific Configurations

**terraform/main/environments/dev.tfvars**:

```hcl
environment  = "dev"
project_name = "my-data-platform"
aws_region   = "us-east-1"

# Dev-specific settings
enable_monitoring   = false
data_retention_days = 7
```

**terraform/main/environments/prod.tfvars**:

```hcl
environment  = "production"
project_name = "my-data-platform"
aws_region   = "us-east-1"

enable_monitoring   = true
data_retention_days = 90
```

Modify workflow to use environment-specific variables:

```yaml
- name: Terraform Plan
  run: |
    terraform -chdir=terraform/main plan \
      -var-file=environments/${{ github.event.inputs.environment }}.tfvars \
      -out=tfplan
```

## Advanced Patterns

### Matrix Deployments for Multiple Environments

```yaml
jobs:
  terraform-plan:
    strategy:
      matrix:
        environment: [dev, staging, production]
    name: Plan - ${{ matrix.environment }}
    runs-on: ubuntu-latest
    environment: ${{ matrix.environment }}
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets[format('AWS_ROLE_ARN_{0}', matrix.environment)] }}
          aws-region: us-east-1
      
      - uses: hashicorp/setup-terraform@v3
      
      - name: Terraform Plan
        run: |
          terraform -chdir=terraform/main plan \
            -var-file=environments/${{ matrix.environment }}.tfvars \
            -out=tfplan-${{ matrix.environment }}
```

### Drift Detection Scheduled Job

**.github/workflows/drift-detection.yml**:

```yaml
name: Terraform Drift Detection

on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM UTC
  workflow_dispatch:

permissions:
  id-token: write
  contents: read
  issues: write

jobs:
  detect-drift:
    name: Detect Infrastructure Drift
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1
      
      - uses: hashicorp/setup-terraform@v3
      
      - name: Terraform Init
        run: terraform -chdir=terraform/main init
      
      - name: Terraform Plan
        id: plan
        run: |
          terraform -chdir=terraform/main plan -detailed-exitcode -no-color > plan.txt
        continue-on-error: true
      
      - name: Create Issue on Drift
        if: steps.plan.outputs.exitcode == 2
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const plan = fs.readFileSync('plan.txt', 'utf8');
            
            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '⚠️ Infrastructure Drift Detected',
              body: `Drift detected in Terraform state.\n\n\`\`\`\n${plan}\n\`\`\``,
              labels: ['drift', 'infrastructure']
            });
```

### Cost Estimation with Infracost

Add to **.github/workflows/ci.yml**:

```yaml
- name: Setup Infracost
  uses: infracost/actions/setup@v2
  with:
    api-key: ${{ secrets.INFRACOST_API_KEY }}

- name: Generate cost estimate
  run: |
    infracost breakdown \
      --path=terraform/main \
      --format=json \
      --out-file=/tmp/infracost.json

- name: Post cost comment
  run: |
    infracost comment github \
      --path=/tmp/infracost.json \
      --repo=$GITHUB_REPOSITORY \
      --github-token=${{ secrets.GITHUB_TOKEN }} \
      --pull-request=${{ github.event.pull_request.number }}
```

## Troubleshooting

### "Error: configuring Terraform AWS Provider: failed to get shared config profile"

**Solution**: Ensure AWS credentials are properly configured in GitHub Actions:

```yaml
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
    aws-region: us-east-1
```

### "Error: Error acquiring the state lock"

**Cause**: Another Terraform operation is running or a previous operation failed to release the lock.

**Solution**:

```bash
# Force unlock (use with caution)
terraform -chdir=terraform/main force-unlock <LOCK_ID>
```

### "Error: InvalidClientTokenId: The security token included in the request is invalid"

**Cause**: OIDC provider not configured correctly or role ARN is incorrect.

**Solution**:
1. Verify the `AWS_ROLE_ARN` secret matches bootstrap output
2. Check OIDC provider trust policy includes your repository
3. Ensure GitHub Actions has `id-token: write` permission

### Format Check Failing

**Error**: Terraform files not properly formatted.

**Solution**:

```bash
# Fix formatting locally
terraform fmt -recursive terraform/

# Check what would change
terraform fmt -check -recursive terraform/

# Commit and push
git add terraform/
git commit -m "fix: format terraform files"
git push
```

### State Backend Not Found

**Error**: "Error: Failed to get existing workspaces: S3 bucket does not exist"

**Cause**: Backend configuration references a bucket that doesn't exist.

**Solution**:
1. Verify bootstrap was applied: `terraform -chdir=terraform/bootstrap output`
2. Update backend configuration in `terraform/main/main.tf` with correct bucket name
3. Re-run `terraform init`

### Manual Approval Not Showing

**Cause**: Production environment not configured or reviewers not set.

**Solution**:
1. Go to `Settings → Environments → production`
2. Enable "Required reviewers"
3. Add at least one reviewer
4. Re-run the workflow

## Cleanup

Destroy all resources:

```bash
# Run the teardown script
./tear-down.sh

# Or manually
terraform -chdir=terraform/main destroy
terraform -chdir=terraform/bootstrap destroy
```

**tear-down.sh** example:

```bash
#!/bin/bash
set -e

echo "Destroying main infrastructure..."
terraform -chdir=terraform/main destroy -auto-approve

echo "Destroying bootstrap resources..."
terraform -chdir=terraform/bootstrap destroy -auto-approve

echo "Cleanup complete!"
```

## Best Practices

1. **Always run `terraform fmt`** before committing
2. **Use meaningful commit messages** that describe infrastructure changes
3. **Review plans carefully** before approving deployments
4. **Enable branch protection** on main branch
5. **Use separate AWS accounts** for dev/staging/production
6. **Monitor state file changes** for unauthorized modifications
7. **Implement drift detection** to catch manual changes
8. **Version your Terraform providers** to ensure consistency
9. **Use workspaces or separate backends** for different environments
10. **Document custom modules** and complex configurations
