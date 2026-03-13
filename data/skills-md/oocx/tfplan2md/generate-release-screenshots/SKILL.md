---
name: generate-release-screenshots
description: Generate PNG screenshots for release notes using the repository's HtmlRenderer and ScreenshotGenerator tools. Use when asked to add screenshots to release notes or documentation.
---

# Skill Instructions

## Purpose
Provide clear, actionable guidance for generating actual PNG screenshot files for release notes and documentation, preventing common mistakes like creating markdown links to source files or referencing non-existent images.

## Hard Rules
### Must
- [ ] **Install Playwright before generating screenshots**: Build the ScreenshotGenerator project (`dotnet build src/tools/Oocx.TfPlan2Md.ScreenshotGenerator/`), then install the browser via `pwsh src/tools/Oocx.TfPlan2Md.ScreenshotGenerator/bin/Debug/net10.0/playwright.ps1 install chromium --with-deps`. Do NOT use `npx playwright install` — the npm version differs from the .NET package version.
- [ ] Generate actual PNG files, NOT markdown links to source files or empty image references.
- [ ] Use `scripts/generate-release-screenshots.sh` for release note screenshots (includes retry logic and error reporting).
- [ ] Use `scripts/generate-screenshot.sh` for individual screenshots with full control (light/dark themes, DPI, crops).
- [ ] Verify generated PNG files exist at expected paths before adding markdown references.
- [ ] Verify screenshots show the intended content (not blank pages or errors) — visually inspect each screenshot.
- [ ] Use focused, small screenshots for release notes: **max 580×400 pixels**.
- [ ] Use only `*-crop*.png` files in release notes, or generate single screenshots using the release wrapper.
- [ ] **Use absolute `raw.githubusercontent.com` URLs in release notes** — relative paths like `./image.png` do NOT work in GitHub Release pages. Use format: `https://raw.githubusercontent.com/oocx/tfplan2md/v{VERSION}/docs/{path}/image.png` where `{VERSION}` is the release tag.
- [ ] **Choose selectors that capture the visual change**: Match the selector to what the feature/fix actually changes (see Selector Guide below).
- [ ] **Generate the report with `--details open`** so resource details blocks are expanded in screenshots — unless you specifically want to capture a collapsed resource.

### Must Not
- [ ] Add `![Screenshot](path/to/image.png)` syntax to markdown before verifying the PNG file exists.
- [ ] Replace actual screenshots with markdown links to source files (e.g., `[View in file.md (lines X-Y)]`).
- [ ] Use text descriptions or placeholders instead of actual PNG files.
- [ ] Proceed with release if screenshot generation fails due to timeouts or tooling issues.
- [ ] Use relative paths (e.g., `./image.png`) in release notes — they break in GitHub Release pages.
- [ ] Reference filenames that don't exist — always verify the actual generated filename matches the markdown reference.

## Golden Example

### For Release Notes (Preferred Method)
```bash
# Generate focused screenshots for release notes
scripts/generate-release-screenshots.sh \
  --plan examples/comprehensive-demo/plan.json \
  --output-prefix feature-name \
  --output-dir docs/features/NNN-feature-slug/ \
  --selector "details:has(summary:has-text('resource_name'))"

# This script:
# - Includes retry logic (3 attempts with 5-second delays)
# - Provides detailed error reporting and troubleshooting guidance
# - Generates focused crop screenshots suitable for release notes
```

### Alternative Methods

#### Using Markdown File as Input
```bash
scripts/generate-release-screenshots.sh \
  --markdown-file artifacts/comprehensive-demo.md \
  --output-prefix demo-screenshot \
  --output-dir docs/features/NNN-feature-slug/ \
  --target-resource-id "azurerm_firewall_network_rule_collection"
```

#### For Individual Screenshots with Full Control
```bash
# Generate with light/dark themes, DPI options, and custom crops
scripts/generate-screenshot.sh \
  --plan examples/comprehensive-demo/plan.json \
  --output-prefix feature-name \
  --selector "details:has(summary:has-text('resource_name'))" \
  --thumbnail-width 580 --thumbnail-height 400 \
  --lightbox-width 1200 --lightbox-height 900 \
  --render-target azdo \
  --open-details-selector "details"

# This generates 12 variants:
# - Thumbnail and lightbox crops
# - Light and dark themes  
# - 1x and 2x DPI versions
```

## Actions

### 0. Install Playwright (PREREQUISITE — REQUIRED)
Before any screenshot generation, ensure the correct Chromium browser is installed for the .NET Playwright package:
```bash
# 1. Build the ScreenshotGenerator project first
dotnet build src/tools/Oocx.TfPlan2Md.ScreenshotGenerator/

# 2. Install Chromium using the .NET project's Playwright script
pwsh src/tools/Oocx.TfPlan2Md.ScreenshotGenerator/bin/Debug/net10.0/playwright.ps1 install chromium --with-deps
```
**⚠️ Do NOT use `npx playwright install`** — the npm Playwright version differs from the .NET `Microsoft.Playwright` NuGet package version, causing browser version mismatches (e.g., the .NET package expects `chromium_headless_shell-1200` but npm installs `chromium_headless_shell-1208`). Always use the .NET project's `playwright.ps1` script to ensure version compatibility.

### 1. Understand What Screenshots Are Needed
Clarify with the user:
- What content should the screenshots show?
- Are they for release notes (small, focused) or documentation (detailed)?
- What resources or sections should be highlighted?

### 2. Choose the Appropriate Script

**For release notes:** Use `scripts/generate-release-screenshots.sh`
- Includes retry logic and error handling
- Generates focused, appropriately-sized screenshots
- Best for user-facing release documentation

**For full control:** Use `scripts/generate-screenshot.sh`
- Supports light/dark themes
- Supports multiple DPI levels (1x, 2x)
- Supports custom crop sizes
- Best for website and detailed documentation

### 3. Generate the Screenshots
Run the chosen script with appropriate parameters:
- Specify input source (`--plan` or `--markdown-file`)
- Set output prefix and directory
- Use selectors to focus on specific content
- For release notes, ensure max 580×400 pixel size
- **Generate the report with `--details open`** so resource attribute tables are visible in the screenshot — unless you specifically want to capture a collapsed resource

### 4. Verify Generation Success
Before proceeding:
- [ ] Check that PNG files exist at the expected paths
- [ ] Open or view the screenshots to confirm they show correct content
- [ ] Verify no blank pages or error messages in screenshots
- [ ] Confirm file sizes are appropriate for release notes

### 5. Add Markdown References
Only after verification, use absolute URLs for release notes:
```markdown
![Feature demonstration](https://raw.githubusercontent.com/oocx/tfplan2md/v{VERSION}/docs/features/NNN-feature-slug/feature-name.png)
```
**Never use relative paths** in release notes — they break in GitHub Release pages.

### 6. Handle Failures
If screenshot generation fails:
- **DO NOT proceed** with release or commit broken image references
- Report the failure to the Maintainer with full error details
- Document the specific error (timeout, CDN failure, tooling issue)
- Wait for tooling fix or Maintainer guidance

## Selector Guide — Choosing What to Capture

The selector determines which part of the rendered HTML page is captured. Choosing the wrong selector is a common mistake that results in screenshots showing irrelevant content.

### How selectors work
- `--selector` captures the bounding box of all matching elements
- `--target-terraform-resource-id` finds the `<details>` block for a specific Terraform resource and captures its full content (attribute tables, body changes, etc.)

### Matching selector to visual change type

| What changed | What to show | Recommended selector |
|---|---|---|
| **Summary line** (emoji, spacing, icons in collapsed view) | The `<summary>` element showing the change | `--selector "summary:has-text('resource_type.resource_name')"` |
| **Resource details** (attribute rendering, body layout) | The expanded `<details>` block | `--target-terraform-resource-id "resource_type.resource_name"` |
| **Section header** (module icons, heading format) | The heading element | `--selector "h3:has-text('Module:')"` or `--selector "h4:has-text('Section Name')"` |
| **Tags rendering** | The tags section within a resource | `--selector "p:has-text('Tags:')"` |
| **Table formatting** | A specific table | `--selector "table:near(summary:has-text('resource'))"` |
| **Multiple elements** (before/after, several fixes) | Wider section containing all changes | `--selector "article"` or use a parent container |

### ❌ Common mistake: Using `--target-terraform-resource-id` for summary-line changes
If a fix only changes the collapsed `<summary>` line (e.g., emoji spacing like `2 🔧`), do NOT use `--target-terraform-resource-id` — this captures the entire expanded resource details block, which shows attribute tables instead of the summary where the fix is visible.

### ✅ Correct: Use a targeted CSS selector
```bash
# To capture wrench icon spacing fix in summary:
--selector "summary:has-text('azurerm_network_security_group')"

# To capture tags emoji addition:
--selector "p:has-text('🏷️ Tags:')"

# To capture module icon fix:
--selector "h3:has-text('📦 Module:')"
```

## Image URLs for Release Notes

### ❌ Wrong: Relative paths (break in GitHub Release pages)
```markdown
![Screenshot](./screenshot.png)
![Screenshot](docs/features/NNN/screenshot.png)
```
Relative paths work when browsing the file in the GitHub repository, but GitHub Release pages render the markdown body without a file context, so relative paths produce broken images.

### ✅ Correct: Absolute raw.githubusercontent.com URLs
```markdown
![Screenshot](https://raw.githubusercontent.com/oocx/tfplan2md/v1.20.0/docs/issues/086/screenshot.png)
```
Use the release tag (e.g., `v1.20.0`) in the URL. Since the release notes are committed before the tag exists, use the tag that will be created by the release pipeline. The format is:
```
https://raw.githubusercontent.com/oocx/tfplan2md/v{VERSION}/docs/{work-item-folder}/{filename}.png
```

**Important:** The release notes file is committed to main before the tag is created. The release workflow copies `release-notes.md` as the GitHub Release body. Since the tag is created by Versionize on the same commit, the file will be accessible at the tag URL.

## Common Mistakes to Avoid

### ❌ Wrong: Adding references before generating files
```markdown
# Release notes created first
![Screenshot](docs/features/072/screenshot.png)

# Then trying to generate the screenshot
# Result: Broken link if generation fails
```

### ✅ Correct: Generate first, then reference
```bash
# 1. Generate the screenshot
scripts/generate-release-screenshots.sh --plan ... --output-prefix feature-name

# 2. Verify it exists
ls -lh docs/features/NNN/feature-name-crop-light-1x.png

# 3. Then add the markdown reference
echo '![Feature](docs/features/NNN/feature-name-crop-light-1x.png)' >> release-notes.md
```

### ❌ Wrong: Using markdown links instead of screenshots
```markdown
See the changes in [comprehensive-demo.md (lines 45-67)](comprehensive-demo.md#L45-L67)
```

### ✅ Correct: Using actual PNG screenshots
```markdown
![Network security rules demonstration](https://raw.githubusercontent.com/oocx/tfplan2md/v1.20.0/docs/features/072/nsg-rules.png)
```

### ❌ Wrong: Referencing filenames that don't exist
```markdown
![Before](https://raw.githubusercontent.com/oocx/tfplan2md/abc123/docs/features/072/before-screenshot.png)
# But the actual file is named "nsg-rules.png", not "before-screenshot.png"
```

### ✅ Correct: Verify actual filenames before referencing
```bash
# 1. Generate screenshots
scripts/generate-release-screenshots.sh --plan ... --output-prefix nsg-rules --output-dir docs/features/072/

# 2. List actual generated files
ls docs/features/072/*.png

# 3. Use the exact filename in markdown
# Output: docs/features/072/nsg-rules.png
```

### ❌ Wrong: Skipping Playwright installation or using npx
```bash
# Wrong: Skipping installation entirely
scripts/generate-release-screenshots.sh --plan ... --output-prefix feature ...
# Result: "Browser not found" error

# Wrong: Using npx (version mismatch with .NET Playwright package)
npx playwright install chromium --with-deps
scripts/generate-release-screenshots.sh --plan ... --output-prefix feature ...
# Result: "Executable doesn't exist at chromium_headless_shell-1200" (npm installed -1208)
```

### ✅ Correct: Install via .NET Playwright script
```bash
dotnet build src/tools/Oocx.TfPlan2Md.ScreenshotGenerator/
pwsh src/tools/Oocx.TfPlan2Md.ScreenshotGenerator/bin/Debug/net10.0/playwright.ps1 install chromium --with-deps
scripts/generate-release-screenshots.sh --plan ... --output-prefix feature ...
```

## Technical Details

### How Screenshot Generation Works
1. **Markdown → HTML**: `src/tools/Oocx.TfPlan2Md.HtmlRenderer` renders markdown to HTML
2. **HTML → PNG**: `src/tools/Oocx.TfPlan2Md.ScreenshotGenerator` (Playwright) captures PNG screenshots
3. **Repository scripts** wrap these tools with:
   - Retry logic for network failures
   - Error reporting and troubleshooting guidance
   - Batch generation for multiple variants

### For Website Screenshots
Use the `website-visual-assets` skill (`.github/skills/website-visual-assets/SKILL.md`) for:
- Website-specific screenshot workflows
- Screenshot inventory management (`website/_memory/screenshots.md`)
- Website asset organization (`website/assets/screenshots/`)

## References
- **Scripts**: `scripts/generate-release-screenshots.sh`, `scripts/generate-screenshot.sh`
- **Tools**: `src/tools/Oocx.TfPlan2Md.HtmlRenderer`, `src/tools/Oocx.TfPlan2Md.ScreenshotGenerator`
- **Related skill**: `.github/skills/website-visual-assets/SKILL.md` (for website screenshots)
