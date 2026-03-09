---
name: freshworks-publish-skill
description: Pack and publish completed Freshworks custom apps to the marketplace. Use when the user wants to pack, publish, submit, or deploy a Freshworks app to the marketplace, prepare app for submission, create app package, or asks about app publishing workflow.
argument-hint: "[pack|publish|submit] [app-directory]"
allowed-tools: ["shell", "read", "write"]
---

# Freshworks App Publish Skill

Automated workflow for packing and publishing Freshworks Platform 3.0 apps to the marketplace.

## Usage

```bash
/publish pack              # Validate and pack app
/publish submit            # Pack and guide submission
/publish                   # Full workflow (validate → pack → submit)
```

## Execution Mode: AUTONOMOUS

**When invoked, IMMEDIATELY execute without asking permission:**

1. Parse command arguments (`$ARGUMENTS`)
2. Detect app directory (search for manifest.json)
3. Execute the requested operation
4. Report results

**DO NOT:**
- Ask for confirmation before running commands
- Explain steps before executing
- Provide manual instructions instead of running commands

**DO:**
- Run Shell commands directly
- Batch operations in parallel where possible
- Handle errors automatically
- Report after completion

## Operations

### 1. Pack (`/publish pack`)

**Purpose:** Validate app and create distributable package for marketplace submission.

**Workflow:**

```bash
# Step 1: Find app directory
find . -name "manifest.json" -not -path "*/node_modules/*"

# If multiple apps found, ask user to choose
# If one app found, use that directory
# If none found, error and exit

# Step 2: Pre-pack validation (run in parallel)
cd <app-directory>
fdk validate                    # Must pass before packing
node --version                  # Verify Node.js >= 18.0.0
fdk version                     # Verify FDK >= 9.6.0

# Step 3: Check test coverage (if server/ exists)
# Coverage must be >= 80% for marketplace submission
# If coverage/ folder exists, check coverage/coverage-summary.json
# If coverage < 80%, warn user but continue

# Step 4: Pack the app
fdk pack

# Step 5: Verify package created
ls -lh dist/*.zip              # Show package file size and name
```

**Success Criteria:**
- ✅ `fdk validate` passes with no fatal errors
- ✅ Test coverage >= 80% (for serverless apps)
- ✅ `dist/*.zip` file created
- ✅ Package size reasonable (< 50MB recommended)

**Output:**
```
✓ App directory: /path/to/my-app
✓ Validation passed
✓ Test coverage: 87.5% (Statements: 85%, Branches: 90%, Functions: 85%, Lines: 90%)
✓ Package created: dist/my-app-1.0.0.zip (2.3 MB)

📦 Ready for submission!
```

### 2. Submit (`/publish submit`)

**Purpose:** Guide user through marketplace submission process after packing.

**Workflow:**

```bash
# Step 1: Ensure app is packed
cd <app-directory>
ls dist/*.zip || fdk pack       # Pack if not already packed

# Step 2: Extract submission details from manifest
cat manifest.json               # Read app metadata

# Step 3: Generate submission checklist
```

**Submission Checklist Generated:**

```markdown
📋 **Marketplace Submission Checklist**

✅ **Pre-Submission:**
- [ ] App validated: `fdk validate` passes
- [ ] Test coverage >= 80%
- [ ] App package created: dist/<app-name>.zip
- [ ] All iparams documented
- [ ] OAuth credentials tested (if applicable)
- [ ] App tested in target product(s)

📦 **Package Information:**
- App Name: [from manifest]
- Version: [from manifest]
- Platform: [from manifest]
- Products: [from manifest modules]
- Package: dist/<filename>.zip

🌐 **Submission Steps:**

1. **Access Developer Portal:**
   - Log in to your Freshworks product account
   - Navigate to Admin > Apps > Build it yourself
   - Or: Neo Admin Center > My Accounts > /developer

2. **Create New App Submission:**
   - Click "Create New App"
   - Select app type:
     • Freshworks App (public marketplace, revenue-generating)
     • Custom App (private, customer-specific, no review)
     • External App (listed in marketplace, installed from external URL)

3. **Upload Package:**
   - Upload: dist/<filename>.zip
   - Fill in app details:
     • App name
     • Description (use Freddy AI assistance)
     • Categories (new framework)
     • Screenshots (min 3, recommended 5)
     • Support email
     • Privacy policy URL
     • Terms of service URL

4. **Configure Pricing (Freshworks Apps only):**
   - Free or Paid
   - If paid: Set pricing tiers
   - Revenue share: 20% to Freshworks

5. **Submit for Review:**
   - Click "Submit for Review"
   - Review timeline: 5-10 business days
   - Custom apps: Published immediately (no review)

📧 **Post-Submission:**
- Monitor email for review updates
- Respond to review feedback within 7 days
- Update app version if changes requested

🔗 **Resources:**
- Developer Portal: https://developers.freshworks.com/
- Submission Guidelines: https://developers.freshworks.com/docs/guides/submission-guidelines/
- App Review Guidelines: https://developers.freshworks.com/docs/guides/submission-guidelines/app-validation/
```

### 3. Full Workflow (`/publish`)

**Purpose:** Complete end-to-end workflow from validation to submission guidance.

**Workflow:**

```bash
# Step 1: Find and validate app
cd <app-directory>
fdk validate

# Step 2: Check coverage (if serverless)
# Parse coverage/coverage-summary.json if exists

# Step 3: Pack app
fdk pack

# Step 4: Generate submission checklist
# (same as /publish submit)
```

## Pre-Pack Validation Checklist

**CRITICAL: These must pass before packing:**

### Mandatory Files
- [ ] `manifest.json` - Platform 3.0 structure
- [ ] `config/iparams.json` - Even if empty `{}`
- [ ] `app/styles/images/icon.svg` - Required for frontend apps
- [ ] `README.md` - App documentation

### Manifest Validation
- [ ] `"platform-version": "3.0"`
- [ ] `"modules"` structure (not `"product"`)
- [ ] `"engines"` block with Node.js and FDK versions
- [ ] All request templates declared in `modules.common.requests`
- [ ] All SMI functions declared in `modules.common.functions`
- [ ] At least one product module declared

### Code Quality (Lint Errors)
- [ ] No async functions without await
- [ ] No unused variables or parameters
- [ ] No unreachable code
- [ ] Function complexity <= 7
- [ ] No eval() or alert() calls
- [ ] No var declarations (use const/let)

### Test Coverage (Serverless Apps)
- [ ] Statements >= 80%
- [ ] Branches >= 80%
- [ ] Functions >= 80%
- [ ] Lines >= 80%

### Configuration
- [ ] All iparams have display_name and type
- [ ] OAuth config has integrations wrapper (if applicable)
- [ ] Request templates use FQDN hosts (no paths)
- [ ] Request templates use `<%= variable %>` syntax

## Error Handling

| Error | Action |
|-------|--------|
| No manifest.json found | Search workspace, ask user to specify directory |
| Multiple apps found | Ask user which app to pack |
| `fdk validate` fails | Show errors, attempt autofix, re-validate |
| Coverage < 80% | Warn user, suggest running tests, allow override |
| `fdk pack` fails | Show error, check Node.js/FDK versions |
| Package size > 50MB | Warn about large package, suggest optimization |
| Missing icon.svg | Error - cannot pack frontend app without icon |

## Package Output

**After successful pack:**

```
dist/
└── <app-name>-<version>.zip    # Marketplace package

Package contents:
- app/ (if frontend)
- server/ (if serverless)
- config/
- manifest.json
- README.md
- package.json (if dependencies)
```

**Package excludes:**
- `node_modules/`
- `.coverage/`
- `.fdk/`
- `.git/`
- `dist/` (previous builds)
- Test files and fixtures
- Development files (.env, .vscode, etc.)

## Coverage Validation

**For serverless apps, check coverage before packing:**

```bash
# Check if coverage exists
ls coverage/coverage-summary.json

# Parse coverage
cat coverage/coverage-summary.json | grep "total"

# Expected format:
{
  "total": {
    "lines": { "pct": 90.5 },
    "statements": { "pct": 88.2 },
    "functions": { "pct": 85.7 },
    "branches": { "pct": 82.3 }
  }
}
```

**If coverage < 80%:**
- Warn user
- Suggest: `fdk run` to regenerate coverage
- Suggest: Write more tests in `server/test/`
- Allow pack with `--skip-coverage` flag (NOT recommended for marketplace)

## Marketplace Submission Types

### 1. Freshworks App (Public Marketplace)

**Characteristics:**
- Public listing in Freshworks Marketplace
- Subject to review (5-10 business days)
- Can be free or paid (revenue share: 20% to Freshworks)
- Requires comprehensive documentation
- Must pass all validation checks

**Best for:**
- Apps with broad appeal
- Revenue-generating apps
- Apps solving common use cases

### 2. Custom App (Private)

**Characteristics:**
- Private to specific customer
- No review required
- Published immediately upon submission
- Can test multiple versions in production
- No revenue generation

**Best for:**
- Customer-specific requirements
- Internal tools
- Rapid deployment needs

### 3. External App (Third-Party)

**Characteristics:**
- Listed in Freshworks Marketplace
- Installed from external URL (not Freshworks-hosted)
- Subject to review
- Uses module-specific methods

**Best for:**
- Third-party integrations
- Apps hosted externally
- Cross-platform solutions

## Post-Pack Next Steps

**After successful pack, inform user:**

```
✅ App packed successfully!

📦 **Package Details:**
- File: dist/<app-name>-<version>.zip
- Size: <size> MB
- Platform: 3.0
- Products: [list from modules]

🚀 **Next Steps:**

1. **Access Developer Portal:**
   - Log in to your Freshworks product account
   - Navigate to: Admin > Apps > Build it yourself
   - Or: Neo Admin Center > /developer

2. **Choose App Type:**
   - Freshworks App: Public marketplace (review required)
   - Custom App: Private, immediate publish (no review)
   - External App: Listed but externally hosted

3. **Upload Package:**
   - Click "Create New App"
   - Upload: dist/<app-name>-<version>.zip
   - Fill in app details with Freddy AI assistance

4. **Required Information:**
   - App name and description
   - Categories (new framework)
   - Screenshots (min 3, recommended 5)
   - Support email
   - Privacy policy URL (if collecting user data)
   - Terms of service URL

5. **Submit:**
   - Review all details
   - Click "Submit for Review" (Freshworks/External apps)
   - Or "Publish" (Custom apps - immediate)

📧 **After Submission:**
- Monitor email for review updates
- Review timeline: 5-10 business days (Freshworks/External apps)
- Custom apps: Available immediately
- Respond to feedback within 7 days

🔗 **Resources:**
- Developer Portal: https://developers.freshworks.com/
- Submission Guidelines: https://developers.freshworks.com/docs/guides/submission-guidelines/
```

## Pre-Pack Validation Automation

**CRITICAL: Always validate before packing**

```bash
# Run validation
cd <app-directory>
fdk validate

# Parse output
# If fatal errors exist:
#   - Attempt autofix (up to 2 iterations)
#   - Re-run fdk validate
#   - If still failing, report errors and stop

# If lint errors exist:
#   - Attempt autofix (common patterns)
#   - Re-run fdk validate
#   - If still failing, report errors and stop

# If warnings only:
#   - Report warnings
#   - Proceed with pack

# If validation passes:
#   - Proceed with pack
```

## Common Pre-Pack Fixes

### 1. Missing icon.svg
```bash
# Check if frontend app
ls app/index.html

# If frontend app exists, check for icon
ls app/styles/images/icon.svg || echo "MISSING - MUST CREATE"

# Create placeholder icon if missing
mkdir -p app/styles/images/
# Create SVG icon (use template or generate)
```

### 2. Coverage < 80%
```bash
# Run tests to regenerate coverage
fdk run
# Press Ctrl+C after app starts
# Check coverage summary
```

### 3. Async without await
```bash
# Scan server/server.js for async functions without await
# Add await to async operations OR remove async keyword
```

### 4. Unused parameters
```bash
# Scan for unused parameters in event handlers
# Prefix with _ or remove if not needed
```

## Template Variables

Use Maestro template variables for context:

- `{{CWD}}` - Current working directory
- `{{DATE}}` - Current date
- `{{AGENT_PATH}}` - Project path
- `{{GIT_BRANCH}}` - Current git branch

Example: `/publish pack` in app at `{{CWD}}`

## Success Output

```
✓ App directory: /path/to/my-app
✓ Platform version: 3.0
✓ Validation: PASSED
✓ Test coverage: 87.5%
  - Statements: 85%
  - Branches: 90%
  - Functions: 85%
  - Lines: 90%
✓ Package created: dist/my-app-1.0.0.zip (2.3 MB)

📦 Package ready for submission!

🚀 Next: Upload to Developer Portal
   → Admin > Apps > Build it yourself
   → Or: Neo Admin Center > /developer
```

## Error Messages

### Validation Failed
```
❌ Validation failed with 3 errors:

1. Missing required file: app/styles/images/icon.svg
   Fix: Create icon.svg in app/styles/images/

2. Async function without await (server/server.js:45)
   Fix: Add await expression or remove async keyword

3. Unused parameter 'args' (server/server.js:23)
   Fix: Remove parameter or prefix with _

Run: fdk validate --fix
Or: /fix to auto-fix all errors
```

### Coverage Too Low
```
⚠️  Test coverage below 80%:
   - Statements: 65%
   - Branches: 70%
   - Functions: 60%
   - Lines: 68%

Marketplace requires >= 80% coverage.

Fix:
1. Run: fdk run (generates coverage)
2. Add tests in server/test/
3. Re-run validation

Or pack anyway: fdk pack --skip-coverage (NOT recommended for marketplace)
```

### Package Too Large
```
⚠️  Package size: 52.3 MB (recommended: < 50 MB)

Large packages may cause:
- Slow installation for users
- Longer review times
- Potential rejection

Optimize:
- Remove unused dependencies
- Compress images
- Remove development files
- Check .gitignore patterns
```

## Detailed Workflows

### Workflow 1: Pack Only

```bash
# 1. Find app
find . -name "manifest.json" -not -path "*/node_modules/*"

# 2. Validate
cd <app-directory>
fdk validate

# 3. Check coverage (if serverless)
if [ -d "server" ]; then
  if [ -f "coverage/coverage-summary.json" ]; then
    # Parse and check >= 80%
    cat coverage/coverage-summary.json
  else
    echo "⚠️  No coverage found. Run 'fdk run' first."
  fi
fi

# 4. Pack
fdk pack

# 5. Report
ls -lh dist/*.zip
```

### Workflow 2: Full Publish Workflow

```bash
# 1. Find app
find . -name "manifest.json" -not -path "*/node_modules/*"

# 2. Read manifest for metadata
cat manifest.json | grep -E "(platform-version|version|modules)"

# 3. Validate
fdk validate

# 4. Check coverage
# (same as Workflow 1)

# 5. Pack
fdk pack

# 6. Generate submission checklist
# (output detailed checklist with app-specific details)
```

### Workflow 3: Submit Guidance

```bash
# 1. Ensure packed
ls dist/*.zip || fdk pack

# 2. Extract app details
APP_NAME=$(cat manifest.json | grep '"name"' | head -1)
APP_VERSION=$(cat manifest.json | grep '"version"' | head -1)
PLATFORM=$(cat manifest.json | grep '"platform-version"')

# 3. Generate personalized submission guide
# (output checklist with extracted details)
```

## App Type Decision Tree

**Help user choose app type:**

```
What type of app are you submitting?

1. **Freshworks App** (Public Marketplace)
   ✅ Choose if:
   - App solves common use cases
   - Want to reach all Freshworks customers
   - Want to generate revenue (optional)
   - Ready for 5-10 day review process

2. **Custom App** (Private)
   ✅ Choose if:
   - Built for specific customer
   - Need immediate deployment
   - No public listing needed
   - Customer-specific requirements

3. **External App** (Listed, External Install)
   ✅ Choose if:
   - App hosted on your infrastructure
   - Want marketplace listing
   - Install happens via external URL
   - Third-party integration
```

## Validation Requirements

### Platform 3.0 Requirements
- ✅ `"platform-version": "3.0"`
- ✅ `"modules"` structure (not `"product"`)
- ✅ `"engines"` block present
- ✅ Request templates use FQDN hosts
- ✅ OAuth uses `integrations` wrapper
- ✅ Crayons components (not plain HTML)

### Lint Requirements
- ✅ No async without await
- ✅ No unused variables
- ✅ No unreachable code
- ✅ Function complexity <= 7
- ✅ No eval() or alert()
- ✅ No var (use const/let)

### Coverage Requirements (Serverless)
- ✅ Statements >= 80%
- ✅ Branches >= 80%
- ✅ Functions >= 80%
- ✅ Lines >= 80%

### Documentation Requirements
- ✅ README.md with setup instructions
- ✅ All iparams documented
- ✅ OAuth setup guide (if applicable)
- ✅ Screenshots prepared (min 3)

## Advanced Options

### Skip Coverage (NOT recommended)
```bash
fdk pack --skip-coverage
```
**Warning:** Marketplace will reject apps with < 80% coverage.

### Skip Lint (Deprecated)
```bash
fdk pack --skip-lint
```
**Warning:** This option is deprecated and will be removed.

### Pack Specific Directory
```bash
fdk pack --app-dir /path/to/app
```

## Troubleshooting

### Pack Fails with "Validation Error"
```bash
# Run validation first
fdk validate

# Fix all errors
# Re-run pack
fdk pack
```

### Pack Fails with "Coverage Error"
```bash
# Regenerate coverage
fdk run
# Wait for app to start, then Ctrl+C
# Check coverage summary
# Re-run pack
fdk pack
```

### Package Not Created
```bash
# Check for dist/ folder
ls -la dist/

# If exists, check permissions
chmod 755 dist/

# Re-run pack
fdk pack
```

### Node.js Version Mismatch
```bash
# Check current Node.js version
node --version

# Check manifest requirement
cat manifest.json | grep "node"

# Update manifest or switch Node.js version
# Re-run pack
fdk pack
```

## Post-Pack Verification

**After pack succeeds, verify package:**

```bash
# 1. Check package exists
ls -lh dist/*.zip

# 2. Check package contents (optional)
unzip -l dist/*.zip

# 3. Verify key files included
unzip -l dist/*.zip | grep -E "(manifest.json|server.js|index.html|icon.svg)"

# 4. Check package size
du -h dist/*.zip
```

## Integration with Other Skills

**This skill works with:**

- **app-dev** - Generate and fix apps before packing
- **fdk-setup** - Ensure FDK is installed and up-to-date
- **Validation** - Fix errors before packing

**Typical workflow:**
1. Use `app-dev` to create app
2. Use `/fix` to resolve validation errors
3. Use `/publish pack` to create package
4. Use `/publish submit` for submission guidance

## References

**For detailed submission guidelines:**
- Freshworks Developer Portal: https://developers.freshworks.com/
- App Validation: https://developers.freshworks.com/docs/guides/submission-guidelines/app-validation/
- Submission Process: https://developers.freshworks.com/docs/app-sdk/v3.0/support_email/app-submission-process/

## Summary

This skill provides:
- **Automated packing** - Validate and pack in one command
- **Coverage checking** - Ensure >= 80% before submission
- **Submission guidance** - Step-by-step checklist
- **Error handling** - Automatic detection and fix suggestions
- **Package verification** - Confirm package contents and size

When uncertain about submission requirements, load the relevant reference or use web search for latest marketplace guidelines.
