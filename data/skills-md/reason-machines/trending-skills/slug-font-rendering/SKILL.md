---
name: slug-font-rendering
description: Reference HLSL shader implementations for the Slug font rendering algorithm, enabling high-quality GPU-accelerated vector font and glyph rendering.
triggers:
  - render fonts on GPU with Slug
  - implement Slug font rendering algorithm
  - HLSL shader for text rendering
  - vector font rendering shader
  - Slug algorithm glyph rendering
  - GPU accelerated font rendering
  - implement slug font shader
  - bezier curve font rendering GPU
---

# Slug Font Rendering Algorithm

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Slug is a reference implementation of the Slug font rendering algorithm — a GPU-accelerated technique for rendering vector fonts and glyphs at arbitrary scales with high quality anti-aliasing. It works by encoding glyph outlines as lists of quadratic Bézier curves and line segments, then resolving coverage directly in fragment shaders without pre-rasterized textures.

**Paper:** [JCGT 2017 — Slug Algorithm](https://jcgt.org/published/0006/02/02/)  
**Blog (updates):** [A Decade of Slug](https://terathon.com/blog/decade-slug.html)  
**License:** MIT — Patent dedicated to public domain. Credit required if distributed.

---

## What Slug Does

- Renders TrueType/OpenType glyphs entirely on the GPU
- No texture atlases or pre-rasterization needed
- Scales to any resolution without quality loss
- Anti-aliased coverage computed per-fragment using Bézier math
- Works with any rendering API that supports programmable shaders (D3D11/12, Vulkan, Metal via translation)

---

## Repository Structure

```
Slug/
├── slug.hlsl          # Core fragment shader — coverage computation
├── band.hlsl          # Band-based optimization for glyph rendering
├── curve.hlsl         # Quadratic Bézier and line segment evaluation
├── README.md
```

---

## Installation / Integration

Slug is a **reference implementation** — you integrate the HLSL shaders into your own rendering pipeline.

### Step 1: Clone the Repository

```bash
git clone https://github.com/EricLengyel/Slug.git
```

### Step 2: Include the Shaders

Copy the `.hlsl` files into your shader directory and include them in your pipeline:

```hlsl
#include "slug.hlsl"
#include "curve.hlsl"
```

### Step 3: Prepare Glyph Data on the CPU

You must preprocess font outlines (TrueType/OTF) into Slug's curve buffer format:
- Decompose glyph contours into quadratic Bézier segments and line segments
- Upload curve data to a GPU buffer (structured buffer or texture buffer)
- Precompute per-glyph "band" metadata for the band optimization

---

## Core Concepts

### Glyph Coordinate System

- Glyph outlines live in **font units** (typically 0–2048 or 0–1000 per em)
- The fragment shader receives a position in glyph space via interpolated vertex attributes
- Coverage is computed by counting signed curve crossings in the Y direction (winding number)

### Curve Data Format

Each curve entry in the GPU buffer stores:

```hlsl
// Line segment: p0, p1
// Quadratic Bézier: p0, p1 (control), p2

struct CurveRecord
{
    float2 p0;   // Start point
    float2 p1;   // Control point (or end point for lines)
    float2 p2;   // End point (unused for lines — flagged via type)
    // Type/flags encoded separately or in padding
};
```

### Band Optimization

The glyph bounding box is divided into horizontal **bands**. Each band stores only the curves that intersect it, reducing per-fragment work from O(all curves) to O(local curves).

---

## Key Shader Code & Patterns

### Fragment Shader Entry Point (Conceptual Integration)

```hlsl
// Inputs from vertex shader
struct PS_Input
{
    float4 position  : SV_Position;
    float2 glyphCoord : TEXCOORD0;  // Position in glyph/font units
    // Band index or precomputed band data
    nointerpolation uint bandOffset : TEXCOORD1;
    nointerpolation uint curveCount : TEXCOORD2;
};

// Glyph curve data buffer
StructuredBuffer<float4> CurveBuffer : register(t0);

float4 PS_Slug(PS_Input input) : SV_Target
{
    float coverage = ComputeGlyphCoverage(
        input.glyphCoord,
        CurveBuffer,
        input.bandOffset,
        input.curveCount
    );

    // Premultiplied alpha output
    float4 color = float4(textColor.rgb * coverage, coverage);
    return color;
}
```

### Quadratic Bézier Coverage Computation

The heart of the algorithm — computing signed coverage from a quadratic Bézier:

```hlsl
// Evaluate whether a quadratic bezier contributes to coverage at point p
// p0: start, p1: control, p2: end
// Returns signed coverage contribution
float QuadraticBezierCoverage(float2 p, float2 p0, float2 p1, float2 p2)
{
    // Transform to canonical space
    float2 a = p1 - p0;
    float2 b = p0 - 2.0 * p1 + p2;

    // Find t values where bezier Y == p.y
    float2 delta = p - p0;
    
    float A = b.y;
    float B = a.y;
    float C = p0.y - p.y;

    float coverage = 0.0;

    if (abs(A) > 1e-6)
    {
        float disc = B * B - A * C;
        if (disc >= 0.0)
        {
            float sqrtDisc = sqrt(disc);
            float t0 = (-B - sqrtDisc) / A;
            float t1 = (-B + sqrtDisc) / A;

            // For each valid t in [0,1], compute x and check winding
            if (t0 >= 0.0 && t0 <= 1.0)
            {
                float x = (A * t0 + 2.0 * B) * t0 + p0.x + delta.x;
                // ... accumulate signed coverage
            }
            if (t1 >= 0.0 && t1 <= 1.0)
            {
                float x = (A * t1 + 2.0 * B) * t1 + p0.x + delta.x;
                // ... accumulate signed coverage
            }
        }
    }
    else
    {
        // Degenerate to linear case
        float t = -C / (2.0 * B);
        if (t >= 0.0 && t <= 1.0)
        {
            float x = 2.0 * a.x * t + p0.x;
            // ... accumulate signed coverage
        }
    }

    return coverage;
}
```

### Line Segment Coverage

```hlsl
// Signed coverage contribution of a line segment from p0 to p1
float LineCoverage(float2 p, float2 p0, float2 p1)
{
    // Check Y range
    float minY = min(p0.y, p1.y);
    float maxY = max(p0.y, p1.y);

    if (p.y < minY || p.y >= maxY)
        return 0.0;

    // Interpolate X at p.y
    float t = (p.y - p0.y) / (p1.y - p0.y);
    float x = lerp(p0.x, p1.x, t);

    // Winding: +1 if p is to the left (inside), -1 if right
    float dir = (p1.y > p0.y) ? 1.0 : -1.0;
    return (p.x <= x) ? dir : 0.0;
}
```

### Anti-Aliasing with Partial Coverage

For smooth edges, use the distance to the nearest curve for sub-pixel anti-aliasing:

```hlsl
// Compute AA coverage using partial pixel coverage
// windingNumber: integer winding from coverage pass
// distToEdge: signed distance to nearest curve (in pixels)
float AntiAliasedCoverage(int windingNumber, float distToEdge)
{
    // Non-zero winding rule
    bool inside = (windingNumber != 0);
    
    // Smooth transition at edges using clamp
    float edgeCoverage = clamp(distToEdge + 0.5, 0.0, 1.0);
    
    return inside ? edgeCoverage : (1.0 - edgeCoverage);
}
```

---

## Vertex Shader Pattern

```hlsl
struct VS_Input
{
    float2 position   : POSITION;     // Glyph quad corner in screen/world space
    float2 glyphCoord : TEXCOORD0;    // Corresponding glyph-space coordinate
    uint   bandOffset : TEXCOORD1;    // Offset into curve buffer for this glyph
    uint   curveCount : TEXCOORD2;    // Number of curves in band
};

struct VS_Output
{
    float4 position   : SV_Position;
    float2 glyphCoord : TEXCOORD0;
    nointerpolation uint bandOffset : TEXCOORD1;
    nointerpolation uint curveCount : TEXCOORD2;
};

VS_Output VS_Slug(VS_Input input)
{
    VS_Output output;
    output.position   = mul(float4(input.position, 0.0, 1.0), WorldViewProjection);
    output.glyphCoord = input.glyphCoord;
    output.bandOffset = input.bandOffset;
    output.curveCount = input.curveCount;
    return output;
}
```

---

## CPU-Side Data Preparation (Pseudocode)

```cpp
// 1. Load font file and extract glyph outlines
FontOutline outline = LoadGlyphOutline(font, glyphIndex);

// 2. Decompose to quadratic Beziers (TrueType is already quadratic)
//    OTF cubic curves must be approximated/split into quadratics
std::vector<SlugCurve> curves = DecomposeToQuadratics(outline);

// 3. Compute bands
float bandHeight = outline.bounds.height / NUM_BANDS;
std::vector<BandData> bands = ComputeBands(curves, NUM_BANDS, bandHeight);

// 4. Upload to GPU
UploadStructuredBuffer(curveBuffer, curves.data(), curves.size());
UploadStructuredBuffer(bandBuffer, bands.data(), bands.size());

// 5. Per glyph instance: store bandOffset and curveCount per band
//    in vertex data so the fragment shader can index directly
```

---

## Render State Requirements

```hlsl
// Blend state: premultiplied alpha
BlendState SlugBlend
{
    BlendEnable    = TRUE;
    SrcBlend       = ONE;           // Premultiplied
    DestBlend      = INV_SRC_ALPHA;
    BlendOp        = ADD;
    SrcBlendAlpha  = ONE;
    DestBlendAlpha = INV_SRC_ALPHA;
    BlendOpAlpha   = ADD;
};

// Depth: typically write disabled for text overlay
DepthStencilState SlugDepth
{
    DepthEnable    = FALSE;
    DepthWriteMask = ZERO;
};

// Rasterizer: no backface culling (glyph quads are 2D)
RasterizerState SlugRaster
{
    CullMode = NONE;
    FillMode = SOLID;
};
```

---

## Common Patterns

### Rendering a String

```cpp
// For each glyph in string:
for (auto& glyph : string.glyphs)
{
    // Emit a quad (2 triangles) covering the glyph bounding box
    // Each vertex carries:
    //   - screen position
    //   - glyph-space coordinate (the same corner in font units)
    //   - bandOffset + curveCount for the fragment shader

    float2 min = glyph.screenMin;
    float2 max = glyph.screenMax;
    float2 glyphMin = glyph.fontMin;
    float2 glyphMax = glyph.fontMax;

    EmitQuad(min, max, glyphMin, glyphMax,
             glyph.bandOffset, glyph.curveCount);
}
```

### Scaling Text

Scaling is handled entirely on the CPU side by transforming the screen-space quad. The glyph-space coordinates stay constant — the fragment shader always works in font units.

```cpp
float scale = desiredPixelSize / font.unitsPerEm;
float2 screenMin = origin + glyph.fontMin * scale;
float2 screenMax = origin + glyph.fontMax * scale;
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Glyph appears hollow/inverted | Winding order reversed | Check contour orientation; TrueType uses clockwise for outer contours |
| Jagged edges | Anti-aliasing not applied | Ensure distance-to-edge is computed and used in final coverage |
| Performance poor | Band optimization not active | Verify per-fragment curve count is small (< ~20); increase band count |
| Cubic curves not rendering | OTF cubic Béziers unsupported natively | Split cubics into quadratic approximations on CPU |
| Artifacts at glyph overlap | Curves not clipped to band | Clip curve Y range to band extents before upload |
| Black box instead of glyph | Blend state wrong | Use premultiplied alpha blend (ONE, INV_SRC_ALPHA) |
| Missing glyphs | Band offset incorrect | Validate bandOffset indexing aligns with buffer layout |

---

## Credits & Attribution

Per the license: if you distribute software using this code, **you must give credit** to Eric Lengyel and the Slug algorithm.

Suggested attribution:
> Font rendering uses the Slug Algorithm by Eric Lengyel (https://jcgt.org/published/0006/02/02/)

---

## References

- [Slug Algorithm Paper (JCGT 2017)](https://jcgt.org/published/0006/02/02/)
- [A Decade of Slug — Blog Post](https://terathon.com/blog/decade-slug.html)
- [GitHub Repository](https://github.com/EricLengyel/Slug)
