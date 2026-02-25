---
name: gsplat-optimizer
description: Optimize 3D Gaussian Splat scenes for real-time rendering on iOS, macOS, and visionOS. Use when working with .ply or .splat files, targeting mobile/Apple GPU performance, or needing LOD, pruning, or compression strategies for 3DGS scenes.
---

# Gaussian Splat Optimizer

Optimize 3D Gaussian Splatting scenes for real-time rendering on Apple platforms (iOS, macOS, visionOS) using Metal.

## When to Use

- Optimizing `.ply` or `.splat` files for mobile/Apple GPU targets
- Reducing gaussian count for performance (pruning strategies)
- Implementing Level-of-Detail (LOD) for large scenes
- Compressing splat data for bandwidth/storage constraints
- Profiling and optimizing Metal rendering performance
- Targeting specific FPS goals on Apple hardware

## Quick Start

**Input**: Provide a `.ply`/`.splat` file path, target device class, and FPS target.

```bash
# Analyze a splat file
python ~/.claude/skills/gsplat-optimizer/scripts/analyze_splat.py scene.ply --device iphone --fps 60
```

**Output**: The skill provides:
1. Point/gaussian pruning plan (opacity, size, error thresholds)
2. LOD scheme suggestion (distance bins, gaussian subsets)
3. Compression recommendation (if bandwidth/storage bound)
4. Metal profiling checklist with shader/compute tips

## Optimization Workflow

### Step 1: Analyze the Scene

First, understand your scene characteristics:
- **Gaussian count**: Total number of splats
- **Opacity distribution**: Histogram of opacity values
- **Size distribution**: Gaussian scale statistics
- **Memory footprint**: Estimated GPU memory usage

### Step 2: Determine Target Device

| Device Class | GPU Budget | Max Gaussians (60fps) | Storage Mode |
|-------------|-----------|----------------------|--------------|
| iPhone (A15+) | 4-6GB unified | ~2-4M | Shared |
| iPad Pro (M1+) | 8-16GB unified | ~6-8M | Shared |
| Mac (M1-M3) | 8-24GB unified | ~8-12M | Shared/Managed |
| Vision Pro | 16GB unified | ~4-6M (stereo) | Shared |
| Mac (discrete GPU) | 8-24GB VRAM | ~10-15M | Private |

### Step 3: Apply Pruning

If gaussian count exceeds device budget:

1. **Opacity threshold**: Remove gaussians with opacity < 0.01-0.05
2. **Size culling**: Remove sub-pixel gaussians (< 1px at target resolution)
3. **Importance pruning**: Use LODGE algorithm for error-proxy selection
4. **Foveated rendering**: For Vision Pro, reduce density in peripheral view

See [references/pruning-strategies.md](references/pruning-strategies.md) for details.

### Step 4: Implement LOD (Large Scenes)

For scenes exceeding single-frame budget:

1. **Distance bins**: Near (0-10m), Mid (10-50m), Far (50m+)
2. **Hierarchical structure**: Octree or LoD tree for spatial queries
3. **Chunk streaming**: Load/unload based on camera position
4. **Smooth transitions**: Opacity blending at chunk boundaries

See [references/lod-schemes.md](references/lod-schemes.md) for details.

### Step 5: Apply Compression (If Needed)

For bandwidth/storage constraints:

| Method | Compression | Use Case |
|--------|-------------|----------|
| SOGS | 20x | Web delivery, moderate quality |
| SOG | 24x | Web delivery, better quality |
| CodecGS | 30x+ | Maximum compression |
| C3DGS | 31x | Fast rendering priority |

See [references/compression.md](references/compression.md) for details.

### Step 6: Profile and Optimize Metal

1. **Choose storage mode**: Private for static data, Shared for dynamic
2. **Optimize shaders**: Function constants, thread occupancy
3. **Profile with Xcode**: GPU Frame Capture, Metal System Trace
4. **Iterate**: Measure, optimize, repeat

See [references/metal-profiling.md](references/metal-profiling.md) for details.

## Key Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Frame time | 16.6ms (60fps) | Metal System Trace |
| GPU memory | < device budget | Xcode Memory Graph |
| Bandwidth | < 50GB/s | GPU Counters |
| Shader time | < 10ms | GPU Frame Capture |

## Reference Implementation

**MetalSplatter** is the primary reference for Swift/Metal gaussian splatting:
- Repository: https://github.com/scier/MetalSplatter
- Supports iOS, macOS, visionOS
- ~8M splat capacity with v1.1 optimizations
- Stereo rendering for Vision Pro

### Getting Started with MetalSplatter

```bash
git clone https://github.com/scier/MetalSplatter.git
cd MetalSplatter
open SampleApp/MetalSplatter_SampleApp.xcodeproj
# Set to Release scheme for best performance
```

## Resources

### Reference Documentation
- [Pruning Strategies](references/pruning-strategies.md) - Gaussian reduction techniques
- [LOD Schemes](references/lod-schemes.md) - Level-of-detail approaches
- [Compression](references/compression.md) - Bandwidth/storage optimization
- [Metal Profiling](references/metal-profiling.md) - Apple GPU optimization

### Research Papers
- [LODGE](https://arxiv.org/abs/2505.23158) - LOD for large-scale scenes
- [FLoD](https://arxiv.org/abs/2408.12894) - Flexible LOD for variable hardware
- [Voyager](https://arxiv.org/html/2506.02774v2) - City-scale mobile rendering
- [3DGS Compression Survey](https://w-m.github.io/3dgs-compression-survey/)

### Apple Developer Resources
- [Metal Best Practices Guide](https://developer.apple.com/library/archive/documentation/3DDrawing/Conceptual/MTLBestPracticesGuide/)
- [Metal Shader Performance (Tech Talk)](https://developer.apple.com/videos/play/tech-talks/111373/)
- [Optimize GPU Renderers (WWDC23)](https://developer.apple.com/videos/play/wwdc2023/10127/)
