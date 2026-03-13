---
name: gh-oss-release-prep
description: >
  Systematic OSS release preparation checklist. Use when preparing a repository for open-source publishing,
  making a project public, or ensuring a repo meets OSS standards.
  Triggers: "prepare for OSS", "ready to publish", "make this public", "OSS checklist",
  "scan repo for publish", "open source this", "/oss-release-prep"
compatibility: Requires git and language-specific linters
metadata:
  author: jackchuka
  scope: generic
---

# OSS Release Preparation

Systematic workflow to prepare a repository for open-source publishing. Covers code quality, licensing, documentation, and release readiness.

## Workflow

### Step 1: Repository Scan

Scan the entire repository to understand its current state:

1. Read the project structure (directories, key files)
2. Check for existing README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT
3. Identify the primary language and build system
4. Check for any sensitive files (.env, credentials, API keys, internal URLs)
5. Review .gitignore for completeness

Report findings as a checklist:

```
Repository Scan:
- [x/!] README.md exists
- [x/!] LICENSE file exists
- [x/!] .gitignore is comprehensive
- [x/!] No sensitive files detected
- [x/!] No hardcoded internal URLs or secrets
```

### Step 2: License & Dependency Audit

1. Identify the intended license (ask user if not specified, default suggestion: MIT)
2. Check all dependencies for license compatibility:
   - Direct dependencies: list each with its license
   - Flag any copyleft (GPL, AGPL) dependencies that conflict with the chosen license
3. If attribution is required, create or update a NOTICES file
4. Verify the LICENSE file content is correct and includes the current year

### Step 3: README Quality Check

Evaluate and improve the README:

1. **Required sections** (create if missing):
   - Project name and tagline (concise, memorable)
   - What it does (1-2 sentences)
   - Installation instructions
   - Quick start / basic usage
   - License

2. **Recommended sections** (suggest if missing):
   - Features list
   - Configuration options
   - Contributing guidelines (or link to CONTRIBUTING.md)
   - Badges (CI status, license, version)

3. **Quality checks**:
   - Does the README match the actual CLI/API interface?
   - Are code examples up to date and runnable?
   - Is the installation method documented correctly?

4. **Tagline**: If the project lacks a compelling tagline, propose 3-5 options that are:
   - Short (under 10 words)
   - Descriptive of the core value
   - Memorable

### Step 4: Code Quality Review

1. Run available linters and fix issues:
   - Go: `golangci-lint run ./...`
   - Node/TS: check `package.json` scripts for lint commands
2. Check for dead code using available tools (e.g., `deadcode ./...` for Go)
3. Ensure public API documentation exists (exported functions/types have comments)
4. Remove TODO/FIXME comments that reference internal context
5. Verify test coverage is reasonable for public consumption

### Step 5: Release Readiness Checklist

Present the final checklist:

```
OSS Release Readiness:
- [ ] LICENSE file is correct and complete
- [ ] All dependency licenses are compatible
- [ ] README is comprehensive and accurate
- [ ] No secrets, internal URLs, or sensitive data in code
- [ ] .gitignore covers build artifacts, IDE files, OS files
- [ ] CI/CD pipeline exists (GitHub Actions, etc.)
- [ ] Tests pass
- [ ] Linter passes with no errors
- [ ] Version/tag strategy defined (semver)
- [ ] Release automation configured (goreleaser, npm publish, etc.)
```

For each unchecked item, provide the specific fix needed.

### Step 6: Final Actions

1. If all checks pass, confirm with user before any publishing steps
2. Suggest the release workflow:
   - Create initial release tag
   - Publish to package registry if applicable
   - Submit to relevant directories (Homebrew tap, npm, etc.)

## Common Issues

- **Goreleaser not configured**: Create `.goreleaser.yaml` for Go projects
- **Missing .gitignore entries**: Add OS-specific (`.DS_Store`), IDE-specific (`.vscode/`, `.idea/`), and language-specific entries
- **Internal references**: Search for company-internal URLs, Slack channels, or employee names in code and docs
- **Inconsistent naming**: Ensure the project name is consistent across README, package.json/go.mod, and CLI help text

## Examples

**Example 1: Go CLI tool**

```
User: "prepare this for OSS"
Action:
1. Scan repo structure
2. Check go.mod dependencies for license compatibility
3. Ensure README matches `--help` output
4. Run golangci-lint, fix issues
5. Verify goreleaser config exists
6. Present checklist
```

**Example 2: Node.js library**

```
User: "make this repo public"
Action:
1. Scan for .env files, hardcoded URLs
2. Check package.json dependencies' licenses
3. Ensure README has install/usage/API docs
4. Run configured lint/test scripts
5. Verify npm publish config
6. Present checklist
```
