---
name: github-actions-cicd
description: GitHub Actions workflow structure, security scanning integration (CodeQL, ZAP), Lighthouse audits, minification, and deployment automation
license: Apache-2.0
---

# GitHub Actions CI/CD Skill

## Purpose

Defines CI/CD pipeline best practices using GitHub Actions for automated testing, security scanning, and deployment.

## Rules

### Workflow Structure

**MUST INCLUDE:**
1. Code quality checks (linting, formatting)
2. Security scanning (CodeQL, Dependabot, ZAP)
3. Performance audits (Lighthouse)
4. Build and minification
5. Deployment (with approval for production)

**Example Workflow:**
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read
  security-events: write

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate HTML
        run: npm run validate:html
      - name: Lint CSS
        run: npm run lint:css

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.10.0
        with:
          target: 'https://www.hack23.com'

  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Lighthouse
        uses: treosh/lighthouse-ci-action@v10
        with:
          urls: |
            https://www.hack23.com/
            https://www.hack23.com/services.html
          budgetPath: ./budget.json
          uploadArtifacts: true

  deploy:
    needs: [validate, security-scan, lighthouse]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1
      - name: Sync to S3
        run: aws s3 sync . s3://${{ secrets.S3_BUCKET }} --delete
      - name: Invalidate CloudFront
        run: aws cloudfront create-invalidation --distribution-id ${{ secrets.CF_DIST_ID }} --paths "/*"
```

### Security Best Practices

**MUST:**
- Use OIDC for AWS authentication (no long-lived keys)
- Store secrets in GitHub Secrets
- Use least-privilege IAM roles
- Pin action versions with full commit SHA
- Enable Dependabot for action updates
- Use `permissions` key to minimize token scope

**MUST NOT:**
- Commit secrets to repository
- Use personal access tokens in workflows
- Grant overly broad permissions

## Related Documentation

- [aws-s3-cloudfront SKILL.md](../aws-s3-cloudfront/SKILL.md)
- [secure-development SKILL.md](../../security/secure-development/SKILL.md)
