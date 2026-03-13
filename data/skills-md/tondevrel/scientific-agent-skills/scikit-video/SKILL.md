---
name: scikit-video
description: Video processing library for scientists. Provides easy access to video files using FFmpeg, motion estimation algorithms, and video quality metrics. Built on NumPy and designed for high-performance research in computer vision and image sequence analysis. Use when working with video files, motion estimation, video quality assessment (VQA), FFmpeg, temporal image data, video codecs, YUV data, or scientific video recordings.
version: 1.1
license: BSD-3-Clause
---

# scikit-video - Scientific Video Processing

scikit-video simplifies the complex world of video codecs and containers by providing a consistent NumPy-based interface. It allows for the calculation of motion vectors, video quality assessment (VQA), and seamless integration with the rest of the scientific Python stack.

## When to Use

- Reading and writing video files in various formats (MP4, AVI, MKV) via FFmpeg.
- Extracting specific frames or segments from long videos without loading them entirely into memory.
- Calculating motion estimation (Block Matching, Optical Flow).
- Measuring video quality (PSNR, SSIM, VIF, NIQE).
- Generating video datasets for machine learning.
- Visualizing temporal changes in pixel data (e.g., scientific recordings).
- Handling raw YUV data streams.

## Reference Documentation

**Official docs**: http://www.scikit-video.org/  
**GitHub**: https://github.com/scikit-video/scikit-video  
**Search patterns**: `skvideo.io.vread`, `skvideo.io.FFmpegReader`, `skvideo.motion`, `skvideo.measure`

## Core Principles

### Video as 4D Arrays
A video is represented as a NumPy array with shape (T, H, W, C):
- **T**: Time (number of frames)
- **H**: Height
- **W**: Width
- **C**: Channels (usually 3 for RGB)

### FFmpeg Backend
Scikit-video does not contain its own codecs; it is a bridge to FFmpeg. You must have FFmpeg installed on your system for `skvideo.io` to function.

### Generators for Large Data
For long videos, scikit-video provides generator-based readers (`vreader`) to process frames one by one, preventing RAM exhaustion.

## Quick Reference

### Installation

```bash
pip install scikit-video
# Note: Ensure ffmpeg is in your system PATH
```

### Standard Imports

```python
import skvideo.io
import skvideo.motion
import skvideo.measure
import numpy as np
```

### Basic Pattern - Read and Inspect

```python
import skvideo.io

# 1. Read the whole video into a NumPy array
# Shape: (frames, height, width, 3)
video_data = skvideo.io.vread("experiment.mp4")

# 2. Get basic info
n_frames, height, width, channels = video_data.shape
print(f"FPS: {n_frames / 10}, Resolution: {width}x{height}")

# 3. Access a specific frame
frame_10 = video_data[10]
```

## Critical Rules

### ✅ DO

- **Use vreader for large files** - Always use generator-based reading for high-resolution or long videos.
- **Set num_frames** - If you know the number of frames you need, specify it to avoid unnecessary scanning.
- **Check FFmpeg path** - Use `skvideo.setFFmpegPath()` if FFmpeg is installed in a non-standard location.
- **Normalize for Metrics** - Ensure pixel values are in the range expected by `skvideo.measure` (usually [0, 255] for uint8).
- **Use vwrite for simple output** - It handles the complex FFmpeg command-line arguments for you.
- **Consider YUV** - When working with raw transmission data, use the specific YUV reading capabilities.

### ❌ DON'T

- **Load 4K video with vread** - A 1-minute 4K video will exceed most RAM capacities.
- **Ignore the inputdict and outputdict** - These allow you to pass specific flags to FFmpeg (like bitrate, pixel format, or codec).
- **Assume RGB order** - Always verify the channel order after reading, especially if using external codecs.
- **Process video without Denoising** - Video noise can ruin motion estimation; apply spatial or temporal filters first.

## Anti-Patterns (NEVER)

```python
import skvideo.io

# ❌ BAD: Loading a massive file at once
# video = skvideo.io.vread("huge_4k_recording.mp4") # CRASH!

# ✅ GOOD: Processing frame by frame
reader = skvideo.io.vreader("huge_4k_recording.mp4")
for frame in reader:
    # Process frame
    pass

# ❌ BAD: Manual frame writing in a loop with manual codec setup
# (Fragile and complex)

# ✅ GOOD: Use FFmpegWriter
writer = skvideo.io.FFmpegWriter("output.mp4")
for frame in processed_frames:
    writer.writeFrame(frame)
writer.close()

# ❌ BAD: Relying on system default FFmpeg without checking
# ✅ GOOD: Verify backend
# print(skvideo._HAS_FFMPEG)
```

## Reading and Writing (skvideo.io)

### Advanced Video I/O

```python
import skvideo.io

# 1. Reading with specific FFmpeg options
input_parameters = {
    "-ss": "00:00:10", # Start at 10 seconds
    "-t": "5"          # Duration 5 seconds
}
video = skvideo.io.vread("video.mp4", inputdict=input_parameters)

# 2. Writing with specific bitrate and codec
output_parameters = {
    "-vcodec": "libx264",
    "-b:v": "5000k", # 5 Mbps bitrate
    "-pix_fmt": "yuv420p"
}
skvideo.io.vwrite("output.mp4", video, outputdict=output_parameters)
```

## Motion Estimation (skvideo.motion)

### Calculating Movement

```python
from skvideo.motion import blockMotion
from skvideo.io import vread

# Load two consecutive frames
video = vread("video.mp4")
frame1 = video[0]
frame2 = video[1]

# Block matching algorithm
# Returns motion vectors for each block
motion_vectors = blockMotion(frame1, frame2, method='DS', mbSize=16)

# motion_vectors shape: (H/mbSize, W/mbSize, 2)
# The last dimension contains (dy, dx) offsets
```

## Video Quality Assessment (skvideo.measure)

### Measuring Degradation

```python
from skvideo.measure import psnr, ssim, mse

# Compare original and compressed video
original = vread("original.mp4")
distorted = vread("compressed.mp4")

# Calculate metrics frame by frame
psnr_scores = psnr(original, distorted)
ssim_scores = ssim(original, distorted)

print(f"Average PSNR: {np.mean(psnr_scores)}")
```

## Datasets and Utilities

### Using Internal Datasets

```python
import skvideo.datasets

# Load a built-in sample video (useful for testing)
path = skvideo.datasets.bigbuckbunny()
reader = skvideo.io.vreader(path)
```

## Practical Workflows

### 1. Simple Background Subtraction Pipeline

```python
def extract_background(video_path):
    """Calculates the static background of a video using the median."""
    reader = skvideo.io.vreader(video_path)
    frames = []
    # Sample every 10th frame to save memory
    for i, frame in enumerate(reader):
        if i % 10 == 0:
            frames.append(frame)
        if len(frames) > 50: break
            
    # Background is the median of frames
    background = np.median(np.array(frames), axis=0).astype(np.uint8)
    return background

# Usage
# bg = extract_background("security_cam.mp4")
```

### 2. Video Stabilization (Frame Alignment)

```python
def stabilize_frames(video_array):
    """Very basic stabilization using motion vectors."""
    stabilized = [video_array[0]]
    for i in range(1, len(video_array)):
        motion = skvideo.motion.blockMotion(video_array[i-1], video_array[i])
        avg_motion = np.mean(motion, axis=(0, 1)) # Global drift
        # Translate frame back (Simplified logic)
        # Use scipy.ndimage.shift for actual translation
        ...
```

### 3. Automated Video Quality Report

```python
def generate_vqa_report(ref_path, test_path):
    ref = skvideo.io.vread(ref_path)
    test = skvideo.io.vread(test_path)
    
    report = {
        "MSE": np.mean(skvideo.measure.mse(ref, test)),
        "PSNR": np.mean(skvideo.measure.psnr(ref, test)),
        "SSIM": np.mean(skvideo.measure.ssim(ref, test))
    }
    return report
```

## Performance Optimization

### Using vreader with Multi-threading
If you are doing heavy processing on each frame, use a queue-based multi-threading approach to keep the FFmpeg pipe full.

### Efficient Slicing
Instead of `vread` and then slicing, use FFmpeg's seek and duration flags via `inputdict` to only read the data you need from the disk.

## Common Pitfalls and Solutions

### FFmpeg Not Found
Scikit-video relies on the ffmpeg executable.

```python
# ✅ Solution: Manually set the path if it's not in environment
import skvideo
skvideo.setFFmpegPath("C:/ffmpeg/bin")
```

### Color Space Mismatches
Some videos are stored in YUV422 or YUV444. Scikit-video converts these to RGB by default.

```python
# ❌ Problem: Colors look washed out or incorrect
# ✅ Solution: Specify the pixel format in inputdict
reader = skvideo.io.vreader("video.mp4", inputdict={"-pix_fmt": "yuv420p"})
```

### Out of Memory (OOM) Errors
Even with `vreader`, if you store all frames in a list, you will run out of memory.

```python
# ❌ Problem: frames.append(frame) in a loop
# ✅ Solution: Process and save to disk, or clear the list periodically.
```

scikit-video brings the power of FFmpeg into the NumPy world. By abstracting the complexities of video containers and providing scientific analysis tools like motion estimation and quality metrics, it is an essential tool for any researcher working with temporal image data.
