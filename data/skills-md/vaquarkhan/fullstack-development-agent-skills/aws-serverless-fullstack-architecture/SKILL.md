---
name: aws-serverless-fullstack-architecture
description: Design and ship AWS serverless fullstack systems using API Gateway, Lambda, Cognito, DynamoDB or RDS, S3, CloudFront, EventBridge, and observability controls.
disable-model-invocation: true
---

# Aws Serverless Fullstack Architecture

## Use When

- Building on AWS with Lambda and managed services
- Need low-ops scaling for API and UI delivery

## Workflow

1. Map user journeys to serverless boundaries and data ownership
2. Define API Gateway routes, auth, and schema validation
3. Implement Lambda handlers with idempotency and DLQ paths
4. Configure CloudFront and S3 for frontend delivery
5. Wire EventBridge or SQS for async workflows
6. Add X-Ray, CloudWatch metrics, and alarm thresholds

## Required Checks

- IAM policies are least-privilege per function and route
- Cold start and timeout budgets are defined per endpoint
- Secrets use Parameter Store or Secrets Manager
- Multi-AZ and backup strategy documented for stateful services

## Decision Framework

- Prefer managed services over self-managed compute when SLO allows
- Keep synchronous chains short to control latency
- Use async boundaries for non-critical side effects
- Define environment-specific config and drift controls

## Common Rationalizations And Rebuttals

- "Serverless means no ops." -> You still own reliability, security, and cost guardrails.
- "One fat Lambda is faster to build." -> It becomes a distributed monolith; split by bounded context.
- "We can skip DLQ handling." -> Failed async work will be lost or duplicated unpredictably.

## Evidence Pack

- Architecture diagram with ownership boundaries
- IAM and network policy review evidence
- Load and cold-start test results for critical APIs
- Rollback and alarm runbook for top failure modes

## Exit Criteria

- AWS serverless stack is production-ready with tested failover paths
- Cost and latency guardrails are monitored
