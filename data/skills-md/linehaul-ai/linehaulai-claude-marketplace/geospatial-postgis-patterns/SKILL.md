---
name: geospatial-postgis-patterns
description: Implement geofences, spatial queries, real-time tracking, and mapping features in laneweaverTMS using PostGIS and PGRouting. Use when building location-based features, distance calculations, ETA predictions, or fleet visualization.
keywords: [postgis, geospatial, gis, location-tracking, mapping]
---

# Geospatial Patterns - PostGIS for laneweaverTMS

## When to Use This Skill

Use when:
- Creating geofence boundaries around facilities
- Calculating distances between points (truck to facility, origin to destination)
- Detecting geofence entry/exit events for tracking
- Building ETA calculations or routing features
- Querying fleet positions and historical tracks
- Implementing spatial indexes for location queries
- Integrating with mapping frontends (Mapbox, Leaflet)

## PostGIS Fundamentals

### Geography vs Geometry Types

**Use `geography` for real-world distance calculations**:

| Type | Use Case | Distance Unit | Earth Curvature |
|------|----------|---------------|-----------------|
| `geography` | GPS coordinates, long distances | Meters | Accounts for curvature |
| `geometry` | Local/planar operations, contains checks | Projection units | Ignores curvature |

```sql
-- Geography: accurate distances in meters for GPS data
SELECT ST_Distance(
    ST_MakePoint(-87.6298, 41.8781)::geography,  -- Chicago
    ST_MakePoint(-122.4194, 37.7749)::geography  -- San Francisco
) / 1609.34 AS distance_miles;
-- Returns: ~1856 miles (accurate)

-- Geometry: faster but less accurate for large distances
SELECT ST_Distance(
    ST_SetSRID(ST_MakePoint(-87.6298, 41.8781), 4326),
    ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)
) AS distance_degrees;
-- Returns: degrees (must convert, less accurate for long distances)
```

### SRID 4326 (WGS84)

**All GPS coordinates use SRID 4326** (World Geodetic System 1984):

```sql
-- Creating a point from GPS coordinates
ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)

-- Creating a geography point (preferred for distance calculations)
ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography

-- Example: Create point for a facility location
ST_SetSRID(ST_MakePoint(-87.6298, 41.8781), 4326)::geography
```

**Important**: PostGIS uses (longitude, latitude) order, NOT (latitude, longitude).

## Geofence Table Design

### Table Structure

```sql
-- Migration: Create geofences table

CREATE TABLE public.geofences (
    -- Primary key
    id UUID DEFAULT gen_random_uuid() NOT NULL,

    -- Identification
    name TEXT NOT NULL,
    description TEXT,

    -- Relationship to facility (optional - standalone geofences allowed)
    facility_id UUID REFERENCES facilities(id) ON DELETE SET NULL,

    -- Spatial boundary - geography type for accurate distance calculations
    boundary geography(Polygon, 4326) NOT NULL,

    -- For circular geofences, store radius for reference
    radius_miles NUMERIC(10,2),

    -- Geofence type for business logic
    geofence_type TEXT NOT NULL DEFAULT 'facility',

    -- Active flag for enabling/disabling
    is_active BOOLEAN NOT NULL DEFAULT true,

    -- Standard audit columns
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    created_by INT4,
    updated_by INT4,
    deleted_at TIMESTAMPTZ,
    deleted_by INT4,

    CONSTRAINT geofences_pkey PRIMARY KEY (id),
    CONSTRAINT chk_geofences_type CHECK (
        geofence_type IN ('facility', 'city', 'region', 'custom')
    )
);

COMMENT ON TABLE public.geofences IS
    'Geographic boundaries for tracking events (arrival, departure, dwell time)';

COMMENT ON COLUMN public.geofences.boundary IS
    'Polygon boundary in WGS84 (SRID 4326). Use geography type for accurate distance calculations';

COMMENT ON COLUMN public.geofences.radius_miles IS
    'For circular geofences, the original radius used to generate the boundary polygon';
```

### Creating Circular Geofences

```sql
-- Create a circular geofence around a facility
INSERT INTO geofences (name, facility_id, boundary, radius_miles, geofence_type)
SELECT
    f.name || ' Geofence',
    f.id,
    -- ST_Buffer creates a circle; convert miles to meters (1 mile = 1609.34 meters)
    ST_Buffer(
        ST_SetSRID(ST_MakePoint(f.longitude, f.latitude), 4326)::geography,
        0.5 * 1609.34  -- 0.5 mile radius in meters
    ),
    0.5,
    'facility'
FROM facilities f
WHERE f.id = $1;
```

### Creating Polygon Geofences

```sql
-- Create a custom polygon geofence (e.g., terminal yard)
INSERT INTO geofences (name, boundary, geofence_type)
VALUES (
    'Terminal Yard A',
    ST_GeomFromText(
        'POLYGON((-87.630 41.878, -87.628 41.878, -87.628 41.876, -87.630 41.876, -87.630 41.878))',
        4326
    )::geography,
    'custom'
);
```

## Spatial Indexes

### Critical: Index All Spatial Columns

```sql
-- Migration: Add spatial indexes to geofences table

-- GIST index on geofence boundaries (required for spatial queries)
CREATE INDEX idx_geofences_boundary
    ON public.geofences USING GIST(boundary);

-- Standard indexes
CREATE INDEX idx_geofences_facility_id
    ON public.geofences(facility_id)
    WHERE facility_id IS NOT NULL;

CREATE INDEX idx_geofences_deleted_at
    ON public.geofences(deleted_at)
    WHERE deleted_at IS NULL;

CREATE INDEX idx_geofences_is_active
    ON public.geofences(is_active)
    WHERE is_active = true;
```

### Index for load_cognition Location Queries

```sql
-- Create index on load_cognition for location-based queries
-- Note: Creates expression index since location is stored as lat/lon columns

CREATE INDEX idx_load_cognition_location
    ON public.load_cognition USING GIST(
        ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography
    );

-- Alternative: Partial index for valid coordinates only
CREATE INDEX idx_load_cognition_location_valid
    ON public.load_cognition USING GIST(
        ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography
    )
    WHERE latitude IS NOT NULL
      AND longitude IS NOT NULL
      AND latitude BETWEEN -90 AND 90
      AND longitude BETWEEN -180 AND 180;
```

### Index for facilities Table

```sql
-- Create spatial index on facilities for proximity queries
CREATE INDEX idx_facilities_location
    ON public.facilities USING GIST(
        ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography
    )
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
```

## Common Spatial Queries

### ST_Distance: Calculate Distance Between Points

```sql
-- Distance from truck to destination facility (in miles)
SELECT
    lc.load_id,
    ST_Distance(
        ST_SetSRID(ST_MakePoint(lc.longitude, lc.latitude), 4326)::geography,
        ST_SetSRID(ST_MakePoint(f.longitude, f.latitude), 4326)::geography
    ) / 1609.34 AS distance_miles
FROM load_cognition lc
JOIN loads l ON lc.load_id = l.id
JOIN stops s ON l.id = s.load_id AND s.stop_type = 'destination'
JOIN facilities f ON s.facility_id = f.id
WHERE lc.load_id = $1
ORDER BY lc.cognition_time DESC
LIMIT 1;
```

### ST_DWithin: Find Points Within Radius

```sql
-- Find all trucks within 50 miles of a facility
SELECT
    lc.load_id,
    l.load_number,
    lc.driver_name,
    ST_Distance(
        ST_SetSRID(ST_MakePoint(lc.longitude, lc.latitude), 4326)::geography,
        ST_SetSRID(ST_MakePoint(f.longitude, f.latitude), 4326)::geography
    ) / 1609.34 AS distance_miles
FROM load_cognition lc
JOIN loads l ON lc.load_id = l.id
CROSS JOIN (
    SELECT longitude, latitude FROM facilities WHERE id = $1
) f
WHERE ST_DWithin(
    ST_SetSRID(ST_MakePoint(lc.longitude, lc.latitude), 4326)::geography,
    ST_SetSRID(ST_MakePoint(f.longitude, f.latitude), 4326)::geography,
    50 * 1609.34  -- 50 miles in meters
)
AND lc.cognition_time > now() - INTERVAL '1 hour'
ORDER BY distance_miles;
```

### ST_Contains: Check if Point is Inside Polygon

```sql
-- Check if truck is inside any active geofence
SELECT g.id, g.name, g.facility_id
FROM geofences g
WHERE ST_Contains(
    g.boundary::geometry,
    ST_SetSRID(ST_MakePoint($longitude, $latitude), 4326)
)
AND g.is_active = true
AND g.deleted_at IS NULL;
```

### ST_Buffer: Create Radius Around Point

```sql
-- Create a 10-mile buffer zone around current truck position
SELECT ST_Buffer(
    ST_SetSRID(ST_MakePoint($longitude, $latitude), 4326)::geography,
    10 * 1609.34  -- 10 miles in meters
) AS buffer_zone;

-- Find facilities within buffer
SELECT f.id, f.name, f.city, f.state
FROM facilities f
WHERE ST_DWithin(
    ST_SetSRID(ST_MakePoint(f.longitude, f.latitude), 4326)::geography,
    ST_SetSRID(ST_MakePoint($longitude, $latitude), 4326)::geography,
    10 * 1609.34
)
AND f.deleted_at IS NULL;
```

## Geofence Event Detection

### Check Geofence Entry

```sql
-- Function to check if a position is inside any geofence
CREATE OR REPLACE FUNCTION public.check_geofence_entry(
    p_longitude NUMERIC,
    p_latitude NUMERIC
)
RETURNS TABLE (
    geofence_id UUID,
    geofence_name TEXT,
    facility_id UUID,
    geofence_type TEXT
)
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = 'public'
AS $$
BEGIN
    RETURN QUERY
    SELECT
        g.id,
        g.name,
        g.facility_id,
        g.geofence_type
    FROM geofences g
    WHERE ST_Contains(
        g.boundary::geometry,
        ST_SetSRID(ST_MakePoint(p_longitude, p_latitude), 4326)
    )
    AND g.is_active = true
    AND g.deleted_at IS NULL;
END;
$$;

COMMENT ON FUNCTION public.check_geofence_entry(NUMERIC, NUMERIC) IS
    'Returns all active geofences containing the given GPS coordinates';
```

### Geofence Event Table

```sql
-- Table to track geofence entry/exit events
CREATE TABLE public.geofence_events (
    id UUID DEFAULT gen_random_uuid() NOT NULL,

    load_id UUID NOT NULL REFERENCES loads(id) ON DELETE CASCADE,
    geofence_id UUID NOT NULL REFERENCES geofences(id) ON DELETE CASCADE,

    event_type TEXT NOT NULL,  -- 'entry', 'exit', 'dwell'
    event_time TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Position at time of event
    latitude NUMERIC(10,7),
    longitude NUMERIC(11,7),

    -- Dwell time tracking (for exit events)
    entry_time TIMESTAMPTZ,
    dwell_minutes INTEGER,

    -- Standard audit columns
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,

    CONSTRAINT geofence_events_pkey PRIMARY KEY (id),
    CONSTRAINT chk_geofence_events_type CHECK (
        event_type IN ('entry', 'exit', 'dwell')
    )
);

CREATE INDEX idx_geofence_events_load_id ON geofence_events(load_id);
CREATE INDEX idx_geofence_events_geofence_id ON geofence_events(geofence_id);
CREATE INDEX idx_geofence_events_event_time ON geofence_events(event_time);
```

### Detect Entry/Exit Pattern

```sql
-- Function to process location update and detect geofence events
CREATE OR REPLACE FUNCTION public.process_location_geofence(
    p_load_id UUID,
    p_longitude NUMERIC,
    p_latitude NUMERIC,
    p_timestamp TIMESTAMPTZ DEFAULT now()
)
RETURNS SETOF geofence_events
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = 'public'
AS $$
DECLARE
    v_current_geofences UUID[];
    v_previous_geofences UUID[];
    v_entered_geofence UUID;
    v_exited_geofence UUID;
    v_entry_time TIMESTAMPTZ;
    v_event geofence_events;
BEGIN
    -- Get current geofences containing this position
    SELECT ARRAY_AGG(g.id) INTO v_current_geofences
    FROM geofences g
    WHERE ST_Contains(
        g.boundary::geometry,
        ST_SetSRID(ST_MakePoint(p_longitude, p_latitude), 4326)
    )
    AND g.is_active = true
    AND g.deleted_at IS NULL;

    -- Get previously active geofences for this load
    SELECT ARRAY_AGG(DISTINCT ge.geofence_id) INTO v_previous_geofences
    FROM geofence_events ge
    WHERE ge.load_id = p_load_id
      AND ge.event_type = 'entry'
      AND NOT EXISTS (
          SELECT 1 FROM geofence_events ge2
          WHERE ge2.load_id = p_load_id
            AND ge2.geofence_id = ge.geofence_id
            AND ge2.event_type = 'exit'
            AND ge2.event_time > ge.event_time
      );

    -- Handle NULL arrays
    v_current_geofences := COALESCE(v_current_geofences, ARRAY[]::UUID[]);
    v_previous_geofences := COALESCE(v_previous_geofences, ARRAY[]::UUID[]);

    -- Detect entries (in current but not in previous)
    FOR v_entered_geofence IN
        SELECT UNNEST(v_current_geofences)
        EXCEPT
        SELECT UNNEST(v_previous_geofences)
    LOOP
        INSERT INTO geofence_events (load_id, geofence_id, event_type, event_time, latitude, longitude)
        VALUES (p_load_id, v_entered_geofence, 'entry', p_timestamp, p_latitude, p_longitude)
        RETURNING * INTO v_event;
        RETURN NEXT v_event;
    END LOOP;

    -- Detect exits (in previous but not in current)
    FOR v_exited_geofence IN
        SELECT UNNEST(v_previous_geofences)
        EXCEPT
        SELECT UNNEST(v_current_geofences)
    LOOP
        -- Get entry time for dwell calculation
        SELECT ge.event_time INTO v_entry_time
        FROM geofence_events ge
        WHERE ge.load_id = p_load_id
          AND ge.geofence_id = v_exited_geofence
          AND ge.event_type = 'entry'
        ORDER BY ge.event_time DESC
        LIMIT 1;

        INSERT INTO geofence_events (
            load_id, geofence_id, event_type, event_time,
            latitude, longitude, entry_time, dwell_minutes
        )
        VALUES (
            p_load_id, v_exited_geofence, 'exit', p_timestamp,
            p_latitude, p_longitude, v_entry_time,
            EXTRACT(EPOCH FROM (p_timestamp - v_entry_time)) / 60
        )
        RETURNING * INTO v_event;
        RETURN NEXT v_event;
    END LOOP;

    RETURN;
END;
$$;

COMMENT ON FUNCTION public.process_location_geofence(UUID, NUMERIC, NUMERIC, TIMESTAMPTZ) IS
    'Processes location update and generates geofence entry/exit events';
```

## ETA Calculations

### Basic Distance-Based ETA

```sql
-- Calculate simple ETA based on distance and average speed
CREATE OR REPLACE FUNCTION public.calculate_eta(
    p_current_lon NUMERIC,
    p_current_lat NUMERIC,
    p_dest_lon NUMERIC,
    p_dest_lat NUMERIC,
    p_avg_speed_mph NUMERIC DEFAULT 50
)
RETURNS TIMESTAMPTZ
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = 'public'
AS $$
DECLARE
    v_distance_miles NUMERIC;
    v_hours NUMERIC;
BEGIN
    -- Calculate distance in miles
    v_distance_miles := ST_Distance(
        ST_SetSRID(ST_MakePoint(p_current_lon, p_current_lat), 4326)::geography,
        ST_SetSRID(ST_MakePoint(p_dest_lon, p_dest_lat), 4326)::geography
    ) / 1609.34;

    -- Calculate travel time
    v_hours := v_distance_miles / p_avg_speed_mph;

    RETURN now() + (v_hours || ' hours')::INTERVAL;
END;
$$;

COMMENT ON FUNCTION public.calculate_eta(NUMERIC, NUMERIC, NUMERIC, NUMERIC, NUMERIC) IS
    'Calculates ETA based on straight-line distance and average speed. For accurate routing, integrate with external routing API';
```

### ETA for Load with Stops

```sql
-- Calculate ETA to next stop for a load
SELECT
    l.load_number,
    s.stop_sequence,
    f.name AS facility_name,
    ST_Distance(
        ST_SetSRID(ST_MakePoint(lc.longitude, lc.latitude), 4326)::geography,
        ST_SetSRID(ST_MakePoint(f.longitude, f.latitude), 4326)::geography
    ) / 1609.34 AS distance_miles,
    now() + (
        (ST_Distance(
            ST_SetSRID(ST_MakePoint(lc.longitude, lc.latitude), 4326)::geography,
            ST_SetSRID(ST_MakePoint(f.longitude, f.latitude), 4326)::geography
        ) / 1609.34) / 50  -- Assume 50 mph average
        || ' hours'
    )::INTERVAL AS estimated_arrival
FROM loads l
JOIN stops s ON l.id = s.load_id
JOIN facilities f ON s.facility_id = f.id
JOIN LATERAL (
    SELECT longitude, latitude
    FROM load_cognition
    WHERE load_id = l.id
    ORDER BY cognition_time DESC
    LIMIT 1
) lc ON true
WHERE l.id = $1
  AND s.actual_arrival IS NULL  -- Not yet arrived
ORDER BY s.stop_sequence
LIMIT 1;
```

### PGRouting Integration Points

For accurate routing with road networks:

```sql
-- PGRouting requires a road network table
-- This is typically populated from OpenStreetMap data

-- Example: Calculate route distance using Dijkstra algorithm
-- Note: Requires pgr_createTopology and road network data

-- SELECT
--     sum(cost) AS total_distance,
--     ST_Union(geom) AS route_geometry
-- FROM pgr_dijkstra(
--     'SELECT id, source, target, cost FROM roads',
--     $start_node, $end_node,
--     directed := false
-- ) AS route
-- JOIN roads ON route.edge = roads.id;

-- For production ETA calculations, consider:
-- 1. External routing APIs (OSRM, Google Directions, Here)
-- 2. Pre-calculated route distances in lanes table
-- 3. Mileage tables from PC*MILER or similar
```

## Real-Time Tracking Patterns

### load_cognition Table Structure

The `load_cognition` table stores GPS tracking data:

```sql
-- Key columns in load_cognition
-- id UUID
-- load_id UUID (FK to loads)
-- driver_name TEXT
-- latitude NUMERIC(10,7)
-- longitude NUMERIC(11,7)
-- cognition_time TIMESTAMPTZ
-- speed_mph NUMERIC
-- heading NUMERIC
-- source TEXT (e.g., 'eld', 'mobile', 'manual')
```

### Query Current Fleet Positions

```sql
-- Get current position of all active loads
SELECT DISTINCT ON (l.id)
    l.id AS load_id,
    l.load_number,
    l.load_status,
    lc.driver_name,
    lc.latitude,
    lc.longitude,
    lc.speed_mph,
    lc.cognition_time,
    -- Calculate time since last update
    EXTRACT(EPOCH FROM (now() - lc.cognition_time)) / 60 AS minutes_since_update
FROM loads l
JOIN load_cognition lc ON l.id = lc.load_id
WHERE l.load_status IN ('dispatched', 'at_origin', 'in_transit', 'at_destination')
  AND l.deleted_at IS NULL
  AND lc.latitude IS NOT NULL
  AND lc.longitude IS NOT NULL
ORDER BY l.id, lc.cognition_time DESC;
```

### Historical Track Query

```sql
-- Get tracking history for a load (for route visualization)
SELECT
    lc.latitude,
    lc.longitude,
    lc.cognition_time,
    lc.speed_mph,
    lc.heading
FROM load_cognition lc
WHERE lc.load_id = $1
  AND lc.latitude IS NOT NULL
  AND lc.longitude IS NOT NULL
ORDER BY lc.cognition_time ASC;
```

### Track as GeoJSON LineString

```sql
-- Get tracking history as GeoJSON for map display
SELECT json_build_object(
    'type', 'Feature',
    'properties', json_build_object(
        'load_id', $1::text,
        'point_count', count(*)
    ),
    'geometry', json_build_object(
        'type', 'LineString',
        'coordinates', json_agg(
            json_build_array(longitude, latitude)
            ORDER BY cognition_time
        )
    )
) AS geojson
FROM load_cognition
WHERE load_id = $1
  AND latitude IS NOT NULL
  AND longitude IS NOT NULL;
```

## Frontend Mapping Integration

### GeoJSON Output for Mapbox/Leaflet

```sql
-- Facilities as GeoJSON FeatureCollection
SELECT json_build_object(
    'type', 'FeatureCollection',
    'features', json_agg(
        json_build_object(
            'type', 'Feature',
            'id', f.id,
            'properties', json_build_object(
                'name', f.name,
                'city', f.city,
                'state', f.state,
                'facility_type', f.facility_type
            ),
            'geometry', json_build_object(
                'type', 'Point',
                'coordinates', json_build_array(f.longitude, f.latitude)
            )
        )
    )
) AS geojson
FROM facilities f
WHERE f.latitude IS NOT NULL
  AND f.longitude IS NOT NULL
  AND f.deleted_at IS NULL;
```

### Geofence Boundaries as GeoJSON

```sql
-- Export geofences as GeoJSON for map overlay
SELECT json_build_object(
    'type', 'FeatureCollection',
    'features', json_agg(
        json_build_object(
            'type', 'Feature',
            'id', g.id,
            'properties', json_build_object(
                'name', g.name,
                'geofence_type', g.geofence_type,
                'facility_id', g.facility_id
            ),
            'geometry', ST_AsGeoJSON(g.boundary::geometry)::json
        )
    )
) AS geojson
FROM geofences g
WHERE g.is_active = true
  AND g.deleted_at IS NULL;
```

### Fleet Positions as GeoJSON

```sql
-- Current fleet positions for real-time map
SELECT json_build_object(
    'type', 'FeatureCollection',
    'features', (
        SELECT json_agg(
            json_build_object(
                'type', 'Feature',
                'id', t.load_id,
                'properties', json_build_object(
                    'load_number', t.load_number,
                    'load_status', t.load_status,
                    'driver_name', t.driver_name,
                    'speed_mph', t.speed_mph,
                    'last_update', t.cognition_time
                ),
                'geometry', json_build_object(
                    'type', 'Point',
                    'coordinates', json_build_array(t.longitude, t.latitude)
                )
            )
        )
        FROM (
            SELECT DISTINCT ON (l.id)
                l.id AS load_id,
                l.load_number,
                l.load_status,
                lc.driver_name,
                lc.latitude,
                lc.longitude,
                lc.speed_mph,
                lc.cognition_time
            FROM loads l
            JOIN load_cognition lc ON l.id = lc.load_id
            WHERE l.load_status IN ('dispatched', 'at_origin', 'in_transit', 'at_destination')
              AND l.deleted_at IS NULL
              AND lc.latitude IS NOT NULL
            ORDER BY l.id, lc.cognition_time DESC
        ) t
    )
) AS geojson;
```

### LayerChart Integration

For geographic visualizations in the frontend, use the `layerchart` plugin:

- **Choropleth**: State/region heat maps for load volume or revenue
- **Bubble Map**: Facility markers sized by load count
- **GeoPath**: Route visualization with tracking data
- **GeoTile**: Background map tiles for context

Reference the `layerchart` skill for component patterns and data transformation utilities.

## PostGIS Functions Quick Reference

| Function | Purpose | Example |
|----------|---------|---------|
| `ST_MakePoint(lon, lat)` | Create point from coordinates | `ST_MakePoint(-87.6298, 41.8781)` |
| `ST_SetSRID(geom, srid)` | Assign coordinate system | `ST_SetSRID(point, 4326)` |
| `ST_Distance(a, b)` | Distance between geometries (meters for geography) | `ST_Distance(a::geography, b::geography)` |
| `ST_DWithin(a, b, dist)` | True if within distance | `ST_DWithin(a, b, 80467)` (50 miles) |
| `ST_Contains(poly, point)` | True if polygon contains point | `ST_Contains(geofence, truck_pos)` |
| `ST_Buffer(geom, dist)` | Create buffer zone | `ST_Buffer(point::geography, 1609.34)` (1 mile) |
| `ST_AsGeoJSON(geom)` | Export as GeoJSON | `ST_AsGeoJSON(boundary)` |
| `ST_GeomFromGeoJSON(json)` | Import from GeoJSON | `ST_GeomFromGeoJSON($1)` |
| `ST_Union(geom)` | Merge geometries | `ST_Union(route_segments)` |
| `ST_Centroid(geom)` | Center point of geometry | `ST_Centroid(state_boundary)` |

## Unit Conversion Reference

| From | To | Multiply By |
|------|-----|-------------|
| Miles | Meters | 1609.34 |
| Meters | Miles | 0.000621371 |
| Kilometers | Miles | 0.621371 |
| Miles | Kilometers | 1.60934 |

## Implementation Checklist

```
PostGIS Setup:
[ ] PostGIS extension enabled (CREATE EXTENSION postgis)
[ ] PGRouting extension enabled if routing needed (CREATE EXTENSION pgrouting)
[ ] SRID 4326 used for all GPS coordinate data
[ ] Geography type used for distance calculations

Geofences:
[ ] Geofences table with geography(Polygon, 4326) boundary column
[ ] GIST index on boundary column
[ ] Functions for geofence entry/exit detection
[ ] Event table for tracking geofence transitions

Spatial Indexes:
[ ] GIST index on all geography/geometry columns
[ ] Expression index on load_cognition for location queries
[ ] Partial indexes for valid coordinate rows only

Tracking:
[ ] load_cognition captures lat/lon with each update
[ ] Efficient queries for current fleet position
[ ] Historical track queries return ordered points
[ ] GeoJSON output for frontend consumption

Frontend Integration:
[ ] GeoJSON endpoints for facilities, geofences, fleet positions
[ ] LayerChart components for geographic visualizations
[ ] Real-time position updates via Supabase realtime subscriptions
```

## Related Skills

- **`supabase:laneweaver-database-design`**: Table conventions, audit columns, migrations
- **`layerchart`**: Geographic visualization components for frontend
- **`load-lifecycle-patterns`**: Load tracking status transitions

---

**Remember**: Use `geography` type for real-world distance calculations with GPS data. Always use SRID 4326 for GPS coordinates. Index all spatial columns with GIST indexes for query performance.
