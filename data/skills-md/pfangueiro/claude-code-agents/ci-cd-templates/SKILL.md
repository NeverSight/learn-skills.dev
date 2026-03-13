---
name: ci-cd-templates
description: Production-ready CI/CD pipeline templates for GitHub Actions, GitLab CI, and CircleCI
---

# CI/CD Templates Skill

Provides production-ready CI/CD pipeline templates for GitHub Actions, GitLab CI, and CircleCI.

## Purpose

This skill provides:
- GitHub Actions workflow templates
- GitLab CI/CD pipeline configurations
- CircleCI config examples
- Best practices for automated testing, building, and deployment
- Security scanning integration
- Deployment strategies (blue/green, canary, rolling)

## When to Use

- "Create a CI/CD pipeline for Node.js"
- "Add GitHub Actions for testing and deployment"
- "Set up automated deployments to AWS"
- "Configure GitLab CI for Docker builds"

## GitHub Actions Templates

### Node.js CI/CD Pipeline

```yaml
name: Node.js CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
    - uses: actions/checkout@v4

    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Run linter
      run: npm run lint

    - name: Run tests
      run: npm test

    - name: Upload coverage
      uses: codecov/codecov-action@v4
      if: matrix.node-version == '20.x'
      with:
        token: ${{ secrets.CODECOV_TOKEN }}

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Run Snyk security scan
      uses: snyk/actions/node@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

    - name: Run npm audit
      run: npm audit --production

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v4

    - name: Build Docker image
      run: docker build -t myapp:${{ github.sha }} .

    - name: Log in to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Push Docker image
      run: |
        docker tag myapp:${{ github.sha }} myapp:latest
        docker push myapp:${{ github.sha }}
        docker push myapp:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - name: Deploy to production
      uses: appleboy/ssh-action@v1.0.0
      with:
        host: ${{ secrets.DEPLOY_HOST }}
        username: ${{ secrets.DEPLOY_USER }}
        key: ${{ secrets.DEPLOY_KEY }}
        script: |
          docker pull myapp:latest
          docker-compose up -d
```

### TypeScript + Vitest Pipeline

```yaml
name: TypeScript CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'

    - run: npm ci

    - name: Type check
      run: npm run type-check

    - name: Run tests with coverage
      run: npm run test:coverage

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v4
```

## GitLab CI Templates

### Full-Stack Application Pipeline

```yaml
stages:
  - build
  - test
  - security
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

build:
  stage: build
  image: node:20-alpine
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

test:unit:
  stage: test
  image: node:20-alpine
  script:
    - npm ci
    - npm run test:coverage
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

test:e2e:
  stage: test
  image: mcr.microsoft.com/playwright:v1.40.0
  script:
    - npm ci
    - npx playwright install
    - npm run test:e2e
  artifacts:
    when: on_failure
    paths:
      - playwright-report/

security:sast:
  stage: security
  image: returntocorp/semgrep
  script:
    - semgrep --config=auto --json --output=semgrep.json .
  artifacts:
    reports:
      sast: semgrep.json

security:dependency:
  stage: security
  image: node:20-alpine
  script:
    - npm audit --json > npm-audit.json
  artifacts:
    reports:
      dependency_scanning: npm-audit.json

deploy:staging:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache curl
  script:
    - curl -X POST $DEPLOY_WEBHOOK_STAGING
  only:
    - develop

deploy:production:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache curl
  script:
    - curl -X POST $DEPLOY_WEBHOOK_PRODUCTION
  only:
    - main
  when: manual
```

## Deployment Strategies

### Blue/Green Deployment (AWS)

```yaml
name: Blue/Green Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1

    - name: Deploy to green environment
      run: |
        aws deploy create-deployment \
          --application-name my-app \
          --deployment-group-name green-env \
          --s3-location bucket=my-bucket,key=app.zip,bundleType=zip

    - name: Run smoke tests
      run: ./scripts/smoke-test.sh https://green.example.com

    - name: Switch traffic to green
      run: |
        aws elbv2 modify-listener \
          --listener-arn ${{ secrets.LISTENER_ARN }} \
          --default-actions TargetGroupArn=${{ secrets.GREEN_TARGET_GROUP }}

    - name: Monitor deployment
      run: ./scripts/monitor-metrics.sh
```

### Canary Deployment (Kubernetes)

```yaml
name: Canary Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up kubectl
      uses: azure/setup-kubectl@v3

    - name: Deploy canary (10% traffic)
      run: |
        kubectl apply -f k8s/canary-10.yaml
        kubectl rollout status deployment/app-canary

    - name: Monitor metrics for 10 minutes
      run: ./scripts/monitor-canary.sh 600

    - name: Increase to 50% traffic
      run: kubectl apply -f k8s/canary-50.yaml

    - name: Monitor metrics for 10 minutes
      run: ./scripts/monitor-canary.sh 600

    - name: Full rollout
      run: |
        kubectl apply -f k8s/production.yaml
        kubectl delete -f k8s/canary-50.yaml
```

## Best Practices

1. **Always run tests before deployment**
2. **Use matrix builds for multiple environments**
3. **Implement security scanning (SAST, dependency checks)**
4. **Cache dependencies to speed up builds**
5. **Use secrets for sensitive data**
6. **Implement rollback strategies**
7. **Monitor deployments with health checks**
8. **Use environment-specific configurations**

## Integration with Agents

Works best with:
- **devops-automation** agent - Generates pipelines for specific platforms
- **security-auditor** agent - Adds security scanning steps
- **test-automation** agent - Integrates testing frameworks

## References

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [GitLab CI/CD](https://docs.gitlab.com/ee/ci/)
- [CircleCI Documentation](https://circleci.com/docs/)
