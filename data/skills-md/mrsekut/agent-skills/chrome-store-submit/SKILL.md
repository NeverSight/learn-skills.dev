---
name: chrome-store-submit
description: Automate new Chrome extension submission to Chrome Web Store using playwright-mcp. Reads manifest.json and source code, generates store listing text in any language, creates store images, and fills all required forms via browser automation. Use when submitting a new Chrome extension to Chrome Web Store, publishing a Chrome extension, or filling Chrome Web Store developer dashboard forms.
---

# Chrome Web Store Submission

Automate the Chrome Web Store new extension submission process using playwright-mcp browser automation.

## Prerequisites

- playwright-mcp configured as MCP server. See [references/setup.md](references/setup.md) if not set up.
- Pillow installed (`pip install Pillow`) for image generation.
- Extension source code with valid `manifest.json` in the working directory.
- Extension packaged as ZIP file ready for upload.

## Workflow

1. **Gather extension info** from source code
2. **Create privacy policy page** — generate `PRIVACY_POLICY.md` and push to GitHub
3. **Launch browser** — user logs in — upload ZIP
4. **Scan all tabs** to identify required fields and current state
5. **Ask user** only for info that cannot be determined from source code
6. **Generate store images and listing text**
7. **Fill all forms** across all tabs
8. **Save as draft** and prompt user to review

## Step 1: Gather Extension Info

Read these files from the project to extract info:

```
manifest.json → name, short_name, description, permissions, version, icons
README.md → feature descriptions, usage details (if exists)
```

Extract:

- `name` (max 75 chars for store)
- `description` (used as short description, max 132 chars)
- `permissions` (needed for privacy justification)
- `version`
- `icons` (path to largest icon for image generation)

## Step 2: Create Privacy Policy Page

Chrome Web Store requires a privacy policy URL. Repository top pages or unrelated pages are not accepted as a valid privacy policy and will be rejected. A **dedicated privacy policy page** must be created.

### 2-1: Generate `PRIVACY_POLICY.md`

Based on `manifest.json` permissions and source code behavior gathered in Step 1, generate a `PRIVACY_POLICY.md` file in the extension's repository root.

Write the content in the user's target language (default to English if unknown), using the following structure:

```markdown
# Privacy Policy for <Extension Name>

Last updated: <today's date>

## Overview
<Extension Name> ("the Extension") is a browser extension that <1-sentence description>.

## Data Collection
<Based on permissions, specifically describe what data is collected. If no data is collected, explicitly state: "This extension does not collect, store, or transmit any personal data.">

## Data Usage
<Describe the purpose of collected data. If none is collected: "No user data is collected or used.">

## Data Storage
<Describe how and where data is stored. If local only, state that explicitly.>

## Data Sharing
<State whether data is shared with third parties. If not, state that explicitly.>

## Permissions
<Explain why each permission from manifest.json is needed, one line per permission.>

## Changes to This Privacy Policy
We may update this Privacy Policy from time to time. Any changes will be posted on this page with an updated revision date.

## Contact
If you have any questions about this Privacy Policy, please create an issue on the [GitHub repository](<repo URL>).
```

**Key points:**
- Even extensions with minimal permissions that collect no personal data must explicitly state so.
- Explain each permission's purpose individually (e.g., `activeTab` → "Used to access the current tab's content only when the user activates the extension").
- Avoid vague wording — be specific about what the extension does and does not do.

### 2-2: Push to GitHub and Get URL

1. Show the generated `PRIVACY_POLICY.md` to the user for review.
2. Ask the user to:
   - Git commit and push `PRIVACY_POLICY.md`.
   - Confirm the GitHub repository is **public** (private repository pages are not accessible).
3. Record the privacy policy URL in the format: `https://github.com/<owner>/<repo>/blob/main/PRIVACY_POLICY.md`

This URL will be used in Step 7 for the Privacy Practices tab.

**Note:** A GitHub repository top page (`https://github.com/<owner>/<repo>`) is not accepted as a valid privacy policy. Always use a direct link to the `PRIVACY_POLICY.md` file.

## Step 3: Browser Launch and Upload

1. Navigate to `https://chrome.google.com/webstore/devconsole`
2. Tell the user: "Please log in to your Google Developer account in the browser. Let me know when you're done."
3. Wait for user confirmation.
4. Click "New item" or equivalent upload button.
5. Use `browser_file_upload` to upload the ZIP file.
6. Wait for upload to complete and dashboard to load.

## Step 4: Scan All Tabs

After upload, navigate through all tabs in the dashboard to identify required fields.

1. **Store Listing tab**: Use `browser_snapshot` to check required fields and their current state.
2. **Privacy Practices tab**: Navigate via sidebar → `browser_snapshot`.
3. **Distribution tab**: Navigate via sidebar → `browser_snapshot`.

For each tab, record:
- Required field names and input types (text, dropdown, file upload, checkbox, etc.)
- Fields already populated (some are auto-filled from manifest.json)
- Empty required fields

## Step 5: Ask User for Missing Info

Cross-reference source code info from Step 1 with form state from Step 4. **Only ask the user about required fields that cannot be filled automatically.**

Fields likely determinable from source code (do not ask):
- Extension name, description (from manifest.json)
- Permission justifications (inferred from permissions + source code usage)
- Remote code declaration (typically No for MV3)
- Data collection status (inferred from permissions and source code)

Fields that typically require user input:
- **Target language** for store listing
- **Primary category**
- **Brand color** (hex, for image generation)
- **Visibility** (Public / Unlisted / Private)

**Privacy Policy URL** is already generated in Step 2 — no need to ask.

These are general tendencies only. Always decide based on actual form state. Do not ask unnecessary questions.

## Step 6: Generate Store Images and Listing Text

### Images

```bash
python3 scripts/generate_store_images.py <icon_path> <output_dir> --name "Extension Name" --color "#hexcolor"
```

This generates:

- `store_icon_128.png` (128x128, with 16px transparent padding)
- `promo_tile_440x280.png` (440x280, small promo tile)
- `marquee_1400x560.png` (1400x560, marquee tile)
- `screenshot_1280x800.png` (1280x800, placeholder screenshot)

Ask the user if they want to use these generated images or provide their own.

### Listing Text

Based on manifest.json info and README, generate in the user's target language:

- **Detailed description**: 2-4 paragraphs covering what the extension does, key features, and how to use it. No HTML, plain text only.
- **Single purpose description**: 1-2 sentences clearly stating the extension's primary functionality.
- **Permission justifications**: One sentence per permission explaining why it's needed.

Show all generated text to the user for approval before filling forms.

## Step 7: Fill All Forms

Navigate back to each tab and fill in the forms. Use `browser_snapshot` before each field interaction to verify the current state.

### Store Listing Tab

1. Fill **Detailed Description** textarea
2. Select **Primary Category** from dropdown
3. Select **Language** from dropdown
4. Upload **Store Icon** (128x128)
5. Upload **Screenshots** (1280x800)
6. Upload **Small Promo Tile** (440x280)
7. Optionally upload **Marquee Promo Tile**

### Privacy Practices Tab

1. Fill **Single Purpose Description**
2. Fill **Permission Justifications** (one per permission from manifest)
3. Set **Remote Code Declaration**
4. Handle **Data Usage Disclosures** and **Limited Use Certification**
5. Enter **Privacy Policy URL** (use the GitHub URL of `PRIVACY_POLICY.md` generated in Step 2)

### Distribution Tab

1. Set **Visibility** (Public/Unlisted/Private)
2. Set **Geographic Distribution** (default: All regions)

## Step 8: Save as Draft

1. Click "Save Draft" button (NOT "Submit for Review")
2. Verify save succeeded via `browser_snapshot`
3. Tell user: "Draft saved successfully. Please review all fields in the browser before submitting for review."

## Important Notes

- Always use `browser_snapshot` before interacting with page elements to find correct selectors.
- Chrome Web Store dashboard is a SPA; wait after navigation for content to load.
- If a form field is not found, take a screenshot and ask the user for guidance.
- Never click "Submit for Review" — only save as draft.
- For form field details and constraints, see [references/store-fields.md](references/store-fields.md).
