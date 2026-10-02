---
name: terraform-data-engineering-iac
description: Infrastructure-as-Code fundamentals for data engineering using Terraform to provision AWS resources (S3, EC2, IAM)
triggers:
  - "set up data engineering infrastructure with terraform"
  - "provision AWS resources for data pipelines"
  - "create S3 buckets and EC2 instances with IaC"
  - "terraform infrastructure for data engineering"
  - "manage data infrastructure as code"
  - "deploy AWS data engineering stack with terraform"
  - "automate data platform provisioning"
  - "terraform state management for data pipelines"
---

# Terraform Data Engineering IaC

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project demonstrates Infrastructure-as-Code (IaC) fundamentals for data engineering using Terraform. It provisions AWS resources commonly used in data pipelines including S3 buckets for data storage and EC2 instances for data processing workloads.

## What It Does

- **Provisions AWS S3 buckets** for data lake storage
- **Creates EC2 instances** for data processing and pipeline execution
- **Manages IAM policies** for secure resource access
- **Uses Terraform state** to track and manage infrastructure changes
- **Provides reproducible infrastructure** for data engineering environments

## Prerequisites

Before using this project, ensure you have:

1. AWS Account with appropriate permissions
2. Terraform CLI installed
3. AWS CLI installed and configured
4. IAM user with S3, EC2, and IAM permissions

## Installation

### 1. Install Terraform

```bash
# macOS
brew install terraform

# Linux
wget https://releases.hashicorp.com/terraform/1.5.0/terraform_1.5.0_linux_amd64.zip
unzip terraform_1.5.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verify installation
terraform version
```

### 2. Install AWS CLI

```bash
# macOS
brew install awscli

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS credentials
aws configure
```

### 3. Set Up IAM Permissions

Create an IAM user with the following managed policies:
- `AmazonS3FullAccess`
- `AmazonEC2FullAccess`
- `IAMFullAccess`

**Note:** For production, use fine-grained permissions instead of full access.

## Project Structure

```
terraform/
├── main.tf           # Main infrastructure definitions
├── variables.tf      # Input variables
├── outputs.tf        # Output values
└── terraform.tfstate # State file (generated)
```

## Key Terraform Commands

### Initialize Terraform

```bash
# Initialize backend and download providers
terraform -chdir=terraform init
```

### Validate Configuration

```bash
# Check syntax and validate configuration
terraform -chdir=terraform validate
```

### Format Code

```bash
# Auto-format HCL files
terraform -chdir=terraform fmt
```

### Plan Infrastructure Changes

```bash
# Preview what will be created/changed
terraform -chdir=terraform plan
```

### Apply Infrastructure

```bash
# Create or update infrastructure
terraform -chdir=terraform apply

# Auto-approve without confirmation (use carefully)
terraform -chdir=terraform apply -auto-approve
```

### Destroy Infrastructure

```bash
# Remove all managed infrastructure
terraform -chdir=terraform destroy

# Auto-approve destruction (use carefully)
terraform -chdir=terraform destroy -auto-approve
```

### State Management

```bash
# List all resources in state
terraform -chdir=terraform state list

# Show detailed resource information
terraform -chdir=terraform state show aws_s3_bucket.data_bucket

# View state as JSON
cat terraform/terraform.tfstate | jq -r '.resources[] | [.type, .name] | join(",")'
```

## Configuration Examples

### Basic S3 Bucket for Data Storage

```hcl
# terraform/main.tf
terraform {
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

resource "aws_s3_bucket" "data_lake" {
  bucket = "my-unique-data-lake-bucket-${var.environment}"
  
  tags = {
    Name        = "Data Lake Bucket"
    Environment = var.environment
    Project     = "data-engineering"
  }
}

resource "aws_s3_bucket_versioning" "data_lake_versioning" {
  bucket = aws_s3_bucket.data_lake.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "data_lake_lifecycle" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    id     = "archive_old_data"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}
```

### EC2 Instance for Data Processing

```hcl
# terraform/main.tf (continued)
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_instance" "data_processor" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  tags = {
    Name        = "Data Processing Server"
    Environment = var.environment
  }

  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update
              sudo apt-get install -y python3-pip
              pip3 install pandas boto3 apache-airflow
              EOF
}

resource "aws_eip" "data_processor_eip" {
  instance = aws_instance.data_processor.id
  domain   = "vpc"
}
```

### Variables Configuration

```hcl
# terraform/variables.tf
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}
```

### Outputs Configuration

```hcl
# terraform/outputs.tf
output "s3_bucket_name" {
  description = "Name of the S3 data lake bucket"
  value       = aws_s3_bucket.data_lake.id
}

output "ec2_public_ip" {
  description = "Public IP of data processing EC2 instance"
  value       = aws_eip.data_processor_eip.public_ip
}

output "ec2_instance_id" {
  description = "Instance ID of data processor"
  value       = aws_instance.data_processor.id
}
```

## Common Patterns

### Multi-Environment Setup

```hcl
# Use workspace or separate state files
terraform workspace new staging
terraform workspace new production

# Or use variable files
terraform apply -var-file="environments/dev.tfvars"
terraform apply -var-file="environments/prod.tfvars"
```

### Remote State with S3 Backend

```hcl
# terraform/backend.tf
terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "data-engineering/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### IAM Role for EC2 with S3 Access

```hcl
resource "aws_iam_role" "data_processor_role" {
  name = "data-processor-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "s3_access" {
  role       = aws_iam_role.data_processor_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_instance_profile" "data_processor_profile" {
  name = "data-processor-profile"
  role = aws_iam_role.data_processor_role.name
}

resource "aws_instance" "data_processor" {
  ami                  = data.aws_ami.ubuntu.id
  instance_type        = var.instance_type
  iam_instance_profile = aws_iam_instance_profile.data_processor_profile.name
}
```

## Verification Commands

### Verify S3 Buckets

```bash
# List all S3 buckets
aws s3 ls

# Get bucket details
aws s3api get-bucket-location --bucket my-data-lake-bucket

# List bucket contents
aws s3 ls s3://my-data-lake-bucket/
```

### Verify EC2 Instances

```bash
# List running instances
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].{ID:InstanceId, Name:Tags[?Key==`Name`].Value, Type:InstanceType, State:State.Name, PublicIP:PublicIpAddress, PrivateIP:PrivateIpAddress}' \
  --output table

# Get specific instance details
aws ec2 describe-instances --instance-ids i-1234567890abcdef0
```

### Connect to EC2 Instance

```bash
# SSH into instance (requires key pair)
ssh -i ~/.ssh/my-key.pem ubuntu@$(terraform -chdir=terraform output -raw ec2_public_ip)
```

## Troubleshooting

### Issue: Terraform Init Fails

```bash
# Clear cache and reinitialize
rm -rf terraform/.terraform
rm terraform/.terraform.lock.hcl
terraform -chdir=terraform init
```

### Issue: State Lock Error

```bash
# Force unlock (use with caution)
terraform -chdir=terraform force-unlock LOCK_ID
```

### Issue: AWS Credentials Not Found

```bash
# Verify AWS configuration
aws configure list
aws sts get-caller-identity

# Set credentials explicitly
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}"
export AWS_DEFAULT_REGION="us-east-1"
```

### Issue: Resource Already Exists

```bash
# Import existing resource into state
terraform -chdir=terraform import aws_s3_bucket.data_lake my-existing-bucket

# Or recreate with unique name
terraform -chdir=terraform apply -var="bucket_suffix=$(date +%s)"
```

### Issue: Permission Denied

Check IAM policies and ensure your user has required permissions:

```bash
# Test S3 permissions
aws s3 ls

# Test EC2 permissions
aws ec2 describe-instances

# Test IAM permissions
aws iam list-users
```

### Debugging Terraform

```bash
# Enable debug logging
export TF_LOG=DEBUG
terraform -chdir=terraform apply

# Show detailed plan
terraform -chdir=terraform plan -out=tfplan
terraform -chdir=terraform show tfplan

# Refresh state from actual infrastructure
terraform -chdir=terraform refresh
```

## Best Practices

1. **Always use unique bucket names**: S3 bucket names must be globally unique
2. **Version your state files**: Enable S3 versioning for state file backups
3. **Use remote state**: Store state in S3 with locking via DynamoDB
4. **Tag all resources**: Apply consistent tagging for cost tracking and organization
5. **Use variables**: Parameterize configurations for reusability
6. **Run `terraform plan`** before apply to review changes
7. **Destroy dev resources**: Don't leave test infrastructure running to avoid costs
