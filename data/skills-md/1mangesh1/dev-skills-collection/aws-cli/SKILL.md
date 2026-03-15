---
name: aws-cli
description: AWS CLI mastery for S3, EC2, Lambda, IAM, and common service operations. Use when user asks to "upload to S3", "launch EC2", "deploy Lambda", "configure AWS", "AWS profiles", "check AWS resources", or any AWS command-line tasks.
---

# AWS CLI

Essential AWS CLI commands and patterns.

## Configuration

```bash
# Initial setup
aws configure
# Enter: Access Key ID, Secret Access Key, Region, Output format

# Named profiles
aws configure --profile staging
aws configure --profile production

# Use profile
aws s3 ls --profile production
export AWS_PROFILE=production  # Set default

# Check identity
aws sts get-caller-identity

# Config files
# ~/.aws/credentials - Access keys
# ~/.aws/config     - Region, output, role settings
```

### Profile with Role Assumption

```ini
# ~/.aws/config
[profile dev]
region = us-east-1
output = json

[profile prod]
role_arn = arn:aws:iam::123456789:role/AdminRole
source_profile = dev
region = us-east-1
```

## S3

```bash
# List buckets/objects
aws s3 ls
aws s3 ls s3://my-bucket/
aws s3 ls s3://my-bucket/prefix/ --recursive

# Copy files
aws s3 cp file.txt s3://my-bucket/
aws s3 cp s3://my-bucket/file.txt ./
aws s3 cp s3://bucket1/file s3://bucket2/file

# Sync directory
aws s3 sync ./dist s3://my-bucket/
aws s3 sync ./dist s3://my-bucket/ --delete  # Mirror (removes extras)
aws s3 sync s3://my-bucket/ ./local/

# With filters
aws s3 sync . s3://bucket/ --exclude "*.log" --include "*.txt"

# Remove
aws s3 rm s3://my-bucket/file.txt
aws s3 rm s3://my-bucket/ --recursive  # Empty bucket

# Presigned URL (temporary access)
aws s3 presign s3://my-bucket/file.txt --expires-in 3600

# Bucket operations
aws s3 mb s3://new-bucket
aws s3 rb s3://empty-bucket
```

## EC2

```bash
# List instances
aws ec2 describe-instances
aws ec2 describe-instances --filters "Name=tag:Name,Values=web-*"
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name,PublicIpAddress]' --output table

# Start/stop
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
aws ec2 reboot-instances --instance-ids i-1234567890abcdef0

# SSH key pairs
aws ec2 create-key-pair --key-name my-key --query 'KeyMaterial' --output text > my-key.pem
chmod 400 my-key.pem

# Security groups
aws ec2 describe-security-groups
aws ec2 authorize-security-group-ingress \
  --group-id sg-123 \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0
```

## Lambda

```bash
# List functions
aws lambda list-functions

# Invoke function
aws lambda invoke --function-name my-func --payload '{"key":"value"}' output.json

# Deploy (zip)
zip -r function.zip .
aws lambda update-function-code \
  --function-name my-func \
  --zip-file fileb://function.zip

# View logs
aws logs tail /aws/lambda/my-func --follow
aws logs tail /aws/lambda/my-func --since 1h

# Environment variables
aws lambda update-function-configuration \
  --function-name my-func \
  --environment "Variables={KEY=value,DB_HOST=localhost}"
```

## IAM

```bash
# Users
aws iam list-users
aws iam create-user --user-name deploy-bot
aws iam create-access-key --user-name deploy-bot

# Policies
aws iam list-attached-user-policies --user-name alice
aws iam attach-user-policy \
  --user-name deploy-bot \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Roles
aws iam list-roles
aws iam get-role --role-name my-role
```

## CloudWatch

```bash
# View log groups
aws logs describe-log-groups

# Tail logs
aws logs tail /ecs/my-service --follow --since 30m

# Filter logs
aws logs filter-log-events \
  --log-group-name /ecs/my-service \
  --filter-pattern "ERROR"
```

## ECS

```bash
# List clusters/services
aws ecs list-clusters
aws ecs list-services --cluster my-cluster
aws ecs describe-services --cluster my-cluster --services my-service

# Force new deployment
aws ecs update-service --cluster my-cluster --service my-service --force-new-deployment

# View tasks
aws ecs list-tasks --cluster my-cluster --service my-service
aws ecs describe-tasks --cluster my-cluster --tasks <task-arn>

# Exec into container
aws ecs execute-command --cluster my-cluster --task <task-id> --container my-app --interactive --command "/bin/sh"
```

## Useful Flags

```bash
# Output formats
--output json     # Default
--output table    # Human-readable
--output text     # Tab-separated
--output yaml

# Query (JMESPath)
--query 'Reservations[].Instances[].InstanceId'
--query 'length(Reservations[])'

# Dry run
--dry-run

# Region override
--region us-west-2

# Wait for state
aws ec2 wait instance-running --instance-ids i-123
aws ecs wait services-stable --cluster my-cluster --services my-service
```

## Reference

For S3 patterns: `references/s3.md`
For EC2 management: `references/ec2.md`
For Lambda functions: `references/lambda.md`
