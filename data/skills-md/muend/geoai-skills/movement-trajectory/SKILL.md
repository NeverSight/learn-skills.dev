---
name: movement-trajectory
description: >-
  Movement and trajectory analytics from GPS/GNSS tracks: cleaning, stop/trip
  detection, road-network map matching, speed/direction, flow aggregation,
  and origin-destination construction. Use for fleets, human mobility, animal
  tracking, AIS, or sports tracks. Trigger on GPS points, GPX, trajectories,
  stop detection, map matching, or timestamped positions per moving object.
  Also invoke for privacy, aggregation, de-identification, or release of
  individual trajectories. Use network-accessibility-analysis for
  hypothetical routes, isochrones, or static OD costs without observed tracks.
license: MIT
metadata:
  author: Muhammed Enes Duran
---

# Movement & Trajectory Analytics

Purpose: turn noisy timestamped points into defensible movement facts. The
recurring failure modes: **speed computed through GPS noise** (teleporting
points → 400 km/h pedestrians), **stops invented by signal drift**, and
**privacy-blind delivery** of individual-level traces.

## Data model first

A trajectory = ordered fixes per object: `(object_id, timestamp, x, y,
[accuracy, ...])`. Before analysis, report per object: fix count, time
span, median sampling interval, and interval distribution — **sampling
rate drives every method choice** (1 s vehicle traces and 1 fix/hour
animal tags are different problems wearing the same schema).

```python
import movingpandas as mpd
import geopandas as gpd

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat),
                       crs=4326).to_crs(gdf_utm_epsg)
tc = mpd.TrajectoryCollection(gdf, "object_id", t="timestamp")
```

### Declare CRS and time base before any threshold

Every distance radius, speed limit and dwell duration in this skill is
meaningless until two things are stated **in the answer, before the number is
used**:

1. **The projected CRS** all distance and speed computation runs in — a "50 m
   stop radius" applied to raw lon/lat degrees is not 50 m anywhere, and the
   error scales with latitude. Name the CRS (`estimate_utm_crs()` for a local
   fleet, an equal-distance projection for continental extents).
2. **The timestamp base**, normalised to timezone-aware UTC. Fleet logs mix
   local times, DST shifts and naive strings; a dwell that straddles a DST
   boundary gains or loses an hour, and stop durations silently corrupt.

State both before proposing a radius or duration, not afterwards as a caveat.

**Declaring is not withholding.** An unknown CRS or timezone is never grounds to
stop and ask instead of answering. State it as an explicit, named assumption and
deliver the method anyway:

> Assuming a local UTM zone for distance and that timestamps are naive local time
> needing UTC normalisation — confirm both, since they change dwell durations.

Then give the cleaning steps, the parameters, and the sensitivity check. A
response that asks for the CRS, the timezone, or the file *in place of* the
method has failed this skill even if the question is a good one. Ask alongside
the answer, never instead of it. Never silently treat naive timestamps as UTC —
but "silently" is the operative word: an assumption you have labelled and
surfaced is exactly what is wanted.

## Cleaning pipeline (in order)

1. **Deduplicate** identical (object, timestamp) fixes.
2. **Accuracy filter**: drop fixes above an HDOP/accuracy threshold if
   the column exists (report the threshold and % dropped).
3. **Speed filter**: drop fixes implying impossible speed for the mode
   (walk > 15 km/h sustained, car > 200 km/h...); iterate — one bad fix
   creates two bad segments (`mpd.OutlierCleaner`).
4. **Gap splitting**: split trajectories at temporal gaps (e.g., > 5×
   median interval) — interpolating across a tunnel/power-off invents
   movement.
5. Optional smoothing (Kalman/rolling median) for jittery urban-canyon
   data — AFTER outlier removal, and never before stop detection tuning.

Accounting line per step: fixes in → out.

## Stops and trips

Stop = spatial dwell: fixes within a distance radius for a minimum
duration (`mpd.TrajectoryStopDetector(max_diameter=50,
min_duration=timedelta(minutes=5))`). The two parameters ARE the result —
report them and run a ±50% sensitivity check; urban-canyon drift mimics
movement, so diameter < GPS noise level yields zero stops.

Trips = segments between stops. Deliver per trip: origin, destination,
start/end time, duration, length, main mode guess if applicable. OD
matrices: aggregate trip endpoints to zones (see privacy below);
accessibility questions on the resulting flows → `network-accessibility-analysis`.

## Map matching

Raw GPS does not sit on the road. For any road-referenced claim (distance
driven, street-level flows, speeding), match to the network first:

- Tools: Valhalla (Meili), OSRM `match`, or `mappymatch`; HMM-based
  matchers are the standard.
- Sampling interval > ~30 s degrades matching sharply — report match
  confidence and the % of unmatched points; don't silently keep unmatched
  geometry.
- Never map-match animal tracks or off-road movement (obviously) — and
  don't compute "distance traveled" from raw noisy fixes either
  (noise inflates path length ~5-20%); smooth first, state the method.

## Aggregate analytics

- **Flow maps / desire lines**: aggregate OD pairs before plotting
  (`cartography-geoviz` for delivery); hairball avoidance = zone-level
  aggregation + minimum-flow threshold.
- **Density**: KDE or hex-bin of fixes vs of trips — fixes overweight slow
  movement (dwell = many fixes); use trip-based or time-weighted density
  and say which.
- **Space-time clustering** (co-location, convoys): ST-DBSCAN family;
  cluster parameters in both space and time reported together.
- Sequence/periodicity: hour-of-day × day-of-week activity matrices per
  object class before any behavioral claims.

## Privacy — non-optional

Individual trajectories are personal data almost everywhere (GDPR etc.)
and are notoriously re-identifiable (home/work anchor pairs identify most
people). Defaults: aggregate before sharing (zones ≥ k objects,
suppress cells < k, typical k=5-10), truncate trip ends near homes,
and never publish raw individual traces without explicit clearance.
State the anonymization applied in every deliverable.

## Verification protocol

1. Speed histogram per mode after cleaning — tail must be physically
   plausible.
2. Map 3 sample trajectories (raw vs cleaned vs matched) over a basemap.
3. Stop-detection sensitivity: parameters ±50%, report stop-count change.
4. OD totals reconcile with trip counts (accounting).

## Pitfalls checklist

- Speeds computed across gaps or through outlier fixes.
- Distance traveled from raw (unsmoothed, unmatched) fixes.
- Stops detected with radius below GPS noise, or drift counted as trips.
- Mixed timezones / DST jumps creating phantom teleports.
- Fix-density maps read as movement-density maps.
- Individual traces shipped without aggregation/suppression.
- Trajectories split by object but not by temporal gap.

## Execution contract

- **Workflow:** validate identifiers, time, and CRS; segment tracks; remove impossible fixes; infer stops or trips; optionally map-match; aggregate; apply privacy controls; verify.
- **Decision rules:** use trajectory methods for observed timestamped movement, network analysis for possible routes or access, and point-pattern methods when sequence and identity are absent.
- **Verification protocol:** inspect speed and gap distributions, map raw-versus-cleaned samples, perturb stop parameters, reconcile trip and OD counts, and audit disclosure risk.
- **Failure modes:** suppress or qualify results for timezone ambiguity, long gaps, implausible speeds, poor network matching, sparse sampling, or re-identification risk.
- **Deliverables:** cleaned trajectories or approved aggregates, segmentation rules, quality report, derived stop/trip tables, privacy treatment, maps, and limitations.
- **Source freshness:** consult [the authoritative source registry](references/authoritative-sources.md) before using format, library, or privacy guidance and record the checked date.
