---
name: terraform-best-practices
description: Industry-standard Terraform patterns, modular structure, and security validation. Use when reviewing, refactoring, or authoring Terraform code (.tf files) to ensure maintainability and security.
---

# Terraform Best Practices

This skill ensures that Terraform configurations are modular, secure, and maintainable by following established industry standards and organizational patterns.

## When to Use
- Reviewing existing Terraform code for anti-patterns and technical debt.
- Refactoring monolithic `.tf` files into reusable, versioned modules.
- Setting up new infrastructure projects to ensure a consistent directory structure from the start.
- Validating security, naming conventions, and resource tagging before committing changes.

## Core Guidelines

### 1. Standard Directory Structure
Every module or root configuration MUST maintain a consistent file layout:
- `main.tf`: Primary resource definitions.
- `variables.tf`: Input variable declarations (always include `description` and `type`).
- `outputs.tf`: Output value definitions (always include `description`).
- `versions.tf`: Minimum required Terraform and provider version constraints.
- `providers.tf`: Provider configurations (restrict this to root modules only).

### 2. The Module Pattern
- **Encapsulate**: Move complex or repetitive logic into a local `modules/` directory or a remote registry.
- **Root Simplicity**: Root modules should primarily serve as an orchestration layer, calling sub-modules.
- **Decouple**: Avoid hardcoding environment-specific values; pass them as variables.

### 3. State Management
- **Remote Backends**: Always use a remote backend (e.g., S3 + DynamoDB for AWS, GCS for GCP) for team collaboration.
- **State Locking**: Ensure state locking is enabled to prevent concurrent modifications and state corruption.

### 4. Semantic Versioning (SemVer)
All separated or shared modules MUST follow semantic versioning (`MAJOR.MINOR.PATCH`) based on the interface (variables and outputs):
- **MAJOR (Breaking)**: Incremented for breaking changes to the module's interface (e.g., removing a variable, changing a variable type, or changing the resource graph in a way that requires recreation).
- **MINOR (Feature)**: Incremented for new features that are backwards-compatible (e.g., adding a new optional variable or a new output).
- **PATCH (Fix)**: Incremented for backwards-compatible bug fixes or internal refactors that do not change the interface.
- **Requirement**: Every version bump MUST be accompanied by successful Terratest execution.

### 5. Naming & Tagging Conventions
- **Naming**: Use `snake_case` for all resource, variable, and output names. Avoid repeating the resource type in the name (e.g., use `resource "aws_instance" "web" {}` instead of `web_instance`).
- **Standard Tagging**: Taggable resources MUST include a standard `tags` block:
  - `Owner`: The team or individual responsible for the resource.
  - `Environment`: Deployment stage (e.g., `dev`, `staging`, `prod`).
  - `Project`: Name of the project or application.
  - `ManagedBy`: Always set to `terraform`.

### 5. Validation & Tooling
Before finalizing changes, execute the following sequence:
1. **Format**: `terraform fmt` (automated style alignment).
2. **Validate**: `terraform validate` (syntactic and structural check).
3. **Lint**: Use `tflint` for deep linting and provider-specific best practices.
4. **Security**: Run `tfsec` or `checkov` to identify security vulnerabilities.
5. **Test**: Execute automated infrastructure tests using **Terratest** to verify behavioral correctness.

## Infrastructure Testing (Terratest)
Every module MUST include automated tests in a `tests/` directory:
- **Language**: Use Go with the `gruntwork-io/terratest` library.
- **Scope**:
    - **Unit Tests**: Deploy a minimal version of the module and verify outputs/resource attributes.
    - **Integration Tests**: Verify the module works correctly when combined with other infrastructure (e.g., VPC + DB).
- **Cleanup**: Always use `defer terraform.Destroy(t, terraformOptions)` to ensure resources are cleaned up after tests.

## Workflow: Reviewing Existing Code
1. **Inventory**: Identify all `.tf` files and their dependencies.
2. **Gap Analysis**: Compare the current layout and code against these best practices.
3. **Detection**: Look for anti-patterns:
   - Missing `description` on variables/outputs.
   - Hardcoded secrets or sensitive data (recommend `vault` or `aws_secretsmanager`).
   - Monolithic files (> 300 lines).
4. **Refactor Plan**: Propose a step-by-step plan to modularize or fix the identified issues.

## Workflow: Authoring New Resources
1. **Scaffold**: Create the standard file set (`main.tf`, `variables.tf`, etc.).
2. **Define**: Declare variables with clear types and descriptions before writing resource blocks.
3. **Document**: Use `terraform-docs` to generate READMEs for modules.

## Overriding Standards (`TERRAFORM.md`)
If a `TERRAFORM.md` file exists in the workspace root, its instructions and conventions take absolute precedence over these general guidelines. Always check for this file first.
