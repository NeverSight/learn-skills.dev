---
name: architectural-drawing-parser
description: >-
  Parse architectural drawings, floor plans, and building code compliance documents using
  Vision AI. Extracts building type, occupancy, floor areas, room layouts, dimensions,
  and code parameters. Use when: reading PDF floor plans, analyzing architectural drawings,
  extracting building data from images or scanned documents.
license: Apache-2.0
compatibility: "Python 3.9+ with the anthropic package, or Node.js 20+ with @anthropic-ai/sdk; ANTHROPIC_API_KEY set. Optional: poppler-utils (pdftoppm)."
metadata:
  author: terminal-skills
  version: "1.1.0"
  category: design
  tags: "architecture, vision-ai, floor-plan, building-codes, pdf-parsing"
---

# Architectural Drawing Parser

## Overview

Vision AI pipeline to extract structured building data from architectural drawings, floor plans, and IBC/IRC code compliance documents. Uses Claude's vision capabilities to read and interpret professional drawings, returning a normalized JSON object suitable for downstream 3D modeling or code validation workflows.

Supports IBC occupancy types (A-1 through U), construction types (I-A through V-B), sprinkler systems (NFPA 13/13R/13D), building dimensions, unit breakdowns, egress data, and floor plan elements (rooms, walls, doors, windows).

## Instructions

### Supported Drawing Types

| Drawing Type | What Is Extracted |
|---|---|
| IBC/IRC code compliance drawings | Occupancy, construction type, heights, stories, areas, egress, units |
| Floor plans (unit-level) | Rooms, dimensions, wall layouts, door/window positions |
| Site plans | Building footprint, setbacks, parking |
| Building area analysis tables | Unit types, SF per unit, occupant loads, travel distances |

### Output Data Structure

The parser returns a `BuildingData` JSON object with these fields:

- **occupancy** -- IBC occupancy type (e.g., "R-2", "A-2", "B")
- **constructionType** -- IBC construction type (e.g., "V-B", "I-A")
- **sprinklerSystem** -- "NFPA 13", "NFPA 13R", "NFPA 13D", or "None"
- **stories** -- `{ permitted, actual }`
- **height** -- `{ permitted: { feet, meters }, actual: { feet, meters } }`
- **totalBuildingArea** -- `{ sqft, sqm }`
- **units** -- Array of `{ name, area: { sqft, sqm }, occupantLoad, loadFactor, count }`
- **travelDistances** -- Array of `{ floor, maximum: { feet, meters } }`
- **scale** -- Scale notation string (e.g., `1/16" = 1'-0"`)
- **rooms** -- Array of `{ name, type, estimatedArea, dimensions }` (floor plans only)

### Parsing Approach

1. Send the drawing to Claude's vision API with a structured extraction prompt: put the image (or PDF) block first and the instructions after it
2. Request all building data as a single JSON object and state the schema in the prompt
3. Convert all areas to both sqft and sqm (1 sqft = 0.0929 sqm)
4. Convert all distances to both feet and meters (1 foot = 0.3048 m)
5. Parse the JSON from the response text and reject the result if required fields are missing

```python
import anthropic, base64, json, pathlib

client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from the environment
page = base64.standard_b64encode(pathlib.Path("A-101-level-1.jpg").read_bytes()).decode()

message = client.messages.create(
    model="claude-opus-5-5",     # any current vision-capable Claude model
    max_tokens=4096,
    messages=[{"role": "user", "content": [
        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": page}},
        {"type": "text", "text": "Extract occupancy, constructionType, sprinklerSystem, stories, height, "
            "totalBuildingArea, units, travelDistances, scale and rooms from this drawing. Give areas in sqft and sqm, "
            "distances in feet and meters. Use null for anything not shown. Reply with one JSON object only."},
    ]}],
)
building = json.loads(message.content[0].text)
```

For a whole PDF set, send it as a `document` block (base64 or a Files API `file_id`) instead of an image; the API takes up to 32 MB and 100 pages per request on 200k-context models (600 on 1M-context models). Per image, the limits are 10 MB and 8000x8000 px, and images are downscaled to a 1568 px long edge on standard models (2576 px on Claude 4.7 and later), so tiny dimension text on a large sheet can be lost.

### Best Practices

- Use 150 DPI or higher for scanned drawings; keep text legible after the long edge is capped
- JPEG or PNG; for sheets with dense notes convert PDFs to images and crop to the table or plan area (`pdftoppm -png -r 200 -f 3 -l 3 drawing.pdf sheet`)
- Process multi-sheet PDFs one page at a time, then merge results
- Label each image ("Sheet A-101:") when sending several in one request
- Treat dimensions read from linework as approximate: prefer dimensions printed on the sheet over measuring from the scale
- Always verify extracted data against the source before structural calculations

## Examples

### Example 1: Parsing a Floor Plan PDF

A developer receives a scanned floor plan of a 2-bedroom apartment unit and needs room dimensions for a renovation estimate.

```
Input: apartment_unit_plan.jpg (scanned at 200 DPI, 1/4" = 1'-0" scale)

Extracted JSON:
{
  "rooms": [
    { "name": "Living Room", "type": "living", "estimatedArea": { "sqft": 240, "sqm": 22.3 }, "dimensions": { "width": 16, "depth": 15, "units": "feet" } },
    { "name": "Kitchen", "type": "kitchen", "estimatedArea": { "sqft": 120, "sqm": 11.1 }, "dimensions": { "width": 12, "depth": 10, "units": "feet" } },
    { "name": "Master Bedroom", "type": "bedroom", "estimatedArea": { "sqft": 168, "sqm": 15.6 }, "dimensions": { "width": 14, "depth": 12, "units": "feet" } },
    { "name": "Bedroom 2", "type": "bedroom", "estimatedArea": { "sqft": 132, "sqm": 12.3 }, "dimensions": { "width": 12, "depth": 11, "units": "feet" } },
    { "name": "Bathroom", "type": "bathroom", "estimatedArea": { "sqft": 48, "sqm": 4.5 }, "dimensions": { "width": 8, "depth": 6, "units": "feet" } }
  ],
  "scale": "1/4\" = 1'-0\""
}
```

The developer uses the room dimensions to calculate material quantities for flooring (708 sqft total) and wall paint coverage.

### Example 2: Extracting Building Data from an IBC Compliance Drawing

An architect submits a code compliance sheet for a 3-story apartment building. The parser extracts all building classification and egress data.

```
Input: ibc_compliance_sheet.jpg (building area analysis table + egress diagram)

Extracted JSON:
{
  "occupancy": "R-2",
  "constructionType": "V-B",
  "sprinklerSystem": "NFPA 13",
  "stories": { "permitted": 4, "actual": 3 },
  "height": {
    "permitted": { "feet": 60, "meters": 18.29 },
    "actual": { "feet": 35, "meters": 10.67 }
  },
  "totalBuildingArea": { "sqft": 8910, "sqm": 827.9 },
  "units": [
    { "name": "Type A", "area": { "sqft": 834, "sqm": 77.5 }, "occupantLoad": 5, "loadFactor": "1/200 SF", "count": 6 },
    { "name": "Type B", "area": { "sqft": 645, "sqm": 59.9 }, "occupantLoad": 4, "loadFactor": "1/200 SF", "count": 6 }
  ],
  "travelDistances": [
    { "floor": "Level 1", "maximum": { "feet": 66, "meters": 20.1 } },
    { "floor": "Level 2", "maximum": { "feet": 66, "meters": 20.1 } },
    { "floor": "Level 3", "maximum": { "feet": 66, "meters": 20.1 } }
  ]
}
```

This data feeds into the `ibc-building-codes` skill for compliance validation and the `spec-to-3d` skill for 3D model generation.

## Guidelines

- Accuracy depends on drawing quality and image resolution; low-res scans may produce incorrect dimensions
- Very small text (title blocks, fine notes) may be misread -- zoom in for detail drawings
- Complex overlapping hatching or linework may confuse room detection
- Proprietary symbols or non-standard abbreviations may not be recognized
- Always treat extracted data as an estimate; verify critical measurements manually
- For multi-sheet sets, parse each sheet separately and merge the structured data
- Permitted stories, heights and areas depend on the IBC edition and local amendments; read them from the sheet rather than inferring them from the occupancy and construction type
- The parser works best with US-standard architectural drawings; metric-only drawings may need prompt adjustments
