---
name: terraform-data-engineering-infrastructure
description: Infrastructure-as-Code patterns for data engineering using Terraform to provision AWS resources (S3, EC2, IAM)
triggers:
  - "set up data engineering infrastructure with terraform"
  - "provision AWS resources for data pipelines"
  - "create infrastructure as code for data engineering"
  - "deploy data engineering infrastructure on AWS"
  - "terraform for data platform setup"
  - "infrastructure as code for analytics workloads"
  - "automate AWS infrastructure for data teams"
  - "manage data engineering resources with terraform"
---

# Terraform Data Engineering Infrastructure

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project provides Infrastructure-as-Code (IaC) patterns for data engineering teams using Terraform to provision and manage AWS resources. It demonstrates how to automate the creation of data infrastructure including S3 buckets for data lakes, EC2 instances for processing, and IAM policies for secure access.

## What This Project Does

- Provisions AWS infrastructure specifically designed for data engineering workloads
- Manages S3 buckets for data storage and data lake architectures
- Creates EC2 instances for data processing and ETL jobs
- Configures IAM roles and policies for secure resource access
- Provides declarative infrastructure definitions that can be version-controlled
- Enables reproducible environment creation across dev/staging/prod

## Prerequisites

Before using this project, ensure you have:

1. An AWS account with root or administrative access
2. Terraform installed (v1.0+)
3. AWS CLI installed and configured
4. IAM user with appropriate permissions (S3, EC2, IAM full access)

### Installing Prerequisites

```bash
# Install Terraform (macOS)
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Install AWS CLI (macOS)
brew install awscli

# Configure AWS CLI
aws configure
# Enter your AWS Access Key ID, Secret Access Key, region, and output format
```

### Setting Up IAM Permissions

Create an IAM user with the following permissions for Terraform:
- Full S3 access (AmazonS3FullAccess)
- Full EC2 access (AmazonEC2FullAccess)
- Full IAM access (IAMFullAccess)

**Note:** This is for development/learning. In production, use least-privilege policies.

```bash
# Create access keys for your IAM user
aws iam create-access-key --user-name your-terraform-user

# Configure AWS CLI with these credentials
aws configure --profile terraform
```

## Project Structure

```
terraform/
├── main.tf           # Main infrastructure definitions
├── variables.tf      # Input variables (if present)
├── outputs.tf        # Output values (if present)
└── terraform.tfstate # State file (generated)
```

## Key Terraform Commands

### Initialize Terraform

```bash
# Initialize the working directory
terraform -chdir=terraform init

# Validate configuration files
terraform -chdir=terraform validate

# Format configuration files
terraform -chdir=terraform fmt
```

### Plan and Apply Infrastructure

```bash
# Preview changes without applying
terraform -chdir=terraform plan

# Apply changes and create infrastructure
terraform -chdir=terraform apply

# Apply without confirmation prompt
terraform -chdir=terraform apply -auto-approve
```

### Inspect Infrastructure

```bash
# List all resources in state
terraform -chdir=terraform state list

# Show details of a specific resource
terraform -chdir=terraform state show aws_s3_bucket.data_bucket

# Output current state
terraform -chdir=terraform show
```

### Destroy Infrastructure

```bash
# Destroy all managed infrastructure
terraform -chdir=terraform destroy

# Destroy specific resources
terraform -chdir=terraform destroy -target=aws_instance.data_processor
```

## Configuration Patterns

### Basic S3 Bucket for Data Lake

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

# S3 bucket for raw data
resource "aws_s3_bucket" "raw_data" {
  bucket = "my-unique-raw-data-bucket-12345"
  
  tags = {
    Environment = "dev"
    Purpose     = "data-lake-raw"
    ManagedBy   = "terraform"
  }
}

# Enable versioning for data recovery
resource "aws_s3_bucket_versioning" "raw_data_versioning" {
  bucket = aws_s3_bucket.raw_data.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

# Block public access
resource "aws_s3_bucket_public_access_block" "raw_data_public_access" {
  bucket = aws_s3_bucket.raw_data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

### EC2 Instance for Data Processing

```hcl
# Security group for EC2 instance
resource "aws_security_group" "data_processor_sg" {
  name        = "data-processor-sg"
  description = "Security group for data processing EC2 instances"

  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Restrict this in production
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name      = "data-processor-sg"
    ManagedBy = "terraform"
  }
}

# EC2 instance for data processing
resource "aws_instance" "data_processor" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI (update for your region)
  instance_type = "t3.medium"
  
  vpc_security_group_ids = [aws_security_group.data_processor_sg.id]
  
  iam_instance_profile = aws_iam_instance_profile.data_processor_profile.name

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y python3 python3-pip
              pip3 install boto3 pandas
              EOF

  tags = {
    Name        = "data-processor"
    Environment = "dev"
    ManagedBy   = "terraform"
  }
}
```

### IAM Role for EC2 to Access S3

```hcl
# IAM role for EC2 instances
resource "aws_iam_role" "data_processor_role" {
  name = "data-processor-role"

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

  tags = {
    ManagedBy = "terraform"
  }
}

# Policy to allow S3 access
resource "aws_iam_role_policy" "s3_access_policy" {
  name = "s3-access-policy"
  role = aws_iam_role.data_processor_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.raw_data.arn,
          "${aws_s3_bucket.raw_data.arn}/*"
        ]
      }
    ]
  })
}

# Instance profile for EC2
resource "aws_iam_instance_profile" "data_processor_profile" {
  name = "data-processor-profile"
  role = aws_iam_role.data_processor_role.name
}
```

### Multi-Environment Setup with Variables

```hcl
# terraform/variables.tf
variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "bucket_prefix" {
  description = "Prefix for S3 bucket names"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

# terraform/main.tf
resource "aws_s3_bucket" "data_bucket" {
  bucket = "${var.bucket_prefix}-${var.environment}-data"
  
  tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}
```

Apply with variables:

```bash
terraform -chdir=terraform apply \
  -var="environment=prod" \
  -var="bucket_prefix=mycompany" \
  -var="instance_type=t3.large"
```

### Output Values for Integration

```hcl
# terraform/outputs.tf
output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.raw_data.id
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.raw_data.arn
}

output "ec2_instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.data_processor.id
}

output "ec2_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.data_processor.public_ip
}

# View outputs
# terraform -chdir=terraform output
```

## Common Workflows

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/josephmachado/iac-for-data-engineering-terraform-.git
cd iac-for-data-engineering-terraform-

# Update bucket name in terraform/main.tf to be globally unique
# Edit terraform/main.tf and change bucket name

# Initialize and apply
terraform -chdir=terraform init
terraform -chdir=terraform validate
terraform -chdir=terraform fmt
terraform -chdir=terraform apply
```

### Verify Resources Created

```bash
# List S3 buckets
aws s3 ls

# Check EC2 instances
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].{ID:InstanceId, Name:Tags[?Key==`Name`].Value, Type:InstanceType, State:State.Name, PublicIP:PublicIpAddress}' \
  --output table

# View Terraform state
terraform -chdir=terraform state list
cat terraform/terraform.tfstate | jq -r '.resources[] | [.type, .name] | join(",")'
```

### Update Infrastructure

```bash
# Edit terraform files
# Then preview changes
terraform -chdir=terraform plan

# Apply changes
terraform -chdir=terraform apply
```

### Clean Up

```bash
# Destroy all resources
terraform -chdir=terraform destroy

# Verify cleanup
aws s3 ls
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"
```

## Advanced Patterns

### Data Lake Structure with Multiple Buckets

```hcl
# Raw data bucket
resource "aws_s3_bucket" "raw" {
  bucket = "${var.bucket_prefix}-raw-${var.environment}"
  tags = {
    Layer = "raw"
  }
}

# Processed data bucket
resource "aws_s3_bucket" "processed" {
  bucket = "${var.bucket_prefix}-processed-${var.environment}"
  tags = {
    Layer = "processed"
  }
}

# Curated data bucket
resource "aws_s3_bucket" "curated" {
  bucket = "${var.bucket_prefix}-curated-${var.environment}"
  tags = {
    Layer = "curated"
  }
}

# Lifecycle policy for raw data
resource "aws_s3_bucket_lifecycle_configuration" "raw_lifecycle" {
  bucket = aws_s3_bucket.raw.id

  rule {
    id     = "archive-old-data"
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

### Remote State Management

```hcl
# Create S3 bucket for state
resource "aws_s3_bucket" "terraform_state" {
  bucket = "my-terraform-state-bucket-12345"
  
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "terraform_state_versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

# Configure backend (in a separate backend.tf file)
# terraform {
#   backend "s3" {
#     bucket = "my-terraform-state-bucket-12345"
#     key    = "data-engineering/terraform.tfstate"
#     region = "us-east-1"
#   }
# }
```

## Troubleshooting

### Bucket Name Already Exists

**Error:** `BucketAlreadyExists: The requested bucket name is not available`

**Solution:** S3 bucket names must be globally unique. Change the bucket name in `main.tf`:

```hcl
resource "aws_s3_bucket" "data_bucket" {
  bucket = "your-unique-prefix-data-bucket-${random_id.bucket_suffix.hex}"
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}
```

### Insufficient IAM Permissions

**Error:** `UnauthorizedOperation` or `AccessDenied`

**Solution:** Verify IAM user has required permissions:

```bash
# Check current user identity
aws sts get-caller-identity

# Verify policies attached to user
aws iam list-attached-user-policies --user-name your-terraform-user
```

### State Lock Issues

**Error:** `Error acquiring the state lock`

**Solution:** 

```bash
# Force unlock (use with caution)
terraform -chdir=terraform force-unlock LOCK_ID

# Or remove local state lock file
rm terraform/.terraform.tfstate.lock.info
```

### Resource Already Exists

**Error:** Resource already exists but not in state

**Solution:** Import existing resource:

```bash
# Import S3 bucket
terraform -chdir=terraform import aws_s3_bucket.data_bucket my-existing-bucket-name

# Import EC2 instance
terraform -chdir=terraform import aws_instance.data_processor i-1234567890abcdef0
```

### Terraform State Drift

**Error:** Resources differ from state

**Solution:**

```bash
# Refresh state to match real infrastructure
terraform -chdir=terraform refresh

# Or during plan/apply
terraform -chdir=terraform apply -refresh=true
```

### Region-Specific AMI Issues

**Error:** Invalid AMI ID for region

**Solution:** Use data source to find correct AMI:

```hcl
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

resource "aws_instance" "data_processor" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.medium"
}
```

## Best Practices

1. **Use Remote State:** Store Terraform state in S3 with versioning enabled
2. **Separate Environments:** Use workspaces or separate state files for dev/staging/prod
3. **Least Privilege IAM:** Use specific IAM policies instead of full access in production
4. **Tag Everything:** Add consistent tags for cost tracking and resource management
5. **Version Control:** Commit `.tf` files but exclude `terraform.tfstate` and `.terraform/`
6. **Plan Before Apply:** Always run `terraform plan` before `apply`
7. **Use Variables:** Parameterize configurations for reusability
8. **Enable Encryption:** Use S3 bucket encryption and EBS encryption for EC2
9. **Implement Lifecycle Policies:** Archive or delete old data automatically
10. **Document Dependencies:** Use comments to explain resource relationships

## Environment Variables

```bash
# AWS credentials (preferred over hardcoding)
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1

# Terraform variables
export TF_VAR_environment=dev
export TF_VAR_bucket_prefix=mycompany
export TF_VAR_instance_type=t3.medium
```
