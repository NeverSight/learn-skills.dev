---
name: terraform-iac-data-engineering
description: Infrastructure-as-Code with Terraform for data engineering on AWS (S3, EC2, IAM)
triggers:
  - "set up terraform for data engineering"
  - "create AWS infrastructure with terraform"
  - "provision S3 and EC2 with IaC"
  - "terraform data engineering setup"
  - "manage AWS resources with terraform"
  - "infrastructure as code for data pipelines"
  - "deploy data infrastructure on AWS"
  - "terraform state management for data engineering"
---

# Terraform IaC for Data Engineering

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project provides Infrastructure-as-Code (IaC) patterns using Terraform specifically for data engineering workloads on AWS. It demonstrates how to provision and manage AWS resources (S3, EC2, IAM) needed for data pipelines and processing.

## What This Project Does

- Provisions AWS S3 buckets for data storage
- Creates EC2 instances for data processing workloads
- Manages IAM users, roles, and policies
- Demonstrates Terraform state management
- Provides reusable IaC patterns for data engineering infrastructure

## Installation

### Prerequisites

1. **Terraform CLI**
   ```bash
   # macOS
   brew install terraform
   
   # Linux
   wget https://releases.hashicorp.com/terraform/1.5.0/terraform_1.5.0_linux_amd64.zip
   unzip terraform_1.5.0_linux_amd64.zip
   sudo mv terraform /usr/local/bin/
   ```

2. **AWS CLI**
   ```bash
   # macOS
   brew install awscli
   
   # Linux
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   ```

3. **Configure AWS CLI**
   ```bash
   aws configure
   # Enter your AWS Access Key ID
   # Enter your AWS Secret Access Key
   # Default region: us-east-1
   # Default output format: json
   ```

### Project Setup

```bash
git clone https://github.com/josephmachado/iac-for-data-engineering-terraform-.git
cd iac-for-data-engineering-terraform-
```

## Key Terraform Commands

### Initialize Terraform

```bash
# Initialize terraform (downloads providers, sets up backend)
terraform -chdir=terraform init

# Validate configuration files
terraform -chdir=terraform validate

# Format configuration files
terraform -chdir=terraform fmt
```

### Plan and Apply Infrastructure

```bash
# Preview changes before applying
terraform -chdir=terraform plan

# Apply infrastructure changes
terraform -chdir=terraform apply

# Auto-approve without confirmation (use with caution)
terraform -chdir=terraform apply -auto-approve
```

### Inspect Infrastructure

```bash
# List all resources in state
terraform -chdir=terraform state list

# Show details of a specific resource
terraform -chdir=terraform state show aws_s3_bucket.data_bucket

# Output specific values
terraform -chdir=terraform output

# Show current state in JSON
terraform -chdir=terraform show -json
```

### Destroy Infrastructure

```bash
# Destroy all managed infrastructure
terraform -chdir=terraform destroy

# Destroy specific resource
terraform -chdir=terraform destroy -target=aws_instance.data_processor
```

## Configuration Structure

### Basic Terraform Configuration for Data Engineering

**main.tf** - Core infrastructure definition:

```hcl
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

# S3 bucket for data storage
resource "aws_s3_bucket" "data_lake" {
  bucket = "my-unique-data-lake-bucket-${var.environment}"
  
  tags = {
    Name        = "Data Lake Bucket"
    Environment = var.environment
    Project     = "DataEngineering"
  }
}

# Enable versioning for data protection
resource "aws_s3_bucket_versioning" "data_lake_versioning" {
  bucket = aws_s3_bucket.data_lake.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

# Block public access
resource "aws_s3_bucket_public_access_block" "data_lake_public_access" {
  bucket = aws_s3_bucket.data_lake.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# EC2 instance for data processing
resource "aws_instance" "data_processor" {
  ami           = var.ec2_ami
  instance_type = var.ec2_instance_type
  
  tags = {
    Name        = "DataProcessor"
    Environment = var.environment
  }
  
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y python3 python3-pip
              pip3 install pandas boto3
              EOF
}

# IAM role for EC2 to access S3
resource "aws_iam_role" "ec2_s3_access_role" {
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

# IAM policy for S3 access
resource "aws_iam_role_policy" "ec2_s3_policy" {
  name = "ec2-s3-policy"
  role = aws_iam_role.ec2_s3_access_role.id
  
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

# Attach IAM role to EC2 instance
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2-s3-profile"
  role = aws_iam_role.ec2_s3_access_role.name
}
```

**variables.tf** - Input variables:

```hcl
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "ec2_ami" {
  description = "AMI ID for EC2 instance"
  type        = string
  default     = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2
}

variable "ec2_instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "bucket_prefix" {
  description = "Prefix for S3 bucket names"
  type        = string
  default     = "data-eng"
}
```

**outputs.tf** - Output values:

```hcl
output "s3_bucket_name" {
  description = "Name of the S3 data lake bucket"
  value       = aws_s3_bucket.data_lake.id
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.data_lake.arn
}

output "ec2_instance_id" {
  description = "ID of the EC2 data processor"
  value       = aws_instance.data_processor.id
}

output "ec2_public_ip" {
  description = "Public IP of EC2 instance"
  value       = aws_instance.data_processor.public_ip
}
```

**terraform.tfvars** - Variable values (gitignore this file):

```hcl
aws_region         = "us-west-2"
environment        = "production"
ec2_instance_type  = "t3.medium"
bucket_prefix      = "my-company-data"
```

## Common Data Engineering Patterns

### Multi-Environment Setup

**environments/dev/main.tf**:

```hcl
module "data_infrastructure" {
  source = "../../modules/data-infra"
  
  environment       = "dev"
  instance_type     = "t2.micro"
  enable_monitoring = false
}
```

**environments/prod/main.tf**:

```hcl
module "data_infrastructure" {
  source = "../../modules/data-infra"
  
  environment       = "prod"
  instance_type     = "t3.xlarge"
  enable_monitoring = true
  backup_enabled    = true
}
```

### S3 Bucket with Lifecycle Policies

```hcl
resource "aws_s3_bucket" "data_archive" {
  bucket = "data-archive-${var.environment}"
}

resource "aws_s3_bucket_lifecycle_configuration" "data_archive_lifecycle" {
  bucket = aws_s3_bucket.data_archive.id
  
  rule {
    id     = "archive-old-data"
    status = "Enabled"
    
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
    
    expiration {
      days = 365
    }
  }
  
  rule {
    id     = "delete-incomplete-uploads"
    status = "Enabled"
    
    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}
```

### VPC Setup for Data Processing

```hcl
resource "aws_vpc" "data_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "data-engineering-vpc"
  }
}

resource "aws_subnet" "private_subnet" {
  vpc_id            = aws_vpc.data_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"
  
  tags = {
    Name = "private-data-subnet"
  }
}

resource "aws_security_group" "data_processor_sg" {
  name        = "data-processor-sg"
  description = "Security group for data processing instances"
  vpc_id      = aws_vpc.data_vpc.id
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
}
```

### Remote State Configuration

**backend.tf**:

```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket-unique-name"
    key            = "data-engineering/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

Create state backend resources:

```hcl
resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-state-bucket-unique-name"
}

resource "aws_s3_bucket_versioning" "terraform_state_versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  
  versioning_configuration {
    status = "Enabled"
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

## Verification and Testing

### Verify S3 Bucket Creation

```bash
# List all S3 buckets
aws s3 ls

# Check specific bucket
aws s3 ls s3://my-unique-data-lake-bucket-dev/

# Upload test file
echo "test data" > test.txt
aws s3 cp test.txt s3://my-unique-data-lake-bucket-dev/
```

### Verify EC2 Instances

```bash
# List running instances
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].{ID:InstanceId, Name:Tags[?Key==`Name`].Value, Type:InstanceType, State:State.Name, PublicIP:PublicIpAddress}' \
  --output table

# Get specific instance details
aws ec2 describe-instances \
  --instance-ids $(terraform -chdir=terraform output -raw ec2_instance_id)
```

### Verify IAM Roles

```bash
# List IAM roles
aws iam list-roles --query 'Roles[?contains(RoleName, `ec2-s3-access`)].RoleName'

# Get role policy
aws iam get-role-policy \
  --role-name ec2-s3-access-role \
  --policy-name ec2-s3-policy
```

## State Management

### Inspect State

```bash
# View state file (formatted)
cat terraform/terraform.tfstate | jq -r '.resources[] | [.type, .name] | join(",")'

# List resources in state
terraform -chdir=terraform state list

# Show resource details
terraform -chdir=terraform state show aws_s3_bucket.data_lake
```

### Import Existing Resources

```bash
# Import existing S3 bucket
terraform -chdir=terraform import aws_s3_bucket.data_lake my-existing-bucket

# Import existing EC2 instance
terraform -chdir=terraform import aws_instance.data_processor i-1234567890abcdef0
```

### Move Resources in State

```bash
# Rename resource in state
terraform -chdir=terraform state mv aws_s3_bucket.old_name aws_s3_bucket.new_name
```

## Troubleshooting

### Common Issues

**Issue: Bucket name already exists**
```hcl
# Solution: Use unique bucket name with random suffix
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "data_lake" {
  bucket = "data-lake-${var.environment}-${random_id.bucket_suffix.hex}"
}
```

**Issue: AWS credentials not found**
```bash
# Check AWS configuration
aws configure list

# Use environment variables
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}"
export AWS_DEFAULT_REGION="us-east-1"
```

**Issue: State file locked**
```bash
# Force unlock (use with caution)
terraform -chdir=terraform force-unlock <LOCK_ID>
```

**Issue: Resource already exists**
```bash
# Import existing resource
terraform -chdir=terraform import <resource_type>.<resource_name> <resource_id>

# Or remove from state
terraform -chdir=terraform state rm <resource_type>.<resource_name>
```

**Issue: Terraform version mismatch**
```hcl
# Specify required version in terraform block
terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

### Debugging

```bash
# Enable debug logging
export TF_LOG=DEBUG
terraform -chdir=terraform apply

# Log to file
export TF_LOG_PATH=terraform-debug.log
terraform -chdir=terraform apply

# Disable logging
unset TF_LOG
unset TF_LOG_PATH
```

### Validate and Format

```bash
# Validate configuration
terraform -chdir=terraform validate

# Format all files
terraform -chdir=terraform fmt -recursive

# Check formatting without making changes
terraform -chdir=terraform fmt -check
```

## Best Practices

1. **Always use variables** for environment-specific values
2. **Enable S3 versioning** for state files and data buckets
3. **Use remote state** for team collaboration
4. **Tag all resources** with environment, project, and owner
5. **Implement lifecycle policies** for cost optimization
6. **Use modules** for reusable infrastructure patterns
7. **Store secrets in AWS Secrets Manager**, reference via data sources
8. **Run `terraform plan`** before apply
9. **Use workspaces** for multiple environments
10. **Document your infrastructure** with comments and README files
