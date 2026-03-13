---
name: pyproj
description: Python interface to PROJ (cartographic projections and coordinate transformations library). Handles transformations between different Coordinate Reference Systems (CRS) and performs geodetic calculations (distance, area on ellipsoids). Use for coordinate transformations, CRS conversions, geodetic calculations, UTM projections, GPS coordinate conversions, ellipsoidal distance calculations, and spatial reference system operations.
version: 3.6
license: MIT
---

# PyProj - Coordinate Projections and Geodetic Math

PyProj is essential for any spatial analysis that requires high precision. It allows you to transform coordinates between thousands of different reference systems and compute distances on the Earth's ellipsoidal surface using the most accurate formulas (Vincenty, Karney).

## When to Use

- Converting GPS coordinates (WGS84) to local projected systems (e.g., UTM, Albers, State Plane).
- Calculating precise distances, bearings, and areas on the Earth's surface (Geodetic math).
- Defining custom Coordinate Reference Systems (CRS).
- Handling transformations between different vertical datums.
- Working with "Great Circle" paths and geodesics.
- Identifying the best UTM zone for a specific location.

## Reference Documentation

**Official docs**: https://pyproj4.github.io/pyproj/  
**PROJ (Engine)**: https://proj.org/  
**EPSG Registry**: https://epsg.io/ (Essential for finding CRS codes)  
**Search patterns**: `pyproj.Transformer`, `pyproj.CRS`, `pyproj.Geod`

## Core Principles

### CRS (Coordinate Reference System)
A definition of how numbers (coordinates) map to the real world. Can be defined via EPSG codes (EPSG:4326), PROJ strings, or WKT (Well-Known Text).

### Transformer
An object optimized for converting many points from one CRS to another. Always use Transformer for bulk operations rather than one-off calls.

### Geod
A class for performing "ellipsoid math". Use this for calculating distances on Earth without projecting to a flat map.

## Quick Reference

### Installation

```bash
pip install pyproj
```

### Standard Imports

```python
import pyproj
from pyproj import CRS, Transformer, Geod
```

### Basic Pattern - Transformation

```python
from pyproj import Transformer

# 1. Define the transformation (WGS84 to Web Mercator)
# always_xy=True ensures (lon, lat) order instead of PROJ default (lat, lon)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

# 2. Transform coordinates
lon, lat = -74.006, 40.7128 # NYC
x, y = transformer.transform(lon, lat)

print(f"Projected Meters: X={x:.2f}, Y={y:.2f}")
```

## Critical Rules

### ✅ DO

- **Use always_xy=True** - By default, PROJ 6+ uses the order defined by the CRS (often lat, lon). Setting always_xy=True forces the consistent longitude, latitude (X, Y) order.
- **Reuse Transformers** - Creating a Transformer is expensive. Create it once and use it for all points in your dataset.
- **Use Geod for distance** - If you need the distance between two GPS points, don't project them to a map; use Geod.inv() for ellipsoidal distance.
- **Check CRS Validity** - Use CRS.from_user_input(code).is_valid to verify your projection strings.
- **Vectorize** - Pass NumPy arrays or lists of coordinates to transformer.transform(). It is significantly faster than looping over points.

### ❌ DON'T

- **Project for short distances** - For global analysis, don't project to a flat map to calculate distance; map projections introduce distortion (e.g., Mercator makes the poles look huge).
- **Hardcode Proj4 strings** - Prefer EPSG codes (e.g., "EPSG:4326") as they are more robust and include modern datum transformations.
- **Ignore the Datum** - Remember that moving between different datums (e.g., NAD27 to WGS84) requires specific transformation parameters.

## Anti-Patterns (NEVER)

```python
from pyproj import Transformer, Geod

# ❌ BAD: Creating a transformer inside a loop (Extremely slow!)
for lon, lat in coordinates:
    t = Transformer.from_crs("EPSG:4326", "EPSG:32633") # Initialization overhead
    x, y = t.transform(lon, lat)

# ✅ GOOD: Initialize once, transform in bulk
t = Transformer.from_crs("EPSG:4326", "EPSG:32633", always_xy=True)
lons, lats = zip(*coordinates)
xs, ys = t.transform(lons, lats)

# ❌ BAD: Calculating distance on a flat projection over long distances
# x1, y1 = t.transform(lon1, lat1)
# x2, y2 = t.transform(lon2, lat2)
# dist = np.sqrt((x1-x2)**2 + (y1-y2)**2) # ❌ Distorted result!

# ✅ GOOD: Use Geod for geodesic distance
g = Geod(ellps='WGS84')
az12, az21, dist = g.inv(lon1, lat1, lon2, lat2) # ✅ Accurate meters
```

## Working with CRS (pyproj.CRS)

### Inspection and Comparison

```python
from pyproj import CRS

crs = CRS.from_epsg(4326)

# Accessing properties
print(crs.name)            # "WGS 84"
print(crs.area_of_use)     # Bounding box of applicability
print(crs.axis_info)       # Order of axes

# Check units
units = crs.axis_info[0].unit_name # 'degree' or 'metre'

# Comparing CRS
is_same = crs.equals(CRS.from_user_input("EPSG:4326"))
```

## Transformation (pyproj.Transformer)

### Handling Large Datasets

```python
import numpy as np
from pyproj import Transformer

# Random points in NYC area
lons = -74.0 + np.random.rand(10000)
lats = 40.7 + np.random.rand(10000)

transformer = Transformer.from_crs(4326, 3857, always_xy=True)

# Transform entire arrays at once (Vectorized)
xs, ys = transformer.transform(lons, lats)
```

## Geodetic Calculations (pyproj.Geod)

### Distance, Area, and Paths

```python
from pyproj import Geod

g = Geod(ellps='WGS84')

# 1. Inverse Transformation: Get distance and azimuth between points
# NYC to London
lon1, lat1 = -74.006, 40.7128
lon2, lat2 = -0.1278, 51.5074
az12, az21, dist = g.inv(lon1, lat1, lon2, lat2)
print(f"Distance: {dist/1000:.2f} km")

# 2. Forward Transformation: Find point given start, bearing, and distance
# Start at NYC, go 1000km East (bearing 90)
lon_new, lat_new, back_az = g.fwd(lon1, lat1, 90, 1000000)

# 3. Intermediate points (Great Circle path)
path = g.npts(lon1, lat1, lon2, lat2, npts=10) # 10 points along the path

# 4. Area of a polygon on the ellipsoid
lons = [-10, 10, 10, -10]
lats = [-10, -10, 10, 10]
area, perimeter = g.polygon_area_perimeter(lons, lats)
print(f"Area: {abs(area)/1e6:.2f} km²")
```

## Practical Workflows

### 1. Identifying the UTM Zone Automatically

```python
def get_utm_crs(lon, lat):
    """Returns the correct UTM CRS for a given lon/lat point."""
    utm_zone = int((lon + 180) / 6) + 1
    hemisphere = 'north' if lat >= 0 else 'south'
    # UTM EPSG ranges: 32601-32660 (North), 32701-32760 (South)
    base = 32600 if hemisphere == 'north' else 32700
    return CRS.from_epsg(base + utm_zone)

# Usage:
# my_crs = get_utm_crs(-74.0, 40.7) # Returns EPSG:32618 (UTM 18N)
```

### 2. Precise Point-to-Point Distance Matrix

```python
import numpy as np
from pyproj import Geod

def calculate_distance_matrix(lons, lats):
    """Computes a symmetric distance matrix using the ellipsoid."""
    g = Geod(ellps='WGS84')
    n = len(lons)
    matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i + 1, n):
            _, _, d = g.inv(lons[i], lats[i], lons[j], lats[j])
            matrix[i, j] = matrix[j, i] = d
    return matrix
```

### 3. Converting Local Measurements to GPS

```python
def local_to_gps(start_lon, start_lat, dx_meters, dy_meters):
    """Moves a GPS point by a local offset in meters."""
    g = Geod(ellps='WGS84')
    # Move in X (East-West)
    lon_tmp, lat_tmp, _ = g.fwd(start_lon, start_lat, 90 if dx_meters > 0 else 270, abs(dx_meters))
    # Move in Y (North-South)
    lon_final, lat_final, _ = g.fwd(lon_tmp, lat_tmp, 0 if dy_meters > 0 else 180, abs(dy_meters))
    return lon_final, lat_final
```

## Performance Optimization

### Using itransform for Iterators

If your data is coming from a generator and you don't want to load it all into memory, use itransform.

```python
# Generator of (x, y) tuples
coords_gen = ((lon, lat) for lon, lat in my_source)

for x, y in transformer.itransform(coords_gen):
    process(x, y)
```

### Parallel Transformation

Transformers are thread-safe. You can use them with concurrent.futures.

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as executor:
    results = list(executor.map(lambda p: transformer.transform(*p), list_of_points))
```

## Common Pitfalls and Solutions

### The "Infinities" Problem

Projecting points outside a CRS's valid area (e.g., projecting 90° latitude in Mercator) will result in inf or nan.

```python
# ✅ Solution: Check bounds before transforming
if not crs.area_of_use.contains(lon, lat):
    print("Point outside projection bounds!")
```

### Lat/Lon vs Lon/Lat

Historically, GIS users say "Lat/Lon", but mathematically X=Lon, Y=Lat.

```python
# ❌ Problem: transformer.transform(40.7, -74.0) -> Wrong result!
# ✅ Solution: Use always_xy=True and pass (Lon, Lat)
transformer = Transformer.from_crs(4326, 3857, always_xy=True)
transformer.transform(-74.0, 40.7)
```

### Accuracy of Geodetic Formulas

By default, Geod is very accurate, but for sub-millimeter precision in complex cases:

```python
# Use the Karney algorithm (built-in for modern pyproj)
g = Geod(ellps='WGS84') # This is already highly accurate
```

## Best Practices

1. Always use `always_xy=True` when creating Transformers to ensure consistent (lon, lat) ordering
2. Create Transformers once and reuse them for bulk operations
3. Use Geod for distance calculations on the ellipsoid rather than projecting to flat coordinates
4. Prefer EPSG codes over Proj4 strings for better robustness and modern datum support
5. Vectorize transformations by passing arrays/lists instead of looping over individual points
6. Check CRS validity and area of use before transforming coordinates
7. Be aware of datum transformations when converting between different reference systems
8. Use itransform for memory-efficient processing of large datasets from generators

PyProj is the definitive tool for coordinate precision. By abstracting the complex spherical and ellipsoidal trigonometry of Earth, it allows scientists to focus on their data while ensuring their spatial calculations remain geographically valid.
