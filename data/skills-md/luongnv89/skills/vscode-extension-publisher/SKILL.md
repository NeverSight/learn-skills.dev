---
name: vscode-extension-publisher
version: 1.0.0
description: Publish VS Code extensions to the Visual Studio Marketplace. Use when asked to "publish my extension", "setup VS Code marketplace publishing", "package vscode extension", "create a publisher", "setup PAT for vsce", "automate extension releases with GitHub Actions", or need help with vsce commands.
---

# VS Code Extension Publisher

Guides users through setting up, packaging, and publishing VS Code extensions to the Visual Studio Marketplace, including PAT/publisher setup, pre-flight validation, and CI/CD automation.

## Instructions

### Step 1: Run Pre-flight Checks

Before anything else, validate the environment and project.

Run the bundled preflight script:

```bash
bash scripts/preflight-check.sh
```

This checks:
- Node.js and npm are installed
- `@vscode/vsce` is installed globally (installs it if missing)
- `package.json` exists and has required fields
- No SVG icons (marketplace restriction)

If the script is not available, manually verify:

1. **Node.js installed:** `node --version` (requires v18+)
2. **npm installed:** `npm --version`
3. **vsce installed:** `vsce --version` — if missing, run `npm install -g @vscode/vsce`
4. **package.json exists** in the extension root directory

### Step 2: Validate package.json

The following fields are **required** for publishing:

| Field | Description | Example |
|---|---|---|
| `name` | Extension identifier (lowercase, no spaces) | `"my-extension"` |
| `displayName` | Human-readable name | `"My Extension"` |
| `description` | Short description | `"Adds cool features"` |
| `version` | Semver version | `"1.0.0"` |
| `publisher` | Your publisher ID | `"my-publisher"` |
| `engines.vscode` | Minimum VS Code version | `"^1.80.0"` |
| `categories` | Marketplace categories | `["Other"]` |

**Recommended fields** for better marketplace presence:

| Field | Description |
|---|---|
| `icon` | Path to PNG icon (min 128x128px, **no SVG**) |
| `repository` | GitHub repo URL |
| `license` | License identifier (e.g., `"MIT"`) |
| `keywords` | Search keywords (max 30) |
| `galleryBanner.color` | Hex color for marketplace banner |
| `galleryBanner.theme` | `"dark"` or `"light"` |

If any required field is missing, help the user add it to `package.json`.

### Step 3: Setup Azure DevOps PAT (if needed)

If the user has never published before, guide them through PAT creation:

1. Go to https://dev.azure.com — sign in (or create a free account)
2. Click **User Settings** (gear icon) > **Personal Access Tokens**
3. Click **+ New Token** with these settings:
   - **Name:** `vsce-publish` (or any descriptive name)
   - **Organization:** Select **All accessible organizations**
   - **Expiration:** Set a reasonable duration (max 1 year)
   - **Scopes:** Click **Custom defined** > **Marketplace** > check **Manage**
4. Click **Create** and **copy the token immediately** (it won't be shown again)

**Important:** The PAT must have:
- Organization: "All accessible organizations" (not a specific org)
- Scope: Marketplace > Manage

### Step 4: Create or Verify Publisher (if needed)

If the user doesn't have a publisher identity:

1. Go to https://marketplace.visualstudio.com/manage
2. Sign in with the same Microsoft account used for the PAT
3. Click **Create publisher**
4. Fill in:
   - **ID:** Unique identifier (cannot be changed later!)
   - **Name:** Display name shown on marketplace
5. Verify by running: `vsce login <publisher-id>`
   - Enter the PAT when prompted

Make sure the `publisher` field in `package.json` matches the publisher ID exactly.

### Step 5: Package the Extension

Create a `.vsix` package for testing before publishing:

```bash
vsce package
```

This generates a file like `my-extension-0.0.1.vsix`.

**Test locally before publishing:**

```bash
code --install-extension my-extension-0.0.1.vsix
```

If there are packaging errors:
- **Missing README.md:** Create a README.md in the project root
- **SVG icon:** Replace with a PNG file (min 128x128px)
- **Missing license:** Add a LICENSE file or set `"license"` in package.json

### Step 6: Publish to Marketplace

Once testing is satisfactory, publish:

```bash
vsce publish
```

**Version bump options:**

```bash
vsce publish patch    # 1.0.0 → 1.0.1
vsce publish minor    # 1.0.0 → 1.1.0
vsce publish major    # 1.0.0 → 2.0.0
vsce publish 1.2.3    # Set exact version
```

In git repos, `vsce publish` automatically creates a version commit and tag.

**After publishing:** The extension appears on the marketplace within ~5 minutes. Verify at:
`https://marketplace.visualstudio.com/items?itemName=<publisher>.<extension-name>`

### Step 7: Setup GitHub Actions CI/CD (Optional)

If the user wants automated publishing, generate a GitHub Actions workflow.

Copy the template from `assets/github-actions-publish.yml` to the project:

```bash
mkdir -p .github/workflows
cp assets/github-actions-publish.yml .github/workflows/publish.yml
```

Then guide the user to:

1. Add the PAT as a GitHub secret named `VSCE_PAT`:
   - Go to repo **Settings** > **Secrets and variables** > **Actions**
   - Click **New repository secret**
   - Name: `VSCE_PAT`, Value: the Azure DevOps PAT
2. Publishing triggers on git tags matching `v*` (e.g., `v1.0.0`)
3. To release: `git tag v1.0.0 && git push origin v1.0.0`

See `references/publishing-guide.md` for CI/CD customization options.

## Examples

### Example 1: First-Time Publishing

User says: "I want to publish my VS Code extension to the marketplace"

Actions:
1. Run preflight checks to verify environment
2. Validate package.json — fill in any missing required fields
3. Walk through PAT creation on Azure DevOps
4. Create publisher identity on marketplace
5. Login with `vsce login`
6. Package with `vsce package` and test locally
7. Publish with `vsce publish`

Result: Extension live on VS Code Marketplace.

### Example 2: Publish Update with Version Bump

User says: "publish a new minor version of my extension"

Actions:
1. Run preflight checks
2. Verify package.json is valid
3. Run `vsce publish minor`

Result: Version bumped and published (e.g., 1.0.0 → 1.1.0).

### Example 3: Setup CI/CD for Auto-Publishing

User says: "create a GitHub Actions workflow to auto-publish my extension"

Actions:
1. Copy `assets/github-actions-publish.yml` to `.github/workflows/publish.yml`
2. Guide user to add `VSCE_PAT` secret to GitHub repo
3. Explain tagging workflow: `git tag v1.0.0 && git push origin v1.0.0`

Result: Extensions auto-publish on version tags.

## Error Handling

### 401 Unauthorized / 403 Forbidden

**Cause:** PAT is invalid, expired, or has wrong scope.
**Solution:**
1. Regenerate PAT at https://dev.azure.com with:
   - Organization: "All accessible organizations"
   - Scope: Marketplace > Manage
2. Re-login: `vsce login <publisher-id>`

### "Extension already exists"

**Cause:** Another publisher owns this extension name.
**Solution:** Change the `name` field in `package.json` to something unique. The `displayName` can still be anything.

### SVG Icon Error

**Cause:** Marketplace prohibits SVG icons for security reasons.
**Solution:** Convert the icon to PNG format (minimum 128x128 pixels) and update the `icon` field in `package.json`.

### Missing Fields in package.json

**Cause:** Required fields are absent.
**Solution:** Run the preflight script to identify missing fields, then add them to `package.json`.

### "Exceeded 30 tags"

**Cause:** Too many items in the `keywords` array.
**Solution:** Reduce `keywords` to 30 or fewer entries.

### vsce package fails with prepublish error

**Cause:** The `vscode:prepublish` script in package.json failed.
**Solution:** Run the prepublish script manually to see the error:
```bash
npm run vscode:prepublish
```
Fix the underlying build issue before retrying.

## Validation

### Triggering Test Suite

**Should trigger:**
- "publish my vscode extension"
- "setup marketplace publishing for my extension"
- "package and publish this extension to VS Code marketplace"
- "create a GitHub Actions workflow to auto-publish my extension"
- "help me create a PAT for vsce"
- "publish a new version of my extension"

**Should NOT trigger:**
- "create a new vscode extension"
- "install the prettier extension"
- "debug my vscode extension"
- "publish this package to npm"
- "configure vscode settings"

### Functional Test Cases

```
Test: First-time publish flow
Given: A VS Code extension project with valid package.json
When: User says "publish my extension to the marketplace"
Then:
  - Preflight checks pass (Node, npm, vsce)
  - package.json validated for required fields
  - User guided through PAT and publisher setup
  - Extension packaged and published successfully

Test: Version bump publish
Given: An already-published extension
When: User says "publish a minor update"
Then:
  - vsce publish minor runs successfully
  - Version incremented in package.json
  - Git commit and tag created

Test: CI/CD setup
Given: A VS Code extension project with a GitHub repo
When: User says "setup GitHub Actions for auto-publishing"
Then:
  - Workflow file created at .github/workflows/publish.yml
  - User instructed to add VSCE_PAT secret
  - Tagging workflow explained
```
