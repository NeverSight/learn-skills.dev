---
name: app-store-screenshot-studio
description: Capture real App Store screenshots via Xcode Build MCP, then generate App Store Connect-ready marketing screenshots with Nano Banana Pro (correct sizes, copy, compliance).
---

# App Store Screenshot Studio

A step-by-step workflow for producing App Store Connect-ready screenshot sets.

**Important:** This is a sequential workflow. Complete each step fully and get user confirmation before moving to the next. Do not skip ahead.

---

## Step 1: Create the Screenshot Brief

**Goal:** Define what screenshots to capture and what marketing copy to use.

### What to do

Create a brief with 5-10 frames. For each frame, specify:

| Field | Description |
|-------|-------------|
| frame_id | e.g., `01_hero`, `02_search` |
| screen | Which app screen/state to capture |
| headline | 2-5 words, benefit-led |
| subheadline | Optional, max 10 words |
| compliance_notes | IAP disclosure needed? Privacy wording? |

**Rules of thumb:**
- One idea per frame
- Strongest value prop first
- Keep text big and scannable
- Use fictional/demo data only
- Never misrepresent features the app doesn't have

See [REFERENCE_APPLE.md](REFERENCE_APPLE.md) for compliance guardrails.

### Checkpoint

**STOP and ask the user:**
> "Here's the screenshot brief. Does this capture the right screens and messaging? Any changes before I start capturing?"

Do NOT proceed to Step 2 until the user approves the brief.

---

## Step 2: Capture Raw Screenshots

**Goal:** Get real screenshots from the app running in a simulator.

### Gate: Verify Xcode Build MCP

Before proceeding, check if Xcode Build MCP tools are available (e.g., `xcodebuild_build`, `simulator_boot`, `simulator_screenshot`).

**If NOT available:**
```
STOP. I need Xcode Build MCP to capture screenshots from the simulator.

Install it with:
  claude mcp add XcodeBuildMCP npx xcodebuildmcp@latest

Or add to your MCP config (~/.claude.json):
  {
    "mcpServers": {
      "XcodeBuildMCP": {
        "command": "npx",
        "args": ["-y", "xcodebuildmcp@latest"]
      }
    }
  }

Alternatively, you can provide raw screenshots manually and I'll skip to Step 3.
```

### What to do

1. Build the app
2. Boot the correct simulator (see [STEP_2_CAPTURE.md](STEP_2_CAPTURE.md) for device selection)
3. Navigate to each screen in the brief
4. Capture screenshots

**Output convention:**
```
./screenshots/raw/<locale>/<device_category>/<frame_id>.png
```

Example: `./screenshots/raw/en-US/iphone_6_9/01_hero.png`

See [STEP_2_CAPTURE.md](STEP_2_CAPTURE.md) for detailed capture guidance.

### Checkpoint

**STOP and show the user the captured screenshots:**
> "Here are the raw screenshots I captured. Do these look correct? Any screens need to be recaptured?"

Do NOT proceed to Step 3 until the user confirms the raw screenshots are good.

---

## Step 3: Generate Draft Composites (1K)

**Goal:** Create low-resolution marketing composites for approval before investing in high-res.

### Gate: Verify Nano Banana Pro

Check if the Nano Banana Pro script exists:
```bash
ls ~/.claude/skills/nano-banana-pro/scripts/generate_image.py
```

**If NOT available:**
```
STOP. I need Nano Banana Pro to generate marketing composites.

Install it with:
  git clone --depth 1 https://github.com/steipete/agent-scripts /tmp/agent-scripts && \
    cp -r /tmp/agent-scripts/skills/nano-banana-pro ~/.claude/skills/ && \
    rm -rf /tmp/agent-scripts
```

### Gate: Verify GEMINI_API_KEY

Check if the API key is set:
```bash
echo $GEMINI_API_KEY | head -c 10
```

**If NOT available:**
```
STOP. Nano Banana Pro requires a Gemini API key.

Set it with:
  export GEMINI_API_KEY="your-key-here"

Get a key at: https://aistudio.google.com/apikey
```

### What to do

For each frame in the brief, generate a **1K draft**:

```bash
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --input-image "./screenshots/raw/en-US/iphone_6_9/01_hero.png" \
  --prompt "Your compositing prompt here" \
  --filename "./screenshots/drafts/en-US/iphone_6_9/01_hero.png" \
  --resolution 1K
```

**CRITICAL:**
- `--input-image` is MANDATORY. Never omit it.
- Use `--resolution 1K` for drafts (faster, cheaper).
- Output to `./screenshots/drafts/` (not `final/`).

See [STEP_3_COMPOSITE.md](STEP_3_COMPOSITE.md) for prompt templates.

### Checkpoint

**STOP and show the user the draft composites:**
> "Here are the 1K draft composites. Do these look good? Any changes to copy, layout, or style before I generate the high-res finals?"

Do NOT proceed to Step 4 until the user approves the drafts.

---

## Step 4: Generate Final Composites (2K/4K)

**Goal:** Re-generate approved drafts at full resolution.

### What to do

For each approved draft, regenerate at **2K** (or 4K for iPad):

```bash
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --input-image "./screenshots/raw/en-US/iphone_6_9/01_hero.png" \
  --prompt "Same prompt as draft" \
  --filename "./screenshots/final/en-US/iphone_6_9/01_hero.png" \
  --resolution 2K
```

**Output convention:**
```
./screenshots/final/<locale>/<device_category>/<index>_<slug>.png
```

### Validate before proceeding

Run these checks:
- [ ] All images are accepted pixel sizes (see [REFERENCE_SIZES.md](REFERENCE_SIZES.md))
- [ ] Format is .png or .jpg
- [ ] 1-10 images per device category
- [ ] No prices or competitor references in copy
- [ ] IAP disclosures present where needed

### Checkpoint

**STOP and show the user the final composites:**
> "Here are the final high-res composites. Ready to package for submission?"

---

## Step 5: Package for Submission

**Goal:** Produce submission-ready assets.

### What to do

1. Create a ZIP of `./screenshots/final/`
2. Generate a manifest file:

```json
{
  "locales": {
    "en-US": {
      "iphone_6_9": [
        "01_hero.png",
        "02_search.png",
        "03_detail.png"
      ]
    }
  }
}
```

### Final summary

End your response with:
1. What was generated (locales, device categories, counts)
2. File tree showing raw + final paths
3. Any compliance notes (IAP disclosures, etc.)
4. Recommended next steps

---

## Quick Reference

- [STEP_2_CAPTURE.md](STEP_2_CAPTURE.md) — Simulator setup, device selection, capture methods
- [STEP_3_COMPOSITE.md](STEP_3_COMPOSITE.md) — Nano Banana Pro prompts and templates
- [REFERENCE_APPLE.md](REFERENCE_APPLE.md) — Apple compliance checklist
- [REFERENCE_SIZES.md](REFERENCE_SIZES.md) — Accepted screenshot dimensions
