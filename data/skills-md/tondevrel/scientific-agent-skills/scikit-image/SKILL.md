---
name: scikit-image
description: A collection of algorithms for image processing in Python. Built on NumPy, SciPy, and Cython. It focuses on scientific image analysis including segmentation, geometric transformations, color space manipulation, analysis, and filtering.
version: 0.22
license: BSD-3-Clause
---

# scikit-image - Scientific Image Processing

scikit-image treats images as NumPy arrays. It provides a comprehensive suite of algorithms for filtering, feature detection, and object measurement, making it the standard for research-grade image analysis.

## When to Use

- Preprocessing scientific images (noise reduction, contrast enhancement).
- Image segmentation (separating cells, particles, or regions of interest).
- Feature extraction (detecting edges, corners, blobs, or textures).
- Geometric transformations (rescaling, rotating, warping).
- Morphological operations (thinning, skeletonization, hole filling).
- Measuring object properties (area, perimeter, eccentricity).
- Restoring degraded images (deconvolution, inpainting).

## Reference Documentation

**Official docs**: https://scikit-image.org/  
**User Guide**: https://scikit-image.org/docs/stable/user_guide.html  
**Search patterns**: `skimage.filters`, `skimage.segmentation`, `skimage.feature`, `skimage.morphology`

## Core Principles

### Images are NumPy Arrays
A grayscale image is a 2D array (M, N). A color image is a 3D array (M, N, 3). A multichannel 3D volume is (P, M, N, C).

### Coordinate System
The origin (0, 0) is at the top-left corner. Coordinates are always represented as (row, column).

### Data Types and Ranges
scikit-image handles various dtypes with specific ranges:
- `uint8`: 0 to 255
- `uint16`: 0 to 65535
- `float`: -1 to 1 or 0 to 1

## Quick Reference

### Installation

```bash
pip install scikit-image
```

### Standard Imports

```python
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, filters, segmentation, feature, measure, morphology, color, util
```

### Basic Pattern - Load and Filter

```python
from skimage import io, filters, color

# Load image
image = io.imread('data.png')

# Convert to grayscale if needed
gray_image = color.rgb2gray(image)

# Apply a filter (e.g., Gaussian blur)
blurred = filters.gaussian(gray_image, sigma=2.0)

# Display
io.imshow(blurred)
io.show()
```

## Critical Rules

### ✅ DO

- **Use utility functions for conversion** - Use `util.img_as_float`, `util.img_as_ubyte` to handle rescaling automatically when changing dtypes.
- **Grayscale for analysis** - Most feature extraction and segmentation algorithms expect 2D grayscale arrays.
- **Check image shape** - Always verify `image.shape` and `image.dtype` before processing.
- **Vectorize** - Use NumPy operations instead of loops over pixels.
- **Apply filters before segmentation** - Denoising (Gaussian, Median) significantly improves segmentation results.
- **Use label for object counting** - `measure.label` is the standard way to identify connected components.

### ❌ DON'T

- **Manually rescale dtypes** - Avoid `image / 255.0`; use `util.img_as_float`.
- **Ignore the "Coordinate Warning"** - Be careful with (x, y) vs (row, col). scikit-image uses (row, col).
- **Modify the input image** - Most functions return a new array; work with copies if you need to mutate.
- **Apply color-sensitive filters to grayscale** - Some filters behave differently on 3D vs 2D arrays.

## Anti-Patterns (NEVER)

```python
# ❌ BAD: Manual dtype conversion (doesn't handle scaling)
image_float = image.astype(float) # Values stay 0-255 but as floats

# ✅ GOOD: Safe utility conversion
from skimage import util
image_float = util.img_as_float(image) # Values scaled to 0.0-1.0

# ❌ BAD: Looping over pixels
for r in range(rows):
    for c in range(cols):
        if image[r, c] > 128:
            image[r, c] = 255

# ✅ GOOD: Vectorized thresholding
image[image > 0.5] = 1.0

# ❌ BAD: Plotting multiple images without a shared axis
plt.imshow(img1); plt.show()
plt.imshow(img2); plt.show()

# ✅ GOOD: Using subplots for comparison
fig, ax = plt.subplots(1, 2)
ax[0].imshow(img1, cmap='gray')
ax[1].imshow(img2, cmap='gray')
```

## Filtering and Restoration (skimage.filters)

### Denoising and Edge Detection

```python
from skimage import filters

# Edge detection
edges_sobel = filters.sobel(image)
edges_canny = feature.canny(image, sigma=3)

# Denoising
denoised = filters.median(image, morphology.disk(3))

# Thresholding (Automatic)
val = filters.threshold_otsu(image)
binary = image > val
```

## Morphology (skimage.morphology)

### Shaping and Structural Analysis

```python
from skimage import morphology

# Binary morphology
struct_element = morphology.disk(5)
eroded = morphology.erosion(binary, struct_element)
dilated = morphology.dilation(binary, struct_element)
opened = morphology.opening(binary, struct_element) # Erosion then Dilation

# Skeletonization (Reducing objects to 1-pixel width)
skeleton = morphology.skeletonize(binary)

# Removing small objects
clean_binary = morphology.remove_small_objects(binary, min_size=64)
```

## Segmentation (skimage.segmentation)

### Separating Objects

```python
from skimage import segmentation, color

# Watershed Segmentation (Marker-based)
from scipy import ndimage as ndi
distance = ndi.distance_transform_edt(binary)
coords = feature.peak_local_max(distance, footprint=np.ones((3, 3)), labels=binary)
mask = np.zeros(distance.shape, dtype=bool)
mask[tuple(coords.T)] = True
markers, _ = ndi.label(mask)
labels = segmentation.watershed(-distance, markers, mask=binary)

# SLIC (Superpixels)
segments = segmentation.slic(image, n_segments=100, compactness=10)
out = color.label2rgb(segments, image, kind='avg')
```

## Feature Detection (skimage.feature)

### Keypoints and Textures

```python
from skimage import feature

# Local Binary Patterns (Texture analysis)
lbp = feature.local_binary_pattern(image, P=8, R=1)

# Corner detection (Harris)
coords = feature.corner_peaks(feature.corner_harris(image), min_distance=5)

# Blob detection (Difference of Gaussian)
blobs = feature.blob_dog(image, max_sigma=30, threshold=.1)
# blobs: array of [row, col, sigma]
```

## Measurements (skimage.measure)

### Quantifying Results

```python
from skimage import measure

# Label connected components
labels = measure.label(binary)

# Calculate properties
props = measure.regionprops(labels)

for prop in props:
    print(f"Label: {prop.label}")
    print(f"Area: {prop.area}")
    print(f"Centroid: {prop.centroid}")
    print(f"Eccentricity: {prop.eccentricity}")

# Find contours
contours = measure.find_contours(binary, 0.8)
```

## Practical Workflows

### 1. Particle Counting Pipeline

```python
def count_particles(image_path):
    # 1. Load and grayscale
    img = color.rgb2gray(io.imread(image_path))
    
    # 2. Denoise
    img_denoised = filters.gaussian(img, sigma=1)
    
    # 3. Threshold
    thresh = filters.threshold_otsu(img_denoised)
    binary = img_denoised < thresh # Assuming dark particles
    
    # 4. Morphological cleaning
    binary = morphology.remove_small_objects(binary, 50)
    binary = morphology.closing(binary, morphology.disk(3))
    
    # 5. Label and measure
    labels = measure.label(binary)
    return measure.regionprops(labels), labels

# properties, label_img = count_particles('samples.tif')
```

### 2. Micrograph Analysis (Nuclei Segmentation)

```python
def segment_nuclei(dna_image):
    """Identify nuclei in a DAPI/Hoechst stained image."""
    # Local thresholding for uneven illumination
    local_thresh = filters.threshold_local(dna_image, block_size=35)
    binary = dna_image > local_thresh
    
    # Fill holes
    filled = ndi.binary_fill_holes(binary)
    
    # Separate touching nuclei
    distance = ndi.distance_transform_edt(filled)
    local_maxi = feature.peak_local_max(distance, indices=False, footprint=np.ones((15, 15)), labels=filled)
    markers = measure.label(local_maxi)
    labels = segmentation.watershed(-distance, markers, mask=filled)
    
    return labels
```

### 3. Change Detection (Image Subtraction)

```python
def detect_change(img_before, img_after, threshold=0.1):
    # Ensure float
    im1 = util.img_as_float(color.rgb2gray(img_before))
    im2 = util.img_as_float(color.rgb2gray(img_after))
    
    # Difference
    diff = np.abs(im1 - im2)
    
    # Filter noise in difference
    diff_clean = filters.median(diff, morphology.disk(2))
    
    return diff_clean > threshold
```

## Performance Optimization

### Using skimage.util.view_as_windows

```python
from skimage.util import view_as_windows

# Create overlapping patches without copying data (using strides)
# Fast for local neighborhood calculations
patches = view_as_windows(image, (64, 64), step=32)
# Shape: (n_patches_r, n_patches_c, 64, 64)
```

### Parallel Processing

```python
# Many skimage functions are already Cython-optimized.
# For batch processing, use standard joblib or multiprocessing.
from joblib import Parallel, delayed

results = Parallel(n_jobs=-1)(delayed(filters.gaussian)(img) for img in image_list)
```

## Common Pitfalls and Solutions

### Handling Multichannel Images

```python
# ❌ Problem: Filters failing on RGB images
# result = filters.median(rgb_image) # Raises error

# ✅ Solution: Filter per channel or convert
# filters.median(color.rgb2gray(rgb_image))
# OR apply to each channel
# result = np.stack([filters.median(rgb_image[..., i]) for i in range(3)], axis=-1)
```

### Memory issues with label

```python
# ❌ Problem: Large noisy images produce millions of 1-pixel labels
# ✅ Solution: Clear small noise before labeling
binary = morphology.remove_small_objects(binary, min_size=10)
labels = measure.label(binary)
```

### Coordinates: (X, Y) vs (Row, Col) confusion

```python
# ❌ Problem: Points appear swapped on plot
# Matplotlib: plt.plot(x, y)
# scikit-image: image[row, col]

# ✅ Solution: Explicitly swap for visualization
coords = feature.peak_local_max(img) # Returns [row, col]
plt.plot(coords[:, 1], coords[:, 0], 'r.') # Plot as [x, y]
```

scikit-image provides the mathematical rigor needed for scientific discovery. By building on the NumPy ecosystem, it allows for a seamless workflow from raw sensor data to quantifiable insights.
