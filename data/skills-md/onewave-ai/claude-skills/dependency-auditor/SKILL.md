---
name: dependency-auditor
description: Audit npm dependencies for security vulnerabilities, outdated packages, and unused dependencies. Use when checking for security issues, updating packages, or cleaning up dependencies.
---

# Dependency Auditor

## Instructions

When auditing dependencies:

1. **Run security audit**
2. **Check for outdated packages**
3. **Find unused dependencies**
4. **Analyze bundle size impact**
5. **Review and update**

## Security Audit

```bash
# NPM audit
npm audit

# Get JSON output for processing
npm audit --json

# Fix automatically (safe fixes only)
npm audit fix

# Force fix (may have breaking changes)
npm audit fix --force

# PNPM
pnpm audit

# Yarn
yarn audit
```

## Check Outdated Packages

```bash
# NPM
npm outdated

# Interactive update
npx npm-check-updates -i

# Update all to latest
npx npm-check-updates -u
npm install

# Check specific package
npm view <package> versions
```

## Find Unused Dependencies

```bash
# Using depcheck
npx depcheck

# With details
npx depcheck --detailed

# Ignore patterns
npx depcheck --ignores="@types/*,eslint-*"
```

### Common False Positives

Depcheck may flag these as unused when they're actually needed:
- `@types/*` packages (used by TypeScript)
- ESLint/Prettier plugins (referenced in config)
- PostCSS plugins (referenced in config)
- Next.js plugins
- Babel presets

## Analyze Bundle Size

```bash
# For Next.js
npx @next/bundle-analyzer

# General purpose
npx source-map-explorer dist/**/*.js

# Check package size before installing
npx package-phobia <package-name>

# Compare alternatives
npx bundlephobia-cli compare lodash ramda
```

## Dependency Review Checklist

### Security
- [ ] No critical/high vulnerabilities
- [ ] Dependencies actively maintained
- [ ] No known malicious packages
- [ ] Lock file committed

### Freshness
- [ ] No major version behind (unless intentional)
- [ ] Security patches applied
- [ ] Deprecated packages replaced

### Cleanliness
- [ ] No unused dependencies
- [ ] No duplicate packages (check lock file)
- [ ] devDependencies vs dependencies correct

## Update Strategies

### Conservative (Recommended)

```bash
# Update patch versions only
npm update

# Update specific package
npm install package@latest
```

### Aggressive

```bash
# Update everything
npx npm-check-updates -u
npm install
npm test
```

### Interactive

```bash
npx npm-check-updates -i

# Options:
# a - update all
# space - toggle selection
# enter - apply selected
```

## Package.json Cleanup

```json
{
  "dependencies": {
    // Runtime dependencies only
  },
  "devDependencies": {
    // Build/test tools only
  },
  "peerDependencies": {
    // For libraries only
  },
  "optionalDependencies": {
    // Platform-specific (rare)
  }
}
```

## Lock File Best Practices

1. **Always commit** lock files (package-lock.json, pnpm-lock.yaml, yarn.lock)
2. **Use `npm ci`** in CI/CD (not `npm install`)
3. **Regenerate** if corrupted: delete lock file + node_modules, reinstall
4. **Single lock file** per project (don't mix package managers)

## Automated Monitoring

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    groups:
      dev-dependencies:
        dependency-type: "development"
```
