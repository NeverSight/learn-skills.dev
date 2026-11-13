---
name: gcp-serverless-fullstack-architecture
description: Deliver GCP serverless fullstack systems with Cloud Run, API Gateway, Cloud Functions, Firebase Auth or IAP, Firestore or Cloud SQL, Cloud CDN, Pub/Sub, and Cloud Monitoring.
disable-model-invocation: true
---

# Gcp Serverless Fullstack Architecture

## Use When

- GCP-first architecture with managed scale
- Event-driven workflows with Pub/Sub

## Workflow

1. Choose Cloud Run vs Cloud Functions per workload shape
2. Define API Gateway or load balancer ingress and auth
3. Implement services with clear contract versioning
4. Configure Cloud CDN and frontend hosting strategy
5. Use Pub/Sub with dead-letter topics and replay procedures
6. Set SLOs, dashboards, and error budgets in Cloud Monitoring

## Required Checks

- Service accounts follow least privilege per workload
- Ingress auth validated on every protected route
- Idempotency enforced for async consumers
- Multi-region or failover strategy documented where required

## Decision Framework

- Prefer Cloud Run for containerized services with flexible runtime needs
- Use Pub/Sub for decoupled domain events
- Keep synchronous call graphs shallow for latency control
- Treat IaC as source of truth across environments

## Common Rationalizations And Rebuttals

- "Cloud Run removes all backend concerns." -> Concurrency, cold start, and egress still need design.
- "Pub/Sub ordering is guaranteed globally." -> Design for duplicates and disorder.
- "Firebase rules replace API auth." -> Backend must enforce authorization independently.

## Evidence Pack

- Auth negative test suite results
- Pub/Sub replay and poison-message handling proof
- CDN cache and purge validation during release
- Terraform plan and rollback checklist

## Exit Criteria

- GCP serverless delivery is observable and recoverable
- Release can be rolled back without data corruption
