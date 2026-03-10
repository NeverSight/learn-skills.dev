---
name: website-visual-assets
description: Generate website HTML exports and screenshots using the repo's HtmlRenderer and ScreenshotGenerator tools.
---

# Skill Instructions

## Purpose
Provide a repeatable workflow to generate HTML exports and screenshots for the website, and keep the screenshot inventory in sync.

## Hard Rules
### Must
- [ ] Use `src/tools/Oocx.TfPlan2Md.HtmlRenderer` to generate HTML from markdown reports.
- [ ] Use `src/tools/Oocx.TfPlan2Md.ScreenshotGenerator` (Playwright) to generate screenshots from those HTML exports.
- [ ] Store website screenshots under `website/assets/screenshots/`.
- [ ] Add/update an entry in `website/_memory/screenshots.md` for every screenshot used by the website.

### Must Not
- [ ] Do not hand-edit screenshots or create “mock” screenshots that aren’t generated from real HTML exports.

## Golden Example

```bash
# Preferred Method: Use the automated script
scripts/generate-screenshot.sh \
  --plan examples/firewall-with-static-analysis/plan.json \
  --output-prefix firewall-example \
  --selector "details:has(summary:has-text('azurerm_firewall_network_rule_collection'))" \
  --thumbnail-width 580 --thumbnail-height 400 \
  --lightbox-width 1200 --lightbox-height 900 \
  --render-target azdo \
  --open-details-selector "details"

# This generates 12 screenshot variants automatically:
# - Thumbnail and lightbox crops
# - Light and dark themes
# - 1x and 2x DPI versions
# - Azure DevOps rendering style

# Manual Method (for advanced use cases):
# 1) Generate HTML (Azure DevOps flavor, wrapped)
dotnet run --project src/tools/Oocx.TfPlan2Md.HtmlRenderer -- \
  --input artifacts/comprehensive-demo.md \
  --flavor azdo \
  --template src/tools/Oocx.TfPlan2Md.HtmlRenderer/templates/azdo-wrapper.html \
  --output artifacts/comprehensive-demo.azdo.html

# 2) Capture a screenshot with details expanded
DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1 dotnet run --project src/tools/Oocx.TfPlan2Md.ScreenshotGenerator -- \
  --input artifacts/comprehensive-demo.azdo.html \
  --output website/assets/screenshots/full-report-azdo.png \
  --open-details "details" \
  --full-page
```

## Actions
1. Pick the markdown report under `artifacts/` to use as the source.
2. Generate the required HTML exports with `src/tools/Oocx.TfPlan2Md.HtmlRenderer`.
3. Generate screenshots from the exported HTML with `src/tools/Oocx.TfPlan2Md.ScreenshotGenerator`.
4. Add/update `website/_memory/screenshots.md` with:
   - Screenshot file name
   - Exact commands used
   - Intended purpose (where it is used on the website)
