---
name: blecsd-media
description: Render images, GIFs, PNGs, and video in the terminal with @blecsd/media. Covers GIF/PNG parsing, ANSI rendering, image widgets, video playback, and W3M overlay.
license: MIT
metadata:
  author: blecsd
  version: "2.0.0"
---

# @blecsd/media Package Skill

The `@blecsd/media` package provides image parsing, rendering, and video playback for blECSd terminal applications. It includes complete GIF and PNG parsers, ANSI rendering to 256-color terminal, animated image widgets, video player integration (mpv/mplayer), and W3M overlay support.

**Install:** `pnpm add @blecsd/media`
**Peer dependency:** `blecsd >= 0.7.0`

## Subpath Imports

The package exposes focused subpath imports:

```typescript
import { parseGIF, frameToRGBA } from '@blecsd/media/gif';
import { parsePNG, extractPixels } from '@blecsd/media/png';
import { renderToAnsi, scaleBitmap, rgbTo256Color } from '@blecsd/media/render';
import { createImage, setImageData, play, pause } from '@blecsd/media/widgets/image';
import { createVideo, detectVideoPlayer } from '@blecsd/media/widgets/video';
import { createW3MOverlay } from '@blecsd/media/overlay';
```

Or use the namespace API from the main entry:

```typescript
import { gif, png, ansiRender, imageWidget, videoWidget, w3m } from '@blecsd/media';
```

## GIF Parser

Complete GIF parser with LZW decompression and animation support.

```typescript
import { parseGIF, frameToRGBA, validateGIFSignature } from '@blecsd/media/gif';

// Read file
const buffer = await fs.readFile('animation.gif');

// Validate
if (!validateGIFSignature(buffer)) throw new Error('Not a GIF');

// Parse
const result = parseGIF(buffer);
// result: { header, frames[], globalColorTable }

// Get RGBA pixels for a frame
const rgba = frameToRGBA(result.frames[0]);
// rgba: Uint8Array of [r, g, b, a, r, g, b, a, ...]
```

**Key functions:**
- `parseGIF(buffer)` - Parse full GIF with animation frames
- `parseGIFHeader(buffer)` - Parse header only
- `validateGIFSignature(buffer)` - Check GIF87a/GIF89a signature
- `frameToRGBA(frame)` - Convert frame to RGBA pixel data
- `deinterlace(pixels, width, height)` - Deinterlace interlaced frames
- `parseColorTable(buffer, offset, size)` - Parse color table
- `readSubBlocks(buffer, offset)` - Read GIF sub-blocks
- `decompressLZW(data, minCodeSize)` - LZW decompression
- `createBitReader(data)` / `readCode(reader, codeSize)` - Bit-level reading

## PNG Parser

Complete PNG parser with filter reconstruction.

```typescript
import { parsePNG, extractPixels, parseChunks } from '@blecsd/media/png';

const buffer = await fs.readFile('image.png');
const result = parsePNG(buffer);
// result: { header (IHDR), pixels, chunks[] }

// Or parse step by step
const chunks = parseChunks(buffer);
const header = parseIHDR(chunks[0].data);
const pixels = extractPixels(chunks);
```

**Key functions:**
- `parsePNG(buffer)` - Parse full PNG
- `parseChunks(buffer)` - Parse PNG chunks
- `parseIHDR(data)` - Parse image header (width, height, bitDepth, colorType)
- `reconstructFilters(scanlines, width, height, bitDepth)` - Reconstruct PNG filters
- `paethPredictor(a, b, c)` - PNG Paeth predictor
- `extractPixels(chunks)` - Extract raw pixel data
- `parsePLTE(buffer)` - Parse palette chunk

## ANSI Rendering

Convert bitmap data to terminal-renderable ANSI output.

```typescript
import { renderToAnsi, scaleBitmap, cellMapToString, rgbTo256Color } from '@blecsd/media/render';

// Render bitmap to ANSI cells
const cellMap = renderToAnsi(bitmap, {
  width: 40,        // Target width in terminal columns
  height: 20,       // Target height in terminal rows
  mode: 'halfblock' // 'halfblock' | 'braille' | 'ascii'
});

// Convert to string for output
const output = cellMapToString(cellMap);

// Scale a bitmap
const scaled = scaleBitmap(bitmap, 40, 20);

// Color conversion
const color256 = rgbTo256Color(255, 128, 0); // RGB to 256-color palette
const lum = rgbLuminance(255, 128, 0);       // Compute luminance
const char = luminanceToChar(lum);            // Map to ASCII char

// Blend colors
const blended = blendWithBackground([255, 128, 0], [0, 0, 0]);
```

**RenderMode options:**
- `'halfblock'` - Uses half-block characters for 2 pixels per cell vertically
- `'braille'` - Uses braille characters for 2x4 pixels per cell (highest density)
- `'ascii'` - Uses ASCII characters mapped by luminance

## Image Widget

High-level widget for displaying static and animated images.

```typescript
import { createImage, setImageData, play, pause, stop } from '@blecsd/media/widgets/image';

// Create image widget
const eid = createImage(world, {
  position: { x: 0, y: 0 },
  dimensions: { width: 40, height: 20 },
  renderMode: 'halfblock',
});

// Set image data (from parsed GIF/PNG)
setImageData(eid, {
  frames: gifResult.frames.map(f => frameToRGBA(f)),
  width: gifResult.header.width,
  height: gifResult.header.height,
  frameCount: gifResult.frames.length,
  delays: gifResult.frames.map(f => f.delay),
});

// Animation control (for animated GIFs)
play(eid);
pause(eid);
stop(eid);

// Set specific frame
setFrame(eid, 3);

// Get current state
const bitmap = getImageBitmap(eid);
const cellMap = getImageCellMap(eid);

// Aspect ratio helper
const { width, height } = calculateAspectRatioDimensions(
  sourceWidth, sourceHeight,
  targetWidth, targetHeight
);

// Cleanup
clearImageCache(eid);
clearAllImageCaches();

// Type guard
if (isImage(world, eid)) { /* ... */ }
```

## Video Widget

Video playback using external players (mpv or mplayer).

```typescript
import { createVideo, detectVideoPlayer, getVideoPlaybackState } from '@blecsd/media/widgets/video';

// Auto-detect available video player
const player = detectVideoPlayer(); // 'mpv' | 'mplayer' | undefined

// Create video widget
const eid = createVideo(world, {
  position: { x: 0, y: 0 },
  dimensions: { width: 80, height: 24 },
  source: '/path/to/video.mp4',
  player: player,        // 'mpv' | 'mplayer'
  autoplay: true,
});

// Check state
const state = getVideoPlaybackState(eid); // 'stopped' | 'playing' | 'paused'

// Get detected player
const detectedPlayer = getVideoPlayer(eid);

// Build command args (for manual control)
const args = buildMpvArgs({ source: 'video.mp4', width: 80, height: 24 });
const args2 = buildMplayerArgs({ source: 'video.mp4' });
const args3 = buildPlayerArgs({ source: 'video.mp4', player: 'mpv' });

// Send commands to running player
sendPauseCommand(handle);
sendSeekCommand(handle, 10); // Seek 10 seconds

// Type guard
if (isVideo(world, eid)) { /* ... */ }
```

## W3M Overlay

Use W3M's terminal graphics protocol for high-quality image display.

```typescript
import { createW3MOverlay } from '@blecsd/media/overlay';

const eid = createW3MOverlay(world, {
  position: { x: 0, y: 0 },
  dimensions: { width: 40, height: 20 },
  imagePath: '/path/to/image.png',
});
```

## Common Patterns

### Display a GIF in Terminal

```typescript
import { parseGIF, frameToRGBA } from '@blecsd/media/gif';
import { renderToAnsi, cellMapToString, scaleBitmap } from '@blecsd/media/render';

const buffer = await fs.readFile('cat.gif');
const gif = parseGIF(buffer);

for (const frame of gif.frames) {
  const rgba = frameToRGBA(frame);
  const bitmap = { data: rgba, width: gif.header.width, height: gif.header.height };
  const scaled = scaleBitmap(bitmap, 40, 20);
  const cellMap = renderToAnsi(scaled, { mode: 'halfblock' });
  console.log(cellMapToString(cellMap));
}
```

### Display a PNG

```typescript
import { parsePNG } from '@blecsd/media/png';
import { renderToAnsi, cellMapToString } from '@blecsd/media/render';

const buffer = await fs.readFile('photo.png');
const png = parsePNG(buffer);
const cellMap = renderToAnsi(
  { data: png.pixels, width: png.header.width, height: png.header.height },
  { width: 60, height: 30, mode: 'braille' }
);
console.log(cellMapToString(cellMap));
```

## Best Practices

1. **Choose the right render mode.** `braille` gives highest density (2x4 pixels per cell), `halfblock` is the default and works well for most images, `ascii` is most compatible.
2. **Scale before rendering.** Use `scaleBitmap` to fit the image to your terminal dimensions before converting to ANSI.
3. **Handle animated GIFs with the image widget.** Don't manually loop frames; the widget handles animation timing.
4. **Video requires external players.** `detectVideoPlayer()` checks for mpv or mplayer. If neither is found, video won't work.
5. **W3M overlay requires w3mimgdisplay.** This is a separate binary from w3m.
6. **Clean up image caches.** Call `clearImageCache(eid)` or `clearAllImageCaches()` to free memory.
7. **Use subpath imports for tree-shaking.** Import from `@blecsd/media/gif` instead of `@blecsd/media` to only pull in what you need.
