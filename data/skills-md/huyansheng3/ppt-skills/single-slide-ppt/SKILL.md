---
name: single-slide-ppt
description: Quick professional single-slide PowerPoint creator for concept visualization, comparisons, feature showcases, and decision frameworks. Use when users need to create "one-page PPT", "single slide presentation", "快速做个PPT", "做一页PPT", or want to visualize concepts like "before/after", "problem/solution", "feature grid", "process flow" in presentation format. Ideal for creating visual summaries, product pitches, architecture diagrams, or comparison slides.
---

# Single-Slide PowerPoint Creator

Create professional, visually engaging single-slide PowerPoint presentations using PptxGenJS.

## When to Use This Skill

- User requests "做一页PPT", "single slide", "create a PPT slide"
- Visualizing comparisons (before/after, old vs new, problem/solution)
- Feature showcases (grid layouts, capability matrices)
- Concept illustrations (workflows, architectures, frameworks)
- Decision frameworks or process flows

## Core Workflow

### 1. Understand Content Structure

Analyze the user's request to identify:
- Main message/title
- Key points or sections (typically 2-6 items)
- Natural groupings (left/right, grid, sequential)
- Visual metaphors (arrows, icons, cards)

### 2. Choose Design Pattern

Select a layout that matches the content structure:

**Comparison Layouts** (2 columns):
- Problem → Solution
- Before → After  
- Old → New
- Plugin → IDE

**Grid Layouts** (2x2, 2x3, 3x3):
- Feature showcase
- Capability matrix
- Multi-option comparison

**Sequential Flow**:
- Process steps
- Timeline
- Decision tree

**Single Focus**:
- Key metric
- Core concept
- Quote or statement

### 3. Design Color Palette

**Select 3-5 colors based on content theme:**

Content-driven palettes:
- **Technology**: Deep blue (#1a1a2e), purple (#4a00e0), accent (#8e2de2)
- **Problem/Solution**: Red (#ff6b6b) for problems, Green (#51cf66) for solutions
- **Professional**: Navy (#2C3E50), teal (#16A085), gold (#F39C12)
- **Creative**: Purple (#722880), pink (#D72D51), orange (#EB5C18)

**Color assignment:**
- Background: Dark (#1a1a2e) or light (#f5f5f5)
- Header: Primary brand color or gradient
- Problem/negative: Red/orange tones
- Solution/positive: Green/blue tones
- Accent: Complementary color for highlights

### 4. Enhance with Relevant Images (Optional)

When creating slides about technical concepts, products, or comparisons, consider adding relevant images to strengthen the message.

**When to use images:**
- Technical architecture diagrams (from official documentation)
- Product screenshots (before/after comparisons)
- Logo or brand assets (for product slides)
- Illustrations (to explain abstract concepts)
- Charts or graphs (data visualization)

**How to find and download images:**

```javascript
// Example: Download VSCode architecture diagram
// Use curl to download images from official sources
const { execSync } = require('child_process');

function downloadImage(url, outputPath) {
  try {
    execSync(`curl -o ${outputPath} "${url}"`, { stdio: 'inherit' });
    console.log(`Downloaded: ${outputPath}`);
    return true;
  } catch (error) {
    console.error(`Failed to download image: ${error.message}`);
    return false;
  }
}

// Example usage:
downloadImage(
  'https://code.visualstudio.com/assets/api/ux-guidelines/examples/architecture-containers.png',
  'workspace/vscode-architecture.png'
);
```

**Strategy for finding images:**
1. **Official documentation**: Search for "[Product Name] architecture documentation" or "[Product Name] official API documentation"
2. **GitHub repositories**: Look for diagrams in README.md or docs/ folders
3. **Technical blogs**: Find explanation diagrams from reputable sources
4. **Use search_web and fetch_web**: Search for relevant content and extract image URLs

**Adding images to slides:**

```javascript
// After downloading the image, add it to the slide
slide.addImage({
  path: 'workspace/downloaded-image.png',
  x: 0.5,    // X position in inches
  y: 1.5,    // Y position in inches
  w: 4.8,    // Width in inches
  h: 2.7     // Height in inches (maintain aspect ratio)
});

// Optional: Add caption
slide.addText('Image caption or source attribution', {
  x: 0.5, y: 4.25, w: 4.8, h: 0.3,
  fontSize: 9, color: '707070', italic: true,
  align: 'center'
});
```

**Best practices for images:**
- ✅ Use official sources (company websites, documentation)
- ✅ Maintain aspect ratio when resizing
- ✅ Add captions for context
- ✅ Ensure images support the narrative
- ❌ Don't use low-resolution images
- ❌ Don't overcrowd slides with too many images
- ❌ Don't use images without permission

### 5. Create Slide with PptxGenJS

```javascript
const pptxgen = require('pptxgenjs');
const { execSync } = require('child_process');
const path = require('path');

async function createSlide() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'Your Name';
  pptx.title = 'Slide Title';
  
  const slide = pptx.addSlide();
  
  // Background
  slide.background = { color: '1a1a2e' };
  
  // Header bar
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: '4a00e0' }
  });
  
  // Title
  slide.addText('Your Title Here', {
    x: 0.5, y: 0.18, w: 9, h: 0.5,
    fontSize: 26, bold: true, color: 'ffffff',
    fontFace: 'Arial'
  });
  
  // Optional: Add downloaded image
  // slide.addImage({
  //   path: 'workspace/image.png',
  //   x: 0.5, y: 1.5, w: 4.8, h: 2.7
  // });
  
  // Content sections...
  // [Add your content here following the patterns below]
  
  await pptx.writeFile({ fileName: 'output.pptx' });
}

createSlide().catch(console.error);
```

## Design Patterns Library

### Pattern: Comparison Cards (Left vs Right)

```javascript
// Left section - Problem/Before
slide.addText('🚫 Current State', {
  x: 0.4, y: 1.0, w: 4, h: 0.4,
  fontSize: 14, bold: true, color: 'ff6b6b'
});

// Card with left border accent
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 0.4, y: 1.5, w: 4.2, h: 0.95,
  fill: { color: '2d1f1f' }
});
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 0.4, y: 1.5, w: 0.08, h: 0.95,
  fill: { color: 'ff6b6b' }
});
slide.addText('Issue Title', {
  x: 0.6, y: 1.55, w: 3.8, h: 0.3,
  fontSize: 12, bold: true, color: 'ff6b6b'
});
slide.addText('Detailed description...', {
  x: 0.6, y: 1.85, w: 3.8, h: 0.5,
  fontSize: 9, color: 'a0a0a0', wrap: true
});

// Right section - Solution/After (mirror structure with green)
slide.addText('✅ New State', {
  x: 5.3, y: 1.0, w: 4, h: 0.4,
  fontSize: 14, bold: true, color: '51cf66'
});
// [Add cards using green color scheme]
```

### Pattern: Feature Grid (2x3)

```javascript
const features = [
  { icon: '🔧', text: 'Feature 1' },
  { icon: '⚡', text: 'Feature 2' },
  { icon: '💻', text: 'Feature 3' },
  { icon: '📝', text: 'Feature 4' },
  { icon: '👻', text: 'Feature 5' },
  { icon: '🎨', text: 'Feature 6' }
];

const startX = 1.0;
const startY = 1.5;
const itemW = 2.6;
const itemH = 0.7;
const gapX = 0.15;
const gapY = 0.12;

features.forEach((feat, idx) => {
  const col = idx % 3;
  const row = Math.floor(idx / 3);
  const x = startX + col * (itemW + gapX);
  const y = startY + row * (itemH + gapY);
  
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x, y, w: itemW, h: itemH,
    fill: { color: '1a2a1a' },
    line: { color: '51cf66', width: 0.5 },
    rectRadius: 0.08
  });
  
  slide.addText(feat.icon + ' ' + feat.text, {
    x: x + 0.1, y: y + 0.15, w: itemW - 0.2, h: itemH - 0.3,
    fontSize: 11, color: 'e0e0e0', valign: 'middle'
  });
});
```

### Pattern: Visual Comparison Boxes

```javascript
// Before box (dashed border)
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 1.5, y: 3.0, w: 2.5, h: 1.5,
  fill: { color: '2a1a1a' },
  line: { color: 'ff6b6b', width: 1, dashType: 'dash' }
});
slide.addText('Before', {
  x: 1.5, y: 3.1, w: 2.5, h: 0.3,
  fontSize: 12, bold: true, color: 'ff6b6b', align: 'center'
});
slide.addText('🧩', {
  x: 1.5, y: 3.5, w: 2.5, h: 0.5,
  fontSize: 32, align: 'center'
});
slide.addText('Old approach', {
  x: 1.5, y: 4.0, w: 2.5, h: 0.3,
  fontSize: 9, color: '888888', align: 'center'
});

// After box (solid border)
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 6.0, y: 3.0, w: 2.5, h: 1.5,
  fill: { color: '1a2a1a' },
  line: { color: '51cf66', width: 2 }
});
slide.addText('After', {
  x: 6.0, y: 3.1, w: 2.5, h: 0.3,
  fontSize: 12, bold: true, color: '51cf66', align: 'center'
});
slide.addText('👑', {
  x: 6.0, y: 3.5, w: 2.5, h: 0.5,
  fontSize: 32, align: 'center'
});
slide.addText('New approach', {
  x: 6.0, y: 4.0, w: 2.5, h: 0.3,
  fontSize: 9, color: '888888', align: 'center'
});
```

### Pattern: Arrow Connector

```javascript
// Arrow between sections
slide.addText('➔', {
  x: 4.5, y: 2.5, w: 0.8, h: 0.6,
  fontSize: 36, color: '8e2de2',
  align: 'center', valign: 'middle'
});
```

## Visual Design Best Practices

### Typography
- **Titles**: 22-28pt, bold, high contrast
- **Section headers**: 12-16pt, bold
- **Body text**: 9-11pt, medium weight
- **Captions**: 8-9pt, lighter color

### Spacing & Alignment
- Header height: 0.7-0.9 inches
- Section margins: 0.4-0.5 inches from edges
- Card padding: 0.1-0.15 inches internal
- Grid gaps: 0.08-0.15 inches

### Color Usage
- **Maximum 5 colors** per slide
- Use transparency for layering: `rgba(R,G,B,0.1)` becomes `RRGGBB` + lighter fill
- Ensure text contrast ratio > 4.5:1 (use #e0e0e0 text on dark backgrounds)

### Visual Hierarchy
1. Title/header (largest, highest contrast)
2. Section headers (medium, color-coded)
3. Content cards (grouped, bordered)
4. Supporting text (smallest, lower contrast)

## Common Slide Types

### 1. Problem → Solution Slide
- Left: Problem cards (red theme)
- Middle: Arrow connector
- Right: Solution features (green theme)
- Bottom: Core value proposition

### 2. Feature Showcase
- Header with product name
- 2x3 or 3x3 grid of features
- Each cell: icon + short description
- Optional: Key benefit card at bottom

### 3. Before/After Comparison
- Title explaining transformation
- Side-by-side comparison boxes
- Visual indicators (emoji/icons)
- Arrow showing progression

### 4. Process Flow
- Sequential numbered cards
- Arrows between steps
- Color progression (gradient)
- End state highlighted

### 5. Technical Architecture Slide (with Images)
- Header with architecture name
- **Official architecture diagram** (downloaded from docs)
- Caption with source attribution
- Key points or limitations highlighted in cards

**Example: VSCode Extension Limitations Slide**

```javascript
const pptxgen = require('pptxgenjs');
const { execSync } = require('child_process');
const path = require('path');

async function createTechnicalSlide() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  
  // Download VSCode architecture image
  const imageUrl = 'https://code.visualstudio.com/assets/api/ux-guidelines/examples/architecture-containers.png';
  const imagePath = 'workspace/vscode-architecture.png';
  
  try {
    execSync(`curl -o ${imagePath} "${imageUrl}"`, { stdio: 'inherit' });
  } catch (error) {
    console.log('Image download failed, continuing without image');
  }
  
  const slide = pptx.addSlide();
  slide.background = { color: 'FFFFFF' };
  
  // Header
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: 'fc5a1f' }
  });
  
  slide.addText('VSCode 插件架构限制', {
    x: 0.5, y: 0.18, w: 9, h: 0.45,
    fontSize: 26, bold: true, color: 'ffffff',
    fontFace: 'Arial'
  });
  
  // Left: Architecture image
  slide.addImage({
    path: imagePath,
    x: 0.5, y: 1.2, w: 4.8, h: 2.7
  });
  
  slide.addText('VSCode 只对插件开放固定的"插槽"（Containers）', {
    x: 0.5, y: 4.0, w: 4.8, h: 0.3,
    fontSize: 10, color: '707070', italic: true,
    align: 'center'
  });
  
  // Right: Limitation cards
  slide.addText('API 限制', {
    x: 5.5, y: 1.2, w: 4.2, h: 0.4,
    fontSize: 18, bold: true, color: 'fc5a1f'
  });
  
  // Add limitation cards...
  
  await pptx.writeFile({ fileName: 'technical-slide.pptx' });
}

createTechnicalSlide().catch(console.error);
```

## Execution Checklist

- [ ] Analyze content to identify structure
- [ ] Choose appropriate design pattern
- [ ] Select color palette matching theme
- [ ] **Search for relevant images** (if needed for technical/product content)
- [ ] **Download images** using curl or web tools
- [ ] Create PptxGenJS script (include image paths)
- [ ] Run script to generate .pptx
- [ ] Generate thumbnail preview
- [ ] Validate visual quality
- [ ] Deliver file and preview to user

## File Output

Save files in a dedicated workspace:
```bash
mkdir -p workspace
cd workspace
node generate-slide.js
```

Generate preview:
```bash
python3 /path/to/pptx/scripts/thumbnail.py output.pptx preview --cols 1
```

## Modifying Existing PPT Files

### Why PptxGenJS Can't Edit Existing Files?

**Technical Reasons:**
1. **Design Focus**: PptxGenJS is a "generation" library focused on creating PPTs from scratch
2. **Complex File Structure**: .pptx files are ZIP archives containing multiple XML files (Office Open XML format)
3. **Relationship Handling**: Editing requires parsing complex relationships between slides, shapes, media, etc.

### Solution: Use `pptx-automizer` for Editing Existing Files

**pptx-automizer** is a powerful Node.js library specifically designed for editing and merging existing .pptx files.

#### Installation

```bash
npm install pptx-automizer
# or
yarn add pptx-automizer
```

#### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Load Templates** | Import existing .pptx files as templates |
| **Merge Slides** | Selectively add slides from multiple templates |
| **Modify Elements** | Locate and modify shapes by name or creationId |
| **Modify Text** | Replace text, use tag-based replacement |
| **Modify Images** | Replace image sources, resize |
| **Modify Tables** | Update table data and styles |
| **Modify Charts** | Update chart data (including extended chart types) |
| **Import Slide Masters** | Preserve original styles and layouts |
| **PptxGenJS Integration** | Use PptxGenJS to create elements on templates |

#### Basic Example: Load and Modify Existing PPT

```javascript
import Automizer from 'pptx-automizer';

const automizer = new Automizer({
  templateDir: 'path/to/templates',
  outputDir: 'path/to/output',
  // Keep existing slides (don't truncate)
  removeExistingSlides: false,
});

let pres = automizer
  // Load root template (output will be based on this)
  .loadRoot('MyPresentation.pptx')
  // Load same file again to modify its slides
  .load('MyPresentation.pptx', 'myPres');

// Add slide 2 from template and modify it
pres.addSlide('myPres', 2, (slide) => {
  // Modify element by shape name
  slide.modifyElement('Title', [
    modify.setText('Updated Title Text'),
  ]);
  
  slide.modifyElement('ContentBox', [
    modify.replaceText([{
      replace: '{{placeholder}}',
      by: { text: 'Dynamic Content' }
    }])
  ]);
});

// Write output
pres.write('UpdatedPresentation.pptx').then(summary => {
  console.log(summary);
});
```

#### Modify Single Slide in Existing PPT

```javascript
import Automizer, { modify, ModifyTextHelper } from 'pptx-automizer';

async function modifySingleSlide(inputFile, slideNumber, modifications) {
  const automizer = new Automizer({
    templateDir: './',
    outputDir: './',
    removeExistingSlides: true, // Start fresh
  });

  // Load the file twice - as root and as template
  let pres = automizer
    .loadRoot(inputFile)
    .load(inputFile, 'source');

  // Get all slide numbers
  const slideNumbers = await pres
    .getTemplate('source')
    .getAllSlideNumbers();

  // Re-add all slides, modifying only the target slide
  for (const num of slideNumbers) {
    if (num === slideNumber) {
      // Apply modifications to target slide
      pres.addSlide('source', num, modifications);
    } else {
      // Keep other slides unchanged
      pres.addSlide('source', num);
    }
  }

  // Write to new file (or same file)
  await pres.write(inputFile.replace('.pptx', '-modified.pptx'));
}

// Usage:
await modifySingleSlide('plugin-to-ide.pptx', 1, (slide) => {
  slide.modifyElement('Title', [
    ModifyTextHelper.setText('New Title'),
  ]);
});
```

#### Modify Chart Data in Existing PPT

```javascript
import Automizer, { modify } from 'pptx-automizer';

pres.addSlide('charts', 2, (slide) => {
  slide.modifyElement('ColumnChart', [
    modify.setChartData({
      series: [
        { label: 'Q1 Sales' },
        { label: 'Q2 Sales' },
      ],
      categories: [
        { label: 'Product A', values: [150, 180] },
        { label: 'Product B', values: [200, 220] },
        { label: 'Product C', values: [130, 160] },
      ],
    }),
  ]);
});
```

#### Replace Images in Existing PPT

```javascript
import Automizer, { ModifyImageHelper, ModifyShapeHelper, CmToDxa } from 'pptx-automizer';

const automizer = new Automizer({
  templateDir: 'templates',
  outputDir: 'output',
  mediaDir: 'images', // Directory for external images
});

let pres = automizer
  .loadRoot('Template.pptx')
  .loadMedia(['new-image.png']) // Load external image
  .load('Template.pptx', 'template');

pres.addSlide('template', 1, (slide) => {
  slide.modifyElement('ImagePlaceholder', [
    // Replace image source
    ModifyImageHelper.setRelationTarget('new-image.png'),
    // Optionally adjust size
    ModifyShapeHelper.setPosition({
      w: CmToDxa(8),
      h: CmToDxa(6),
    }),
  ]);
});

pres.write('UpdatedWithNewImage.pptx');
```

#### Use Tag-Based Text Replacement

PowerPoint shapes can contain placeholder tags like `{{title}}` that get replaced:

```javascript
pres.addSlide('template', 1, (slide) => {
  slide.modifyElement('TextWithTags', [
    modify.replaceText([
      { replace: 'title', by: { text: 'My Dynamic Title' } },
      { replace: 'date', by: { text: '2026-02-28' } },
      { replace: 'author', by: { text: 'Your Name' } },
    ]),
  ]);
});
```

### Comparison: PptxGenJS vs pptx-automizer

| Feature | PptxGenJS | pptx-automizer |
|---------|-----------|----------------|
| Create from scratch | ✅ Excellent | ⚠️ Limited (wraps PptxGenJS) |
| Edit existing files | ❌ No | ✅ Yes |
| Merge templates | ❌ No | ✅ Yes |
| Preserve styles | ❌ N/A | ✅ Yes |
| Modify charts | ❌ No | ✅ Yes |
| Tag replacement | ❌ No | ✅ Yes |
| Learning curve | Low | Medium |

### Recommended Workflow

**For creating new PPTs**: Use PptxGenJS
**For editing existing PPTs**: Use pptx-automizer
**For hybrid workflows**: Use pptx-automizer with PptxGenJS integration

```javascript
// pptx-automizer can wrap PptxGenJS for creating new elements
pres.addSlide('template', 1, (slide) => {
  // Use pptxgenjs to add new shapes from scratch
  slide.generate((pptxGenJSSlide, pptxGenJs) => {
    pptxGenJSSlide.addText('New Text Box', {
      x: 1, y: 1, w: 3, h: 0.5,
      fontSize: 14, color: '333333'
    });
    
    pptxGenJSSlide.addChart(pptxGenJs.ChartType.bar, chartData, {
      x: 4, y: 1, w: 5, h: 3
    });
  });
});
```

### Shape Selection Methods

#### By Shape Name (Simple)
```javascript
slide.modifyElement('MyShapeName', [ /* modifiers */ ]);
```

#### By creationId (Robust)
```javascript
// More stable - survives slide rearrangement
slide.modifyElement('{E43D12C3-AD5A-4317-BC00-FDED287C0BE8}', [ /* modifiers */ ]);
```

#### With Fallback
```javascript
slide.modifyElement({
  creationId: '{E43D12C3-AD5A-4317-BC00-FDED287C0BE8}',
  name: 'MyShapeName', // Fallback if creationId not found
}, [ /* modifiers */ ]);
```

### Best Practices

1. **Template Management**: Keep a library of well-designed .pptx templates
2. **Shape Naming**: Give shapes meaningful names in PowerPoint (ALT+F10 to open Selection Pane)
3. **Tag Convention**: Use consistent tag format like `{{tagName}}`
4. **Version Control**: Track changes to templates in git
5. **Preview After Edit**: Always generate thumbnails to verify changes
6. **Error Handling**: Handle missing shapes gracefully

## Notes

- **No # prefix in colors**: Use `"ff6b6b"` not `"#ff6b6b"` (causes corruption)
- **Web-safe fonts only**: Arial, Helvetica, Times New Roman, Georgia, Courier New, Verdana
- **Test emoji support**: Some emoji may not render on all platforms
- **16:9 aspect ratio**: Standard for most presentations (10 x 5.625 inches)
- **pptx-automizer**: Use for editing existing .pptx files
- **PptxGenJS**: Use for creating new presentations from scratch
