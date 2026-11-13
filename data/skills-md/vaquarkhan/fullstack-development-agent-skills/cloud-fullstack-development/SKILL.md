---
name: cloud-fullstack-development
description: Deliver cloud-ready fullstack systems across frontend and microservices with environment strategy, security, observability, and CI/CD controls. Use when users ask for AWS, Azure, or GCP fullstack architecture and deployment planning.
disable-model-invocation: true
---

# Cloud Fullstack Development

## Use When

- Planning or delivering fullstack systems on AWS, Azure, or GCP
- Environment strategy, security, observability, or CI/CD needs definition

## Workflow

1. Define frontend, API, and data architecture for the target cloud.
2. Define environment boundaries (dev, staging, prod).
3. Implement identity, secrets, and network security controls.
4. Add observability and release automation.
5. Validate cost, reliability, and disaster recovery readiness.

## Required Checks

- Infrastructure-as-code plan exists
- Least-privilege access model is documented
- Service and UI telemetry are correlated
- Rollback and incident response paths are tested

## Decision Framework

- Separate dev/staging/prod accounts or subscriptions with least-privilege IAM per environment.
- Define frontend hosting, API compute, data tier, and secrets vault before first deploy script.
- Correlate UI telemetry with backend trace IDs across the cloud boundary.
- Validate DR, cost guardrails, and rollback paths in a staging environment that mirrors prod topology.

## Common Rationalizations And Rebuttals

- "Console clicks are fine for v1." -> Undocumented console state blocks reproducibility; use IaC from day one.
- "Same IAM role everywhere speeds delivery." -> Shared roles expand blast radius; scope roles per service and environment.
- "Observability can follow launch." -> Blind launches extend incidents; wire metrics and alerts before traffic.

## Evidence Pack

- IaC plan or module layout with environment matrix
- IAM policy summary showing least-privilege per service
- Correlated trace or log example from browser through cloud API to data tier
- Staging deploy proof with rollback or blue-green switch evidence

## Exit Criteria

- Workflow decisions are documented and implementation-ready
- Validation evidence exists for quality, reliability, and compatibility
- Operational readiness and rollback expectations are explicit

