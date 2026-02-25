---
name: iac
description: |
  Use when working with Infrastructure as Code tools and platforms. Covers Terraform, Pulumi, CloudFormation, Bicep, ARM, Kubernetes, Helm, Docker, Crossplane, and Dagger.
  USE FOR: choosing IaC tools, comparing Terraform vs Pulumi vs CloudFormation, infrastructure strategy
  DO NOT USE FOR: specific tool syntax (use the sub-skills: terraform, pulumi, bicep, etc.)
license: MIT
metadata:
  displayName: "Infrastructure as Code"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Terraform Documentation"
    url: "https://developer.hashicorp.com/terraform/docs"
  - title: "Kubernetes Documentation"
    url: "https://kubernetes.io/docs/home/"
  - title: "Pulumi Documentation"
    url: "https://www.pulumi.com/docs/"
---

# Infrastructure as Code

## Overview
Infrastructure as Code (IaC) defines and manages cloud resources, containers, and deployment pipelines through declarative or imperative code rather than manual configuration. This skill covers the major IaC tools and their trade-offs.

## Tool Landscape

| Tool | Approach | Language | Scope |
|------|----------|----------|-------|
| **Terraform** | Declarative | HCL | Multi-cloud infrastructure |
| **Pulumi** | Imperative | TypeScript, Python, Go, C# | Multi-cloud infrastructure |
| **CloudFormation** | Declarative | JSON/YAML | AWS-only infrastructure |
| **Bicep** | Declarative | Bicep DSL | Azure-only infrastructure |
| **ARM** | Declarative | JSON | Azure-only infrastructure |
| **Kubernetes** | Declarative | YAML | Container orchestration |
| **Helm** | Declarative (templated) | YAML + Go templates | Kubernetes package management |
| **Docker** | Declarative | Dockerfile | Container image builds |
| **Crossplane** | Declarative | YAML (K8s CRDs) | Kubernetes-native cloud provisioning |
| **Dagger** | Imperative | TypeScript, Python, Go | CI/CD pipelines as code |

## Choosing the Right Tool

### Cloud Infrastructure
- **Multi-cloud or cloud-agnostic?** Use Terraform or Pulumi
- **AWS-only?** CloudFormation is native, or use Terraform/Pulumi
- **Azure-only?** Bicep is the modern choice (replaces ARM templates)
- **Kubernetes-native approach?** Crossplane extends the K8s control plane to cloud resources

### Containers and Orchestration
- **Building images?** Dockerfile with multi-stage builds
- **Running containers?** Kubernetes manifests or Docker Compose
- **Packaging K8s apps?** Helm charts for templated, distributable deployments

### Pipelines
- **Programmable CI/CD?** Dagger runs pipelines in containers with real language SDKs

## General Best Practices
- Store all IaC in version control alongside application code.
- Use state management (Terraform state, Pulumi state, CloudFormation stacks) to track what's deployed.
- Pin provider/module versions for reproducible deployments.
- Use environments (dev/staging/prod) with parameterized configurations.
- Validate changes before applying: `terraform plan`, `pulumi preview`, CloudFormation change sets.
- Use secrets management — never hardcode credentials in IaC files.
