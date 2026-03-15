---
name: terraform
description: Terraform infrastructure as code for provisioning, modules, state management, and workspaces. Use when user asks to "create infrastructure", "write Terraform", "manage state", "create module", "import resource", "plan changes", or any IaC tasks.
---

# Terraform

Infrastructure as Code with Terraform.

## Core Workflow

```bash
# Initialize (download providers)
terraform init

# Preview changes
terraform plan
terraform plan -out=tfplan          # Save plan

# Apply changes
terraform apply
terraform apply tfplan              # Apply saved plan
terraform apply -auto-approve       # Skip confirmation

# Destroy resources
terraform destroy
terraform destroy -target=aws_instance.web

# Format code
terraform fmt
terraform fmt -recursive

# Validate configuration
terraform validate

# Show current state
terraform show
terraform state list
terraform state show aws_instance.web
```

## Basic Configuration

```hcl
# main.tf
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.region
}
```

## Variables

```hcl
# variables.tf
variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default = {
    Environment = "dev"
    ManagedBy   = "terraform"
  }
}

variable "allowed_cidrs" {
  description = "Allowed CIDR blocks"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
```

```bash
# Pass variables
terraform plan -var="region=us-west-2"
terraform plan -var-file="production.tfvars"

# Auto-loaded files: terraform.tfvars, *.auto.tfvars
```

## Outputs

```hcl
# outputs.tf
output "instance_ip" {
  description = "Public IP of the instance"
  value       = aws_instance.web.public_ip
}

output "bucket_arn" {
  description = "S3 bucket ARN"
  value       = aws_s3_bucket.main.arn
  sensitive   = true
}
```

```bash
terraform output
terraform output instance_ip
terraform output -json
```

## Resources

```hcl
# EC2 Instance
resource "aws_instance" "web" {
  ami           = "ami-0abcdef1234567890"
  instance_type = var.instance_type

  tags = merge(var.tags, {
    Name = "web-server"
  })

  lifecycle {
    create_before_destroy = true
    prevent_destroy       = true
    ignore_changes        = [tags["UpdatedAt"]]
  }
}

# S3 Bucket
resource "aws_s3_bucket" "main" {
  bucket = "my-app-${var.environment}"
}

# Security Group
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Web server security group"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidrs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## Data Sources

```hcl
# Look up existing resources
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*-amd64-server-*"]
  }
}

data "aws_vpc" "default" {
  default = true
}

# Use in resource
resource "aws_instance" "web" {
  ami = data.aws_ami.ubuntu.id
}
```

## Modules

```hcl
# Using module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
}

# Local module
module "web_server" {
  source = "./modules/web-server"

  instance_type = "t3.small"
  subnet_id     = module.vpc.public_subnets[0]
}
```

## State Management

```bash
# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0

# Move resource in state
terraform state mv aws_instance.old aws_instance.new

# Remove from state (without destroying)
terraform state rm aws_instance.web

# Pull remote state
terraform state pull > state.json

# Replace provider
terraform state replace-provider hashicorp/aws registry.terraform.io/hashicorp/aws
```

## Workspaces

```bash
# List workspaces
terraform workspace list

# Create/switch workspace
terraform workspace new staging
terraform workspace select production

# Use in config
resource "aws_instance" "web" {
  instance_type = terraform.workspace == "production" ? "t3.large" : "t3.micro"
}
```

## Common Patterns

```hcl
# Conditional resource
resource "aws_instance" "bastion" {
  count = var.enable_bastion ? 1 : 0
  # ...
}

# For each
resource "aws_iam_user" "users" {
  for_each = toset(var.user_names)
  name     = each.value
}

# Dynamic blocks
resource "aws_security_group" "main" {
  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = "tcp"
      cidr_blocks = ingress.value.cidrs
    }
  }
}

# Local values
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}
```

## Reference

For module patterns, workspaces, and backends: `references/patterns.md`
