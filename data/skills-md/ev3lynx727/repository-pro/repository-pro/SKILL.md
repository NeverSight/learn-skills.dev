---
name: repository-pro
description: "Create professional, well-structured GitHub repositories with industry best practices. Use when: (1) Creating new GitHub repositories, (2) Setting up repository structure, (3) Adding essential files (README, LICENSE, .gitignore), (4) Configuring CI/CD workflows, (5) Setting up contribution guidelines, (6) Adding issue/PR templates, (7) Configuring branch protection rules, (8) Setting description and topics for discoverability, (9) Identifying tech stack and applying appropriate templates (React, Next.js, Django, FastAPI, Go, MERN, T3, etc.)"
license: MIT
metadata:
  version: "0.1.2"
  author: repository-pro
  tags: [github, repository, best-practices, ci-cd, github-actions, devops]
allowed-tools:
  - github_*
---

# Repository Pro

Create production-ready GitHub repositories with professional structure and best practices.

## Core Principles

1. **Every repo needs a README** - First thing users see, explains project purpose and usage
2. **License matters** - Define open source terms from day one
3. **.gitignore from start** - Avoid committing sensitive files
4. **CI/CD from day one** - Automated testing and checks
5. **Contribution clarity** - Guidelines for collaborators
6. **Issue templates** - Standardize bug reports and feature requests
7. **Security scanning** - Enable Dependabot, code scanning

## Repository Structure

### Universal Files (Every Project)

```
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── LICENSE
├── README.md
└── CONTRIBUTING.md
```

### Language-Specific Structure

**Node.js/TypeScript:**
```
├── src/
├── test/
├── package.json
├── tsconfig.json
├── .eslintrc.json
├── .prettierrc
└── jest.config.js
```

**Python:**
```
├── src/
├── tests/
├── pyproject.toml
├── setup.py
├── .flake8
├── mypy.ini
└── requirements.txt
```

**Go:**
```
├── cmd/
├── pkg/
├── internal/
├── go.mod
├── .golangci.yml
└── Makefile
```

## Essential Files

### README.md Structure

```markdown
# Project Name

Brief description (1-2 sentences)

[![CI](badge-url)](link)
[![License](badge-url)](link)
[![Version](badge-url)](link)

## Features

- Feature 1
- Feature 2

## Quick Start

\`\`\`bash
# Installation
npm install package-name
\`\`\`

## Usage

\`\`\`javascript
const example = require('package-name');
\`\`\`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License - see [LICENSE](LICENSE)
```

### .gitignore Templates

Use appropriate template from [github/gitignore](https://github.com/github/gitignore)

### CONTRIBUTING.md

```markdown
# Contributing

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch

## Development

\`\`\`bash
# Install dependencies
npm install

# Run tests
npm test
\`\`\`

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md

## Code Style

- Use consistent formatting
- Write meaningful commit messages
- Follow existing code patterns
```

### Issue Templates

**Bug Report:**
```markdown
---
name: Bug Report
about: Create a report to help us improve
---

## Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- OS: [e.g., macOS]
- Version: [e.g., 1.0.0]
```

**Feature Request:**
```markdown
---
name: Feature Request
about: Suggest an idea for this project
---

## Problem
What problem does this solve?

## Proposed Solution
Your proposed solution

## Alternatives
Other solutions considered
```

## CI/CD Workflows

### Basic CI Workflow

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Use Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
```

### Node.js with Coverage

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v4
```

## Repository Metadata

### Description Best Practices

A good GitHub description:
- **Max 160 characters** - Displayed in search results
- **Starts with action verb** - "A", "An", "Build", "Create", "Simple"
- **Explains what it does** - Not just "parser" but "parses JSON into TypeScript types"
- **Includes primary benefit** - What problem does it solve?

| Type | Template | Example |
|------|----------|---------|
| Library | "A [language] library for [action]" | "A Python library for building CLI applications" |
| CLI | "CLI tool to [action]" | "CLI tool to convert video to GIF" |
| Web App | "[What] built with [framework]" | "Task manager built with React and Node.js" |
| API | "REST API for [domain]" | "REST API for managing todo lists" |
| Config | "[Name] config for [purpose]" | "Docker configs for Node.js microservices" |

### Topics Best Practices

GitHub topics help with discoverability:
- **Use lowercase** - `machine-learning`, not `Machine-Learning`
- **Max 20 topics** - GitHub limit
- **Include ecosystem** - `react`, `python`, `golang`
- **Include category** - `cli`, `api`, `library`, `tool`
- **Add status** - `beta`, `stable`, `deprecated`
- **Include type** - `starter-template`, `boilerplate`

### Recommended Topic Categories

| Category | Topics |
|----------|--------|
| **Language** | javascript, typescript, python, go, rust, java, kotlin |
| **Framework** | react, vue, angular, nextjs, django, fastapi, express |
| **Type** | library, cli, api, webapp, boilerplate, starter-template |
| **Purpose** | automation, machine-learning, data-visualization, security |
| **Features** | graphql, rest-api, websocket, serverless, docker |

See [references/topics.md](references/topics.md) for comprehensive topic lists by project type.

### Branch Protection Rules

For `main` branch:
- Require pull request reviews (1-2 reviewers)
- Require status checks to pass
- Require branches to be up to date
- Include administrators in protections

### Dependabot Configuration

```yaml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
```

## Repository Creation Workflow

1. **Plan metadata** - Write description (max 160 chars) and select relevant topics
2. **Create repository** using `github_create_repository` with description and topics
3. **Push initial commit** with:
   - README.md
   - LICENSE
   - .gitignore
   - CONTRIBUTING.md
   - .github/ISSUE_TEMPLATE/
   - .github/PULL_REQUEST_TEMPLATE.md
   - .github/workflows/ci.yml
4. **Enable security features** (Dependabot, code scanning)

## Common Tasks

### Create new repository with full structure

```python
# 1. Plan metadata
# Description: "CLI tool to convert video to GIF with optimal compression"
# Topics: ["cli", "golang", "video", "gif", "converter", "ffmpeg"]

# 2. Create repository
github_create_repository(
    name="video-to-gif",
    description="CLI tool to convert video to GIF with optimal compression",
    private=False,
    autoInit=True
)

# 3. Push files using github_push_files
# Include all essential files in initial commit
```

### Add workflow to existing repo

```python
github_create_or_update_file(
    owner="username",
    repo="repository",
    path=".github/workflows/ci.yml",
    content=workflow_yaml,
    message="Add CI workflow",
    branch="main"
)
```

## Project Type Recommendations

| Type | Key Files | CI Focus |
|------|-----------|----------|
| Library | package.json, tsconfig, README | Test + Lint + Publish |
| CLI | package.json, Makefile, README | Test + Build + Release |
| Web App | package.json, Dockerfile, README | Test + Build + Deploy |
| API | OpenAPI spec, Dockerfile, README | Test + Security Scan |
| Data Science | notebooks/, requirements.txt | Notebook linting, Tests |

## Quick Checklist

Before marking repository as "production-ready":

- [ ] README clearly explains project purpose
- [ ] LICENSE file present and appropriate
- [ ] .gitignore excludes sensitive files
- [ ] CI/CD workflow runs tests
- [ ] Issue templates configured
- [ ] PR template configured
- [ ] CONTRIBUTING.md explains how to contribute
- [ ] Dependabot configured (for dependencies)
- [ ] Branch protection enabled on main
- [ ] Description is clear and descriptive (max 160 chars)
- [ ] Topics include relevant language, framework, and category tags

- [GitHub Best Practices](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories)
- [Gitignore Templates](https://github.com/github/gitignore)
- [Choose a License](https://choosealicense.com)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## Tech Stack Knowledge

This skill recognizes common technology stacks and knows how to structure repositories for each.

### Recognized Tech Stacks

The skill automatically identifies these stacks and applies appropriate templates:

| Stack | Keywords | Structure |
|-------|----------|-----------|
| **Node.js/Express** | express, nodejs | src/, routes/, middleware/, test/ |
| **React** | react, create-react-app | src/components/, src/hooks/, src/pages/ |
| **Next.js** | nextjs, next.js | app/, pages/, components/ |
| **Vue** | vue, vuejs, nuxt | components/, pages/, stores/ |
| **Django** | django | project/, apps/, templates/ |
| **FastAPI** | fastapi | app/, api/, models/ |
| **Flask** | flask | app/, routes/, models/ |
| **Go/Gin** | gin, golang | cmd/, internal/, pkg/ |
| **Rust** | rust, cargo | src/, tests/, examples/ |
| **Python/ML** | pytorch, tensorflow, ml | notebooks/, models/, data/ |

### Stack Detection

When user provides a project idea, identify the stack from:
1. Explicit mention: "I want a React app"
2. Keywords in description: "API", "bot", "CLI"
3. File types: .jsx, .py, .go, .rs

### Stack-Specific Configuration

For each detected stack, automatically apply:

- **Language config**: tsconfig.json, pyproject.toml, go.mod
- **Linting config**: ESLint, ruff, golangci-lint
- **Testing config**: Jest, pytest, go test
- **CI workflow**: Stack-appropriate action versions
- **Dependencies**: Package manager (npm, pip, go mod, cargo)

### Common Stacks with Templates

#### MERN Stack (MongoDB, Express, React, Node)

```
├── backend/
│   ├── src/
│   │   ├── routes/
│   │   ├── models/
│   │   ├── controllers/
│   │   └── config/
│   ├── package.json
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── services/
│   ├── package.json
│   └── .env.example
└── docker-compose.yml
```

**Topics**: `mern, mongodb, express, react, nodejs, rest-api`

#### T3 Stack (Next.js, tRPC, TypeScript, Tailwind)

```
├── src/
│   ├── server/
│   │   ├── routers/
│   │   └── trpc.ts
│   ├── pages/
│   ├── components/
│   ├── styles/
│   └── utils/
├── prisma/
│   └── schema.prisma
├── next.config.js
├── tailwind.config.ts
└── tsconfig.json
```

**Topics**: `nextjs, trpc, typescript, tailwind, prisma, fullstack`

#### Serverless Stack (AWS Lambda)

```
├── src/
│   ├── handlers/
│   └── utils/
├── serverless.yml
├── webpack.config.js
├── jest.config.js
└── tsconfig.json
```

**Topics**: `serverless, aws-lambda, aws, serverless-framework, typescript`

#### Data Engineering Stack

```
├── dags/              # Airflow DAGs
├── scripts/           # ETL scripts
├── notebooks/         # Jupyter notebooks
├── src/               # Python packages
├── tests/
├── requirements.txt
├── setup.py
└── docker-compose.yml
```

**Topics**: `data-engineering, airflow, etl, python, apache-spark, docker`

### Stack-Specific CI

| Stack | CI Focus |
|-------|----------|
| Frontend | Build, lint, test, Lighthouse audit |
| Backend | Build, test, security scan, coverage |
| Fullstack | Frontend + Backend + integration tests |
| Data | Notebook linting, data validation, tests |
| Infrastructure | Terraform validation, Ansible lint |

See [references/stacks.md](references/stacks.md) for detailed configurations.
