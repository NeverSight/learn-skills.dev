---
name: visual-digest
description: Generate branded visual digests (posters/emails) from markdown activity reports. Use when running /visual-digest, /poster, or when user wants a shareable visual version of a digest.
---

# Visual Digest Generator

Transform markdown digest files into polished, branded visuals for sharing via email, Slack, or as posters.

## When to Use

- Running `/visual-digest [date]` or `/poster [date]` commands
- User asks for "shareable version" of a digest
- Creating email-ready weekly summaries
- Generating Slack-friendly visual updates

## AskElephant Brand Guidelines

### Colors

| Element        | Color       | Hex                    |
| -------------- | ----------- | ---------------------- |
| Background     | Light Gray  | `#F5F5F5`              |
| Primary Text   | Near Black  | `#1A1A1A`              |
| Secondary Text | Medium Gray | `#6B7280`              |
| Accent (CTA)   | Lime Green  | `#BFFF00` or `#D4FF00` |
| Success        | Green       | `#22C55E`              |
| Warning        | Amber       | `#F59E0B`              |
| Cards          | White       | `#FFFFFF`              |
| Borders        | Light       | `#E5E7EB`              |

### Typography

- **Headlines**: Inter Bold, 32-48px
- **Section Headers**: Inter Semibold, 20-24px
- **Body**: Inter Regular, 14-16px
- **Stats/Numbers**: Inter Bold, 36-64px (for big metrics)
- **Captions**: Inter Regular, 12px, gray

### Logo Usage

- Black elephant icon with "AskElephant" wordmark
- Logo should appear in header
- Minimum clear space: 1x logo height on all sides

### Layout Principles

- Generous whitespace (24-48px padding)
- Card-based sections with subtle shadows
- Left-aligned text (no center alignment for body)
- Clear visual hierarchy
- Maximum 2-3 sections visible without scrolling

## Visual Formats

### 1. Email Digest (600px wide)

```
┌────────────────────────────────────┐
│  🐘 AskElephant                    │
│  Weekly Digest • Week XX, 2026    │
├────────────────────────────────────┤
│                                    │
│  🏆 HEADLINE                       │
│  ━━━━━━━━━━━━━━━━━━━━━            │
│  [Main achievement in large text]  │
│                                    │
├────────────────────────────────────┤
│                                    │
│  📊 THIS WEEK'S NUMBERS            │
│  ┌─────┐ ┌─────┐ ┌─────┐          │
│  │ 21  │ │  6  │ │ 14  │          │
│  │feat.│ │impr.│ │bugs │          │
│  └─────┘ └─────┘ └─────┘          │
│                                    │
├────────────────────────────────────┤
│                                    │
│  ✨ NEW FEATURES                   │
│  • Feature 1                       │
│  • Feature 2                       │
│                                    │
│  🔧 IMPROVEMENTS                   │
│  • Improvement 1                   │
│                                    │
│  🐛 BUGS FIXED                     │
│  • Bug fix 1                       │
│                                    │
├────────────────────────────────────┤
│  👥 Team • Coming Next             │
└────────────────────────────────────┘
```

### 2. Poster/Slack Visual (1200x630px - Social Preview)

```
┌──────────────────────────────────────────────────┐
│                                                  │
│   🐘 AskElephant Weekly                          │
│                                                  │
│   ┌────────────────────────────────────────┐    │
│   │                                        │    │
│   │   "Dialpad Integration Now Live"       │    │
│   │                                        │    │
│   │   21 Features • 6 Improvements • 14 Bugs│    │
│   │                                        │    │
│   └────────────────────────────────────────┘    │
│                                                  │
│   Week 4 • January 20-24, 2026                  │
│                                                  │
└──────────────────────────────────────────────────┘
```

### 3. Full Poster (Portrait - 800x1200px)

For printing or high-res sharing with all sections visible.

## Generation Procedure

### Step 1: Parse Markdown Digest

Extract from the digest file:

1. **Title/Date** - From header (e.g., "Week 4: January 20-24, 2026")
2. **Headline** - From "WEEK'S HEADLINE" or "TODAY'S HEADLINE" section
3. **Stats** - Features count, Improvements count, Bugs count
4. **Features List** - Items under "NEW FEATURES"
5. **Improvements List** - Items under "IMPROVEMENTS"
6. **Bugs Summary** - Count and highlights from "BUGS FIXED"
7. **Team Contributions** - Names and focus areas
8. **Coming Next** - Future items

### Step 2: Generate Image Prompt

Use the GenerateImage tool with a detailed prompt:

```
Professional business newsletter visual for AskElephant (B2B meeting intelligence platform).

Style:
- Clean, modern SaaS design
- Light gray (#F5F5F5) background
- White cards with subtle shadows
- Inter or similar sans-serif font
- Black text with lime green (#BFFF00) accents
- Professional but approachable

Layout:
- AskElephant logo (black elephant icon) in top left
- "Weekly Digest" header with date
- Large headline quote in center card
- Three stat boxes showing: [X] Features, [X] Improvements, [X] Bugs Fixed
- Clean typography hierarchy
- Minimal decoration, lots of whitespace

Content:
- Headline: "[HEADLINE TEXT]"
- Stats: [X] Features, [X] Improvements, [X] Bugs Fixed
- Date: [DATE RANGE]

Do NOT include:
- Stock photos of people
- Generic tech imagery
- Busy backgrounds
- Multiple colors (keep monochrome + green accent)
```

### Step 3: Save Output

Save generated visual to:

- `pm-workspace-docs/status/activity/visuals/digest-YYYY-MM-DD.png`
- `pm-workspace-docs/status/activity/visuals/digest-YYYY-WXX.png`

## Command Options

| Command                     | Description                                |
| --------------------------- | ------------------------------------------ |
| `/visual-digest`            | Generate visual for most recent digest     |
| `/visual-digest YYYY-MM-DD` | Generate visual for specific daily digest  |
| `/visual-digest YYYY-WXX`   | Generate visual for specific weekly digest |
| `/poster`                   | Alias for `/visual-digest`                 |
| `--format email`            | Optimize for email (600px wide)            |
| `--format social`           | Optimize for social/Slack (1200x630px)     |
| `--format poster`           | Full poster format (800x1200px)            |

## Example Prompt for Week 4 Digest

```
Professional weekly newsletter poster for AskElephant, a B2B meeting intelligence SaaS platform.

Design specifications:
- Dimensions: 1200x630 pixels (social media preview size)
- Background: Light warm gray (#F5F5F5)
- Cards: White with very subtle shadow
- Typography: Modern sans-serif (Inter-style)
- Accent color: Bright lime green (#D4FF00) for highlights
- Overall feel: Clean, professional, minimal

Layout (top to bottom):
1. Header bar: Black elephant logo icon + "AskElephant" wordmark + "Weekly Digest" badge
2. Main card (centered):
   - Large quote: "Dialpad Integration Now Live"
   - Subtext: "Customers using Dialpad can now connect their telephony directly to AskElephant"
3. Stats row: Three pill-shaped badges showing:
   - "21 Features" (green accent)
   - "6 Improvements"
   - "14 Bugs Fixed"
4. Footer: "Week 4 • January 20-24, 2026"

Visual style:
- NO stock photos or people
- NO busy patterns or gradients
- Clean vector-style graphics only
- High contrast text for readability
- Professional B2B SaaS aesthetic
```

## HTML Email Template (Alternative)

For email platforms that support HTML, generate this template:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>AskElephant Weekly Digest</title>
    <style>
      body {
        font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif;
        background: #f5f5f5;
        margin: 0;
        padding: 24px;
      }
      .container {
        max-width: 600px;
        margin: 0 auto;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
      }
      .header {
        background: #1a1a1a;
        color: white;
        padding: 24px;
        display: flex;
        align-items: center;
        gap: 12px;
      }
      .logo {
        font-weight: bold;
        font-size: 18px;
      }
      .badge {
        background: #d4ff00;
        color: #1a1a1a;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 600;
      }
      .headline {
        padding: 32px 24px;
        border-bottom: 1px solid #e5e7eb;
      }
      .headline h1 {
        font-size: 24px;
        margin: 0 0 8px 0;
        color: #1a1a1a;
      }
      .headline p {
        color: #6b7280;
        margin: 0;
        font-size: 14px;
      }
      .stats {
        display: flex;
        padding: 24px;
        gap: 16px;
        background: #fafafa;
      }
      .stat {
        flex: 1;
        text-align: center;
        padding: 16px;
        background: white;
        border-radius: 8px;
      }
      .stat-number {
        font-size: 32px;
        font-weight: bold;
        color: #1a1a1a;
      }
      .stat-label {
        font-size: 12px;
        color: #6b7280;
        text-transform: uppercase;
      }
      .section {
        padding: 24px;
        border-bottom: 1px solid #e5e7eb;
      }
      .section h2 {
        font-size: 14px;
        text-transform: uppercase;
        color: #6b7280;
        margin: 0 0 16px 0;
        letter-spacing: 0.5px;
      }
      .section ul {
        margin: 0;
        padding: 0;
        list-style: none;
      }
      .section li {
        padding: 8px 0;
        color: #1a1a1a;
        font-size: 14px;
      }
      .footer {
        padding: 24px;
        text-align: center;
        color: #6b7280;
        font-size: 12px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <span class="logo">🐘 AskElephant</span>
        <span class="badge">Weekly Digest</span>
      </div>

      <div class="headline">
        <h1>{{HEADLINE}}</h1>
        <p>{{HEADLINE_DESCRIPTION}}</p>
      </div>

      <div class="stats">
        <div class="stat">
          <div class="stat-number">{{FEATURES_COUNT}}</div>
          <div class="stat-label">Features</div>
        </div>
        <div class="stat">
          <div class="stat-number">{{IMPROVEMENTS_COUNT}}</div>
          <div class="stat-label">Improvements</div>
        </div>
        <div class="stat">
          <div class="stat-number">{{BUGS_COUNT}}</div>
          <div class="stat-label">Bugs Fixed</div>
        </div>
      </div>

      <div class="section">
        <h2>✨ New Features</h2>
        <ul>
          {{#each FEATURES}}
          <li>{{this}}</li>
          {{/each}}
        </ul>
      </div>

      <div class="section">
        <h2>🔧 Improvements</h2>
        <ul>
          {{#each IMPROVEMENTS}}
          <li>{{this}}</li>
          {{/each}}
        </ul>
      </div>

      <div class="footer">{{DATE_RANGE}} • For the AskElephant team</div>
    </div>
  </body>
</html>
```

## Reference Assets

Brand assets location:

- Logo: `.cursor/skills/visual-digest/assets/askelephant-logo.png`
- Screenshots: `~/.cursor/projects/.../assets/` (user-provided examples)

## Integration

### With Activity Reporter

After generating a digest, suggest:

```
Would you like me to create a visual version for sharing?
Run /visual-digest to generate an email/poster version.
```

### Output Locations

| Format           | Location                                       |
| ---------------- | ---------------------------------------------- |
| Generated images | `pm-workspace-docs/status/activity/visuals/`   |
| HTML templates   | `pm-workspace-docs/status/activity/templates/` |

## Error Handling

### Missing Digest

```
No digest found for [date].
Run /eod --digest or /eow --digest first to generate the markdown digest.
```

### Image Generation Failed

```
Image generation failed. Creating HTML template instead.
[Save HTML to templates/ folder]
```
