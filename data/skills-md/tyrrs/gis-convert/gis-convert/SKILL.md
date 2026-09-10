---
name: gis-convert
description: Convert GIS data between vector, geodatabase, CAD, point-cloud, and practical 3D formats with CRS checks. Use for WKT, GeoJSON, SHP, GDB, MDB, DXF/DWG, LAS/LAZ, CityGML, 3D Tiles, I3S, glTF/OBJ, and related workflows.
---

# gis-convert

## Purpose

Use this skill by calling the bundled CLI. The CLI owns format detection, driver mapping, CRS flags, CSV WKT handling, ESRIJSON output, and land-boundary TXT handling.

## Script Entry

`<skill-root>` is the directory that contains this `SKILL.md`. The conversion script belongs to `<skill-root>`, not to the user's data directory.

```bash
python <skill-root>/scripts/gis_convert.py --input /absolute/input --output /absolute/output --overwrite
```

Use absolute paths for user input and output files whenever possible. Never assume `scripts/gis_convert.py` exists under the user's current data folder.

## Required Arguments

| Argument | Value | Rule |
|---|---|---|
| `--input` | File or dataset path | Required unless using `--list-formats`; prefer an absolute path. |
| `--output` | File or dataset path | Required unless using `--list-formats`; prefer an absolute path. |

## Optional Arguments

| Argument | Value | Default / Rule |
|---|---|---|
| `--from-format` | Format value | Override input format only when suffix inference is wrong. |
| `--to-format` | Format value | Override output format only when suffix inference is wrong or ambiguous. |
| `--source-crs` | CRS string | Use values such as `EPSG:3857`; overrides missing or wrong input CRS. |
| `--target-crs` | CRS string | Use only when reprojection is requested. |
| `--layer` | Layer name | Use for multi-layer data sources. |
| `--geometry-column` | CSV WKT column name | Default: `wkt`. Used for CSV input and output. |
| `--encoding` | Text encoding | Used for TXT/CSV input or output; common value: `gb18030`. |
| `--landtxt-meta` | `KEY=VALUE` | Repeatable. Used only for land-boundary TXT output. |
| `--overwrite` | Flag | Required when replacing an existing output path. |
| `--validate-only` | Flag | Validate the request without writing output. |
| `--list-formats` | Flag | Print local OGR driver capabilities. |

## Format Values

Use these values with `--from-format` or `--to-format` when an override is needed:

| User value / alias | Normalized format |
|---|---|
| `geojson`, `json`, `geojosn` | GeoJSON |
| `wkt` | WKT |
| `csv` | CSV with a WKT geometry column |
| `esrijson`, `esri json` | ESRIJSON |
| `land-boundary-txt`, `txt`, `勘测定界txt`, `勘测定界` | Land-boundary TXT |
| `shp`, `shapefile`, `esri-shapefile` | ESRI Shapefile |
| `gpkg`, `geopackage` | GeoPackage |
| `gdb`, `filegdb`, `openfilegdb` | OpenFileGDB |
| `kml`, `kmz` | KML / LIBKML |
| `dxf` | DXF |
| `dwg`, `cad` | CAD/DWG |
| `mdb`, `pgeo`, `personal gdb` | Personal GDB / MDB |
| `las`, `laz`, `e57`, `ply` | Point-cloud formats |

## Suffix Inference

If `--to-format` is omitted, the CLI infers output format from `--output` suffix:

`.geojson`, `.json`, `.wkt`, `.csv`, `.esrijson`, `.txt`, `.kml`, `.kmz`, `.gdb`, `.gpkg`, `.dxf`, `.dwg`, `.mdb`, `.shp`, `.las`, `.laz`, `.e57`, `.ply`.

Use `--to-format land-boundary-txt` for land-boundary TXT output when `.txt` could be ambiguous. Use `--to-format esrijson` when output suffix is `.json` but the requested format is Esri JSON, not GeoJSON.

## Special Parameters

- CSV input must contain the WKT geometry column named by `--geometry-column`; CSV output writes attributes plus that WKT column.
- Land-boundary TXT output accepts repeated metadata overrides such as `--landtxt-meta 坐标系=2000国家大地坐标系` and `--landtxt-meta 带号=39`.
- Use `--encoding gb18030` for Chinese TXT/CSV files that are not UTF-8.
- Land-boundary TXT output is for polygon or multipolygon features; use CSV WKT or GeoJSON for point/line data.

## CRS Rules

- If `--target-crs` is omitted, the CLI keeps the input CRS.
- If input CRS cannot be read and coordinates look like longitude/latitude, the CLI assigns `EPSG:4326`.
- Use `--source-crs` when the input CRS is missing or wrong.
- Use `--target-crs` only when reprojection is requested.

## Error Handling

Run the CLI first and report its stderr/stdout clearly if conversion fails. Do not bypass this CLI with lower-level tools. If a request is ambiguous, ask for the missing output format, CRS, layer, encoding, or CSV geometry column.
