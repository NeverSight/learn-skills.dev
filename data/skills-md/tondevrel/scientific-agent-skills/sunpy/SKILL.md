---
name: sunpy
description: The community-developed free and open-source software package for solar physics. Provides tools for data search and download, coordinate transformations specific to solar physics, and powerful image processing through the Map object. Use when working with solar data, solar images (EUV, magnetograms, white light), solar coordinates (Helioprojective, Heliographic), Fido data search, solar time series, differential rotation, limb fitting, or multi-instrument solar analysis (AIA, HMI, GOES).
version: 5.1
license: BSD-2-Clause
---

# SunPy - Solar Physics Analysis

SunPy is built on top of the Astropy ecosystem but extends it with functionalities required by solar physicists. Its core strengths are the Map object for 2D imaging data, TimeSeries for light curves, and the Fido interface for unified data searching across multiple repositories.

## When to Use

- Searching and downloading solar data from VSO, JSOC, and other archives.
- Visualizing solar images (EUV, magnetograms, white light).
- Transforming coordinates between different solar frames (e.g., Stonyhurst to Helioprojective).
- Analyzing solar time series data (GOES X-ray flux, sunspot counts).
- Correcting for solar differential rotation.
- Overlapping data from different instruments (e.g., AIA and HMI).
- Performing limb-fitting and feature tracking on the solar disk.

## Reference Documentation

**Official docs**: https://docs.sunpy.org/  
**SunPy Gallery**: https://docs.sunpy.org/en/stable/generated/gallery/index.html  
**Search patterns**: `sunpy.map.Map`, `sunpy.net.Fido`, `sunpy.coordinates.frames`, `sunpy.timeseries`

## Core Principles

### The Map Object
The primary data structure for 2D spatial data. It combines the image array with metadata (FITS header) and a Coordinate Reference System (WCS), allowing for physically accurate plotting and cropping.

### Solar Coordinates
Solar physics uses many non-Cartesian frames. SunPy handles the math of projecting 3D solar positions onto 2D telescope planes, taking into account the Earth's position relative to the Sun.

### Fido (Federated IDO)
A unified interface for searching data. You define what you want (Time, Instrument, Wavelength), and Fido finds it across different providers automatically.

## Quick Reference

### Installation

```bash
pip install "sunpy[all]"
```

### Standard Imports

```python
import sunpy.map
import sunpy.coordinates
from sunpy.net import Fido, attrs as a
import astropy.units as u
from astropy.coordinates import SkyCoord
```

### Basic Pattern - Search, Download, and Plot

```python
from sunpy.net import Fido, attrs as a
import sunpy.map

# 1. Search for data
result = Fido.search(a.Time("2011/06/07 06:30", "2011/06/07 06:35"),
                     a.Instrument.aia,
                     a.Wavelength(171*u.angstrom))

# 2. Download (returns list of file paths)
# downloaded_files = Fido.fetch(result)

# 3. Create and plot map
# aiayamap = sunpy.map.Map(downloaded_files[0])
# aiayamap.peek()
```

## Critical Rules

### ✅ DO

- **Use sunpy.map.Map** - It is the only reliable way to handle solar images with correct coordinate metadata.
- **Use Physical Units** - Always use astropy.units for wavelengths, distances, and times.
- **Check Observer Information** - Solar coordinates depend on where the observer (usually Earth or a satellite) is. Ensure your map header has valid observer metadata.
- **Normalize Maps** - Use `map.plot(norm=...)` or `aiamap.exposure_time` to account for varying exposure times when comparing images.
- **Vectorize Coordinate Transforms** - SkyCoord arrays are much faster than individual points.
- **Use Fido for downloads** - It handles retries, local caching, and multiple providers seamlessly.

### ❌ DON'T

- **Plot with raw plt.imshow** - This ignores the World Coordinate System (WCS). Use `ax = plt.subplot(projection=my_map)` instead.
- **Ignore Time Scales** - Like Astropy, be careful with UTC vs TAI.
- **Hardcode Wavelengths** - Use `a.Wavelength(193 * u.AA)` to ensure the search is units-aware.
- **Crop manually** - Don't slice the numpy array; use `my_map.submap(bottom_left, top_right)` to preserve coordinate metadata.

## Anti-Patterns (NEVER)

```python
# ❌ BAD: Manual cropping by pixel indices
# cropped_data = my_map.data[100:200, 300:400] # Coordinates lost!

# ✅ GOOD: Submap using SkyCoord
from astropy.coordinates import SkyCoord
bottom_left = SkyCoord(-500*u.arcsec, -500*u.arcsec, frame=my_map.coordinate_frame)
top_right = SkyCoord(500*u.arcsec, 500*u.arcsec, frame=my_map.coordinate_frame)
submap = my_map.submap(bottom_left, top_right=top_right)

# ❌ BAD: Hardcoding solar radius or distance
# distance = 1.496e11 # meters

# ✅ GOOD: Get from map or constants
from sunpy.coordinates import sun
dist = my_map.dsun # Distance to Sun at observation time
```

## Solar Maps (sunpy.map)

### Manipulation and Visualization

```python
import sunpy.map
import matplotlib.pyplot as plt

# Load map
aia_map = sunpy.map.Map("aia_data.fits")

# Coordinate-aware plotting
fig = plt.figure()
ax = fig.add_subplot(projection=aia_map)
aia_map.plot(ax=ax)
aia_map.draw_limb(ax=ax, color='white')
aia_map.draw_grid(ax=ax, color='white', linestyle='dotted')

# Basic Map Math
# Note: Adding/subtracting maps is possible if they share the same WCS
diff_map = aia_map_t2 - aia_map_t1
```

## Solar Coordinates (sunpy.coordinates)

### Frame Transformations

```python
from sunpy.coordinates import frames

# Helioprojective (Arcsec from Sun center)
coord = SkyCoord(100*u.arcsec, 200*u.arcsec, frame=frames.Helioprojective, 
                 obstime="2023-01-01", observer="earth")

# Convert to Heliographic Stonyhurst (Lat/Lon on the Sun)
hgs_coord = coord.transform_to(frames.HeliographicStonyhurst)
print(f"Lat: {hgs_coord.lat}, Lon: {hgs_coord.lon}")

# Rotating a coordinate with the Sun's differential rotation
from sunpy.physics.differential_rotation import solar_rotate_coordinate
new_coord = solar_rotate_coordinate(coord, time="2023-01-02")
```

## Data Searching (sunpy.net.Fido)

### Complex Queries

```python
from sunpy.net import Fido, attrs as a

# Search for GOES X-ray flares AND AIA images simultaneously
query = Fido.search(
    a.Time("2012-08-31 19:00", "2012-08-31 20:00"),
    (a.Instrument.goes & a.XRayRange("low")) | 
    (a.Instrument.aia & a.Wavelength(171 * u.AA))
)

print(query)
# files = Fido.fetch(query)
```

## TimeSeries (sunpy.timeseries)

### Handling Light Curves

```python
import sunpy.timeseries as ts

# Load GOES data
goes = ts.TimeSeries("goes_data.nc")

# Plotting
goes.peek()

# Export to Pandas
df = goes.to_dataframe()
# Perform rolling mean in pandas
df_smooth = df.rolling('1min').mean()
```

## Solar Physics Algorithms

### Limb Fitting and Surface Math

```python
# Finding the solar limb in an image
from sunpy.map.maputils import all_coordinates_is_on_disk

# Mask pixels off-disk
mask = all_coordinates_is_on_disk(aia_map)
aia_map_masked = sunpy.map.Map(aia_map.data * mask, aia_map.meta)
```

## Practical Workflows

### 1. Overlaying AIA and HMI (Multi-Instrument Analysis)

```python
def plot_overlay(aia_file, hmi_file):
    aia = sunpy.map.Map(aia_file)
    hmi = sunpy.map.Map(hmi_file)
    
    # Re-project HMI to AIA's viewpoint
    hmi_reprojected = hmi.reproject_to(aia.wcs)
    
    fig = plt.figure()
    ax = fig.add_subplot(projection=aia)
    aia.plot(ax=ax)
    # Draw HMI contours (magnetic fields) over AIA (hot plasma)
    hmi_reprojected.draw_contours(ax=ax, levels=[-100, 100]*u.G, colors='white')
```

### 2. Measuring Flare Flux Evolution

```python
def get_flare_evolution(timeseries_file):
    goes = ts.TimeSeries(timeseries_file)
    # Filter for the X-ray flare window
    flare_data = goes.truncate("2017-09-06 11:50", "2017-09-06 12:30")
    
    # Get peak time and flux
    peak_time = flare_data.to_dataframe()['xrsa'].idxmax()
    return peak_time, flare_data.max()
```

### 3. Differential Rotation Correction for a Series of Images

```python
def rotate_map_series(maps, reference_time):
    rotated_maps = []
    for m in maps:
        # Rotate each map to the reference time
        m_rot = m.rotate(reproject=True, order=3) # Basic rotation
        # For actual solar surface rotation, use differential_rotation modules
        rotated_maps.append(m_rot)
    return rotated_maps
```

## Performance Optimization

### Downsampling for Preview

Large AIA images (4096x4096) are slow to plot.

```python
# Create a lower resolution map for fast display
aia_resampled = aia_map.resample([512, 512] * u.pix)
```

### Parallel Downloads

Fido.fetch can use multiple connections for faster downloads.

```python
files = Fido.fetch(result, path='./data/', max_conn=5)
```

## Common Pitfalls and Solutions

### The "Missing Observer" Error

Calculations fail because SunPy doesn't know where the satellite was.

```python
# ❌ Problem: SkyCoord transformation fails
# ✅ Solution: Manually set observer if missing in FITS header
from sunpy.coordinates import get_body_heliographic_stonyhurst
obs_coord = get_body_heliographic_stonyhurst('earth', aia_map.date)
aia_map.meta['hgln_obs'] = obs_coord.lon.value
aia_map.meta['hglt_obs'] = obs_coord.lat.value
aia_map.meta['dsun_obs'] = obs_coord.radius.to(u.m).value
```

### Orientation Issues (North is not Up)

Solar telescopes rotate.

```python
# ❌ Problem: Solar North is tilted in the raw image
# ✅ Solution: Rotate to align Solar North with the Y-axis
aia_rotated = aia_map.rotate() # This aligns the CROTA or PCi_j matrix
```

### Empty Search Results

Fido might return nothing if providers are down.

```python
# ✅ Solution: Always check result length
result = Fido.search(...)
if len(result) == 0:
    raise ValueError("No data found for the given criteria.")
```

SunPy is the definitive toolkit for exploring the dynamics of our closest star. By integrating physical units and solar-specific coordinate systems, it enables robust and reproducible heliophysics research.
