---
name: github-actions-workflows
description: GitHub Actions workflow patterns for static site CI/CD, security scanning, and quality checks
license: Apache-2.0
---

# GitHub Actions Workflows

## Purpose

Optimize GitHub Actions workflows for Riksdagsmonitor's static site CI/CD pipeline.

## Core Patterns

### Quality Checks Workflow
```yaml
name: Quality Checks

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # HTML validation
      - name: Validate HTML
        run: |
          npm install -g htmlhint
          htmlhint *.html
      
      # Link checking
      - name: Check Links
        run: |
          npm install -g linkinator
          python3 -m http.server 8080 &
          sleep 5
          linkinator http://localhost:8080/ --recurse
```

### Security Scanning
```yaml
name: Security

on: [push, pull_request]

permissions:
  security-events: write

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # CodeQL
      - uses: github/codeql-action/init@v3
        with:
          languages: javascript
      
      - uses: github/codeql-action/analyze@v3
      
      # Dependency check
      - name: Dependency Scan
        uses: dependency-check/Dependency-Check_Action@main
```

### Deployment Workflow
```yaml
name: Deploy

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

## Best Practices

- ✅ Minimal permissions (least privilege)
- ✅ Pin actions to SHA (supply chain security)
- ✅ Cache dependencies (faster builds)
- ✅ Parallel jobs (faster feedback)
- ✅ Matrix testing (cross-browser)

## References

- **GitHub Actions**: https://docs.github.com/en/actions
- **Workflow Files**: `.github/workflows/`
