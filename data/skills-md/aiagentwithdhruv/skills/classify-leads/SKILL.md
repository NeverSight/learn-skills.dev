---
name: classify-leads
description: Classify leads using LLM for complex distinctions like product SaaS vs agencies. Use when user asks to classify leads, filter leads by type, or categorize businesses.
---

# LLM Lead Classification

## Goal
Classify leads using Claude for complex distinctions that keyword matching can't handle.

## When to Use
- Product SaaS vs IT consulting agencies
- High-ticket vs low-ticket businesses
- Subscription vs one-time payment models
- NOT for simple categories (dentists, realtors)

## Scripts
- `./scripts/classify_leads_llm.py` - Main classification script
- `./scripts/update_sheet.py` - Update sheets
- `./scripts/read_sheet.py` - Read from sheets

## Usage

```bash
python3 ./scripts/classify_leads_llm.py .tmp/leads.json \
  --classification_type product_saas \
  --output .tmp/classified_leads.json
```

## Performance
- ~2 minutes for 3,000 leads
- ~$0.30 per 1,000 leads
- Default: includes "unclear" classifications (medium confidence)

## Classification Types
- `product_saas`: Product companies vs service/consulting
- Custom types can be added

## Output
JSON file with classification added to each lead record.

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `leads_file` | file_path | Yes | JSON file with lead data |
| `classification_type` | string | Yes | Classification type (e.g., 'product_saas') |
| `output` | file_path | No | Output JSON file path |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `classified_file` | file_path | JSON file with classification added to each lead |

### Credentials
| Name | Source |
|------|--------|
| `ANTHROPIC_API_KEY` | .env |

### Composable With
Skills that chain well with this one: `scrape-leads`, `gmaps-leads`, `instantly-campaigns`

### Cost
$0.30 per 1,000 leads
