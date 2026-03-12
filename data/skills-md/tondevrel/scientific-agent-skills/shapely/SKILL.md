---
name: shapely
description: Manipulation and analysis of planar geometric objects. Based on the widely deployed GEOS library. Provides data structures for points, curves, and surfaces, and standardized algorithms for geometric operations. Use for 2D geometry operations, spatial relationships, set-theoretic operations (intersection, union, difference), point-in-polygon queries, geometric calculations (area, distance, centroid), buffering, simplifying geometries, linear referencing, and cleaning invalid geometries. Essential for GIS operations, spatial analysis, and geometric computations.
version: 2.0
license: BSD-3-Clause
---

# Shapely - Planar Geometry

Shapely is the engine behind GeoPandas and many other GIS tools. It focuses on the geometry itself: calculating intersections, unions, distances, and checking spatial relationships (like "is this point inside this polygon?").

## When to Use

- Precise manipulation of 2D geometric shapes.
- Performing set-theoretic operations (Intersection, Union, Difference).
- Checking spatial predicates (Contains, Within, Intersects, Touches).
- Cleaning and validating "dirty" geometry (fixing self-intersections).
- Calculating geometric properties (Area, Length, Centroid, Bounds).
- Generating buffers or simplifying complex lines.
- Linear referencing (finding points along a line).

## Reference Documentation

**Official docs**: https://shapely.readthedocs.io/  
**GEOS (Engine)**: https://libgeos.org/  
**Search patterns**: `shapely.geometry`, `shapely.ops.unary_union`, `shapely.validation.make_valid`

## Core Principles

### Geometric Objects

Objects are immutable. Once created, you don't change them; you perform an operation that returns a new object.

- **Points**: 0-dimensional.
- **LineStrings**: 1-dimensional curves.
- **Polygons**: 2-dimensional surfaces with optional holes.

### Cartesian Geometry

Shapely operates in a Cartesian plane. It does not know about Earth's curvature, latitudes, or longitudes. Distance is sqrt(dx² + dy²).

### Vectorization (Shapely 2.0+)

Modern Shapely supports vectorized operations on NumPy arrays of geometry objects, making it significantly faster than older versions.

## Quick Reference

### Installation

```bash
pip install shapely numpy
```

### Standard Imports

```python
import numpy as np
from shapely import Point, LineString, Polygon, MultiPoint, MultiPolygon
from shapely import ops, wkt, wkb
import shapely
```

### Basic Pattern - Creation and Analysis

```python
from shapely.geometry import Point, Polygon

# 1. Create objects
p = Point(0, 0)
poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])

# 2. Check relationships
is_inside = p.within(poly) # True
is_on_border = p.touches(poly) # False (interior counts as within)

# 3. Calculate
print(f"Area: {poly.area}")
print(f"Distance: {p.distance(Point(10, 10))}")
```

## Critical Rules

### ✅ DO

- **Check Validity** - Use `.is_valid` before complex operations. Invalid geometry (like a self-intersecting polygon) will cause errors.
- **Use unary_union** - When merging many polygons, `ops.unary_union([list])` is orders of magnitude faster than a loop of `p1.union(p2)`.
- **Prefer Vectorized Functions** - Use `shapely.intersects(array_a, array_b)` instead of loops for performance.
- **Use prepare()** - If you are checking many points against the same polygon, use `shapely.prepare(poly)` to speed up subsequent queries.
- **Simplify for Analysis** - Use `.simplify(tolerance)` for complex boundaries to improve performance if high precision isn't required.

### ❌ DON'T

- **Mix Cartesian and Spherical** - Don't calculate distance on Lat/Lon points; the result will be in meaningless "degrees".
- **Assume Polygon Orientation** - While Shapely handles it, remember that exterior rings should ideally be counter-clockwise and holes clockwise.
- **Use for 3D Math** - Shapely supports Z-coordinates for storage, but most operations (like area, intersection) ignore Z and project onto the XY plane.
- **Loop over large collections** - Use NumPy-style vectorization provided in Shapely 2.0+.

## Anti-Patterns (NEVER)

```python
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

# ❌ BAD: Merging geometries in a loop (O(n²) complexity)
result = geometries[0]
for g in geometries[1:]:
    result = result.union(g)

# ✅ GOOD: Use unary_union (O(n log n) complexity)
result = unary_union(geometries)

# ❌ BAD: Checking many points without preparing
for p in many_points:
    if complex_poly.contains(p): # Slow for complex shapes
        pass

# ✅ GOOD: Prepare the geometry (Builds a spatial index)
from shapely import prepare
prepare(complex_poly)
for p in many_points:
    if complex_poly.contains(p): # Much faster
        pass
```

## Geometry Types and Creation

### Standard Primitives

```python
# Point (x, y, z)
pt = Point(1.0, 2.0)

# LineString (Ordered sequence of points)
line = LineString([(0, 0), (1, 1), (2, 0)])

# Polygon (Shell, [Holes])
shell = [(0, 0), (10, 0), (10, 10), (0, 10)]
hole = [(2, 2), (2, 4), (4, 4), (4, 2)]
poly = Polygon(shell, [hole])

# Multi-Geometries (Collections)
points = MultiPoint([(0,0), (1,1)])
```

## Spatial Predicates (Relationships)

### Checking how objects relate

```python
a = Point(1, 1).buffer(1.5) # A circle
b = Polygon([(0,0), (2,0), (2,2), (0,2)]) # A square

print(a.intersects(b))  # Shared space?
print(a.contains(b))    # B entirely inside A?
print(a.disjoint(b))    # No shared space?
print(a.overlaps(b))    # Same dimension, shared space, but not within?
print(a.touches(b))     # Only boundaries share space?
print(a.crosses(b))     # Line crossing a polygon?
```

## Set-Theoretic Operations

### Creating new geometries from old ones

```python
poly1 = Point(0, 0).buffer(1)
poly2 = Point(1, 0).buffer(1)

# Intersection (Shared area)
inter = poly1.intersection(poly2)

# Union (Combined area)
union = poly1.union(poly2)

# Difference (Area in poly1 NOT in poly2)
diff = poly1.difference(poly2)

# Symmetric Difference (Area in either but NOT both)
sdiff = poly1.symmetric_difference(poly2)
```

## Constructive Methods

### Buffering, Splicing, and Simplifying

```python
# Buffer: Expand/shrink geometry
# cap_style: 1=Round, 2=Flat, 3=Square
line_thick = line.buffer(0.5, cap_style=2)

# Centroid: Geometric center
center = poly.centroid

# Representative Point: Guaranteed to be INSIDE the geometry
# Useful for label placement in U-shaped polygons
label_pt = poly.representative_point()

# Simplify: Reduce number of vertices
simple_line = complex_line.simplify(tolerance=0.1, preserve_topology=True)

# Convex Hull: Smallest convex box containing all points
hull = MultiPoint(points).convex_hull
```

## Linear Referencing

### Working with positions along a LineString

```python
line = LineString([(0, 0), (0, 10), (10, 10)])

# Find distance along line to the point nearest to (5, 5)
dist = line.project(Point(5, 5)) # returns 5.0 (it's at (0, 5))

# Find the actual point at a specific distance along the line
pt = line.interpolate(15.0) # returns Point(5, 10)
```

## I/O: WKT, WKB, and NumPy

### Serialization and Data Exchange

```python
# WKT (Well-Known Text) - Human readable
text = "POINT (10 20)"
p = wkt.loads(text)
print(p.wkt)

# WKB (Well-Known Binary) - Fast and compact
binary = wkb.dumps(p)
p_new = wkb.loads(binary)

# NumPy Integration (Shapely 2.0)
points_array = np.array([Point(0,0), Point(1,1), Point(2,2)])
areas = shapely.area(points_array) # Returns array of zeros
dist_matrix = shapely.distance(points_array[:, np.newaxis], points_array)
```

## Practical Workflows

### 1. Cleaning Invalid Geometries

```python
from shapely.validation import make_valid

def safe_area(geom):
    """Calculates area even for invalid/self-intersecting polygons."""
    if not geom.is_valid:
        geom = make_valid(geom)
    
    # After make_valid, a Polygon might become a MultiPolygon or GeometryCollection
    return geom.area
```

### 2. Point-in-Polygon Search (Optimized)

```python
from shapely import prepare

def find_points_in_poly(points, poly):
    """Efficiently filters points inside a complex polygon."""
    prepare(poly) # Builds internal STRtree or spatial index
    
    # Using vectorized intersection (much faster)
    mask = shapely.contains(poly, points)
    return points[mask]
```

### 3. Splitting a Polygon by a Line

```python
from shapely.ops import split

def divide_land(polygon, line):
    """Splits a polygon into multiple parts using a LineString."""
    result = split(polygon, line)
    # Returns a GeometryCollection of the resulting parts
    return list(result.geoms)
```

## Performance Optimization

### STRtree for Nearest Neighbors

If you have thousands of geometries and need to find which ones are near a point, use STRtree.

```python
from shapely import STRtree

tree = STRtree(geometries)

# Find indices of geometries whose bounding boxes intersect the point's buffer
indices = tree.query(Point(0,0).buffer(10))

# Find the single nearest geometry index
nearest_idx = tree.nearest(Point(0,0))
```

## Common Pitfalls and Solutions

### The "Sliver Polygon" problem

Calculations like intersection can sometimes produce tiny, almost invisible polygons due to floating-point errors.

```python
# ✅ Solution: Filter by area
intersection = p1.intersection(p2)
if intersection.area < 1e-9:
    intersection = None
```

### Latitude/Longitude Confusion

Points are (x, y). In GIS, this usually means (Longitude, Latitude).

```python
# ❌ Error: Point(Latitude, Longitude)
# This will plot your maps sideways!
# ✅ Solution: Always use (Lon, Lat) to match (X, Y)
nyc = Point(-74.006, 40.7128)
```

### GeometryCollections

Operations like split or intersection can return GeometryCollection. This is a container for mixed types.

```python
# ❌ Problem: Calling .area on a collection with Lines and Polygons
# ✅ Solution: Filter for the type you want
polys = [g for g in collection.geoms if g.geom_type == 'Polygon']
```

## Best Practices

1. Always validate geometry with `.is_valid` before complex operations
2. Use `unary_union` instead of looping over unions
3. Prepare geometries with `prepare()` when checking many points against the same shape
4. Use vectorized operations in Shapely 2.0+ for performance
5. Remember Shapely is Cartesian - don't use lat/lon directly for distance calculations
6. Filter sliver polygons by area threshold after geometric operations
7. Use STRtree for spatial indexing when working with many geometries
8. Simplify complex geometries when high precision isn't required
9. Handle GeometryCollections properly - filter by geometry type when needed
10. Use representative_point() for guaranteed interior points in complex polygons

Shapely is a specialized, sharp tool. It doesn't care about your coordinate system or your file format — it only cares about the pure, mathematical relationship between shapes. Mastering it is the key to building advanced spatial algorithms.
