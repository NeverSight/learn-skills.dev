---
name: blur-image
description: "Use when the user wants to blur, redact, or anonymize parts of an image — screenshots with API keys, emails, PII, customer data, or any sensitive text. Also triggers on 'hide text in screenshot', 'redact image', 'blur sensitive', 'anonymize screenshot', 'prepare screenshot for sharing', or privacy-related image editing. Use this skill even if the user just says 'blur this' with an image file."
---

# Blur Image

Detect and blur sensitive regions in screenshots using AI vision + ImageMagick.

**Announce:** "I'm using the blur-image skill to identify and blur sensitive regions."

**Use when:** Blur, redact, anonymize, hide text in screenshots, prepare images for sharing, remove PII from images.

**Skip when:** Crop, resize, format conversion, color adjustments, or non-privacy image editing.

**Common mistake:** Output goes to `<name>-blurred.webp` by default, not overwriting the original. If the user expects in-place editing, they need to say so.

## How It Works

The skill combines two tools: AI vision finds sensitive text (the part humans miss), and ImageMagick blurs it (the part AI can't do with pixels). The workflow is: check prerequisites → scan the image → ask the user what to blur → **calibrate coordinates with a grid overlay** → run ImageMagick → verify the output by re-reading it → fix any misses.

## Critical Rules

| Do | Why |
|----|-----|
| Check `which magick` before running | ImageMagick 7+ is required; v6 uses different syntax |
| Run `magick identify -format '%wx%h\n'` first | Validates the file and gives you the coordinate space |
| **Calibrate coordinates with a grid overlay before blurring** | Visual estimation of pixel positions is routinely off by 15-25px. A 30-second grid overlay prevents multiple failed blur attempts. This is the single most common failure mode. |
| Use sigma >= 20 for blur, >= 50 with double-pass for terminal screenshots | Sigma below 10 is reversible with deblurring algorithms. High-contrast text (green on black) bleeds through even at sigma=35. |
| Anchor blur left edge right after the `=` or `:` delimiter | Padding left eats into labels — pad right and vertically instead. The delimiter is your anchor point. |
| Clamp regions to image edges | X >= 0, Y >= 0, X+W <= width, Y+H <= height |
| Present findings in plain language, not coordinates | Users think in "the email in the sidebar," not "240x18+350+92" |
| Ask 1-3 clarifying questions based on what you actually found | People have different sensitivity thresholds — one person's "public info" is another's PII |
| Read the output image back and verify each region | A blur that misses a few characters of an API key defeats the purpose |

## Phase 1: Preflight

1. Run `which magick`. If missing, show install instructions and **stop**:
   - macOS: `brew install imagemagick`
   - Ubuntu/Debian: `sudo apt install imagemagick`
   - Other: https://imagemagick.org/script/download.php
2. Run `magick identify -format '%wx%h\n' image.png` — validates the file, confirms format support (png, jpg, jpeg, webp, tiff), and returns pixel dimensions. If multiple lines appear, the image is animated — stop and tell the user (`-region` blur only affects the first frame)
3. Note the dimensions — Retina/HiDPI screenshots are often 2x logical resolution

## Phase 2: Identify and Discuss

This is the conversational heart of the skill. Scan the image, present what you found, and have a focused discussion about what needs blurring.

### Step 1: Scan the image

Read the image with multimodal vision. Look for anything that could identify a person, compromise a system, or reveal internal infrastructure:

- Credentials: API keys, tokens, passwords, connection strings, `.env` values, bearer tokens
- Personal data: emails, phone numbers, SSNs, names, physical addresses, dates of birth
- Financial: credit card numbers, bank accounts, billing info
- Infrastructure: internal hostnames, private IPs, file paths with usernames, internal URLs
- Business: customer names, account IDs, license keys, proprietary data

This list isn't exhaustive — use judgment. A hostname like `prod-db-3.internal.acme.co` is sensitive even though it's not on any checklist. Err toward flagging things the user can dismiss rather than missing things they'd want blurred.

### Step 2: Present findings

Group what you found by type. Describe in plain language — never show pixel coordinates, region dimensions, or the raw ImageMagick command:

```
I found sensitive content in 3 areas:

- .env values: 4 secret values after the = signs
  (DATABASE_URL, STRIPE_SECRET_KEY, SENDGRID_API_KEY, JWT_SECRET)
- Authorization header: Bearer token in the curl command
- API response: personal data (login, email, name fields)

Blur all of these? Or tell me which to skip.
```

### Step 3: Ask targeted questions

Ask 1-3 questions based on what you actually found. Don't run through a generic questionnaire — focus on the ambiguous cases in *this* image:

- **Structured content:** "Blur just the values after the = signs, or the entire lines?"
- **Partial vs full:** "The database URL has a hostname and password — blur the whole thing, or just the password?"
- **Borderline items:** "There's a person's name in the response — is that sensitive for your use case?"
- **Things you might have missed:** "Is there anything else you'd like blurred that I haven't mentioned?"

If the content is clearly all-sensitive (a screenshot is nothing but credentials), skip the questions and just confirm: "I'll blur all the credential values. Sound good?"

If you found nothing sensitive, say so and offer to blur specific content the user describes.

### User-guided mode

When the user specifies what to blur ("blur the email in the top right"), locate what they described, confirm what you'll blur, and also mention anything else sensitive you noticed: "I'll blur the email. I also see an API key in the terminal — want that blurred too?"

## Phase 3: Calibrate Coordinates

Visual estimation of pixel positions is the #1 failure mode — Y coordinates are routinely off by 15-25px, causing every blur region to land on the wrong line. A grid overlay takes 30 seconds and prevents multiple failed iterations.

**When to calibrate:** Always calibrate for multi-region structured content (terminals, config files, JSON, tables). For 1-2 large isolated regions ("blur that phone number at the top"), you can skip to Phase 4 — the region is big enough that small offsets don't matter.

### Step 1: Draw a calibration grid

Overlay lines at regular intervals. Scale the interval to the image — aim for 5-8 grid lines per axis:

| Image dimension | Interval |
|----------------|----------|
| < 500px | 50px |
| 500-1500px | 100px |
| > 1500px | 200px |

Generate the grid lines programmatically to cover the full image:

```bash
# Build grid commands dynamically based on image dimensions
# Example for 820x404 at 100px intervals:
magick input.png \
  -fill none -stroke red -strokewidth 1 \
  -draw 'line 100,0 100,404' -draw 'line 200,0 200,404' \
  -draw 'line 300,0 300,404' -draw 'line 400,0 400,404' \
  -draw 'line 500,0 500,404' -draw 'line 600,0 600,404' \
  -draw 'line 700,0 700,404' \
  -draw 'line 0,50 820,50' -draw 'line 0,100 820,100' \
  -draw 'line 0,150 820,150' -draw 'line 0,200 820,200' \
  -draw 'line 0,250 820,250' -draw 'line 0,300 820,300' \
  -draw 'line 0,350 820,350' \
  input-grid.webp
```

Use a color that contrasts with the image background — red for dark images, blue or black for light images.

Read the grid image back with vision. For each line of text you need to blur, note which grid lines it falls between. Derive:
- **Character width** — pick a long line, count its characters, measure how many grid cells it spans
- **Left margin** — where the first character starts relative to x=0
- **Line height and Y positions** — which horizontal grid lines each text line falls between

### Step 2: Verify with colored diagnostic rectangles

Using the coordinates derived from the grid, draw semi-transparent colored rectangles (one color per region) over the **original** image. Use a different color for each region so you can tell them apart:

```bash
magick input.png \
  -fill 'rgba(255,0,0,0.5)' -draw 'rectangle x1,y1 x2,y2' \
  -fill 'rgba(0,255,0,0.5)' -draw 'rectangle x1,y1 x2,y2' \
  -fill 'rgba(0,0,255,0.5)' -draw 'rectangle x1,y1 x2,y2' \
  input-diag.webp
```

Note: the `-draw 'rectangle'` syntax uses corner-to-corner coordinates `(x1,y1 x2,y2)`, while Phase 4's `-region` syntax uses `WxH+X+Y`. Convert between them: `W=x2-x1, H=y2-y1, X=x1, Y=y1`.

Read the diagnostic image back with vision. Check:
- Does each colored rectangle cover exactly the value portion of its target line?
- Are any rectangles landing on the wrong line (off by a full line height)?
- Are the left edges aligned with the delimiter (`=` or `:`) rather than clipping into the label?

If rectangles are misaligned, adjust coordinates and re-check. This is cheap — much cheaper than discovering misalignment after running the blur.

### Step 3: Proceed to blur

Keep the grid and diagnostic images until Phase 5 confirms the blur is correct — you may need them if re-calibration is required. Delete them after final verification.

## Phase 4: Blur

Build and run the ImageMagick command using the coordinates verified in Phase 3. The user already confirmed what to blur — don't ask again.

**Coordinate conversion:** If you calibrated with `-draw 'rectangle x1,y1 x2,y2'`, convert to `-region` format: `-region (x2-x1)x(y2-y1)+(x1)+(y1)`. Example: `rectangle 120,73 525,97` → `-region 405x24+120+73`.

**Per-line precision for structured content:** When blurring key=value pairs, JSON fields, or config lines, use a separate narrow `-region` per line targeting only the value portion. Size each region to its content — short values get narrow regions, long values get wide ones.

**Anchor the left edge at the delimiter:** The `=` or `:` character is your reference point — you already verified this position with diagnostic rectangles in Phase 3. Start the blur region right after it. Add 30-50px of padding to the **right** side and vertically, but do **not** pad left past the delimiter — that clips the label. The full label (`JWT_SECRET=`, `"email":`) should always be readable.

**Include value quotes in the blur:** For JSON values like `"email": "jane.doe@acmecorp.com"`, blur the value **including its surrounding quotes** — the visible portion should be `"email": ` and the blurred portion should cover `"jane.doe@acmecorp.com"` (both the opening and closing `"`). Leaving stray quotes visible at blur edges looks sloppy and can hint at value length.

**Command template:**
```bash
magick input.png \
  -region WxH+X+Y -gaussian-blur 0x30 \
  -region WxH+X+Y -gaussian-blur 0x30 \
  -strip -quality 85 output-blurred.webp
```

For terminal/high-contrast content, double-pass each region (repeat the same `-region` line twice in a row). Below, regions A and B are each blurred twice:
```bash
magick input.png \
  -region 405x24+120+73 -gaussian-blur 0x50 \
  -region 405x24+120+73 -gaussian-blur 0x50 \
  -region 273x24+157+91 -gaussian-blur 0x50 \
  -region 273x24+157+91 -gaussian-blur 0x50 \
  -strip -quality 85 output-blurred.webp
```

**Execution time:** Double-pass sigma=50 is computationally expensive — expect 1-3 minutes for 8+ regions. Run as a background command if available and don't retry thinking it failed.

**Sigma guide:**
| Content type | Sigma | Passes | Why |
|-------------|-------|--------|-----|
| Light text on light background | 20 | 1 | Low contrast, blurs easily |
| Dark text on white background | 20-25 | 1 | Standard documents, web pages |
| Terminal text (green/white on dark) | 50 | 2 | High contrast bleeds through at sigma=35 even with correct coordinates. Double-pass is essential. |
| Bright colored text on black | 50 | 2 | Very high contrast needs aggressive blur |

If the first attempt doesn't fully obscure the text (you'll check in the next phase), increase sigma or add a third pass.

**Solid fill alternative:** When the user asks for maximum security, or blur isn't working after adjustment, use solid fill — it replaces pixels entirely and can't be reversed. Sample the actual background color rather than guessing:
```bash
# Sample background color — pick coordinates in an obviously empty area
magick input.png -format '%[hex:p{X,Y}]' info:
# Use the sampled color (e.g., #1E1E2E) for the fill
```
Then apply with `-draw 'rectangle'` for clean, hard-edged redaction:
```bash
magick input.png -fill '#1E1E2E' \
  -draw 'rectangle x1,y1 x2,y2' \
  -draw 'rectangle x1,y1 x2,y2' \
  -strip -quality 85 output-blurred.webp
```
Note: solid fill looks like the content was deleted rather than redacted. Some users prefer the visual indication of Gaussian blur. If the user objects to the appearance, switch back to Gaussian blur with the verified coordinates.

**Non-text content (faces, logos, photos):** For blurring regions that aren't structured text — faces in photos, logos, handwritten notes, address labels — use a single large rectangular region covering the whole area. Calibration is usually unnecessary since the region is large and a few pixels of offset don't matter. Use sigma=30 for faces/photos (they blur easily due to smooth gradients) and sigma=20 for handwritten text. For faces, extend the region 20-30px beyond the face boundary so ears and hairline are also covered.

**Output:** Save as `<original-name>-blurred.webp` alongside the original. `-strip` removes EXIF metadata. Tell the user where the file will be saved before running.

If the user asks to overwrite the original, do so — but confirm first since it's irreversible.

## Phase 5: Verify and Fix

Read the output image back with vision and check each blurred region:

1. **Each region:** Can you still read any characters? Even partial text (a few letters, trailing digits, stray quotes) means the blur failed for that region.
2. **Edges:** Are characters peeking through at the borders? This is the most common failure — the region was slightly too narrow. For JSON values, the blur should cover the value's surrounding quotes too — stray `"` at blur edges means the region needs to extend a few pixels further.
3. **Missed content:** Scan the rest of the image for anything sensitive that wasn't in the original list. Fresh eyes on the blurred version sometimes catch things.
4. **Labels intact:** Confirm the full label is readable — `JWT_SECRET=`, not `JWT_SECR`. If a label is clipped, the blur region started too far left. Shift the region's X position right until the full label (including the `=` or `:`) is visible.

**Diagnosing failures — coordinates vs sigma:**

When blur regions don't obscure the text, the cause is almost always **wrong coordinates** rather than insufficient sigma. Two symptoms help distinguish:
- **Entire value visible** (no blur effect at all) → the region missed the text line entirely (Y coordinate is wrong, typically off by 15-25px). Go back to Phase 3 and re-calibrate with a grid overlay.
- **Partial characters leaking at edges** but center is blurred → coordinates are approximately right but need small X adjustments.
- **Text visible through the blur** (you can see a blur effect but still read the text) → sigma is genuinely too low. Increase sigma or add another pass.

**If something is wrong, fix it:**
- Entire region missed (text fully visible) → **re-run calibration grid** (Phase 3). Do not increase sigma — the coordinates are wrong.
- Text still visible through blur → increase sigma or add another pass
- Characters at edges → extend the region 20-30px in the leaking direction
- Label clipped → shift the region's X start to the right (never fix label clipping by shrinking — move the region)
- After 2 failed blur attempts on the same region → switch to solid fill for that region
- Re-run and re-verify the fix (don't assume it worked)

**When everything is clean:**
Delete any remaining calibration images (grid, diagnostic). Then report what was verified: "Saved to screenshot-blurred.webp. All 4 .env values fully obscured, variable names readable. Bearer token gone. JSON values blurred per-field, keys visible. Want me to adjust anything?"

## Example

```
User: blur the sensitive stuff in screenshot.png

Claude: I'm using the blur-image skill to identify and blur sensitive regions.

Preflight: magick found at /opt/homebrew/bin/magick (v7.1.2)
Image: screenshot.png (1920x1080 PNG)

I found sensitive content in 3 areas:

- .env values: 4 secret values after the = signs
  (DATABASE_URL, STRIPE_SECRET_KEY, SENDGRID_API_KEY, JWT_SECRET)
- Authorization header: Bearer token in the curl command
- API response: personal data (login, email, name fields)

For the .env lines — blur just the values after the = signs,
or the whole lines? And the API response has login, email,
and name — all three?

User: just the values after = and blur all three in the response

Claude: Calibrating coordinates with a grid overlay...

[draws grid at 100px intervals, reads back, derives char width ~7.5px,
 margin ~18px, line height ~20px, first text line at y≈75]

Verifying with diagnostic rectangles...

[draws colored rectangles on original, reads back, confirms all 8 regions
 align with target text — adjusts SENDGRID Y down 3px]

Running blur (double-pass sigma=50, this may take 1-2 minutes)...

✓ Saved to screenshot-blurred.webp

I've checked each region:
- All 4 .env values: fully obscured, full labels readable (DATABASE_URL=, STRIPE_SECRET_KEY=, etc.)
- Bearer token: fully obscured, "Authorization: Bearer" still visible
- JSON login, email, name: each blurred individually (including value quotes), keys and colons visible

Everything looks clean. Want me to adjust anything?
```
