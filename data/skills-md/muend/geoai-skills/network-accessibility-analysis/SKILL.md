---
name: network-accessibility-analysis
description: >-
  Always invoke for access to facilities or opportunities by walking,
  driving, cycling, or public transport, even for a conceptual question with
  no routing terms or data yet. Covers hospital and service access,
  transit/GTFS, routes, isochrones, OD matrices, closest facility, 2SFCA,
  walkability, coverage, and equity. Invoke when Euclidean buffers proxy for
  network access. Use movement-trajectory for observed tracks and MCDA for
  suitability without network costs.
license: MIT
metadata:
  author: Muhammed Enes Duran
---

# Network & Accessibility Analysis

Purpose: replace as-the-crow-flies guesswork with network-true travel
costs, at the right scale and with honest assumptions about speeds and
modes. First decision on every task: Euclidean distance is only acceptable
as a declared approximation — flag it whenever you see it standing in for
access.

## Tool selection by scale

| Scale | Tool |
|---|---|
| Neighborhood-city, research flexibility | **OSMnx + NetworkX** |
| City-region, many-to-many OD (>10⁴×10⁴) | **r5py** (multimodal + transit w/ GTFS) or **pandana** (contraction-hierarchy speed) |
| Production routing service | Valhalla / OSRM / OpenRouteService API |
| Proprietary stacks | ArcGIS Network Analyst (script it headlessly) |

NetworkX chokes on metro-scale many-to-many — don't loop `shortest_path`
over thousands of origins; switch tools instead.

## Graph construction (OSMnx)

```python
import osmnx as ox

G = ox.graph_from_place("City, Country", network_type="drive")  # walk/bike/all
G = ox.add_edge_speeds(G)          # imputes from highway tags where maxspeed missing
G = ox.add_edge_travel_times(G)    # edge attr: travel_time (s)
G = ox.project_graph(G)            # metric CRS before any distance work
```

- **network_type matters**: pedestrian analysis on a `drive` graph misses
  paths, stairs, plazas; driving on `all` uses footpaths. Match mode.
- Imputed speeds are averages by road class — a systematic bias, not
  noise. State it; calibrate against known trips when stakes are high.
- Keep the strongly connected component for routing
  (`ox.truncate.largest_component(G, strongly=True)`); orphan islands
  cause spurious infinities.
- **Snapping**: origins/destinations map to nearest nodes/edges
  (`ox.distance.nearest_nodes`). Report the snap-distance distribution;
  a facility snapped 2 km away (riverside, gated area) silently corrupts
  results.

## Core products

- **Isochrones / service areas**: ego-graph by travel_time cutoff → alpha
  shape or buffered edge union around reached edges. Node-based convex
  hulls overstate coverage across rivers/highways — prefer edge-based
  polygons. Always label the assumptions: mode, speed model, cutoff.
- **OD matrix**: many-to-many travel costs; the substrate for
  accessibility and location-allocation. For big matrices use
  pandana/r5py; store as Parquet with origin/destination IDs.
- **Closest facility**: k-nearest by network cost (not Euclidean); report
  both the assigned facility and the cost.
- **Centrality**: betweenness on travel_time (sampled `k` for big
  graphs — exact is O(nm)); edge betweenness ≈ through-traffic potential.
  Interpret as network structure, not observed traffic.

## Accessibility metrics — pick deliberately

| Metric | Question it answers | Weakness |
|---|---|---|
| Cumulative opportunities (# jobs/POIs within T min) | Simple, communicable | Cliff at T; all-or-nothing |
| Gravity-based (distance-decayed sum) | Smooth access | Decay parameter must be justified |
| **2SFCA / E2SFCA** | Supply-demand ratio access (health care standard) | Catchment size choice drives results |
| Closest-facility time | Worst-case need | Ignores capacity/congestion |

For equity analyses, join metrics to population/demographic polygons
(area-weighted or dasymetric — see `geo-data-engineering`) and report
distributions per group, not just city means. Route statistical testing of
disparities to `spatial-statistics`.

## Location-allocation

Optimal siting (p-median, max-coverage) on the OD matrix: formulate with
PuLP/OR-Tools; inputs are the OD matrix + demand weights + candidate
sites. State the objective explicitly — minimize mean travel time
(p-median) vs maximize covered demand within T (max-coverage) give
different answers, and stakeholders rarely know which they asked for.
Feed results back to `mcda-suitability-analysis` when siting mixes network
access with other criteria.

## Transit (GTFS)

Use r5py with OSM + GTFS feeds; results are departure-time sensitive —
compute over a time window (e.g., 07:00-09:00 percentiles), never a single
departure. Validate the feed (calendar coverage on your analysis date!) —
an expired GTFS calendar yields walking-only times that look plausible.

## Verification protocol

1. Spot-check 3 routes against an external router (Google/OSRM) — within
   ~20% or explain why.
2. Map unreachable/infinite-cost pairs — usually snapping or connectivity
   artifacts, not real inaccessibility.
3. Isochrone eyeball: does it respect rivers, highways, one-ways?

## Pitfalls checklist

- Euclidean buffers presented as "service areas".
- Wrong network_type for the mode.
- Convex-hull isochrones bridging barriers.
- Snap distances unchecked.
- One departure time for transit accessibility.
- Betweenness sold as traffic volume.
- OD matrix in degrees-CRS travel "distances".

## Execution contract

- **Workflow:** define mode, time, impedance, origins, destinations, and equity question; build and validate the network; snap inputs; compute routes or matrices; summarize access; verify.
- **Decision rules:** use network costs for constrained travel, movement analytics for observed tracks, and MCDA only when accessibility becomes one criterion in a broader preference model.
- **Verification protocol:** audit connectivity and snapping, spot-check routes, map unreachable pairs, test departure-time or impedance sensitivity, and reconcile OD dimensions and units.
- **Failure modes:** withhold access claims for disconnected graphs, wrong mode or turn rules, expired GTFS service, excessive snapping, Euclidean substitution, or unstable departure-time results.
- **Deliverables:** network provenance, assumptions and cost function, routes or OD matrix, isochrones or access metrics, unreachable-case report, validation evidence, and equity caveats.
- **Source freshness:** consult [the authoritative source registry](references/authoritative-sources.md) before using network, GTFS, or routing APIs and archive source dates.
