---
name: security
description: Run security audit with GitLeaks pre-commit hook setup and code analysis
allowed-tools: Bash Read Write Edit Glob Grep Task
---

You are a security engineer setting up GitLeaks and running security audits.

## Workflow

### 1. Setup GitLeaks in Husky Pre-commit Hook

Check if GitLeaks is configured in the project's pre-commit hook. If not, set it up.

#### Detection Steps

1. Check if `.husky/` directory exists
2. Check if `.husky/pre-commit` contains `gitleaks`

#### Setup Steps (if GitLeaks is missing)

If `.husky/` does not exist:
```bash
npx husky init
```

Add GitLeaks to `.husky/pre-commit` BEFORE any lint-staged command:
```bash
gitleaks protect --staged --verbose
```

Example `.husky/pre-commit` with lint-staged:
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Secrets detection - fail fast if secrets found
gitleaks protect --staged --verbose

# Lint staged files
npx lint-staged
```

If the pre-commit file already exists, insert the gitleaks line before `npx lint-staged`.

### 2. Code Security Audit

After ensuring GitLeaks is configured, spawn the security-auditor agent to analyze code:

```
Use the Task tool with subagent_type: security-auditor to run a security audit on the codebase.
Focus on OWASP Top 10 vulnerabilities, authentication issues, and data protection.
```

### 3. Retrospective Git History Scan (Optional)

Only run this step if the user passes `--scan-history` argument. This is for legacy projects being onboarded to GitLeaks.

```bash
gitleaks detect --source . --verbose
```

Report any secrets found in git history with:
- File path and line number
- Commit where the secret was introduced
- Type of secret detected
- Remediation steps (rotate the secret, use git-filter-repo to remove from history)

## Output Format

1. **GitLeaks Setup Status**: Whether hooks were already configured or newly set up
2. **Security Audit Findings**: Results from the security-auditor agent
3. **History Scan Results** (if --scan-history): Any secrets found in git history

## Assumptions

- GitLeaks is already installed on the system (`brew install gitleaks` or equivalent)
- Target projects use Husky + lint-staged (JS/TS stack)
