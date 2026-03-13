---
name: title-variants
description: Generate title variants for YouTube videos from outlier analysis. Use when user asks to create title variations, generate YouTube titles, or adapt video titles.
---

# Title Variant Generation

## Goal
Analyze top-performing video titles and generate variants adapted to your niche.

## Scripts
- `./scripts/generate_title_variants.py` - Generate variants
- `./scripts/update_sheet.py` - Update sheets

## Usage

```bash
# Mode A: Update existing sheet with variants
python3 ./scripts/generate_title_variants.py \
  --sheet-url "SHEET_URL" \
  --mode update

# Mode B: Create new sheet with variants
python3 ./scripts/generate_title_variants.py \
  --input .tmp/outliers.json \
  --mode create
```

## How It Works
1. Analyzes original title's hook, emotional trigger, structure
2. Adapts to your specific niche (AI agents, automation, etc.)
3. Generates 3 meaningfully different variants
4. Keeps under 100 characters (YouTube best practice)

## Configuration
```python
USER_CHANNEL_NICHE = "AI agents, automation, LangGraph, CrewAI, agentic workflows"
```

## Output
Three title variants per input, stored in sheet columns:
- Title Variant 1
- Title Variant 2
- Title Variant 3

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sheet_url` | string | No | Google Sheet with outlier titles to generate variants for |
| `input_file` | file_path | No | JSON file with outlier data |
| `mode` | string | Yes | 'update' (existing sheet) or 'create' (new sheet) |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `sheet_url` | string | Sheet with Title Variant 1/2/3 columns added |

### Credentials
| Name | Source |
|------|--------|
| `ANTHROPIC_API_KEY` | .env |

### Composable With
Skills that chain well with this one: `cross-niche-outliers`, `youtube-outliers`

### Cost
Claude API (minimal)
