---
name: aws-limits
description: Reviews infrastructure code for AWS service quota violations. Use when reviewing Terraform, CloudFormation, CDK, Pulumi, or SDK code that provisions AWS resources.
---

# AWS Limits Review

## Goal
Catch AWS service limit/quota violations in infrastructure code before they cause production issues.

## When to use
- Reviewing Terraform, CloudFormation, CDK, or Pulumi code
- Code that provisions or configures AWS resources
- PR reviews involving AWS infrastructure changes
- Before deploying infrastructure changes to production

## When not to use
- Non-AWS cloud providers (future skills: cloudflare-limits, gcp-limits)
- Application code without infrastructure components
- AWS SDK usage for read-only operations

## Inputs
- Infrastructure code files (`.tf`, `.json`, `.yaml`, `.yml`, `.ts`, `.py`)
- Context about expected scale/traffic patterns (if available)

## Outputs
- List of potential limit violations with severity
- Links to official AWS documentation
- Recommended mitigations

## Default workflow

1. **Identify AWS services** in the code:
   - Scan for resource types (e.g., `aws_lambda_function`, `AWS::Lambda::Function`)
   - Note service patterns in SDK calls

2. **Check against known limits** in [REFERENCE.md](./REFERENCE.md):
   - Hard limits (cannot be increased)
   - Soft limits at default values
   - Limits that commonly cause production issues

3. **Flag violations** with context:
   - Quote the specific code
   - Explain the limit and why it matters
   - Link to AWS documentation
   - Suggest mitigation if applicable

4. **Prioritize by severity**:
   - **Critical**: Hard limits that will fail immediately
   - **High**: Default limits likely to be hit at moderate scale
   - **Medium**: Limits that may cause issues at high scale
   - **Low**: Informational, worth noting for awareness

## Key patterns to watch

### Lambda
- Functions with >15 min expected runtime (hard limit: 15 min)
- Synchronous payloads >6MB
- VPC-connected functions without sufficient ENI capacity
- High concurrency without reserved/provisioned concurrency

### API Gateway
- Integrations expecting >29s response time (default timeout)
- Missing throttling configuration for public APIs
- WebSocket connections without connection management

### S3
- Single-prefix designs with high throughput expectations
- Missing retry logic for 503 responses

### DynamoDB
- Items approaching 400KB
- Single-table designs without GSI capacity planning
- On-demand tables without understanding burst limits

### Step Functions
- Long-running workflows approaching 25,000 event limit
- Map states without concurrency limits
- Large payloads (>256KB state data)

### Load Balancing
- Multiple load balancers sharing target groups (limit: 5 LBs per target group)
- Target groups with many targets without health check tuning
- Weighted routing with many target groups per action

### Cognito
- Auth flows without rate limit handling (default: 120 RPS)
- Bulk user imports without throttling

## Validation checklist

- [ ] All identified AWS services checked against REFERENCE.md
- [ ] Hard limits flagged as Critical
- [ ] Soft limits noted with current defaults
- [ ] Links to AWS docs included for each finding
- [ ] Mitigations suggested where applicable

## Output format

```markdown
## AWS Limits Review

### Critical
- **[Service]: [Limit name]**
  - File: `path/to/file.tf:42`
  - Issue: [Description]
  - Limit: [Value] ([hard/soft])
  - Docs: [AWS link]
  - Mitigation: [Suggestion]

### High
...

### Medium
...

### Low / Informational
...

### No Issues Found
- [List of services reviewed with no concerns]
```

## Examples

### Example 1: Lambda timeout
**Input**: Terraform defining Lambda with Step Functions integration
```hcl
resource "aws_lambda_function" "processor" {
  timeout = 900  # 15 minutes
}
```
**Output**:
> **High: Lambda timeout at maximum**
> - File: `lambda.tf:12`
> - Issue: Lambda timeout set to maximum (900s). Any operation exceeding this will fail.
> - Limit: 900 seconds (hard)
> - Docs: https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html
> - Mitigation: For longer processes, use Step Functions with Lambda iterations or switch to Fargate.

### Example 2: Multiple LBs per target group
**Input**: Terraform with shared target groups
```hcl
resource "aws_lb_target_group" "shared" {
  name = "shared-targets"
}

resource "aws_lb_listener" "lb1" {
  default_action {
    target_group_arn = aws_lb_target_group.shared.arn
  }
}
# ... repeated for 6 load balancers
```
**Output**:
> **Critical: Target group shared across too many load balancers**
> - File: `alb.tf:15-45`
> - Issue: Target group "shared-targets" referenced by 6 load balancers. Maximum is 5.
> - Limit: 5 load balancers per target group (hard)
> - Docs: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-limits.html
> - Mitigation: Create separate target groups for additional load balancers.
