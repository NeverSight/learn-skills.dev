---
name: drawio-to-png
description: Convert draw.io diagram files (.drawio, .dio, .xml) to high-resolution PNG images. Use when users ask to "convert drawio to png", "export drawio diagrams", "generate png from drawio", "drawio导出png", "转换drawio图片", "生成高清drawio图片", or need to convert draw.io files to image format for documentation, presentations, or publishing.
version: 1.0.0
---

# Draw.io to PNG Converter

Convert draw.io diagram files to high-resolution PNG images using draw.io desktop command-line interface or headless browser automation.

## Overview

This skill provides guidance for converting draw.io format files (.drawio, .dio, .xml) to high-quality PNG images. It supports batch conversion, custom resolution settings, transparent backgrounds, and page selection for multi-page diagrams.

## When to Use

Use this skill when:
- Converting draw.io diagrams to PNG for documentation
- Exporting diagrams for presentations or articles
- Generating images from draw.io files for web publishing
- Batch processing multiple diagram files
- Creating high-DPI images for print materials

## Trigger Phrases

- "convert drawio to png"
- "export drawio diagram"
- "generate png from drawio"
- "drawio导出png"
- "转换drawio图片"
- "drawio转图片"
- "生成高清drawio图片"
- "批量导出drawio"

## Conversion Methods

### Method 1: Using draw.io Desktop CLI (Recommended)

The official draw.io desktop application provides a command-line interface for conversion.

**Installation**:
```bash
# macOS
brew install --cask drawio

# Or download from: https://github.com/jgraph/drawio-desktop/releases
```

**Basic Conversion**:
```bash
# Convert single file
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -o output.png input.drawio

# With custom scale (higher DPI)
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -s 2 -o output.png input.drawio

# Transparent background
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png --transparent -o output.png input.drawio

# Export specific page (for multi-page diagrams)
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -p 0 -o output.png input.drawio
```

**Parameters**:
- `-x`: Export mode
- `-f png`: Output format (png)
- `-o`: Output file path
- `-s <scale>`: Scale factor (1.0 = 100%, 2.0 = 200%, etc.)
- `--transparent`: Transparent background
- `-p <page>`: Page index (0-based) for multi-page diagrams
- `-w <width>`: Custom width in pixels
- `-h <height>`: Custom height in pixels
- `--border <size>`: Border size in pixels

### Method 2: Using Puppeteer with draw.io Web

Use headless browser automation to render diagrams via draw.io web interface.

**Installation**:
```bash
npm install puppeteer
```

**Conversion Script** (see `scripts/convert-with-puppeteer.js`):
```javascript
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function convertDrawioToPng(inputPath, outputPath, options = {}) {
  const {
    scale = 2,
    transparent = true,
    page = 0
  } = options;

  const browser = await puppeteer.launch();
  const browserPage = await browser.newPage();
  
  // Set viewport for high DPI
  await browserPage.setViewport({
    width: 1920,
    height: 1080,
    deviceScaleFactor: scale
  });

  // Read drawio file
  const drawioContent = fs.readFileSync(inputPath, 'utf8');
  const encoded = encodeURIComponent(drawioContent);
  
  // Load in draw.io viewer
  await browserPage.goto(`https://viewer.diagrams.net/?lightbox=1&edit=_blank#R${encoded}`);
  
  // Wait for diagram to render
  await browserPage.waitForSelector('.geDiagramContainer', { timeout: 10000 });
  await browserPage.waitForTimeout(1000);

  // Take screenshot
  const element = await browserPage.$('.geDiagramContainer');
  await element.screenshot({
    path: outputPath,
    omitBackground: transparent
  });

  await browser.close();
}
```

### Method 3: Using @diagram.net/drawio-cli (Docker)

Official Docker-based CLI tool.

**Installation**:
```bash
docker pull rlespinasse/drawio-cli
```

**Conversion**:
```bash
docker run --rm -v "$(pwd):/data" rlespinasse/drawio-cli \
  -x -f png -s 2 -o /data/output.png /data/input.drawio
```

## Workflow

### Single File Conversion

1. **Detect draw.io file format**
   - Check if file exists and is valid (.drawio, .dio, .xml)
   - Verify file is XML format and contains draw.io structure

2. **Determine output path**
   - Default: same directory, same name with .png extension
   - Ask user if custom output path is needed

3. **Configure options**
   - Scale factor (default: 2 for high DPI)
   - Transparent background (default: true)
   - Page selection (if multi-page)

4. **Execute conversion**
   - Use draw.io CLI (Method 1) as primary method
   - Fall back to Puppeteer if CLI not available

5. **Verify output**
   - Check PNG file was created
   - Validate file size is reasonable
   - Show output path to user

### Batch Conversion

1. **Scan directory for draw.io files**
   ```bash
   find . -type f \( -name "*.drawio" -o -name "*.dio" -o -name "*.xml" \)
   ```

2. **Filter valid draw.io files**
   - Exclude non-diagram XML files
   - Check file content for draw.io structure

3. **Process each file**
   - Use same naming convention (replace extension with .png)
   - Apply consistent export settings
   - Track success/failure for each file

4. **Report results**
   - List successfully converted files
   - Report any failures with reasons
   - Show total count and output location

## Common Use Cases

### For Documentation
```bash
# Export with border for better visibility
drawio -x -f png -s 2 --border 10 -o docs/images/architecture.png architecture.drawio
```

### For Presentation Slides
```bash
# High resolution with transparent background
drawio -x -f png -s 3 --transparent -o slides/diagram.png diagram.drawio
```

### For Web Publishing
```bash
# Moderate resolution to balance quality and file size
drawio -x -f png -s 1.5 -o public/images/flowchart.png flowchart.drawio
```

### Multi-page Diagrams
```bash
# Export all pages
for i in {0..4}; do
  drawio -x -f png -s 2 -p $i -o "output-page-$i.png" multi-page.drawio
done
```

## Quality Settings

### Scale Factor Guidelines
- `1.0`: Standard resolution (72-96 DPI) - web thumbnails
- `2.0`: High resolution (144-192 DPI) - standard export (recommended)
- `3.0`: Very high resolution (216-288 DPI) - presentations
- `4.0`: Print quality (288-384 DPI) - professional printing

### File Size Considerations
- Higher scale = larger file size
- Transparent background slightly increases size
- Complex diagrams with many shapes = larger files
- Consider compression for web use

## Error Handling

### Common Issues

1. **draw.io CLI not found**
   - Check if draw.io desktop is installed
   - Verify path: `/Applications/draw.io.app/Contents/MacOS/draw.io` (macOS)
   - Try alternative methods (Puppeteer or Docker)

2. **Invalid draw.io file**
   - Verify file is XML format
   - Check for corrupted file content
   - Open in draw.io desktop to validate

3. **Export fails silently**
   - Check disk space
   - Verify write permissions for output directory
   - Try with simpler diagram to isolate issue

4. **Blank or partial output**
   - Increase wait time for complex diagrams
   - Check for external image references
   - Verify all fonts are available

## Best Practices

1. **Version Control**
   - Keep .drawio source files in version control
   - Regenerate PNG files on demand (don't commit)
   - Use CI/CD to auto-generate images

2. **Naming Convention**
   - Use same name for .drawio and .png files
   - Add suffix for different scales: `diagram-2x.png`, `diagram-3x.png`
   - Include page number for multi-page: `flow-page-1.png`

3. **Automation**
   - Create npm scripts or Makefile for batch conversion
   - Watch for file changes and auto-regenerate
   - Integrate with documentation build process

4. **Optimization**
   - Use appropriate scale for use case
   - Compress PNG files with tools like `pngquant` or `optipng`
   - Consider SVG export for web (smaller, scalable)

## Alternative Formats

While this skill focuses on PNG export, draw.io also supports:
- **SVG**: Vector format, scalable, smaller file size
- **PDF**: Print-ready, preserves quality
- **JPEG**: Smaller size, no transparency, lossy compression

Use `scripts/convert.sh` for flexible format selection.

## References

See `references/` directory for:
- **cli-reference.md**: Complete draw.io CLI documentation
- **quality-guide.md**: Detailed quality and DPI guidelines
- **automation-examples.md**: Scripts for CI/CD integration

## Examples

See `examples/` directory for:
- **single-file.sh**: Single file conversion example
- **batch-convert.sh**: Batch conversion script
- **watch-and-convert.sh**: File watcher for auto-conversion
