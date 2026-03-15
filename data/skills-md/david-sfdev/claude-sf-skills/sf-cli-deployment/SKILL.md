---
name: sf-cli-deployment
description: Expert guidance for Salesforce CLI (sf) development deployments. Use this skill when deploying code during development, testing changes in sandboxes/scratch orgs, or when the user mentions sf CLI, deployments, or org operations. Focused on iterative development workflow.
---

# Salesforce CLI Development Deployment Guide

## Core Principles

**CRITICAL**: Use the modern `sf` CLI (not legacy `sfdx`) for all Salesforce operations. This skill focuses on **development deployments** for iterative coding workflows, not production migrations or CI/CD pipelines.

## Understanding Deployment Commands

### ❌ CRITICAL MISTAKE TO AVOID

**NEVER use `deploy start` to check deployment status!**

```bash
# ❌ WRONG - Starting new deployment when you meant to check status
sf project deploy start --source-dir force-app
# This starts a NEW deployment, doesn't check existing one!

# ✅ CORRECT - Check status of existing deployment
sf project deploy report --job-id <deployment-id>

# ✅ CORRECT - Resume waiting for existing deployment
sf project deploy resume --job-id <deployment-id> --wait 30
```

### Deployment Command Breakdown

**Starting a deployment:**
```bash
# Deploy and get deployment ID
sf project deploy start --source-dir force-app

# Returns:
# Deploying... ID: 0Af1234567890ABCD
# Status: InProgress
```

**Checking deployment status:**
```bash
# Use the deployment ID to check status
sf project deploy report --job-id 0Af1234567890ABCD

# Shows current status: InProgress, Succeeded, Failed
```

**Waiting for completion:**
```bash
# Resume waiting for deployment to complete
sf project deploy resume --job-id 0Af1234567890ABCD --wait 30

# Waits up to 30 minutes for completion
```

**Canceling a deployment:**
```bash
# Cancel long-running deployment if needed
sf project deploy cancel --job-id 0Af1234567890ABCD

# Use when deployment is taking too long or was started by mistake
```

## Modern sf CLI Commands

**Always use `sf` (not legacy `sfdx`):**
```bash
# ✅ CORRECT - Modern sf CLI
sf project deploy start --source-dir force-app
sf org login web --alias mydev
sf data query --query "SELECT Id, Name FROM Account"
sf org open

# ❌ WRONG - Legacy sfdx (deprecated)
sfdx force:source:deploy -p force-app
sfdx force:auth:web:login -a mydev
```

## Development Deployment Workflows

### Quick Iteration Loop (LWC, Visualforce, Aura)

**For front-end components that need testing in the org:**

```bash
# 1. Deploy changes
sf project deploy start --source-dir force-app/main/default/lwc/myComponent

# 2. Open org to test
sf org open --target-org mydev

# 3. Test your changes in browser

# 4. Make adjustments and repeat
```

**No tests needed** - Front-end components don't require Apex tests.

### Apex Deployment with Test Options

**When deploying Apex classes or triggers, ASK the user about testing:**

**Prompt:** "Would you like to run tests with this Apex deployment?"

**Option 1: No tests (fastest - 1-2 minutes)**
```bash
sf project deploy start \
  --source-dir force-app \
  --test-level NoTestRun

# Best for: rapid iteration, syntax fixes, development sandboxes
```

**Option 2: Specific test classes (moderate - 2-10 minutes)**
```bash
sf project deploy start \
  --source-dir force-app \
  --test-level RunSpecifiedTests \
  --tests AccountServiceTest \
  --tests ContactTriggerHandlerTest

# Best for: testing specific functionality you changed
```

**Option 3: All local tests (slow - 15-60+ minutes)**

⚠️ **WARN USER FIRST:**
```
Running all local tests can take a long time (15-60+ minutes depending on org size).
Continue with RunLocalTests? (yes/no)
```

If user confirms:
```bash
# Start deployment with all tests
DEPLOY_ID=$(sf project deploy start \
  --source-dir force-app \
  --test-level RunLocalTests \
  --json | jq -r '.result.id')

echo "Deployment ID: $DEPLOY_ID"
echo "⏳ Running all tests... this may take 15-60+ minutes"
echo "💡 To cancel: sf project deploy cancel --job-id $DEPLOY_ID"

# Monitor progress
sf project deploy resume --job-id $DEPLOY_ID --wait 60
```

### Monitoring Long-Running Deployments

**For deployments that take time:**

```bash
# Check status without waiting
sf project deploy report --job-id <deployment-id>

# Resume waiting (if interrupted)
sf project deploy resume --job-id <deployment-id> --wait 30

# Cancel if taking too long
sf project deploy cancel --job-id <deployment-id>
```

**Status indicators:**
- `InProgress` - Still running
- `Succeeded` - Completed successfully
- `Failed` - Deployment failed
- `Canceled` - User canceled deployment

## Deployment Scenarios

### Deploy Specific Components

```bash
# Single LWC component
sf project deploy start \
  --source-dir force-app/main/default/lwc/accountList

# Single Apex class and its test
sf project deploy start \
  --metadata ApexClass:AccountService \
  --metadata ApexClass:AccountServiceTest

# Custom object with fields
sf project deploy start \
  --source-dir force-app/main/default/objects/CustomObject__c

# Multiple metadata types
sf project deploy start \
  --metadata ApexClass:AccountService \
  --metadata ApexTrigger:AccountTrigger \
  --test-level NoTestRun
```

### Deploy Entire Project

```bash
# Deploy all source
sf project deploy start --source-dir force-app

# Deploy with test validation
sf project deploy start \
  --source-dir force-app \
  --test-level RunLocalTests
```

### Preview What Will Deploy

```bash
# See what would be deployed (dry run)
sf project deploy start --source-dir force-app --dry-run

# Preview changes
sf project deploy preview --source-dir force-app
```

## Org Management

### Authentication

```bash
# Login to sandbox (interactive)
sf org login web --alias mydev --instance-url https://test.salesforce.com

# Login to production
sf org login web --alias prod --instance-url https://login.salesforce.com

# Login to custom domain
sf org login web --alias myorg --instance-url https://mycompany.my.salesforce.com

# List authenticated orgs
sf org list

# Open org in browser
sf org open --target-org mydev

# Set default org
sf config set target-org=mydev
```

### Scratch Orgs

```bash
# Create scratch org
sf org create scratch \
  --definition-file config/project-scratch-def.json \
  --alias scratch-dev \
  --duration-days 7 \
  --set-default

# Push source to scratch org (source tracking)
sf project deploy start --source-dir force-app

# Open scratch org
sf org open

# Delete scratch org
sf org delete scratch --target-org scratch-dev --no-prompt
```

## Running Tests Separately

**After deploying without tests, run tests independently:**

```bash
# Run specific test class
sf apex run test \
  --tests AccountServiceTest \
  --result-format human \
  --code-coverage

# Run multiple test classes
sf apex run test \
  --tests AccountServiceTest,ContactHandlerTest \
  --result-format human

# Run all tests in org
sf apex run test \
  --test-level RunLocalTests \
  --result-format human \
  --code-coverage \
  --wait 60

# Get test results with coverage
sf apex get test \
  --test-run-id <test-run-id> \
  --code-coverage \
  --result-format human
```

## Post-Deployment Workflow

### After Successful Deployment

**When deployment succeeds, guide user:**

```
✅ Deployment successful!

Next steps:
1. Test your changes: sf org open --target-org mydev
2. [If git detected] Commit your changes? (yes/no)
```

**If user wants to commit (and git is available):**
```bash
# Check git status
git status

# Stage changes
git add force-app/

# Commit
git commit -m "Description of changes"

# Push (optional)
git push origin feature-branch
```

## Retrieving Metadata from Org

**Pull changes from org to local project:**

```bash
# Retrieve specific metadata
sf project retrieve start --metadata ApexClass:AccountService

# Retrieve by source directory
sf project retrieve start --source-dir force-app

# Retrieve using manifest
sf project retrieve start --manifest package.xml

# Preview what would be retrieved
sf project retrieve preview
```

## Data Operations

### Query Data

```bash
# Simple query
sf data query --query "SELECT Id, Name FROM Account LIMIT 10"

# Query to file
sf data query \
  --query "SELECT Id, Name, Industry FROM Account" \
  --result-format csv > accounts.csv

# Use SOQL file
sf data query --file query.soql
```

### Import/Export Data

```bash
# Export with related records
sf data export tree \
  --query "SELECT Id, Name, (SELECT Id, FirstName FROM Contacts) FROM Account" \
  --output-dir data \
  --plan

# Import data
sf data import tree --plan data/plan.json

# Import CSV
sf data import csv --file accounts.csv --sobject Account
```

## Common Development Patterns

### LWC Development Loop

```bash
# 1. Make changes to LWC component
# (edit HTML, JS, CSS files)

# 2. Deploy component
sf project deploy start \
  --source-dir force-app/main/default/lwc/myComponent

# 3. Open org and test
sf org open

# 4. Check browser console for errors
# 5. Make fixes and repeat
```

### Apex Development Loop

```bash
# 1. Write/modify Apex class and test

# 2. Deploy without tests (fast iteration)
sf project deploy start \
  --metadata ApexClass:MyClass \
  --metadata ApexClass:MyClassTest \
  --test-level NoTestRun

# 3. Run tests separately
sf apex run test \
  --tests MyClassTest \
  --result-format human \
  --code-coverage

# 4. Review results and iterate
```

### Custom Object Changes

```bash
# 1. Modify object fields, validation rules, etc.

# 2. Deploy object
sf project deploy start \
  --source-dir force-app/main/default/objects/MyObject__c

# 3. Test in org
sf org open

# 4. Verify fields, page layouts, etc.
```

## Troubleshooting Development Deployments

### Deployment Failed

```bash
# Get detailed error report
sf project deploy report --job-id <deployment-id> --verbose

# Check for common issues:
# - Missing dependencies (deploy parent objects first)
# - Field references that don't exist
# - Validation rule conflicts
# - Test failures (if running tests)
```

### Test Failures

```bash
# View test failure details
sf project deploy report --job-id <deployment-id>

# Run failed test individually
sf apex run test \
  --tests FailedTestClass \
  --result-format human

# Check test coverage
sf apex get test --code-coverage --result-format human
```

### Dependency Issues

```bash
# Deploy in order:
# 1. Objects
sf project deploy start --metadata CustomObject

# 2. Fields
sf project deploy start --metadata CustomField

# 3. Apex
sf project deploy start --metadata ApexClass

# 4. Triggers
sf project deploy start --metadata ApexTrigger
```

### Long-Running Deployment

```bash
# Check progress
sf project deploy report --job-id <deployment-id>

# If stuck or taking too long, cancel
sf project deploy cancel --job-id <deployment-id>

# Then deploy without tests or with fewer tests
sf project deploy start \
  --source-dir force-app \
  --test-level NoTestRun
```

## Key Development Reminders

1. **Use `deploy report` to check status** - Never use `deploy start` for status checks
2. **Cancel long deployments** - Use `deploy cancel` if needed
3. **NoTestRun for iteration** - Skip tests during rapid development
4. **Test separately** - Run tests after deployment for faster feedback
5. **Open org to test** - Use `sf org open` after deployment
6. **Deploy specific components** - Faster than deploying entire project
7. **Preview before deploy** - Use `--dry-run` to check what will deploy
8. **No git requirements** - Commit only when ready, not before deployment
9. **Warn for long tests** - Alert user before running all local tests
10. **Monitor progress** - Check status periodically for long deployments

## Time Estimates

- **LWC/Visualforce deployment**: 30 seconds - 2 minutes
- **Apex without tests**: 1-2 minutes
- **Apex with specific tests**: 2-10 minutes
- **Apex with all local tests**: 15-60+ minutes (warn user!)
- **Large metadata deployments**: 5-15 minutes

## Quick Command Reference

### Deploy
- `sf project deploy start --source-dir <dir>` - Deploy source
- `sf project deploy start --metadata <type>:<name>` - Deploy specific metadata
- `sf project deploy start --dry-run` - Preview deployment
- `sf project deploy report --job-id <id>` - Check status
- `sf project deploy resume --job-id <id>` - Resume waiting
- `sf project deploy cancel --job-id <id>` - Cancel deployment

### Org
- `sf org login web --alias <name>` - Login to org
- `sf org open` - Open org in browser
- `sf org list` - List orgs
- `sf org display` - Show org info

### Test
- `sf apex run test --tests <class>` - Run tests
- `sf apex get test --code-coverage` - Get coverage

### Data
- `sf data query --query <soql>` - Query data
- `sf org open` - Open org to test UI changes

---

**Focus**: Development iteration and testing
**NOT included**: Production deployments, CI/CD, environment migrations
**Created for**: Claude Code
**Last Updated**: November 2025
