---
name: feature-image
argument-hint: [feature description]
description: "Generate a branded social media image announcing a new feature or update. Analyzes git history, auto-detects brand from codebase (Tailwind, CSS vars, design tokens), replicates UI elements, and captures via Playwright. Use when the user wants to create an announcement image, says 'feature image,' 'announcement graphic,' 'social image for feature,' or wants to visually announce a code change."
---

Generate a branded social media image for announcing a feature or update. The image is built as an HTML page styled to match the project's brand, then screenshotted with Playwright.

## Phase 1: Ensure Playwright is Available

```bash
npx playwright --version 2>/dev/null || (echo "Installing Playwright..." && npx playwright install chromium)
```

If installation fails, inform the user and suggest `npm install -D playwright && npx playwright install chromium`.

## Phase 2: Understand What Changed (Git-Aware)

Analyze the recent git history to understand what feature/update to announce:

1. **Check recent commits:**
   ```bash
   git log --oneline -20
   ```

2. **Check current diff (staged + unstaged):**
   ```bash
   git diff HEAD --stat
   git diff HEAD -- '*.tsx' '*.jsx' '*.vue' '*.svelte' '*.html' '*.css' '*.scss' '*.rb' '*.erb'
   ```

3. **Check recent branch name** (often describes the feature):
   ```bash
   git branch --show-current
   ```

4. **Synthesize** what the feature/update is from this context.

5. **Present findings to user** with `AskUserQuestion`:
   - Header: "Feature"
   - Question: "Based on recent changes, it looks like you're working on [X]. What should this announcement be about?"
   - Options:
     - "[Auto-detected feature description]" - Use what was detected
     - "Something else" - Let user describe it
   - If `$1` was provided as an argument, use that instead of asking.

## Phase 3: Auto-Generate Announcement Text

Generate text elements for the image:

- **Headline**: A punchy, short headline (3-8 words) about the feature
- **Tagline**: A one-sentence supporting description
- **Badge/Label**: Optional category label (e.g., "New Feature", "Update", "Improvement")

Present these to the user with `AskUserQuestion`:
- Header: "Copy"
- Question: "Here's the text I'd put on the image. Want to adjust anything?"
- Options:
  - "Looks good" - Use as-is
  - "Edit headline" - User provides custom headline
  - "Edit everything" - User provides all text
  - "No text overlay" - Generate image without text

## Phase 4: Choose Platform & Size

Use `AskUserQuestion`:
- Header: "Platform"
- Question: "What platform is this image for?"
- Options:
  - "Twitter/X (1200x675)" - Standard Twitter card size
  - "LinkedIn (1200x627)" - LinkedIn share image
  - "Instagram (1080x1080)" - Square format
  - "Open Graph (1200x630)" - Universal social preview

Store the chosen width and height for the Playwright viewport.

## Phase 5: Choose Visual Style

Use `AskUserQuestion`:
- Header: "Style"
- Question: "What visual style should the image use?"
- Options:
  - "Stylized mockup (Recommended)" - Simplified, polished recreation of UI elements using the app's actual components and CSS. Recognizable but not pixel-perfect.
  - "Screenshot + overlay" - Takes a real screenshot of the running app and adds branded text overlays, gradients, and annotations.
  - "Abstract/illustrative" - Uses brand colors and typography to create a geometric or gradient design that suggests the feature without replicating specific UI.

### Style: Stylized Mockup

This is the most involved style. The goal is to create a representation of the UI that *feels* like the app without being a literal screenshot.

1. **Find relevant UI components** related to the feature:
   - Search for component files that match the feature (e.g., if the feature is "dark mode", find theme toggle components)
   - Read the component markup to understand the UI structure
   - Note key visual elements: buttons, cards, inputs, tables, navigation items

2. **Extract visual patterns from components:**
   - Border radius values
   - Shadow styles
   - Specific layout patterns (sidebar + main, card grids, etc.)
   - Icon usage
   - Interactive element styles (buttons, toggles, inputs)

3. **Build a simplified HTML mockup** that:
   - Shows the key UI elements of the feature in a stylized, editorial layout
   - Uses the actual brand colors, fonts, and border-radius from the codebase
   - Adds subtle visual polish (soft shadows, slight gradients, generous whitespace)
   - Frames the UI in a "browser window" or "device frame" if appropriate
   - Is NOT a full working page -- it's a curated, art-directed composition

### Style: Screenshot + Overlay

1. Ask the user for the URL of the running app (suggest common localhost URLs)
2. Navigate to the relevant page with Playwright
3. Take a base screenshot
4. Create an HTML overlay page that:
   - Embeds the screenshot as a background image
   - Adds a gradient overlay (using brand colors) for text readability
   - Places headline and tagline text on top
   - Adds a badge/label if applicable
5. Screenshot the overlay page

### Style: Abstract/Illustrative

Build an HTML page with:
- A gradient or geometric background using brand colors
- The project logo (if found in `/public`, `/assets`, or `/src/assets`)
- Large, bold headline text using the project's font
- Supporting tagline
- Abstract shapes, lines, or patterns that evoke the feature category
- Clean, modern aesthetic with generous whitespace

## Phase 6: Deep Brand Analysis

This is the most important phase. Spend real time here. The generated image must feel like it was made by the same team that built the product -- not a generic template with brand colors swapped in. The goal is to internalize the brand's visual identity so deeply that the image is indistinguishable from something the design team would produce.

### 6.1: Study Existing Marketing Materials First

Before looking at config files, study how the brand actually presents itself. These are your primary references:

1. **Landing pages and marketing pages** -- search for:
   - `pages/index`, `app/page`, `pages/home`, `components/landing/`, `components/marketing/`, `components/hero`
   - Any files with `landing`, `marketing`, `home`, `hero`, `cta` in the name
   - Read these files thoroughly. Note the exact tone, layout patterns, how they compose text + visuals, gradient directions, decorative elements, background treatments

2. **Existing social/OG images** -- search for:
   - `og-image`, `social`, `share`, `twitter`, `preview` in `/public` or `/assets`
   - Any existing announcement or marketing images in the repo
   - These are your strongest reference for what the brand considers "on-brand" for social

3. **Blog or changelog pages** -- search for:
   - `blog`, `changelog`, `updates`, `announcements` in page/route files
   - These show how the brand communicates updates -- mirror this tone and style

4. **Email templates** -- search for:
   - `email`, `mailer`, `newsletter` templates
   - These reveal another facet of the brand's visual language

5. **README and docs** -- check for badges, banner images, or styled headers that reveal brand personality

### 6.2: Color Palette

Extract the full color system, not just primary/secondary:

1. **Tailwind config** (`tailwind.config.js`, `tailwind.config.ts`):
   - Read the entire `theme.extend.colors` block
   - Note the full palette: primary, secondary, accent, neutral, success, warning, error
   - Pay attention to color *relationships* -- how does the brand pair colors?

2. **CSS custom properties** (search for `:root` in global CSS files):
   - Look for `--primary`, `--brand`, `--accent`, `--background`, `--foreground`, `--muted`, `--card` or similar
   - Extract HSL/RGB/hex values
   - Note if there are separate light/dark mode palettes

3. **Design token files** (search for `tokens`, `theme`, `design-system` in filenames):
   - Extract color definitions and semantic mappings

4. **Actual usage in marketing components**:
   - Read hero sections, CTA buttons, feature cards, pricing tables
   - Note which colors are used for backgrounds vs. text vs. accents vs. borders
   - Look for gradient definitions -- exact stops, directions, and where they're used
   - Find the brand's "signature" color combinations (e.g., dark bg + bright accent, soft pastels, bold primaries)

### 6.3: Typography

1. **Font imports** (search for `@import` with font URLs, `@font-face`, or Google Fonts links)
2. **Tailwind fontFamily config**
3. **CSS font-family declarations** on body/headings
4. **Package.json** for font packages (e.g., `@fontsource/*`, `next/font`)
5. **Actual heading styles** -- read marketing page headings to see:
   - Font weight (bold? black? medium?)
   - Letter spacing (tight? normal? wide?)
   - Text transform (uppercase? normal?)
   - Line height
   - How headlines are sized relative to body text

For the image, use the detected font. If it's a Google Font, include the `<link>` tag in the HTML. If it's a local/custom font, fall back to a similar system font or Google Font alternative.

### 6.4: Logo & Assets

Search for logo files:
```
public/logo*, public/images/logo*, src/assets/logo*, assets/logo*
public/*.svg (check for logo-like SVGs)
public/brand*, src/assets/brand*
```

If a logo is found, embed it in the image (inline SVG or base64-encoded).

Also look for:
- Icon libraries or custom icon sets used in the app
- Illustration styles (line art? filled? duotone?)
- Background patterns or textures
- Decorative elements (dots, grids, blobs, rings)

### 6.5: Visual Language & Patterns

Go beyond basic config -- study the visual *personality* of the brand:

- **Border radius**: Is the app rounded (`rounded-xl`, `rounded-2xl`) or sharp (`rounded-none`, `rounded-sm`)? Use the exact same radii.
- **Shadows**: Soft/elevated or flat? What shadow values are used? (e.g., `shadow-lg` vs `shadow-sm` vs no shadow)
- **Dark mode**: Is dark mode the default or primary theme? What's the background color?
- **Gradients**: Are gradients used prominently? What direction, what colors, where?
- **Glass/blur effects**: Any `backdrop-blur` usage? Translucent cards?
- **Borders**: Are borders used for separation or are things borderless? What color/opacity?
- **Spacing rhythm**: Is the design dense and compact or airy with lots of whitespace?
- **Decorative elements**: Does the brand use background grids, dot patterns, glow effects, noise textures, gradient orbs?
- **Animation style**: While animation won't appear in the image, the *feel* of a brand that uses smooth spring animations vs. no animations tells you about its personality

### 6.6: Synthesize a Brand Brief

Before building the image, write a short internal summary of the brand's visual identity:

- "This brand uses [dark/light] backgrounds with [color] accents. Typography is [font] at [weight], [tight/normal] letter spacing. The aesthetic is [minimal/bold/playful/corporate]. Key visual motifs include [gradients/glass/sharp corners/etc]. Marketing pages use [layout pattern] with [decorative elements]."

Use this brief as your guide for every design decision in the image. Every element should pass the test: "Would this look at home on their landing page?"

## Phase 7: Build the HTML Image Page

**Unique temp files:** To avoid race conditions when multiple agents run in parallel, generate a slug-based ID for this run. Format: `{project-slug}-{feature-slug}-{short-id}` where project slug comes from the directory name or package.json name, feature slug is a 2-3 word kebab-case summary of the feature, and short ID is 4-6 random alphanumeric chars. Example: `baremetrics-dark-mode-a3f2`. Use this slug in all temp file paths below (shown as `[UNIQUE_ID]`). Both the HTML file and the capture script must use the same slug.

Create a self-contained HTML file at `/tmp/feature-image-[UNIQUE_ID]-page.html` that:

1. **Is exactly the chosen dimensions** (viewport-sized, no scroll)
2. **Embeds all styles inline** (no external CSS dependencies)
3. **Includes fonts via Google Fonts link** (or similar CDN)
4. **Uses the detected brand colors, fonts, and visual patterns**
5. **Contains the chosen text overlay** (headline, tagline, badge)
6. **Matches the chosen visual style** (mockup, screenshot+overlay, or abstract)

### HTML Structure Template

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link href="https://fonts.googleapis.com/css2?family=[DETECTED_FONT]&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body {
      width: [WIDTH]px;
      height: [HEIGHT]px;
      overflow: hidden;
      font-family: '[DETECTED_FONT]', system-ui, sans-serif;
    }
    body {
      background: [BRAND_GRADIENT_OR_COLOR];
      color: [TEXT_COLOR];
      display: flex;
      /* Layout depends on style choice */
    }
    /* ... style-specific CSS ... */
  </style>
</head>
<body>
  <!-- Content depends on style choice -->
</body>
</html>
```

### Design Quality Guidelines

The image should look like it was designed by a professional. Follow these principles:

- **Hierarchy**: Headline is the largest element. Tagline supports it. Badge is small.
- **Contrast**: Text must be easily readable against the background.
- **Alignment**: Use a clear grid. Left-align or center consistently.
- **Polish**: Subtle shadows, smooth gradients, refined typography (letter-spacing, line-height).
- **Restraint**: Don't use more than 2-3 colors. Don't use more than 2 font weights.

### Space Usage (CRITICAL)

These images will be viewed at small sizes in social feeds, timeline cards, and link previews. Every pixel matters. Dead space is wasted space.

**Mandatory rules:**

1. **Fill the canvas.** Content should use 85-95% of the available area. Padding should be tight -- 40-60px max on a 1200px-wide image, not 100+.
2. **Make text BIG.** Headlines should be 48-72px minimum (at 1x). If the headline is short (3-4 words), go even bigger -- 80-100px. The text needs to be readable at thumbnail size (~400px wide). If you squint at the image and can't read the headline, it's too small.
3. **No empty centers.** If the layout has a headline on top and a UI mockup on the bottom, don't leave a big gap in the middle. Stack elements tightly or fill the space with supporting content.
4. **UI mockups should be large.** If showing a stylized UI element, it should take up at least 50-60% of the image area. Don't render a tiny card floating in a sea of background gradient.
5. **Edge-to-edge when appropriate.** UI mockups can bleed off the edges of the canvas -- this looks more dynamic and uses space better than centering everything with margins.
6. **Badge/label text should be 14-18px**, not smaller. It needs to be visible.
7. **Test at thumbnail size.** Before finalizing, mentally shrink the image to 400px wide. Can you still read the headline? Can you tell what the UI shows? If not, make things bigger.

**Common mistakes to avoid:**
- A small headline centered in the middle of a large background -- scale it up, push it to a corner or edge
- A UI mockup that's 30% of the canvas surrounded by gradient -- make it dominant
- Excessive padding that makes content feel like it's floating in space
- Tagline text at 14-16px -- bump it to 20-24px minimum
- Using the same spacing between all elements instead of grouping related items tightly

## Phase 8: Screenshot with Playwright

Create and run a Node.js script:

```javascript
import { chromium } from 'playwright';
import { readFileSync } from 'fs';

async function capture() {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: [WIDTH], height: [HEIGHT] },
    deviceScaleFactor: 2, // Retina quality
  });
  const page = await context.newPage();

  // Load the HTML file
  const html = readFileSync('/tmp/feature-image-[UNIQUE_ID]-page.html', 'utf-8');
  await page.setContent(html, { waitUntil: 'networkidle' });

  // Wait for fonts to load
  await page.waitForTimeout(1000);

  await page.screenshot({
    path: './feature-image.png',
    type: 'png',
  });

  await browser.close();
  console.log('Saved: ./feature-image.png');
}

capture().catch(console.error);
```

Save the script to `/tmp/feature-image-[UNIQUE_ID]-capture.mjs`, run it, then clean up:

```bash
node /tmp/feature-image-[UNIQUE_ID]-capture.mjs && rm /tmp/feature-image-[UNIQUE_ID]-capture.mjs /tmp/feature-image-[UNIQUE_ID]-page.html
```

## Phase 9: Verify & Present

1. **Check the file exists and has reasonable size:**
   ```bash
   ls -la ./feature-image.png
   sips -g pixelWidth -g pixelHeight ./feature-image.png 2>/dev/null || file ./feature-image.png
   ```

2. **Read the image** using the Read tool to show it to the user.

3. **Ask if adjustments are needed** with `AskUserQuestion`:
   - Header: "Result"
   - Question: "Here's your feature image. What do you think?"
   - Options:
     - "Looks great" - Done
     - "Adjust colors" - Tweak the color palette
     - "Adjust text" - Change headline/tagline
     - "Try different style" - Switch to another visual style
   - If adjustments are needed, go back to the relevant phase and regenerate.

4. **Output summary:**
   ```
   Generated: ./feature-image.png
   Size: [W]x[H] @ 2x ([actual_W]x[actual_H] pixels)
   Platform: [chosen platform]
   Style: [chosen style]
   ```

## Error Handling

- **Playwright not found after install attempt**: Suggest manual installation with `npm install -D playwright && npx playwright install chromium`
- **No git history**: Skip git analysis, ask user directly what the feature is
- **No brand colors found**: Fall back to a clean, neutral palette (dark background, white text, blue accent)
- **No fonts detected**: Fall back to Inter (Google Font) as a safe, modern default
- **Screenshot fails**: Check if the HTML file was created correctly, try with a simpler layout
- **Font not loading in screenshot**: Increase the wait timeout, or fall back to system fonts

## Tips for Best Results

1. Run this skill from within the project directory so brand detection works
2. If the app has a running dev server, the "Screenshot + overlay" style will produce the most authentic results
3. For abstract style, the skill works well even without UI components to reference
4. The generated image is 2x resolution (retina) -- it will look sharp on all screens
