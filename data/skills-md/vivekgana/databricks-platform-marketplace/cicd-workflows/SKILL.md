---
name: cicd-workflows
description: GitHub Actions and CI/CD patterns for Databricks, including automated testing, deployment, and quality gates.
triggers:
  - ci cd
  - github actions
  - continuous integration
  - continuous deployment
  - automated testing
category: devops
---

# CI/CD Workflows Skill

## Overview

Comprehensive CI/CD patterns for Databricks using GitHub Actions, including automated testing, quality gates, multi-environment deployments, and rollback strategies.

**Key Benefits:**
- Automated testing and validation
- Consistent deployments
- Environment promotion workflows
- Quality gates enforcement
- Rollback capabilities
- Audit trails

## When to Use This Skill

Use CI/CD workflows when you need to:
- Automate deployment processes
- Enforce quality standards
- Deploy across multiple environments
- Implement approval gates
- Track deployment history
- Enable rapid iterations
- Reduce manual errors

## Core Concepts

### 1. CI Pipeline

**Continuous Integration Workflow:**
```yaml
# .github/workflows/ci.yml
name: Continuous Integration

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]

jobs:
  lint:
    name: Code Quality Checks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install black ruff mypy
          pip install -r requirements.txt

      - name: Run Black
        run: black --check src/

      - name: Run Ruff
        run: ruff check src/

      - name: Run MyPy
        run: mypy src/

  test:
    name: Unit Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install pytest pytest-cov pytest-spark
          pip install -r requirements.txt

      - name: Run Tests
        run: pytest tests/ -v --cov=src --cov-report=xml

      - name: Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true

  validate-bundle:
    name: Validate Databricks Bundle
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
        run: databricks bundle validate -t dev
```

### 2. CD Pipeline

**Continuous Deployment Workflow:**
```yaml
# .github/workflows/cd.yml
name: Continuous Deployment

on:
  push:
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
  deploy-dev:
    name: Deploy to Development
    if: github.event_name == 'push' || github.event.inputs.environment == 'dev'
    runs-on: ubuntu-latest
    environment: development
    steps:
      - uses: actions/checkout@v3

      - name: Install Databricks CLI
        run: |
          curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

      - name: Deploy Bundle
        env:
          DATABRICKS_HOST: ${{ secrets.DEV_DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DEV_DATABRICKS_TOKEN }}
        run: |
          databricks bundle deploy -t dev
          databricks bundle run -t dev integration_tests

  deploy-staging:
    name: Deploy to Staging
    needs: deploy-dev
    if: github.event_name == 'push' || github.event.inputs.environment == 'staging'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v3

      - name: Install Databricks CLI
        run: |
          curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

      - name: Deploy Bundle
        env:
          DATABRICKS_HOST: ${{ secrets.STAGING_DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.STAGING_DATABRICKS_TOKEN }}
        run: databricks bundle deploy -t staging

      - name: Run Smoke Tests
        env:
          DATABRICKS_HOST: ${{ secrets.STAGING_DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.STAGING_DATABRICKS_TOKEN }}
        run: databricks bundle run -t staging smoke_tests

  deploy-prod:
    name: Deploy to Production
    needs: deploy-staging
    if: github.event_name == 'push' || github.event.inputs.environment == 'prod'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://prod-workspace.databricks.com
    steps:
      - uses: actions/checkout@v3

      - name: Install Databricks CLI
        run: |
          curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

      - name: Create Backup
        env:
          DATABRICKS_HOST: ${{ secrets.PROD_DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.PROD_DATABRICKS_TOKEN }}
        run: |
          # Backup current state
          databricks bundle generate deployment-state --target prod > backup-state.json

      - name: Deploy Bundle
        env:
          DATABRICKS_HOST: ${{ secrets.PROD_DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.PROD_DATABRICKS_TOKEN }}
        run: databricks bundle deploy -t prod

      - name: Run Health Checks
        env:
          DATABRICKS_HOST: ${{ secrets.PROD_DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.PROD_DATABRICKS_TOKEN }}
        run: databricks bundle run -t prod health_check

      - name: Notify Deployment
        if: success()
        run: |
          echo "Production deployment successful"
          # Send notification (Slack, email, etc.)
```

### 3. Quality Gates

**Enforce Quality Standards:**
```yaml
# .github/workflows/quality-gates.yml
name: Quality Gates

on:
  pull_request:
    branches: [main, develop]

jobs:
  security-scan:
    name: Security Vulnerability Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Bandit Security Scan
        run: |
          pip install bandit
          bandit -r src/ -f json -o bandit-report.json

      - name: Run Safety Check
        run: |
          pip install safety
          safety check --json

  code-coverage:
    name: Code Coverage Gate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Run Tests with Coverage
        run: |
          pip install pytest pytest-cov
          pip install -r requirements.txt
          pytest tests/ --cov=src --cov-report=term --cov-fail-under=80

  data-quality:
    name: Data Quality Checks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Validate Data Contracts
        run: |
          python scripts/validate_contracts.py

      - name: Check DLT Expectations
        run: |
          python scripts/validate_dlt_expectations.py
```

### 4. Rollback Strategy

**Automated Rollback:**
```yaml
# .github/workflows/rollback.yml
name: Rollback Deployment

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to rollback'
        required: true
        type: choice
        options:
          - dev
          - staging
          - prod
      version:
        description: 'Version to rollback to (commit SHA or tag)'
        required: true
        type: string

jobs:
  rollback:
    name: Rollback to Previous Version
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment }}
    steps:
      - uses: actions/checkout@v3
        with:
          ref: ${{ github.event.inputs.version }}

      - name: Install Databricks CLI
        run: |
          curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

      - name: Validate Rollback Version
        run: |
          echo "Rolling back to version: ${{ github.event.inputs.version }}"
          databricks bundle validate -t ${{ github.event.inputs.environment }}

      - name: Deploy Previous Version
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
        run: |
          databricks bundle deploy -t ${{ github.event.inputs.environment }}

      - name: Verify Rollback
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
        run: |
          databricks bundle run -t ${{ github.event.inputs.environment }} health_check
```

## Implementation Patterns

### Pattern 1: Matrix Testing

**Test Across Multiple Versions:**
```yaml
name: Matrix Testing

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
        spark-version: ['3.3.0', '3.4.0']

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install PySpark ${{ matrix.spark-version }}
        run: |
          pip install pyspark==${{ matrix.spark-version }}
          pip install -r requirements.txt

      - name: Run Tests
        run: pytest tests/ -v
```

### Pattern 2: Blue-Green Deployment

**Zero-Downtime Deployments:**
```yaml
name: Blue-Green Deployment

on:
  workflow_dispatch:
    inputs:
      color:
        description: 'Deployment color'
        required: true
        type: choice
        options:
          - blue
          - green

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to ${{ github.event.inputs.color }}
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
          COLOR: ${{ github.event.inputs.color }}
        run: |
          # Deploy to color-specific namespace
          databricks bundle deploy -t prod --var environment_color=$COLOR

      - name: Run Health Checks
        run: |
          # Verify new deployment
          python scripts/health_check.py --color $COLOR

      - name: Switch Traffic
        if: success()
        run: |
          # Update routing to new color
          python scripts/switch_traffic.py --to $COLOR

      - name: Cleanup Old Deployment
        run: |
          # Remove old color after successful switch
          OLD_COLOR=$([ "$COLOR" == "blue" ] && echo "green" || echo "blue")
          databricks bundle destroy -t prod --var environment_color=$OLD_COLOR --auto-approve
```

### Pattern 3: Canary Deployment

**Gradual Rollout:**
```yaml
name: Canary Deployment

on:
  workflow_dispatch:
    inputs:
      canary_percentage:
        description: 'Percentage of traffic for canary'
        required: true
        type: choice
        options:
          - '10'
          - '25'
          - '50'
          - '100'

jobs:
  canary-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy Canary
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
        run: |
          databricks bundle deploy -t prod-canary

      - name: Route Traffic to Canary
        run: |
          python scripts/route_traffic.py \\
            --canary-percentage ${{ github.event.inputs.canary_percentage }}

      - name: Monitor Canary
        timeout-minutes: 30
        run: |
          python scripts/monitor_canary.py \\
            --duration 30 \\
            --error-threshold 0.01

      - name: Promote or Rollback
        run: |
          if python scripts/check_canary_health.py; then
            echo "Canary healthy - promoting"
            databricks bundle deploy -t prod
          else
            echo "Canary unhealthy - rolling back"
            python scripts/rollback_canary.py
            exit 1
          fi
```

### Pattern 4: Scheduled Deployments

**Time-Based Deployment Windows:**
```yaml
name: Scheduled Production Deployment

on:
  schedule:
    # Deploy every Tuesday at 2 AM UTC
    - cron: '0 2 * * 2'
  workflow_dispatch:

jobs:
  check-deployment-window:
    runs-on: ubuntu-latest
    outputs:
      should_deploy: ${{ steps.check.outputs.should_deploy }}
    steps:
      - name: Check if in deployment window
        id: check
        run: |
          # Check if current time is within deployment window
          HOUR=$(date +%H)
          DAY=$(date +%u)
          if [ "$DAY" == "2" ] && [ "$HOUR" -ge "2" ] && [ "$HOUR" -le "4" ]; then
            echo "should_deploy=true" >> $GITHUB_OUTPUT
          else
            echo "should_deploy=false" >> $GITHUB_OUTPUT
          fi

  deploy:
    needs: check-deployment-window
    if: needs.check-deployment-window.outputs.should_deploy == 'true'
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
          databricks bundle deploy -t prod

      - name: Send Notification
        if: always()
        run: |
          python scripts/send_notification.py \\
            --status ${{ job.status }} \\
            --environment production
```

### Pattern 5: Integration Testing

**Automated Integration Tests:**
```yaml
name: Integration Tests

on:
  push:
    branches: [develop]
  schedule:
    - cron: '0 */4 * * *'  # Every 4 hours

jobs:
  integration-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install pytest databricks-connect databricks-sdk
          pip install -r requirements.txt

      - name: Run Integration Tests
        env:
          DATABRICKS_HOST: ${{ secrets.TEST_DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.TEST_DATABRICKS_TOKEN }}
        run: |
          pytest tests/integration/ -v \\
            --junit-xml=test-results.xml

      - name: Publish Test Results
        if: always()
        uses: EnricoMi/publish-unit-test-result-action@v2
        with:
          files: test-results.xml

      - name: Cleanup Test Data
        if: always()
        run: python scripts/cleanup_test_data.py
```

## Best Practices

### 1. Secrets Management

```yaml
# Use GitHub Secrets for credentials
env:
  DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
  DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}

# Never commit secrets to repository
# Use environment-specific secrets
```

### 2. Approval Gates

```yaml
# Require manual approval for production
environment:
  name: production
  url: https://prod-workspace.databricks.com
  # Configure required reviewers in GitHub settings
```

### 3. Deployment Notifications

```yaml
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Deployment to ${{ github.event.inputs.environment }}'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### 4. Artifact Management

```yaml
- name: Upload Bundle Artifact
  uses: actions/upload-artifact@v3
  with:
    name: databricks-bundle
    path: |
      databricks.yml
      resources/
      src/
    retention-days: 90
```

## Common Pitfalls to Avoid

Don't:
- Skip testing in CI pipeline
- Deploy without validation
- Hard-code secrets
- Deploy directly to production
- Skip rollback planning

Do:
- Test every change
- Validate before deploying
- Use secret management
- Use staging environments
- Plan rollback strategy

## Complete Examples

See `/examples/` directory for:
- `full_cicd_pipeline/`: Complete CI/CD setup
- `blue_green_deployment/`: Zero-downtime deployment

## Related Skills

- `databricks-asset-bundles`: Bundle deployment
- `testing-patterns`: Automated testing
- `data-quality`: Quality validation
- `delta-live-tables`: Pipeline deployment

## References

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Databricks CI/CD Best Practices](https://docs.databricks.com/dev-tools/ci-cd/index.html)
- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html)
