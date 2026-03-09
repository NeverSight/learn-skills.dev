---
name: databricks-asset-bundles
description: Modern deployment with Databricks Asset Bundles (DAB), supporting multi-environment configurations and CI/CD integration.
triggers:
  - databricks asset bundles
  - dab deployment
  - bundle configuration
  - multi environment
  - infrastructure as code
category: deployment
---

# Databricks Asset Bundles Skill

## Overview

Databricks Asset Bundles (DAB) is a modern deployment framework that packages notebooks, DLT pipelines, jobs, and configurations into versioned, environment-aware bundles. It enables Infrastructure as Code for Databricks.

**Key Benefits:**
- Infrastructure as Code
- Multi-environment support (dev, staging, prod)
- Version control for all artifacts
- Automated deployment
- Environment-specific configurations
- Integrated with CI/CD

## When to Use This Skill

Use Databricks Asset Bundles when you need to:
- Deploy pipelines across multiple environments
- Implement Infrastructure as Code
- Automate deployment workflows
- Manage environment-specific configurations
- Version control Databricks artifacts
- Enable collaborative development
- Standardize deployment processes

## Core Concepts

### 1. Bundle Structure

**Standard Bundle Layout:**
```
my-bundle/
├── databricks.yml          # Main configuration
├── environments/
│   ├── dev.yml            # Development overrides
│   ├── staging.yml        # Staging overrides
│   └── prod.yml           # Production overrides
├── src/
│   ├── notebooks/
│   │   ├── bronze_ingestion.py
│   │   └── silver_transformation.py
│   └── pipelines/
│       └── dlt_pipeline.py
├── resources/
│   ├── jobs.yml
│   ├── pipelines.yml
│   └── clusters.yml
└── tests/
    └── test_transformations.py
```

### 2. Main Configuration

**databricks.yml:**
```yaml
bundle:
  name: data-platform-bundle
  # Optional git configuration
  git:
    branch: main
    origin_url: https://github.com/org/repo.git

workspace:
  host: https://your-workspace.databricks.com
  root_path: /Workspace/bundles/${bundle.name}

# Define variables
variables:
  catalog_name:
    description: "Unity Catalog name"
    default: "dev_catalog"

  storage_path:
    description: "Base storage path"
    default: "/mnt/dev/data"

  cluster_size:
    description: "Cluster size"
    default: "small"

# Include other configuration files
include:
  - resources/*.yml

# Define resources
resources:
  jobs:
    daily_pipeline:
      name: "[${bundle.environment}] Daily Pipeline"

      tasks:
        - task_key: bronze_ingestion
          notebook_task:
            notebook_path: ./src/notebooks/bronze_ingestion
            source: WORKSPACE
            base_parameters:
              catalog: ${var.catalog_name}
              storage: ${var.storage_path}

          new_cluster:
            num_workers: 2
            spark_version: 13.3.x-scala2.12
            node_type_id: i3.xlarge
            spark_conf:
              spark.databricks.delta.preview.enabled: "true"

        - task_key: silver_transformation
          depends_on:
            - task_key: bronze_ingestion
          notebook_task:
            notebook_path: ./src/notebooks/silver_transformation
            source: WORKSPACE

          job_cluster_key: shared_cluster

      job_clusters:
        - job_cluster_key: shared_cluster
          new_cluster:
            num_workers: "${var.cluster_size == 'small' ? 2 : 8}"
            spark_version: 13.3.x-scala2.12
            node_type_id: i3.xlarge

      schedule:
        quartz_cron_expression: "0 0 1 * * ?"  # Daily at 1 AM
        timezone_id: "America/New_York"

      email_notifications:
        on_failure:
          - data-team@company.com

  pipelines:
    bronze_to_gold:
      name: "[${bundle.environment}] Bronze to Gold Pipeline"
      target: ${var.catalog_name}
      storage: ${var.storage_path}/dlt

      libraries:
        - notebook:
            path: ./src/pipelines/dlt_pipeline.py

      clusters:
        - label: default
          num_workers: 4
          node_type_id: i3.xlarge

      configuration:
        source_path: ${var.storage_path}/landing
        checkpoint_path: ${var.storage_path}/checkpoints

      development: false
      continuous: false

targets:
  dev:
    mode: development
    workspace:
      host: https://dev-workspace.databricks.com
      root_path: /Workspace/dev/${bundle.name}
    variables:
      catalog_name: dev_catalog
      storage_path: /mnt/dev/data
      cluster_size: small

  staging:
    mode: production
    workspace:
      host: https://staging-workspace.databricks.com
      root_path: /Workspace/staging/${bundle.name}
    variables:
      catalog_name: staging_catalog
      storage_path: /mnt/staging/data
      cluster_size: medium

  prod:
    mode: production
    workspace:
      host: https://prod-workspace.databricks.com
      root_path: /Workspace/prod/${bundle.name}
    variables:
      catalog_name: prod_catalog
      storage_path: /mnt/prod/data
      cluster_size: large
```

### 3. Environment-Specific Configuration

**environments/prod.yml:**
```yaml
# Production-specific overrides
variables:
  catalog_name: prod_catalog
  storage_path: /mnt/prod/data
  cluster_size: large

resources:
  jobs:
    daily_pipeline:
      # Production-specific settings
      max_concurrent_runs: 1
      timeout_seconds: 7200

      job_clusters:
        - job_cluster_key: shared_cluster
          new_cluster:
            num_workers: 8
            node_type_id: i3.2xlarge
            autoscale:
              min_workers: 4
              max_workers: 16

      email_notifications:
        on_start:
          - data-team@company.com
        on_success:
          - data-team@company.com
        on_failure:
          - data-team@company.com
          - oncall@company.com

  pipelines:
    bronze_to_gold:
      development: false
      continuous: true  # Continuous processing in prod

      clusters:
        - label: default
          num_workers: 8
          node_type_id: i3.2xlarge
          autoscale:
            min_workers: 4
            max_workers: 16

      notifications:
        - email_recipients:
            - data-team@company.com
          on_failure: true
          on_success: false
```

### 4. Deployment Workflow

**CLI Commands:**
```bash
# Install Databricks CLI
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

# Authenticate
databricks auth login --host https://your-workspace.databricks.com

# Validate bundle
databricks bundle validate -t dev

# Deploy to development
databricks bundle deploy -t dev

# Run a job
databricks bundle run -t dev daily_pipeline

# Deploy to production
databricks bundle deploy -t prod

# Destroy bundle (cleanup)
databricks bundle destroy -t dev
```

## Implementation Patterns

### Pattern 1: Multi-Environment Pipeline

**Complete Bundle with Environment Variations:**
```yaml
# databricks.yml
bundle:
  name: customer-analytics

variables:
  environment:
    description: "Deployment environment"
  catalog:
    description: "Unity Catalog"
  min_workers:
    description: "Minimum cluster workers"
    default: 2
  max_workers:
    description: "Maximum cluster workers"
    default: 8

resources:
  jobs:
    customer_pipeline:
      name: "[${var.environment}] Customer Analytics Pipeline"

      tasks:
        - task_key: ingest
          notebook_task:
            notebook_path: ./notebooks/ingest_customers
          new_cluster:
            num_workers: ${var.min_workers}
            spark_version: 13.3.x-scala2.12
            node_type_id: i3.xlarge

        - task_key: transform
          depends_on:
            - task_key: ingest
          notebook_task:
            notebook_path: ./notebooks/transform_customers
          new_cluster:
            autoscale:
              min_workers: ${var.min_workers}
              max_workers: ${var.max_workers}
            spark_version: 13.3.x-scala2.12
            node_type_id: i3.xlarge

        - task_key: aggregate
          depends_on:
            - task_key: transform
          notebook_task:
            notebook_path: ./notebooks/aggregate_metrics
          new_cluster:
            num_workers: ${var.min_workers}
            spark_version: 13.3.x-scala2.12
            node_type_id: i3.xlarge

targets:
  dev:
    variables:
      environment: dev
      catalog: dev_catalog
      min_workers: 2
      max_workers: 4

  prod:
    variables:
      environment: prod
      catalog: prod_catalog
      min_workers: 4
      max_workers: 16
```

### Pattern 2: Modular Configuration

**Split Configuration Across Files:**
```yaml
# databricks.yml
bundle:
  name: data-platform

include:
  - resources/jobs/*.yml
  - resources/pipelines/*.yml
  - resources/clusters/*.yml

# resources/jobs/ingestion_jobs.yml
resources:
  jobs:
    ingest_customers:
      name: "[${bundle.environment}] Ingest Customers"
      tasks:
        - task_key: main
          notebook_task:
            notebook_path: ./notebooks/ingest_customers

    ingest_orders:
      name: "[${bundle.environment}] Ingest Orders"
      tasks:
        - task_key: main
          notebook_task:
            notebook_path: ./notebooks/ingest_orders

# resources/pipelines/dlt_pipelines.yml
resources:
  pipelines:
    customer_pipeline:
      name: "[${bundle.environment}] Customer DLT Pipeline"
      target: ${var.catalog}.customer
      libraries:
        - notebook:
            path: ./pipelines/customer_dlt

    order_pipeline:
      name: "[${bundle.environment}] Order DLT Pipeline"
      target: ${var.catalog}.orders
      libraries:
        - notebook:
            path: ./pipelines/order_dlt
```

### Pattern 3: Python Deployment Script

**Automated Deployment:**
```python
"""
Automated bundle deployment script.
"""
import subprocess
import sys
from typing import Dict, Any


class BundleDeployer:
    """Deploy Databricks Asset Bundles."""

    def __init__(self, bundle_path: str):
        self.bundle_path = bundle_path

    def validate(self, target: str) -> bool:
        """Validate bundle configuration."""
        print(f"Validating bundle for target: {target}")

        result = subprocess.run(
            ["databricks", "bundle", "validate", "-t", target],
            cwd=self.bundle_path,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Validation failed: {result.stderr}")
            return False

        print("Validation successful")
        return True

    def deploy(self, target: str, force: bool = False) -> bool:
        """Deploy bundle to target environment."""
        if not self.validate(target):
            return False

        print(f"Deploying bundle to {target}")

        cmd = ["databricks", "bundle", "deploy", "-t", target]
        if force:
            cmd.append("--force")

        result = subprocess.run(
            cmd,
            cwd=self.bundle_path,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Deployment failed: {result.stderr}")
            return False

        print(f"Deployment successful: {result.stdout}")
        return True

    def run_job(self, target: str, job_key: str) -> bool:
        """Run a specific job from bundle."""
        print(f"Running job: {job_key} on {target}")

        result = subprocess.run(
            ["databricks", "bundle", "run", "-t", target, job_key],
            cwd=self.bundle_path,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Job run failed: {result.stderr}")
            return False

        print(f"Job started: {result.stdout}")
        return True

    def destroy(self, target: str, auto_approve: bool = False) -> bool:
        """Destroy bundle resources."""
        print(f"WARNING: Destroying bundle resources in {target}")

        cmd = ["databricks", "bundle", "destroy", "-t", target]
        if auto_approve:
            cmd.append("--auto-approve")

        result = subprocess.run(
            cmd,
            cwd=self.bundle_path,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Destroy failed: {result.stderr}")
            return False

        print("Bundle resources destroyed")
        return True


# Usage
if __name__ == "__main__":
    deployer = BundleDeployer("./my-bundle")

    # Deploy to development
    if deployer.deploy("dev"):
        deployer.run_job("dev", "daily_pipeline")

    # Deploy to production (requires approval)
    if len(sys.argv) > 1 and sys.argv[1] == "--prod":
        deployer.deploy("prod")
```

### Pattern 4: GitOps Integration

**GitHub Actions Workflow:**
```yaml
# .github/workflows/bundle-deploy.yml
name: Deploy Databricks Bundle

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options:
          - dev
          - staging
          - prod

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Databricks CLI
        run: |
          curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

      - name: Validate Bundle
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
        run: |
          cd bundle/
          databricks bundle validate -t dev

  deploy-dev:
    needs: validate
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: development
    steps:
      - uses: actions/checkout@v3

      - name: Install Databricks CLI
        run: |
          curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

      - name: Deploy to Development
        env:
          DATABRICKS_HOST: ${{ secrets.DEV_DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DEV_DATABRICKS_TOKEN }}
        run: |
          cd bundle/
          databricks bundle deploy -t dev

  deploy-prod:
    needs: validate
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v3

      - name: Install Databricks CLI
        run: |
          curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

      - name: Deploy to Production
        env:
          DATABRICKS_HOST: ${{ secrets.PROD_DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.PROD_DATABRICKS_TOKEN }}
        run: |
          cd bundle/
          databricks bundle deploy -t prod
```

## Best Practices

### 1. Bundle Organization

- Keep bundle files under version control
- Use environment-specific overrides
- Separate resources into logical files
- Document variable purposes
- Include README for bundle usage

### 2. Environment Management

```yaml
# Use consistent naming
targets:
  dev:
    mode: development  # Enables faster iterations
  staging:
    mode: production   # Production-like behavior
  prod:
    mode: production   # Full production settings
```

### 3. Variable Usage

```yaml
# Define reusable variables
variables:
  project_name:
    description: "Project identifier"
    default: "customer-analytics"

# Use variables consistently
resources:
  jobs:
    ${var.project_name}_job:
      name: "[${bundle.environment}] ${var.project_name}"
```

### 4. Testing Strategy

```bash
# Test bundle locally
databricks bundle validate -t dev

# Deploy to dev for testing
databricks bundle deploy -t dev

# Run integration tests
databricks bundle run -t dev test_job

# Deploy to prod after validation
databricks bundle deploy -t prod
```

## Common Pitfalls to Avoid

Don't:
- Hard-code environment-specific values
- Skip validation before deployment
- Modify resources outside of bundles
- Use development mode in production
- Deploy without testing

Do:
- Use variables for environment differences
- Always validate before deploying
- Manage all resources through bundles
- Use production mode for prod
- Test in lower environments first

## Complete Examples

See `/examples/` directory for:
- `complete_bundle_project/`: Full bundle structure
- `multi_workspace_deployment/`: Cross-workspace deployment

## Related Skills

- `delta-live-tables`: Deploy DLT pipelines
- `cicd-workflows`: Automate deployments
- `testing-patterns`: Test before deploy
- `data-products`: Deploy data products

## References

- [Databricks Asset Bundles Docs](https://docs.databricks.com/dev-tools/bundles/index.html)
- [Bundle Configuration Reference](https://docs.databricks.com/dev-tools/bundles/settings.html)
- [CLI Reference](https://docs.databricks.com/dev-tools/cli/index.html)
