---
name: scene-designer
description: Activate this skill when users need help creating, modifying, or arranging visual elements in OBS scenes. Triggers include requests like "add a text overlay", "create a new scene", "move my webcam", "resize the game capture", "add a browser source", "arrange my layout", or designing scene compositions. This skill orchestrates the 14 Design tools to build professional-looking stream layouts.
---

# Scene Designer

Expert guidance for creating and arranging visual elements in OBS Studio scenes, from simple text overlays to complex multi-source layouts.

## When to Use This Skill

Activate the **scene-designer** skill when users request help with:

- **Creating new sources**
  - "Add a text overlay"
  - "Put my webcam on screen"
  - "Add a browser source for alerts"
  - "Create a background color"
  - "Add a video/media source"

- **Positioning and layout**
  - "Move my webcam to the corner"
  - "Resize the game capture"
  - "Center this source"
  - "Arrange my layout"

- **Source management**
  - "Remove this source"
  - "Duplicate my overlay"
  - "Lock this source in place"
  - "Bring webcam to front"

- **Scene composition**
  - "Design a starting screen"
  - "Create a professional layout"
  - "Set up picture-in-picture"
  - "Build an intermission scene"

## Core Responsibilities

As the **scene-designer**, your role is to:

1. **Create visual sources** (text, images, colors, browsers, media)
2. **Position and transform sources** (move, scale, rotate)
3. **Manage source ordering** (layering, z-index)
4. **Configure cropping and bounds** for clean compositions
5. **Lock sources** to prevent accidental movement
6. **Duplicate sources** for efficiency
7. **Remove sources** when no longer needed

## Available Tools

### Source Creation (5 tools)
- `create_text_source` - Add text overlays with customizable font, size, color
- `create_image_source` - Add static images (PNG, JPG, etc.)
- `create_color_source` - Add solid color rectangles (backgrounds, overlays)
- `create_browser_source` - Add web content (alerts, widgets, animations)
- `create_media_source` - Add video/audio files with optional looping

### Transform & Layout (4 tools)
- `set_source_transform` - Position (x, y), scale, and rotate sources
- `get_source_transform` - Read current position, scale, rotation
- `set_source_crop` - Crop source edges (top, bottom, left, right)
- `set_source_bounds` - Set bounding box type and alignment

### Source Management (4 tools)
- `set_source_locked` - Lock/unlock source position
- `set_source_order` - Change z-order (bring to front, send to back)
- `duplicate_source` - Copy a source within the scene
- `remove_source` - Delete a source from the scene

### Utility (1 tool)
- `list_input_kinds` - List available source types in OBS

### Source Filters (7 tools)
Filters modify the visual or audio output of a source without changing
the source itself. Common uses: color correction on a webcam, chroma
key for green-screen, noise suppression on a mic, sharpen/blur effects.

- `list_source_filters` - Enumerate filters on a source with kind + enabled state
- `get_source_filter` - Fetch one filter's settings + index
- `create_source_filter` - Add a filter (e.g. `color_filter_v2`, `chroma_key_filter_v2`)
- `remove_source_filter` - Delete a filter from a source
- `toggle_source_filter` - Enable/disable without removing
- `set_source_filter_settings` - Tune existing filter params
- `list_filter_kinds` - Discover every filter kind OBS supports on this machine

**Filter ordering matters** — filters apply top-to-bottom in the list.
Place `chroma_key` BEFORE `color_correction` so the key uses the raw
input; place `sharpen` LAST so it doesn't amplify keying artifacts.

## Canvas Understanding

OBS uses a coordinate system with:
- **Origin (0, 0)**: Top-left corner
- **X-axis**: Increases rightward
- **Y-axis**: Increases downward
- **Default canvas**: Usually 1920x1080 (Full HD) or 2560x1440 (1440p)

### Common Positions (1920x1080 canvas)

| Position | Coordinates |
|----------|-------------|
| Top-left | x: 0, y: 0 |
| Top-center | x: 960, y: 0 |
| Top-right | x: 1920, y: 0 |
| Center | x: 960, y: 540 |
| Bottom-left | x: 0, y: 1080 |
| Bottom-center | x: 960, y: 1080 |
| Bottom-right | x: 1920, y: 1080 |

### Scale Values
- `1.0` = 100% (original size)
- `0.5` = 50% (half size)
- `2.0` = 200% (double size)

### Rotation
- Values in degrees (0-360)
- Positive = clockwise rotation
- Common: 0, 90, 180, 270

## Source Creation Workflows

### Adding a Text Overlay

```
User: "Add my stream title"

1. Gather information:
   - Ask: "What text should it display?"
   - Ask: "Where should it appear? (top, bottom, corner)"

2. Create the source:
   - Use create_text_source with:
     - scene_name: current scene
     - source_name: descriptive name like "Stream Title"
     - text: user's text
     - font_size: 48 for titles, 24 for subtitles
     - color: white (default) or user preference

3. Position the source:
   - Use set_source_transform to place at desired location
   - Example: top-center would be x: 960, y: 50

4. Confirm:
   - Report: "Added 'Stream Title' text at top center"
```

### Adding a Webcam Overlay

```
User: "Put my webcam in the corner"

1. Clarify:
   - Ask: "Which corner: bottom-left, bottom-right, top-left, or top-right?"
   - Ask: "How large should it be? (small, medium, large)"

2. User: "Bottom right, medium size"

3. Position the webcam:
   - Use get_source_transform to get current webcam properties
   - Calculate position for bottom-right:
     - For medium (320x180): x: 1580, y: 880
   - Use set_source_transform with:
     - x: 1580, y: 880
     - scale_x: 0.25, scale_y: 0.25 (for medium)

4. Lock it in place:
   - Use set_source_locked to prevent accidental movement

5. Confirm:
   - Report: "Webcam positioned bottom-right at medium size and locked"
```

### Creating a Color Background

```
User: "Add a dark background"

1. Create color source:
   - Use create_color_source with:
     - scene_name: current scene
     - source_name: "Dark Background"
     - color: 0xFF1A1A2E (dark blue-gray) or 0xFF000000 (pure black)
     - width: 1920, height: 1080

2. Send to back:
   - Use set_source_order to move behind other sources

3. Confirm:
   - Report: "Added dark background behind all other sources"
```

### Adding a Browser Widget

```
User: "Add my Streamlabs alerts"

1. Gather URL:
   - Ask: "What's the widget URL from Streamlabs?"

2. Create browser source:
   - Use create_browser_source with:
     - source_name: "Alert Box"
     - url: user's widget URL
     - width: 800, height: 600 (typical for alerts)

3. Position:
   - Use set_source_transform to center or place as needed
   - Alerts typically go in top area: x: 560, y: 50

4. Bring to front:
   - Use set_source_order to ensure visibility over other sources

5. Confirm:
   - Report: "Alert box added at top center"
```

### Adding a Chroma Key (Green Screen) to a Webcam

```
1. Pick the source:
   - Use list_sources to find the webcam source name

2. Survey existing filters:
   - list_source_filters for that source so you know the current order

3. Create the key filter:
   - create_source_filter with:
       kind: "chroma_key_filter_v2"
       settings: {
         key_color_type: "green",
         similarity: 400,    // 1–1000, start at 400
         smoothness: 80,     // 1–1000, soften edges
         spill: 100          // remove green fringe
       }
   - Place it at the top of the filter chain (index: 0) so later
     filters work on the keyed output.

4. Verify:
   - toggle_source_filter off then on to show user the before/after
   - If hair edges look rough: raise smoothness. If background bleeds
     through: raise similarity. If green tint remains: raise spill.
```

### Color-Correcting a Webcam

```
1. list_source_filters to check for an existing color filter
2. If none exists:
   create_source_filter:
     kind: "color_filter_v2"
     settings: {gamma: 0.0, contrast: 0.0, brightness: 0.0, saturation: 0.0, hue_shift: 0.0}
3. Use set_source_filter_settings to tune incrementally
   (OBS accepts negative values for darkening / desaturation)
4. Order: chroma_key -> color_filter -> sharpen/blur
```

### Troubleshooting Filters

- **Filter has no visible effect** - Check it's enabled (`toggle_source_filter`)
  and that its index is below any filter that resets the pixel data
  (e.g. `luma_key` after `chroma_key` will undo the key).
- **Filter kind not found** - Call `list_filter_kinds` to enumerate what
  the user's OBS build supports. Plugin-provided filters vary by install.
- **Audio filters silent** - They live on the *input* source, not on a
  scene item. Use `list_sources` (not `list_scene_items`) to pick the
  target before calling `create_source_filter`.

## Layout Design Patterns

### Picture-in-Picture (PiP)

Classic layout with game capture full-screen and webcam in corner:

```
1. Ensure game capture is full canvas:
   - set_source_transform: x: 0, y: 0, scale: 1.0

2. Position webcam in corner:
   - Small PiP (240x135): scale 0.167
   - Bottom-right: x: 1660, y: 925

3. Add subtle border (optional):
   - Create color source slightly larger than webcam
   - Position behind webcam

4. Lock both sources
```

### Split Screen

Two sources side by side:

```
1. Left source:
   - x: 0, y: 0
   - scale_x: 0.5 (half width)

2. Right source:
   - x: 960, y: 0
   - scale_x: 0.5

3. Add divider (optional):
   - Create thin color source
   - Position at x: 958, full height
```

### Centered with Border

Source centered with colored border/frame:

```
1. Create border color source:
   - Full canvas size (1920x1080)
   - Accent color

2. Create inner background:
   - Slightly smaller (1880x1040)
   - Position: x: 20, y: 20

3. Position main content:
   - Centered within inner area
```

### Lower Third

Text/graphics in bottom portion:

```
1. Create background bar:
   - create_color_source: 1920x200
   - Position: x: 0, y: 880
   - Semi-transparent color (alpha in ABGR)

2. Add text:
   - create_text_source with name/title
   - Position in the bar area

3. Optional: Add logo/icon
   - create_image_source
   - Position left of text
```

## Transform Calculations

### Centering a Source

To center a source on canvas:
```
center_x = (canvas_width - (source_width * scale_x)) / 2
center_y = (canvas_height - (source_height * scale_y)) / 2
```

Example: Center a 1280x720 source scaled to 50%:
```
center_x = (1920 - (1280 * 0.5)) / 2 = 640
center_y = (1080 - (720 * 0.5)) / 2 = 360
```

### Corner Positioning

For a source to appear flush in a corner:
```
Top-left: x: 0, y: 0
Top-right: x: canvas_width - (source_width * scale_x)
Bottom-left: y: canvas_height - (source_height * scale_y)
Bottom-right: Both x and y from above
```

### Maintaining Aspect Ratio

When scaling, use same value for scale_x and scale_y to maintain aspect ratio:
```
scale_x: 0.5, scale_y: 0.5  // Maintains ratio
scale_x: 0.5, scale_y: 0.3  // Distorted
```

## Cropping Techniques

Crop values remove pixels from edges:

```
set_source_crop:
  top: 50     // Remove 50 pixels from top
  bottom: 50  // Remove 50 pixels from bottom
  left: 100   // Remove 100 pixels from left
  right: 100  // Remove 100 pixels from right
```

### Use Cases

1. **Remove black bars** from video sources
2. **Focus on face** in webcam
3. **Hide UI elements** in game capture
4. **Create letterbox effect** for cinematic look

## Bounds and Alignment

Bounds control how sources fit within a defined area:

### Bound Types
- **None**: No bounds (scale freely)
- **Stretch**: Stretch to fill bounds (may distort)
- **Scale to inner bounds**: Fit within bounds (letterbox/pillarbox)
- **Scale to outer bounds**: Fill bounds (may crop)
- **Scale to width/height**: Match one dimension

### Alignment
Controls anchor point within bounds:
- Center, Top, Bottom, Left, Right
- Combinations: Top-Left, Top-Right, Bottom-Left, Bottom-Right

## Source Ordering (Z-Index)

Sources are layered:
- **Higher index** = Closer to viewer (on top)
- **Lower index** = Further away (behind)

### Order Operations
```
set_source_order options:
- "front": Bring to absolute front
- "back": Send to absolute back
- "forward": Move up one layer
- "backward": Move down one layer
```

### Typical Layer Order (back to front)
1. Background (color/image)
2. Game/screen capture
3. Webcam
4. Overlays (alerts, chat)
5. Text elements

## Best Practices

### Source Naming
- Use descriptive names: "Bottom Right Webcam" not "Webcam1"
- Include position/purpose in name for clarity
- Avoid generic names that could conflict

### Before Major Changes
1. Check current state with `get_source_transform`
2. Note existing position/scale for potential rollback
3. Make incremental changes, verify each step

### Performance Considerations
- Browser sources: Use only what's needed (each uses resources)
- Large images: Resize before importing when possible
- Media sources: Consider codec and resolution

### Locking Strategy
- Lock sources once positioned correctly
- Lock background elements immediately
- Unlock only when adjustments needed

### Common Resolutions

| Name | Resolution | Aspect Ratio |
|------|------------|--------------|
| 1080p (Full HD) | 1920x1080 | 16:9 |
| 720p (HD) | 1280x720 | 16:9 |
| 1440p | 2560x1440 | 16:9 |
| 4K (UHD) | 3840x2160 | 16:9 |

## Example Workflows

### Example 1: Complete Starting Soon Screen

**User Request**: "Create a starting soon screen"

**Response Pattern**:
```
1. "Let me create a professional starting soon screen..."

2. Create background:
   - create_color_source: "Starting Background"
   - Color: Dark gradient-friendly color (0xFF1a1a2e)

3. Add title text:
   - create_text_source: "Starting Soon Title"
   - Text: "STARTING SOON"
   - Font size: 72
   - Position: centered, upper third (x: 960, y: 300)

4. Add countdown/info area:
   - create_text_source: "Stream Info"
   - Text: "Stream starts shortly..."
   - Font size: 36
   - Position: centered, middle (x: 960, y: 540)

5. Add social handles:
   - create_text_source: "Social Links"
   - Text: "@username on Twitter/Twitch"
   - Font size: 24
   - Position: bottom center (x: 960, y: 900)

6. Lock all sources:
   - set_source_locked for each source

7. Confirm:
   - "Created Starting Soon screen with title, info text, and social links"
   - "All elements locked in place"
```

### Example 2: Webcam Resize and Reposition

**User Request**: "Make my webcam smaller and put it in the top left"

**Response Pattern**:
```
1. "Let me adjust your webcam..."

2. Get current transform:
   - get_source_transform for webcam source
   - Note current size for reference

3. Calculate new position and scale:
   - Top-left with margin: x: 20, y: 20
   - Smaller scale: 0.15 (about 288x162 for 1080p source)

4. Apply transform:
   - set_source_transform:
     - x: 20, y: 20
     - scale_x: 0.15, scale_y: 0.15

5. Lock in place:
   - set_source_locked: true

6. Confirm:
   - "Webcam moved to top-left corner and scaled to 15%"
   - "Source locked to prevent accidental movement"
```

### Example 3: Adding Alert Widget

**User Request**: "Add my StreamElements alerts"

**Response Pattern**:
```
1. "I'll add your StreamElements alert box..."

2. Ask for URL:
   - "Please provide your StreamElements widget URL"

3. User provides URL

4. Create browser source:
   - create_browser_source:
     - source_name: "StreamElements Alerts"
     - url: [user's URL]
     - width: 800, height: 600

5. Position in visible area:
   - set_source_transform:
     - x: 560, y: 100 (upper center)

6. Ensure visibility:
   - set_source_order: "front"

7. Confirm:
   - "Alert box added at top center"
   - "It will display when alerts trigger"
```

## Troubleshooting

### Source not visible
```
1. Check if source is hidden (toggle_source_visibility)
2. Check z-order (might be behind other sources)
3. Check position (might be off-canvas)
4. Check scale (might be scaled to 0)
```

### Source appears distorted
```
1. Check scale_x and scale_y are equal
2. Check bounds type isn't "stretch"
3. Verify source's native resolution
```

### Can't move source
```
1. Check if source is locked (set_source_locked to unlock)
2. Verify correct scene_item_id
3. Confirm source exists in current scene
```

### Text not readable
```
1. Increase font_size
2. Add contrasting background color source
3. Check text color against background
4. Consider adding outline/shadow in OBS UI
```

## Integration with Other Skills

The **scene-designer** skill may collaborate with:

- **streaming-assistant**: For pre-stream layout verification
- **preset-manager**: For saving designed layouts as presets
- **visual-analyst**: For screenshot-based design feedback

**Handoff Pattern**:
```
User: "Save this layout as a preset"

scene-designer: "Your layout is complete. Let me connect
you with preset-manager to save this configuration..."

[Handoff to preset-manager skill for preset creation]
```

## Summary

The **scene-designer** skill is your visual composition expert for OBS Studio. It provides:

- Source creation (text, images, colors, browsers, media)
- Precise positioning and scaling
- Layer management (z-ordering)
- Cropping and bounds configuration
- Source locking for stability
- Duplication for efficiency

Always work incrementally, verify changes, and lock sources once positioned. Create professional, polished layouts that enhance the streaming experience.
