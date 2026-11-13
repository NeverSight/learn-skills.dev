---
name: synthetic-data-generation
description: "Generate realistic synthetic oil & gas data (LAS well logs, SEG-Y seismic, core photos, time-series) with proper physical constraints for testing, demos, and training."
---

# Synthetic Data Generator

Natural language interface for generating realistic oil & gas domain data.

## Purpose

Generate synthetic well logs (LAS/DLIS), seismic (SEG-Y), core photos, and time-series data with proper physical constraints for testing, demos, and training.

## Capabilities

Generate data with realistic relationships:
- Well logs (GR, RHOB, NPHI, RT, DT) with Archie equation constraints
- Seismic volumes with proper geometry
- OSDU-compliant metadata
- Core photos using AI image generation (requires API key, expensive operation)

## Invoking

```python
from synthetic_data.well_log import LASGenerator
from synthetic_data.seismic import SEGYGenerator
```

## Well Log Generation

Create realistic LAS files:

```python
generator = LASGenerator(seed=42)
las_path = generator.create_record(
    well_name="Test-Well-001",
    curves=["GR", "RHOB", "NPHI", "RT"],
    depth_range=(1000.0, 2000.0),
    sample_interval=0.15,
    lithology="sandstone"
)
```

Options:
- `well_name`: Well identifier
- `curves`: Log curves to generate (GR, RHOB, NPHI, RT, DT, CALI)
- `depth_range`: (start, end) in meters
- `sample_interval`: Sampling interval in meters
- `lithology`: sandstone | shale | carbonate
- `seed`: Random seed for reproducibility

## Seismic Generation

Create SEG-Y volumes:

```python
generator = SEGYGenerator(seed=42)
segy_path = generator.create_record(
    survey_name="Test-Survey",
    n_inlines=100,
    n_crosslines=100,
    n_samples=500,
    sample_interval=4000  # microseconds
)
```

## Core Photo Generation

**IMPORTANT: Expensive Operation**

Core photo generation uses AI image generation APIs which are costly. Before generating:
1. **Always ask for count** - Never generate without explicit number confirmation
2. **Ask about aspects** based on detail level needed

### Mandatory Questions

When user requests core photos, ask these in order:

**Question 1 - Count:**
> "How many core photos do you need? (Image generation is expensive - each photo costs API credits)"

**Question 2 - Lithology:**
> "What lithology? (A) Sandstone (B) Shale (C) Carbonate (D) Limestone (E) Dolomite (F) Mixed/varies"

**Question 3 - Visual Features (if user wants detail):**
> "Any specific visual features? (A) Default/random (B) With fractures (C) With oil staining (D) Specific bedding angles (E) Let me specify"

**Question 4 - Full Context (if user wants geological accuracy):**
> "Need full geological context? If yes, specify: depth range, formation name, field name, well naming convention"

### Usage

```python
from synthetic_data.core_photos import CorePhotoGenerator

generator = CorePhotoGenerator(api_key="YOUR_GOOGLE_AI_API_KEY")
result = generator.create_record(
    well_name="Test-Well-001",
    lithology="sandstone",
    depth_range=(1000.0, 2000.0),
    output_dir="./output"
)
```

Options:
- `well_name`: Well identifier
- `lithology`: sandstone | shale | carbonate | limestone | dolomite
- `depth_range`: (start, end) in meters
- `core_length`: Length of core sample in meters (default: 1.0)
- `field_name`: Field name for metadata
- `formation`: Formation name for metadata
- `output_dir`: Directory to save images and metadata

### Example Assets

Reference examples available at `synthetic_data/assets/`:
- `core-photos.png` - Real core sample photographs showing proper format
- `core-photos.webp` - WebP version

These show proper format: depth markers, well identification, lithology variations, and scale bars.

## Validation

Files validate against domain libraries:
- LAS → lasio
- SEG-Y → segyio
- DLIS → dlisio

## OSDU Integration

Generate manifests for OSDU:

```python
from synthetic_data.osdu import LASMapper

mapper = LASMapper()
manifest = mapper.to_manifest(
    las_path,
    legal_tags={"legaltags": ["test-license"]}
)
```

## Example Usages

User says:
```
"Generate 5 LAS files for testing"
```

→ Uses LASGenerator.create_dataset(n_records=5)

User says:
```
"Create realistic well log with GR, RHOB, NPHI for carbonate formation"
```

→ Uses lithology="carbonate"

User says:
```
"Generate well log data with OSDU manifests for demo deployment"
```

→ Creates LAS files + OSDU-compliant JSON manifests

User says:
```
"Generate core photos for testing"
```

→ Ask: "How many?" then "What lithology?" then generate

User says:
```
"I need 5 sandstone core photos with visible fractures"
```

→ Confirms count (5), lithology (sandstone), feature (fractures) → generate

User says:
```
"Generate synthetic data for my reservoir project"
```

→ Ask: "What type of data? (well logs, seismic, core photos, production data)"
→ If core photos selected, proceed with mandatory questions

## Software Tasks

If user requests:
- Full OSDU ingestion pipeline → invoke `petropowers:oil-gas-delegation`
- Real-time data generation → Explain this is batch-only
- Proprietary format support → Explain only open standards (LAS, SEG-Y, DLIS) supported

## Dependencies

```
pip install lasio welly dlisio segyio numpy pandas scipy
```

## Reference Documentation

See `references/physical-constraints.md` for detailed petrophysical relationships.