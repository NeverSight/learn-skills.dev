---
name: iac-terraform-data-engineering
description: Infrastructure-as-Code fundamentals for data engineers using Terraform to provision AWS resources (S3, EC2, IAM)
triggers:
  - "set up terraform for data engineering"
  - "create AWS infrastructure with terraform"
  - "provision S3 and EC2 using IaC"
  - "terraform for data pipelines"
  - "manage data infrastructure as code"
  - "deploy data engineering resources on AWS"
  - "terraform state management for data platforms"
  - "destroy terraform data infrastructure"
---

# IaC for Data Engineering with Terraform

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project provides Infrastructure-as-Code (IaC) templates and patterns for data engineers using Terraform to provision and manage AWS resources. It focuses on creating reproducible, version-controlled infrastructure for data platforms including S3 storage, EC2 compute instances, and IAM permissions.

## What This Project Does

- Provides Terraform configurations for common data engineering infrastructure on AWS
- Demonstrates IaC best practices for S3 buckets, EC2 instances, and IAM roles
- Shows state management and lifecycle operations for data infrastructure
- Teaches reproducible infrastructure provisioning for data pipelines

## Prerequisites

Before using this project, ensure you have:

1. **AWS Account** with root or admin access
2. **Terraform CLI** installed ([installation guide](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli))
3. **AWS CLI** installed and configured ([setup guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))
4. **AWS Credentials** configured via `aws configure`

## AWS IAM Setup

Create an IAM user with appropriate permissions:

1. **Create IAM User**: Navigate to AWS Console → IAM → Users → Create user
2. **Create Inline Policy**: Attach a custom policy to the user
3. **Grant Permissions**: For development/learning, grant full access to:
   - Amazon S3
   - Amazon EC2
   - AWS IAM

**⚠️ Security Note**: Full service access is NOT recommended for production. Use least-privilege policies in production environments.

## Project Structure

```
terraform/
├── main.tf           # Main Terraform configuration
├── variables.tf      # Input variables (if present)
├── outputs.tf        # Output values (if present)
└── terraform.tfstate # State file (generated)
```

## Key Terraform Commands

### Initialize Terraform

Initialize the working directory and download provider plugins:

```bash
terraform -chdir=terraform init
```

### Validate Configuration

Check if the configuration is syntactically valid:

```bash
terraform -chdir=terraform validate
```

### Format Code

Automatically format Terraform files to canonical style:

```bash
terraform -chdir=terraform fmt
```

### Plan Infrastructure Changes

Preview what Terraform will create/modify/destroy:

```bash
terraform -chdir=terraform plan
```

### Apply Configuration

Create or update infrastructure:

```bash
terraform -chdir=terraform apply
```

Terraform will show a plan and ask for confirmation. Type `yes` to proceed.

### Auto-approve (for automation)

```bash
terraform -chdir=terraform apply -auto-approve
```

### Destroy Infrastructure

Remove all resources managed by Terraform:

```bash
terraform -chdir=terraform destroy
```

## Configuration

### Basic Terraform Configuration Example

Before applying, modify `terraform/main.tf` to customize resource names:

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
  region = "us-east-1"
}

# S3 bucket for data storage
resource "aws_s3_bucket" "data_bucket" {
  bucket = "my-unique-data-engineering-bucket-12345"
  
  tags = {
    Name        = "Data Engineering Bucket"
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}

# EC2 instance for data processing
resource "aws_instance" "data_processor" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2
  instance_type = "t2.micro"
  
  tags = {
    Name        = "Data Processor"
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}

# IAM role for EC2 instance
resource "aws_iam_role" "ec2_s3_role" {
  name = "ec2-s3-access-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}
```

### Variables Configuration

Create `terraform/variables.tf` for reusable configurations:

```hcl
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

variable "bucket_name" {
  description = "S3 bucket name for data storage"
  type        = string
  # Set via terraform.tfvars or -var flag
}
```

Use variables in `main.tf`:

```hcl
provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "data_bucket" {
  bucket = var.bucket_name
  
  tags = {
    Environment = var.environment
  }
}
```

Create `terraform/terraform.tfvars`:

```hcl
bucket_name  = "my-unique-bucket-name-2026"
aws_region   = "us-west-2"
environment  = "production"
```

## State Management

### Inspect State

List all resources in the state:

```bash
terraform -chdir=terraform state list
```

View detailed state information:

```bash
cat terraform/terraform.tfstate | jq -r '.resources[] | [.type, .name] | join(",")'
```

### Remote State (Production Pattern)

For production, store state remotely in S3:

```hcl
# terraform/backend.tf
terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "data-platform/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

Initialize with backend configuration:

```bash
terraform -chdir=terraform init -backend-config="bucket=${TERRAFORM_STATE_BUCKET}"
```

## Verification Commands

### Verify S3 Bucket Creation

```bash
aws s3 ls
```

### Verify EC2 Instance

```bash
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].{ID:InstanceId, Name:Tags[?Key==`Name`].Value, Type:InstanceType, State:State.Name, PublicIP:PublicIpAddress, PrivateIP:PrivateIpAddress}' \
  --output table
```

### Check Specific Resource

```bash
terraform -chdir=terraform show aws_s3_bucket.data_bucket
```

## Common Patterns for Data Engineering

### Pattern 1: Data Lake with Multiple Buckets

```hcl
# Raw data bucket
resource "aws_s3_bucket" "raw_data" {
  bucket = "my-data-lake-raw-${var.environment}"
}

# Processed data bucket
resource "aws_s3_bucket" "processed_data" {
  bucket = "my-data-lake-processed-${var.environment}"
}

# Enable versioning for data lineage
resource "aws_s3_bucket_versioning" "raw_data_versioning" {
  bucket = aws_s3_bucket.raw_data.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

# Lifecycle rules for cost optimization
resource "aws_s3_bucket_lifecycle_configuration" "raw_data_lifecycle" {
  bucket = aws_s3_bucket.raw_data.id
  
  rule {
    id     = "archive-old-data"
    status = "Enabled"
    
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
  }
}
```

### Pattern 2: EC2 with Data Processing Tools

```hcl
# Security group for data processor
resource "aws_security_group" "data_processor_sg" {
  name        = "data-processor-sg"
  description = "Security group for data processing instances"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Restrict in production
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 instance with user data for setup
resource "aws_instance" "data_processor" {
  ami           = var.ami_id
  instance_type = "t3.medium"
  
  vpc_security_group_ids = [aws_security_group.data_processor_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
  
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y python3 python3-pip
              pip3 install pandas boto3
              EOF
  
  tags = {
    Name = "Data Processor Instance"
  }
}

# IAM instance profile
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2-data-processor-profile"
  role = aws_iam_role.ec2_s3_role.name
}
```

### Pattern 3: Outputs for Integration

```hcl
# terraform/outputs.tf
output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.data_bucket.id
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.data_bucket.arn
}

output "ec2_instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.data_processor.id
}

output "ec2_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.data_processor.public_ip
}
```

Access outputs:

```bash
terraform -chdir=terraform output
terraform -chdir=terraform output -json | jq -r '.s3_bucket_name.value'
```

## Troubleshooting

### Issue: "Error acquiring the state lock"

**Cause**: Another Terraform process is running or a previous run didn't release the lock.

**Solution**:
```bash
# Force unlock (use with caution)
terraform -chdir=terraform force-unlock <LOCK_ID>
```

### Issue: "bucket name already exists"

**Cause**: S3 bucket names must be globally unique across all AWS accounts.

**Solution**: Change the bucket name in `main.tf` to something unique:
```hcl
resource "aws_s3_bucket" "data_bucket" {
  bucket = "my-unique-name-${random_id.bucket_suffix.hex}"
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}
```

### Issue: "insufficient IAM permissions"

**Cause**: The IAM user doesn't have required permissions.

**Solution**: Verify IAM policy includes necessary actions:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*",
        "ec2:*",
        "iam:*"
      ],
      "Resource": "*"
    }
  ]
}
```

### Issue: State file out of sync

**Cause**: Manual changes made outside Terraform.

**Solution**: Refresh the state:
```bash
terraform -chdir=terraform refresh
```

Or import existing resources:
```bash
terraform -chdir=terraform import aws_s3_bucket.data_bucket my-existing-bucket
```

## Workflow Example

Complete workflow for setting up data infrastructure:

```bash
# 1. Configure AWS credentials
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}"
export AWS_DEFAULT_REGION="us-east-1"

# 2. Customize configuration
cd terraform
# Edit main.tf to set unique bucket name

# 3. Initialize Terraform
terraform init

# 4. Validate configuration
terraform validate

# 5. Format code
terraform fmt

# 6. Preview changes
terraform plan

# 7. Apply configuration
terraform apply

# 8. Verify resources
aws s3 ls
aws ec2 describe-instances --output table

# 9. When done, clean up
terraform destroy
```

## Best Practices for Data Engineering IaC

1. **Use variables** for environment-specific values
2. **Enable S3 versioning** for data lineage and recovery
3. **Tag all resources** for cost tracking and management
4. **Store state remotely** in S3 with encryption and locking
5. **Use modules** to organize reusable infrastructure components
6. **Never commit** `.tfstate` files or AWS credentials to version control
7. **Implement lifecycle rules** on S3 for cost optimization
8. **Use IAM roles** instead of access keys for EC2 instances
9. **Plan before apply** to review changes
10. **Destroy unused resources** to avoid unnecessary costs
