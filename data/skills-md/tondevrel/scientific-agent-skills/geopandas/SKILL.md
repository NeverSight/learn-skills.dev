---
name: geopandas
description: Open source project to make working with geospatial data in python easier. Extends the datatypes used by pandas to allow spatial operations on geometric types. Built on top of Shapely, Fiona, and Pyproj. Use for reading and writing spatial formats (Shapefile, GeoJSON, GeoPackage, KML), performing spatial joins, coordinate system transformations (reprojecting), geometric analysis (buffers, centroids, convex hulls), thematic mapping (Choropleth maps), calculating spatial relationships (contains, overlaps, touches, within), working with OpenStreetMap data or satellite-derived vector data.
version: 0.14
license: BSD-3-Clause
---

# GeoPandas - Geospatial Data Analysis

GeoPandas enables you to perform spatial joins, geometric manipulations, and coordinate transformations using the familiar Pandas API. It treats "geometry" as just another column in a DataFrame, but one that knows how to calculate areas, distances, and intersections.

## When to Use

- Reading and writing spatial formats (Shapefile, GeoJSON, GeoPackage, KML).
- Performing spatial joins (e.g., "which points fall inside this polygon?").
- Coordinating system transformations (reprojecting from Lat/Lon to Meters).
- Geometric analysis (calculating buffers, centroids, convex hulls).
- Thematic mapping (Choropleth maps).
- Calculating spatial relationships (contains, overlaps, touches, within).
- Working with OpenStreetMap data or satellite-derived vector data.

## Reference Documentation

**Official docs**: https://geopandas.org/  
**Interactive tutorials**: https://geopandas.org/en/stable/gallery/index.html  
**Search patterns**: `gpd.read_file`, `gdf.to_crs`, `gpd.sjoin`, `gdf.buffer`, `gdf.explore`

## Core Principles

### The GeoDataFrame

A GeoDataFrame is a pandas.DataFrame that has at least one GeoSeries column (usually named geometry). Each row represents a feature (point, line, or polygon).

### Coordinate Reference Systems (CRS)

Data without a CRS is just numbers on a grid. To perform real-world calculations (like area in km²), you must define the CRS (e.g., WGS84 - EPSG:4326 or UTM).

### Predicates and Set Operations

Spatial analysis relies on binary predicates (intersects, within, contains) and set-theoretic operations (union, intersection, difference).

## Quick Reference

### Installation

```bash
pip install geopandas pyarrow pyproj fiona shapely
```

### Standard Imports

```python
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, Polygon
```

### Basic Pattern - Load and Plot

```python
import geopandas as gpd

# Load built-in dataset
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Filter and Project
europe = world[world.continent == 'Europe']
europe = europe.to_crs(epsg=3035) # Equal Area projection for Europe

# Plot
europe.plot(column='pop_est', legend=True, cmap='viridis')
```

## Critical Rules

### ✅ DO

- **Always check the CRS** - Verify `gdf.crs` before any spatial operation.
- **Project for measurements** - Use a projected CRS (meters/feet) like UTM before calculating area or distance.
- **Use Spatial Indexing** - For large datasets, use `gdf.sindex` or ensure `sjoin` is used to speed up queries.
- **Validate Geometries** - Use `gdf.is_valid` to find broken polygons (self-intersections).
- **Simplify for visualization** - Use `gdf.simplify()` to speed up plotting of complex borders.
- **Use .explore()** - For quick interactive maps in Jupyter (uses Leaflet/Folium).

### ❌ DON'T

- **Measure Area in Degrees** - Never calculate `.area` on a Lat/Lon CRS (EPSG:4326). The result will be in "square degrees" (meaningless).
- **Iterate with loops** - Avoid looping over rows; use vectorized spatial operations.
- **Ignore Topology** - Be aware that "touches" and "intersects" are different (boundary vs. interior).
- **Forget to set the Active Geometry** - If a GeoDataFrame has multiple geometry columns, specify which one to use via `gdf.set_geometry()`.

## Anti-Patterns (NEVER)

```python
# ❌ BAD: Manual distance calculation on Lat/Lon (ignores Earth's curvature)
def dist(p1, p2):
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

# ✅ GOOD: Reproject and use vectorized distance
gdf = gdf.to_crs(epsg=3857) # Web Mercator (meters)
distances = gdf.distance(other_point)

# ❌ BAD: Manually checking points in polygons
for i, poly in countries.iterrows():
    for j, pt in cities.iterrows():
        if poly.geometry.contains(pt.geometry):
            print("Found")

# ✅ GOOD: Spatial Join (Optimized with spatial index)
cities_with_country = gpd.sjoin(cities, countries, predicate='within')
```

## Geometry Creation and Manipulation

### Creating from Coordinates

```python
# From a Pandas DataFrame with Lat/Lon
df = pd.DataFrame({'City': ['NY', 'London'], 'Lat': [40.7, 51.5], 'Lon': [-74.0, -0.1]})
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Lon, df.Lat))
gdf.set_crs(epsg=4326, inplace=True)
```

### Geometric Operations

```python
# Centroids and Envelopes
gdf['centroid'] = gdf.centroid
gdf['envelope'] = gdf.envelope # Bounding box

# Buffering (Creating a zone around features)
# Warning: Do this in a projected CRS (meters)
stations_buffered = metro_stations.to_crs(epsg=32633).buffer(500) # 500 meters

# Unifying overlapping polygons
total_area = gdf.union_all()
```

## Spatial Queries

### Spatial Joins (sjoin)

```python
# Find which district each school belongs to
schools_in_districts = gpd.sjoin(schools, districts, how="inner", predicate="within")

# sjoin types:
# 'intersects' (default), 'contains', 'within', 'touches', 'overlaps', 'crosses'
```

### Overlays (Set Operations)

```python
# Intersection of two layers (e.g., protected area vs. forest)
forest_in_park = gpd.overlay(forests, parks, how='intersection')

# 'union', 'intersection', 'difference', 'symmetric_difference'
```

## Coordinate Reference Systems (CRS)

### Reprojection

```python
# Checking the current CRS
print(gdf.crs)

# Reprojecting to a specific EPSG code
# EPSG:4326 -> WGS84 (Degrees, used for GPS)
# EPSG:3857 -> Web Mercator (Meters, used for web maps)
gdf_meters = gdf.to_crs(epsg=3857)

# Match CRS of another layer
gdf_2 = gdf_2.to_crs(gdf_1.crs)
```

## Visualization

### Static and Interactive Maps

```python
# Layered plotting
fig, ax = plt.subplots(figsize=(10, 10))
base = countries.plot(ax=ax, color='white', edgecolor='black')
cities.plot(ax=base, marker='o', color='red', markersize=5)

# Interactive exploration (requires folium)
cities.explore(column='population', cmap='magma', m=None)
```

## Practical Workflows

### 1. Proximity Analysis (Point-in-Buffer)

```python
def find_entities_near_road(roads, entities, distance_m=1000):
    """Find all entities within 1km of any road."""
    # 1. Project to a metric CRS (e.g., UTM)
    roads_m = roads.to_crs(epsg=3857)
    entities_m = entities.to_crs(epsg=3857)
    
    # 2. Create buffer
    road_buffer = roads_m.buffer(distance_m)
    
    # 3. Create a GeoDataFrame from buffer to use in sjoin
    buffer_gdf = gpd.GeoDataFrame(geometry=road_buffer, crs=roads_m.crs)
    
    # 4. Spatial Join
    nearby = gpd.sjoin(entities_m, buffer_gdf, predicate='within')
    return nearby
```

### 2. Clipping Data to a Boundary

```python
def clip_data(data, boundary):
    """Clip a large vector dataset to a specific boundary polygon."""
    return gpd.clip(data, boundary)

# Usage: city_parks = clip_data(national_parks, city_limits)
```

### 3. Calculating Percentage Area Coverage

```python
def calculate_land_use_pct(region, land_use_layer):
    """Calculate what % of 'region' is covered by each land use type."""
    # Ensure CRS matches and is projected
    land_use_layer = land_use_layer.to_crs(region.crs)
    
    # Intersect region with land use
    intersections = gpd.overlay(land_use_layer, region, how='intersection')
    
    # Calculate area
    intersections['area'] = intersections.area
    total_area = region.area.sum()
    
    return intersections.groupby('class')['area'].sum() / total_area * 100
```

## Performance Optimization

### Using Spatial Index (sindex)

```python
# Check if a point is within any polygon in a large GDF efficiently
spatial_index = countries.sindex

# Find possible matches using bounding boxes first
possible_matches_index = list(spatial_index.intersection(target_point.bounds))
possible_matches = countries.iloc[possible_matches_index]

# Precise check only on candidates
precise_match = possible_matches[possible_matches.intersects(target_point)]
```

### Reading Large Files (Parquet)

```python
# GeoJSON is slow to read/write. GeoParquet is significantly faster and smaller.
gdf.to_parquet("large_data.parquet")
gdf = gpd.read_parquet("large_data.parquet")
```

## Common Pitfalls and Solutions

### CRS Mismatch

```python
# ❌ Problem: sjoin returns 0 results even if data looks overlapping
# ✅ Solution: Align CRS
if cities.crs != districts.crs:
    cities = cities.to_crs(districts.crs)
```

### Invalid Geometries (Self-intersections)

```python
# ❌ Problem: Overlay or Area calculation fails/gives weird results
# ✅ Solution: Fix with buffer(0) or check validity
invalid = gdf[~gdf.is_valid]
gdf['geometry'] = gdf['geometry'].buffer(0) # Common trick to fix minor topology errors
```

### Memory Exhaustion with Buffers

```python
# ❌ Problem: Buffering millions of points with high resolution
# ✅ Solution: Use low resolution or simplify
gdf.buffer(100, resolution=4) # Default is 16, 4 is often enough for analysis
```

GeoPandas bridges the gap between traditional GIS software and the Python data science stack. It makes spatial analysis as easy as writing a line of Pandas code.
