---
name: fabric-icons
description: Search and fetch official Microsoft Fabric / Azure SVG icons for use in diagrams, documentation, and UI. Use when building architecture diagrams (HTML, PPTX, or any visual format) that need icons for Fabric concepts like Lakehouse, Data Warehouse, Pipeline, Eventhouse, Power BI, OneLake, Dataflow, Notebook, Semantic Model, KQL Database, and other Fabric items. Also use when the user asks for Microsoft Fabric or Azure data platform icons.
---

# Fabric Icons

175 official Microsoft Fabric SVG icons with metadata.

## Finding Icons

Run the search script instead of reading the full index (saves context):

```bash
python3 scripts/search_icons.py "<query>" [limit]
```

Examples:
```bash
python3 scripts/search_icons.py "lakehouse"
python3 scripts/search_icons.py "pipeline" 5
python3 scripts/search_icons.py "streaming kql"
```

Returns matching icons as JSON with `id`, `name`, `description`, `tags`, and `url`. Use the `url` field directly as an image source.

For bulk operations or browsing all icons, read `references/index.json`.

### Index Entry Format

```json
{
  "id": "lakehouse",
  "name": "Lakehouse",
  "description": "Lakehouse database built over a data lake for big data processing with Apache Spark and SQL",
  "tags": ["data", "lakehouse", "storage"],
  "filename": "lakehouse_48_item.svg",
  "url": "https://raw.githubusercontent.com/AlahmadiQ8/icons/main/icons/lakehouse_48_item.svg"
}
```

## Using Icons in HTML Diagrams

```html
<img src="https://raw.githubusercontent.com/AlahmadiQ8/icons/main/icons/lakehouse_48_item.svg"
     alt="Lakehouse" width="48" height="48" />
```

## Using Icons in PPTX

Download the SVG from the `url` and add it as a picture:

```python
from pptx import Presentation
from pptx.util import Inches
import urllib.request, tempfile, os

url = "https://raw.githubusercontent.com/AlahmadiQ8/icons/main/icons/lakehouse_48_item.svg"
tmp = tempfile.NamedTemporaryFile(suffix=".svg", delete=False)
urllib.request.urlretrieve(url, tmp.name)

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.shapes.add_picture(tmp.name, Inches(1), Inches(1), Inches(1), Inches(1))
os.unlink(tmp.name)
```

## Common Icon IDs

Key Fabric items: `lakehouse`, `data_warehouse`, `pipeline`, `notebook`, `dataflow_gen2`, `eventstream`, `event_house`, `kql_database`, `semantic_model`, `report`, `dashboard`, `sql_database`, `spark_job_direction`, `model`, `experiments`, `environment`, `copilot`, `reflex`, `datamart`, `copy_job`

Workloads: `fabric`, `data_engineering`, `data_factory`, `data_science`, `real_time_intelligence`, `power_bi`, `databases`, `industry_solutions`

Storage: `one_lake`, `lakehouse`, `data_warehouse`, `sql_database`
