---
name: audit-env-variables
description: Analyze environment variables in JavaScript/TypeScript projects. Identifies unused variables, infers permission scopes, detects specific services (Stripe, AWS, Supabase), and documents code paths. Includes optional cleanup of unused variables with regression detection. Use when auditing .env files, reviewing security, or documenting project configuration.
argument-hint: "[output-path] [--cleanup]"
allowed-tools: [Read, Grep, Glob, Bash, Write, Edit, AskUserQuestion]
---

<objective>
Perform a comprehensive audit of environment variables in a JS/TS project:

1. **Discovery** - Find all env files and code references
2. **Usage Analysis** - Identify which variables are used vs unused
3. **Service Detection** - Recognize services (Stripe, AWS, Supabase, etc.) and their permission implications
4. **Code Path Mapping** - Document where each variable is used in the codebase
5. **Report Generation** - Output a structured markdown document
6. **Cleanup** (optional) - Safely remove unused variables with user confirmation
7. **Regression Prevention** - Validate no regressions via build/test validation with automatic rollback
</objective>

<quick_start>
**Audit only (default):**
1. Scan for `.env*` files in project root
2. Grep codebase for `process.env.`, `import.meta.env.`, and destructured env patterns
3. Cross-reference declared vs used variables
4. Identify services by naming patterns and categorize permissions
5. Generate markdown report using the template

**With cleanup (`--cleanup` flag):**
6. Check for dynamic access patterns that might hide usage
7. Present unused variables and get user confirmation
8. Create backups, remove confirmed variables
9. Run build/tests to detect regressions
10. Auto-rollback if regressions detected
</quick_start>

<process>
## Step 1: Discover Environment Files

Find all env-related files:
```bash
find . -maxdepth 2 -name ".env*" -o -name "env.d.ts" | grep -v node_modules
```

Common files:
- `.env` - Local development
- `.env.local` - Local overrides
- `.env.development` / `.env.production` - Environment-specific
- `.env.example` - Template for required variables

## Step 2: Extract Declared Variables

Parse each env file for variable declarations:
```
Grep pattern: ^[A-Z][A-Z0-9_]+=
```

Build a list of all declared variables with their source file.

## Step 3: Find Code References

Search for environment variable usage patterns:

**Direct access:**
```
process.env.VARIABLE_NAME
import.meta.env.VARIABLE_NAME
process.env["VARIABLE_NAME"]
```

**Destructured patterns:**
```javascript
const { API_KEY, DATABASE_URL } = process.env
```

**Framework-specific:**
```javascript
// Next.js public vars
NEXT_PUBLIC_*

// Vite
VITE_*
```

Use Grep tool with patterns:
```
process\.env\.([A-Z][A-Z0-9_]+)
import\.meta\.env\.([A-Z][A-Z0-9_]+)
```

## Step 4: Cross-Reference Usage

For each declared variable:
- **Used**: Found in code references
- **Unused**: Declared but no code references found
- **Undeclared**: Referenced in code but not in any env file

Flag potential issues:
- Unused variables (cleanup candidates)
- Undeclared variables (missing from .env.example)
- Variables only in .env but not .env.example (documentation gap)

## Step 5: Detect Services and Infer Permissions

Match variable names against known service patterns. See references/service-patterns.md for the complete list.

**Categories:**
- **Database** - Connection strings, credentials
- **Authentication** - JWT secrets, OAuth credentials
- **Payment** - Stripe, payment processor keys
- **Cloud Services** - AWS, GCP, Azure credentials
- **Third-party APIs** - Various service integrations
- **Feature Flags** - Toggle configurations
- **Application Config** - URLs, ports, modes

**Permission levels:**
- **Critical** - Full account access, billing, admin operations
- **High** - Read/write access to user data
- **Medium** - Limited API access, specific operations
- **Low** - Public keys, non-sensitive configuration

## Step 6: Map Code Paths

For each used variable, document:
- File path where it's used
- Function/component context
- Purpose (inferred from surrounding code)

Example:
```
STRIPE_SECRET_KEY
├── src/lib/stripe.ts:15 - Stripe client initialization
├── src/api/webhooks/stripe.ts:8 - Webhook signature verification
└── src/api/checkout/route.ts:23 - Create checkout session
```

## Step 7: Generate Report

Use the template in templates/env-audit-report.md to generate the final document.

Output to: `ENV_AUDIT.md` in project root (or user-specified location)

## Step 8: Cleanup Unused Variables (Optional)

**Trigger:** User passes `--cleanup` flag or explicitly requests cleanup after reviewing the audit report.

### 8.1 Present Cleanup Candidates

Display unused variables with context:
```
UNUSED VARIABLES (candidates for removal):

1. OLD_API_KEY (.env, .env.local)
   - Last modified: [file date]
   - No code references found

2. DEPRECATED_SERVICE_URL (.env)
   - Last modified: [file date]
   - No code references found
```

### 8.2 Dynamic Access Check

Before confirming removal, search for dynamic access patterns that grep may have missed:

```javascript
// These patterns indicate variables might be used dynamically:
process.env[variableName]        // Dynamic key access
process.env[`${prefix}_KEY`]     // Template literal access
Object.keys(process.env)         // Iteration over all env vars
{ ...process.env }               // Spread operator
```

Use Grep with patterns:
```
process\.env\[
Object\.keys\(process\.env\)
Object\.entries\(process\.env\)
\.\.\.process\.env
```

**If dynamic access patterns found:** Flag affected variables for manual review and warn user.

### 8.3 User Confirmation

Use AskUserQuestion to confirm each removal:

```
The following variables appear unused. Select which to remove:

[ ] OLD_API_KEY - Remove from .env, .env.local
[ ] DEPRECATED_SERVICE_URL - Remove from .env
[ ] Skip cleanup

⚠️ Variables will be backed up before removal.
```

**Safety rules:**
- NEVER auto-delete without explicit user confirmation
- NEVER remove variables from `.env.example` (it serves as documentation)
- Create backup before any modifications

### 8.4 Create Backups

Before modifying any file:
```bash
# Create timestamped backup directory
mkdir -p .env-backups/$(date +%Y%m%d_%H%M%S)

# Backup each env file being modified
cp .env .env-backups/$(date +%Y%m%d_%H%M%S)/.env.backup
cp .env.local .env-backups/$(date +%Y%m%d_%H%M%S)/.env.local.backup
```

### 8.5 Remove Confirmed Variables

For each confirmed variable:
1. Use Edit tool to remove the line from each env file
2. Preserve comments associated with the variable (line immediately above if it starts with #)
3. Log the removal

### 8.6 Document Cleanup

Append cleanup summary to ENV_AUDIT.md:
```markdown
## Cleanup Log

**Date:** [timestamp]
**Backup Location:** .env-backups/[timestamp]/

### Removed Variables
| Variable | Removed From | Reason |
|----------|--------------|--------|
| OLD_API_KEY | .env, .env.local | Unused - no code references |

### Preserved (Manual Review Required)
| Variable | Reason |
|----------|--------|
| DYNAMIC_VAR | Dynamic access pattern detected |
```

## Step 9: Regression Prevention

**Purpose:** Validate that removing unused variables doesn't break the application.

### 9.1 Pre-Cleanup Baseline

Before removing any variables, capture baseline state:

```bash
# Check if project builds successfully
npm run build 2>&1 | tee .env-backups/pre-cleanup-build.log
echo $? > .env-backups/pre-cleanup-build-status

# Run tests if available
npm test 2>&1 | tee .env-backups/pre-cleanup-test.log
echo $? > .env-backups/pre-cleanup-test-status
```

Store exit codes:
- `0` = Success (baseline is green)
- Non-zero = Already failing (warn user but proceed if they confirm)

### 9.2 Dynamic Access Detection

Search for patterns that indicate runtime env var access:

**High-risk patterns (require manual review):**
```javascript
// Config objects that spread env
const config = { ...process.env }

// Dynamic key construction
const key = `${SERVICE}_API_KEY`
process.env[key]

// Iteration patterns
Object.entries(process.env).filter(([k]) => k.startsWith('FEATURE_'))

// External config loaders
require('dotenv').config({ path: customPath })
```

**Detection commands:**
```
Grep: process\.env\[(?!['"][A-Z])
Grep: Object\.(keys|values|entries)\(process\.env\)
Grep: \.\.\.process\.env
Grep: dotenv.*config
```

**If detected:** List affected files and require explicit user acknowledgment before proceeding.

### 9.3 Post-Cleanup Validation

After removing variables, run validation:

```bash
# Verify build still succeeds
npm run build 2>&1 | tee .env-backups/post-cleanup-build.log
POST_BUILD_STATUS=$?

# Verify tests still pass
npm test 2>&1 | tee .env-backups/post-cleanup-test.log
POST_TEST_STATUS=$?
```

### 9.4 Regression Detection

Compare pre and post states:

| Check | Pre-Cleanup | Post-Cleanup | Status |
|-------|-------------|--------------|--------|
| Build | ✅ Pass | ✅ Pass | OK |
| Tests | ✅ Pass | ✅ Pass | OK |

**If regression detected:**
1. Immediately alert user
2. Offer automatic rollback:
   ```
   ⚠️ REGRESSION DETECTED

   Build/tests failed after removing variables.

   Options:
   1. Rollback all changes (restore from backup)
   2. Rollback specific variables
   3. Investigate failure (show diff)
   4. Proceed anyway (not recommended)
   ```

### 9.5 Automatic Rollback

If user requests rollback:
```bash
# Restore from backup
cp .env-backups/[timestamp]/.env.backup .env
cp .env-backups/[timestamp]/.env.local.backup .env.local

# Verify restoration
npm run build && npm test
```

### 9.6 Git Integration (Optional)

If in a git repository, offer branch-based cleanup:

```bash
# Create cleanup branch
git checkout -b env-cleanup/$(date +%Y%m%d)

# After cleanup, changes can be reviewed via PR
git add .env .env.local
git commit -m "chore: remove unused environment variables

Removed:
- OLD_API_KEY (unused)
- DEPRECATED_SERVICE_URL (unused)

Backup: .env-backups/[timestamp]/"
```

**Benefits:**
- Easy rollback via `git checkout -`
- Changes visible in PR review
- CI/CD will validate before merge
</process>

<reference_index>
**Service Patterns:** references/service-patterns.md - Known services and their variable naming conventions
</reference_index>

<success_criteria>
**Audit is complete when:**
- [ ] All .env files discovered and parsed
- [ ] All code references found
- [ ] Variables categorized as used/unused/undeclared
- [ ] Services detected and permission levels assigned
- [ ] Code paths documented for each variable
- [ ] Markdown report generated with all sections
- [ ] Report saved to specified location

**Cleanup is complete when (if --cleanup requested):**
- [ ] Dynamic access patterns checked
- [ ] User confirmed variables to remove
- [ ] Backups created in .env-backups/
- [ ] Variables removed from env files (not .env.example)
- [ ] Cleanup log appended to report

**Regression prevention is complete when:**
- [ ] Pre-cleanup build/test baseline captured
- [ ] Post-cleanup validation run
- [ ] No regressions detected OR rollback performed
- [ ] Git branch created (if opted in)
</success_criteria>
