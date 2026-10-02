---
name: iac-data-engineering-terraform
description: Infrastructure-as-Code patterns for data engineering with Terraform on AWS (S3, EC2, IAM)
triggers:
  - "set up terraform for data engineering"
  - "create AWS infrastructure with terraform"
  - "manage data engineering infrastructure as code"
  - "terraform for S3 and EC2 setup"
  - "IaC patterns for data pipelines"
  - "deploy data engineering resources on AWS"
  - "terraform state management for data infrastructure"
  - "automate AWS data infrastructure provisioning"
---

# IaC for Data Engineering with Terraform

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project demonstrates Infrastructure-as-Code (IaC) fundamentals for data engineers using Terraform to provision AWS resources including S3 buckets, EC2 instances, and IAM configurations. It provides reusable patterns for managing data infrastructure declaratively.

## What This Project Does

- Provisions AWS S3 buckets for data storage
- Creates and configures EC2 instances for data processing
- Sets up IAM roles and policies with proper permissions
- Manages infrastructure state with Terraform
- Provides reproducible data engineering environments

## Prerequisites

Before using this project, ensure you have:

```bash
# Install Terraform
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Install AWS CLI
brew install awscli

# Configure AWS credentials
aws configure
# Enter your AWS Access Key ID, Secret Access Key, region, and output format
```

Set up required environment variables:

```bash
export AWS_ACCESS_KEY_ID=$YOUR_ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=$YOUR_SECRET_KEY
export AWS_DEFAULT_REGION=us-east-1
```

## Project Structure

```
terraform/
├── main.tf          # Main infrastructure definitions
├── variables.tf     # Input variables
├── outputs.tf       # Output values
└── terraform.tfstate # State file (auto-generated)
```

## Core Terraform Commands

### Initialize Terraform

```bash
# Initialize the working directory and download providers
terraform -chdir=terraform init

# Validate configuration syntax
terraform -chdir=terraform validate

# Format configuration files
terraform -chdir=terraform fmt
```

### Plan and Apply Infrastructure

```bash
# Preview changes without applying
terraform -chdir=terraform plan

# Apply infrastructure changes
terraform -chdir=terraform apply

# Auto-approve without prompts (use carefully)
terraform -chdir=terraform apply -auto-approve
```

### Inspect Infrastructure

```bash
# List all resources in state
terraform -chdir=terraform state list

# Show detailed state information
terraform -chdir=terraform show

# Output specific values
terraform -chdir=terraform output
```

### Destroy Infrastructure

```bash
# Destroy all managed infrastructure
terraform -chdir=terraform destroy

# Destroy specific resource
terraform -chdir=terraform destroy -target=aws_s3_bucket.data_bucket
```

## Key Configuration Patterns

### S3 Bucket for Data Storage

```hcl
# main.tf
resource "aws_s3_bucket" "data_lake" {
  bucket = "my-data-engineering-bucket-${random_id.bucket_suffix.hex}"
  
  tags = {
    Environment = "dev"
    Purpose     = "data-engineering"
    ManagedBy   = "terraform"
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# Enable versioning for data protection
resource "aws_s3_bucket_versioning" "data_lake_versioning" {
  bucket = aws_s3_bucket.data_lake.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

# Configure lifecycle rules
resource "aws_s3_bucket_lifecycle_configuration" "data_lake_lifecycle" {
  bucket = aws_s3_bucket.data_lake.id

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

### EC2 Instance for Data Processing

```hcl
# main.tf
resource "aws_instance" "data_processor" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2
  instance_type = "t3.medium"
  
  key_name = aws_key_pair.data_eng_key.key_name
  
  vpc_security_group_ids = [aws_security_group.data_processor_sg.id]
  
  iam_instance_profile = aws_iam_instance_profile.data_processor_profile.name
  
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y python3 python3-pip
              pip3 install pandas boto3 awscli
              EOF
  
  tags = {
    Name        = "data-processor"
    Environment = "dev"
    ManagedBy   = "terraform"
  }
  
  root_block_device {
    volume_size = 50
    volume_type = "gp3"
  }
}

resource "aws_key_pair" "data_eng_key" {
  key_name   = "data-engineering-key"
  public_key = file("~/.ssh/id_rsa.pub")
}
```

### Security Group Configuration

```hcl
resource "aws_security_group" "data_processor_sg" {
  name        = "data-processor-sg"
  description = "Security group for data processing EC2 instances"
  
  # SSH access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Restrict in production
  }
  
  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "data-processor-sg"
  }
}
```

### IAM Role for EC2 with S3 Access

```hcl
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
}

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
          aws_s3_bucket.data_lake.arn,
          "${aws_s3_bucket.data_lake.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_instance_profile" "data_processor_profile" {
  name = "data-processor-profile"
  role = aws_iam_role.data_processor_role.name
}
```

## Variables and Outputs

### Define Variables

```hcl
# variables.tf
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

variable "bucket_prefix" {
  description = "Prefix for S3 bucket names"
  type        = string
  default     = "data-engineering"
}
```

### Configure Outputs

```hcl
# outputs.tf
output "s3_bucket_name" {
  description = "Name of the created S3 bucket"
  value       = aws_s3_bucket.data_lake.id
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.data_lake.arn
}

output "ec2_instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.data_processor.id
}

output "ec2_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.data_processor.public_ip
}

output "ec2_private_ip" {
  description = "Private IP of the EC2 instance"
  value       = aws_instance.data_processor.private_ip
}
```

## Remote State Management

For team collaboration, use S3 backend for state:

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket-name"
    key            = "data-engineering/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

Create the backend resources:

```hcl
resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-state-bucket-name"
  
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }
}
```

## Verification Commands

After applying infrastructure:

```bash
# Verify S3 buckets
aws s3 ls

# Verify EC2 instances
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].{ID:InstanceId,Name:Tags[?Key==`Name`].Value,Type:InstanceType,State:State.Name,PublicIP:PublicIpAddress,PrivateIP:PrivateIpAddress}' \
  --output table

# Check IAM roles
aws iam list-roles --query 'Roles[?contains(RoleName, `data-processor`)].RoleName'

# Inspect Terraform state
terraform -chdir=terraform state list
cat terraform/terraform.tfstate | jq -r '.resources[] | [.type, .name] | join(",")'
```

## Common Patterns

### Multi-Environment Setup

```hcl
# environments/dev/main.tf
module "data_infrastructure" {
  source = "../../modules/data-infra"
  
  environment   = "dev"
  instance_type = "t3.small"
  bucket_prefix = "dev-data"
}

# environments/prod/main.tf
module "data_infrastructure" {
  source = "../../modules/data-infra"
  
  environment   = "prod"
  instance_type = "t3.large"
  bucket_prefix = "prod-data"
}
```

### Using terraform.tfvars

```hcl
# terraform.tfvars
aws_region    = "us-west-2"
environment   = "staging"
instance_type = "t3.medium"
bucket_prefix = "staging-data-lake"
```

Apply with variables:

```bash
terraform -chdir=terraform apply -var-file="terraform.tfvars"
```

## Troubleshooting

### State Lock Issues

```bash
# Force unlock if state is stuck
terraform -chdir=terraform force-unlock LOCK_ID

# View current state
terraform -chdir=terraform show
```

### S3 Bucket Name Conflicts

If bucket name is taken:

```hcl
# Use random suffix
resource "random_id" "bucket_suffix" {
  byte_length = 8
}

resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.bucket_prefix}-${random_id.bucket_suffix.hex}"
}
```

### Import Existing Resources

```bash
# Import existing S3 bucket
terraform -chdir=terraform import aws_s3_bucket.data_lake existing-bucket-name

# Import EC2 instance
terraform -chdir=terraform import aws_instance.data_processor i-1234567890abcdef0
```

### Debugging Terraform

```bash
# Enable detailed logging
export TF_LOG=DEBUG
terraform -chdir=terraform apply

# Disable logging
unset TF_LOG
```

### Refresh State

```bash
# Sync state with real infrastructure
terraform -chdir=terraform refresh

# Replace corrupted resource
terraform -chdir=terraform apply -replace=aws_instance.data_processor
```

## Best Practices

1. **Always use variables** for environment-specific values
2. **Enable S3 versioning** for data protection
3. **Use IAM roles** instead of access keys for EC2
4. **Tag all resources** for cost tracking and management
5. **Store state remotely** for team collaboration
6. **Use modules** for reusable infrastructure patterns
7. **Run `terraform plan`** before every apply
8. **Never commit** `.tfstate` files or sensitive variables to Git
9. **Use `.gitignore`** for Terraform files:

```gitignore
# .gitignore
.terraform/
*.tfstate
*.tfstate.backup
.terraform.lock.hcl
terraform.tfvars
*.auto.tfvars
```
