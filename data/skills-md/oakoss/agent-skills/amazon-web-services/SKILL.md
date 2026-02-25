---
name: amazon-web-services
description: |
  Core AWS services for application developers. Covers S3 (storage, presigned URLs, lifecycle), Lambda (functions, layers, cold starts), IAM (roles, policies, least privilege), DynamoDB (single-table design, GSI/LSI, streams), SQS/SNS (queues, topics, fan-out), CloudFront (CDN, caching), RDS/Aurora (Postgres/MySQL, connection pooling), ECR/ECS/Fargate (containers), Route 53 (DNS), Secrets Manager, and CDK v2 (TypeScript IaC, constructs, stacks, testing).

  Use when building AWS infrastructure, writing CDK stacks, configuring IAM policies, designing DynamoDB tables, setting up Lambda functions, creating S3 presigned URLs, deploying containers on ECS/Fargate, or configuring CloudFront distributions.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://docs.aws.amazon.com/'
user-invocable: false
---

# Amazon Web Services

## Overview

Amazon Web Services (AWS) provides cloud computing services for building scalable applications. The AWS SDK for JavaScript v3 uses modular packages (`@aws-sdk/client-*`) with first-class TypeScript support. AWS CDK v2 defines infrastructure as code using TypeScript constructs that synthesize to CloudFormation templates.

**When to use:** Building cloud-native applications, serverless architectures, container deployments, managed databases, CDN distribution, event-driven systems, or infrastructure as code.

**When NOT to use:** Simple static sites (consider Vercel/Netlify), local-only development tools, projects with no cloud deployment requirement.

## Quick Reference

| Service / Pattern | API / Construct                                            | Key Points                                                   |
| ----------------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| S3 upload         | `PutObjectCommand`                                         | Modular import from `@aws-sdk/client-s3`                     |
| S3 presigned URL  | `getSignedUrl()`                                           | From `@aws-sdk/s3-request-presigner`, max 7 days             |
| Lambda function   | `new lambda.Function()`                                    | CDK L2 construct, set `memorySize` and `timeout`             |
| Lambda layers     | `new lambda.LayerVersion()`                                | Share code/deps across functions                             |
| IAM policy        | `new iam.PolicyStatement()`                                | Always use least privilege, avoid `*` resources              |
| DynamoDB table    | `new dynamodb.Table()`                                     | Single-table design, PAY_PER_REQUEST for variable loads      |
| DynamoDB GSI      | `table.addGlobalSecondaryIndex()`                          | Separate throughput, eventual consistency                    |
| SQS queue         | `new sqs.Queue()`                                          | DLQ for failed messages, long polling with `WaitTimeSeconds` |
| SNS topic         | `new sns.Topic()`                                          | Fan-out to SQS, Lambda, HTTP endpoints                       |
| CloudFront        | `new cloudfront.Distribution()`                            | OAC for S3 origins, cache policies                           |
| RDS/Aurora        | `new rds.DatabaseCluster()`                                | Use RDS Proxy for connection pooling                         |
| ECS Fargate       | `new ecs_patterns.ApplicationLoadBalancedFargateService()` | Higher-level pattern construct                               |
| Route 53          | `new route53.ARecord()`                                    | Alias records for AWS resources                              |
| Secrets Manager   | `secretsmanager.Secret.fromSecretNameV2()`                 | Automatic rotation, never hardcode secrets                   |
| CDK stack         | `new cdk.Stack(app, 'Id')`                                 | One stack per deployment unit                                |
| CDK testing       | `Template.fromStack(stack)`                                | Fine-grained assertions and snapshot tests                   |

## Common Mistakes

| Mistake                                             | Correct Pattern                                                 |
| --------------------------------------------------- | --------------------------------------------------------------- |
| Using AWS SDK v2 (`aws-sdk`)                        | Use modular v3 (`@aws-sdk/client-*`) for smaller bundles        |
| IAM `Action: "*"` or `Resource: "*"`                | Scope to specific actions and resource ARNs                     |
| No DLQ on SQS queues                                | Always attach a dead-letter queue for failed messages           |
| DynamoDB scan for queries                           | Design access patterns first, use Query with GSI/LSI            |
| Hardcoding secrets in code or env vars              | Use Secrets Manager or SSM Parameter Store                      |
| Lambda bundling `node_modules` without tree-shaking | Use `NodejsFunction` with esbuild bundling                      |
| Missing `RemovalPolicy` on stateful resources       | Set `RemovalPolicy.RETAIN` for production databases and buckets |
| Creating one Lambda per CRUD operation              | Group related operations, use event routing                     |
| No connection pooling for RDS                       | Use RDS Proxy or limit `max_connections` per Lambda             |
| CloudFront without cache policy                     | Define explicit `CachePolicy` to control TTL and headers        |
| CDK testing only with snapshots                     | Combine fine-grained assertions with snapshot tests             |
| Presigned URL without content-type                  | Include `ContentType` in `PutObjectCommand` for uploads         |

## Delegation

- **Infrastructure patterns**: Use `Explore` agent for AWS architecture discovery
- **Security review**: Use `Task` agent for IAM policy auditing
- **Cost optimization**: Use `Task` agent for resource right-sizing

> If the `docker` skill is available, delegate container build patterns and Dockerfile optimization to it.
> If the `github-actions` skill is available, delegate CI/CD pipeline patterns for AWS deployments to it.
> If the `typescript-patterns` skill is available, delegate TypeScript strict mode and type patterns used in CDK code to it.
> If the `application-security` skill is available, delegate AWS security best practices and threat modeling to it.

## References

- [S3 storage, presigned URLs, and lifecycle policies](references/s3-storage.md)
- [Lambda functions, layers, cold starts, and event sources](references/lambda-functions.md)
- [IAM roles, policies, and least-privilege patterns](references/iam-security.md)
- [DynamoDB single-table design, GSI/LSI, and streams](references/dynamodb.md)
- [SQS queues, SNS topics, and fan-out messaging](references/messaging-sqs-sns.md)
- [ECS/Fargate container deployment and ECR](references/containers-ecs-fargate.md)
- [CloudFront CDN, Route 53 DNS, and networking](references/networking-cloudfront-route53.md)
- [CDK v2 infrastructure as code, constructs, stacks, and testing](references/cdk-infrastructure.md)
